/*

# skal ikke længere bruges til programmet da vi er overgået til dbdataparse.py

// secondary html parser, not used in the final project (csvdataparse.py is used instead)

var dontask = $.csv.toObjects('bildata.csv');

fetch('bil_data.csv')
    .then(response => response.text())
    .then(data => {
        const rows = data.split('\n');
        const sectionElement = document.querySelector('section');

        rows.forEach(row => {
            const columns = row.split(',');

            const rowElement = document.createElement('div');
            rowElement.className = 'row';

            columns.forEach(column => {
                const columnElement = document.createElement('div');
                columnElement.className = 'column';
                columnElement.textContent = column;

                rowElement.appendChild(columnElement);
            });

            sectionElement.appendChild(rowElement);
        });
    });

*/