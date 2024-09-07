import argparse
from notion_client import Client
import os

# 初始化 Notion 客户端
notion = Client(auth="secret_3bHaTYpWVZVU6e9UuAxSabtDEUAsnBK00mIcWbslNRF")


def upload_to_notion(file_path):
    # 读取文件内容
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    # 文件名作为标题
    title = os.path.basename(file_path)

    # 创建 Notion 页面
    notion.pages.create(
        parent={"database_id": "41c7fac6dece48af8cf496223aafb694"},
        properties={"标题": {"title": [{"type": "text", "text": {"content": title}}]}},
        children=[
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [  # 使用 rich_text 而不是 text
                        {"type": "text", "text": {"content": content}}
                    ]
                },
            }
        ],
    )


# 解析命令行参数
parser = argparse.ArgumentParser(description="Upload a file to Notion.")
parser.add_argument("file_path", type=str, help="The path of the file to upload")

args = parser.parse_args()

# 执行上传
upload_to_notion(args.file_path)
