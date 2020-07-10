from selenium import webdriver
import time

try:
    browser = webdriver.Chrome()
    # 需要安装chrome driver, 和浏览器版本保持一致
    # http://chromedriver.storage.googleapis.com/index.html
    
    browser.get(' https://shimo.im')
    time.sleep(1)

   # browser.switch_to_frame(browser.find_elements_by_tag_name('iframe')[0])
    btm1 = browser.find_element_by_xpath('//button[@class="login-button btn_hover_style_8"]')
    btm1.click()

    browser.find_element_by_xpath('//input[@type="text"]').send_keys('15055495@qq.com')
    browser.find_element_by_xpath('//input[@type="password"]').send_keys('test123test456')
    time.sleep(1)
    browser.find_element_by_xpath('//button[@class="sm-button submit sc-1n784rm-0 bcuuIb"]').click()

    cookies = browser.get_cookies() # 获取cookies
    print(cookies)
    time.sleep(3)

except Exception as e:
    print(e)
finally:    
    browser.close()
    