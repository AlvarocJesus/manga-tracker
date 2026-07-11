import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import bs4
import json
import requests
from unidecode import unidecode

from config.log.log import Log
from infra.db.database import Database
from scrap import Scrap

class OldiSussy:
	logger = None

	def __init__(self):
		self.logger = Log().initLog('oldiSussy.log')
		self.scrap = Scrap()

	# url = 'https://oldi.sussytoons.com/manga/logando-10-000-anos-no-futuro/'

	"""  url = 'https://www.amazon.com.br/Monitor-Gamer-AOC-FreeSync-Q27G2/dp/B0C6FHZW5C'
	preço amazon

	def get_data(self, url):
		try:
			html = requests.get(url)
			soup = bs4.BeautifulSoup(html.text, 'html.parser')

			with open('teste.html', 'w', encoding='utf-8') as file:
				file.write(soup.prettify())
			
			Log().log(self.logger, 'info', 'Data retrieved successfully')
			return soup
		except Exception as e:
			Log().log(self.logger, 'error', f'Error: {e}') """

	def extract_data(self, soup):
		try:
			titulo = soup.find('div', class_='post-title').find('h1').text.strip()
			capitulo_recente = soup.find('ul', class_='main version-chap no-volumn').find_all('li')[0].find('a').text.strip().split(' ')[-1]
			ultimo_capitulo_link = soup.find('ul', class_='main version-chap no-volumn').find_all('li')[0].find('a')['href']

			Log().log(self.logger, 'info', 'Data extracted successfully')
			return { 'titulo': titulo, 'capitulo_mais_novo': capitulo_recente, 'ultimo_capitulo_link': ultimo_capitulo_link, 'total_capitulos': capitulo_recente }
		except Exception as e:
			Log().log(self.logger, 'error', f'Error: {e}')
	
	def saveManga(self, data):
		print(f'Data: {json.dumps(data, indent=2)}')
		mangaUpdate = {
			'titulo': data['titulo'],
			'total_caps': data['capitulo_mais_novo']
		}

		Database().updataManga(mangaUpdate)

	def run(self):
		# soup = self.get_data(self.url)
		soup = self.scrap.get_data(self.url)
		data = self.extract_data(soup)
		self.saveManga(data)

# OldiSussy().run()