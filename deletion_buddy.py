import argparse
import os
import inspect
from datetime import datetime

parser = argparse.ArgumentParser(description="Delete files from dir B which are not in dir A")
parser.add_argument("a", type=str, help="Source directory (A)")
parser.add_argument("b", type=str, help="Destination directory (B)")
parser.add_argument("--file_type", type=str, help="File type to delete", default=None, nargs="?")
parser.add_argument("--d", action="store_true", help="Delete files from directory B without asking", default=False)
parser.add_argument("--c", action="store_true", help="Copy files from directory A to B without asking", default=False)
parser.add_argument("--l", action="store_true", help="List files to delete", default=True)
parser.add_argument("--list_all", action="store_true", help="List all files from both directories", default=False)
parser.add_argument("--log", action="store_true", help="Log system messages.", default=True)
parser.add_argument("--disable_print", action="store_true", help="Disable output to terminal.", default=False)

def get_input(args, log_file, msg):
  ret = input(msg)

  if args.log and log_file != None:
    log_to_file(log_file, "OUT:" + msg)
    log_to_file(log_file, "IN:" + ret)

  return ret

def log(args, log_file, msg):
  if not args.disable_print:
    print(msg)
  
  if args.log and log_file != None:
    log_to_file(log_file, "OUT:" + msg)

def count_files(directory):
  file_count = 0
  for root, dirs, files in os.walk(directory):
    file_count += len(files)
  return file_count

def get_files_to_copy(a_files: list, b_files: list):
  for f1 in a_files:
    match = False
    for f2 in b_files:
      # check if the name matches a file in b_files, extension doesn't matter
      if f1.split(".")[0] == f2.split(".")[0]:
        match = True
    if not match:
      yield f1

def get_files_to_delete(a_files: list, b_files: list):
  for f1 in b_files:
    match = False
    for f2 in a_files:
      # check if the name matches a file in a_files, extension doesn't matter
      if f1.split(".")[0] == f2.split(".")[0]:
        match = True
    if not match:
      yield f1

def print_files(files: list):
  for f in files:
    log(args, log_file, f"\t{f}")

def log_to_file(filename: str, msg: str):
  with open(filename, '+a') as file:
    file.write(datetime.today().strftime('%Y-%m-%d %H:%M:%S | '))
    file.write(msg)
    file.write("\n")

def get_plural(files, s_or_is: bool = True):
  val = ''

  if len(files) > 1 and s_or_is:
    val = 's'
  
  if len(files) > 1 and not s_or_is:
    val = 'are'

  if len(files) <= 1 and not s_or_is:
    val = 'is'

  return val

def do_delete(files_to_delete):
  for f in files_to_delete:
    os.remove(os.path.join(args.b, f))
    log(args, log_file, f"Deleted {f}")

def do_copy(files_to_copy):
  for f in files_to_copy:
    src = os.path.join(args.a, f)
    dst = os.path.join(args.b, f)
    error = os.system(f"cp '{src}' '{dst}'")
    if error > 0:
      raise RuntimeError()
    
    log(args, log_file, f"Copied {f}")

def main(args, log_file):
  a_cnt = count_files(args.a)
  b_cnt = count_files(args.b)

  log(args, log_file, f"{a_cnt} files in directory A ({args.a})")
  log(args, log_file, f"{b_cnt} files in directory B ({args.b})")

  if a_cnt == 0:
    log(args, log_file, "No files in directory A")
    return
  if b_cnt == 0:
    log(args, log_file, "No files in directory B")
    return
  
  a_files = sorted(os.listdir(args.a))
  b_files = sorted(os.listdir(args.b))

  if args.list_all:
    log(args, log_file, f"Files in Directory A ({args.a}): ")
    print_files(a_files)
    log(args, log_file, f"Files in Directory B ({args.b}): ")
    print_files(b_files)

  if args.file_type:
    # only consider files with the specified file type in dir B
    b_files = filter(lambda x: x.endswith(args.file_type), b_files)

    log(args, log_file, f"Directory B ({args.b}): ")
    print_files(b_files)

  files_to_delete = list(get_files_to_delete(a_files, b_files))
  log(args, log_file, f"{len(files_to_delete)} files to be deleted{': ' if args.l and len(files_to_delete) > 0 else '.'}")
  
  if len(files_to_delete) > 0:
    if args.l:
      print_files(files_to_delete)
    else:
      do_print_files_to_delete = get_input(args, log_file, "List files (Y/n)? ").lower()
      if do_print_files_to_delete == "" or do_print_files_to_delete == "y":
        print_files(files_to_delete)

    if not args.d:
      delete = get_input(args, log_file, f"Should {len(files_to_delete)} file{get_plural(files_to_delete)} be deleted (Y/n)? ").lower()
      if delete == "" or delete == "y":
        do_delete(files_to_delete)
    else:
      do_delete(files_to_delete)   

  files_to_copy = list(get_files_to_copy(a_files, b_files))

  log(args, log_file, f"Found {len(files_to_copy)} file{get_plural(files_to_copy)} that {get_plural(files_to_copy, False)} in A, but not in B.")
  if args.list_all:
    print_files(files_to_copy)
  else:
    do_list_files_to_copy = get_input(args, log_file, f"List file{get_plural(files_to_copy)} (Y/n)? ").lower()
    if do_list_files_to_copy == "" or do_list_files_to_copy == "y":
      print_files(files_to_copy)
  
  if not args.c:
    copy = get_input(args, log_file, f"Copy files from A to B (Y/n)? ").lower()
    if copy == "" or copy == "y":
      do_copy(files_to_copy)
  else:
    do_copy(files_to_copy)

  log(args, log_file, "Done!")

if __name__ == "__main__":
  args = parser.parse_args()
  if args.l:
    args.list_all = True

  log_file = None
  if args.log:
    py_file = inspect.getframeinfo(inspect.currentframe()).filename
    working_dir = os.path.dirname(os.path.abspath(py_file))
    file_name = datetime.today().strftime('%Y-%m-%d_%H-%M-%S') + ".log"
    log_file = os.path.join(working_dir, file_name)

  try:
    main(args, log_file)
  except KeyboardInterrupt:
    log(args, log_file, "")
    log(args, log_file, "Keyboard Interrupt. Aborting...")
    pass
  except RuntimeError:
    log(args, log_file, "An Error occured! Check files!")

  log(args, log_file, "Exiting...")
