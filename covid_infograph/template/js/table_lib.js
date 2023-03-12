var hideIcon = function (cell, formatterParams, onRendered) { //plain text value
    if (cell.getRow().getData().interventions != null && cell.getRow().getData().interventions.length > 0) {
        return cell.getRow().getData().interventions.length + " ↘️";
    } else {
        return "0 ❌";
    }
};
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
                frozen: true
            },
            {
                title: "Registry",
                field: "registry",
                visible: true,
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
                formatter: hideIcon, align: "center", title: "Interventions", headerSort: false, cellClick: function (e, cell, formatterParams) {
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
                maxHeight: 100,
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
                sorter: "string",
                frozen: true
            },
            {
                title: "Year",
                field: "year",
                visible: true,
                sorter: "number"
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
