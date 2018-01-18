from selenium import webdriver

browser = webdriver.Chrome()
browser.get(raw_input("https://twitter.com/kingstoune/followers"))
html_source = browser.page_source

print html_source