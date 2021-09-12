from __future__ import annotations
import logging
import os
from datetime import date

from selenium.common.exceptions import TimeoutException
from browser import xpath, loginWithCredentials, Credential, wait_until_presence, WaitCondition, input_text, \
    click_element, TIMESTAMP1, click_until_presence, get_text
from selenium import webdriver

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument("--no-sandbox")  # Bypass OS security model
options.add_argument("--disable-dev-shm-usage")  # overcome limited resource problems
options.add_argument('--ignore-ssl-errors=yes')  # bypass non-secure page
options.add_argument('--ignore-certificate-errors')  # bypass non-secure page
options.add_argument('--start-maximized')
options.add_argument('--disable-gpu')

logger = logging.getLogger(__name__)
level = logging.getLevelName(os.environ.get('LOG_LEVEL', 'INFO'))
logger.setLevel(level)

@wait_until_presence(wc=WaitCondition(timeout=15, xpath=xpath["LOGIN_SUBMIT_BTN"], sleep=2))
def login(driver, id:str, pwd:str):
    input_text(driver, xpath["LOGIN_ID_TF"], id)
    input_text(driver, xpath["LOGIN_PWD_TF"], pwd)
    driver.save_screenshot('screenshot/login.png')
    click_element(driver, xpath["LOGIN_SUBMIT_BTN"])

@wait_until_presence(wc=WaitCondition(timeout=15, xpath=xpath["CLOCK_TIME_TF"], sleep=2))
def clock_on(driver, time:str ="09:30"):
    input_text(driver, xpath["CLOCK_TIME_TF"], time)
    driver.save_screenshot('screenshot/clock_on.png')
    click_element(driver, xpath["CLOCK_ON_DIV"])

@wait_until_presence(wc=WaitCondition(timeout=15, xpath=xpath["CLOCK_TIME_TF"], sleep=2))
def clock_out(driver, time:str ="18:30"):
    input_text(driver, xpath["CLOCK_TIME_TF"], time)
    driver.save_screenshot('screenshot/clock_out.png')
    click_element(driver, xpath["CLOCK_OUT_DIV"])

def doclock():
    driver = None
    try:
        driver = webdriver.Remote("http://chrome:4444/wd/hub", options=options)
        WTMS_URL = os.environ.get("WTMSURL", "https://working-time-management-system-tw.internal.ericsson.com/#/login")
        logger.info(f"1. Open {WTMS_URL}")
        driver.get(WTMS_URL)
        driver.save_screenshot('screenshot/open.png')

        logger.info("2. Login with credentials")
        login(driver,
              id=os.environ.get("WTMS_ID", "myid"),
              pwd=os.environ.get("WTMS_PWD", "mypwd"))

        CLOCK_ON_TIME = os.environ.get("CLOCK_ON_TIME", "09:30")
        logger.info(F"3. Clock On at {CLOCK_ON_TIME}")
        clock_on(driver, time=CLOCK_ON_TIME )

        CLOCK_OUT_TIME = os.environ.get("CLOCK_OUT_TIME", "18:30")
        logger.info(f"4. Clock Out at {CLOCK_OUT_TIME}")
        clock_out(driver, time= CLOCK_OUT_TIME)
    except TimeoutException as e1:
        logger.exception("TimeoutException:{}".format(str(e1)))
        driver.save_screenshot("screenshot/TimeoutException-{}.png".format(TIMESTAMP1))
        driver.quit()
    except ConnectionResetError as e2:
        logger.exception("ConnectionResetError:{}".format(str(e2)))
        driver.save_screenshot("screenshot/ConnectionResetError-{}.png".format(TIMESTAMP1))
        driver.quit()
    except Exception as e:
        logger.exception("Exception:{}".format(str(e)))
        driver.save_screenshot("screenshot/Exception-{}.png".format(TIMESTAMP1))
        driver.quit()
    finally:
        driver.quit()


@click_until_presence(wc=WaitCondition(timeout=15, xpath=xpath["ATTENDANCE_LK"], sleep=1))
@click_until_presence(wc=WaitCondition(timeout=15, xpath=xpath["RECLOCK_APPROVAL_LK"], sleep=1))
@wait_until_presence(wc=WaitCondition(timeout=15, xpath=xpath["RECLOCK_APPROVE_ALL_BTN"], sleep=2))
def approve_all(driver) -> str:
    total_str = get_text(driver, xpath["RECLOCK_APPROVE_ALL_TOTAL_TX"])
    if "Total 0" not in total_str:
        click_element(driver, xpath["RECLOCK_APPROVE_ALL_CB"])
        click_element(driver, xpath["RECLOCK_APPROVE_ALL_BTN"])
        driver.save_screenshot('screenshot/approve_all.png')
    return total_str

