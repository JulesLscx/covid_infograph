var hideIcon = function (cell, formatterParams, onRendered) { //plain text value
    if (cell.getRow().getData().interventions != null && cell.getRow().getData().interventions.length > 0) {
        return cell.getRow().getData().interventions.length + " ↘️";
    } else {
        return "0 ❌";
    }
};
//custom max min header filter
var minMaxFilterEditor = function (cell, onRendered, success, cancel, editorParams) {

    var end;

    var container = document.createElement("span");

    //create and style inputs
    var start = document.createElement("input");
    start.setAttribute("type", "number");
    start.setAttribute("placeholder", "Min");
    start.setAttribute("min", 0);
    start.setAttribute("max", 100);
    start.style.padding = "4px";
    start.style.width = "50%";
    start.style.boxSizing = "border-box";

    start.value = cell.getValue();

    function buildValues() {
        success({
            start: start.value,
            end: end.value,
        });
    }

    function keypress(e) {
        if (e.keyCode == 13) {
            buildValues();
        }

        if (e.keyCode == 27) {
            cancel();
        }
    }

    end = start.cloneNode();
    end.setAttribute("placeholder", "Max");

    start.addEventListener("change", buildValues);
    start.addEventListener("blur", buildValues);
    start.addEventListener("keydown", keypress);

    end.addEventListener("change", buildValues);
    end.addEventListener("blur", buildValues);
    end.addEventListener("keydown", keypress);


    container.appendChild(start);
    container.appendChild(end);

    return container;
}

//custom max min filter function
function minMaxFilterFunction(headerValue, rowValue, rowData, filterParams) {
    //headerValue - the value of the header filter element
    //rowValue - the value of the column in this row
    //rowData - the data for the row being filtered
    //filterParams - params object passed to the headerFilterFuncParams property

    if (rowValue) {
        if (headerValue.start != "") {
            if (headerValue.end != "") {
                return rowValue >= headerValue.start && rowValue <= headerValue.end;
            } else {
                return rowValue >= headerValue.start;
            }
        } else {
            if (headerValue.end != "") {
                return rowValue <= headerValue.end;
            }
        }
    }

    return true; //must return a boolean, true if it passes the filter.
}


