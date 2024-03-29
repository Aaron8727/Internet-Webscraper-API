from fastapi import FastAPI, HTTPException
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import time
import urllib.parse
app = FastAPI()
@app.get("/scrape/")
async def scrape_website(url: str):
    try:
        print(url)
        chrome_options = Options()
        #chrome_options.add_argument('--headless')
        driver = webdriver.Chrome(options=chrome_options)
        state = 'va'
        cityname= 'arlington'
        primary = '3109'
        street_number = '9th'
        st = "St"
        post_direction = 'N'
        street_name = f'{primary}%20{street_number}%20{st}%20{post_direction}'
        zip_5 = '22201'
        zip_9 = f'{zip_5}-2024'

        alconnect_url = f"https://www.allconnect.com/local/{state}/{cityname}?city={cityname}&primary={primary}&street_line={street_name}&street={street_number}%20{st}&postDirection={post_direction}&point=%7B%22latitude%22%3A38.883003%2C%22longitude%22%3A-77.095169%7D&state={state}&zip9={zip_9}&zip5={zip_5}&zip9or5={zip_9}&prettyAddress=3109%209th%20St%20N%2C%20Arlington%2C%20VA%2022201-2024&zip={zip_9}"

        driver.get(alconnect_url)
        time.sleep(5)
        '''
        try:
            # Wait until the element with class "mb-16" appears
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'article.title-card')))
            print("Element found!")
        except TimeoutException:
            print("Timed out waiting for element")
        '''
        html_text = driver.page_source
        """
        this was old system using requests instead of selenium
        response = requests.get(url)
        response.raise_for_status()
        html_text = response.text
        """
        soup = BeautifulSoup(html_text, 'lxml')
        Li_elements = soup.find_all('li', class_='mb-16 last:mb-0')
        scraped_data = [li.text for li in Li_elements]
        return {"here you go": scraped_data}
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail="Failed to fetch URL") from e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to scrape website") from e
