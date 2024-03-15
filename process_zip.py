import os
import json
import shutil
import zipfile
import sys  # Ensure this import is here
from tqdm import tqdm

def process_json_file(json_file_path):
    with open(json_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    processed_data = {item['key']: item['translation'] for item in data if item['translation'].strip()}

    with open(json_file_path, 'w', encoding='utf-8') as file:
        json.dump(processed_data, file, ensure_ascii=False, indent=2)

def copy_to_output_directory(source, destination):
    if os.path.exists(destination):
        shutil.rmtree(destination)
    shutil.copytree(source, destination)

def main(zip_path):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    converted_folder_path = os.path.join(dir_path, 'converted')
    output_txt_path = os.path.join(dir_path, 'output.txt')

    # Clear the contents of the converted folder
    if os.path.exists(converted_folder_path):
        shutil.rmtree(converted_folder_path)
    os.makedirs(converted_folder_path)

    # Extract the ZIP file into the converted folder
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(converted_folder_path)

    # Remove raw folder if exists
    raw_folder_path = os.path.join(converted_folder_path, 'raw')
    if os.path.exists(raw_folder_path):
        shutil.rmtree(raw_folder_path)

    # Process each JSON file in the utf8 folder
    utf8_folder_path = os.path.join(converted_folder_path, 'utf8')
    assets_folder_path = os.path.join(converted_folder_path, 'assets')
    if os.path.exists(utf8_folder_path):
        os.rename(utf8_folder_path, assets_folder_path)
        for root, _, files in os.walk(assets_folder_path):
            for file in tqdm(files, desc='Processing JSON files'):
                if file.endswith('.json'):
                    process_json_file(os.path.join(root, file))

    # Create scracherry folder and move assets into it
    scracherry_folder_path = os.path.join(converted_folder_path, 'scracherry')
    os.makedirs(scracherry_folder_path, exist_ok=True)
    shutil.move(assets_folder_path, os.path.join(scracherry_folder_path, 'assets'))

    # Create pack.mcmeta file
    pack_mcmeta_content = {
        "pack": {
            "pack_format": 15,
            "description": "scracherry overriding"
        },
        "language": {
            "zh_scr": {
                "name": "简体中文",
                "region": "Scracherry",
                "bidirectional": False
            }
        }
    }
    with open(os.path.join(scracherry_folder_path, 'pack.mcmeta'), 'w', encoding='utf-8') as file:
        json.dump(pack_mcmeta_content, file, ensure_ascii=False, indent=2)

    # Check if output.txt exists and contains a valid directory path
    if os.path.exists(output_txt_path):
        with open(output_txt_path, 'r') as file:
            output_directory = file.read().strip()
            if os.path.isdir(output_directory):
                copy_to_output_directory(scracherry_folder_path, os.path.join(output_directory, 'scracherry'))
                return  # Exit after copying to prevent opening the converted folder

    # Open the converted folder in file explorer
    os.startfile(converted_folder_path)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python process_zip.py <path_to_zip_file>")
    else:
        main(sys.argv[1])
