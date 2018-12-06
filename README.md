# CIS 4290 Web Scraper
This is a basic web scraper written in Python.
The website we are scraping is https://www.security.stackexchange.com.
The data we collect with the scraper are all relevant questions (with a minimum number of answers), answers, comments, and user/user metrics.
All collected data is stored in a sqlite3 database and pushed to the webpages served by Flask.

## Requirements
We developed and tested this application in a Python3 virtual environment.
https://docs.python.org/3.6/tutorial/venv.html
Python 3.6 is required for the application to function properly.

To install the required modules run:
`pip install -r requirements.txt`

## Configuring the web scraper
All relevant scraper files are located in [/scraper-files](/scraper-files)

### Change the number of pages per tag that are scraped
[/scraper-files/functions.py](scraper-files/functions.py) contains the code in which you can change the number of pages to scrape per tag
```
# change the range of pages to increase the amount of pages. 1 page = 50 questions.
pages = [str(i) for i in range(1,6)]
```

### Change the minimum number of answers required on a question
[/scraper-files/functions.py](scraper-files/functions.py)
To change the minimum number of answers required, change the integer below
```
if not isNotAnswered and answerCount >= 5:
```

## Running the web scraper
[/scraper-files/run.py](scraper-files/run.py) contains the code to run the web scraper
URLs are provided to the scrape_pages() function.  These URLs point to the questions of a specific StackExchange tag.
```
scrape_pages('https://security.stackexchange.com/questions/tagged/iot?page=')
scrape_pages('https://security.stackexchange.com/questions/tagged/cloud-computing?page=')
scrape_pages('https://security.stackexchange.com/questions/tagged/mobile?page=')
```
To change which tags are being scraped, simply add/delete/replace the URLs.

In a terminal, navigate to /flask-scraper/scraper-files/ and run:
```
python run.py
```
Once the scraper has finished it will display metrics on the data collected and written to csv files.

## Pushing from CSV to the database
Navigate back to the root directory of the project /flask-scraper and run the file [csvtodb.py](csvtodb.py):
```
python csvtodb.py
```

## Starting the Flask server
In the root directory of the project /flask-scraper run [run.py](run.py):
```
python run.py
```
In your browser go to localhost:8000 to view the webpage.
