import os
import pandas as pd
from bs4 import BeautifulSoup
import re

# Initialize a list to store extracted data
data = []

# Process HTML files
folder_path = "4"
for filename in os.listdir(folder_path):
    if filename.endswith(".html") or filename.endswith(".htm"):
        file_path = os.path.join(folder_path, filename)
        with open(file_path, "r", encoding="utf-8") as file:
            soup = BeautifulSoup(file.read(), "html.parser")
       
            input_elements = soup.find_all('input', {'type': 'hidden'})
            id_values = [
                elem.get('value') for elem in input_elements
                if elem.get('id') and elem.get('id').startswith('in_')
            ]
            extracted_ids = []
            for id_value in id_values:
                extracted_ids.append(id_value.split("=")[1])

            extracted_dirs = []

            # Extract the report title based on identifiable attributes
            title_elements = soup.find_all('a', title="Click para ver as Informações")

            for title_element in title_elements:
                content = title_element.get_text(strip=True).split('-')[0]
                if len(content) < 45:
                    extracted_dirs.append(content)
            # for title_element in title_elements:
            #     extracted_dirs.append(title_element.text.strip())

            # Extract links
            for id, Dir in zip(extracted_ids, extracted_dirs):
                data.append({"Page number": filename, "ID": id, "Dir": Dir, "niv": "4"})
# Save to CSV using pandas
df = pd.DataFrame(data)
df.to_csv("predata.csv", index=False, encoding="utf-8")
print("Data saved to extracted_data.csv")