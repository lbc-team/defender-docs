import llm_translator
from config import LLM_MODEL_DEEPSEEK_V3, LLM_MODEL_GPT_4O_MINI, OPENROUTER_MODEL_GEMINI_20_FLASH
import os
from pathlib import Path


def translate_markdownx(content):
    models = [OPENROUTER_MODEL_GEMINI_20_FLASH, LLM_MODEL_GPT_4O_MINI]
    for model in models:
        try:
            translator = llm_translator.LLMTranslator(model)
            result = translator.translate_markdown(content)
            if result:
                return result
        except Exception as e:
            print(f"使用模型 {model} 翻译失败: {e}")
            continue
    return None

def translate_docs_directory():
    # OpenZeppelin文档目录列表 - 包含本地组件和外部仓库
    base_path = Path(__file__).parent.parent  # 获取项目根目录
    doc_directories = [
        # 本地组件
        base_path / "modules/ROOT/",
    ]
    
    for doc_dir in doc_directories:
        docs_path = Path(doc_dir)
        if not docs_path.exists():
            print(f"警告: {doc_dir} 目录不存在，跳过")
            continue
        
        print(f"正在处理目录: {docs_path}")
        
        # 遍历当前目录下的所有.adoc文件
        for file_path in docs_path.rglob("*.adoc"):
            try:
                print(f"正在处理文件: {file_path}")

                # 如果已经有 .bak 的同名文件，跳过翻译
                bak_path = file_path.with_suffix(".adoc.bak")
                print(f"bak_path: {bak_path}")
                if bak_path.exists():
                    print(f"跳过翻译文件: {file_path}，因为存在同名 .bak 文件")
                    continue
                
                # 读取文件内容
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                
                # 翻译内容
                translated_content = translate_markdownx(content)
                
                if translated_content:
                    # 备份原文件
                    backup_path = str(file_path) + ".bak"
                    os.rename(file_path, backup_path)
                    
                    # 写入翻译后的内容
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(translated_content)
                    print(f"成功翻译文件: {file_path}")
                else:
                    print(f"翻译失败: {file_path}")
                    
            except Exception as e:
                print(f"处理文件 {file_path} 时发生错误: {e}")




if __name__ == "__main__":
    translate_docs_directory()


    # with open("../core/getting-started.md", "r", encoding="utf-8") as f:
    #     content = f.read()
    
    # # 翻译内容
    # translated_content = translate_markdownx(content)

    # with open("../core/getting-started_trans.md", "w", encoding="utf-8") as f:
    #     f.write(translated_content)
