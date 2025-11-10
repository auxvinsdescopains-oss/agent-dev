import openai
import os
from agent.utils import backup_file

openai.api_key = os.getenv('OPENAI_API_KEY')

def process_task(file_path, task):
    backup_file(file_path)
    with open(file_path, 'r', encoding='utf-8') as f:
        code = f.read()

    prompt = f"Task: {task}\nOriginal Code:\n{code}\nOptimized Version:"
    
    response = openai.ChatCompletion.create(
        model="gpt-5-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    optimized_code = response['choices'][0]['message']['content']

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(optimized_code)

    return optimized_code
