const progressLoad = document.querySelector(".progress-load");

window.addEventListener("load", () => {
    progressLoad.style.clipPath = "polygon(100% 0, 0 0, 0 100%, 100% 100%)";
    let tl = gsap.timeline({
        delay: 1
    });

    tl.from(".slide-up", {
        yPercent: 100,
        opacity: 0,
        duration: 1,
        stagger: 0.3,
        ease: "power4.out",
    });
    setTimeout(() => {
        progressLoad.style.opacity = 0;
    }, 1000);
});
