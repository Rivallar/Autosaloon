import pytest
from pytest_factoryboy import register
from django.db import connections


import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from tests.factories import AutosaloonFactory

register(AutosaloonFactory)


def run_sql(sql):
	conn = psycopg2.connect(database='postgres', user='Autosaloon')
	conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
	cur = conn.cursor()
	cur.execute(sql)
	conn.close()
	
	
@pytest.fixture(scope='session')
def django_db_setup():
	from django.conf import settings
	
	#settings.DATABASES['default']['NAME'] = 'the_copied_db'
	
	#run_sql('DROP DATABASE IF EXISTS the_copied_db')
	#run_sql('CREATE DATABASE the_copied_db TEMPLATE postgres')
	
	#yield
	
	#for connection in connections.all():
	#	connection.close()
		
	#run_sql('DROP DATABASE the_copied_db')

	settings.DATABASES['default'] = {
		'ENGINE': 'django.db.backends.postgresql',
		'HOST': 'localhost',
		'NAME': 'postgres'
	}
