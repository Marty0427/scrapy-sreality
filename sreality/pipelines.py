# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import psycopg2
import yaml
class SavingToPostgresPipeline(object):

    def __init__(self):

        #loads the docker-compose.yml file to read the postgres password
        with open("docker-compose.yml", "r") as stream:
            cfg = yaml.safe_load(stream)
            self.host = cfg['services']['scrapy']['environment']['POSTGRES_HOST']
            self.db = cfg['services']['scrapy']['environment']['POSTGRES_DB']
            self.user = cfg['services']['scrapy']['environment']['POSTGRES_USER']
            self.password = cfg['services']['scrapy']['environment']['POSTGRES_PASSWORD']
        self.create_connection()

    def create_connection(self):
      
        # Connect to the default PostgreSQL database
        self.connection = psycopg2.connect(
            host=self.host,
            database="postgres",
            port="5432",
            user=self.user,
            password=self.password
        )

        #check if the database exists
        self.cursor = self.connection.cursor()
        self.cursor.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{self.db}';")
        exists = self.cursor.fetchone()

        #if the databse does not exists, create it and close connection for postgres database
        if not exists:
            self.connection.set_isolation_level(0)
            self.connection.autocommit = True
            self.cursor = self.connection.cursor()
            self.cursor.execute(f"CREATE DATABASE {self.db};")
            self.cursor.close()
        self.connection.close()

        #connect to the target database
        self.connection = psycopg2.connect(
            host=self.host,
            database=self.db,
            port="5432",
            user=self.user,
            password=self.password)
        
        self.cursor = self.connection.cursor()

        #create table offers if it does not exists
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
        return item


    def store_db(self, item):

        #insert the data into the table
        self.cursor.execute(""" insert into offers (title, image_url) values (%s,%s)""", (
            item["title"],
            item["image_url"]
            
        ))

        self.connection.commit()


    def close_spider(self, spider):

        #load all data from the table
        self.cursor.execute("SELECT * FROM offers")
        records = self.cursor.fetchall()
        
        #create a static html file with the data
        with open('output.html', mode = 'w', encoding='utf-8') as f:

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

        self.cursor.close()
        self.connection.close()



class SrealityPipeline:
    def process_item(self, item, spider):
        return item
