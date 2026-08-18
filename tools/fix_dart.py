import os
import re

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content = content
    # Remove 'const Text(L10n.t' -> 'Text(L10n.t'
    new_content = new_content.replace('const Text(L10n.t', 'Text(L10n.t')
    
    # Add import if missing
    if 'L10n.t' in new_content and 'l10n.dart' not in new_content:
        import_stmt = "import '../utils/l10n.dart';\n"
        if filepath.startswith('lib\\screens\\') or filepath.startswith('lib/screens/'):
            pass
        elif filepath.startswith('lib\\widgets\\') or filepath.startswith('lib/widgets/'):
            pass
        else:
            import_stmt = "import 'utils/l10n.dart';\n"
        
        # Add after last import or at top
        imports = re.findall(r"^import\s+['\"].*?['\"];\s*", new_content, re.MULTILINE)
        if imports:
            last_import = imports[-1]
            new_content = new_content.replace(last_import, last_import + import_stmt)
        else:
            new_content = import_stmt + new_content
            
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Fixed {filepath}")

for root, dirs, files in os.walk('lib'):
    for file in files:
        if file.endswith('.dart'):
            process_file(os.path.join(root, file))

