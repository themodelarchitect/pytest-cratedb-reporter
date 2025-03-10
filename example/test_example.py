import time 

def test_pass():
    time.sleep(2)
    assert True

def test_fail():
    time.sleep(1)
    assert False
