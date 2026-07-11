import requests
from requests.adapters import HTTPAdapter, Retry
import bs4
from time import perf_counter

from config.log.log import Log
from infra.db.database import Database

class Scrap():
	logger = None
	request_timeout = (5, 20)

	def __init__(self, url):
		self.database = Database(database=False)
		self.logger = Log().initLog('scrap.log')
		self.session = requests.Session()
		retries = Retry(
			total=3,
			connect=3,
			read=3,
			status=3,
			backoff_factor=0.3,
			status_forcelist=[502, 503, 504],
			allowed_methods=frozenset(['GET', 'HEAD'])
		)
		adapter = HTTPAdapter(max_retries=retries)
		self.session.mount('http://', adapter)
		self.session.mount('https://', adapter)
		
		self.url = url

	def get_data(self):
		print(f'Getting data from URL: {self.url}')
		try:
			start_time = perf_counter()
			headers = {
				'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
				'accept-language': 'en-US,en;q=0.9',
				'cache-control': 'max-age=0',
				'priority': 'u=0, i',
				'sec-ch-ua': '"Brave";v="149", "Chromium";v="149", "Not)A;Brand";v="24"',
				'sec-ch-ua-mobile': '?0',
				'sec-ch-ua-platform': '"Linux"',
				'sec-fetch-dest': 'document',
				'sec-fetch-mode': 'navigate',
				'sec-fetch-site': 'same-origin',
				'sec-fetch-user': '?1',
				'sec-gpc': '1',
				'upgrade-insecure-requests': '1',
				'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36'
			}

			html = self.session.get(self.url, headers=headers, timeout=self.request_timeout)
			request_time = perf_counter() - start_time
			print(f'Request time: {request_time:.3f}s')
			Log().log(self.logger, 'info', f'Request time: {request_time:.3f}s')
			
			if html.status_code != 200:
				# self.database.deactivateMangaSite(self.url)
				Log().log(self.logger, 'error', f'Error: {html.status_code}')
				return None

			soup = bs4.BeautifulSoup(html.text, 'lxml')
			Log().log(self.logger, 'info', 'Data retrieved successfully')
			return soup
		except Exception as e:
			Log().log(self.logger, 'error', f'Error: {e}')

	def verificar_status(self):
		try:
			response = requests.get(self.url)
			return response.status_code
		except Exception as e:
			return e