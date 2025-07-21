document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("form-reserva");
  const alerta = document.getElementById("alerta-reserva");

  if (!form) return;

  form.addEventListener("submit", async function (e) {
    e.preventDefault();

    const token = localStorage.getItem("token");
    if (!token) {
      alerta.innerHTML = `<div class="alert alert-danger">Debes iniciar sesión para reservar.</div>`;
      return;
    }

    const data = {
      plaza: document.getElementById("plaza").value,
      placa: document.getElementById("placa").value,
      fecha_inicio: document.getElementById("fecha_inicio").value,
      fecha_fin: document.getElementById("fecha_fin").value
    };

    // 🔸 Validar campos vacíos
    if (!data.plaza || !data.placa || !data.fecha_inicio || !data.fecha_fin) {
      alerta.innerHTML = `<div class="alert alert-warning">Todos los campos son obligatorios.</div>`;
      return;
    }

    try {
      // 🔍 Verificar disponibilidad de plaza
      const checkRes = await fetch(`http://localhost:5000/api/verificar-plaza`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`
        },
        body: JSON.stringify({
          plaza: data.plaza,
          fecha_inicio: data.fecha_inicio,
          fecha_fin: data.fecha_fin
        })
      });

      const checkResult = await checkRes.json();

      if (checkRes.status === 409) {
        alerta.innerHTML = `<div class="alert alert-warning">La plaza ya está ocupada en ese horario.</div>`;
        return;
      }

      // ✅ Registrar reserva si la plaza está libre
      const res = await fetch("http://localhost:5000/api/reservar", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`
        },
        body: JSON.stringify(data)
      });

      const result = await res.json();

      if (res.ok) {
        alerta.innerHTML = `<div class="alert alert-success">${result.mensaje}</div>`;
        form.reset();
      } else {
        alerta.innerHTML = `<div class="alert alert-danger">${result.error || "Error en la reserva."}</div>`;
      }
    } catch (error) {
      // ❌ Error al comunicarse con el servidor
      alerta.innerHTML = `<div class="alert alert-danger">Error de conexión con el servidor.</div>`;
      console.error("Error:", error);
    }
  });
});
