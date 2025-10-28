import csv
import json
import os


def read_csv_file(filename: str) -> list:
    """
    Read data from a CSV file and convert it to a list of dictionaries.

    Args:
        filename (str): Path to the CSV file to read

    Returns:
        list: List of dictionaries where keys are column headers and values
              are row data
    """
    with open(filename, 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        headers = next(csv_reader)
        data = []

        for row in csv_reader:
            row_dict = {}
            for i, header in enumerate(headers):
                clean_header = header.strip()
                clean_value = row[i].strip()
                row_dict[clean_header] = clean_value
            data.append(row_dict)

    return data


def read_json_file(filename: str) -> list:
    """
    Read data from a JSON file and parse it as a list.

    Args:
        filename (str): Path to the JSON file to read

    Returns:
        list: Parsed JSON data as a Python list
    """
    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data


def import_financial_data(filename: str) -> list:
    """
    Import financial data from either CSV or JSON file based on file extension.

    Args:
        filename (str): Path to the financial data file (CSV or JSON)

    Returns:
        list: Financial data as a list of transactions
    """
    ext = os.path.splitext(filename)[1].lower()

    if ext == '.csv':
        return read_csv_file(filename)
    elif ext == '.json':
        return read_json_file(filename)
    else:
        raise ValueError(f'Unsupported file type {ext}. Use .csv or .json')
