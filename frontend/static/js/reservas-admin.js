// URL base de la API y token desde localStorage
const API_BASE = "http://127.0.0.1:5000/api/admin/reservas";
const token = localStorage.getItem("token");

// 📥 Cargar todas las reservas en la tabla
async function cargarReservas() {
    try {
        const response = await fetch(API_BASE, {
            headers: { Authorization: `Bearer ${token}` }
        });

        if (!response.ok) throw new Error("Error al cargar");

        const data = await response.json();
        const tbody = document.getElementById("tabla-reservas");
        tbody.innerHTML = "";

        // Renderizar cada fila
        data.forEach(reserva => {
            const tr = document.createElement("tr");
            tr.innerHTML = `
                <td>${reserva.id}</td>
                <td>${reserva.plaza}</td>
                <td>${reserva.placa}</td>
                <td>${reserva.fecha_inicio}</td>
                <td>${reserva.fecha_fin}</td>
                <td>${reserva.usuario_id}</td>
                <td>
                    <button class="btn btn-warning btn-sm" onclick="abrirModalEditar(${reserva.id})">Editar</button>
                    <button class="btn btn-danger btn-sm" onclick="eliminarReserva(${reserva.id})">Eliminar</button>
                </td>
            `;
            tbody.appendChild(tr);
        });
    } catch (err) {
        Swal.fire("Error", "❌ No se pudieron cargar las reservas", "error");
        console.error(err);
    }
}

// 🟩 Mostrar modal para nueva reserva
document.getElementById("btn-agregar-reserva").addEventListener("click", () => {
    document.getElementById("formRegistrarReserva").reset();
    new bootstrap.Modal(document.getElementById("modalRegistrarReserva")).show();
});

// 📝 Registrar nueva reserva
document.getElementById("formRegistrarReserva").addEventListener("submit", async (e) => {
    e.preventDefault();
    const form = e.target;

    const reserva = {
        placa: form.placa.value,
        plaza: form.plaza.value,
        fecha_inicio: form.fecha_inicio.value,
        fecha_fin: form.fecha_fin.value,
        usuario_id: parseInt(form.usuario_id.value)
    };

    if (!reserva.plaza) {
        Swal.fire("Campo requerido", "Selecciona una plaza", "warning");
        return;
    }

    try {
        const res = await fetch(API_BASE, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`
            },
            body: JSON.stringify(reserva)
        });

        const data = await res.json();
        if (res.ok) {
            bootstrap.Modal.getInstance(document.getElementById("modalRegistrarReserva")).hide();
            Swal.fire("¡Éxito!", "Reserva registrada", "success");
            cargarReservas();
        } else {
            Swal.fire("Error", data.error || "Error al registrar", "error");
        }
    } catch (err) {
        console.error(err);
        Swal.fire("Error", "❌ Error al registrar", "error");
    }
});

// ✏️ Mostrar modal para editar reserva
async function abrirModalEditar(id) {
    try {
        const res = await fetch(`${API_BASE}/${id}`, {
            headers: { Authorization: `Bearer ${token}` }
        });

        if (!res.ok) throw new Error("No encontrada");

        const data = await res.json();
        if (!data.plaza) {
            Swal.fire("Advertencia", "Plaza inválida", "warning");
            return;
        }

        const form = document.getElementById("formEditarReserva");
        form.id.value = data.id;
        form.placa.value = data.placa;
        form.plaza.value = data.plaza;
        form.fecha_inicio.value = data.fecha_inicio;
        form.fecha_fin.value = data.fecha_fin;
        form.usuario_id.value = data.usuario_id;

        new bootstrap.Modal(document.getElementById("modalEditarReserva")).show();
    } catch (err) {
        Swal.fire("Error", "No se pudo abrir", "error");
        console.error(err);
    }
}

// 💾 Guardar edición
document.getElementById("formEditarReserva").addEventListener("submit", async (e) => {
    e.preventDefault();
    const form = e.target;

    const reserva = {
        placa: form.placa.value,
        plaza: form.plaza.value,
        fecha_inicio: form.fecha_inicio.value,
        fecha_fin: form.fecha_fin.value,
        usuario_id: parseInt(form.usuario_id.value)
    };

    if (!reserva.plaza) {
        Swal.fire("Campo requerido", "Selecciona una plaza", "warning");
        return;
    }

    try {
        const res = await fetch(`${API_BASE}/${form.id.value}`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`
            },
            body: JSON.stringify(reserva)
        });

        const data = await res.json();
        if (res.ok) {
            bootstrap.Modal.getInstance(document.getElementById("modalEditarReserva")).hide();
            Swal.fire("¡Éxito!", "Reserva actualizada", "success");
            cargarReservas();
        } else {
            Swal.fire("Error", data.error || "No se pudo editar", "error");
        }
    } catch (err) {
        console.error(err);
        Swal.fire("Error", "❌ Error al editar", "error");
    }
});

// 🗑️ Eliminar reserva con confirmación
async function eliminarReserva(id) {
    const resultado = await Swal.fire({
        title: "¿Eliminar?",
        text: "Esto eliminará la reserva.",
        icon: "warning",
        showCancelButton: true,
        confirmButtonText: "Sí",
        cancelButtonText: "No"
    });

    if (!resultado.isConfirmed) return;

    try {
        const res = await fetch(`${API_BASE}/${id}`, {
            method: "DELETE",
            headers: { Authorization: `Bearer ${token}` }
        });

        const data = await res.json();
        if (res.ok) {
            Swal.fire("Eliminado", "Reserva eliminada", "success");
            cargarReservas();
        } else {
            Swal.fire("Error", data.error || "No se pudo eliminar", "error");
        }
    } catch (err) {
        console.error(err);
        Swal.fire("Error", "❌ Error al eliminar", "error");
    }
}

// 🚀 Cargar reservas al iniciar la página
window.addEventListener("DOMContentLoaded", cargarReservas);
