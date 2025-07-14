document.addEventListener("DOMContentLoaded", function () {
  const formLogin = document.getElementById("loginForm"); // ✅ cambia esto

  if (!formLogin) return;

  formLogin.addEventListener("submit", async function (e) {
    e.preventDefault();

    const form = e.target;
    const data = {
      correo: form.correo.value,
      password: form.password.value
    };

    try {
      const res = await fetch("http://localhost:5000/api/usuario/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
      });

      const result = await res.json();

      // Asegúrate que exista este div en el HTML
      const alerta = document.getElementById("alerta");

      if (res.ok) {
        localStorage.setItem("token", result.access_token);
        localStorage.setItem("rol", result.rol || "usuario");
        localStorage.setItem("nombre", result.nombre)
        if (alerta) {
          alerta.innerHTML = `<div class="alert alert-success">Inicio de sesión exitoso</div>`;
        }
        setTimeout(() => {
          if (result.rol === "admin") {
            window.location.href = "dashboard.html";
          } else {
            window.location.href = "index.html";
          }
        }, 1500);
      } else {
        if (alerta) {
          alerta.innerHTML = `<div class="alert alert-danger">${result.error || "Credenciales inválidas"}</div>`;
        }
      }
    } catch (error) {
      console.error("Error:", error);
      if (alerta) {
        alerta.innerHTML =
          `<div class="alert alert-danger">Error al conectar con el servidor.</div>`;
      }
    }
  });
});
