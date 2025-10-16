from google.genai import types
import os

def get_files_info(working_directory, directory="."):
    new_path = os.path.join(working_directory, directory)
    print(f"Working directory is {os.path.abspath(working_directory)}")
    print(f"Current path is {os.path.abspath(new_path)}")
    if not (os.path.abspath(new_path).startswith(os.path.abspath(working_directory))):
        return f'Error: Cannot list "{new_path}" as it is outside the permited working directory'
    elif not (os.path.isdir(new_path)):
        return f'Error: "{new_path}" is not a directory'
    else:
        contents = os.listdir(new_path)
        results = [ ]
        for element in contents:
            path_to_element = os.path.join(new_path, element)
            if os.path.isdir(path_to_element):
                results.append( f'- {element}: file_size={os.path.getsize(path_to_element)} bytes, is_dir=True' )
            else:
                results.append( f'- {element}: file_size={os.path.getsize(path_to_element)} bytes, is_dir=False' )

        print("Result for current directory:")
        return "\n".join(results)

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

schema_get_file_content = types.FunctionDeclaration(
    name="get_files_content",
    description="Lists a file's contents while truncating it to a maximum of 10,000 characters.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to read files from, relative to the working directory. If not provided, function will fail.",
            ),
        },
    ),
)

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Will attempt to run the given file with optional parameters if included in the call.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to run files from, relative to the working directory. If not provided, function might fail or run the wrong file if names match.",
            ),
        },
    ),
)

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Will attempt to overwrite an existing file's contents, or create it, if it doesn't already exist.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to find the file to write to from, relative to the working directory. If not provided, function will try to create the directory and add the file to it.",
            ),
        },
    ),
)