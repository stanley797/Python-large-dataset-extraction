import csv

# Define the input and output CSV file paths
input_file = 'result.csv'  # Replace with your actual input file path
cleaned_output_file = 'cleaned_result.csv'  # Output file to save the cleaned data
filtered_output_file = 'filtered_result.csv'  # Output file to save filtered rows (where both 'doc_date' and 'doc_content' are 'NA')

# Open the input CSV file and read data
with open(input_file, mode='r', encoding='latin1') as infile:
    reader = csv.DictReader(infile)
    rows = list(reader)

# Step 1: Get the total number of rows in the dataset
total_rows = len(rows)
print(f"Total rows in the dataset: {total_rows}")

# Step 2: Separate rows into two categories:
# - `cleaned_rows`: Rows where not both 'doc_date' and 'doc_content' are 'NA'
# - `filtered_rows`: Rows where both 'doc_date' and 'doc_content' are 'NA'
cleaned_rows = [row for row in rows if not (row['doc_code'] == '' and row['doc_title'] == '')]
filtered_rows = [row for row in rows if row['doc_code'] == '' and row['doc_title'] == '']

# Print statistics
rows_removed = total_rows - len(cleaned_rows)
print(f"Rows removed (both 'doc_code' and 'doc_title' are ''): {rows_removed}")
print(f"Rows where both 'doc_code' and 'doc_title' are '': {len(filtered_rows)}")

# Step 3: Write the cleaned data to one CSV file
if cleaned_rows:
    with open(cleaned_output_file, mode='w', newline='', encoding='latin1') as cleaned_file:
        fieldnames = reader.fieldnames  # Get fieldnames from the input CSV header
        writer = csv.DictWriter(cleaned_file, fieldnames=fieldnames)
        
        writer.writeheader()  # Write the header row
        writer.writerows(cleaned_rows)  # Write the cleaned rows

    print(f"Cleaned data saved to {cleaned_output_file}")
else:
    print("No cleaned data left to save.")

# Step 4: Write the filtered rows to another CSV file
if filtered_rows:
    with open(filtered_output_file, mode='w', newline='', encoding='latin1') as filtered_file:
        fieldnames = reader.fieldnames  # Get fieldnames from the input CSV header
        writer = csv.DictWriter(filtered_file, fieldnames=fieldnames)
        
        writer.writeheader()  # Write the header row
        writer.writerows(filtered_rows)  # Write the filtered rows

    print(f"Filtered data saved to {filtered_output_file}")
else:
    print("No rows matching the criteria were found.")
