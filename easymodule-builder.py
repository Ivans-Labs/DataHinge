import argparse
import json
import os
import subprocess
from typing import Any, Dict, List

def create_module(module_name: str, args: List[Dict[str, Any]], overwrite: bool = False, force: bool = False) -> None:
    """Create a new module with the given name and arguments."""
    # Check if the module file already exists
    filename = os.path.join("scripts", f"{module_name}.py")
    if os.path.exists(filename):
        if not overwrite:
            print(f"Error: File {filename} already exists. Use the --overwrite option to overwrite the file.")
            return
        elif not force:
            choice = input(f"File {filename} already exists. Do you want to overwrite it? (y/n) ")
            if choice.lower() != "y":
                print("Module creation cancelled.")
                return

    # Prompt the user for information about the module
    print("Enter information about the module:")
    function_name = input("Function name: ")
    description = input("Description: ")
    arguments = []
    while True:
        arg_name = input("Argument name (leave blank to finish): ")
        if not arg_name:
            break
        arg_description = input("Argument description: ")
        arg_type = select_arg_type()
        arg_required = input("Is argument required? (y/n): ")
        arg_required = arg_required.lower() == "y"
        arguments.append({
            "name": arg_name,
            "description": arg_description,
            "type": arg_type,
            "required": arg_required
        })

    # Create the new module script
    with open(filename, "w") as f:
        f.write(f"import argparse\n\n")
        f.write(f"def {function_name}(args):\n")
        f.write(f"    # {description}\n")
        for arg in arguments:
            f.write(f"    {arg['name']} = args.{arg['name']}\n")
        f.write(f"    # Implement module functionality here\n")
        f.write(f"    # Example usage of arguments:\n")
        f.write(f"    # print(f'Value of {arguments[0]['name']} is: ', {arguments[0]['name']})\n\n")
        f.write(f"def parse_arguments() -> argparse.Namespace:\n")
        f.write(f"    parser = argparse.ArgumentParser(description='{description}')\n")
        for arg in arguments:
            if arg["required"]:
                f.write(f"    parser.add_argument('--{arg['name']}', type={arg['type']}, required=True, help='{arg['description']}')\n")
            else:
                f.write(f"    parser.add_argument('--{arg['name']}', type={arg['type']}, help='{arg['description']}')\n")
        f.write(f"    return parser.parse_args()\n\n")
        f.write(f"def main() -> None:\n")
        f.write(f"    args = parse_arguments()\n")
        f.write(f"    {function_name}(args)\n\n")
        f.write(f"if __name__ == '__main__':\n")
        f.write(f"    main()\n")

    # Create a metadata entry for the new module
    metadata = {
        module_name: {
            "title": module_name.capitalize(),
            "description": description,
            "meta_title": module_name.capitalize(),
            "args": arguments
        }
    }

    # Add the new metadata to the modules.json file
    with open("modules.json", "r+") as f:
        data = json.load(f)
        data["modules"].append(metadata)
        f.seek(0)
        json.dump(data, f, indent=4)

    # Check if the user wants to add a dependency
    while True:
        choice = input("Do you want to add a dependency? (y/n) ")
        if choice.lower() == "y":
            dependency = input("Enter the name of the dependency: ")
            # Verify that the dependency exists on PyPI
            try:
                subprocess.check_call(["pip", "search", dependency])
                # Add the dependency to requirements.txt
                with open("requirements.txt", "a") as f:
                    f.write(f"{dependency}\n")
                print(f"Dependency {dependency} added successfully.")
            except subprocess.CalledProcessError:
                print(f"Error: Dependency {dependency} not found on PyPI.")
        elif choice.lower() == "n":
            break

    print(f"Module {module_name} created successfully.")

def select_arg_type() -> str:
    """Prompt the user to select an argument type."""
    choices = [
        "str",
        "int",
        "float",
        "bool",
        "list",
        "tuple",
        "dict",
    ]
    print("Select argument type:")
    for i, choice in enumerate(choices):
        print(f"{i+1}. {choice}")
    while True:
        try:
            choice = int(input(f"Enter choice (1-{len(choices)}): "))
            if 1 <= choice <= len(choices):
                return choices[choice-1]
        except ValueError:
            pass
        print("Invalid choice. Try again.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a new module for the data CLI tool.")
    parser.add_argument("module_name", help="The name of the new module.")
    parser.add_argument("-o", "--overwrite", action="store_true", help="Overwrite the module file if it already exists.")
    parser.add_argument("-f", "--force", action="store_true", help="Do not prompt before overwriting the module file.")
    args = parser.parse_args()

    create_module(args.module_name, [], args.overwrite, args.force)