def doapprove_all():
    driver = None
    try:
        driver = webdriver.Remote("http://chrome:4444/wd/hub", options=options)
        WTMS_URL = os.environ.get("WTMSURL", "https://working-time-management-system-tw.internal.ericsson.com/#/login")

        logger.info(f"1. Open {WTMS_URL}")
        driver.get(WTMS_URL)
        driver.save_screenshot('screenshot/open.png')

        logger.info("2. Login with credentials")
        login(driver,
              id=os.environ.get("WTMS_ID", "myid"),
              pwd=os.environ.get("WTMS_PWD", "mypwd"))

        total_str = approve_all(driver)
        logger.info(f"3. Approve All, {total_str} found")
        return (total_str)

    except TimeoutException as e1:
        logger.exception("TimeoutException:{}".format(str(e1)))
        driver.save_screenshot("screenshot/TimeoutException-{}.png".format(TIMESTAMP1))
        driver.quit()
    except ConnectionResetError as e2:
        logger.exception("ConnectionResetError:{}".format(str(e2)))
        driver.save_screenshot("screenshot/ConnectionResetError-{}.png".format(TIMESTAMP1))
        driver.quit()
    except Exception as e:
        logger.exception("Exception:{}".format(str(e)))
        driver.save_screenshot("screenshot/Exception-{}.png".format(TIMESTAMP1))
        driver.quit()
    finally:
        driver.quit()

@click_until_presence(wc=WaitCondition(timeout=15, xpath=xpath["ATTENDANCE_LK"], sleep=3))
@click_until_presence(wc=WaitCondition(timeout=15, xpath=xpath["RECLOCK_LK"], sleep=3))
@wait_until_presence(wc=WaitCondition(timeout=15, xpath=xpath["RECLOCK_DATE_TF"], sleep=3))
def reclock(driver, rc_date:str, rc_on_time:str, rc_out_time:str):
    input_text(driver, xpath["RECLOCK_DATE_TF"], rc_date, True)
    input_text(driver, xpath["RECLOCK_TIME_ON_TF"], rc_on_time, True)
    input_text(driver, xpath["RECLOCK_TIME_OUT_TF"], rc_out_time, True)
    input_text(driver, xpath["RECLOCK_REASON_TA"], "Reclock")
    driver.save_screenshot('screenshot/reclock_on.png')
    click_element(driver, xpath["RECLOCK_SUBMIT_BTN"])

def doreclock(rc_day:str):
    driver = None
    try:
        driver = webdriver.Remote("http://chrome:4444/wd/hub", options=options)
        WTMS_URL = os.environ.get("WTMSURL", "https://working-time-management-system-tw.internal.ericsson.com/#/login")

        logger.info(f"1. Open {WTMS_URL}")
        driver.get(WTMS_URL)
        # driver.maximize_window()
        driver.save_screenshot('screenshot/open.png')

        logger.info("2. Login with credentials")
        login(driver,
              id=os.environ.get("WTMS_ID", "myid"),
              pwd=os.environ.get("WTMS_PWD", "mypwd"))

        CLOCK_ON_TIME = os.environ.get("CLOCK_ON_TIME", "09:30")
        CLOCK_OUT_TIME = os.environ.get("CLOCK_OUT_TIME", "18:30")
        today = date.today()
        year = today.strftime("%Y")
        month = today.strftime("%m")
        day = "{:0>2}".format(rc_day)
        rc_date=f"{year}-{month}-{day}"
        logger.info(F"3. Reclock on {rc_date}, {CLOCK_ON_TIME}-{CLOCK_OUT_TIME}")
        reclock(driver, rc_date, CLOCK_ON_TIME, CLOCK_OUT_TIME)
    except TimeoutException as e1:
        logger.exception("TimeoutException:{}".format(str(e1)))
        driver.save_screenshot("screenshot/TimeoutException-{}.png".format(TIMESTAMP1))
        driver.quit()
    except ConnectionResetError as e2:
        logger.exception("ConnectionResetError:{}".format(str(e2)))
        driver.save_screenshot("screenshot/ConnectionResetError-{}.png".format(TIMESTAMP1))
        driver.quit()
    except Exception as e:
        logger.exception("Exception:{}".format(str(e)))
        driver.save_screenshot("screenshot/Exception-{}.png".format(TIMESTAMP1))
        driver.quit()
    finally:
        driver.quit()


if __name__ == "__main__":
    doclock()