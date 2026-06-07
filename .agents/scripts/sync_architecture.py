import os

AGENTS_DIR = '.agents'
OUTPUT_FILE = os.path.join(AGENTS_DIR, 'ARCHITECTURE.md')

def get_metadata(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            content = f.read()
        # Busca simples por linha que começa com name: ou description:
        name = None
        description = None
        for line in content.split('\n'):
            line = line.strip().lower()
            if line.startswith('name:'):
                name = line.replace('name:', '').strip().strip('"').strip("'")
            if line.startswith('description:'):
                description = line.replace('description:', '').strip().strip('"').strip("'")
            if name and description:
                break
        return name, description
    except:
        return None, None

def update_arch():
    md = "# 🗺️ Mapa Arquitetural JINC Skills\n\n"
    for folder in ['agents', 'skills', 'workflows', 'rules']:
        md += f"## 📂 `{folder}/`\n\n"
        path = os.path.join(AGENTS_DIR, folder)
        if not os.path.exists(path): continue
        
        for root, _, files in os.walk(path):
            for file in sorted(files):
                if file.endswith('.md'):
                    n, d = get_metadata(os.path.join(root, file))
                    if n and d:
                        md += f"- **`{n}`** (`{file}`): {d}\n"
                    else:
                        md += f"- `{file}`: _(Aguardando conformidade SDD)_\n"
        md += "\n"
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(md)

if __name__ == "__main__":
    update_arch()
    print("✅ ARCHITECTURE.md atualizado.")
