document.addEventListener("DOMContentLoaded", function() {
    const uploadPhotoButton = document.getElementById("upload-photo-button");
    const contentInput = document.getElementById("content");
    const modal = document.getElementById("custom-modal");
    const closeModal = document.getElementsByClassName("close")[0];
    const localVideo = document.getElementById("localVideo");

    let pc = null;
    let localStream = null;

    async function startWebcam() {
        localStream = await navigator.mediaDevices.getUserMedia({ video: true });
        localVideo.srcObject = localStream;
        
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
        await pc.setRemoteDescription(new RTCSessionDescription(answer));
    }

    uploadPhotoButton.onclick = function() {
        modal.style.display = "block";
        startWebcam();
    }

    closeModal.onclick = function() {
        modal.style.display = "none";
        if (localStream) {
            localStream.getTracks().forEach(track => track.stop());
        }
        if (pc) {
            pc.close();
        }
    }

    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
            if (localStream) {
                localStream.getTracks().forEach(track => track.stop());
            }
            if (pc) {
                pc.close();
            }
        }
    }
});
