import sqlite3
from datetime import datetime

def read_database():
    connection = sqlite3.connect('bil_data.db')
    cursor = connection.cursor()
    tables_query = "SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'bil_data_%' ORDER BY name DESC;"
    cursor.execute(tables_query)
    tables = cursor.fetchall()
    data = {}
    for table in tables:
        table_name = table[0]
        select_query = f"SELECT * FROM {table_name};"
        cursor.execute(select_query)
        columns = [column[0] for column in cursor.description]
        rows = cursor.fetchall()
        table_data = []
        for row in rows:
            row_dict = {col: val.decode('utf-8') if isinstance(val, bytes) else val for col, val in zip(columns, row)}
            table_data.append(row_dict)
        data[table_name] = {'table_data': table_data, 'num_records': len(table_data)}
    connection.close()
    return data

def generate_html(data):
    html_content = "<html><head><title>Data Output</title></head><body>"
    
    
    # Iterate through each table's data
    for table_name, table_info in data.items():
        
        # Extract the datetime from the table name
        table_datetime = datetime.strptime(table_name.split('_')[2], "%Y%m%d")
        table_datetime = table_datetime.replace(hour=int(table_name.split('_')[3][:2]), minute=int(table_name.split('_')[3][2:4]), second=int(table_name.split('_')[3][4:]))
        
        # Convert datetime to the desired format
        formatted_datetime = table_datetime.strftime('%d-%m-%Y %H:%M:%S')
        
        # Add section header with datetime and number of records
        num_records = table_info['num_records']
        html_content += f"<h2>Bildata fra dato: {formatted_datetime} - Antal biler: {num_records}</h2>"
        
        # Add table with data
        table_data = table_info['table_data']
        html_content += "<table border='1'><tr><th>Model</th><th>Pris</th><th>Dato</th><th>Lokation</th></tr>"
        for item in table_data:
            html_content += "<tr>"
            html_content += f"<td>{item['model']}</td>"
            html_content += f"<td>{item['pris']}</td>"
            html_content += f"<td>{item['dato']}</td>"
            html_content += f"<td>{item['lokation']}</td>"
            html_content += "</tr>"
        html_content += "</table>"
    
    html_content += "</body></html>"
    return html_content

def main():
    data = read_database()
    html_content = generate_html(data)    
    with open('bildata.html', 'w', encoding='utf-8') as file:
        file.write(html_content)

if __name__ == "__main__":
    main()
