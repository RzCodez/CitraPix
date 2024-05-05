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
        onShow: (modal) => console.info(`${modal.id} is shown`), // [1]
        onClose: (modal) => console.info(`${modal.id} is hidden`), // [2]
        openTrigger: "data-custom-open", // [3]
        closeTrigger: "data-custom-close", // [4]
        openClass: "is-open", // [5]
        disableScroll: true, // [6]
        disableFocus: false, // [7]
        awaitOpenAnimation: true, // [8]
        awaitCloseAnimation: true, // [9]
        debugMode: true, // [10]
    });
});

const imagePreview = document.querySelector(".imagePreview"),
    inputFoto = document.querySelector("#input-foto");

let preview = gsap.timeline();
inputFoto.onchange = (e) => {
    let fileReader = new FileReader();
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
    fileReader.onload = (e) => {
        imagePreview.style.backgroundImage = `url(${e.target.result})`;
        console.log(e.target.result);
    };

    fileReader.readAsDataURL(e.target.files[0]);
};

const blurSelect = document.querySelectorAll(".select-blur");

blurSelect.forEach((el, index) => {
    const selectInput = blurSelect[index].querySelector("input[type='radio']");
    el.onclick = () => {
        blurSelect.forEach((el) => {
            el.classList.remove("bg-blue-500/10", "border-blue-500");
            el.querySelector("input[type='radio']").checked = false;
        });
        selectInput.checked = true;
        blurSelect[index].classList.add("bg-blue-500/10", "border-blue-500");

        const dataBlurAtribute = selectInput.getAttribute("data-blur");
        console.log(dataBlurAtribute);
    };
});

const checkFace = document.getElementById("check-face");
const faceOption = document.querySelector(".face-option-ct");
faceOption.style.display = "none";
faceOption.style.opacity = 0;
checkFace.addEventListener("click", () => {
    if (checkFace.checked == true) {
        faceOption.style.display = "flex";
        setTimeout(() => {
            faceOption.style.opacity = 1;
        }, 300);
    } else {
        faceOption.style.opacity = 0;
        setTimeout(() => {
            faceOption.style.display = "none";
        }, 300);
    }
});

const faceSelect = document.querySelectorAll(".face-option");

faceSelect.forEach((el, index) => {
    const selectInput = faceSelect[index].querySelector("input[type='radio']");
    el.onclick = () => {
        faceSelect.forEach((el) => {
            el.classList.remove("bg-blue-500/10", "border-blue-500");
            el.querySelector("input[type='radio']").checked = false;
        });
        selectInput.checked = true;
        faceSelect[index].classList.add("bg-blue-500/10", "border-blue-500");

        const dataBlurAtribute = selectInput.getAttribute("data-blur");
        console.log(dataBlurAtribute);
    };
});

// Delete image after blurring image

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

function downloadImage() {
    const downloadImage = document.querySelector(".download-button");
    const imageResultContainer = document.querySelector(".image-result-container");
    const imageResult = imageResultContainer.querySelector("img");

    downloadImage.onclick = () => {
        const imageSrc = imageResult.src;
        // const imageSrc = imageResult ? imageResult.src : null;
        if (imageSrc && imageSrc !== "") {
            const imageName = imageSrc.substring(imageSrc.lastIndexOf("/") + 1);
            const anchor = document.createElement("a");
            anchor.href = imageSrc;
            anchor.download = imageName;
            document.body.appendChild(anchor);
            anchor.click();
            document.body.removeChild(anchor);
        } else if (imageSrc === "") {
            alert("Silahkan pilih gambar terlebih dahulu");
            Toastify({
                text: "Gambar tidak tersedia/dihapus!",
                duration: 3000,
                destination: "https://github.com/apvarun/toastify-js",
                newWindow: true,
                close: true,
                gravity: "bottom", // `top` or `bottom`
                position: "center", // `left`, `center` or `right`
                stopOnFocus: true, // Prevents dismissing of toast on hover
                style: {
                    background: "linear-gradient(to right, #00b09b, #96c93d)",
                },
                onClick: function () {}, // Callback after click
            }).showToast();
        }
    };

    const observer = new MutationObserver(() => {
        if (!imageResult.getAttribute("src")) {
            downloadImage.onclick = null;
        }
    });

    observer.observe(imageResult, { attributes: true });
}

downloadImage();
