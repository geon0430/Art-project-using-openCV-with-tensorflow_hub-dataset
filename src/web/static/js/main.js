function showResults(event) {
    event.preventDefault();
    const form = document.getElementById('upload-form');
    const formData = new FormData(form);

    fetch('/predict/', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('content-image').src = '/uploads/' + data.content_path.split('/').pop();
        document.getElementById('style-image').src = '/uploads/' + data.style_path.split('/').pop();
        document.getElementById('output-image').src = '/results/output.jpg';
        
        document.getElementById('results').style.display = 'block';
        document.getElementById('content-container').style.display = 'inline-block';
        document.getElementById('style-container').style.display = 'inline-block';
        document.getElementById('output-container').style.display = 'inline-block';
    })
    .catch(error => console.error('Error:', error));
}
