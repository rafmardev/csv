import csv
from pathlib import Path

def process_csv(input_filename: str):    
    output_dir = Path("results")
    output_dir.mkdir(exist_ok=True)

    insurance_data = {}

    with open(input_filename, 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        for row in reader:
            row['Version'] = int(row['Version'])
            key = (row['Insurance Company'], row['User Id'])

            if (existing := insurance_data.get(key)) is None or row['Version'] > existing['Version']:
                insurance_data[key] = row

    sorted_records = sorted(insurance_data.values(), key=lambda x: (x['Insurance Company'], x['Last Name'], x['First Name']))
    file_writers = {}

    for row in sorted_records:
        company = row['Insurance Company']
        if company not in file_writers:
            file_path = output_dir / f"{company.replace(' ', '_')}_enrollees.csv"
            file_writers[company] = open(file_path, 'w', newline='', encoding='utf-8')
            writer = csv.DictWriter(file_writers[company], fieldnames=row.keys())
            writer.writeheader()
            file_writers[company].writer = writer

        file_writers[company].writer.writerow(row)

    for file in file_writers.values():
        file.close()

    print("Proceso terminado")

input_filename = 'enrollees.csv'
process_csv(input_filename)
