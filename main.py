from mangum import Manum
import requests
from bs4 import BeautifulSoup
from fastapi import FastAPI

app = FastAPI()

main_url = 'https://fawzyabuzeid.net/our-sermons/'

@app.get('/get_things')
async def get_things():
    response = requests.get(main_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    result = soup.find('div', class_='row')
    lista = result.find_all('div', class_='col-md-6')

    data = []

    for item in lista:
        try:
            title_tag = item.find('h3').find('a')
            title = title_tag.text.strip()
            sermon_url = title_tag.get('href')

            # محاولة استخراج رابط الصوت
            audio_div = item.find('div', class_='sermon-btns')
            if audio_div:
                audio_url = audio_div.find('a').get('data-src')
            else:
                audio_url = None

            data.append({
                'title': title,
                'url': sermon_url,
                'audio': audio_url
            })
        except Exception as e:
            print(f"Error parsing item: {e}")

    return data

handler = Manum(app)
