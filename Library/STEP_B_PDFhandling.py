
from folders_files_open import open_folder, create_directory_if_not_exists, open_pdf

import os
import glob
import time

def STEP_B_PDF_HANDLING(temp_path, valid_dict):
    """
    Handles PDF loading, renaming, and opening based on extracted data.
    
    Parameters:
        temp_path (str): The path where the temporary PDF is stored.
        valid_dict (dict): Dictionary containing metadata fields for naming.

    Returns:
        None
    """
    print("\n📄 Con los datos extraídos, es momento de pasar a cargar el PDF\n")

    # Ensure the temp directory exists
    create_directory_if_not_exists(temp_path)
    open_folder(temp_path)  # Opens the temp directory for user review

    while True:
        # List PDF files in the directory
        pdf_files = [f for f in os.listdir(temp_path) if f.endswith('.pdf')]

        if len(pdf_files) == 1:
            break  # Continue processing if exactly one PDF is found

        elif len(pdf_files) > 1:
            print("⚠️ Se detectaron múltiples archivos PDF en la carpeta temporal:")
            for file in pdf_files:
                print(f"   - {file}")

            input("🗑️ Elimina los archivos extra y deja solo uno. Luego presiona ENTER para continuar...")
            continue  # Restart the loop after cleaning

        elif not pdf_files:
            print("❌ No se encontró ningún archivo PDF en la carpeta temporal.")
            input("📂 Agrega un archivo PDF en la carpeta y presiona ENTER para continuar...")
            continue  # Restart the loop

    # Build the filename using dictionary values
    pdf_name = f"{valid_dict.get('Proyecto')}_ejemplo.pdf"

    # Locate the first (and now only) PDF
    temp_pdf_path = os.path.join(temp_path, pdf_files[0])
    pdf_path = os.path.join(temp_path, pdf_name)

    # Rename the file
    try:
        os.rename(temp_pdf_path, pdf_path)
        print(f"✅ Archivo renombrado a: {pdf_path}")
    except Exception as e:
        print(f"❌ Error al renombrar el archivo: {e}")
        return

    # Open the renamed PDF
    open_pdf(pdf_path)