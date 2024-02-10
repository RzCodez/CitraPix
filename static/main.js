window.addEventListener("load", () => {
    const a = document.querySelectorAll("a");

    a.forEach((element) => {
        element.addEventListener("click", (e) => {
            e.preventDefault();
        });
    });

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
