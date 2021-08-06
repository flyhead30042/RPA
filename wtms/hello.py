import logging
from  selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium import webdriver

from selenium import webdriver
from selenium.webdriver import DesiredCapabilities

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s | %(name)s | %(levelname)s | %(message)s"
                    )
logger = logging.getLogger(__name__)

def main():
    logger.info("Load webdriver")
    # driver = webdriver.Chrome(
    #     executable_path="webdriver/chromedriver-92.exe") if platform.system() == "Windows" else webdriver.Chrome()
    PROXY = "www-proxy.apac.mgmt.ericsson.se:8080"
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument("--no-sandbox")   # bypass OS security model
    options.add_argument("--disable-dev-shm-usage")  # overcome limited resource problems
    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--ignore-certificate-errors')

    # driver = webdriver.Remote("http://chrome:4444/wd/hub", options=options)
    driver = webdriver.Remote("http://localhost:4444/wd/hub", options=options)

    try:
        # driver.get("http://cpistore.internal.ericsson.com/elex#")
        driver.get("https://working-time-management-system-tw.internal.ericsson.com/#/login")

        logging.info("title=" + driver.title)
        logging.info("page source=" + driver.page_source[:500])
        driver.save_screenshot('test.png')
    finally:
        driver.quit()

if __name__ == "__main__":
    main()



