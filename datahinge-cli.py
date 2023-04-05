import argparse
import importlib
import json
import os
import sys
import readline
from typing import List, Dict, Any, Tuple
from prompt_toolkit.completion import Completer, Completion


def completer(text: str, state: int) -> str:
    """Completion function for readline."""
    available_commands = ["exit", "module", "reload", "info"]
    options = [cmd for cmd in available_commands if cmd.startswith(text)]
    if state < len(options):
        return options[state]
    else:
        return None
        
class ModuleCompleter(Completer):
    """Completion class for module selector."""
    def __init__(self, modules):
        self.modules = modules

    def get_completions(self, document, complete_event):
        word_before_cursor = document.get_word_before_cursor()
        matches = [mod for mod in self.modules if mod.startswith(word_before_cursor)]
        for m in matches:
            yield Completion(m, -len(word_before_cursor))


def load_scripts() -> Dict[str, Dict[str, Any]]:
    """Load module data and import modules."""
    sys.path.append(os.path.join(os.getcwd(), "scripts"))

    scripts = {}
    with open("modules.json") as f:
        modules_data = json.load(f)
    for filename in [f for f in os.listdir("scripts") if f.endswith(".py") and not f.startswith("__")]:
        module_name = filename[:-3]
        module_data = modules_data.get(module_name, {})
        module = importlib.import_module(f"scripts.{module_name}")
        scripts[module_name] = {
            "module": module,
            "title": module_data.get("title", module_name),
            "meta_title": module_data.get("meta_title", module_name),
            "description": module_data.get("description", ""),
            "args": module_data.get("args", []),
        }
        print(f"Loaded module {module_name}")

        if module_name == "gh_repo_downloader":
            scripts[module_name]["module"].main = module.main

    return scripts


def main() -> None:
    """Main CLI function."""
    readline.set_completer(completer)
    readline.parse_and_bind("tab: complete")

    print("Welcome to Ivan's Data CLI Tool!")
    scripts = load_scripts()

    while True:
        try:
            user_input = input("Enter a command: ").split()
            if not user_input:
                continue

            command = user_input[0]
            arguments = user_input[1:]

            if command == "exit":
                break

            if command == "module":
                if len(arguments) == 0:
                    print("Error: Module name is missing.")
                    continue

                module_name = arguments[0]
                if module_name in scripts:
                    try:
                        script = scripts[module_name]
                        script["module"].main(arguments[1:])
                    except KeyboardInterrupt:
                        print("\nExiting...")
                    except SystemExit as e:
                        print(f"Error: {e}")
                        print(f"Usage: module {module_name} {' '.join(script['args'])}")
                    except argparse.ArgumentError as e:
                        print(f"Error: {e}")
                        print(f"Usage: module {module_name} {' '.join(script['args'])}")
                    except Exception as e:
                        print(f"Error: {e}")
                else:
                    print(f"Error: Module {module_name} not found.")
            elif command == "reload":
                scripts = load_scripts()
            elif command == "info":
                if len(arguments) == 0:
                    print("Error: Module name is missing.")
                    continue

                module_name = arguments[0]
                if module_name in scripts:
                    script = scripts[module_name]
                    print(f"{script['title']}")
                    print(f"  Description: {script['description']}")
                    print(f"  Usage: module {module_name} {' '.join(script['args'])}")
                else:
                    print(f"Error: Module {module_name} not found.")
            else:
                # Print help for modules
                print("Available modules:")
                for module_name, script in scripts.items():
                    print(f"{module_name} - {script['description']}")
                print("\nUse 'module [module_name] --help' for module usage instructions.")
        except KeyboardInterrupt:
            print("\nExiting...")
            break


if __name__ == "__main__":
    main()