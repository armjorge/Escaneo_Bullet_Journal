def get_month_year():
    input_mes = "¿Cuál es mes del primer registro? (2 dígitos)?: "            
    mm_dd_digitos = 2
    mes_enero = 1
    mes_diciembre = 12
    input_year = "¿Cuál es el año del primer registro (4 dígitos)?: "
    year_digits = 4
    year_min = 1900
    year_max = 2060            
    mes = get_specific_digits_as_string(input_mes, mm_dd_digitos, mes_enero, mes_diciembre)
    year = get_specific_digits_as_string(input_year, year_digits, year_min, year_max)
    
    return mes, year

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
 