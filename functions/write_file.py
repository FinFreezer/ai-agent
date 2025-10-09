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
