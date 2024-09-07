from selenium.webdriver.common.by import By
from time import sleep
from selenium.common import exceptions
import csv

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from selenium import webdriver

# 创建保存文件
f = open("BOSS直聘1.csv", mode="a", encoding="utf-8-sig", newline="")
csv_writer = csv.DictWriter(
    f,
    fieldnames=[
        "职位名称",
        "地区",
        "薪水",
        "标签",
        "能力要求",
        "公司名字",
        "公司介绍",
        "福利待遇",
        "职位描述",
        "企业类型",
        "工作地址",
        "详情链接",
    ],
)
csv_writer.writeheader()  # 写入表头

options = Options()
webdriver_service = Service(
    "/usr/local/bin/chromedriver"
)  # 请将 'path/to/chromedriver' 替换为你的 ChromeDriver 路径

# 创建浏览器对象
driver = webdriver.Chrome(options=options, service=webdriver_service)
# 反检测
# 设置隐性等待时间为10s
driver.implicitly_wait(10)
driver.get(
    "https://www.zhipin.com/web/geek/job?query=%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90&city=101010100&page=1"
)

for page in range(1, 4):  # 爬取3页
    k = 0  # 用来设置每页爬取的数量，每页有30条数据，因全部爬取用selenium较慢，为测试效果每页只爬取5条
    sleep(2)
    # 滚动条滚到底部
    driver.execute_script(
        "document.documentElement.scrollTop = document.documentElement.scrollHeight"
    )
    li_lists = driver.find_elements(By.CSS_SELECTOR, ".job-card-wrapper")
    print(len(li_lists))

    for li in li_lists:
        job_name = li.find_element(By.CLASS_NAME, "job-name").text
        job_area = li.find_element(By.CLASS_NAME, "job-area").text
        salary = li.find_element(By.CLASS_NAME, "salary").text
        job_tag = li.find_element(
            By.CSS_SELECTOR, ".job-card-wrapper .job-card-left .tag-list"
        ).text.replace("\n", ",")
        job_ability = li.find_element(By.XPATH, "./div[2]/ul").text
        company_name = li.find_element(By.CLASS_NAME, "company-name").text
        welfare = li.find_element(By.CLASS_NAME, "info-desc").text
        link = li.find_element(By.CLASS_NAME, "job-card-left").get_attribute("href")
        # 点击详情页
        clic = li.find_element(By.CSS_SELECTOR, ".job-card-left")
        driver.execute_script("arguments[0].click()", clic)
        # 窗口切换到最新打开的页面
        driver.switch_to.window(driver.window_handles[-1])
        sleep(2)
        job_des = driver.find_element(
            By.XPATH, '//*[@id="main"]/div[3]/div/div[2]/div[1]/div[2]'
        ).text.replace("\n", " ")
        try:  # 有的公司没有公司介绍
            company_info = driver.find_element(
                By.CSS_SELECTOR, ".job-body-wrapper .company-info-box .fold-text"
            ).text.replace("\n", " ")
        except exceptions.NoSuchElementException:
            company_info = ""
        try:
            company_type = driver.find_element(
                By.CLASS_NAME, "company-type"
            ).text.replace("企业类型\n", "")
        except exceptions.NoSuchElementException:
            company_type = ""
        address = driver.find_element(By.CLASS_NAME, "location-address").text
        dic = {
            "职位名称": job_name,
            "地区": job_area,
            "薪水": salary,
            "标签": job_tag,
            "能力要求": job_ability,
            "公司名字": company_name,
            "公司介绍": company_info,
            "福利待遇": welfare,
            "职位描述": job_des,
            "企业类型": company_type,
            "工作地址": address,
            "详情链接": link,
        }
        # 写入数据
        csv_writer.writerow(dic)
        k += 1
        print(dic)
        driver.close()
        # 窗口切换到第一个页面
        driver.switch_to.window(driver.window_handles[0])
        if k == 5:  # 每页爬取5条数据
            break
    sleep(2)
    # 点击下一页，这里下一页的按钮不好定位，用XPATH的话只对1-4页有用，第五页后面要改成a[11]
    c = driver.find_element(By.XPATH, '//*[@class="options-pages"]/a[10]')
    driver.execute_script("arguments[0].click()", c)
driver.close()
driver.quit()
