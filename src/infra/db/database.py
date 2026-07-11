import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# import psycopg2
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

from config.log.log import Log

load_dotenv()

class Database:
	logger = None
	
	def __init__(self, database=True):
		self.logger = Log().initLog('database.log')
		self.database = os.getenv('DATABASE_URL') if database else os.getenv('SQLITE_DATABASE_URL')

	def getEngine(self):
		try:
			# conn = psycopg2.connect('dbname=postegre_notify_manga user=postegre_notify_manga_user password=8UesZFjtUpAtLGhcn7JZO8GrJlV0VZtN')
			# cursor = conn.cursor()

			engine = create_engine(self.database)

			Log().log(self.logger, 'info', 'Connection with database')
			# return conn, cursor
			return engine
		except Exception as e:
			Log().log(self.logger, 'error', e)

	def executeQuery(self, query, parameter={}):
		engine = self.getEngine()

		try:
			with engine.connect() as conn:
				teste = conn.execute(text(query), parameter)

				conn.commit()
				insertedId = teste.scalar()
				conn.close()
			return insertedId
		except Exception as e:
			Log().log(self.logger, 'error', e)

	def addManga(self, manga):
		insertedId = self.executeQuery(
			"""insert into mangas (id, nome, url_origem, ultimo_capitulo_lancado, total_cap, data_ultima_verificacao, site_id) values (:id, :nome, :url_origem, :ultimo_capitulo_lancado, :total_cap, :data_ultima_verificacao, :site_id) returning id_manga""",
			{
				'id': manga['id'],
				'nome': manga['nome'],
				'url_origem': manga['url_origem'],
				'ultimo_capitulo_lancado': manga['ultimo_capitulo_lancado'],
				'total_cap': manga['total_cap'],
				'data_ultima_verificacao': manga['data_ultima_verificacao'],
				'site_id': manga['site_id']
			}
		)

		return insertedId
	
	def addUserManga(self, userManga):
		insertedId = self.executeQuery(
			"""insert into manga_user (user_id,	manga_id,	capitulo_atual_usuario) values (:user_id,	:manga_id,	:capitulo_atual_usuario) returning id""",
			{
				'user_id': userManga['user_id'],
				'manga_id': userManga['manga_id'],
				'capitulo_atual_usuario': userManga['capitulo_atual_usuario']
			}
		)
		
		return insertedId

	def addSiteManga(self, siteManga):
		insertedId = self.executeQuery(
			"""insert into sites (id,	nome,	url_base,	slug_script, ativo) values (:id, :nome, :url_base, :slug_script, :ativo) returning id""",
			{
				'id': siteManga['id'],
				'nome': siteManga['nome'],
				'url_base': siteManga['url_base'],
				'slug_script': siteManga['slug_script'],
				'ativo': siteManga['ativo']
			}
		)

		return insertedId
	
	def addUser(self, user):
		insertedId = self.executeQuery(
			"""insert into users (id,	nome,	telegram_chat_id) values (:id, :nome, :telegram_chat_id) returning id""",
			{
				'id': user['id'],
				'nome': user['nome'],
				'telegram_chat_id': user['telegram_chat_id']
			}
		)

		return insertedId

	""" def getAllManga(self):
		conn, cursor = self.getEngine()

		try:
			mangas = cursor.execute('select * from manga with(nolock)')
			conn.commit()
			conn.close()

			Log().log(self.logger, 'info', 'Manga added')
			return mangas
		except Exception as e:
			Log().log(self.logger, 'error', e)
	
	def getMyMangas(self, userId):
		try:
			conn, cursor = self.getEngine()
			mangas = cursor.execute('select * from user_manga where user_id')
			conn.commit()
			conn.close()

			return mangas
		except Exception as e:
			Log().log(self.logger, 'error', e) """

	def updataManga(self, manga):
		try:
			engine = self.getEngine()

			with engine.connect() as conn:
				updated = conn.execute(
					text("""update manga set total_caps = :total_caps where name = :titulo"""),
					{'total_caps': manga['total_caps'], 'titulo': manga['id_manga']}
				)
				conn.commit()
				conn.close()
			
			Log().log(self.logger, 'info', 'Manga updated')
			return updated
		except Exception as e:
			Log().log(self.logger, 'error', e)

	def deactivateMangaSite(self, siteUrl=None):
		try:
			print(f'Deactivating site: {siteUrl}')
			self.executeQuery(
				'update sites set ativo = 0 where url_base = :siteUrl',
				{'siteUrl': siteUrl}
			)
		except Exception as e:
			Log().log(self.logger, 'error', e)

	def resetar_banco(self):
		# engine = self.getEngine()
		# print("🗑️ Apagando todas as tabelas...")
		# # Esse comando procura todas as tabelas mapeadas no Base e dropa do banco
		# Base.metadata.drop_all(bind=engine)
		
		# print("✨ Recriando as tabelas com a nova estrutura...")
		# # Esse comando cria tudo de novo
		# Base.metadata.create_all(bind=engine)
		
		# print("✅ Banco resetado com sucesso!")
		pass

if __name__ == "__main__":
	# pass
	db = Database(database=False)
	db.deactivateMangaSite()