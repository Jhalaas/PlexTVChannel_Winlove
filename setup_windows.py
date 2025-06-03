import os
import sys
import subprocess
import shutil


def install_requirements():
    req_file = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    if os.path.exists(req_file):
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', req_file])
    else:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'moviepy', 'tvdb_api'])


def create_shortcut():
    repo_dir = os.path.dirname(os.path.abspath(__file__))
    batch_path = os.path.join(repo_dir, 'run_gui.bat')
    with open(batch_path, 'w') as f:
        f.write(f"@echo off\ncd /d \"{repo_dir}\"\npython gui.py\n")

    desktop = os.path.join(os.environ.get('USERPROFILE', ''), 'Desktop')
    if os.path.isdir(desktop):
        shutil.copy(batch_path, os.path.join(desktop, 'PlexTVChannel_GUI.bat'))
        print('Desktop shortcut created.')
    else:
        print('Could not locate Desktop path. Shortcut not created.')


if __name__ == '__main__':
    install_requirements()
    create_shortcut()
    print('Setup complete. Use the desktop shortcut to launch the GUI.')
