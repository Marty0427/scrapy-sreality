# scrapy-sreality
**Task**: Use scrapy framework to scrape the first 500 items (title, image url) from sreality.cz (flats, sell) and save it in the Postgresql database. Implement a simple HTTP server in python and show these 500 items on a simple page (title and image) and put everything to single docker-compose command so that I can just run "docker-compose up" in the Github repository and see the scraped ads on http://127.0.0.1:8080 page.

## Usage
- provide the password for postgres user in *docker-compose.yml* file
- **docker-compose up**
- server is deployed on http://127.0.0.1:8080 adress

## Scraping
usage: **run_spider.py**
- scrapes first 500 flats for sale on sreality.cz
- uses sreality api (described here: https://www.vut.cz/www_base/zav_prace_soubor_verejne.php?file_id=148805), no api documentation available
- store the items to postgres DB
- at the end of scraping creates a simple html file *output.html*, that displays the name of the offer and first picture

## Database
- database configuration is taken from *docker-compose.yml* file
- connects as *postgres* user and creates the database *sreality*, if it does not exists
- in database *sreality* creates table *offers* where the data are stored

## Server
usage: **app.py**
- creates a http server on port 8080 and displays the *output.html* file