from .utils import send_mail_registr
from school.celery import app

@app.task()
def send_mail_registr_celery(email):
    send_mail_registr(email)