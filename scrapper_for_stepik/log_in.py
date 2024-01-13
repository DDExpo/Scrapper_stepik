import json
import os

from playwright.sync_api import Browser
from dotenv import load_dotenv

load_dotenv()

BASE_PATH = os.getenv('BASE_PATH')


def log_in_to_github(browser: Browser, courseid: str):

    url = f'https://stepik.org/course/{courseid}/promo?auth=login"'

    page = browser.new_page()
    page.goto(url, wait_until='commit')
    page.get_by_alt_text('GitHub').click()

    page.fill('input#login_field', os.getenv('LOGIN'))
    page.fill('input#password', os.getenv('PASSWORD'))
    page.wait_for_timeout(5000)

    page.click(
        'xpath=/html/body/div[1]/div[3]/main/div/div[3]/form/div/input[13]'
    )

    page.wait_for_timeout(7000)

    file = open(BASE_PATH + 'data.json',
                'w', encoding='utf-8')
    json.dump(page.context.cookies(), file,
              ensure_ascii=False, indent=4)

    file.close()
    page.close()
