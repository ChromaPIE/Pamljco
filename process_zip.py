import os
import json
import shutil
import zipfile
from tqdm import tqdm

def process_json_file(json_file_path):
    try:
        with open(json_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        processed_data = {item['key']: item['translation'] for item in data if item['translation'].strip()}

        with open(json_file_path, 'w', encoding='utf-8') as file:
            json.dump(processed_data, file, ensure_ascii=False, indent=2)
            
    except Exception as e:
        print(f"An error occurred while processing the JSON file: {e}")
        return False
    return True

def main(zip_path):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    converted_folder_path = os.path.join(dir_path, 'converted')

    # Clear the contents of the converted folder
    if os.path.exists(converted_folder_path):
        shutil.rmtree(converted_folder_path)
    os.makedirs(converted_folder_path)

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(converted_folder_path)

    # Remove raw folder if exists
    raw_folder_path = os.path.join(converted_folder_path, 'raw')
    if os.path.exists(raw_folder_path):
        shutil.rmtree(raw_folder_path)

    utf8_folder_path = os.path.join(converted_folder_path, 'utf8')
    assets_folder_path = os.path.join(converted_folder_path, 'assets')
    scracherry_folder_path = os.path.join(converted_folder_path, 'scracherry')

    if os.path.exists(utf8_folder_path):
        os.rename(utf8_folder_path, assets_folder_path)

    # Process each JSON file
    for root, dirs, files in os.walk(assets_folder_path):
        for file in tqdm(files, desc='Processing JSON files'):
            if file.endswith('.json'):
                process_json_file(os.path.join(root, file))

    # Create scracherry folder and pack.mcmeta file
    os.makedirs(scracherry_folder_path, exist_ok=True)
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

    # Move assets folder into scracherry folder
    shutil.move(assets_folder_path, os.path.join(scracherry_folder_path, 'assets'))

    print("The processing is complete.")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python process_zip.py <path_to_zip_file>")
        # Keep the window open until the user closes it
        input("Press Enter to close...")
    else:
        main(sys.argv[1])
