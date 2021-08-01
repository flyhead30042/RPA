import logging
import platform
from selenium import webdriver

logger = logging.getLogger(__name__)

#
# logging.basicConfig(level=logging.INFO,
#                     format="%(asctime)s | %(name)s | %(levelname)s | %(message)s"
#                     )

def main():
    logger.info("Load webdriver")
    # driver = webdriver.Chrome(
    #     executable_path="webdriver/chromedriver-92.exe") if platform.system() == "Windows" else webdriver.Chrome()

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument("--no-sandbox")   #Bypass OS security model
    options.add_argument("--disable-dev-shm-usage")  # overcome limited resource problems
    options.add_argument('--window-size=1420,1080')
    options.add_argument('--disable-gpu')

    driver = webdriver.Remote("http://chrome:4444/wd/hub", options=options)

    try:
        logger.info("Open http://www.google.com")
        driver.get("http://www.google.com")
        driver.save_screenshot('test.png')
        logging.info("title=" + driver.title)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()



