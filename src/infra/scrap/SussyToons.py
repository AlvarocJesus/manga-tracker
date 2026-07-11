import sys
import os
import requests
import bs4
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.log.log import Log
from scrap import Scrap

class SussyToons:
	logger = None
	# url = 'https://api-dev.sussytoons.site/obras/847'
	
	def __init__(self):
		self.logger = Log().initLog('sussyToons.log')
		self.scrap = Scrap()

	def get_data(self, url):
		try:
			headers = {
				'Accept': 'application/json, text/plain, */*',
				'Accept-Encoding': 'gzip, deflate, br, zstd',
				'Connection': 'keep-alive',
				'Host': 'api-dev.sussytoons.site',
				'Origin': 'https://www.sussytoons.site',
				'Referer': 'https://www.sussytoons.site/',
				'Sec-Fetch-Dest': 'empty',
				'Sec-Fetch-Mode': 'cors',
				'Sec-Fetch-Site': 'same-site',
				'Sec-GPC': '1',
				'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
				'accept-language': 'pt-br,pt;q=0.9,en-us;q=0.8,en;q=0.7',
				'scan-id': '1',
				'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Brave";v="132"',
				'sec-ch-ua-mobile': '?0',
				'sec-ch-ua-platform': "Windows"
			}

			html = requests.get(url, headers=headers)
			# soup = bs4.BeautifulSoup(html.text, 'html.parser')

			# with open('teste.json', 'w', encoding='utf-8') as file:
				# file.write(soup.prettify())
				# file.write(html.text)

			Log().log(self.logger, 'info', 'Data retrieved successfully')
			return html.json()
		except Exception as e:
			Log().log(self.logger, 'error', f'Error: {e}')

	def extract_data(self, soup):
		try:
			print('Extracting data...')

			titulo = soup['resultado']['obr_nome']
			capitulo_recente = soup['resultado']['capitulos'][0]['cap_nome']
			ultimo_capitulo_link = soup['resultado']['capitulos'][0]['cap_id']
			data_atualizacao = soup['resultado']['capitulos'][0]['cap_lancado_em']
			status_manga = soup['resultado']['status']['stt_nome']
			
			Log().log(self.logger, 'info', 'Data retrieved successfully')
			return { 'titulo': titulo, 'capitulo_mais_novo': capitulo_recente, 'ultimo_capitulo_link': 'https://www.sussytoons.site/capitulo/{ultimo_capitulo_link}', 'data_atualizacao': data_atualizacao, 'status_manga': status_manga }
		except Exception as e:
			Log().log(self.logger, 'error', f'Error: {e}')

	def saveManga(self, data):
		try:
			print('Saving data...')
			print(f'Data: {json.dumps(data, indent=2)}')
			Log().log(self.logger, 'info', 'Data saved successfully')
		except Exception as e:
			Log().log(self.logger, 'error', f'Error: {e}')

	def run(self, url):
		# soup = self.get_data(url)
		soup = self.scrap.get_data(url)
		data = self.extract_data(soup)
		self.saveManga(data)

# SussyToons().run()
		