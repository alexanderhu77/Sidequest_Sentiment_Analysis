from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import csv
from selenium.webdriver.common.keys import Keys


url = 'https://sidequestvr.com/category/all'  
driver = webdriver.Chrome()
driver.get(url)


WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a.ng-star-inserted[tabindex="-1"]')))


def click_center():
    window_size = driver.get_window_size()
    center_x = window_size['width'] // 2
    center_y = window_size['height'] // 2
    actions = ActionChains(driver)
    actions.move_by_offset(center_x, center_y).click().perform()
    time.sleep(1)
click_center()

def scroll_down_by_keypress(pause=0.01, max_checks=5):
    
    body = driver.find_element(By.TAG_NAME, "body")
    
    # Checks used to make sure not reaching end of page
    checks = 0
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    while True:
        # Press the down arrow
        body.send_keys(Keys.ARROW_DOWN)
        time.sleep(pause)
        
        # Get the new scroll height and compare it to the previous height
        new_height = driver.execute_script("return document.body.scrollHeight")
        
        if new_height == last_height:
            checks += 1
            if checks >= max_checks:
                break
        else:
            checks = 0 
        
        
        last_height = new_height

print ("checkpoint 1")

links = set()
max_links = 100 


while len(links) < max_links:
    
    scroll_down_by_keypress()

    content = driver.page_source
    soup = BeautifulSoup(content, 'html.parser')

    # Select anchor tags with specific attributes and classes
    app_links = soup.select('a.ng-star-inserted[tabindex="-1"]')
    

    
    for link in app_links:
        if len(links) >= max_links:  
            break 
        
        link_url = link['href']  # Get the href attribute
        links.add("https://sidequestvr.com" + link_url)  

    
    print(f"Links collected: {len(links)}")


print(f"Total links collected: {len(links)}")
for url in links:
    print(url)
print (links)

file_path = r"C:\YOUR PATH\sidequest_links.csv"  


with open(file_path, mode='w', newline='') as file:
    writer = csv.writer(file)

    for url in links:
        writer.writerow([url])



driver.quit()