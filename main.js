document.addEventListener("DOMContentLoaded", function () {
  const iniciarJornadaBtn = document.getElementById("iniciar-jornada-btn");

  // Verificar si el botón ya fue ocultado
  if (localStorage.getItem("jornadaIniciada") === "true") {
      iniciarJornadaBtn.style.display = ""; // Cambiado a "none" para ocultar el botón
  }

  // Ocultar el botón y mostrar la animación al hacer clic
  document
      .getElementById("iniciar-jornada-form")
      .addEventListener("submit", function (event) {
          event.preventDefault(); // Prevenir el envío del formulario para la animación

          // Aplicar animación de desvanecimiento
          iniciarJornadaBtn.classList.add("fade-out");

          // Esperar 1 segundo antes de enviar el formulario y ocultar el botón
          setTimeout(() => {
              localStorage.setItem("jornadaIniciada", "true");
              iniciarJornadaBtn.disabled = true; // Deshabilitar el botón después de iniciar la jornada
              iniciarJornadaBtn.style.display = "none"; // Cambiar a "none" para ocultar el botón
          }, 1000);

          // Enviar el formulario después de la animación
          setTimeout(() => {
              document.getElementById("iniciar-jornada-form").submit();
          }, 2000); // Esperar 2 segundos antes de enviar
      });
});

// Función para habilitar/deshabilitar el checkbox de "Repitió"
function toggleRepitio(checkbox) {
  const row = checkbox.closest('tr');
  const repitioCheckbox = row.querySelector('input[name^="Repitio_"]');

  repitioCheckbox.disabled = !checkbox.checked; // Habilita o deshabilita según "Almorzó"

  if (!checkbox.checked) {
      repitioCheckbox.checked = false; // Desmarca "Repitió" si "Almorzó" no está seleccionado
  }
}
