import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'autosaloon.settings')

app = Celery('autosaloon')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


# celery beat tasks
app.conf.beat_schedule = {
	'recheck_autos_and_dealers': {
		'task': 'cars.tasks.recheck_autos_and_dealers',
		'schedule': crontab(minute=0, hour='*/1'),
			},
	'saloons_are_buying': {
		'task': 'trading.tasks.saloons_are_buying',
		'schedule': crontab(minute='*/10'),
			},
		}
