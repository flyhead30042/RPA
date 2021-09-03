import logging
import os
import time
from os import listdir
from os.path import isfile, join, getctime, getmtime
from typing import AnyStr

from apscheduler.job import Job
# from apscheduler.schedulers.background import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger


import hello
from clock import doclock, doreclock
from flask import Flask, render_template, send_from_directory

level = logging.getLevelName(os.environ.get('LOG_LEVEL', 'DEBUG'))
logging.basicConfig(level=level, format="%(asctime)s | %(name)s | %(levelname)s | %(message)s")
logger = logging.getLogger(__name__)
level = logging.getLevelName(os.environ.get('LOG_LEVEL', 'INFO'))
logger.setLevel(level)
os.environ['TZ'] = 'Asia/Taipei'

app = Flask(__name__)

@app.route('/wtms')
def index():
    return render_template('index.html', message="WTMS is up and running!")

@app.route('/wtms/clock')
def clock():
    doclock()
    return render_template('index.html', message="Clock Now is completed!")

@app.route('/wtms/reclock/<day>')
def reclock(day):
    doreclock(day)
    return render_template('index.html', message="Reclock is completed!")

@app.route('/wtms/screenshot')
def scrrenshot():
    screenshot_path = app.root_path +"/screenshot"
    flist = [f for f in listdir(screenshot_path) if isfile(join(screenshot_path, f))]
    ctime = [time.ctime(getctime(join(screenshot_path, f))) for f in flist ]
    mtime = [time.ctime(getmtime(join(screenshot_path, f))) for f in flist ]
    src = [ "/wtms/screenshot/" + f for f in flist]
    table = zip(flist, ctime, mtime, src)
    return render_template('screenshot.html', table=table)

@app.route('/wtms/screenshot/<pngname>')
def scrrenshot_route(pngname):
    return send_from_directory(directory=app.root_path + "/screenshot/",  filename=pngname, as_attachment=False, cache_timeout=0 )

if __name__ == "__main__":
    # BlockingScheduler: use when the scheduler is the only thing running in your process
    scheduler = BackgroundScheduler()

    # Schedules the clock.main() to be executed.
    crontab = os.environ.get("CRONTAB_CLOCK", "05 13 * * 1-5")
    job:Job = scheduler.add_job(doclock, CronTrigger.from_crontab(crontab), timezone='Asia/Taipei')
    logger.info("0. Add {}(), {}".format(job.func_ref, job.trigger))
    # scheduler.add_job(clock_main, 'cron', day_of_week='mon-fri', hour=cron_hr, minute=cron_min,
    #                   start_date='2021-03-23 12:00:00', timezone='Asia/Taipei')

    # !! For Testing !!
    # scheduler.add_job(clock_main, 'interval', id='hello.main', seconds=15)

    # Schedules the approve.main() to be executed.

    # Start the scheduler
    scheduler.start()

    # app.run(debug=True, host='0.0.0.0')
    app.run(host='0.0.0.0')