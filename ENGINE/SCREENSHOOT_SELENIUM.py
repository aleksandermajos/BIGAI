from selenium import webdriver

# 1. create a web driver instance
driver = webdriver.Chrome()

# 2. navigate to the website
driver.get("https://www.hackerrank.com/challenges/three-month-preparation-kit-plus-minus/problem?isFullScreen=true&h_l=interview&playlist_slugs%5B%5D=preparation-kits&playlist_slugs%5B%5D=three-month-preparation-kit&playlist_slugs%5B%5D=three-month-week-one")

# 3. save a screenshot of the current page
driver.save_screenshot("hr1.png")

# 4. close the web driver
driver.quit()