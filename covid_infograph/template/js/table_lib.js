var hideIcon = function (cell, formatterParams, onRendered) { //plain text value
    return "<i>➕</i>";
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
                formatter: hideIcon, align: "center", title: "Interventions", headerSort: false, cellClick: function (e, row, formatterParams) {
                    const id = row.getData()._id;
                    $(".subTable" + id + "").toggle();
                }
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
