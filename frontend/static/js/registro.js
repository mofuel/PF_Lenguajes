document.getElementById("form-registro").addEventListener("submit", async function (e) {
  e.preventDefault();

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
    const res = await fetch("http://localhost:5000/api/usuario/registro", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data)
    });

    const result = await res.json();
    const alerta = document.getElementById("alerta");

    if (res.ok) {
      alerta.innerHTML = `<div class="alert alert-success">${result.mensaje}</div>`;
      form.reset();
      setTimeout(() => {
        window.location.href = "login.html"; // Redirige al login si quieres
      }, 1500);
    } else {
      alerta.innerHTML = `<div class="alert alert-danger">${result.error}</div>`;
    }
  } catch (error) {
    console.error("Error:", error);
    document.getElementById("alerta").innerHTML = `<div class="alert alert-danger">Error al conectar con el servidor.</div>`;
  }
});
