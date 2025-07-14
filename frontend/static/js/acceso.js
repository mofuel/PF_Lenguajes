document.addEventListener("DOMContentLoaded", function () {
    const rol = localStorage.getItem("rol");

    if (rol !== "admin") {
        window.location.href = "sin-acceso.html";
    }
});