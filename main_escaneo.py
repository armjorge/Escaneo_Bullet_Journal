
import os
import sys
script_directory = os.path.dirname(os.path.abspath(__file__))
function_library = os.path.abspath(os.path.join(script_directory, 'Library'))
sys.path.append(function_library) 
from folders_files_open import open_folder, create_directory_if_not_exists
from user_date_input import get_month_year

def main():
    working_folder = os.path.abspath(os.path.join(script_directory, '..'))    
    PDF_library = os.path.join(working_folder, "PDF_Library")
    create_directory_if_not_exists(PDF_library)
    print("¿El Inserto ya tiene un código en la portada?")
    print("1. Sí, ya tiene")
    print("2. No, es un inserto nuevo")
    print("3. Enlista todos los insertos")

    while True:
        step_0 = input("Seleccione una opción (1/2/3): ")

        if step_0 == "1":
            print("Funcionalidad por desarrollar")
            break

        elif step_0 == "2":
            mes, year = get_month_year()
            print(f"Mes ingresado: {mes}, Año ingresado: {year}")
            insert_label = input("¿Cuál es la Materia o tema del inserto? (sin espacios): ").replace(" ", "")
            insert_label2 = input("¿Cuál es la referencia o número de inserto? (sin espacios): ").replace(" ", "")

            pdf_name = f"{year} - {mes}_{insert_label}_{insert_label2}.pdf"
            pdf_path = os.path.join(PDF_library, pdf_name)

            temp_directory = os.path.join(working_folder, 'Temp')
            create_directory_if_not_exists(temp_directory)
            open_folder(temp_directory)
            input("Pasa el PDF que hayas escaneado a la carpeta que se abrió y presiona enter")

            # Search for a PDF file in the temp directory
            pdf_files = [f for f in os.listdir(temp_directory) if f.endswith('.pdf')]

            if not pdf_files:
                print("No se encontró ningún archivo PDF en la carpeta temporal. Inténtalo de nuevo.")
                continue

            # Assuming there's only one PDF file
            temp_pdf_path = os.path.join(temp_directory, pdf_files[0])
            os.rename(temp_pdf_path, pdf_path)
            os.rmdir(temp_directory)

            print(f"Inserto agregado: {pdf_name}")
            break

        elif step_0 == "3":
            pdf_files = [f for f in os.listdir(PDF_library) if f.endswith('.pdf')]
            if pdf_files:
                print("Insertos disponibles:")
                for pdf in pdf_files:
                    print(f"- {pdf}")
            else:
                print("No hay insertos disponibles en la biblioteca PDF.")
            break

        else:
            print("Opción no válida. Por favor, intente de nuevo.")


if __name__ == "__main__":
    main()
