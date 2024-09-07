import openai
import argparse
import os


def summarize_text(file_path, openai_api_key):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")

    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    openai.api_key = openai_api_key

    prompt_message = (
        "作为一个专业的阅读助手，你的任务是总结文章的主要内容。用户可能会给你文章的文本或链接。"
        "对于文本输入，直接提取并总结关键信息。如果给出的是链接，使用你的浏览能力访问并阅读该链接的内容，然后进行总结。"
        "请按以下格式输出摘要：\n\n"
        "**#标题**\n"
        "- [在这里输入文章的主题或标题]\n\n"
        "**#一句话总结**\n"
        "- [用一句话简洁概括文章的核心内容]\n\n"
        "**#关键信息点**\n"
        "- [罗列文章中的主要信息点，用点列形式展示]\n\n"
        "**#内容问答**\n"
        "- [如果文章中包含问答形式的内容，这里提取并列出一问一答]\n\n"
        "**#标签**\n"
        "- [基于文章内容，提供最多三个相关标签，以捕捉文章的关键主题]"
    )

    print(
        [
            {
                "role": "system",
                "content": "提取文章摘要",
            },
            {"role": "user", "content": f"{prompt_message}\n\n{content}"},
        ]
    )

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "提取文章摘要.",
            },
            {"role": "user", "content": f"{prompt_message}\n\n{content}"},
        ],
    )

    return response.choices[0].message["content"]


def main():
    parser = argparse.ArgumentParser(
        description="Summarize a text file using OpenAI GPT-3.5-turbo."
    )
    parser.add_argument(
        "file_path", type=str, help="Path to the text file to summarize."
    )
    parser.add_argument("--api_key", type=str, required=True, help="OpenAI API key.")
    args = parser.parse_args()

    summary = summarize_text(args.file_path, args.api_key)
    print("Summary:")
    print(summary)


if __name__ == "__main__":
    main()
