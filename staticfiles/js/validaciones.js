document.addEventListener("DOMContentLoaded", function () {
  const deleteButtons = document.querySelectorAll(".eliminar-btn");

  deleteButtons.forEach((button) => {
    button.addEventListener("click", function () {
      const url = this.getAttribute("data-url");
      const csrfToken = document
        .querySelector('meta[name="csrf-token"]')
        .getAttribute("content");

      Swal.fire({
        title: "¿Estás seguro de eliminar la informacion?",
        text: "¡No podrás revertir esto!",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#d33",
        cancelButtonColor: "#6c757d",
        confirmButtonText: "Sí, eliminar",
        cancelButtonText: "Cancelar",
      }).then((result) => {
        if (result.isConfirmed) {
          // Crear y enviar el formulario de eliminación
          const form = document.createElement("form");
          form.method = "POST";
          form.action = url;

          // Agregar CSRF token
          const csrfInput = document.createElement("input");
          csrfInput.type = "hidden";
          csrfInput.name = "csrfmiddlewaretoken";
          csrfInput.value = csrfToken;
          form.appendChild(csrfInput);

          document.body.appendChild(form);
          form.submit();
        }
      });
    });
  });
});
