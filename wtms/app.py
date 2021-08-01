import logging
import os

from apscheduler.schedulers.background import BlockingScheduler
import hello
# import clock

logging_level = {"INFO": logging.INFO, "DEBUG": logging.DEBUG, "ERROR": logging.ERROR}
logging.basicConfig(level=logging_level[os.environ.get("LOGGING_LEVEL", "INFO")],
                    format="%(asctime)s | %(name)s | %(levelname)s | %(message)s"
                    )
logger = logging.getLogger(__name__)

os.environ['TZ'] = 'Asia/Taipei'


if __name__ == "__main__":
    # BlockingScheduler: use when the scheduler is the only thing running in your process
    scheduler = BlockingScheduler()

    # Schedules the clock.main() to be executed.
    # TASKER_CLOCK_HOUR = os.environ.get("SCHEDULER_CLOCK_HOUR", 12)
    # TASKER_CLOCK_MINUTE = os.environ.get("TASKER_CLOCK_MINUTE", 45)
    # logger.info(f"0. Add clock job w/ schedule at {TASKER_CLOCK_HOUR}:{TASKER_CLOCK_MINUTE}, Mon.~Fri.")
    # scheduler.add_job(clock.main, 'cron', day_of_week='mon-fri', hour=TASKER_CLOCK_HOUR, minute=TASKER_CLOCK_MINUTE,
    #                   start_date='2021-03-23 12:00:00', timezone='Asia/Taipei')

    # !! Testing !!
    scheduler.add_job(hello.main, 'interval', id='hello.main', seconds=15)

    # Schedules the approve.main() to be executed.

    # Start the scheduler
    scheduler.start()