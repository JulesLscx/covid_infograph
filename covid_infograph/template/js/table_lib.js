var hideIcon = function (cell, formatterParams, onRendered) { //plain text value
    if (cell.getRow().getData().interventions != null && cell.getRow().getData().interventions.length > 0) {
        return cell.getRow().getData().interventions.length + " ↘️";
    } else {
        return "0 ❌";
    }
};
var dateFilterEditor = function (cell, onRendered, success, cancel, editorParams) {

    var container = document.createElement("span");
    //create and style input
    var start = document.createElement("input");
    start.type = 'date';
    start.placeholder = 'Start';

    var end = document.createElement("input");
    end.type = 'date';
    end.placeholder = 'End';

    container.appendChild(start);
    container.appendChild(end);

    var inputs = container.querySelectorAll("input");


    inputs.forEach(function (input) {
        input.style.padding = '4px';
        input.style.width = '50%';
        input.style.boxSizing = 'border-box';
        input.value = cell.getValue();
    });

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
    start.addEventListener("change", buildValues);
    start.addEventListener("blur", buildValues);
    start.addEventListener("keydown", keypress);

    end.addEventListener("change", buildValues);
    end.addEventListener("blur", buildValues);
    end.addEventListener("keydown", keypress);

    return container;
}

//custom filter function
function dateFilterFunction(headerValue, rowValue, rowData, filterParams) {
    //headerValue - the value of the header filter element
    //rowValue - the value of the column in this row
    //rowData - the data for the row being filtered
    //filterParams - params object passed to the headerFilterFuncParams property

    function isValid(d) {
        return d instanceof Date && !isNaN(d);
    }
    var s = headerValue.start.split('-');
    var e = headerValue.end.split('-');
    var start = new Date(s[0], s[1] - 1, s[2]);
    var end = new Date(e[0], e[1] - 1, e[2]);
    console.log(typeof end);
    var values = rowValue.$date.split('-');
    var value = new Date(values[0], values[1] - 1, values[2].split('T')[0]);
    if (rowValue) {
        if (isValid(start)) {
            if (isValid(end)) {
                return value >= start && value <= end;
            } else {
                return value >= start;
            }
        } else {
            if (isValid(end)) {
                return value <= end;
            }
        }
    }
    return true;
}

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
        if (rowValue == '0')
            return false;
        if (headerValue.start != "") {
            if (headerValue.end != "") {
                return rowValue >= headerValue.start && rowValue <= headerValue.end;
            } else {
                return rowValue != null && rowValue >= headerValue.start;
            }
        } else {
            if (headerValue.end != "") {

                return rowValue <= headerValue.end;
            }
        }
    }

    return true; //must return a boolean, true if it passes the filter.
}


