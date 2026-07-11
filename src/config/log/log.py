import os
import logging

class Log:
	encoding = ''
	level = ''
	logFormat = ''
	datefmt = ''
	
	def __init__(self):
		self.encoding = 'utf-8'
		self.level = logging.DEBUG
		self.logFormat = '%(asctime)s | %(levelname)s | %(message)s'
		self.datefmt='%d/%m/%Y %I:%M:%S %p'
	
	def initLog(self, fileName):
		log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../logs')
		log_path = os.path.join(log_dir, fileName)
		
		logger = logging.getLogger(__name__)
		
		logging.basicConfig(
			filename= log_path,
			filemode='a',
			encoding = self.encoding,
			level = self.level,
			format=self.logFormat,
			datefmt=self.datefmt
		)

		return logger
	
	def log(self, logger, level, msg):
		match level:
			case 'debug':
				logger.debug(msg)
			case 'info':
				logger.info(msg)
			case 'warning':
				logger.warning(msg)
			case 'error':
				logger.error(msg)
			case 'critical':
				logger.critical(msg)
