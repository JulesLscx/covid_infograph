import { loadData } from "./utils/loadData";
function init(num_page, limit) {
  // Récupérer les données du serveur
  loadData(`{% url 'get_data' page limit %}`)
    .then((tableData) => {
      // Définir les colonnes
      const columns = get_column_dict(
        num_page,
        JSON.parse("{{ combo|escapejs }}")
      );
      // Créer le tableau
      const table = createTable(tableData, columns, {
        height: "80vh",
        rowHeight: 60,
        downloadRowRange: "selected",
        resizableRows: true,
        dataTreeStartExpanded: false,
        childIndent: 0,
        dataTree: true,
        movableColumns: true,
        renderHorizontal: "virtual",
        layout: "fitColumns",
        pagination: "local",
        paginationSize: 10,
        paginationSizeSelector: [10, 25, 50, 100],
        rowFormatter: rowFormatter,
      });
      // Ajouter les gestionnaires d'événements pour le téléchargement de données
      addDownloadHandlers(table);
    })
    .catch((error) => {
      console.error("Error loading data:", error);
    });
}

function addDownloadHandlers(table) {
  document.getElementById("download-csv").addEventListener("click", () => {
    table.download("csv", "data.csv");
  });
  document.getElementById("download-json").addEventListener("click", () => {
    table.download("json", "data.json");
  });
  document.getElementById("download-html").addEventListener("click", () => {
    table.download("html", "data.html", { style: true });
  });
}

function createTable(tableData, columns, options) {
  const table = new Tabulator("#example-table", {
    data: tableData,
    columns: columns,
    ...options, // Petite propagation d'objet pour ajouter les options
  });
  return table;
}

function rowFormatter(row, e) {
  if (num_page > 2) {
    return;
  }
  //create and style holder elements
  var holderEl = document.createElement("div");
  var tableEl = document.createElement("div");

  const id = row.getData()._id;
  holderEl.style.boxSizing = "border-box";
  holderEl.style.padding = "10px 10px 10px 10px";
  holderEl.style.borderTop = "1px solid #333";
  holderEl.style.borderBotom = "1px solid #333";
  holderEl.style.background = "#ddd";
  holderEl.setAttribute("class", "subTable" + id + "");

  tableEl.style.border = "1px solid #333";
  tableEl.setAttribute("class", "subTable" + id + "");

  holderEl.appendChild(tableEl);
  holderEl.classList.add("hidden");
  tableEl.classList.add("hidden");

  row.getElement().appendChild(holderEl);
  tableEl.setAttribute("class", "subTable" + id + "");
  if (
    !(row.getData().interventions === null) &&
    row.getData().interventions.length > 0
  ) {
    var subTable = new Tabulator(tableEl, {
      layout: "fitData",
      rowHeight: 60,
      height: 100,
      data: row.getData().interventions,
      columns: [
        {
          title: "Arm group lablels",
          field: "arm_group_label",
          formatter: "textarea",
        },
        { title: "Types", field: "types", formatter: "textarea" },
        {
          title: "Other names",
          field: "other_names",
          formatter: "textarea",
        },
        { title: "Name", field: "name", formatter: "textarea" },
        {
          title: "Description",
          field: "description",
          formatter: "textarea",
          widthGrow: 2,
        },
      ],
    });

    row.getElement().appendChild(holderEl);
  }
}

function loadData(url) {
  return new Promise((resolve, reject) => {
    fetch(url)
      .then((response) => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then((data) => {
        // Vérifier si les données sont valides
        if (!Array.isArray(data)) {
          throw new Error("Invalid data format: expected an array.");
        }
        // Renvoyer les données sous forme de tableau
        resolve(data);
      })
      .catch((error) => {
        console.error(`Error fetching data: ${error}`);
        reject(error);
      });
  });
}
