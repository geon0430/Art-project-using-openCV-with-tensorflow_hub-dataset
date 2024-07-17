document.addEventListener("DOMContentLoaded", function() {
    const contentInput = document.getElementById("content");
    const styleInput = document.getElementById("style");
    const modal = document.getElementById("custom-modal");
    const closeModal = document.getElementsByClassName("close")[0];
    const localVideo = document.getElementById("localVideo");
    const emojiButton = document.getElementsByClassName("emoji-button")[0];
    const uploadedImageContainer = document.getElementById("uploaded-image-container");
    const uploadedImage = document.getElementById("uploaded-image");
    const selectedImageContainer = document.getElementById("selected-image-container");
    const selectedImage = document.getElementById("selected-image");
    const resultModal = document.getElementById("result-modal");
    const closeResultModal = document.getElementById("close-result-modal");
    const resultImageModal = document.getElementById("result-image-modal");
    const qrContainer = document.getElementById("qr-container");
    const qrImage = document.getElementById("qr-image");

    let pc = null;
    let localStream = null;

    modal.style.display = "none";
    resultModal.style.display = "none";

    async function startWebcam() {
        try {
            if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
                alert("Your browser does not support webcam access. Please use a different browser.");
                return;
            }

            if (!localStream) {
                localStream = await navigator.mediaDevices.getUserMedia({ video: true });
                localVideo.srcObject = localStream;
            }

            if (!pc) {
                pc = new RTCPeerConnection();
                localStream.getTracks().forEach(track => pc.addTrack(track, localStream));

                const offer = await pc.createOffer();
                await pc.setLocalDescription(offer);

                const response = await fetch('/offer/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        sdp: pc.localDescription.sdp,
                        type: pc.localDescription.type
                    })
                });

                const answer = await response.json();
                if (answer.error) {
                    throw new Error(answer.error);
                }
                await pc.setRemoteDescription(new RTCSessionDescription(answer));
            }
        } catch (error) {
            console.error("Error accessing webcam: ", error);
            alert("Error accessing webcam: " + error.message);
        }
    }

    function captureScreenshot() {
        const canvas = document.createElement('canvas');
        canvas.width = localVideo.videoWidth;
        canvas.height = localVideo.videoHeight;
        const context = canvas.getContext('2d');
        context.drawImage(localVideo, 0, 0, canvas.width, canvas.height);

        canvas.toBlob(async function(blob) {
            const formData = new FormData();
            formData.append('image', blob, 'screenshot.jpg');

            try {
                const response = await fetch('/save_screenshot/', {
                    method: 'POST',
                    body: formData
                });

                if (!response.ok) {
                    throw new Error('Failed to save screenshot');
                }

                const result = await response.json();
                console.log(result);

                const imageUrl = URL.createObjectURL(blob);
                uploadedImage.src = imageUrl;
                uploadedImage.style.display = "block"; 
                uploadedImageContainer.style.display = "block";

                localStorage.setItem('content_image_path', result.image_path);

                modal.style.display = "none";
            } catch (error) {
                console.error('Error uploading screenshot:', error);
                alert('Error uploading screenshot: ' + error.message);
            }
        }, 'image/jpg');
    }

    uploadedImageContainer.onclick = function() {
        modal.style.display = "flex";
        startWebcam();
    }

    selectedImageContainer.onclick = function() {
        styleInput.click();
    }

    styleInput.onchange = async function(event) {
        const file = event.target.files[0];
        if (file) {
            const formData = new FormData();
            formData.append('image', file);

            try {
                const response = await fetch('/save_screenshot/', {
                    method: 'POST',
                    body: formData
                });

                if (!response.ok) {
                    throw new Error('Failed to save style image');
                }

                const result = await response.json();
                console.log(result);

                selectedImage.src = URL.createObjectURL(file);
                selectedImage.style.display = "block";
                selectedImageContainer.style.display = "block";

                localStorage.setItem('style_image_path', result.image_path);
            } catch (error) {
                console.error('Error uploading style image:', error);
                alert('Error uploading style image: ' + error.message);
            }
        }
    }

    closeModal.onclick = function() {
        modal.style.display = "none";
    }

    closeResultModal.onclick = function() {
        resultModal.style.display = "none";
        // 초기화 코드 추가
        localStorage.removeItem('content_image_path');
        localStorage.removeItem('style_image_path');
        uploadedImage.src = "";
        uploadedImage.style.display = "none";
        selectedImage.src = "";
        selectedImage.style.display = "none";
        // 파일 입력 초기화
        contentInput.value = null;
        styleInput.value = null;
    }

    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
        if (event.target == resultModal) {
            resultModal.style.display = "none";
            // 초기화 코드 추가
            localStorage.removeItem('content_image_path');
            localStorage.removeItem('style_image_path');
            uploadedImage.src = "";
            uploadedImage.style.display = "none";
            selectedImage.src = "";
            selectedImage.style.display = "none";
            // 파일 입력 초기화
            contentInput.value = null;
            styleInput.value = null;
        }
    }

    emojiButton.onclick = function() {
        captureScreenshot();
    }

    document.getElementById('upload-form').onsubmit = async function(event) {
        event.preventDefault();

        const contentPath = localStorage.getItem('content_image_path');
        const stylePath = localStorage.getItem('style_image_path');

        if (!contentPath || !stylePath) {
            alert("Both images are required.");
            return;
        }

        const formData = new FormData();
        formData.append('content_path', contentPath);
        formData.append('style_path', stylePath);

        try {
            const response = await fetch('/predict/', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error('Failed to process images');
            }

            const result = await response.json();
            console.log(result);

            resultImageModal.src = `/saved_images/${result.result_image_filename}`;
            resultModal.style.display = "flex";

            const qrResponse = await fetch(`/generate_qr/${result.result_image_filename}`);
            if (!qrResponse.ok) {
                throw new Error('Failed to generate QR code');
            }
            const qrResult = await qrResponse.json();
            qrImage.src = `/${qrResult.qr_code_path}`;
            qrContainer.style.display = "block";
        } catch (error) {
            console.error('Error processing images:', error);
            alert('Error processing images: ' + error.message);
        }
    }
});
