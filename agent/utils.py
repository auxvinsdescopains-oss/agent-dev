import shutil
import os

def backup_file(file_path):
    backup_dir = 'backups'
    os.makedirs(backup_dir, exist_ok=True)
    shutil.copy(file_path, os.path.join(backup_dir, os.path.basename(file_path)))
