import calendar
import pandas as pd
import os
import ast
import re


def STEP_A_get_string_populated(df_to_load): 
    print("🛠️ Iniciando la generación del diccionario para el inserto...\n")

    # Mostrar estructura esperada antes de poblar con datos
    expected_structure = """
    📌 Estructura esperada del diccionario:
    {
        'Primer registro': 'dd/mm/yyyy',  # Fecha en formato Año-Mes
        'Materia': 'NombreMateria',    # Extraído del DataFrame
        'Tipo': 'CategoríaTipo',       # Extraído del DataFrame
        'Nota': 'Texto corto'          # Ingresado manualmente
    }
    """
    print(expected_structure)

    # Crear el diccionario poblado
    Output_dict = f"""
    {{
        'Primer registro': '{STEP_A_1_GetDate()}',
        'Proyecto': '{STEP_A_2_df_fields(df_to_load, 'Proyecto')}',
        'Materia': '{STEP_A_2_df_fields(df_to_load, 'Materia')}',
        'Nota': '{STEP_A_3_GetNote(15)}'
    }}
    """

    # Mostrar valores antes de devolver el diccionario
    print("\n🔹 Diccionario generado con valores actuales:")
    print(Output_dict)

    return Output_dict

def STEP_A_1_GetDate():
    input_day = "¿Cuál es día del primer registro? (2 dígitos)?: "            
    input_mes = "¿Cuál es mes del primer registro? (2 dígitos)?: "            
    input_year = "¿Cuál es el año del primer registro (4 dígitos)?: "
    mm_dd_digitos = 2
    mes_enero = 1
    mes_diciembre = 12
    year_digits = 4
    year_min = 1900
    year_max = 2060
    def get_specific_digits_as_string(prompt, needed_digits, min_input, max_input):
        """
        Prompts the user for input and validates it using specific conditions:
        - Input must be numeric.
        - Input must have the specified number of digits.
        - Input must fall within the specified range.
        """
        while True:
            user_input = input(prompt)
            error_message = "Vuelve a intentar"
            if user_input.isdigit() and len(user_input) == needed_digits and min_input <= int(user_input) <= max_input:
                return user_input
            print(f"{error_message}, necesitas meter un número de mín de {min_input} y máx {max_input} caracteres")    
    mes = get_specific_digits_as_string(input_mes, mm_dd_digitos, mes_enero, mes_diciembre)
    year = get_specific_digits_as_string(input_year, year_digits, year_min, year_max)
    day_min = 1
    # Función para obtener los días máximos de ese mes. 
    def get_month_days(year, month):
        """
        Returns the maximum number of days in a given month for a specific year.
        
        Parameters:
            year (str or int): The year in 4-digit format.
            month (str): The month in 2-digit string format.

        Returns:
            int: Maximum number of days in the specified month.
        """

        # Convert inputs to integers
        year = int(year)
        month = int(month)

        # Get the last day of the month
        day_max = calendar.monthrange(year, month)[1]

        return day_max
    day_max = get_month_days(year,mes)
    day = get_specific_digits_as_string(input_day, mm_dd_digitos, day_min, day_max)            
    date = f"{day}/{mes}/{year}"
    return date

