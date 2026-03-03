document.querySelectorAll(".menu a").forEach(link => {
    link.addEventListener("click", function (e) {
        e.preventDefault();
        let target = this.getAttribute("href");
        document.querySelector(target).scrollIntoView({
            behavior: "smooth"
        });
    });
});

let imageInput = document.getElementById("leaf_image");
let previewImage = document.getElementById("preview");

if (imageInput && previewImage) {
    imageInput.addEventListener("change", function () {
        let file = this.files[0];

        if (file) {
            let reader = new FileReader();

            reader.onload = function () {
                previewImage.src = reader.result;
                previewImage.style.display = "block";
            };

            reader.readAsDataURL(file);
        }
    });
}

//Detect diseases main
async function detectDisease(event) {
    event.preventDefault();

    let fileInput = document.getElementById("leaf_image");
    let file = fileInput.files[0];

    // Validation
    if (!file) {
        alert(" Please upload image first");
        return;
    }

    // Loading state
    document.getElementById("disease").innerText = "Detecting...";
    document.getElementById("confidence").innerText = "...";
    document.getElementById("solution").innerText = "...";


        // FormData banana
        let formData = new FormData();
        formData.append("leaf_image", file);

        try {
        //Yahan apni python api url
        let response = await fetch("", {
            method: "POST",
            body: formData
        })

        if (!response.ok) {
            throw new Error("Server response not OK");
        }

        let data = await response.json();

        // Result show
        document.getElementById("disease").innerText = data.disease;
        document.getElementById("confidence").innerText = data.confidence + "%";
        document.getElementById("solution").innerText = data.solution;
    } catch (error) {
        console.error("Error:", error);
        alert("Server error. Please try again.");
    }
}
