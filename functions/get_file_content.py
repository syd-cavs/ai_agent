import os
from config import MAX_CHARS

def get_file_content(working_directory, file_path):
    filepath_directory = os.path.join(working_directory, file_path)
    working_directory_abs = os.path.abspath(working_directory)
    filepath_abs = os.path.abspath(filepath_directory)
    
    if not filepath_abs.startswith(working_directory_abs):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(filepath_abs):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    try:
        with open(filepath_abs, "r", encoding="utf-8") as f:
            file_content_string = f.read(MAX_CHARS)
            extra_string = f.read(1)

            if not extra_string:
                return file_content_string 
            else:
                return file_content_string + f'[...File "{file_path}" truncated at 10000 characters]'
        
    except Exception as e:
        return f"Error: {e}"