from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from fuzzywuzzy import fuzz
import re
from plyer import notification
import time

# Set up the driver
driver_path = r"C:\Users\David\Downloads\chromedriver.exe"
service = Service(driver_path)
driver = webdriver.Chrome(service=service)

def process_and_normalize_titles(movie_titles):
    # Updated keywords list
    keywords = ["1080p", "720p", "480p", "2160p", "4k", "UHD", "DTS", "AC3", "AAC", "5.1", "7.1",
                "x264", "x265", "H.264", "HEVC", "Eng", "English", "Hindi", "DualAudio", "Multi",
                "Dubbed", "Subs", "BluRay", "WEBRip", "WEB-DL", "HDRip", "DVDRip", "BRRip", "Extended",
                "Director's Cut", "Remastered", "WEB", "HDTV", "DDP5.1", "NF", "[TGx]", "MeGusta",
                "ETHEL", "ELEANOR", "EDITH", "TORRENTGALAXY"]

    normalized_titles = []
    for title in movie_titles:
        processed_title = title.lower()
        processed_title = re.sub(r'[^a-z\s]', '', processed_title)  # Remove non-alphabetical characters
        for keyword in keywords:
            processed_title = processed_title.replace(keyword.lower(), "")
        normalized_title = ' '.join(processed_title.split()).strip()  # Remove extra spaces
        normalized_titles.append(normalized_title)
    return normalized_titles

def optimized_deduplication(titles):
    filtered_titles = []
    for title in titles:
        is_duplicate = any(fuzz.ratio(title, filtered_title) > 80 for filtered_title in filtered_titles)
        if not is_duplicate:
            filtered_titles.append(title)
    return filtered_titles

# Get new titles and compare with old ones
def get_new_titles(old_titles, current_titles):
    return [title for title in current_titles if title not in old_titles]

# Show Windows Notification
def show_notification(new_titles):
    if new_titles:
        message = f"New Movies: {', '.join(new_titles[:3])} and {len(new_titles) - 3} more" if len(new_titles) > 3 else ', '.join(new_titles)
        notification.notify(
            title="New Movies Released",
            message=message,
            timeout=10
        )

# Existing code for scraping remains largely unchanged

# Navigate to the initial page to find the last page number
url = "https://thepiratebay.party/browse/207"
driver.get(url)
page_elements = driver.find_elements(By.CSS_SELECTOR, "a[href^='/browse/207/']")
last_page = 0

for elem in page_elements:
    try:
        page_num = int(elem.text)
        if page_num > last_page:
            last_page = page_num
    except ValueError:
        pass

all_titles = []

# Loop through all pages and scrape data
for page in range(last_page + 1):
    driver.get(f"https://thepiratebay.party/browse/207/{page}/3")
    movie_elements = driver.find_elements(By.CSS_SELECTOR, "td > a[title^='Details for']")
    movie_titles = [element.text for element in movie_elements]
    all_titles.extend(movie_titles)
    time.sleep(2)  # Rate limiting

# Clean up and close the browser
driver.quit()

# Process and filter the titles
normalized_movie_titles = process_and_normalize_titles(all_titles)
refined_movie_titles = optimized_deduplication(normalized_movie_titles)

# Define the file path for storing movie titles
file_path = "all_refined_movie_titles.txt"

# Load old titles and compare with new ones
try:
    with open(file_path, 'r', encoding='utf-8') as file:
        old_titles = file.read().splitlines()
except FileNotFoundError:
    old_titles = []

new_titles = get_new_titles(old_titles, refined_movie_titles)

# Show Windows Notification if there are new titles
show_notification(new_titles)

# Append only the new titles to the file
if new_titles:
    with open(file_path, 'a', encoding='utf-8') as file:
        for title in new_titles:
            file.write(title + '\n')

print(f"{len(new_titles)} new movie titles have been added to {file_path}")
