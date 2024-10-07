import sys
import os
from file_detector import process_file

def main():
    if len(sys.argv) < 3:
        print("Usage: python main.py <directory_path> <api_key>")
        sys.exit(1)

    directory_path = sys.argv[1]
    api_key = sys.argv[2]

    if not os.path.isdir(directory_path):
        print(f"The specified path {directory_path} is not a directory.")
        sys.exit(1)

    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        if os.path.isfile(file_path):
            try:
                print(f"\nProcessing {filename}...")
                extracted_text = process_file(file_path, api_key)
                print(f"Extracted Text from {filename}:\n", extracted_text)
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")

if __name__ == "__main__":
    main()