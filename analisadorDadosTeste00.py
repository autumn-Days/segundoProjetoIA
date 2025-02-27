import os
import re

# Define directories
input_dir = "resultadosTeste00_1"  # Folder containing input files
output_dir = "analiseResultadosTeste00_1"  # Folder to store results
output_file = os.path.join(output_dir, "summary00_1.txt")

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

# Pattern to extract 'aptidão best' values
pattern = re.compile(r"aptidão best: •(\d+)")

# Open output file
with open(output_file, "w", encoding="utf-8") as out:
    for filename in os.listdir(input_dir):
        file_path = os.path.join(input_dir, filename)
        
        if not os.path.isfile(file_path):
            continue  # Skip directories
        
        first_value, last_value = None, None
        
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                match = pattern.search(line)
                if match:
                    value = int(match.group(1))
                    if first_value is None:
                        first_value = value
                    last_value = value  # Keep updating until the last match
        
        if first_value is not None and last_value is not None:
            difference = first_value - last_value
            out.write(f"-=-==-=-=\n")
            out.write(f"COMBINAÇÃO: {filename}\n")
            out.write(f"Melhor aptidão 1° gen: {first_value}\n")
            out.write(f"Melhor aptidão última gen: {last_value}\n")
            out.write(f"Diferença de aptidões gen: {difference}\n")
            out.write(f"-=-==-=-=\n\n")
