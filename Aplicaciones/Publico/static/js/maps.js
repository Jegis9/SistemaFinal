// Esperar a que el DOM esté completamente cargado antes de ejecutar el código
window.onload = function () {
  // Coordenadas de Totonicapán, Guatemala
  var defaultLatLng = [14.9119, -91.3618]; // Coordenadas de Totonicapán
  var map = L.map("map").setView(defaultLatLng, 13); // Vista inicial por defecto

  // Cargar el mapa desde OpenStreetMap
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 19,
  }).addTo(map);

  // Crear un marcador inicial en Totonicapán
  var marker = L.marker(defaultLatLng, { draggable: true }).addTo(map);

  // Intentar obtener la geolocalización del usuario
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      function (position) {
        var userLat = position.coords.latitude;
        var userLng = position.coords.longitude;
        var userLatLng = [userLat, userLng];

        // Centrar el mapa en la ubicación del usuario
        map.setView(userLatLng, 13);
        // Mover el marcador a la ubicación del usuario
        marker.setLatLng(userLatLng);
        // Actualizar el campo de ubicación
        document.getElementById("location").value = userLat + ", " + userLng;
      },
      function (error) {
        // Si la geolocalización falla, centrar en Totonicapán
        handleLocationError();
      }
    );
  } else {
    // Si el navegador no soporta la geolocalización, centrar en Totonicapán
    handleLocationError();
  }

  // Función para manejar el error de geolocalización
  function handleLocationError() {
    alert(
      "No se pudo obtener tu ubicación. Mostrando Totonicapán por defecto."
    );
    map.setView(defaultLatLng, 13);
    marker.setLatLng(defaultLatLng);
    document.getElementById("location").value =
      defaultLatLng[0] + ", " + defaultLatLng[1];
  }

  // Detectar cuando el marcador es arrastrado y actualizar la ubicación
  marker.on("dragend", function () {
    var position = marker.getLatLng();
    document.getElementById("location").value =
      position.lat + ", " + position.lng;
  });

  // Mensaje de confirmación antes de enviar el formulario
  const btnRegistrarReporte = document.getElementById("report");
  if (btnRegistrarReporte) {
    btnRegistrarReporte.addEventListener("click", (e) => {
      e.preventDefault(); // Previene que el formulario se envíe inmediatamente

      Swal.fire({
        title: "¿Estás seguro de tus datos ingresados?",
        text: "¿Quieres reportar la emergencia?",
        icon: "warning",
        showCancelButton: true, // Esto agrega el botón de cancelar
        confirmButtonColor: "#3085d6", // Color del botón de confirmación
        cancelButtonColor: "#d33", // Color del botón de cancelar
        confirmButtonText: "Sí, reportar",
        cancelButtonText: "Cancelar",
      }).then((result) => {
        if (result.isConfirmed) {
          // Si el usuario hace clic en "Sí", envía el formulario
          document.getElementById("emergencyForm").submit();
        }
      });
    });
  }
};
