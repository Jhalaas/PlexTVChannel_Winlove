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


def schedule_tasks():
    """Create Windows Task Scheduler entries for automation scripts."""
    repo_dir = os.path.dirname(os.path.abspath(__file__))
    start_ps1 = os.path.join(repo_dir, 'tvStart.ps1')
    continue_ps1 = os.path.join(repo_dir, 'tvContinue.ps1')

    # Schedule tvStart.ps1 to run at logon
    subprocess.call([
        'schtasks', '/Create', '/TN', 'PlexTV_Start',
        '/TR', f'powershell.exe -ExecutionPolicy Bypass -File "{start_ps1}"',
        '/SC', 'ONLOGON', '/RL', 'HIGHEST', '/F'
    ])

    # Schedule tvContinue.ps1 to run every 15 minutes
    subprocess.call([
        'schtasks', '/Create', '/TN', 'PlexTV_Continue',
        '/TR', f'powershell.exe -ExecutionPolicy Bypass -File "{continue_ps1}"',
        '/SC', 'MINUTE', '/MO', '15', '/RL', 'HIGHEST', '/F'
    ])


if __name__ == '__main__':
    install_requirements()
    create_shortcut()
    schedule_tasks()
    print('Setup complete. Automation tasks have been scheduled.')
