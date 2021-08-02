import logging
import platform
from time import sleep

from selenium import webdriver


logger = logging.getLogger(__name__)


logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s | %(name)s | %(levelname)s | %(message)s"
                    )

def main():
    logger.info("Load webdriver")
    # driver = webdriver.Chrome(
    #     executable_path="webdriver/chromedriver-92.exe") if platform.system() == "Windows" else webdriver.Chrome()
    PROXY = "www-proxy.apac.mgmt.ericsson.se:8080"
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument("--no-sandbox")   # bypass OS security model
    options.add_argument("--disable-dev-shm-usage")  # overcome limited resource problems
    # options.add_argument('--proxy-server=http://' + PROXY)

    capabilities = webdriver.DesiredCapabilities.CHROME.copy()
    capabilities["proxy"] = {
        "httpProxy": PROXY,
        "ftpProxy": PROXY,
        "sslProxy": PROXY,
        "proxyType": "MANUAL",
    }

    # driver = webdriver.Remote("http://chrome:4444/wd/hub", options=options)
    driver = webdriver.Remote("http://localhost:4444/wd/hub", options=options, desired_capabilities = capabilities)

    try:
        # driver.get("https://www.google.com/")
        driver.get("https://working-time-management-system-tw.internal.ericsson.com/#/login")
        driver.save_screenshot('test.png')
        logging.info("title=" + driver.title)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()



