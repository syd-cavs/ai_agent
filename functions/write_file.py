import os
from google.genai import types

def write_file(working_directory, file_path, content):
    filepath_directory = os.path.join(working_directory, file_path)
    working_directory_abs = os.path.abspath(working_directory)
    filepath_abs = os.path.abspath(filepath_directory)

    if not filepath_abs.startswith(working_directory_abs):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    file_directory = os.path.dirname(filepath_abs)

    if not os.path.exists(file_directory):
        os.makedirs(file_directory, exist_ok=True)

    try:
        with open(filepath_abs, "w", encoding="utf-8") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"
    
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write contents to file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to write, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to write into the file.",
            ),
        },
        required=["file_path", "content"],
    ),
)