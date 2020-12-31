
function table() {
    return  new Tabulator("#movies", {
                 //load row data from array
        layout: "fitColumns",      //fit columns to width of table
        responsiveLayout: "hide",  //hide columns that dont fit on the table
        tooltips: true,            //show tool tips on cells
        addRowPos: "top",          //when adding a new row, add it to the top of the table
        history: true,             //allow undo and redo actions on the table
        pagination: "local",       //paginate the data
        paginationSize: 7,         //allow 7 rows per page of data
        movableColumns: true,      //allow column order to be changed
        resizableRows: true,       //allow row order to be changed
        initialSort: [             //set the initial sort order of the data
            {column: "Title", dir: "asc"},
        ],
        columns: [                 //define the table columns
            {title: "Id", field: "apiId"},
            {title: "Title", field: "title"},
        ]
    });
}