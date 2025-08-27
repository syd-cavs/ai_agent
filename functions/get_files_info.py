import os

def get_files_info(working_directory, directory="."):
    file_directory = os.path.join(working_directory, directory)
    working_directory_abs = os.path.abspath(working_directory)
    file_directory_abs = os.path.abspath(file_directory)
    
    answer = ""

    if not file_directory_abs.startswith(working_directory_abs):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    if not os.path.isdir(file_directory):
        return f'Error: "{directory}" is not a directory'

    try:
        files_list = os.listdir(file_directory_abs)
    except:
        return f"Error: {directory} cannot list directory"

    for file in files_list:
        try:
            indiv_filepath = os.path.join(file_directory_abs, file) 
            file_size = os.path.getsize(indiv_filepath)
            is_directory = os.path.isdir(indiv_filepath) 
            result = f"- {file}: file_size={file_size} bytes, is_dir={is_directory}\n"   
            answer += result
        except:
            continue
    return answer