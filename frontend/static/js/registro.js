document.getElementById("form-registro").addEventListener("submit", async function (e) {
  e.preventDefault(); // 🔸 Evita que el formulario recargue la página

  const form = e.target;

  const data = {
    nombre: form.nombre.value,
    apellido: form.apellido.value,
    dni: form.dni.value,
    telefono: form.telefono.value,
    correo: form.correo.value,
    password: form.password.value,
    confirm_password: form.confirm_password.value
  };

  try {
    // 🔽 Enviar los datos al backend
    const res = await fetch("http://localhost:5000/api/usuario/registro", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data)
    });

    const result = await res.json();
    const alerta = document.getElementById("alerta"); // 🔽 Contenedor para mostrar mensajes

    if (res.ok) {
      // ✅ Registro exitoso
      alerta.innerHTML = `<div class="alert alert-success">${result.mensaje}</div>`;
      form.reset();

      // 🔽 Redirigir al login después de un breve mensaje
      setTimeout(() => {
        window.location.href = "login.html";
      }, 1500);
    } else {
      // ❌ Error en el registro
      alerta.innerHTML = `<div class="alert alert-danger">${result.error}</div>`;
    }
  } catch (error) {
    console.error("Error:", error);
    // ❌ Error de conexión
    document.getElementById("alerta").innerHTML = 
      `<div class="alert alert-danger">Error al conectar con el servidor.</div>`;
  }
});
