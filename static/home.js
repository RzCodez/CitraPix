const a = document.querySelectorAll("a");

a.forEach((element) => {
    element.addEventListener("click", (e) => {
        e.preventDefault();
    });
});
