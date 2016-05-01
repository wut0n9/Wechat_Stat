# coding:utf8

import logging
import os
from time import sleep
from appium import webdriver
import re
import codecs


PLATFORM_VERSION = '5.1.1'
logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', level=logging.INFO)
pattern = re.compile(r'&#\d+;')

YOUR_QQ = 'YOUR_QQ'
YOUR_PASSWORD = 'YOUR_PASSWORD'


class Wechat():
    """
    本程序运行可能需要这样：node --max_old_space_size=4096 ./software/..../appium
    """

    def __int__(self):

        app = os.path.abspath(
                os.path.join(os.path.dirname(__file__),
                             'weixin6313android740.apk'))

        desired_caps = {
            'app': app,
            'appPackage': 'com.tencent.mm',
            'appActivity': '.ui.LauncherUI',
            'platformName': 'Android',
            'platformVersion': PLATFORM_VERSION,
            'deviceName': 'ZTEQ519T',  # emulator-22 It's True
            # 'automationName': 'selendroid',
            'newCommandTimeout': 90,  # default 60s
            'unicodeKeyboard': True,
            'resetKeyboard': True,
            'autoWebviewTimeout': 3000,
            'autoWebview': True
        }
        """
        Android < 4.4
        if (PLATFORM_VERSION != '4.4'):
            desired_caps['automationName'] = 'selendroid'
        """
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
        self.loginWechat()

    def loginWechat(self):
        self.driver.implicitly_wait(40)
        button_login = self.driver.find_element_by_name(u'语言')
        # sleep(20)
        button_login.click()
        sleep(1)
        self.driver.find_elements_by_xpath('//android.widget.CheckBox')[4].click()
        self.driver.find_element_by_name(u'保存').click()
        self.driver.implicitly_wait(30)
        self.driver.find_element_by_name('Log In').click()
        self.driver.find_element_by_name('Change Login Mode').click()
        username = self.driver.find_element_by_name('WeChat ID/Email/QQ ID')
        sleep(0.3)
        username.send_keys(YOUR_QQ)
        sleep(0.3)
        password = self.driver.find_elements_by_xpath('//android.widget.EditText')[1]
        sleep(0.3)
        password.send_keys(YOUR_PASSWORD)

        self.driver.find_element_by_name('Log In').click()
        self.driver.implicitly_wait(30)
        # self.driver.find_element_by_name('No').click()
        self.driver.implicitly_wait(100)  # 必须

        self.driver.find_element_by_name('Discover').click()
        sleep(.1)
        self.driver.find_element_by_name('Moments').click()
        sleep(3)

        self.getall()

    def getall(self):
        i = 0
        singal_page_content = []
        while True:

            # Very important
            sleep(4)
            ps = self.driver.page_source
            if '&#' in ps:
                ps_delete = pattern.sub('', ps)
                # print ps_delete
                with codecs.open('wechat.utf8.text', encoding='utf-8', mode='ab') as f:
                    f.write(ps_delete + '\n')
            del ps
            # swipe down
            self.driver.swipe(start_x=520, start_y=1000, end_x=520, end_y=0, duration=250)  # duration越小，swipe跨度越大

        self.driver.quit()


if __name__ == '__main__':
    Wechat().__int__()