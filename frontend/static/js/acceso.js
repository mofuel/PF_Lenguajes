// Esperar a que el DOM esté completamente cargado
document.addEventListener("DOMContentLoaded", function () {
    // Obtener el rol guardado en el navegador
    const rol = localStorage.getItem("rol");

    // Si no es admin, redirigir a página de acceso denegado
    if (rol !== "admin") {
        window.location.href = "sin-acceso.html";
    }
});
