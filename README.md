# Deletion Buddy

A photography tool used to sync two folders, where folder A stores processed - and folder B raw pictures. 
Often you sort out pictures in folder A and want to edit them later in folder B. If you don't want to delete the raw images from folder B as well, use this tool!

## Requirements

Python needs to be installed and you need to be able to call it from the CLI. See [Python Downloads](https://www.python.org/downloads/).
[PIP](https://pypi.org/project/pip/) needs to be installed (usually installs while installing python from python.org).

You can check if you have all requirements installed by typing

```bash
python --version
pip --version
```

, or if you are using OSX

```bash
python3 --version
pip3 --version
```

. This should display the current version number.

After verifying the installation, you need to install the necessary python packages. You can do this using the following command

```bash
pip install -r requierements.txt
```

, or on OSX

```bash
pip3 install -r requirements.txt
```

## Usage

```
usage: deletion_buddy.py [-h] [--file_type [FILE_TYPE]] [--d] [--c] [--l] [--list_all] [--log] [--disable_print] a b

Delete files from dir B which are not in dir A

positional arguments:
  a                     Source directory (A)
  b                     Destination directory (B)

options:
  -h, --help            show this help message and exit
  --file_type [FILE_TYPE]
                        File type to delete
  --d                   Delete files from directory B without asking
  --c                   Copy files from directory A to B without asking
  --l                   List files to delete
  --list_all            List all files from both directories
  --log                 Log system messages.
  --disable_print       Disable output to terminal.
```

