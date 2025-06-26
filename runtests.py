import os

def rename_test_files(base_dir):
    for root, dirs, files in os.walk(base_dir):
        if os.path.basename(root) == "tests":
            app_name = os.path.basename(os.path.dirname(root))

            for filename in files:
                if filename in ("test_models.py", "test_views.py"):
                    file_type = filename.replace("test_", "").replace(".py", "")
                    new_name = f"test_{app_name}_{file_type}.py"

                    old_path = os.path.join(root, filename)
                    new_path = os.path.join(root, new_name)

                    # Rename file
