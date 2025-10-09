def get_files_info(working_directory, directory="."):
    import os
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