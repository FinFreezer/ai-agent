from google.genai import types
def run_python_file(working_directory, file_path, args=[]):
	import os
	import subprocess
	import sys
	working_directory_abs = os.path.abspath(working_directory)
	new_path = os.path.abspath( os.path.join(working_directory, file_path) )

	if not ( os.path.abspath(new_path).startswith( os.path.abspath(working_directory))):
		return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
	if not os.path.exists(new_path):
		return f'Error: File "{file_path}" not found.'
	if not new_path.endswith(".py"):
		return f'Error: "{file_path}" is not a Python file.'
	full_args = [sys.executable, file_path] + args
	try:
		outcome = subprocess.run(full_args, cwd=working_directory_abs, capture_output=True, text=True, timeout=30)
		stderr = outcome.stderr
		stdout = outcome.stdout
		if outcome.returncode != 0:
			return f"Received STDOUT: {stdout} and STDERR: {stderr}, Process exited with code {outcome.returncode}"
		if not outcome:
			return f'No output produced.'
			
		return f"Received STDOUT: {stdout} and STDERR: {stderr}"
	except Exception as e:
		return f'Error: executing Python file: {e}'
	
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a python file within the working directory and returns the output.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file we want to run, relative to the working directory."
            ),
            "args": types.Schema(
                type=types.Type.STRING, 
                description="The additional arguments passed on to the file being run."
            ),
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to run files from, relative to the working directory. If not provided, function might fail or run the wrong file if names match.",
            ),
        },
    ),
)