import requests
import os
import sys
import json


def get_token():
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"

    # 准备请求体
    payload = {
        "app_id": "cli_a51cf7beeeae500b",
        "app_secret": "Y96LVVrbBfgEFj7jN1aXDc2CfSHSIgFQ",
    }
    headers = {"Content-Type": "application/json"}

    # 发送 POST 请求
    response = requests.post(url, headers=headers, data=json.dumps(payload))

    # 解析响应
    if response.status_code == 200:
        token_info = response.json()
        # print("Token Info:", token_info)
    else:
        print("Failed to get token. Status code:", response.status_code)

    return token_info["tenant_access_token"]


def get_document_content(document_id):
    # 从环境变量读取 token
    token = get_token()

    if not token:
        print("Token not found in environment variables.")
        return

    headers = {"Authorization": f"Bearer {token}"}
    url = "https://open.feishu.cn/open-apis/docx/v1/documents/{}/raw_content?lang=0".format(
        document_id
    )

    print(url)
    response = requests.get(url, headers=headers)
    return response.text


# python3 feishu.py https://open.feishu.cn/open-apis/docx/v1/documents/HLZbdktF3onqpux550kc35f5n0e/raw_content\?lang\=0
def main():
    # 检查命令行参数
    if len(sys.argv) != 2:
        print("Usage: python3 xxx.py [url]")
        sys.exit(1)

    url = sys.argv[1]
    # 使用 split 方法分割 URL
    parts = url.split("/")

    # 'document_id' 是倒数第二个部分
    document_id = parts[-1]
    content = get_document_content(document_id)
    print(content)


if __name__ == "__main__":
    main()
