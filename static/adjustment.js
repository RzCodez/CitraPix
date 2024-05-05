const progressLoad = document.querySelector(".progress-load");

window.addEventListener("load", () => {
    progressLoad.style.clipPath = "polygon(100% 0, 0 0, 0 100%, 100% 100%)";
    let tl = gsap.timeline({
        delay: 1,
    });

    tl.from(".slide", {
        yPercent: 60,
        opacity: 0,
        duration: 0.5,
        stagger: 0.1,
        ease: "power3.out",
    });
    setTimeout(() => {
        progressLoad.style.opacity = 0;
    }, 1000);

    // Modal function
    MicroModal.init({
        onShow: (modal) => console.info(`${modal.id} is shown`),
        onClose: (modal) => console.info(`${modal.id} is hidden`),
        openTrigger: "data-custom-open",
        closeTrigger: "data-custom-close",
        openClass: "is-open",
        disableScroll: true,
        disableFocus: false,
        awaitOpenAnimation: true,
        awaitCloseAnimation: true,
        debugMode: true,
    });
});

const imagePreview = document.querySelector(".imagePreview"),
    inputFoto = document.querySelector("#input-foto"),
    oldImage = document.getElementById("old-image");

inputFoto.value = "";

let preview = gsap.timeline();
inputFoto.onchange = (e) => {
    let fileReader = new FileReader();
    // if(inputFoto.files.length > 0) {
    //     oldImage.style.display = "none";
    // }
    // oldImage.style.display = "none";
    preview.restart();
    preview.to(".placeholder", {
        color: "white",
        opacity: 0,
        duration: 0.5,
        ease: "power1.out",
    });
    preview.to(".blur", {
        opacity: 0,
        delay: 1,
        duration: 0.5,
        ease: "power1.out",
    });

    fileReader.onerror = (error) => {
        console.error("Error reading the file:", error);
    };

    fileReader.onload = (e) => {
        imagePreview.style.backgroundImage = `url(${e.target.result})`;
        console.log(e.target.result);
        if (e.target.result) {
            oldImage.classList.add("hidden");
            // alert("Gambar diupload! Menghapus old image...")
        }
    };

    fileReader.readAsDataURL(e.target.files[0]);
};

function deleteImage() {
    const deleteButton = document.querySelector(".delete-button");
    const imageResultContainer = document.querySelector(".image-result-container");
    const imageResult = imageResultContainer.querySelector("img");
    deleteButton.onclick = () => {
        // imageResult.src = "";
        imageResult.remove();
    };
}

deleteImage();

function getRangeValue() {
    const rangeInput = document.querySelectorAll(".range-ct input[type=range]"),
        rangeValue = document.querySelectorAll(".range-ct .label-range input[type=text]");

    rangeInput.forEach((input, i) => {
        input.addEventListener("input", () => {
            rangeValue[i].value = input.value;

            var refinedValue = rangeValue[i].value;

            console.log(refinedValue);
        });
    });
}

getRangeValue();
