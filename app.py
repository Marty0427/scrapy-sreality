import psycopg2
from flask import Flask


app = Flask(__name__)
outputfile = 'output.html'

def html_file(outputfile):
    connection = psycopg2.connect(
            host="localhost",
            database = 'sreality',
            port="5432",
            user="postgres",
            password="password"
        )
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM offers")
    records = cursor.fetchall()
    
    with open(outputfile, mode = 'w', encoding='utf-8') as f:

        f.write('''<head>
                    <meta charset="utf-8">
                    <style>
                        body {
                        font-family: "Arial Unicode MS", Arial, sans-serif;
                        }
                    </style>
                </head>''')

        f.write(    "<table>\n")
        for row in records:
            f.write("  <tr>\n")
            f.write("    <td>{0}</td>\n".format(row[1].strip()))
            f.write("    <td><img src=\"{0}\" alt=\"{1}\"></td>\n".format(row[2].strip(), row[1].strip()))
            f.write("  </tr>\n")
        f.write(    "</table>")



@app.route('/')
def serve_html():
    with open(outputfile, 'r', encoding='utf-8') as f:
        html = f.read()
    return html

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
