import logging
import os
from datetime import datetime
from typing import AnyStr

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

# def get_cron_time(timestr:AnyStr):
#     time = datetime.strptime(timestr, "%H:%M")
#     cron_hr = str(time.hour)
#     cron_min = str(time.minute)
#     return cron_hr, cron_min

if __name__ == "__main__":
    # BlockingScheduler: use when the scheduler is the only thing running in your process
    scheduler = BlockingScheduler()

    # Schedules the clock.main() to be executed.
    # cron_hr, cron_min = get_cron_time(os.environ.get("CRON_CLOCK", "14:30"))

    crontab = os.environ.get("CRONTAB_CLOCK", "05 13 * * 1-5")
    logger.info(f"0. Add clock job w/ schedule at {crontab}")
    scheduler.add_job(clock.main, CronTrigger.from_crontab(crontab))
    # scheduler.add_job(clock.main, 'cron', day_of_week='mon-fri', hour=cron_hr, minute=cron_min,
    #                   start_date='2021-03-23 12:00:00', timezone='Asia/Taipei')

    # !! For Testing !!
    # scheduler.add_job(clock.main, 'interval', id='hello.main', seconds=15)

    # Schedules the approve.main() to be executed.

    # Start the scheduler
    scheduler.start()