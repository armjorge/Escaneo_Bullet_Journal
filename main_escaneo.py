import os
import sys
script_directory = os.path.dirname(os.path.abspath(__file__))
function_library = os.path.abspath(os.path.join(script_directory, 'Library'))
sys.path.append(function_library) 
from folders_files_open import open_folder, create_directory_if_not_exists
from STEP_A_Dict import STEP_A_get_string_populated, STEP_A_4_validdict
from STEP_B_PDFhandling import STEP_B_PDF_HANDLING

def main():
    working_folder = os.path.abspath(os.path.join(script_directory, '..'))    
    PDF_library = os.path.join(working_folder, "PDF_Library")
    df_path = os.path.join(working_folder, "input_fields.pickle")
    temp_directory = os.path.join(working_folder, 'Temp')    
    create_directory_if_not_exists(PDF_library)
    print("¿El Inserto ya tiene un código en la portada?")
    print("1. Sí, ya tiene")
    print("2. No, es un inserto nuevo")
    print("3. Enlista todos los insertos")
    while True:
        step_0 = input("Seleccione una opción (1/2/3): ")
        if step_0 == "1":
            print("Sí, ya tiene un código en la portada")
            break
        elif step_0 == "2":
            print("\n\tPASO A: GENERAR DE DICCIONARIO PARA ESCANEO NUEVO\n")
            dicct_book = STEP_A_get_string_populated(df_path)
            print()
            computer_dict = STEP_A_4_validdict(dicct_book)
            print('Diccionario Capturado\n', dicct_book, "\nDiccionario Procesado\n", computer_dict)
            print("\n\tPASO B: MANEJAR EL PDF\n")            
            STEP_B_PDF_HANDLING(temp_directory, computer_dict)
            print(f"Inserto agregado: ")
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
