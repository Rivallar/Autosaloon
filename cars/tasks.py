from autosaloon.celery import app

from cars.models import AutoSaloon


@app.task
def recheck_autos_and_dealers():
	for saloon in AutoSaloon.objects.all():
		saloon.save()
