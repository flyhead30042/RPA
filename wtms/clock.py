from __future__ import annotations
import logging
import os
from time import sleep
from selenium.common.exceptions import TimeoutException
from browser import xpath, loginWithCredentials, Credential, wait_until_presence, WaitCondition, input_text, \
    click_element, TIMESTAMP1
from selenium import webdriver

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument("--no-sandbox")  # Bypass OS security model
options.add_argument("--disable-dev-shm-usage")  # overcome limited resource problems
options.add_argument('--ignore-ssl-errors=yes')  # bypass non-secure page
options.add_argument('--ignore-certificate-errors')  # bypass non-secure page
options.add_argument('--start-maximized')
options.add_argument('--disable-gpu')
driver = webdriver.Remote("http://chrome:4444/wd/hub", options=options)

logger = logging.getLogger(__name__)
level = logging.getLevelName(os.environ.get('LOG_LEVEL', 'INFO'))
logger.setLevel(level)

@wait_until_presence(driver = driver, wc=WaitCondition(timeout=15, xpath=xpath["LOGIN_SUBMIT_BTN"]))
def login(driver, id:str, pwd:str):
    input_text(driver, xpath["LOGIN_ID_TF"], id)
    input_text(driver, xpath["LOGIN_PWD_TF"], pwd)
    driver.save_screenshot('screenshot/login.png')
    click_element(driver, xpath["LOGIN_SUBMIT_BTN"])

@wait_until_presence(driver=driver, wc=WaitCondition(timeout=15, xpath=xpath["CLOCK_TIME_TF"]))
def clock_on(driver, time:str ="09:30"):
    input_text(driver, xpath["CLOCK_TIME_TF"], time)
    driver.save_screenshot('screenshot/clock_on.png')
    click_element(driver, xpath["CLOCK_ON_DIV"])

@wait_until_presence(driver=driver, wc=WaitCondition(timeout=15, xpath=xpath["CLOCK_TIME_TF"]))
def clock_out(driver, time:str ="18:30"):
    input_text(driver, xpath["CLOCK_TIME_TF"], time)
    driver.save_screenshot('screenshot/clock_out.png')
    click_element(driver, xpath["CLOCK_OUT_DIV"])

def main():
    try:
        WTMS_URL = os.environ.get("WTMSURL", "https://working-time-management-system-tw.internal.ericsson.com/#/login")
        logger.info(f"1. Open {WTMS_URL}")
        driver.get(WTMS_URL)
        # driver.maximize_window()
        driver.save_screenshot('screenshot/open.png')

        logger.info("2. login with credentials")
        login(driver,
              id=os.environ.get("WTMS_ID", "myid"),
              pwd=os.environ.get("WTMS_PWD", "mypwd"))

        CLOCK_ON_TIME = os.environ.get("CLOCK_ON_TIME", "09:30")
        logger.info(F"3. Clock On at {CLOCK_ON_TIME}")
        clock_on(driver, time=CLOCK_ON_TIME )
        sleep(3)

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

if __name__ == "__main__":
    main()