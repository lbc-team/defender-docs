import os
from dotenv import load_dotenv

load_dotenv(".env")


OPENROUTER_PREFIX = "openrouter:"

MODEL_GEMINI_20_FLASH = "google/gemini-2.0-flash-001"
OPENROUTER_MODEL_GEMINI_20_FLASH = OPENROUTER_PREFIX +  MODEL_GEMINI_20_FLASH

LLM_MODEL_GPT_4O_MINI = "gpt-4o-mini-2024-07-18"
LLM_MODEL_DEEPSEEK_R1 = "deepseek-r1"
LLM_MODEL_DEEPSEEK_V3 = "deepseek-v3"

MAX_TOKENS = 8000  


