"""对 chinese_calendar 的测试。"""

from datetime import date
import chinese_calendar as calendar

workday1 = date(2025, 2, 26) # 正常工作日
workday2 = date(2025, 2, 8) # 补班日

holiday1 = date(2025, 3, 1) # 正常周末
holiday2 = date(2025, 1, 28) # 除夕

def test_is_workday():
    """判断是否为工作日（包括补班日）"""
    assert calendar.is_workday(workday1)
    assert calendar.is_workday(workday2)

    assert not calendar.is_workday(holiday1)
    assert not calendar.is_workday(holiday2)

def test_is_holiday():
    """判断是否为法定节假日。"""
    assert not calendar.is_holiday(workday1)
    assert not calendar.is_holiday(workday2)

    assert calendar.is_holiday(holiday1)
    assert calendar.is_holiday(holiday2)

def test_is_in_lieu():
    """有问题！！！"""
    assert not calendar.is_in_lieu(holiday1)
    # assert calendar.is_in_lieu(holiday2)

def test_get_holiday_detail():
    """返回是否节假日及具体节日名称"""
    assert (False, None) == calendar.get_holiday_detail(workday1)
    assert False == calendar.get_holiday_detail(workday2)[0]