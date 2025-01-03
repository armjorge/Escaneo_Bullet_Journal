import os

def create_directory_if_not_exists(path):
    """Creates a directory if it does not exist."""
    if not os.path.exists(path):
        os.makedirs(path)

def get_validated_input(prompt, validation_fn, error_message):
    """Prompts the user for input and validates it using a provided function."""
    while True:
        user_input = input(prompt)
        if validation_fn(user_input):
            return user_input
        print(error_message)

def main():
    folder_path = 'G:\\My Drive\\Projects\\Escaneo Insertos'
    PDF_library = os.path.join(folder_path, "PDF_Library")
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
            # Validating year
            insert_ano = get_validated_input(
                "¿Cuál es año del primer registro? (4 dígitos): ",
                lambda x: x.isdigit() and len(x) == 4,
                "Por favor, ingrese un año válido de 4 dígitos."
            )

            # Validating month
            insert_mes = get_validated_input(
                "¿Cuál es mes del primer registro? (2 dígitos): ",
                lambda x: x.isdigit() and len(x) == 2 and 1 <= int(x) <= 12,
                "Por favor, ingrese un mes válido entre 01 y 12."
            )

            insert_label = input("¿Cuál es la Materia o tema del inserto? (sin espacios): ").replace(" ", "")
            insert_label2 = input("¿Cuál es la referencia o número de inserto? (sin espacios): ").replace(" ", "")

            pdf_name = f"{insert_ano}{insert_mes}_{insert_label}_{insert_label2}.pdf"
            pdf_path = os.path.join(PDF_library, pdf_name)

            temp_directory = os.path.join(folder_path, 'Temp')
            create_directory_if_not_exists(temp_directory)

            os.startfile(temp_directory)  # Open the temp directory
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
