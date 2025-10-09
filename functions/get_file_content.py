def get_file_content(working_directory, file_path):
    import os
    from functions.config import CHARACTER_LIMIT

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

