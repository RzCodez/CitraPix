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

