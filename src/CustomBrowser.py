import os
import time
from inspect import isfunction

from selenium import webdriver


class CustomBrowser(object):

    def __init__(self, cookies, user_agent, chromedriver_path=None, chrome_path=None):

        chrome_options = webdriver.ChromeOptions()
        chrome_options.headless = True
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument(f'user-agent="{user_agent}"')
        chrome_options.add_argument(f'--user-data-dir={os.path.dirname(os.getcwd())}/Browser/Data')
        chrome_options.add_argument(f'-–disk-cache-dir={os.path.dirname(os.getcwd())}/Browser/Cache')
        chrome_options.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])
        if chrome_path:
            chrome_options.binary_location = chrome_path
        if chromedriver_path:
            self.client = webdriver.Chrome(executable_path=chromedriver_path, chrome_options=chrome_options)
        else:
            self.client = webdriver.Chrome(chrome_options=chrome_options)
        client = self.client
        domain = 'jd.com'
        url = f'www.{domain}'
        client.get(f'https://{url}')
        time.sleep(1)
        for cookie in iter(cookies):
            if domain in cookie.domain:
                cookie_dict = {
                    'name': cookie.name,
                    'value': cookie.value,
                    'path': cookie.path,
                    'domain': cookie.domain,
                    'secure': cookie.secure
                }
                if cookie.expires:
                    cookie_dict['expiry'] = cookie.expires
                client.add_cookie(cookie_dict)

    def openUrl(self, url, jsScript=None, timeout=5):
        client = self.client
        client.set_script_timeout(timeout)
        client.get(url)
        if jsScript:
            js_str = jsScript.js_str
            if js_str:
                time.sleep(2)
                js_data = client.execute_script(js_str)
                js_callback = jsScript.js_callback
                if isfunction(js_callback):
                    return js_callback(js_data)
        return client.page_source

    def quit(self):
        self.client.quit()


class JsScript:

    def __init__(self, js_str, js_callback):
        self.js_str = js_str
        self.js_callback = js_callback
