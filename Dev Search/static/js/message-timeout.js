let alertWrapper = document.querySelector(".alert");
let alertClose = document.querySelector(".alert__close");

try {
    alertWrapper.style.position = "fixed";
    alertWrapper.style.top = "12%";
    alertWrapper.style.right = "1%";
} catch (error) {}

if (alertWrapper) {
    alertClose.addEventListener("click", () => {
        alertWrapper.style.display = "none";
    });
}
setTimeout(function () {
    try {
        alertWrapper.style.display = "none";
    } catch (error) {}
}, 3500);