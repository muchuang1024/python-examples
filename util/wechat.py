from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import argparse


def fetch_article_content(url):
    # 设置 WebDriver
    service = Service(ChromeDriverManager().install())
    browser = webdriver.Chrome(service=service)

    try:
        # 使用 Selenium 打开页面
        browser.get(url)

        # 等待页面加载，可能需要根据实际情况调整
        # 例如：WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, 'element_id')))

        # 提取文章内容，更新选择器的使用方式
        article_content = browser.find_element(By.ID, "js_content").text
        return article_content
    finally:
        browser.quit()


def generate_summary(article_text):
    # 生成摘要
    summary = article_text[:200]  # 示例：提取前200个字符
    return summary


def main():
    parser = argparse.ArgumentParser(
        description="Extract summary from a WeChat article link."
    )
    parser.add_argument("url", help="URL of the WeChat article")
    args = parser.parse_args()

    article_text = fetch_article_content(args.url)
    summary = generate_summary(article_text)
    print(summary)


if __name__ == "__main__":
    main()
