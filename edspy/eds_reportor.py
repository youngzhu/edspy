from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException

import chinese_calendar as calendar
import time
from datetime import date, timedelta

from . import _logger

from edspy.mimi import Mimi
from edspy.settings import Settings
from edspy.work_report import get_work_report

class EdsReportor:
    # 周报填写页面元素的ID与WorkReport字段的映射关系
    WEEKLY_REPORT_MAP = {
        'txtWorkContent': 'last_week_work_content', # 上周工作任务完成情况
        'txtStudyContent': 'last_week_study_content', # 上周学习完成任务情况
        'txtSummary': 'last_week_summary', # 经验和收获总结
        'txtPlanWork': 'work_plan', # 本周工作计划与重点
        'txtPlanStudy': 'study_plan', # 本周学习计划
    }

    def __init__(self) -> None:
        self.mimi = Mimi()
        self.settings = Settings()

    def run(self):
        """完成每周的周报和日报"""
        self._add_driver()

        _logger.info("Run the logger")
        self._login()
        # time.sleep(5)

        if self.settings.debugging:
            _logger.info("调试中...")
        else:
            # 准备周报的数据
            # TODO 后面考虑并发
            self._prepped_data()

            # 填周报
            self._weekly_report()
            time.sleep(2)

            # 开始填日报
            self._daily_report()

    def _daily_report(self):
        # print(f'日报内容：{self.logContent.daily()}')
        self.driver.get(self.settings.daily_url)

        # 填7天
        report_date = date.today()
        # report_date = date(2025, 3, 3)
        for _ in range(7):
            self._do_daily_report(report_date)
            time.sleep(1)

            # 当天日报完成，NEXT
            self.driver.find_element(By.ID, "btnnext").click()
            report_date = report_date + timedelta(days=1)
    
    def _do_daily_log(self, report_date):
        """填日报"""
        if self._should_report(report_date):
            memo = self.work_report.daily_work_report()

            # 页面上点2次【确定】，即可完成一天的日志
            # 上午
            # self.driver.find_element(By.ID, "txtMemo").send_keys(memo)
            # self.driver.find_element(By.ID, "btnSave").click()
            # 下午
            # self.driver.find_element(By.ID, "txtMemo").send_keys(memo)
            # self.driver.find_element(By.ID, "btnSave").click()
            for member in AMPM:
                btn_save = WebDriverWait(self.driver, self.settings.timeout).until(
                    EC.presence_of_element_located((By.ID, "btnSave"))
                )

                try:
                    self.driver.find_element(By.ID, "txtMemo").send_keys(memo)
                    # self.driver.find_element(By.ID, "btnSave").click()
                    btn_save.click()

                except Exception as e:
                    _logger.error(f"日报{report_date} {member.value} 出现错误：{e}")
                
                time.sleep(1)

            _logger.info(f"{report_date} - 日报完成")

    def _should_report(self, report_date):
        """ {report_date} 这天是否还需要填写日报"""
        if calendar.is_workday(report_date):
            # 开始时间 
            # 还未填日志的，有值；已经填过的，值为空
            retries = 3
            for i in range(retries):
                try:
                    start_time = WebDriverWait(self.driver, self.settings.timeout).until(
                        EC.presence_of_element_located((By.ID, "txtStartTime"))
                    )
                    break
                except StaleElementReferenceException:
                    _logger.info(f"retry {retries}...")
                    if i == retries - 1:
                        raise
            start_time_value = start_time.get_attribute("value")
            # print(f"{report_date}: {start_time_value}")
            
            if start_time_value:
                return True
            else:
                print(f"{report_date} - 已填写")
                return False
        else:
            print(f"{report_date} - 休息")
            return False

    def _weekly_report(self):
        """填周报"""
        self.driver.get(self.settings.weekly_url)

        # 周报填写日期：周一
        monday = date.today()
        # monday = date(2025, 3, 3)
        week_report_date = self.driver.find_element(By.ID, "WeekReportDate")
        week_report_date.clear()
        week_report_date.send_keys(str(monday))

        # 填充周报内容
        for key, val in self.WEEKLY_REPORT_MAP.items():
            element = self.driver.find_element(By.ID, key)
            element.clear()
            element.send_keys(getattr(self.work_report, val))
                                
        # 提交
        self.driver.find_element(By.ID, "lblSubmit").click()

        _logger.info('周报填写完成')

    def _prepped_data(self):
        """准备周报数据"""
        self.work_report = get_work_report(self)


    def _login(self):
        """登录"""
        user_id = self.mimi.user_id
        user_pwd = self.mimi.user_pwd
        self.driver.get(self.settings.login_url)

        btn = WebDriverWait(self.driver, self.settings.timeout).until(
            EC.presence_of_element_located((By.ID, "btnSubmit"))
        )
        self.driver.find_element(By.ID, "UserId").send_keys(user_id)
        self.driver.find_element(By.ID, "UserPassword").send_keys(user_pwd)
        btn.click()

        # print(f"{self.driver.current_url}")

        # 等待页面加载完成
        WebDriverWait(self.driver, self.settings.timeout).until(EC.url_contains("StffIndex.aspx"))
        # print(f"{self.driver.current_url}")
        # time.sleep(200)
        _logger.info("登录成功！")

    def _add_driver(self):
        """添加WebDriver

        不放在 init 里，是因为单元测试里不需要
        """
        # options = webdriver.ChromeOptions()
        options = Options()
        options.add_argument("--headless=new")

        # 解决了握手问题，又有其他问题。。。
        # options.add_argument('--ignore-certificate-errors')
        # options.add_argument('--disable-cache') # 禁用缓存

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
        if self.settings.action:
            _logger.info("使用 DriverManager")
            service = Service(ChromeDriverManager().install()) # 本地执行，网络不行
            
        self.driver = webdriver.Chrome(options=options, service=service) 
        # 不用 driver 好像也可以啊
        # self.driver = webdriver.Chrome(options=options) 

from enum import Enum

class AMPM(Enum):
    AM = "AM"  # 显式赋值
    PM = "PM"  # 显式赋值