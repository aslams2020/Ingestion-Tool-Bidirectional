import pandas as pd
import os

def process_flat_file(file):
    os.makedirs('data/uploads', exist_ok=True)
    filepath = os.path.join('data/uploads', file.filename)
    file.save(filepath)
    return filepath

def get_csv_columns(filepath, delimiter=','):
    return pd.read_csv(filepath, delimiter=delimiter, nrows=0).columns.tolist()

def generate_csv(data, columns, output_name='output.csv'):
    os.makedirs('data/outputs', exist_ok=True)
    output_path = os.path.join('data/outputs', output_name)
    pd.DataFrame(data, columns=columns).to_csv(output_path, index=False)
    return output_path