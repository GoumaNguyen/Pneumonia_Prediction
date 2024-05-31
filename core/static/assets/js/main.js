function getCSRFToken() {
    return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
}

document.addEventListener("DOMContentLoaded", function() {
    let uploadedImage;

    document.getElementById("image-upload").addEventListener("change", function(event) {
        var file = event.target.files[0];
        uploadedImage = file;
        var reader = new FileReader();

        reader.onload = function(e) {
            var imageDisplay = document.getElementById("image-display");
            imageDisplay.innerHTML = "<img src='" + e.target.result + "' alt='Uploaded Image'>";
        };

        reader.readAsDataURL(file);
    });

    document.getElementById("process-image").addEventListener("click", function() {
        if (uploadedImage) {
            var formData = new FormData();
            formData.append("image", uploadedImage);

            fetch("/predictImages/predict/", {
                method: "POST",
                headers: {
                    'X-CSRFToken': getCSRFToken()
                },
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                var labels_link;
                if (data.label === -1) {
                    labels_link = "/static/assets/images/wait.png";
                } else if (data.label === 0) {
                    labels_link = "/static/assets/images/normal_label.png";
                } else if (data.label === 1) {
                    labels_link = "/static/assets/images/pneumonia_label.png";
                }

                document.getElementById("result-image").src = labels_link;
                document.getElementById("returned-image").src = data.image_url;
            })
            .catch(error => console.error("Error:", error));
        } else {
            alert("Please upload an image first.");
        }
    });
});
