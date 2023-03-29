function sub_table_render(row, index) {
  // Vérifiez si la ligne est déjà ouverte
  if (row.getTreeParent()) {
    row.getTreeParent().toggle();
  } else {
    // Sinon, chargez les données et ouvrez la ligne
    var rowData = row.getData();
    var subTableData = rowData.interventions;
    // Créez un élément de tableau pour la sous-table
    var subTableEl = document.createElement("div");
    // Créez une nouvelle sous-table avec les données et l'élément du tableau créé ci-dessus
    var subTable = new Tabulator(subTableEl, {
      data: subTableData,
      layout: "fitColumns",
      autoColumns: true,
    });
    // Ajoutez la sous-table à la ligne et ouvrez-la
    row.toggle();
    row.getElement().appendChild(subTableEl);
  }
}
function onclick_render(cell, formatterParams, onRendered) {
  const id = row.getData().id;
  $(".subTable" + id + "").toggle();
}

async function make_all() {
  const num_page = {};
  var limit = {};
  var combo = JSON.parse("{{ combo|escapejs }}");
  let url = "{% url 'get_data' page limit  %}";
  const Http = new XMLHttpRequest();
  Http.open("GET", url);
  Http.send();
  Http.onreadystatechange = function () {
    if (this.readyState === 4 && this.status === 200) {
      try {
        const tabledata = JSON.parse(Http.responseText.replace(/\n/g, ""));
        document.getElementById("value_nb_lines").innerHTML = tabledata.length;
        let col = get_column_dict(num_page, combo);
        var table = new Tabulator("#example-table", {
          data: tabledata, //assign data to table
          movableColumns: true,
          renderHorizontal: "virtual",
          layout: "fitColumns",
          pagination: "local",
          paginationSize: 10,
          paginationSizeSelector: [10, 25, 50, 100],
          columns: col,
          rowFormatter: function (row, e) {
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
          },
          //autoColumns:true,
          height: "80vh",
          rowHeight: 60,
          downloadRowRange: "selected",
          resizableRows: true,
          dataTreeStartExpanded: false,
          childIndent: 0,
          dataTree: true,
        });

        document
          .getElementById("download-csv")
          .addEventListener("click", function () {
            table.download("csv", "data.csv");
          });

        //trigger download of data.json file
        document
          .getElementById("download-json")
          .addEventListener("click", function () {
            table.download("json", "data.json");
          });

        //trigger download of data.html file
        document
          .getElementById("download-html")
          .addEventListener("click", function () {
            table.download("html", "data.html", { style: true });
          });
      } catch (err) {
        console.error("Error parsing JSON data:", err);
      }
    } else if (this.readyState === 4 && this.status !== 200) {
      console.error("Error retrieving data. Status code:", Http.status);
    }
  };
}
make_all();

// Appelle la fonction make_all
