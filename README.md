# DataHinge-CLI

DataHinge-CLI is a command-line interface (CLI) tool that makes it easy to manage and process data files. Whether you need to clean up messy datasets, extract specific information, or transform data into a different format, DataHinge can help.

## Features

-   Easy-to-use CLI interface for managing data files
-   Multiple built-in modules for common data processing tasks, including:
    -   Empty directory remover
    -   Directory cleaner
    -   GitHub repository downloader
-   Support for custom modules and scripts
-   Multi-threaded processing for faster performance

## Installation

DataHinge requires Python 3.6 or later. To install, simply run:

`pip3 install datahinge-cli`

## Usage

To run DataHinge, simply enter the following command in your terminal:

`datahinge-cli`

This will start the interactive CLI, where you can choose from available modules or create your own.

## Available Modules

DataHinge comes with several built-in modules for common data processing tasks:

-   `emptyremover`: A tool to remove empty directories in a specified directory
-   `mrcleaner`: Cleans directory and sub-directory everything except a file extension
-   `gh_repo_downloader`: Clone GitHub repositories based on criteria.

Use the `module` command to select and run a module:


`DataHinge module mrcleaner --dir /path/to/directory --file-ext .txt --num-workers 4`

This will run the `mrcleaner` module with the specified arguments.

## Custom Modules

You can create your own custom modules and scripts to extend the functionality of DataHinge. Simply add your script to the `scripts` directory and define its arguments in the `modules.json` file.

## Contributing

Contributions are welcome! If you find a bug or have an idea for a new feature, please open an issue or submit a pull request.

## License

DataHinge is licensed under the [MIT License](https://chat.openai.com/chat/LICENSE).
