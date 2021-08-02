from __future__ import annotations
import logging
import os
from time import sleep
from selenium.common.exceptions import TimeoutException
from browser import xpath, driver, loginWithCredentials, Credential, wait_until_presence, WaitCondition, input_text, \
    click_element, TIMESTAMP1
import sched, time

WTMS_ID = os.environ.get("WTMS_ID", "ecihsia")
WTMS_PWD = os.environ.get("WTMS_PWD", "ZAQ!xsw2")
WTMS_URL = os.environ.get("WTMS_URL", "https://working-time-management-system-tw.internal.ericsson.com/#/login")

logging_level = {"INFO": logging.INFO, "DEBUG": logging.DEBUG, "ERROR": logging.ERROR}
logging.basicConfig(level=logging_level[os.environ.get("LOGGING_LEVEL", "INFO")],
                    format="%(asctime)s | %(name)s | %(levelname)s | %(message)s"
                    )
logger = logging.getLogger(__name__)

@wait_until_presence(driver=driver, wc=WaitCondition(timeout=15, xpath=xpath["CLOCK_TIME_TF"]))
def clock_on(time:str ="09:30"):
    input_text(driver, xpath["CLOCK_TIME_TF"], time)
    click_element(driver, xpath["CLOCK_ON_DIV"])

@wait_until_presence(driver=driver, wc=WaitCondition(timeout=15, xpath=xpath["CLOCK_TIME_TF"]))
def clock_out(time:str ="18:30"):
    input_text(driver, xpath["CLOCK_TIME_TF"], time)
    click_element(driver, xpath["CLOCK_OUT_DIV"])

if __name__ == "__main__":
    try:
        logger.info("1. Login")
        driver.get(WTMS_URL)
        driver.maximize_window()

        loginWithCredentials(driver, Credential(id=WTMS_ID, pwd=WTMS_PWD))
        logger.info("2. Clock On")
        clock_on()
        sleep(1)
        logger.info("3. Clock Out")
        clock_out()

    except TimeoutException as e1:
        logger.error("TimeoutException:{}".format(str(e1)))
        driver.get_screenshot_as_file("screenshot-{}.png".format(TIMESTAMP1))
    except ConnectionResetError as e2:
        logger.error("ConnectionResetError:{}".format(str(e2)))
        driver.get_screenshot_as_file("screenshot-{}.png".format(TIMESTAMP1))
    except Exception as e:
        logger.error("Exception:{}".format(str(e)))
        driver.get_screenshot_as_file("screenshot-{}.png".format(TIMESTAMP1))
    finally:
        # browser.driver.close()
        pass