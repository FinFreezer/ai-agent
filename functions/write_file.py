from google.genai import types
def write_file(working_directory, file_path, content):
	import os
	new_path = os.path.abspath( os.path.join(working_directory, file_path) )
	print(f"Working directory is {os.path.abspath(working_directory)}")
	print(f"Current path is {os.path.abspath(new_path)}")

	if not ( os.path.abspath(new_path).startswith( os.path.abspath(working_directory))):
		return f'Error: Cannot write to "{file_path}" as it is outside the permited working directory'
	if not os.path.exists(new_path):
		try:
			os.makedirs( os.path.dirname(new_path), exist_ok=True)
		except Exception as e:
			return f"Error: creating directory: {e}"

	if os.path.exists(new_path) and os.path.isdir(new_path):
		return f'Error: "{file_path}" is a directory, not a file'
	
	try:
		with open(new_path, "w") as f:
			f.write(content)
			return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
	except Exception as e:
		return f"Error: writing to file: {e}"

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Will attempt to overwrite an existing file's contents, or create it, if it doesn't already exist.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to the desired file. Will be created if does not already exist."
        ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content the function will attempt to write to the designated file path."
        ),
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to find the file to write to from, relative to the working directory. If not provided, function will try to create the directory and add the file to it.",
            ),
        },
    ),
)