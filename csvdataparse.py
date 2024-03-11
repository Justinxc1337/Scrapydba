import csv

def read_csv(filename):
    data = []
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    return data

def generate_html(data):
    html_content = "<html><head><title>Data Output</title></head><body><table border='1'><tr><th>Pris</th><th>Dato</th><th>Lokation</th></tr>"
    for item in data:
        html_content += "<tr>"
        html_content += f"<td>{item['pris']}</td>"
        html_content += f"<td>{item['dato']}</td>"
        html_content += f"<td>{item['lokation']}</td>"
        html_content += "</tr>"
    html_content += "</table></body></html>"
    return html_content

def main():
    data = read_csv('bil_data.csv')
    html_content = generate_html(data)    
    with open('bildata.html', 'w') as file:
        file.write(html_content)

if __name__ == "__main__":
    main()