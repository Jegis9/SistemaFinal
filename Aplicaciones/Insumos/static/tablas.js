document.addEventListener("DOMContentLoaded", function () {
  // Selecciona todas las celdas con la clase 'stock-cell'
  const stockCells = document.querySelectorAll(".stock-cell");

  stockCells.forEach(function (cell) {
    // Obtener el valor de 'data-stock' y convertirlo a número
    const stockActual = parseInt(cell.getAttribute("data-stock"), 10);

    // Verificar si 'stockActual' es un número válido
    if (isNaN(stockActual)) {
      console.warn(
        `Valor no numérico encontrado en data-stock: ${cell.getAttribute(
          "data-stock"
        )}`
      );
      return; // Saltar a la siguiente iteración
    }

    // Aplicar el color de fondo basado en el valor de 'stock_actual'
    if (stockActual <= 10) {
      cell.style.backgroundColor = "#D12923";
    } else if (stockActual < 50) {
      cell.style.backgroundColor = "#F8BD4F";
    } else {
      // Cambiar el último 'else if' a 'else' para cubrir todos los casos >= 50
      cell.style.backgroundColor = "#30B52C";
    }
  });
});