function get_column_dict(page) {
    if (page < 3) {
        return [
            //First column is a selector
            {
                formatter: "rowSelection",
                frozen: true,
                titleFormatter: "rowSelection",
                hozAlign: "center",
                headerSort: false,
                cellClick: function (e, cell) {
                    cell.getRow().toggleSelect();
                }
            },
            {
                title: "Id",
                field: "_id",
                visible: true,
                sorter: "string",
                headerFilter: "input",
                headerFilterLiveFilter: false,
                frozen: true
            },
            {
                title: "Registry",
                field: "registry",
                visible: true,
                headerFilter: "input",
                headerFilterLiveFilter: false,
                sorter: "string"
            },
            {
                title: "Date inserted",
                field: "dateInserted",
                visible: true,
                formatter: format_date,
                sorter: sort_date
            },
            {
                title: "Date",
                field: "date",
                visible: true,
                formatter: format_date,
                sorter: sort_date
            },
            {
                title: "Linkout",
                field: "linkout",
                visible: true,
                sorter: "string",
                formatter: "link",
                formatterParams: { target: "_blank" }
            },
            {
                title: "Gender",
                field: "gender",
                editor: "list", editorParams: { values: { "Male": "Male", "Female": "Female", "All": "All", "N/A": "N/A", clearable: true } }, headerFilter: true, headerFilterParams: { values: { "Male": "Male", "Female": "Female", "All": "All", "N/A": "N/A" }, clearable: true },
                visible: true,
                sorter: "string"
            },
            {
                title: "Conditions",
                field: "conditions",
                visible: true,
                sorter: "string"
            },
            {
                formatter: hideIcon, sorter: "string", align: "center", title: "Interventions", cellClick: function (e, cell, formatterParams) {
                    const id = cell.getRow().getData()._id;
                    if (document.querySelector(".subTable" + id + "").style.display == "block") {
                        document.querySelector(".subTable" + id + "").style.display = "none";
                    } else {
                        document.querySelector(".subTable" + id + "").style.display = "block";
                    }
                }
            },
            {
                title: "Acronym",
                field: "acronym",
                visible: true,
                sorter: "string"
            },
            {
                title: "Title",
                field: "title",
                visible: true,
                sorter: "string",
                formatter: "textarea"
            },
            {
                title: "Abstract",
                field: "abstract",
                visible: true,
                sorter: "string",
                formatter: "html"
            },
            {
                title: "Phase",
                field: "phase",
                visible: true,
                sorter: "string"
            }
        ];
    } else {
        return [
            //First column is a selector
            {
                formatter: "rowSelection",
                frozen: true,
                titleFormatter: "rowSelection",
                hozAlign: "center",
                headerSort: false,
                cellClick: function (e, cell) {
                    cell.getRow().toggleSelect();
                }
            },
            {
                title: "Id",
                field: "_id",
                visible: true,
                headerFilter: "input",
                headerFilterLiveFilter: false,
                sorter: "string",
                frozen: true
            },
            {
                title: "Year",
                field: "year",
                visible: true,
                sorter: "number",
                headerFilter: minMaxFilterEditor, headerFilterFunc: minMaxFilterFunction, headerFilterLiveFilter: false
            },
            {
                title: "Date Inserted",
                field: "dateInserted",
                visible: true,
                formatter: format_date,
                sorter: sort_date
            },
            {
                title: "Date Published",
                field: "datePublished",
                visible: true,
                formatter: format_date,
                sorter: sort_date
            },
            {
                title: "Document Type",
                field: "docType",
                visible: true,
                sorter: "string"
            },
            {
                title: "DOI",
                field: "doi",
                visible: true,
                sorter: "string"
            },
            {
                title: "pmid",
                field: "pmid",
                visible: true,
                headerFilter: "input",
                headerFilterLiveFilter: false,
                sorter: "string"
            },
            {
                title: "Linkout",
                field: "linkout",
                visible: true,
                sorter: "string",
                formatter: "link",
                formatterParams: { target: "_blank" },
                maxInitialWidth: 200
            },
            {
                title: "Times Cited",
                field: "timesCited",
                visible: true,
                sorter: "number"
            },
            {
                title: "Altmetric Score",
                field: "altmetric",
                visible: true,
                sorter: "number"
            },
            {
                title: "Venue",
                field: "venue",
                visible: true,
                sorter: "string"
            },
            {
                title: "Publisher",
                field: "publisher",
                visible: true,
                sorter: "string"
            },
            {
                title: "Title",
                field: "title",
                visible: true,
                sorter: "string",
                formatter: "textarea",
                maxInitialWidth: 400
            },
            {
                title: "Open Access",
                field: "openAccess",
                visible: true,
                sorter: "string"
            },
            {
                title: "Concepts",
                field: "concepts",
                visible: true,
                sorter: "string",
                formatter: "textarea",
                maxInitialWidth: 400
            },
            {
                title: "Mesh Terms",
                field: "meshTerms",
                visible: true,
                sorter: "string",
                formatter: "textarea",
                maxInitialWidth: 400
            }
        ];
    }
}




function sort_date(a, b) {
    try {
        var dateA = luxon.DateTime.fromISO(a.$date);
    } catch (e) {
        return -1;
    }
    try {
        var dateB = luxon.DateTime.fromISO(b.$date);
    } catch (e) {
        return 1;
    }
    if (dateA < dateB) {
        return -1;
    } else if (dateA > dateB) {
        return 1;
    } else {
        return 0;
    }
}

function format_date(cell, formatterParams, onRendered) {
    var value = cell.getValue();
    if (value) {
        var date = luxon.DateTime.fromISO(value.$date);
        return date.toFormat("dd/MM/yyyy");
    } else {
        return "";
    }
}
