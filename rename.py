import os

def rename_files(directory):
    for root, dirs, files in os.walk(directory):
        for file_name in files:
            if file_name == "django.po":
                old_path = os.path.join(root, file_name)
                new_path = os.path.join(root, "ginger.po")
                os.rename(old_path, new_path)
                print(f"Renamed {old_path} to {new_path}")
            elif file_name == "django.mo":
                old_path = os.path.join(root, file_name)
                new_path = os.path.join(root, "ginger.mo")
                os.rename(old_path, new_path)
                print(f"Renamed {old_path} to {new_path}")

        for dir_name in dirs:
            rename_files(os.path.join(root, dir_name))

# Start renaming from the current directory and its subdirectories
current_directory = os.getcwd()
rename_files(current_directory)
