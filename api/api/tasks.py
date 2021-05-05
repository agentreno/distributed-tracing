from api.models import Event, Vulnerability
from eventapi.celery import app


@app.task(bind=True)
def process_events(self):
    for event in Event.objects.all():
        vuln = Vulnerability(data=event.data)
        vuln.save()