function get_column_dict(page, combo) {
    console.log(combo);
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
                width: 150,
                visible: true,
                sorter: "string",
                headerFilter: "input",
                headerFilterLiveFilter: false,
                frozen: true
            },
            {
                title: "Registry",
                field: "registry",
                width: 100,
                visible: true,
                headerFilter: "input",
                headerFilterLiveFilter: false,
                sorter: "string"
            },
            {
                title: "Date inserted",
                field: "dateInserted",
                width: 150,
                visible: true,
                formatter: format_date,
                sorter: sort_date,
                headerFilter: dateFilterEditor, headerFilterFunc: dateFilterFunction
            },
            {
                title: "Date",
                field: "date",
                width: 150,
                visible: true,
                formatter: format_date,
                sorter: sort_date,
                headerFilter: dateFilterEditor, headerFilterFunc: dateFilterFunction
            },
            {
                title: "Linkout",
                field: "linkout",
                width: 200,
                visible: true,
                sorter: "string",
                formatter: "link",
                headerFilter: "input",
                headerFilterLiveFilter: false,
                formatterParams: { target: "_blank" }
            },
            {
                title: "Gender",
                field: "gender",
                editor: "list", headerFilter: true, headerFilterParams: { values: { "Male": "Male", "Female": "Female", "All": "All", "N/A": "N/A" }, clearable: true },
                visible: true,
                width: 50,
                sorter: "string"
            },
            {
                title: "Conditions",
                field: "conditions",
                visible: true,
                width: 200,
                formatter: "textarea",
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
                }, width: 50, headerSort: false, hozAlign: "center", headerFilter: "input", headerFilterLiveFilter: false
            },
            {
                title: "Acronym",
                field: "acronym",
                visible: true,
                sorter: "string",
                headerFilter: "input",
                width: 100,
            },
            {
                title: "Title",
                field: "title",
                visible: true,
                width: 450,
                sorter: "string",
                formatter: "textarea"
            },
            {
                title: "Abstract",
                field: "abstract",
                visible: true,
                width: 450,
                sorter: "string",
                formatter: "textarea"
            },
            {
                title: "Phase",
                field: "phase",
                visible: true,
                width: 80,
                editor: "list", headerFilter: true, headerFilterParams: { values: { "Phase 4": "Phase 4", "Phase 3": "Phase 3", "Phase 2/3": "Phase 2/3", "Phase 2": "Phase 2", "Phase 1/2": "Phase 1/2", "Phase 1": "Phase 1", "N/A": "N/A" }, clearable: true },
                sorter: "string",

            },
            {
                title: "Authors",
                field: "authors",
                visible: true,
                sorter: "string",
                headerFilter: "input",
                width: 400,
                formatter: "textarea"
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
                width: 150,
                visible: true,
                headerFilter: "input",
                headerFilterLiveFilter: false,
                sorter: "string",
                frozen: true
            },
            {
                title: "Year",
                field: "year",
                width: 100,
                visible: true,
                sorter: "number",
                headerFilter: minMaxFilterEditor, headerFilterFunc: minMaxFilterFunction, headerFilterLiveFilter: true
            },
            {
                title: "Date Inserted",
                field: "dateInserted",
                visible: true,
                formatter: format_date,
                sorter: sort_date,
                width: 150,
                headerFilter: dateFilterEditor, headerFilterFunc: dateFilterFunction
            },
            {
                title: "Date Published",
                field: "datePublished",
                visible: true,
                width: 150,
                formatter: format_date,
                sorter: sort_date,
                headerFilter: dateFilterEditor, headerFilterFunc: dateFilterFunction

            },
            {
                title: "Document Type",
                field: "doctype",
                visible: true,
                sorter: "string",
                headerFilter: "input",
                width: 100
            },
            {
                title: "DOI",
                field: "doi",
                visible: true,
                sorter: "string",
                headerFilter: "input",
                width: 150
            },
            {
                title: "pmid",
                field: "pmid",
                visible: true,
                headerFilter: "input",
                sorter: "string",
                width: 150
            },
            {
                title: "Linkout",
                field: "linkout",
                visible: true,
                sorter: "string",
                formatter: "link",
                formatterParams: { target: "_blank" },
                maxInitialWidth: 200,
                width: 200,
                headerFilter: "input",
            },
            {
                title: "Times Cited",
                field: "timesCited",
                visible: true,
                sorter: "number",
                width: 80,
                headerFilter: minMaxFilterEditor, headerFilterFunc: minMaxFilterFunction, headerFilterLiveFilter: false

            },
            {
                title: "Altmetric Score",
                field: "altmetric",
                visible: true,
                width: 80,
                sorter: "number",
                headerFilter: minMaxFilterEditor, headerFilterFunc: minMaxFilterFunction, headerFilterLiveFilter: false

            },
            {
                title: "Venue",
                field: "venue",
                headerFilter: true, headerFilterParams: { values: combo.venue, clearable: true, multiselect: true },
                headerFilter: 'select',
                headerFilterFunc: "in",
                editor: "list", editorParams: { values: combo.venue, clearable: true },
                visible: true,
                sorter: "string",
                width: 150
            },
            {
                title: "Publisher",
                field: "publisher",
                headerFilter: true, headerFilterParams: { values: combo.publisher, clearable: true, multiselect: true },
                headerFilter: 'select',
                headerFilterFunc: "in",
                editor: "list", editorParams: { values: combo.publisher, clearable: true },
                visible: true,
                sorter: "string",
                width: 150
            },
            {
                title: "Title",
                field: "title",
                visible: true,
                sorter: "string",
                formatter: "textarea",
                maxInitialWidth: 400,
                width: 400
            },
            {
                title: "Open Access",
                field: "openAccess",
                visible: true,
                sorter: "string",
                width: 100,
            },
            {
                title: "Concepts",
                field: "concepts",
                visible: true,
                headerFilter: "input",
                sorter: "string",
                formatter: "textarea",
                maxInitialWidth: 400,
                width: 400
            },
            {
                title: "Mesh Terms",
                field: "meshTerms",
                visible: true,
                sorter: "string",
                formatter: "textarea",
                maxInitialWidth: 400,
                width: 400,
                headerFilter: "input"
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
