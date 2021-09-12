import logging
import os
import time
from os import listdir
from os.path import isfile, join, getctime, getmtime
from typing import AnyStr
from apscheduler.job import Job
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from clock import doclock, doreclock, doapprove_all
from flask import Flask, render_template, send_from_directory

level = logging.getLevelName(os.environ.get('LOG_LEVEL', 'DEBUG'))
logging.basicConfig(level=level, format="%(asctime)s | %(name)s | %(levelname)s | %(message)s")
logger = logging.getLogger(__name__)
level = logging.getLevelName(os.environ.get('LOG_LEVEL', 'INFO'))
logger.setLevel(level)
tz = os.environ.get('TZ', 'Asia/Taipei')

scheduler = BackgroundScheduler(timezone=tz, job_default={"max_instances": 1})
app = Flask(__name__)

@app.route('/wtms')
def index():
    jobs = scheduler.get_jobs()
    data={}
    data["msg"] = "WTMS (Build: {:s}) is up and running!".format(os.environ['BUILD'])
    data["scheduler_is_running"] = scheduler.running
    data["jobs"] = [(j.id, j.name, j.func) for j in jobs]
    data ["envs"] = [ (k,v) for (k,v) in os.environ.items() ]

    return render_template('index.html', data = data)

@app.route('/wtms/clock')
def clock():
    doclock()
    data={}
    data["msg"] = "Clock Now is completed!"
    return render_template('result.html', data=data)

@app.route('/wtms/approve')
def approveall():
    total_str = doapprove_all()
    data={}
    data["msg"] = f"Approve All is completed! {total_str} found"
    return render_template('result.html',  data=data)

# @app.route('/wtms/reclock/<day>')
# def reclock(day):
#     doreclock(day)
#     return render_template('result.html', message="Reclock is completed!")

@app.route('/wtms/screenshot')
def screenshot():
    screenshot_path = app.root_path +"/screenshot"
    flist = [f for f in listdir(screenshot_path) if isfile(join(screenshot_path, f))]
    ctime = [time.ctime(getctime(join(screenshot_path, f))) for f in flist ]
    mtime = [time.ctime(getmtime(join(screenshot_path, f))) for f in flist ]
    src = [ "/wtms/screenshot/" + f for f in flist]
    data = zip(flist, ctime, mtime, src)
    return render_template('screenshot.html', data=data)

@app.route('/wtms/screenshot/<pngname>')
def scrrenshot_route(pngname):
    return send_from_directory(directory=app.root_path + "/screenshot/",  filename=pngname, as_attachment=False, cache_timeout=0 )

if __name__ == "__main__":
    '''
    Schedules clock task    
    '''
    crontab = os.environ.get("CRONTAB_CLOCK", "15 13 * * mon-fri")
    job:Job = scheduler.add_job(doclock, CronTrigger.from_crontab(crontab))
    logger.info("0. Add {}(), {}".format(job.func_ref, job.trigger))

    '''
    TODO: Out-of-Office 
    '''
    # scheduler.add_job(clock_main, 'cron', day_of_week='mon-fri', hour=cron_hr, minute=cron_min,
    #                   start_date='2021-03-23 12:00:00', timezone='Asia/Taipei')

    '''
    Schedules approve_all task    
    '''
    if os.environ.get("CRONTAB_APPROVE_ALL_ENABLED", "false").lower() == "true":
        crontab = os.environ.get("CRONTAB_APPROVE_ALL", "45 13 * * wed")
        job:Job = scheduler.add_job(doapprove_all, CronTrigger.from_crontab(crontab))
        logger.info("0. Add {}(), {}".format(job.func_ref, job.trigger))

    # Kick off scheduler
    scheduler.start()

    # Launch Flask server
    app.run(host='0.0.0.0')