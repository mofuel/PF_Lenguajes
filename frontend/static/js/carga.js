// 🔽 Cargar el contenido del footer desde un archivo externo
fetch('../static/html/footer.html')
  .then(response => response.text())
  .then(data => {
      document.getElementById('footer').innerHTML = data;
  });


// 🔽 Ejecutar cuando el DOM esté listo
document.addEventListener("DOMContentLoaded", function () {
    // Obtener datos del usuario desde localStorage
    const token = localStorage.getItem("token");
    const nombreUsuario = localStorage.getItem("nombre");
    const rol = localStorage.getItem("rol");

    // Referencias a elementos del DOM
    const mensajeUsuario = document.getElementById("mensaje-usuario");
    const linkLogin = document.getElementById("link-login");
    const btnLogout = document.getElementById("btn-logout");
    const menuCliente = document.getElementById("menu-cliente");
    const menuAdmin = document.getElementById("menu-admin");

    // Si no existe el contenedor del mensaje, salir
    if (!mensajeUsuario) return;

    // Si hay token, mostrar saludo y menú correspondiente
    if (token) {
        mensajeUsuario.innerHTML = `
    <div class="dropdown">
        <a class="nav-link dropdown-toggle text-white" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
            Hola, <strong>${nombreUsuario || "Usuario"}</strong>
        </a>
        <ul class="dropdown-menu dropdown-menu-end">
            <li><a class="dropdown-item" href="../templates/perfilcli.html">Perfil</a></li>
            <li><hr class="dropdown-divider"></li>
            <li><a class="dropdown-item text-danger" href="../templates/login.html" onclick="logout()">Cerrar sesión</a></li>
        </ul>
    </div>`;

        // Ocultar el enlace de login si ya está autenticado
        if (linkLogin) linkLogin.style.display = "none";
        if (btnLogout) btnLogout.classList.remove("d-none");

        // Mostrar menú según el rol
        if (rol === "cliente" && menuCliente) {
            menuCliente.classList.remove("d-none");
        } else if (rol === "admin" && menuAdmin) {
            menuAdmin.classList.remove("d-none");
        }
    }
});

// 🔽 Cerrar sesión: limpiar datos y redirigir
function logout() {
    localStorage.clear();
    window.location.href = "/login";
}
