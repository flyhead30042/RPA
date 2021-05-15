from __future__ import annotations

import logging
from argparse import ArgumentParser
from datetime import datetime
from time import sleep
from selenium.common.exceptions import TimeoutException
from browser import click_until_presence, driver, click_element, wait_until_presence, loginWithCredentials, input_text, \
    Credential, WaitCondition
from browser import logger as browser_logger
from setting import DATEF2, DATESTAMP2, TIMESTAMP1

ATTENDANCE_LK = '//*[@id ="root"]/div/div/div/div[2]/div/ul/li[2]/a'
RECHECKINOUT_LK = '//*[@id="root"]/div/div/div/div[3]/div/div/div/div[2]/div[1]/div/div[3]/div/img'

RECHECKINOUT_DATE_TF ='//*[@id="root"]/div/div/div/div[3]/div/div/div/div[2]/div[3]/div/div[2]/form/div[1]/div[1]/div/div/div/input'

# RECHECKINOUT_TYPE_DP = '//*[@id="root"]/div/div/div/div[3]/div/div/div/div[2]/div[3]/div/div[2]/form/div[1]/div[2]/div/div/div/div/div/span'
RECHECKINOUT_TYPE_DP = '//*[@id="root"]/div/div/div/div[3]/div/div/div/div[2]/div[3]/div/div[2]/form/div[1]/div[2]/div/div/div/div'
RECHECKINOUT_TYPE_ONDUTY_OP = '//*[@id="root"]/div/div/div/div[3]/div/div/div/div[2]/div[3]/div/div[2]/form/div[1]/div[2]/div/div/div/div/div[2]/div/div[1]'
RECHECKINOUT_TYPE_OFFDUTY_OP = '//*[@id="root"]/div/div/div/div[3]/div/div/div/div[2]/div[3]/div/div[2]/form/div[1]/div[2]/div/div/div/div/div[2]/div/div[2]'

# RECHECKINOUT_TIME_DP = '//*[@id="root"]/div/div/div/div[3]/div/div/div/div[2]/div[3]/div/div[2]/form/div[1]/div[3]/div/div[1]/div/div/div/span'
RECHECKINOUT_TIME_DP = '//*[@id="root"]/div/div/div/div[3]/div/div/div/div[2]/div[3]/div/div[2]/form/div[1]/div[3]/div/div[1]/div/div'
RECHECKINOUT_TIME_09_OP = '//*[@id="root"]/div/div/div/div[3]/div/div/div/div[2]/div[3]/div/div[2]/form/div[1]/div[3]/div/div[1]/div/div/div[2]/div/div[10]'
RECHECKINOUT_TIME_18_OP = '//*[@id="root"]/div/div/div/div[3]/div/div/div/div[2]/div[3]/div/div[2]/form/div[1]/div[3]/div/div[1]/div/div/div[2]/div/div[19]'

# RECHECKINOUT_LOC_DP = '//*[@id="root"]/div/div/div/div[3]/div/div/div/div[2]/div[3]/div/div[2]/form/div[1]/div[4]/div/div/div/div/div/span'
RECHECKINOUT_LOC_DP = '//*[@id="root"]/div/div/div/div[3]/div/div/div/div[2]/div[3]/div/div[2]/form/div[1]/div[4]/div/div/div/div'

RECHECKINOUT_LOC_ERT_OP = '//*[@id="root"]/div/div/div/div[3]/div/div/div/div[2]/div[3]/div/div[2]/form/div[1]/div[4]/div/div/div/div/div[2]/div/div[1]'
RECHECKINOUT_OK_BTN = '//*[@id="root"]/div/div/div/div[3]/div/div/div/div[2]/div[3]/div/div[2]/form/div[2]/button[1]'
RECHECKINOUT_CONFIRM_BTN = '//*[@id="root"]/div/div[2]/div/div[2]/button[1]'

logger = logging.getLogger(__name__)


@click_until_presence(driver=driver, wc=WaitCondition(timeout=15, xpath=ATTENDANCE_LK))
@click_until_presence(driver=driver, wc=WaitCondition(timeout=15, xpath=RECHECKINOUT_LK))
@wait_until_presence(driver=driver, wc=WaitCondition(timeout=15, xpath=RECHECKINOUT_LOC_DP))
def punch(driver, dt: str, duty: str):
    sleep(1)
    logger.info("dt={}, duty={}".format(dt, duty))
    input_text(driver, RECHECKINOUT_DATE_TF, dt)

    click_element(driver, RECHECKINOUT_TYPE_DP)
    if duty == 'on':
        click_element(driver, RECHECKINOUT_TYPE_ONDUTY_OP)
    elif duty == 'off':
        click_element(driver, RECHECKINOUT_TYPE_OFFDUTY_OP)

    click_element(driver, RECHECKINOUT_TIME_DP)
    if duty == 'on':
        click_element(driver, RECHECKINOUT_TIME_09_OP)
    elif duty == 'off':
        click_element(driver, RECHECKINOUT_TIME_18_OP)

    click_element(driver, RECHECKINOUT_LOC_DP)
    click_element(driver, RECHECKINOUT_LOC_ERT_OP)
    click_element(driver, RECHECKINOUT_OK_BTN)

@click_until_presence(driver = driver, wc=WaitCondition(timeout=15, xpath=RECHECKINOUT_CONFIRM_BTN))
def confirmPunch(driver):
    return

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-id",  dest="id",
                        help="your id", required=False)
    parser.add_argument("-pwd",  dest="pwd",
                        help="your password", required=False)
    parser.add_argument("-punch",  dest="punch",
                        help="on/off/all", required=False)
    parser.add_argument("-dt",  dest="dt",
                        help="punch date with format yyyy/mm/dd ", required=False)
    parser.add_argument("-debug", action='store_true', dest="debug",
                        help="debug", required=False)
    args = parser.parse_args()
    logger.info(args)

    if args.debug:
        logger.setLevel(logging.DEBUG)
        browser_logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
        browser_logger.setLevel(logging.INFO)

    try:
        driver.get('https://auth.mayohr.com/HRM/Account/Login')
        driver.maximize_window()

        loginWithCredentials(driver, Credential(id=args.id, pwd=args.pwd))
        try:
            d = datetime.strptime(args.dt, DATEF2)
            dt = d.strftime(DATEF2)
        except TypeError:
            logger.info("no -dt argument found, punch today")
            dt = DATESTAMP2
        except ValueError:
            logger.error("-dt argument({}) is incorrect".format(args.dt))
            dt = DATESTAMP2
        logger.debug("-dt argument is {}".format(dt))

        if args.punch == 'on' or args.punch == 'off':
            punch(driver, dt, args.punch)
            confirmPunch(driver)
            logging.info("Punch {:s} Success!!".format(args.punch))
        elif args.punch == 'all' or not args.punch:
            punch(driver, dt, "on")
            confirmPunch(driver)
            logging.info("Punch on Success!!")
            punch(driver, dt, "off")
            confirmPunch(driver)
            logging.info("Punch off Success!!")
        else:
            logger.error("-punch argument({}) is incorrect".format(args.punch))

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
        driver.close()




