import os
import sys

def extract_files_from_exe(exe_file, output_dir):
    # File signatures and footers
    FILE_SIGNATURES = {
        "PNG": {"header": b"\x89PNG\r\n\x1a\n", "footer": b"IEND\xaeB`\x82"},
        "OGG": {"header": b"OggS", "footer": None},  # OGG doesn't have a strict footer
        "MP3": {"header": b"\xFF\xFB", "footer": None},  # MP3 doesn't have a strict footer
    }

    try:
        # Open the executable file in binary mode
        with open(exe_file, 'rb') as file:
            data = file.read()

        # Ensure the output directory exists
        os.makedirs(output_dir, exist_ok=True)

        for file_type, markers in FILE_SIGNATURES.items():
            header = markers["header"]
            footer = markers["footer"]

            start = 0
            count = 0

            while start < len(data):
                # Find the file header
                start = data.find(header, start)
                if start == -1:
                    break

                # Find the file footer if it exists
                if footer:
                    end = data.find(footer, start) + len(footer)
                    if end == -1 or end <= start:
                        break
                else:
                    # If no footer, set an arbitrary size limit (e.g., 10MB max size for unknown length)
                    end = start + 10 * 1024 * 1024

                # Extract the file data
                file_data = data[start:end]

                # Save the extracted file
                output_file = os.path.join(output_dir, f'{file_type.lower()}_{count:04d}.{file_type.lower()}')
                with open(output_file, 'wb') as out_file:
                    out_file.write(file_data)

                print(f'Extracted {file_type} #{count} to {output_file}')
                count += 1

                # Move the search position past the current file
                start = end

            if count == 0:
                print(f"No {file_type} files found in the file.")
            else:
                print(f"Successfully extracted {count} {file_type} file(s).")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python extract_files.py <path_to_exe> <output_dir>")
        sys.exit(1)

    exe_file_path = sys.argv[1]
    output_dir_path = sys.argv[2]

    extract_files_from_exe(exe_file_path, output_dir_path)
