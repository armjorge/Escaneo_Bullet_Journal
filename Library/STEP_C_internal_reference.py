import os
import pandas as pd
import ast  # To convert string dictionary back to dictionary

def STEP_C_feed_DF(df_referencia_interna, result_dict):
    # Check if the pickle file exists
    if not os.path.exists(df_referencia_interna):
        print("❌ Archivo no localizado, procedemos a crear uno.")
        df = pd.DataFrame(columns=['filename', 'data_dict'])  # Create DataFrame with required columns
        df.to_pickle(df_referencia_interna)
        print("✅ Archivo pickle creado.")

    # Load the DataFrame
    df = pd.read_pickle(df_referencia_interna)
    print("✅ Archivo con información cargada.")

    # Ensure required columns exist
    required_columns = {'filename', 'data_dict'}
    missing_columns = required_columns - set(df.columns)
    
    if missing_columns:
        print(f"🔹 Columnas faltantes {missing_columns}, agregándolas ahora.")
        for column in missing_columns:
            df[column] = None  # Add missing columns
        df.to_pickle(df_referencia_interna)  # Save updated DataFrame
        print("✅ Columnas agregadas y guardadas.")

    # Iterate over result_dict to update DataFrame
    for filename, data_str in result_dict.items():
        data_dict = ast.literal_eval(data_str)  # Convert string to dictionary
        
        # Check if the file already exists in the DataFrame
        existing_entry = df[df['filename'] == filename]
        
        if not existing_entry.empty:
            print(f"🔹 El archivo '{filename}' ya existe en la base de datos. Se omite.")
            continue
        
        # Append new data
        new_row = pd.DataFrame({'filename': [filename], 'data_dict': [data_dict]})
        df = pd.concat([df, new_row], ignore_index=True)
        print(f"✅ Archivo '{filename}' agregado.")

    # Save the updated DataFrame back to pickle
    df.to_pickle(df_referencia_interna)
    print("✅ Base de datos actualizada y guardada.")
    print(df.head())
    return df