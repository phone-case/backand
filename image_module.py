from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import requests
import random
import time
import requests

def to_eng(text):
    client_id = 'da4pBBoI_an3UAjZea1G'  # 자신의 Papago API 클라이언트 ID로 바꿔주세요
    client_secret = 'VC5119mo8E'  # 자신의 Papago API 클라이언트 시크릿으로 바꿔주세요

    url = "https://openapi.naver.com/v1/papago/n2mt"
    headers = {
        "X-Naver-Client-Id": client_id,
        "X-Naver-Client-Secret": client_secret
    }
    data = {
        "source": "ko",
        "target": "en",
        "text": text
    }

    response = requests.post(url, headers=headers, data=data)
   
    if response.status_code == 200:
        result = response.json()
        if 'message' in result and 'result' in result['message']:
            return result['message']['result']['translatedText']
   
    return "번역에 실패했습니다."

def searchimage(text):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # headless 모드로 실행
    
    driver = webdriver.Chrome(options=chrome_options)
    
    url = "https://lexica.art/"  # 대상 웹 페이지 URL로 변경
    driver.get(url)
    
    text_input = driver.find_element("id", "main-search") # 입력 필드 ID로 변경
    text_input.send_keys(text)
    
    generate_button = driver.find_element(By.XPATH, "/html/body/div/div[2]/div/div[2]/div[3]/div/button")
    generate_button.click()
    
    time.sleep(3)
    
    
    xpath_pattern = '/html/body/div/div[2]/div/div[2]/div[7]/div/div[{}]/div/a/img'
    
    start_image_count = random.randint(1, 10)
    
    image_up_count = random.randint(1, 5)
    
    max_image_count = 4 * image_up_count + start_image_count
    image_urls = []
    i = start_image_count
    while len(image_urls) < 4:
        xpath = xpath_pattern.format(i)
        try:
            image_element = driver.find_element("xpath", xpath)
            image_url = image_element.get_attribute("src")
            image_urls.append(image_url)
            i += image_up_count
        except NoSuchElementException:
            i += 1
            if (i>50):
                i = 1 + start_image_count
            # Handle the case where the image is not found by increasing i by 1
        
    
    #for url in image_urls:print("Image URL:", url)
    driver.quit()
    return image_urls

def create_image(text):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # headless 모드로 실행
    
    driver = webdriver.Chrome(options=chrome_options)
    
    driver.get("https://huggingface.co/spaces/dalle-mini/dalle-mini")
    
    iframe = driver.find_element(By.ID, "iFrameResizer0")
    
    driver.switch_to.frame(iframe)
    time.sleep(3)
    input_element = driver.find_element(By.CLASS_NAME, "gr-text-input")
    input_element.send_keys(text)
    
    button_element = driver.find_element(By.ID, "8")
    button_element.click()
    
    xpath_list = [
        '//*[@id="gallery"]/div[2]/div/button[1]/img',
        '//*[@id="gallery"]/div[2]/div/button[2]/img',
        '//*[@id="gallery"]/div[2]/div/button[3]/img',
        '//*[@id="gallery"]/div[2]/div/button[4]/img'
    ]
    
    image_urls = []
    
    for xpath in xpath_list:
        image_element = WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.XPATH, xpath)))
        image_url = image_element.get_attribute("src")
        image_urls.append(image_url)
    
    driver.quit()
    return image_urls
