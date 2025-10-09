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
	
