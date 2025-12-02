# verify_imports.py
import ast
import os

def check_imports_in_file(filepath):
    """Check if file contains required imports"""
    with open(filepath, 'r') as file:
        content = file.read()
        tree = ast.parse(content)
        
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ''
                for alias in node.names:
                    imports.append(f"{module}.{alias.name}")
        
        return imports

# Check views.py
views_path = os.path.join('api', 'views.py')
imports = check_imports_in_file(views_path)

print("Checking imports in api/views.py:")
print("=" * 50)

required_imports = [
    'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    'rest_framework.permissions.IsAuthenticated'
]

for req in required_imports:
    found = any(req in imp for imp in imports)
    status = "✓ FOUND" if found else "✗ MISSING"
    print(f"{status}: {req}")

print("\nAll imports in file:")
for imp in imports:
    print(f"  - {imp}")