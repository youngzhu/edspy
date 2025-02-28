from datetime import date

def test_today():
    assert date.today()

def test_date_format():
    test_date = date(2025, 3, 1)
    assert str(test_date) == "2025-03-01"
    assert not str(test_date) == "2025/03/01"
    assert test_date.strftime("%Y-%m-%d") == "2025-03-01" 