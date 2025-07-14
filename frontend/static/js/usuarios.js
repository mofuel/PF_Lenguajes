document.addEventListener("DOMContentLoaded", async () => {
  const token = localStorage.getItem("token");
  const tabla = document.getElementById("tabla-usuarios");

  try {
    const res = await fetch("http://localhost:5000/api/usuario/listar", {
      headers: {
        "Authorization": `Bearer ${token}`
      }
    });

    const data = await res.json();

    if (res.ok) {
      data.forEach(usuario => {
        tabla.innerHTML += `
          <tr>
            <td>${usuario.id}</td>
            <td>${usuario.nombre}</td>
            <td>${usuario.apellido}</td>
            <td>${usuario.correo}</td>
            <td>${usuario.dni}</td>
            <td>${usuario.telefono}</td>
            <td>${usuario.rol}</td>
            <td>
              <button class="btn btn-sm btn-primary btn-editar" 
                data-usuario='${JSON.stringify(usuario).replace(/'/g, "&apos;")}'>
                Editar
              </button>
              <button class="btn btn-sm btn-danger ms-2" onclick="eliminarUsuario(${usuario.id})">Eliminar</button>
            </td>
          </tr>
        `;
      });
    } else {
      tabla.innerHTML = `<tr><td colspan="8" class="text-danger text-center">${data.error}</td></tr>`;
    }

  } catch (error) {
    tabla.innerHTML = `<tr><td colspan="8" class="text-danger text-center">Error de conexión</td></tr>`;
    console.error(error);
  }

  // Mostrar modal de registrar usuario
  document.getElementById("btn-agregar").addEventListener("click", () => {
    const form = document.getElementById("formRegistrarUsuario");
    form.reset();
    new bootstrap.Modal(document.getElementById("modalRegistrarUsuario")).show();
  });

  // Registrar usuario
  document.getElementById("formRegistrarUsuario").addEventListener("submit", async (e) => {
    e.preventDefault();
    const form = e.target;
    const datos = {
      nombre: form.nombre.value,
      apellido: form.apellido.value,
      dni: form.dni.value,
      telefono: form.telefono.value,
      correo: form.correo.value,
      password: form.password.value,
      confirm_password: form.confirm_password.value,
      rol: form.rol.value
    };

    try {
      const res = await fetch("http://localhost:5000/api/usuario/registro", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(datos)
      });

      const data = await res.json();
      if (res.ok) {
        Swal.fire("Éxito", "Usuario registrado correctamente", "success").then(() => location.reload());
      } else {
        Swal.fire("Error", data.error, "error");
      }
    } catch (error) {
      Swal.fire("Error", "Error al registrar usuario", "error");
      console.error(error);
    }
  });

  // Editar usuario
  document.getElementById("formEditarUsuario").addEventListener("submit", async (e) => {
    e.preventDefault();
    const token = localStorage.getItem("token");
    const form = e.target;
    const id = form.id.value;
    const datos = {
      nombre: form.nombre.value,
      apellido: form.apellido.value,
      dni: form.dni.value,
      telefono: form.telefono.value,
      correo: form.correo.value,
      rol: form.rol.value
    };

    try {
      const res = await fetch(`http://localhost:5000/api/usuario/${id}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify(datos)
      });

      const data = await res.json();
      if (res.ok) {
        Swal.fire("Actualizado", "Usuario actualizado correctamente", "success").then(() => location.reload());
      } else {
        Swal.fire("Error", data.error, "error");
      }
    } catch (error) {
      Swal.fire("Error", "Error al editar usuario", "error");
      console.error(error);
    }
  });
});

// Listener global para botón editar
document.addEventListener("click", function (e) {
  if (e.target.classList.contains("btn-editar")) {
    const data = e.target.dataset.usuario;
    const usuario = JSON.parse(data.replace(/&apos;/g, "'"));
    mostrarEditar(usuario);
  }
});

function mostrarEditar(usuario) {
  const form = document.getElementById("formEditarUsuario");

  form.id.value = usuario.id;
  form.nombre.value = usuario.nombre;
  form.apellido.value = usuario.apellido;
  form.dni.value = usuario.dni;
  form.telefono.value = usuario.telefono;
  form.correo.value = usuario.correo;
  form.rol.value = usuario.rol;

  new bootstrap.Modal(document.getElementById("modalEditarUsuario")).show();
}

async function eliminarUsuario(id) {
  const confirm = await Swal.fire({
    title: "¿Estás seguro?",
    text: "Esta acción eliminará el usuario permanentemente.",
    icon: "warning",
    showCancelButton: true,
    confirmButtonColor: "#d33",
    cancelButtonColor: "#3085d6",
    confirmButtonText: "Sí, eliminar",
    cancelButtonText: "Cancelar"
  });

  if (!confirm.isConfirmed) return;

  try {
    const token = localStorage.getItem("token");
    const res = await fetch(`http://localhost:5000/api/usuario/${id}`, {
      method: "DELETE",
      headers: {
        "Authorization": `Bearer ${token}`
      }
    });

    const data = await res.json();
    if (res.ok) {
      Swal.fire("Eliminado", "Usuario eliminado correctamente", "success").then(() => location.reload());
    } else {
      Swal.fire("Error", data.error, "error");
    }
  } catch (error) {
    Swal.fire("Error", "Error al eliminar usuario", "error");
    console.error(error);
  }
}
