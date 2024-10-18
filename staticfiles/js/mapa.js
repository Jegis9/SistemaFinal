document.addEventListener("DOMContentLoaded", function () {
  var map; // Variable para el mapa

  // Escucha todos los botones con la clase "ver-btn"
  document.querySelectorAll(".ver-btn").forEach(function (button) {
    button.addEventListener("click", function () {
      // Obtener las coordenadas del atributo data-coordenadas
      var coordenadas = button.getAttribute("data-coordenadas");
      var descripcion = button.getAttribute("data-descripcion");
      var usuario = button.getAttribute("data-usuario");
      var correo = button.getAttribute("data-usuario-correo");

      document.getElementById("descripcion").value = descripcion;
      document.getElementById("coordenadas").value = coordenadas;
      document.getElementById("usuario").value = usuario;
      document.getElementById("correo").value = correo;

      var coordsArray = coordenadas.split(",");

      // Si el mapa no ha sido inicializado, inicializarlo
      if (!map) {
        map = L.map("map").setView([coordsArray[0], coordsArray[1]], 13);

        // Cargar tiles desde OpenStreetMap
        L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
          attribution:
            '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
        }).addTo(map);

        // Añadir un marcador en la posición de la emergencia
        L.marker([coordsArray[0], coordsArray[1]])
          .addTo(map)
          .bindPopup("Ubicación de la emergencia")
          .openPopup();
      } else {
        // Si el mapa ya está inicializado, solo mover el mapa a la nueva posición
        map.setView([coordsArray[0], coordsArray[1]], 13);

        // Actualizar el marcador
        L.marker([coordsArray[0], coordsArray[1]])
          .addTo(map)
          .bindPopup("Ubicación de la emergencia")
          .openPopup();
      }

      // Forzar la actualización del tamaño del mapa
      setTimeout(function () {
        map.invalidateSize();
      }, 400); // Pequeño retraso para asegurarse de que el contenedor está visible
    });
  });

  // Mensaje de confirmación antes de enviar el formulario
  const btnCerrarEmergencia = document.getElementById("cerrar");
  if (btnCerrarEmergencia) {
    btnCerrarEmergencia.addEventListener("click", (e) => {
      e.preventDefault(); // Previene que el formulario se envíe inmediatamente

      Swal.fire({
        title: "¿Marcar como atendida?",
        text: "¿Quieres marcar esta emergencia como atendida?",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "Sí, reportar",
        cancelButtonText: "Cancelar",
      }).then((result) => {
        if (result.isConfirmed) {
          // Si el usuario hace clic en "Sí", envía el formulario
          document.getElementById("atendido").submit();
        }
      });
    });
  }
});
