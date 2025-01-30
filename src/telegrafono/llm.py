from typing import Any, Tuple
import requests
import re

url = "http://127.0.0.1:5555/v1/chat/completions"
headers = {
    "Content-Type": "application/json"
}

def request_llm(query: str) -> Any:
    data = {
        "model": "deepseek-r1-distill-qwen-7b",
        "messages": [
            {"role": "user", "content": query}
        ],
        "temperature": 0.7,
        "max_tokens": -1,
        "stream": False
    }
    response = requests.post(url, headers=headers, json=data, stream=True)
    return response.json()

def parse_llm_response(response: Any) -> tuple[str, str]:
    content = response["choices"][0]["message"]["content"]
    thinking_match = re.search(r'<think>(.*?)</think>', content, re.DOTALL)
    if thinking_match:
        thinking_content = thinking_match.group(1)
        remaining_content = content.replace(thinking_match.group(0), '').strip()
        return thinking_content, remaining_content
    return thinking_content, remaining_content

if __name__ == "__main__":
    proc = request_llm("What information do you have about JAC?")
    thinking, remaining = parse_llm_response(proc)
    print(f"Thinking: {thinking}")
    print(f"Remaining: {remaining}")