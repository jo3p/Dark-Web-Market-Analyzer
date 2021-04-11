import os

from selenium.common.exceptions import WebDriverException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from helpers import WebDriver
from pathlib import Path

TYPE = 'ddos'  # 'login' or 'ddos'
SAVE_DIR = Path(f'{TYPE}-captchas')
N_SAMPLES = 100000


class CaptchaCollector:
    def __init__(self, save_dir: Path, n_samples: int):
        self.save_dir = save_dir
        self.n_samples = n_samples

        # Create folder to store captchas
        self.full_path = os.getcwd() / self.save_dir
        if not os.path.exists(self.full_path):
            os.makedirs(self.full_path)

    def collect_login_captchas(self):
        driver = WebDriver()
        driver.run()

        # Open captcha page
        for i in range(self.n_samples):
            i += 1
            file_name = f'captcha-{i}.png'
            file_path = self.full_path/file_name
            driver.driver.get('http://worldps45uh3rhedmx7g3jgjf3vw52wkvvcastfm46fzrpwoc7f33lid.onion/captcha.png')
            driver.driver.get_screenshot_as_file(str(file_path))

        driver.exit()

    def collect_ddos_captchas(self):
        start_no = 1
        while True:    
            driver = WebDriver()

            for i in range(start_no, self.n_samples):
                start_no = i
                file_name = f'captcha-{i}.png'
                file_path = self.full_path/file_name

                # try to load the webpage, if loading fails, break loop and relaunch WebDriver
                try:
                    driver.driver.get("http://worldps45uh3rhedmx7g3jgjf3vw52wkvvcastfm46fzrpwoc7f33lid.onion/")
                except WebDriverException:
                    driver.exit()
                    break

                # wait for the image to be loaded, otherwise break loop and restart
                try:
                    WebDriverWait(driver.driver, 100).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'img')))
                except TimeoutException:
                    driver.exit()
                    break
                finally:
                    pass

                # save CAPTCHA to disk and break loop if save fails.
                image_element = driver.driver.find_element_by_css_selector('img')
                save_result = image_element.screenshot(str(file_path))
                if save_result:
                    pass
                else:
                    driver.exit()
                    break
                i += 1


if __name__ == '__main__':
    # create collector instance
    captcha_collector = CaptchaCollector(SAVE_DIR, N_SAMPLES)

    # run scrape-function
    if TYPE == 'login':
        captcha_collector.collect_login_captchas()
    elif TYPE == 'ddos':
        captcha_collector.collect_ddos_captchas()
