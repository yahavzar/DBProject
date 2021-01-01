var table = new Tabulator("#movie", {
        layout:"fitColumns",
        placeholder: "No Data Set",
    columns:[
    {title:"ApiId", field:"ApiId"},
    {title:"Title", field:"Title", hozAlign:"right", sorter:"number"},

    ],
});