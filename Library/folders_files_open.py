import subprocess
import os

def open_folder(os_path):
    """Opens a folder in the appropriate file explorer depending on the OS."""
    try:
        if os.name == 'nt':  # Windows
            os.startfile(os_path)
        elif os.name == 'posix':  # macOS or Linux
            if "darwin" in os.uname().sysname.lower():  # macOS
                subprocess.run(["open", os_path])
            else:  # Linux
                subprocess.run(["xdg-open", os_path])
        else:
            print(f"Unsupported OS: {os.name}")
    except Exception as e:
        print(f"Error opening folder: {e}")

def create_directory_if_not_exists(path):
    """Creates a directory if it does not exist."""
    if not os.path.exists(path):
        os.makedirs(path)
        
def create_directory_if_not_exists(path):
    """Creates a directory if it does not exist."""
    if not os.path.exists(path):
        os.makedirs(path)