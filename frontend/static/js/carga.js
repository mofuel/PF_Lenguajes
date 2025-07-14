fetch('../static/html/footer.html')
.then(response => response.text())
.then(data => {
    document.getElementById('footer').innerHTML = data;
});




document.addEventListener("DOMContentLoaded", function () {
    const token = localStorage.getItem("token");
    const nombreUsuario = localStorage.getItem("nombre");
    const rol = localStorage.getItem("rol");

    const mensajeUsuario = document.getElementById("mensaje-usuario");
    const linkLogin = document.getElementById("link-login");
    const btnLogout = document.getElementById("btn-logout");
    const menuCliente = document.getElementById("menu-cliente");
    const menuAdmin = document.getElementById("menu-admin");

    if (!mensajeUsuario) return; // 👈 Protege si el span no existe

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
        if (linkLogin) linkLogin.style.display = "none";
        if (btnLogout) btnLogout.classList.remove("d-none");

        if (rol === "cliente" && menuCliente) {
            menuCliente.classList.remove("d-none");
        } else if (rol === "admin" && menuAdmin) {
            menuAdmin.classList.remove("d-none");
        }
    }
});

function logout() {
    localStorage.clear();
    window.location.href = "/login";
}

