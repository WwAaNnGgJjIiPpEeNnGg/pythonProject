import openai
import os

# 设置API密钥

openai.api_key = os.environ["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"]

# 调用API生成文本
response = openai.Completion.create(
  engine="davinci",
  prompt="Hello, my name is",
  max_tokens=5
)
# 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
# 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
# 输出生成的文本
print(response.choices[0].text)
