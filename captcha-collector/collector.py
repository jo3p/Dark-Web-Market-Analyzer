import logging
import os
import time
from helpers import init_logging, WebDriver
from pathlib import Path

SAVE_DIR = Path('captchas')
N_SAMPLES = 100000


class CaptchaCollector:
    def __init__(self):
        logging.info("CAPTCHA-scraper launched.")

        # Initialize webdriver class
        self.driver = WebDriver()
        self.driver.run()

    def run(self, save_dir: Path, n_samples: int):
        full_path = os.getcwd()/save_dir
        logging.info(f"Start saving images in {full_path}")
        if not os.path.exists(full_path):
            os.makedirs(full_path)

        # Open captcha page
        for i in range(n_samples):
            i += 1
            file_name = f'captcha-{i}.png'
            file_path = full_path/file_name
            self.driver.driver.get('http://worldps45uh3rhedmx7g3jgjf3vw52wkvvcastfm46fzrpwoc7f33lid.onion/captcha.png')
            self.driver.driver.get_screenshot_as_file(str(file_path))
            logging.info(f'Saved CAPTCHA in {file_path}')
            time.sleep(0.1)

        self.driver.exit()
        logging.info(f"Stored {n_samples} images to {full_path}")


if __name__ == '__main__':
    # Initialize logging
    init_logging()
    captcha_collector = CaptchaCollector()
    captcha_collector.run(SAVE_DIR, N_SAMPLES)
