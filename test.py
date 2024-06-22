import requests
import json

def test_get_book_info(image_url):
    api_url = "https://api.pumpkinaigc.online/v1/chat/completions"
    headers = {
        "Authorization": "Bearer sk-5g27w3Dwsd0KnmLvB53f988fC0E24dE2880cC87c47E4864d",  # 替换为你的 OpenAI API Key
        "Content-Type": "application/json"
    }

    data = {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "根据这张图书封面，以json的格式，查询后告诉我这本书的title,author,publisher,publication,isbn,category.无需告我我其他内容"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_url
                        }
                    }
                ]
            }
        ]
    }

    response = requests.post(api_url, headers=headers, data=json.dumps(data))
    response_json = response.json()
    print(response_json)

# 测试获取书籍信息
test_get_book_info("https://pics4.baidu.com/feed/f31fbe096b63f62430fdd9e135548ef51b4ca34a.jpeg@f_auto?token=bd2415d6c1c854c59b59a590b8bc3447")
