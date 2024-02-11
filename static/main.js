const progressLoad = document.querySelector(".progress-load");

window.addEventListener("load", () => {
    progressLoad.style.clipPath = "polygon(100% 0, 0 0, 0 100%, 100% 100%)";
    let tl = gsap.timeline({
        delay: 1,
    });

    tl.from(".slide-up", {
        yPercent: 30,
        opacity: 0,
        duration: 1,
        stagger: 0.1,
        ease: "expo.out",
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
