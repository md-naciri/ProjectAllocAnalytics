import os


def get_user_file_path(prompt, must_exist=True):
    """
    Get a file path from the user with validation.

    Args:
        prompt (str): Prompt to display to the user
        must_exist (bool): Whether the file must exist

    Returns:
        str: The validated file path
    """
    while True:
        file_path = input(prompt)
        file_path = file_path.strip('"')  # Remove quotes if user included them

        if not must_exist or os.path.exists(file_path):
            return file_path
        else:
            print(f"Error: File not found at '{file_path}'")
            print("Please enter a valid file path.")


def get_user_choice(prompt, options):
    """
    Get a choice from the user with validation.

    Args:
        prompt (str): Prompt to display to the user
        options (list): List of valid options

    Returns:
        str: The validated user choice
    """
    while True:
        choice = input(prompt)
        if choice in options:
            return choice
        else:
            print(f"Invalid choice. Please choose from: {', '.join(options)}")


def get_default_output_path(input_file, suffix="_output"):
    """
    Generate a default output file path based on an input file.

    Args:
        input_file (str): Path to the input file
        suffix (str): Suffix to add to the filename

    Returns:
        str: Default output file path
    """
    input_dir = os.path.dirname(input_file) or '.'
    input_filename = os.path.basename(input_file)
    name, ext = os.path.splitext(input_filename)

    return os.path.join(input_dir, f"{name}{suffix}{ext}")


def create_directories(path_list):
    """
    Create all directories in the given list if they don't exist.

    Args:
        path_list (list): List of directory paths to create
    """
    for directory in path_list:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Created directory: {directory}")