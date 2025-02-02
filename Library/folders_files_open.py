import subprocess
import subprocess
import platform
import glob
import os

def open_pdf(pdf_path):
    """
    Opens the given PDF file in a system-compatible way.
    - Tries to use Adobe Acrobat if available.
    - Otherwise, uses the default PDF viewer.

    Parameters:
        pdf_path (str): The full path to the PDF file.

    Returns:
        None
    """
    if not os.path.exists(pdf_path):
        print(f"❌ Error: El archivo no existe: {pdf_path}")
        return

    system = platform.system()

    try:
        if system == "Windows":
            # Try opening with Acrobat Reader
            acrobat_path = r"C:\Program Files\Adobe\Acrobat DC\Acrobat\Acrobat.exe"
            if os.path.exists(acrobat_path):
                subprocess.run([acrobat_path, pdf_path], check=False)
            else:
                os.startfile(pdf_path)  # Open with default PDF viewer
        elif system == "Darwin":  # macOS
            acrobat_path = "/Applications/Adobe Acrobat DC/Adobe Acrobat.app"
            if os.path.exists(acrobat_path):
                subprocess.run(["open", "-a", acrobat_path, pdf_path], check=False)
            else:
                subprocess.run(["open", pdf_path], check=False)  # Default PDF viewer
        elif system == "Linux":
            subprocess.run(["xdg-open", pdf_path], check=False)

    except Exception as e:
        print(f"⚠️ No se pudo abrir el archivo: {e}")

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