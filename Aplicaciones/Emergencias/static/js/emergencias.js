document.addEventListener("DOMContentLoaded", function () {
  const servicioRadios = document.querySelectorAll('input[name="servicio"]');
  const camposVarios = document.getElementById("varios-form");
  const camposAmbulancia = document.getElementById("ambulancia-form");
  const camposIncendios = document.getElementById("incendios-form");

  function toggleFields() {
    camposVarios.style.display = "none";
    camposAmbulancia.style.display = "none";
    camposIncendios.style.display = "none";

    const selectedService = document.querySelector(
      'input[name="servicio"]:checked'
    );
    if (selectedService) {
      if (selectedService.value === "1") {
        // Cambiado de "varios" a "1"
        camposVarios.style.display = "block";
      } else if (selectedService.value === "2") {
        camposAmbulancia.style.display = "block";
      } else if (selectedService.value === "3") {
        camposIncendios.style.display = "block";
      }
    }
  }

  servicioRadios.forEach((radio) => {
    radio.addEventListener("change", toggleFields);
  });

  // Ejecutar la función al cargar la página para manejar ediciones
  toggleFields();
});
