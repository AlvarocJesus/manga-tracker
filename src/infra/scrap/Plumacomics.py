import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import json
from scrap import Scrap
from config.log.log import Log
from infra.db.database import Database

class Plumacomics:
	logger = False
	
	def __init__(self):
		self.logger = Log().initLog('Plumacomics.log')
		self.database = Database(database=False)
	
	def extract_data(self, soup, url):
		try:
			print(f'Lista: {soup.find('div', class_='col-12 chapters-list')}')
			if soup.find('div', class_='col-12 chapters-list') is None:
				print('Chapter list not found') # Log para depuração
				self.database.deactivateMangaSite(url)
				Log().log(self.logger, 'warning', 'Chapter list not found')
				return None

			titulo = soup.find('title').text.strip().split(' - ')[0]
			ultimo_capitulo = ' '.join(soup.find('div', class_='card').find_all('div')[1])#.find('a').find('h5').text.strip().replace(' ', '').split('\n')[:2])
			print({
				'titulo': titulo,
				'ultimo_capitulo': ultimo_capitulo,
			})
			# url_ultimo_capitulo = soup.find('div', class_='col-12 chapters-list').find_all('div')[0].find('a')['href']

			# Log().log(self.logger, 'info', 'Data extracted successfully')
			# return { 
			# 	'titulo': titulo,
			# 	'ultimo_capitulo': ultimo_capitulo,
			# 	'url_ultimo_capitulo': f'https://mangabr.net{url_ultimo_capitulo}'
			# }
		except Exception as e:
			print('Exception occurred') # Log para depuração
			Log().log(self.logger, 'error', f'Error: {e}')

	def format_data(self, data):
		print('Format data')
		print(json.dumps(data, indent=2))

	def run(self, url):
		soup = Scrap(url).get_data()
		print(f'Soup: {soup}')
		# if soup is None:
		# 	return None

		# data = self.extract_data(soup, url)
		# if data is None:
		# 	return None

		# self.format_data(data)

if __name__ == '__main__':
	Plumacomics().run('https://plumacomics.cloud/series/faca-matadora-de-porcos')