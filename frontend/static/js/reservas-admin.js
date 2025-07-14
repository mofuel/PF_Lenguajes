const API_BASE = "http://127.0.0.1:5000/api/admin/reservas";
const token = localStorage.getItem("token");

// Función para cargar todas las reservas
async function cargarReservas() {
    try {
        const response = await fetch(API_BASE, {
            headers: {
                Authorization: `Bearer ${token}`
            }
        });

        if (!response.ok) throw new Error("No se pudieron cargar las reservas");

        const data = await response.json();
        const tbody = document.getElementById("tabla-reservas");
        tbody.innerHTML = "";

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
                    <button class="btn btn-sm btn-warning" onclick="abrirModalEditar(${reserva.id})">Editar</button>
                    <button class="btn btn-sm btn-danger" onclick="eliminarReserva(${reserva.id})">Eliminar</button>
                </td>
            `;
            tbody.appendChild(tr);
        });
    } catch (err) {
        Swal.fire("Error", "❌ No se pudieron cargar las reservas", "error");
        console.error(err);
    }
}

// Abrir modal para registrar nueva reserva
document.getElementById("btn-agregar-reserva").addEventListener("click", () => {
    document.getElementById("formRegistrarReserva").reset();
    new bootstrap.Modal(document.getElementById("modalRegistrarReserva")).show();
});

// Registrar nueva reserva
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
        Swal.fire("Campo requerido", "Por favor selecciona una plaza.", "warning");
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
            Swal.fire("¡Éxito!", "✅ Reserva registrada correctamente", "success");
            cargarReservas();
        } else {
            Swal.fire("Error", data.error || "❌ Error al registrar la reserva", "error");
        }
    } catch (err) {
        console.error(err);
        Swal.fire("Error", "❌ Error al registrar la reserva", "error");
    }
});

// Abrir modal con datos de reserva para editar
async function abrirModalEditar(id) {
    try {
        const res = await fetch(`${API_BASE}/${id}`, {
            headers: {
                Authorization: `Bearer ${token}`
            }
        });

        if (!res.ok) throw new Error("Reserva no encontrada");

        const data = await res.json();

        if (!data.plaza) {
            Swal.fire("Campo requerido", "La reserva no tiene una plaza válida.", "warning");
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
        Swal.fire("Error", "❌ Error al abrir modal de edición", "error");
        console.error("Error al abrir modal de edición:", err);
    }
}

// Guardar cambios al editar
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
        Swal.fire("Campo requerido", "Por favor selecciona una plaza.", "warning");
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
            Swal.fire("¡Éxito!", "✅ Reserva actualizada correctamente", "success");
            cargarReservas();
        } else {
            Swal.fire("Error", data.error || "❌ Error al editar la reserva", "error");
        }
    } catch (err) {
        console.error(err);
        Swal.fire("Error", "❌ Error al editar la reserva", "error");
    }
});

// Eliminar reserva
async function eliminarReserva(id) {
    const resultado = await Swal.fire({
        title: "¿Estás seguro?",
        text: "Esta acción eliminará la reserva permanentemente.",
        icon: "warning",
        showCancelButton: true,
        confirmButtonText: "Sí, eliminar",
        cancelButtonText: "Cancelar"
    });

    if (!resultado.isConfirmed) return;

    try {
        const res = await fetch(`${API_BASE}/${id}`, {
            method: "DELETE",
            headers: {
                Authorization: `Bearer ${token}`
            }
        });

        const data = await res.json();
        if (res.ok) {
            Swal.fire("¡Eliminado!", "✅ Reserva eliminada correctamente", "success");
            cargarReservas();
        } else {
            Swal.fire("Error", data.error || "❌ No se pudo eliminar la reserva", "error");
        }
    } catch (err) {
        console.error(err);
        Swal.fire("Error", "❌ Error al eliminar la reserva", "error");
    }
}

// Cargar reservas al inicio
window.addEventListener("DOMContentLoaded", cargarReservas);
