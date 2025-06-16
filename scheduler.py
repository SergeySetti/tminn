import os
import time
from datetime import datetime

from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.jobstores.mongodb import MongoDBJobStore
from apscheduler.schedulers.background import BackgroundScheduler
from injector import Injector
from pymongo import MongoClient
from pytz import utc

from app import AppModule

injector = Injector(AppModule)

jobstores = {
    'mongo': MongoDBJobStore(client=injector.get(MongoClient))
}
executors = {
    'default': ThreadPoolExecutor(4)
}
job_defaults = {
    'coalesce': False,
    'max_instances': 3
}
scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults, timezone=utc)


def tick():
    print(f"Tick! The time is: {datetime.now()}")


def my_listener(event):
    if event.exception:
        print('The job crashed :( because:', event.exception)


scheduler.add_listener(my_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)

scheduler.add_job(tick, 'interval', seconds=1, id='my_job_id', replace_existing=True, jobstore="mongo")

if __name__ == "__main__":
    scheduler.start()
    print("Press Ctrl+{} to exit".format("Break" if os.name == "nt" else "C"))

    while True:
        time.sleep(30)
