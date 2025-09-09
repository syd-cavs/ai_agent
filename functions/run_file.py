import os, subprocess, sys
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    file_abs = os.path.abspath(os.path.join(working_directory, file_path))
    working_directory_abs = os.path.abspath(working_directory)
    common = os.path.commonpath([working_directory_abs, file_abs])
    
    if common != working_directory_abs:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    elif not os.path.isfile(file_abs):
        return f'Error: File "{file_path}" not found.'
    elif not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        cmd = [sys.executable, file_abs, *args]
        completed = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=working_directory_abs,
            timeout=30,
        )
        out = completed.stdout or ""
        err = completed.stderr or ""

        if not out and not err:
            return "No output produced."

        result = f"STDOUT: {out}\nSTDERR: {err}".rstrip()

        if completed.returncode != 0:
            result += f"\nProcess exited with code {completed.returncode}"

        return result

    except Exception as e:
        return f"Error: executing Python file: {e}"

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Execute a Python file with optional arguments.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to run, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Optional list of CLI arguments to pass to the script.",
                items=types.Schema(type=types.Type.STRING),
            ),
        },
        required=["file_path"],
    ),
)