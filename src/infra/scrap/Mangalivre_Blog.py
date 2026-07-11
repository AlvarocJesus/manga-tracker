from datetime import datetime
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import json
from scrap import Scrap
from config.log.log import Log
from infra.db.database import Database

class Mangalivre_Blog:
	logger = False
	
	def __init__(self):
		print('Initializing Mangalivre_Blog...')
		self.logger = Log().initLog('Mangalivre_Blog.log')
		self.database = Database(database=False)
	
	def extract_data(self, soup, url):
		try:
			print('Extracting data...')
			manga_chapters = soup.find('div', class_='manga-chapters')
			
			if manga_chapters is None:
				print('Chapter list not found')
				self.database.deactivateMangaSite(url)
				Log().log(self.logger, 'warning', 'Chapter list not found')
				return None

			titulo = soup.find('title').text.strip().split(' - ')[0]
			print(f'Extracted data: titulo={titulo}')
			
			ultimo_capitulo = soup.find('div', class_='manga-chapters').find('div', class_='chapters-container').find_all('li')[0].find('span', class_='chapter-number').text.strip().replace('Capítulo ', '').replace('Capitulo', '').strip()
			print(f'Extracted data: ultimo_capitulo={ultimo_capitulo}')
			
			url_ultimo_capitulo = soup.find('div', class_='manga-chapters').find('div', class_='chapters-container').find_all('li')[0].find('a', class_='read-button')['href']
			print(f'Extracted data: url_ultimo_capitulo={url_ultimo_capitulo}')

			Log().log(self.logger, 'info', 'Data extracted successfully')
			# return { 
			# 	'titulo': titulo,
			# 	'ultimo_capitulo': ultimo_capitulo,
			# 	'url_ultimo_capitulo': url_ultimo_capitulo
			# }
		except Exception as e:
			print('Exception occurred') # Log para depuração
			Log().log(self.logger, 'error', f'Error: {e}')

	def format_data(self, data):
		# print('Format data')
		# print(json.dumps(data, indent=2))

		self.database.updataManga(
			data['titulo'],
			data['ultimo_capitulo'],
			data['url_ultimo_capitulo'],
			datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
			data['site_id']
		)

	def run(self, url):
		print(f'Running Mangalivre_Blog with URL: {url}')
		soup = Scrap(url).get_data()
		if soup is None:
			return None

		data = self.extract_data(soup, url)
		if data is None:
			return None

		self.format_data(data)

if __name__ == '__main__':
	Mangalivre_Blog().run('https://mangalivre.blog/manga/blue-lock/')