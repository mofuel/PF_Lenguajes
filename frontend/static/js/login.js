document.addEventListener("DOMContentLoaded", function () {
  const formLogin = document.getElementById("loginForm"); // 🔽 Referencia al formulario

  if (!formLogin) return; // 🔸 Si no existe el formulario, salir

  // 🔽 Escuchar el evento de envío del formulario
  formLogin.addEventListener("submit", async function (e) {
    e.preventDefault(); // 🔸 Evita recargar la página

    const form = e.target;
    const data = {
      correo: form.correo.value,
      password: form.password.value
    };

    try {
      // 🔽 Enviar datos al backend para autenticación
      const res = await fetch("http://localhost:5000/api/usuario/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
      });

      const result = await res.json();
      const alerta = document.getElementById("alerta"); // 🔽 Div donde se muestra la respuesta

      if (res.ok) {
        // 🔽 Guardar token y datos en localStorage
        localStorage.setItem("token", result.access_token);
        localStorage.setItem("rol", result.rol || "usuario");
        localStorage.setItem("nombre", result.nombre);

        // 🔽 Mostrar mensaje de éxito
        if (alerta) {
          alerta.innerHTML = `<div class="alert alert-success">Inicio de sesión exitoso</div>`;
        }

        // 🔽 Redirigir según el rol
        setTimeout(() => {
          if (result.rol === "admin") {
            window.location.href = "dashboard.html";
          } else {
            window.location.href = "index.html";
          }
        }, 1500);
      } else {
        // 🔽 Mostrar error devuelto por el backend
        if (alerta) {
          alerta.innerHTML = `<div class="alert alert-danger">${result.error || "Credenciales inválidas"}</div>`;
        }
      }
    } catch (error) {
      console.error("Error:", error);
      // 🔽 Error de conexión
      const alerta = document.getElementById("alerta");
      if (alerta) {
        alerta.innerHTML =
          `<div class="alert alert-danger">Error al conectar con el servidor.</div>`;
      }
    }
  });
});
