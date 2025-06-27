# from django.db import models
# from django.contrib.auth.models import AbstractUser
# from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
# from django.utils import timezone
# from django.core.exceptions import ValidationError
import os
import ast

def find_models_in_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read(), filename=file_path)
    
    models = []
    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            for base in node.bases:
                if isinstance(base, ast.Attribute) and base.attr == 'Model':
                    models.append(node.name)
                elif isinstance(base, ast.Name) and base.id == 'Model':
                    models.append(node.name)
    return models

def convert_to_module_path(file_path, root_dir):
    rel_path = os.path.relpath(file_path, root_dir)
    module_path = rel_path.replace(os.sep, ".").replace(".py", "")
    return module_path

def main(root_dir="."):
    imports = []

    for dirpath, dirnames, filenames in os.walk(root_dir):
        if 'migrations' in dirnames:
            dirnames.remove('migrations')  # skip migrations folders
        if 'tests' in dirnames:
            dirnames.remove('tests')       # skip tests folders
        for filename in filenames:
            if filename == "models.py":
                full_path = os.path.join(dirpath, filename)
                model_names = find_models_in_file(full_path)
                if model_names:
                    module_path = convert_to_module_path(full_path, root_dir)
                    line = f"from {module_path} import {', '.join(model_names)}"
                    imports.append(line)
    
    # اطبع أو خزّن النتيجة
    print("# === Generated imports ===")
    for imp in imports:
        print(imp)

if __name__ == "__main__":
    main()
