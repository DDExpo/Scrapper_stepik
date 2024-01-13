import json
import os

from playwright.sync_api import sync_playwright
import lxml.html as html

from Projects.scrapping.scrapper_for_stepik.Scrapper_stepik.scrapper_for_stepik.log_in import log_in_to_github, BASE_PATH
from text_formatter import text_formatting


url = 'https://stepik.org/lesson/307317/step/8?unit=289405'
lesson = [part for part in url.split('/') if part.isdigit()][0]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
    'AppleWebKit/537.36 (KHTML, like Gecko)'
    ' Chrome/118.0.0.0 YaBrowser/23.11.0.0 Safari/537.36'
}

while True:
    with sync_playwright() as p:
        browser = p.chromium.launch()
        browser_with_cookie = browser.new_context()
        browser_with_cookie.add_cookies(
            json.load(open(BASE_PATH + 'data.json'))
        )
        page = browser_with_cookie.new_page()
        page.goto(url)
        page.wait_for_timeout(7000)

        if page.is_visible('xpath=/html/body/main/section[1]/div/div/h1'):
            log_in_to_github(browser, lesson)
            new_cookies = json.load(open(
                BASE_PATH + 'data.json')
            )
            browser.close()
            continue

        tree = html.document_fromstring(page.content())
        data = tree.xpath('//*[@class="step-inner page-fragment"]')
        name, text, examples = text_formatting(data)

        if not os.path.exists(os.path.dirname(os.path.realpath(__file__)) + '/stepik'):
            os.makedirs('stepik')

        with open(BASE_PATH + f'stepik/{name}' + 'txt',
                'w', encoding='utf-8') as file:
            file.writelines(text)
            file.writelines(examples)

        browser.close()
        break
