import os
import time
from datetime import date

from dotenv import load_dotenv

from settings import Settings
from log_content import LogContent
from mimi import Mimi

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class EdsLogger:
    def __init__(self):
        load_dotenv()
        self.mimi = Mimi()
        self.settings = Settings()

        # options = webdriver.ChromeOptions()
        options = Options()
        # options.add_argument("--headless=new")

        # options.add_argument('--ignore-certificate-errors')
        # options.add_argument('--ignore-ssl-errors')
        # options.add_argument('--allow-insecure-localhost')  # 允许本地不安全的连接
        # options.add_argument("--disable-extensions")  # 禁用扩展
        # options.add_argument("--no-sandbox")         # 禁用沙箱模式（Linux环境下可能需要）
        # options.add_argument("--disable-dev-shm-usage")  # 避免内存不足问题
        # options.add_argument("--disable-gpu")
        # options.add_argument("--disable-blink-features=AutomationControlled")
        # options.add_experimental_option("excludeSwitches", ["enable-automation"])
        # options.add_argument("--user-data-dir=/tmp/chrome-test-profile")
        # 忽略SSL证书错误（临时方案）
        # options.add_argument("--ignore-certificate-errors")
        # # 禁用TLS/SSL协议兼容性检查
        # options.add_argument("--ssl-version-min=tls1.2")
        # # 允许不安全的本地主机（针对本地测试）
        # options.add_argument("--allow-insecure-localhost")
        # # 禁用QUIC协议（避免网络协议冲突）
        # options.add_argument("--disable-quic")
        # options.add_argument("--ignore-certificate-errors")
        # options.add_argument("--ssl-version=tls1.2")
        # options.add_argument("--allow-insecure-localhost")
        # options.add_argument("--disable-web-security")  # 允许跨域请求（针对复杂登录场景）

        # 绕过自动化检测机制
        # options.add_argument("--disable-blink-features=AutomationControlled")
        # options.add_experimental_option("excludeSwitches", ["enable-automation"])
        # options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")

        # options.add_argument("--no-sandbox")
        # options.add_argument("--disable-dev-shm-usage")
        # options.add_argument("--disable-gpu")
        # options.add_argument("--disable-software-rasterizer")

        # options.add_argument("--proxy-server='direct://'")
        # options.add_argument("--proxy-bypass-list=*")

        # options.add_argument("--no-sandbox")          # 禁用沙箱（Linux/Windows高权限需求）
        # options.add_argument("--disable-dev-shm-usage") # 避免共享内存不足
        # options.add_argument("--disable-blink-features=AutomationControlled") # 绕过自动化检测

        # 为什么不能起名为 webdriver ？
        # self.webdriver = webdriver.Chrome()
        # self.driver = webdriver.Chrome(options=options)
        driver_path = r'E:/drivers/chromedriver-win64/chromedriver.exe'
        # driver_path = r"E:\drivers\chromedriver-win64\chromedriver.exe"
        # driver_path = r'E:/drivers/chromedriver-win32/chromedriver.exe'
        service = Service(executable_path=driver_path)
        # service = Service(
        #     executable_path=driver_path,
        #     log_output="chromedriver_ssl_error.log",  # 日志输出到文件
        #     service_args=["--verbose"]             # 启用详细日志
        # )
        # service = Service(ChromeDriverManager().install()) # 网络不行
        self.driver = webdriver.Chrome(options=options, service=service) 
        # 不用 driver 好像也可以啊
        # self.driver = webdriver.Chrome(options=options) 


    def run(self):
        """完成每周的周报和日报"""
        print("Run the logger")
        self._login()
        time.sleep(1)

        # 准备周报的数据
        self._prepped_data()

        # 填周报
        self._do_weekly_log()
        time.sleep(2)

        # 开始填日报
        self._do_daily_log()

    def _do_weekly_log(self):
        """填周报"""
        # self.driver.find_element(By.ID, "lblWorkLog").click()
        self.driver.get("http://eds.newtouch.cn/eds36web/WorkWeekly/WorkWeeklyInfo.aspx")

        # 周报填写日期：周一
        monday = date.today()
        monday = date(2025, 3, 3)
        week_report_date = self.driver.find_element(By.ID, "WeekReportDate")
        week_report_date.clear()
        week_report_date.send_keys(str(monday))

        # 上周工作任务完成情况
        work_content = self.driver.find_element(By.ID, "txtWorkContent")
        work_content.clear()
        work_content.send_keys(self.logContent.weeklyWorkContent)

        # 上周学习完成任务情况
        study_content = self.driver.find_element(By.ID, "txtStudyContent")
        study_content.clear()
        study_content.send_keys(self.logContent.weeklyStudyContent)
        
        # 经验和收获总结
        summary = self.driver.find_element(By.ID, "txtSummary")
        summary.clear()
        summary.send_keys(self.logContent.weeklySummary)
                
        # 本周工作计划与重点
        plan_work = self.driver.find_element(By.ID, "txtPlanWork")
        plan_work.clear()
        plan_work.send_keys(self.logContent.weeklyPlanWork)
                        
        # 本周学习计划
        plan_study = self.driver.find_element(By.ID, "txtPlanStudy")
        plan_study.clear()
        plan_study.send_keys(self.logContent.weeklyPlanStudy)
                                
        # 提交
        self.driver.find_element(By.ID, "lblSubmit").click()

    def _do_daily_log(self):
        print(f'日报内容：{self.logContent.daily()}')
        # self.driver.get(self.settings.daily_url)
        # self.driver.get("http://eds.newtouch.cn/eds3/worklog.aspx")




    def _prepped_data(self):
        """准备周报数据"""
        self.logContent = LogContent(self)
        self.logContent.get()

    
    def _login(self):
        """登录"""
        user_id = os.getenv("USER_ID")
        user_pwd = os.getenv("USER_PWD")
        # print("Login as user: " + userId)
        # print(self.settings.login_url
        self.driver.get(self.settings.login_url)
        self.driver.find_element(By.ID, "UserId").send_keys(user_id)
        self.driver.find_element(By.ID, "UserPassword").send_keys(user_pwd)
        self.driver.find_element(By.ID, "btnSubmit").click()

        # 等待页面加载完成
        # WebDriverWait(self.driver, 10).until(
        #     EC.presence_of_element_located((By.ID, "lblWorkLog"))
        # )
        print("登录成功！")
        