from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time

MAX_WAIT_TIME = 30  # Maximale Wartezeit in Sekunden
NUM_SCROLLS = 2  # Anzahl der Scroll-Durchläufe
SLEEP_BETWEEN_SCROLLS = 3  # Zeit zwischen den Scroll-Durchläufen in Sekunden
CHANNEL_NAME = "@AfDFraktionimBundestag"


def init_driver():
    return webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

def scroll_page(driver, num_scrolls, sleep_time):
    for _ in range(num_scrolls):
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
        time.sleep(sleep_time)

def extract_video_data(driver):
    anchor_elements = driver.find_elements(By.CSS_SELECTOR, "a#video-title-link.yt-simple-endpoint")
    video_data = []
    for anchor in anchor_elements:
        link = anchor.get_attribute("href")
        title = anchor.get_attribute("title")
        if link and title:
            video_data.append({"title": title, "link": link})
    return video_data

def clean_channel_name(channel_name):
    return channel_name.replace("@", "")  # Entfernt das '@' für den Dateinamen

def write_to_csv(video_data, channel_name):
    filename = f"{clean_channel_name(channel_name)}_videos.csv"  # Generiert den Dateinamen
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['title', 'link']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in video_data:
            writer.writerow(row)

def main():
    driver = init_driver()
    driver.get(f"https://www.youtube.com/{CHANNEL_NAME}/videos")

    try:
        wait = WebDriverWait(driver, MAX_WAIT_TIME)
        wait.until(EC.presence_of_element_located((By.ID, "video-title")))

        scroll_page(driver, NUM_SCROLLS, SLEEP_BETWEEN_SCROLLS)

        video_data = extract_video_data(driver)
        
        write_to_csv(video_data, CHANNEL_NAME)  # Übergibt CHANNEL_NAME an die Funktion

        for data in video_data:
            print(f"Title: {data['title']}, Link: {data['link']}")

    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
    
