from google.genai import types
from functions.config import CHARACTER_LIMIT
def get_file_content(working_directory, file_path):
    import os

    new_path = os.path.join(working_directory, file_path)
    print(f"Working directory is {os.path.abspath(working_directory)}")
    print(f"Current path is {os.path.abspath(new_path)}")
    if not (os.path.abspath(new_path).startswith(os.path.abspath(working_directory))):
        return f'Error: Cannot list "{file_path}" as it is outside the permited working directory'
    if not ( os.path.isfile(new_path) ):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    with open(new_path, "r") as f:
        position = f.tell()
        text = f.read()
        f.seek(position)
        chars = sum(len(word) for word in text)
        print(f"Original length is {chars} characters.")
        if chars > 10000:
            file_content_string = f.read(CHARACTER_LIMIT)
            chars = sum(len(word) for word in file_content_string)
            file_content_string += f' [...File "{file_path}" truncated at 10000 characters]'
            print(f"Truncated file is: {chars} characters long")
            return file_content_string
        else:
            file_content_string = f.read()
            print(f"File is: {chars} characters long")
            return file_content_string

        
    

    return f'Error: Something went wrong.'

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description=f"Reads and returns the first {CHARACTER_LIMIT} characters of the content from a specified file within the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file whose content should be read, relative to the working directory.",
            ),
        },
        required=["file_path"],
    ),
)