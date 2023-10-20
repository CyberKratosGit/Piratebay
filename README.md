**Piratebay Movie Notifier**


**Description**

This script automatically scrapes movie titles from The Pirate Bay and notifies the user when new movies are released. It is designed to be run periodically, and on each run, it will compare the current list of movies on the site to the previously scraped list. If there are new movie releases, a Windows notification will be displayed to inform the user.

**Features**

Uses Selenium for web scraping.
Employs Fuzzy Matching to process and deduplicate movie titles.
Notifies the user of new releases via Windows notifications.
Stores the refined list of movie titles for future reference and comparison.

**Setup & Requirements**

1. Install the necessary Python libraries:

pip install selenium fuzzywuzzy plyer

2. Download ChromeDriver and place it in a known location on your computer.

https://sites.google.com/a/chromium.org/chromedriver/downloads

3. Update the driver_path variable in the script to point to the location of ChromeDriver.

**Usage**

python path_to_script.py

Make sure to replace path_to_script.py with the path to your Python script.

On each run, the script will scrape the latest movie titles, compare them to the titles from the previous run, and notify you of any new releases.