def STEP_A_2_df_fields(df_to_load, column):
    """
    Handles loading a DataFrame from a pickle file, ensuring the specified column exists.
    Allows the user to input or select values.
    
    Parameters:
        df_to_load (str): Path to the pickle file.
        column (str): Column name to retrieve data from.
    
    Returns:
        Selected value from the column.
    """

    # Check if the pickle file exists
    if not os.path.exists(df_to_load):
        print("❌ Archivo no localizado, procedemos a crear uno.")
        df = pd.DataFrame()  # Create an empty DataFrame
        df.to_pickle(df_to_load)
        print("✅ Archivo pickle creado.")

    # Load the DataFrame
    df = pd.read_pickle(df_to_load)
    print("✅ Archivo con información cargada.")

    # Ensure the column exists in the DataFrame
    if column not in df.columns:
        print(f"🔹 Columna '{column}' no encontrada. Se generará una nueva columna.")
        df[column] = pd.Series(dtype="object")  # Add an empty column
        df.to_pickle(df_to_load)  # Save updated DataFrame
        print(f"✅ Nueva columna '{column}' creada y guardada.")

    # Check if there are any values in the column
    if len(df[column].dropna()) > 0:
        print("✅ Se encontró al menos un registro:")
        unique_values = df[column].dropna().unique()
        for idx, value in enumerate(unique_values):
            print(f"\t{idx}) {value}")
    else:
        print(f"❌ No se encontraron registros en la columna {column}.")

    # Main loop for user input
    while True:
        print("\n📌 Opciones:")
        print(f"\t1) Agregar más valores o actualizar en la columna {column}")
        print(f"\t2) Seleccionar un valor existente en la columna {column}")
        
        try:
            choice = int(input("Selecciona una opción (1/2): "))
        except ValueError:
            print("⚠️ Entrada no válida. Ingresa 1 o 2.")
            continue

        if choice == 1:
            # Save the column to a CSV for user input
            csv_path = os.path.join(os.path.dirname(df_to_load), f"{column}.csv")
            df[[column]].to_csv(csv_path, index=False)
            print(f"📂 Se generó el archivo: {csv_path}")
            print("📂 Búscalo en tu CODE o desarrolla código para abrirlo en cualquier sistema")
            input("📝 Agrega nuevos valores en el archivo CSV y presiona ENTER cuando termines...")

            # Reload the updated CSV
            updated_df = pd.read_csv(csv_path)

            df[column] = updated_df[column]  # Replace column data
            df.to_pickle(df_to_load)  # Save changes
            print("✅ DataFrame maestro actualizado con estos datos: ")
            print("\n🔹 Valores disponibles:")
            unique_values = df[column].dropna().unique()
            for idx, value in enumerate(unique_values):
                print(f"\t{idx}) {value}")
            os.remove(csv_path)
            print("✅ CSV de la captura eliminado")
                            
        elif choice == 2:
            # Let the user choose a value from the list
            unique_values = df[column].dropna().unique()
            if len(unique_values) == 0:
                print("⚠️ No hay valores disponibles para seleccionar.")
                continue
            
            print("\n🔹 Valores disponibles:")
            for idx, value in enumerate(unique_values):
                print(f"\t{idx}) {value}")

            try:
                index = int(input("🔹 Dame el índice del valor: "))
                if index in range(len(unique_values)):
                    return unique_values[index]
                else:
                    print("⚠️ Índice fuera de rango.")
            except ValueError:
                print("⚠️ Entrada no válida. Ingresa un número válido.")

        else:
            print("⚠️ Opción no válida. Intenta de nuevo.")

def STEP_A_3_GetNote(words): 
    """
    Prompts the user to enter a message with a word limit.

    Parameters:
        words (int): Maximum number of words allowed in the input.

    Returns:
        str: User's input message within the word limit.
    """

    words = int(words)  # Ensure the input is treated as an integer

    while True:
        note = input(f"📝 Por favor, escriba hasta {words} palabras: ")
        
        # Count words in the input
        word_count = len(note.split())

        if word_count <= words:
            return note  # Valid input, return message
        else:
            print(f"⚠️ Demasiadas palabras ({word_count}/{words}). Intenta de nuevo.")

def STEP_A_4_validdict(dicct_book):
    try:
        # Step 1: Trim leading/trailing spaces
        dicct_book = dicct_book.strip()

        # Step 2: Fix common syntax issues
        dicct_book = dicct_book.replace("‘", "'").replace("’", "'")  # Smart quotes to normal quotes
        dicct_book = dicct_book.replace("“", '"').replace("”", '"')  # Smart double quotes fix
        
        # Step 3: Count brackets
        open_brackets = dicct_book.count('{')
        close_brackets = dicct_book.count('}')
        
        if open_brackets != close_brackets:
            print(f"⚠️ Desajuste en corchetes: {open_brackets} abiertos, {close_brackets} cerrados.")
            return None

        # Step 4: Try parsing the string into a dictionary
        cleaned_dict = ast.literal_eval(dicct_book)

        if not isinstance(cleaned_dict, dict):
            raise ValueError("⚠️ Error: La estructura no es un diccionario válido.")

        print("✅ Diccionario validado y corregido correctamente.")
        return cleaned_dict

    except (SyntaxError, ValueError) as e:
        print(f"❌ Error al analizar el diccionario: {e}")
        print("⚠️ Revisa los corchetes, comillas y la estructura del diccionario.")
        
        # Suggest a manual fix
        print("\n🔹 Sugerencia: Asegúrate de que el diccionario esté bien formateado:")
        print("{ 'Clave': 'Valor', 'Otra Clave': 'Otro Valor' }")
        return None    