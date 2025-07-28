import openai
import os
import json
from spliter import split_text

from dotenv import load_dotenv

load_dotenv(".env")

from config import OPENROUTER_MODEL_GEMINI_20_FLASH, OPENROUTER_PREFIX, LLM_MODEL_DEEPSEEK_R1, LLM_MODEL_GPT_4O_MINI

TRANSLATE_PROMPT = """
用户将提供给你一段 OpenZeppelin 区块链智能合约相关的英文 AsciiDoc 文档内容，请你将内容翻译成中文，注意只做翻译，不要删减内容，不要添加解释和演绎。
输出格式保持 AsciiDoc 格式。

你必须严格遵循以下规则：
1. 保持所有 AsciiDoc 特有的标记和组件不变，比如：
   - 标题标记：= == === ====
   - 属性引用：{attribute}
   - 交叉引用：<<reference>>
   - 包含指令：include::[]
   - 块标记：[source], [NOTE], [TIP], [WARNING]
   - 链接格式：link:url[text] 或 https://url[text]

2. 遇到以下专业术语时，保留英文原文：
   - 区块链术语：Ethereum, Solidity, Smart Contract, Gas, Wei, Gwei
   - OpenZeppelin术语：OpenZeppelin, Contracts, Upgrades, Defender, Governor
   - 技术术语：JavaScript, TypeScript, Node.js, npm, yarn
   - 函数名、变量名、合约名等代码标识符

3. 翻译后的内容必须保持原文的结构，包括标题层级、段落、列表、表格、空行等和原文一致

4. 代码块处理规则：
   - 只翻译代码注释，代码本身保持不变
   - 保持代码块的语言标记，如 [source,solidity], [source,javascript]
   - 保持单行代码标记，如 `code`
   - 所有的合约代码、配置文件内容保持原文不变

5. 格式转换规则：
   - 保持所有链接格式不变，仅翻译链接文本内容
   - 文档属性（如 :page-title:）不翻译标记，仅翻译其对应的文本内容
   - 保持所有 AsciiDoc 指令和宏不变

6. 翻译完成后仔细检查：
   - 是否完整保留了所有 AsciiDoc 标记
   - 检查代码块、属性引用等是否和原文一致
   - 检查所有专业术语翻译是否恰当，没有合适的翻译请保持英文
"""

class LLMTranslator:
    def __init__(self, model=OPENROUTER_MODEL_GEMINI_20_FLASH):
        self.model = model

        # 初始化客户端，API密钥从环境变量读取
        if model.startswith("gpt-"):
            api_key=os.getenv("OPENAI_API_KEY")
            base_url=os.getenv("OPENAI_BASE_URL")

            self.client = openai.OpenAI(api_key=api_key, base_url=base_url)
        elif model.startswith("deepseek"):
            api_key = os.getenv("ALI_AI_API_KEY")
            base_url = os.getenv("ALI_AI_BASE_URL")

            self.client = openai.OpenAI(api_key=api_key, base_url=base_url)
        elif model.startswith(OPENROUTER_PREFIX):
            api_key = os.getenv("OPENROUTER_API_KEY")
            base_url = os.getenv("OPENROUTER_BASE_URL")

            colIndex = model.find(":")
            self.model = model[colIndex+1:]
            print(f"使用 OpenRouter 模型: {self.model}")
            self.client = openai.OpenAI(api_key=api_key, base_url=base_url)

    def simple_translate(self, text):
        system_prompt = "你是一个精通中文的与英文的计算机技术专家，请将以下英文内容翻译成中文，仅返回翻译后的中文内容，不要添加任何解释。"

        request_params = {
            "model": self.model,
            "temperature": 1, 
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text}
            ]
        }

        if self.model == LLM_MODEL_DEEPSEEK_R1:
            request_params["stream"] = True
            response = self.client.chat.completions.create(**request_params)
            
            # print(response.choices[0].message.reasoning_content)
            # print(response.choices[0].message.content)

            responseContent = ""
            for chunk in response:
                answer_chunk = chunk.choices[0].delta.content
                # print(answer_chunk)
                if answer_chunk and answer_chunk != "":
                    responseContent += answer_chunk
            return responseContent
        else:
            response = self.client.chat.completions.create(**request_params)
            return response.choices[0].message.content



    def translate_markdown(self, markdown_text):

        translated_text = ""
        chunks = split_text(markdown_text)

        for chunk in chunks:
            translated_chunk = self.translate(chunk)
            translated_text += translated_chunk

        return translated_text

    def translate(self, markdown_text):
        request_params = {
            "model": self.model,
            "temperature": 1.1, 
            "messages": [
                {"role": "system", "content": TRANSLATE_PROMPT},
                {"role": "user", "content": markdown_text}
            ]
        }

        if self.model == LLM_MODEL_DEEPSEEK_R1:
            request_params["stream"] = True
            response = self.client.chat.completions.create(**request_params)
            
            # print(response.choices[0].message.reasoning_content)
            # print(response.choices[0].message.content)

            print("等待 DEEPSEEK R1 大模型返回翻译结果...")
            responseContent = ""
            for chunk in response:
                if chunk and chunk.choices[0].delta.content:
                    answer_chunk = chunk.choices[0].delta.content
                    # print(answer_chunk)
                    if answer_chunk and answer_chunk != "":
                        responseContent += answer_chunk
            return responseContent
        else:
            response = self.client.chat.completions.create(**request_params)
            return response.choices[0].message.content
