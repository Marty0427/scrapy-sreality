# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import psycopg2

class SavingToPostgresPipeline(object):

    def __init__(self):
        self.create_connection()

    def create_connection(self):

        databasename = 'sreality'

        # Connect to the default PostgreSQL database
        self.connection = psycopg2.connect(
            host="localhost",
            port="5432",
            user="postgres",
            password="password"
        )

        self.cursor = self.connection.cursor()
        self.cursor.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{databasename}';")
        exists = self.cursor.fetchone()


        if not exists:
            # Create a new connection to the default database
            self.connection.set_isolation_level(0)
            self.connection.autocommit = True
            self.cursor = self.connection.cursor()
            self.cursor.execute(f"CREATE DATABASE {databasename};")
            self.cursor.close()
        # Close the connection to the default database
        self.connection.close()

        self.connection = psycopg2.connect(
            host="localhost",
            database=databasename,
            user="postgres",
            password="password")
        
        self.cursor = self.connection.cursor()

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS offers(
            id serial PRIMARY KEY,
            title text,
            image_url text
        )
        """)
        self.cursor.execute("""
        DELETE FROM offers *
        """)



    def process_item(self, item, spider):
        self.store_db(item)
        #we need to return the item below as scrapy expects us to!
        return item

    def store_db(self, item):


        self.cursor.execute(""" insert into offers (title, image_url) values (%s,%s)""", (
            item["title"],
            item["image_url"]
            
        ))

        self.connection.commit()


    def close_spider(self, spider):
        self.cursor.execute("SELECT * FROM offers")
        records = self.cursor.fetchall()

        with open('output.html', mode = 'w', encoding='utf-8') as f:

            f.write('''
                    <head>
                        <meta charset="utf-8">
                        <style>
                            body {
                            font-family: "Arial Unicode MS", Arial, sans-serif;
                            }
                        </style>
                    </head>
                    ''')

            f.write(    "<table>\n")
            for row in records:
                f.write("  <tr>\n")
                f.write("    <td>{0}</td>\n".format(row[1].strip()))
                f.write("    <td><img src=\"{0}\" alt=\"{1}\"></td>\n".format(row[2].strip(), row[1].strip()))
                f.write("  </tr>\n")
            f.write(    "</table>")

        self.cursor.close()
        self.connection.close()



class SrealityPipeline:
    def process_item(self, item, spider):
        return item
