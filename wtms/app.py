import logging
import os
from datetime import datetime
from typing import AnyStr

from apscheduler.job import Job
from apscheduler.schedulers.background import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

import hello
import clock

level = logging.getLevelName(os.environ.get('LOG_LEVEL', 'DEBUG'))
logging.basicConfig(level=level, format="%(asctime)s | %(name)s | %(levelname)s | %(message)s")
logger = logging.getLogger(__name__)
level = logging.getLevelName(os.environ.get('LOG_LEVEL', 'INFO'))
logger.setLevel(level)
os.environ['TZ'] = 'Asia/Taipei'

if __name__ == "__main__":
    # BlockingScheduler: use when the scheduler is the only thing running in your process
    scheduler = BlockingScheduler()

    # Schedules the clock.main() to be executed.
    crontab = os.environ.get("CRONTAB_CLOCK", "05 13 * * 1-5")
    job:Job = scheduler.add_job(clock.main, CronTrigger.from_crontab(crontab), timezone='Asia/Taipei')
    logger.info("0. Add {}(), {}".format(job.func_ref, job.trigger))
    # scheduler.add_job(clock.main, 'cron', day_of_week='mon-fri', hour=cron_hr, minute=cron_min,
    #                   start_date='2021-03-23 12:00:00', timezone='Asia/Taipei')

    # !! For Testing !!
    # scheduler.add_job(clock.main, 'interval', id='hello.main', seconds=15)

    # Schedules the approve.main() to be executed.

    # Start the scheduler
    scheduler.start()