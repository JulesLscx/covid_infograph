import Handsontable from "handsontable";
import "handsontable/dist/handsontable.min.css";
import "pikaday/css/pikaday.css";

import { data } from "/js/constants";
import {
  alignHeaders,
  addClassesToRows,
  changeCheckboxCell
} from "/js/hooksCallbacks";

const example = document.getElementById("handsontable");

new Handsontable(example, {
  data,
  height: 450,
  colWidths: [100, 100, 100,100,100,100,100,100,100,100,100,100,100,100,100,100],
  colHeaders: [
    "_id",
    "year",
    "dateInserted",
    "datePublished",
    "doctype",
    "doi",
    "pmid",
    "linkout",
      "timesCited",
      "altmetric",
      "venue",
      "publisher",
      "title",
      "openAccess",
      "concepts",
    "meshTerms",
  ],
  columns: [
    { data: 1, type: "text" },
    { data: 2, type: "numeric" },
    { data: 3, type: "date", allowInvalid: false },
    {
      data: 4,
      type: "date",
      allowInvalid: false
    },
    { data: 5, type: "text" },
    {
      data: 6,
      type: "text"
    },
    {
      data: 7,
      type: "text"
    },
    {
        data: 8,
        type: "numeric",
      readOnly: true,
    },
    {
      data: 9,
      readOnly: true,
      },
        {
      data: 10,
      readOnly: true,
      },
            {
      data: 11,
      readOnly: true,
      },
                {
      data: 12,
      readOnly: true,
      },
                    {
      data: 13,
      readOnly: true,
      },
                        {
      data: 14,
      readOnly: true,
      },
                            {
      data: 15,
      readOnly: true,
      },
                                {
      data: 16,
      readOnly: true,
      }
  ],
  dropdownMenu: true,
  hiddenColumns: {
    indicators: true
  },
  contextMenu: true,
  multiColumnSorting: true,
  filters: true,
  rowHeaders: true,
  manualRowMove: true,
  afterGetColHeader: alignHeaders,
  afterOnCellMouseDown: changeCheckboxCell,
  beforeRenderer: addClassesToRows,
  licenseKey: "non-commercial-and-evaluation"
});
