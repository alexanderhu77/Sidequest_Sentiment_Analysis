import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time


input_path = r'C:\Tian-Starter-Task\sidequest_links.csv'  
output_path= r'C:\Tian-Starter-Task\sidequest_review_scrape.csv' 


def extract_reviews_from_url(url, driver):
    reviews = []
    try:
        driver.get(url)
        time.sleep(3)  
        
        # Find all elements matching the review structure
        review_elements = driver.find_elements(By.CLASS_NAME, "mat-card-title")
        
        # Check if any review elements were found
        if review_elements:
            print(f"Found {len(review_elements)} elements {url}.")
            for element in review_elements:
                review_text = element.text.strip()
                reviews.append({'url': url, 'review': review_text})
        else:
            print(f"No elements found.")
    
    except Exception as e:
        print(f"Error {url}: {e}")
    
    return reviews




urls = pd.read_csv(input_path, header=None)[0].tolist()


chrome_options = Options() 
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)


all_reviews = []

# Iterate over all URLs and scrape reviews
for url in urls:  
    print(f"Processing URL: {url}")
    reviews = extract_reviews_from_url(url, driver)
    all_reviews.extend(reviews)
    time.sleep(3) 


driver.quit()


reviews_df = pd.DataFrame(all_reviews)
reviews_df.to_csv(output_path, index=False)
    

