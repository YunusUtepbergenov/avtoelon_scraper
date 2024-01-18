from selenium import webdriver
from pandas import DataFrame
from bs4 import BeautifulSoup
import time
from selenium.webdriver.chrome.service import Service

column_names = ['link', 'название', 'цена', 'год', 'город', 'дата', 'двигатель', 'кузов', 'пробег', 'коробка', 'цвет', 'привод', 'описание']
dataframe = DataFrame(columns=column_names)
array = []

service = Service(executable_path=r"C:/SeleniumDrivers/chromedriver.exe")

options= webdriver.ChromeOptions()
options.add_argument("headless")
options.add_argument("--disable-gpu")
options.add_argument('--blink-settings=imagesEnabled=false')
options.add_argument('--log-level=3')

driver = webdriver.Chrome(service=service, options=options)

row = 1
for page in range(10000):
    print("Scraping page " + str(page+1))
    page_link = 'https://avtoelon.uz/avto/?page=' + str(page+1)
    for i in range(100):
        try:
            time.sleep(2)
            driver.get(page_link)
            break
        except:
            time.sleep(15)
            continue
    html_text = driver.page_source

    soup = BeautifulSoup(html_text, 'html.parser')
    cars = soup.find_all('div', class_="a-elem")

    for car in cars:
        list = []

        link_span = car.find('span', class_="a-el-info-title")
        car_url = link_span.find('a')
        url = 'https://www.avtoelon.uz' + car_url['href']

        dataframe.at[row, 'link'] = url
        dataframe.at[row, 'название'] = car_url.text

        car_price = car.find('span', class_="price").text
        dataframe.at[row, 'цена'] = car_price.replace("Цена: ", "")

        dataframe.at[row, 'год'] = car.find('span', class_="year").text.strip()
        dataframe.at[row, 'город'] = car.find('a', class_="a-info-text__region").text
        if car.find('span', class_="date"):
            dataframe.at[row, 'дата'] = car.find('span', class_="date").text
        else:
            dataframe.at[row, 'дата'] = "Null"

        for i in range(10000):
            try:
                time.sleep(2)
                driver.get(url)
                break
            except:
                time.sleep(15)
                continue

        car_page_html = driver.page_source
        soup = BeautifulSoup(car_page_html, 'html.parser')
        
        dt = soup.find_all('dt', class_="value-title")
        dd = soup.find_all('dd', class_="value clearfix")

        if dt:
            for ctr, d in enumerate(dt):
                if d:
                    if d.text == "Объем двигателя, л":
                        dataframe.at[row, 'двигатель'] = dd[ctr].text
                        break
                    else:
                        dataframe.at[row, 'двигатель'] = 'Null'

            for ctr, d in enumerate(dt):
                if d:
                    if d.text == "Кузов":
                        dataframe.at[row, 'кузов'] = dd[ctr].text
                        break
                    else:
                        dataframe.at[row, 'кузов'] = 'Null'

            for ctr, d in enumerate(dt):
                if d:
                    if d.text == "Пробег":
                        dataframe.at[row, 'пробег'] = dd[ctr].text.strip()
                        break
                    else:
                        dataframe.at[row, 'пробег'] = 'Null'
            for ctr, d in enumerate(dt):
                if d:
                    if d.text == "Коробка передач":
                        dataframe.at[row, 'коробка'] = dd[ctr].text
                        break
                    else:
                        dataframe.at[row, 'коробка'] = 'Null'
            for ctr, d in enumerate(dt):
                if d:
                    if d.text == "Привод":
                        dataframe.at[row, 'привод'] = dd[ctr].text
                        break
                    else:
                        dataframe.at[row, 'привод'] = 'Null'
            for ctr, d in enumerate(dt):
                if d:
                    if d.text == "Цвет":
                        dataframe.at[row, 'цвет'] = dd[ctr].text
                        break
                    else:
                        dataframe.at[row, 'цвет'] = 'Null'

        if soup.find('div', class_="description-text"):
            dataframe.at[row, 'описание'] = soup.find('div', class_="description-text").text
        else:
            dataframe.at[row, 'описание'] = "Null"
        row = row + 1
        time.sleep(3)

dataframe.to_excel('avtoelon_uz.xlsx')