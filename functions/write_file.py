import os
from config import MAX_CHARS

def write_file(working_directory, file_path, content):
    filepath_directory = os.path.join(working_directory, file_path)
    working_directory_abs = os.path.abspath(working_directory)
    filepath_abs = os.path.abspath(filepath_directory)

    if not filepath_abs.startswith(working_directory_abs):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    file_directory = os.path.dirname(filepath_abs)

    if not os.path.exists(file_directory):
        new_file = os.makedirs(file_directory)

    try:
        with open(filepath_abs, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"
    
    