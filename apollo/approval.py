from __future__ import annotations
import logging
from argparse import ArgumentParser

from selenium.common.exceptions import TimeoutException

from browser import click_until_presence, wait_until_presence, driver, click_element, loginWithCredentials, Credential, \
    WaitCondition
from browser import logger as browser_logger
from setting import TIMESTAMP1

ATTENDANCE_LK = '//*[@id ="root"]/div/div/div/div[2]/div/ul/li[2]/a'
APPROVAL_LK = '//*[@id="root"]/div/div/div/div[3]/div/div/div/div[2]/div[1]/div/div[8]/a'

APPROVAL_SELECT_ALL_CKB = '//*[@id="root"]/div/div/div/div[3]/div/div/div/div[2]/div[1]/div[3]/div[1]/table/tbody/tr/th[6]/input'
APPROVAL_BATCH_BTN = '//*[@id="root"]/div/div/div/div[3]/div/div/div/div[2]/div[1]/div[2]/div/button'
APPROVAL_TR1_TD = '//*[@id="root"]/div/div/div/div[3]/div/div/div/div[2]/div[1]/div[3]/div[2]/div[1]/table/tbody/tr/td[6]/input | ' \
                     '//*[@id="root"]/div/div/div/div[3]/div/div/div/div[2]/div[1]/div[3]/div[2]/div[1]/table/tbody/tr[1]/td[6]/input | ' \
                     '//*[@id="root"]/div/div/div/div[3]/div/div/div/div[2]/div[1]/div[3]/div[2]/div[1]/table/tbody/tr/td/span'

APPROVAL_TR1 = '//*[@id="root"]/div/div/div/div[3]/div/div/div/div[2]/div[1]/div[3]/div[2]/div[1]/table/tbody/tr'

APPROVAL_CONFIRM_BTN = '//*[@id="root"]/div/div/div/div[3]/div/div/div/div[2]/div[2]/div/div[2]/form/div[2]/button[1]'
APPROVAL_RESULT_CONFIRM_BTN = '//*[@id="root"]/div/div/div/div[3]/div/div/div/div[2]/div[3]/div/div[2]/div[2]/button'

logger = logging.getLogger(__name__)

def is_data_found(driver) -> bool:
    """
    Check if any data to be approved

    :Return:
        - True - data found
        - False - No data found
    """
    tr1 = driver.find_element_by_xpath(APPROVAL_TR1)

    # use  find_elements_by_tag_name() instead of find_element_by_tag_name()
    tds = tr1.find_elements_by_tag_name("td")
    td_len = len(tds)
    logger.debug("TD #={:d}".format( td_len ))
    return True if td_len > 1 else False

@click_until_presence(driver = driver, wc=WaitCondition(timeout=15, xpath=ATTENDANCE_LK))
@click_until_presence(driver = driver, wc=WaitCondition(timeout=15, xpath=APPROVAL_LK))
@wait_until_presence(driver = driver, wc=WaitCondition(timeout=15, xpath=APPROVAL_TR1_TD))
def approveAll(driver) -> bool:
    is_found = is_data_found(driver)
    logger.info("is_found={}".format(is_found))
    if is_found:
        click_element(driver, APPROVAL_SELECT_ALL_CKB)
        click_element(driver, APPROVAL_BATCH_BTN)

    return True if is_found else False

@click_until_presence(driver = driver, wc=WaitCondition(timeout=15, xpath=APPROVAL_CONFIRM_BTN))
@click_until_presence(driver = driver, wc=WaitCondition(timeout=15, xpath=APPROVAL_RESULT_CONFIRM_BTN))
def approveConfirm(driver):
    return


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-id",  dest="id",
                        help="your id", required=False, default="c.i.hsiao@ericsson.com")
    parser.add_argument("-pwd",  dest="pwd",
                        help="your password", required=False, default="brU4epC8")
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

        if approveAll(driver):
            approveConfirm(driver)
            logging.info("Approval Success!!")
        else:
            logger.info("No data found")
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




