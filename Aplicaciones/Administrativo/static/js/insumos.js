document.addEventListener("DOMContentLoaded", function () {
  // Selecciona todas las celdas con la clase 'stock-cell'
  const stockCells = document.querySelectorAll(".stock-cell");

  stockCells.forEach(function (cell) {
    // Obtener el valor de 'data-stock' y convertirlo a número
    const stockActual = parseInt(cell.getAttribute("data-stock"));

    // Aplicar el color de fondo basado en el valor de 'stock_actual'
    if (stockActual <= 10) {
      cell.style.backgroundColor = "#D12923";
    } else if (stockActual < 50) {
      cell.style.backgroundColor = "#F8BD4F";
    } else if (stockActual > 50) {
      cell.style.backgroundColor = "#30B52C";
    }
  });
});

$(document).ready(function () {
  $("#myTable").DataTable({
    language: {
      decimal: "",
      emptyTable: "No hay información",
      info: "Mostrando _START_ a _END_ de _TOTAL_ Entradas",
      infoEmpty: "Mostrando 0 to 0 of 0 Entradas",
      infoFiltered: "(Filtrado de _MAX_ total entradas)",
      infoPostFix: "",
      thousands: ",",
      lengthMenu: "Mostrar _MENU_ Entradas",
      loadingRecords: "Cargando...",
      processing: "Procesando...",
      search: "Buscar:",
      zeroRecords: "Sin resultados encontrados",
      paginate: {
        first: "Primero",
        last: "Ultimo",
        next: "Siguiente",
        previous: "Anterior",
      },
      buttons: {
        copy: "Copiar",
        colvis: "Visibilidad",
        collection: "Colección",
        colvisRestore: "Restaurar visibilidad",
        copyKeys:
          "Presione ctrl o u2318 + C para copiar los datos de la tabla al portapapeles del sistema. <br /> <br /> Para cancelar, haga clic en este mensaje o presione escape.",
        copySuccess: {
          1: "Copiada 1 fila al portapapeles",
          _: "Copiadas %ds fila al portapapeles",
        },
        copyTitle: "Copido al portapapeles",
        csv: "CSV",
        excel: "Excel",
        pageLength: {
          "-1": "Mostrar todas las filas",
          _: "Mostrar %d filas",
        },
        pdf: "PDF",
        print: "Imprimir",
        renameState: "Cambiar nombre",
        updateState: "Actualizar",
        createState: "Crear Estado",
        removeAllStates: "Remover Estados",
        removeState: "Remover",
        savedStates: "Estados Guardados",
        stateRestore: "Estado %d",
      },
    },
    dom: '<"d-flex justify-content-between"fB>rtip',
    buttons: [
      {
        extend: "copy",
        exportOptions: {
          columns: ":not(:last-child)", // Excluye la última columna (opciones)
        },
      },
      {
        extend: "excel",
        exportOptions: {
          columns: ":not(:last-child)", // Excluye la última columna (opciones)
        },
        customize: function (xlsx) {
          var sheet = xlsx.xl.worksheets["sheet1.xml"];
          $('row c[r^="A"]', sheet).attr("s", "2");
          $("row:first c", sheet).attr("s", "27");
        },
      },
      {
        extend: "pdf",
        exportOptions: {
          columns: ":not(:last-child)", // Excluye la última columna (opciones)
        },
        customize: function (doc) {
          // Cambiar el título
          doc.content[0].text = "Reporte";

          doc.content[1].table.widths = Array(
            doc.content[1].table.body[0].length + 1
          )
            .join("*")
            .split("");
          doc.defaultStyle.alignment = "center";
          doc.styles.tableHeader = {
            color: "white",

            alignment: "center",
            fontSize: 12,
            bold: true,
          };
          doc.content[0].alignment = "center";
          doc.content[0].fontSize = 16;
          doc.content[0].bold = true;
        },
      },
      {
        extend: "print",
        exportOptions: {
          columns: ":not(:last-child)", // Excluye la última columna (opciones)
        },
        customize: function (win) {
          $(win.document.body).css("font-size", "10pt");
          $(win.document.body)
            .find("table")
            .addClass("compact")
            .css("font-size", "inherit");

          // Cambiar el título
          $(win.document.body)
            .find("h1")
            .text("Reporte")
            .css("text-align", "center")
            .css("font-size", "18pt");

          $(win.document.body)
            .find("thead")
            .css("background-color", "#2196F3")
            .css("color", "white");
        },
      },
    ],
  });
});
