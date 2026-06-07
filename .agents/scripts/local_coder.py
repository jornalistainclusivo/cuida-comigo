import sys
import json
import urllib.request
import argparse

def ask_local_ai(prompt, model="deepseek-r1"):
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }
    
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result['response']
    except Exception as e:
        return f"Erro ao conectar com o Ollama: {e}"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="JINC Local Vibe Coding via Ollama")
    parser.add_argument("file", help="O arquivo que você quer que a IA leia")
    parser.add_argument("instruction", help="O que a IA deve fazer com o código")
    parser.add_argument("--model", default="deepseek-r1", help="Modelo a utilizar (ex: llama3, phi3, gemma)")
    
    args = parser.parse_args()
    
    try:
        with open(args.file, 'r', encoding='utf-8') as f:
            code_context = f.read()
            
        full_prompt = f"Aqui está o código do arquivo {args.file}:\n\n
http://googleusercontent.com/immersive_entry_chip/0

