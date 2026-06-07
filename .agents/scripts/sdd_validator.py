import os
import re
import sys
import yaml

# Constantes de Cores e Configurações (Mantidas do contexto original)
class Colors:
    HEADER, GREEN, RED, ENDC = '\033[95m', '\033[92m', '\033[91m', '\033[0m'

EXEMPT_FILES = ['readme.md', 'architecture.md', 'changelog.md']

def validate_sdd_contract(filepath: str) -> bool:
    if not os.path.exists(filepath):
        return False

    filename = os.path.basename(filepath).lower()
    # Bypass para regras core e arquivos isentos
    if filename in EXEMPT_FILES or '/.agents/rules/' in filepath.replace('\\', '/').lower():
        print(f"{Colors.HEADER}⏭️ Isento: {filename}{Colors.ENDC}")
        return True

    try:
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            content = f.read()

        # Extração Robusta: Captura o bloco YAML ignorando espaços iniciais
        yaml_match = re.search(r'^\s*---\s*\n(.*?)\n---\s*\n', content, re.S | re.M)
        
        meta = {}
        if yaml_match:
            try:
                meta = yaml.safe_load(yaml_match.group(1)) or {}
            except yaml.YAMLError:
                meta = {} # Fallback para busca literal se o YAML for inválido

        # Validação de chaves (Prioridade Semântica)
        has_name = isinstance(meta, dict) and 'name' in meta
        has_desc = isinstance(meta, dict) and 'description' in meta

        # Fallback de Compatibilidade (Busca literal nos primeiros 1000 chars)
        if not (has_name and has_desc):
            header_sample = content[:1000].lower()
            has_name = has_name or ('name:' in header_sample)
            has_desc = has_desc or ('description:' in header_sample)

        if has_name and has_desc:
            print(f"{Colors.GREEN}✅ Validado: {filename}{Colors.ENDC}")
            return True
        else:
            # Feedback detalhado para o log do GitHub Actions
            found_keys = list(meta.keys()) if isinstance(meta, dict) else "Formato Inválido"
            print(f"{Colors.RED}❌ Falha em {filename}: Chaves incompletas. Detectado: {found_keys}{Colors.ENDC}")
            return False

    except Exception as e:
        print(f"{Colors.RED}❌ Erro crítico em {filename}: {str(e)}{Colors.ENDC}")
        return False

if __name__ == "__main__":
    files = sys.argv[1:]
    if not files:
        sys.exit(0)
    success = all(validate_sdd_contract(f) for f in files)
    sys.exit(0 if success else 1)
