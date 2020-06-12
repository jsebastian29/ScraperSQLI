# ScraperSQLI
Python script that uses Scrapy for getting SQL injection vulnerable web pages

# Usage
In the file *dorks.txt* you have to put the dorks to analyze, for example *products.php?id=*. When you run the script it'll ask you for the number of pages to check in Google for that dork, if you write 2 pages it'll check 20 results of that dork. When the script finishes it generates a new file named *vulnerable_urls_txt* containing all the urls found with sql injection vulnerability.

### Note
Use it carefully to prevent being banned for Google.
