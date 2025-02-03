import os
import segno
import re
from PIL import Image, ImageDraw, ImageFont

def STEP_D_CODE(result_dict, QR_library):
    """
    Generates Aztec barcodes with the text displayed below for readability.

    Args:
        result_dict (dict): Dictionary where keys are filenames and values are metadata strings.
        QR_library (str): Path to the folder where Aztec codes will be saved.
    """
    # Ensure directory exists
    os.makedirs(QR_library, exist_ok=True)

    for key, value in result_dict.items():
        # 🛠 1️⃣ Clean the text for readability
        cleaned_value = re.sub(r"[{}]", "", value)  # Remove curly brackets
        cleaned_value = re.sub(r"\s+", " ", cleaned_value)  # Remove extra spaces/newlines
        cleaned_value = cleaned_value.replace(":", " -")  # Replace colons with a readable separator
        cleaned_value = cleaned_value.replace(",", " |")  # Use "|" instead of commas for better readability
        
        # 🛠 2️⃣ Format the final text
        text = f"Archivo: {key} | Detalles: {cleaned_value}"  
        print(f"Encoding: {text}")  # Debug output

        # 🛠 3️⃣ Generate Aztec Code
        aztec = segno.make(text, error="H")
        barcode_filename = os.path.splitext(key)[0].replace(" ", "_")
        barcode_filepath = os.path.join(QR_library, f"{barcode_filename}.png")
        aztec.save(barcode_filepath, scale=10)  # Save barcode

        # 🛠 4️⃣ Load the barcode image
        aztec_img = Image.open(barcode_filepath)

        # 🛠 5️⃣ Create a new image with space for text
        width, height = aztec_img.size
        text_height = 100  # Space for text
        new_img = Image.new("RGB", (width, height + text_height), "white")

        # 🛠 6️⃣ Paste the Aztec barcode onto the new image
        new_img.paste(aztec_img, (0, 0))

        # 🛠 7️⃣ Add text below the barcode
        draw = ImageDraw.Draw(new_img)
        try:
            font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 25)
        except:
            font = ImageFont.load_default()  # Use default font if Arial not found

        # Wrap text for better display
        max_width = width - 10  # Keep some margin
        lines = []
        words = text.split(" ")
        current_line = ""
        
        for word in words:
            test_line = f"{current_line} {word}".strip()
            text_width = draw.textbbox((0, 0), test_line, font=font)[2]  # ✅ FIXED: Use textbbox()
            
            if text_width < max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word
        lines.append(current_line)

        y_position = height + 5  # Start text below barcode
        for line in lines:
            draw.text((10, y_position), line, fill="black", font=font)
            y_position += 30  # Line spacing

        # 🛠 8️⃣ Save final image
        final_filepath = os.path.join(QR_library, f"{barcode_filename}_with_text.png")
        new_img.save(final_filepath)
        print(f"Aztec code with text saved: {final_filepath}")
