import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from selenium.webdriver.chrome.service import Service

from selenium.webdriver.common.action_chains import ActionChains

from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementNotInteractableException

from datetime import datetime

home_url = "https://trainspace.cfnet.org.cn/K200#/"

class ChangFeng(object):
    def __init__(self, mobile, password):
        self.mobile = mobile
        self.password = password

        driver_path = r'E:/drivers/chromedriver-win64/chromedriver.exe'
        # driver_path = r"E:\drivers\chromedriver-win64\chromedriver.exe"
        # driver_path = r'E:/drivers/chromedriver-win32/chromedriver.exe'
        service = Service(executable_path=driver_path)
        self.driver = webdriver.Chrome(service=service)
        # self.driver = webdriver.Chrome()

    def click(self):
        """查找弹出框，如果有则点击，如果没有则等待"""
        while True:
            # /html/body/div[3]/div/button
            confirm_xpath = "/html/body/div[3]/div/button"

            try:
                # button = self.driver.find_element(by=By.XPATH, value=confirm_xpath)
                # print(f"元素是否可见: {button.is_displayed()}, 是否可点击: {button.is_enabled()}")
                # button.click()

                # 有些弹窗是异步加载的，需要显式等待
                wait = WebDriverWait(self.driver, 5)
                alert_div = wait.until(
                    EC.visibility_of_element_located((By.XPATH, "/html/body/div[3]"))
                )
                alert_div.find_element(By.XPATH, "./div/button").click()

                # 处理可能的遮挡问题
                # ActionChains(self.driver).move_to_element(button).click().perform()

                # alert = self.driver.switch_to.alert
                # alert.accept()  # 点击确定

                current_time = datetime.now().strftime("[%H:%M:%S]")  # 例如 [15:30:22]
                print(f"{current_time} ###点击确定###")
            except NoSuchElementException:
                print("###还没到时间###")
                # pass
            except Exception as e:  # 其他异常
                print(f"发生未知错误: {str(e)}")

            time.sleep(50)


    def login(self):
        self.driver.get(home_url)  # 载入登录界面
        print('###开始登录###')
        try:
            # /html/body/div/div/div[1]/div/div/div[3]/button[1]
            login_button_xpath = "/html/body/div/div/div[1]/div/div/div[3]/button[1]"
            #
            login_button = (WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.XPATH, login_button_xpath))))
            login_button.click()
            time.sleep(1)

            # 手机号
            # /html/body/div/div/div[1]/div/div/div[4]/div[2]/div/div[2]/div/div[2]/div/div/div[1]/input
            mobile_xpath = "/html/body/div/div/div[1]/div/div/div[4]/div[2]/div/div[2]/div/div[2]/div/div/div[1]/input"
            self.driver.find_element(by=By.XPATH, value=mobile_xpath).send_keys(self.mobile)
            # 密码
            # /html/body/div/div/div[1]/div/div/div[4]/div[2]/div/div[2]/div/div[2]/div/div/div[2]/input
            # /html/body/div/div/div[1]/div/div/div[4]/div[2]/div/div[2]/div/div[2]/div/div/div[2]/input
            pwd_xpath = "/html/body/div/div/div[1]/div/div/div[4]/div[2]/div/div[2]/div/div[2]/div/div/div[2]/input"
            self.driver.find_element(by=By.XPATH, value=pwd_xpath).send_keys(self.password)
            # 登录
            # /html/body/div/div/div[1]/div/div/div[4]/div[2]/div/div[2]/div/div[2]/div/div/button/span
            login_xpath = "/html/body/div/div/div[1]/div/div/div[4]/div[2]/div/div[2]/div/div[2]/div/div/button/span"
            self.driver.find_element(by=By.XPATH, value=login_xpath).click()
        except Exception as e:
            print(e)
            # print('###定位不到登录框###')

        # self.driver.switch_to.frame('alibaba-login-box')  # 里面这个是iframe的id
        # self.driver.find_element_by_id('fm-login-id').send_keys(self.uid)
        # self.driver.find_element_by_id('fm-login-password').send_keys(self.upw)
        # self.driver.find_element_by_tag_name("button").click()
        print('###登录成功###')



if __name__ == '__main__':
    try:
        # print('如果需要就点击')

        cf = ChangFeng('15201705723', '123456')
        cf.login()

        cf.click()

        time.sleep(1000)

        # /html/body/div[5]/div/div[1]/p/ul
        # #timeout
    except Exception as e:
        print(e)
        exit(1)