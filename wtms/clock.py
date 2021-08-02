from __future__ import annotations
import logging
import os
from time import sleep
from selenium.common.exceptions import TimeoutException
from browser import xpath, loginWithCredentials, Credential, wait_until_presence, WaitCondition, input_text, \
    click_element, TIMESTAMP1
from selenium import webdriver
import platform

# Declare a global driver due to decoration
driver = None

logger = logging.getLogger(__name__)

@wait_until_presence(driver = driver, wc=WaitCondition(timeout=15, xpath=xpath["LOGIN_SUBMIT_BTN"]))
def login(driver, id:str, pwd:str):
    loginWithCredentials(driver, Credential(id=id, pwd=pwd))

@wait_until_presence(driver=driver, wc=WaitCondition(timeout=15, xpath=xpath["CLOCK_TIME_TF"]))
def clock_on(driver, time:str ="09:30"):
    input_text(driver, xpath["CLOCK_TIME_TF"], time)
    click_element(driver, xpath["CLOCK_ON_DIV"])

@wait_until_presence(driver=driver, wc=WaitCondition(timeout=15, xpath=xpath["CLOCK_TIME_TF"]))
def clock_out(driver, time:str ="18:30"):
    input_text(driver, xpath["CLOCK_TIME_TF"], time)
    click_element(driver, xpath["CLOCK_OUT_DIV"])


def main():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument("--no-sandbox")   #Bypass OS security model
    options.add_argument("--disable-dev-shm-usage")  # overcome limited resource problems
    options.add_argument('--window-size=1420,1080')
    options.add_argument('--disable-gpu')
    driver = webdriver.Remote("http://chrome:4444/wd/hub", options=options)

    try:
        WTMS_URL = os.environ.get("WTMS_URL", "https://working-time-management-system-tw.internal.ericsson.com/#/login")
        logger.info(f"1. Open {WTMS_URL}")
        driver.get(WTMS_URL)
        driver.maximize_window()

        logger.info("2. login with credentials")
        login(driver,
              id=os.environ.get("WTMS_ID", "ecihsia"),
              pwd=os.environ.get("WTMS_PWD", "ZAQ!xsw2"))

        CLOCK_ON_TIME = os.environ.get("CLOCK_ON_TIME", "09:30")
        logger.info(F"3. Clock On at {CLOCK_ON_TIME}")
        clock_on(driver, time=CLOCK_ON_TIME )
        sleep(1)

        CLOCK_OUT_TIME = os.environ.get("CLOCK_OUT_TIME", "18:30")
        logger.info(f"4. Clock Out at {CLOCK_OUT_TIME}")
        clock_out(driver, time= CLOCK_OUT_TIME)

        driver.save_screenshot('wtms_result.png')

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
        driver.quit()

if __name__ == "__main__":
    main()