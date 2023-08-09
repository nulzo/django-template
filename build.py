import sys
import os 
import re
import time
import random
import pathlib
import subprocess

YELLOW = "\033[1;33m"
RED = "\033[1;31m"
LIGHT_BLUE = "\033[1;34m"
END = "\033[0m"
LIGHT_GREEN = "\033[1;32m"
TEMPLATE_SUBDIR = "template_struct"
TEMPLATE_PLACEHOLDER_DIRS = "PROJECTNAME"

def display(*args) -> None:
    for arg in args:
        print(f"{YELLOW}{arg[0]}{END}:", end="")
        time.sleep(0.5)
        print(f"\t{LIGHT_BLUE}{arg[1]}{END}")

def print_title() -> None:
    print(f"""{LIGHT_BLUE}
______ _                          ______          _           _    ___  ___      _             
|  _  (_)                         | ___ \        (_)         | |   |  \/  |     | |            
| | | |_  __ _ _ __   __ _  ___   | |_/ / __ ___  _  ___  ___| |_  | .  . | __ _| | _____ _ __ 
| | | | |/ _` | '_ \ / _` |/ _ \  |  __/ '__/ _ \| |/ _ \/ __| __| | |\/| |/ _` | |/ / _ \ '__|
| |/ /| | (_| | | | | (_| | (_) | | |  | | | (_) | |  __/ (__| |_  | |  | | (_| |   <  __/ |   
|___/ | |\__,_|_| |_|\__, |\___/  \_|  |_|  \___/| |\___|\___|\__| \_|  |_/\__,_|_|\_\___|_|   
     _/ |             __/ |                     _/ |                                           
    |__/             |___/                     |__/                                               {END}""")
    print(f"\n{'Version: 0.0.1':^90}")
    print(f"{'Created by: nulzo':^90}")
    print("\n")

def cursor():
    return ">>  "

def open_or_create(out_name: str) -> str:
    os.makedirs(os.path.dirname(out_name), exist_ok=True)
    return out_name

def show_error(MSG: str):
    return f"{cursor()}{RED}ERROR: {MSG}{END}"

def is_path(PATH: str, FILE: str) -> bool:
    return os.path.exists(os.path.join(PATH, FILE))

def ellipses(string: str) -> None:
    diff: int = 120 - len(string)
    for _ in range(diff):
        time.sleep(random.random() / random.randint(50, 100))
        print(".", end="")

def terminate_process() -> None:
    sys.exit(f"{cursor()}{RED}TERMINATING PROCESS...{END}")

def validate(MSG: str) -> bool:
    cursor()
    CONFIRM: str = input(f"{cursor()}{YELLOW}CONFIRM:{END} {MSG} [y/n]: ").upper()
    while CONFIRM != "N" and CONFIRM != "Y":
        print(show_error(f"Value must be either [Y] or [N]!"))
        CONFIRM: str = input(MSG).upper()
    if CONFIRM == "N":
        terminate_process()
    print(f"{cursor()}{LIGHT_GREEN}CONFIRMED{END}\n")
    return True

def validate_email(EMAIL: str) -> bool:
     return re.search("""(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])""", EMAIL)

def get_author(PRMPT: str, CNFM: str) -> str:
    AUTHOR: str = input(f"{cursor()}{PRMPT}")
    validate(f"{CNFM}{LIGHT_BLUE}{AUTHOR}{END}")
    return AUTHOR

def get_project_name(PRMPT: str, CNFM: str) -> str:
    PROJECT_NAME: str = input(f"{cursor()}{PRMPT}")
    validate(f"{CNFM}")
    return PROJECT_NAME

def get_author_email(PRMPT: str, CNFM: str) -> str:
    AUTHOR_EMAIL: str = input(f"{cursor()}{PRMPT}")
    while not validate_email(AUTHOR_EMAIL):
        print(show_error("Please enter a valid email address!"))
        AUTHOR_EMAIL: str = input(f"{cursor()}Author email of the project [for Poetry]: ")
    validate(f"{CNFM}{LIGHT_BLUE}{AUTHOR_EMAIL}{END}")
    return AUTHOR_EMAIL

def get_project_name(PRMPT: str, CNFM: str) -> str:
    PROJECT_NAME: str = input(f"{cursor()}{PRMPT}")
    validate(f"{CNFM}{LIGHT_BLUE}{PROJECT_NAME}{END}")
    return PROJECT_NAME

def get_build_path(FILE_NAME: str) -> str:
    PATH: str = input(f"{cursor()}Enter the path to build the project OR [enter] to build in current directory: ")
    if not PATH:
        PATH = os.path.join(pathlib.Path(__file__).parent.resolve())
    TRUE_PATH: str = os.path.join(PATH, FILE_NAME)
    while is_path(PATH=PATH, FILE=FILE_NAME):
        print(show_error("Location is not empty! Please enter an empty path!"))
        PATH: str = input(f"{cursor()}Enter the path to build the project: ")
    validate(f"The build location for the project is: {LIGHT_BLUE}{TRUE_PATH}{END}")
    return PATH

def main():

    print_title()
    PROJECT_NAME: str = get_project_name("Enter a name for the Django project: ", "The name of the project is: ")
    PROJECT_AUTHOR: str = get_author("Enter an author for the Django project [for Poetry]: ", "The author of the project is: ")
    PROJECT_EMAIL: str = get_author_email("Enter an email for the Django project [for Poetry]: ", "The email of the project is: ")
    BUILD_PATH: str = get_build_path(PROJECT_NAME)
    TEMPLATE_PATH: str = os.path.join(pathlib.Path(__file__).parent.resolve(), TEMPLATE_SUBDIR)

    display(("PROJECT NAME", PROJECT_NAME), 
            ("PROJECT AUTHOR", PROJECT_AUTHOR),
            ("PROJECT EMAIL", PROJECT_EMAIL),
            ("BUILD LOCATION", BUILD_PATH))
        
    print(f"\n{YELLOW}STARTING BUILD PROCESS OF PROJECT: {LIGHT_BLUE}{PROJECT_NAME}{END}")

    for root, _, file_names in os.walk(TEMPLATE_PATH):
        for file in file_names:
            ROOT = os.path.join(root, file)
            print(f"\nPARSING FILE:\t{YELLOW}{ROOT}{END}", end=" ")
            ellipses(ROOT)
            print(f" {LIGHT_GREEN}SUCCESS{END}")
            START_IDX = ROOT.find(TEMPLATE_PLACEHOLDER_DIRS)
            DIR_NAMES = re.sub(TEMPLATE_PLACEHOLDER_DIRS, PROJECT_NAME, ROOT[START_IDX:])

            IN_FILE = open(ROOT, "r")
            OUT_FILE_PATH = open_or_create(os.path.join(BUILD_PATH, DIR_NAMES))
            print(f"WRITING TO:\t{LIGHT_BLUE}{OUT_FILE_PATH}{END}", end=" ")
            ellipses(OUT_FILE_PATH)
            print(f" {LIGHT_GREEN}SUCCESS{END}")
            OUT_FILE = open(OUT_FILE_PATH, "w")

            FILE_READER = IN_FILE.read()
            if re.search("_{2}P.*?_{2}", FILE_READER):
                FILE_READER = re.sub("_{2}P.*?_{2}", PROJECT_NAME, FILE_READER)
            if re.search("_{2}A.*?_{2}", FILE_READER):
                FILE_READER = re.sub("_{2}A.*?_{2}", f'[\"{PROJECT_AUTHOR} <{PROJECT_EMAIL}>\"]', FILE_READER)
            OUT_FILE.write(FILE_READER)

            IN_FILE.close()
            OUT_FILE.close()

    OUT_FILE_PATH = open_or_create(os.path.join(BUILD_PATH, PROJECT_NAME, ".env"))
    OUT_FILE = open(OUT_FILE_PATH, "w")
    print(f"\nPOPULATE ENV:\t{LIGHT_BLUE}{OUT_FILE_PATH}{END}", end=" ")
    time.sleep(1)
    ellipses(f"{OUT_FILE_PATH}")
    print(f" {LIGHT_GREEN}DONE{END}")
    OUT_FILE.writelines(["SECRET_KEY=SECRET_KEY\n", "DEBUG=True"])
    OUT_FILE.close()

    OUT_FILE_PATH = open_or_create(os.path.join(BUILD_PATH, PROJECT_NAME))
    print(f"\nVALIDATING:\t{LIGHT_BLUE}{OUT_FILE_PATH}{END}", end=" ")
    time.sleep(1)
    ellipses(f"{OUT_FILE_PATH}")
    print(f" {LIGHT_GREEN}VALIDATED{END}")

    print(f"\n{LIGHT_GREEN}SUCCESS{END}: Parsed and processed all files! Switching to new project directory...\n")
    time.sleep(1)
    os.chdir(OUT_FILE_PATH)
    print(f"{YELLOW}NAGIVATED TO{END}: {LIGHT_BLUE}{OUT_FILE_PATH}{END}")
    print(f"\n{YELLOW}CREATING POETRY ENVIRONMENT{END}")
    subprocess.run(["pip", "install", "poetry"])
    print(f"\n{LIGHT_GREEN}SUCCESS{END}: Installed Poetry!\n")
    print(f"\n{YELLOW}INSTALLING POETRY PACKAGES{END}")
    subprocess.run(["poetry", "install"])
    print(f"\n{LIGHT_GREEN}SUCCESS{END}: Installed Poetry packages!\n")
    print(f"\n{YELLOW}WRITING POETRY LOCK FILE{END}")
    subprocess.run(["poetry", "lock", "--no-update"])
    print(f"\n{LIGHT_GREEN}SUCCESS{END}: Wrote Poetry lock file!\n")
    print(f"\n{YELLOW}APPLYING INITIAL DJANGO MIGRATIONS{END}")
    subprocess.run(["poetry", "run", "python", "manage.py", "makemigrations"])
    subprocess.run(["poetry", "run", "python", "manage.py", "migrate"])
    print(f"\n{LIGHT_GREEN}SUCCESS{END}: Applied initial Django migrations and initialized database!")
    print(f"\n{LIGHT_GREEN}SUCCESS{END}: New Django project has been built and initialized in {LIGHT_BLUE}{OUT_FILE_PATH}{END}!")
    print(f"\n{LIGHT_GREEN}SUCCESS{END}: Build has completed. Closing window in {RED}5{END} seconds.")
    time.sleep(5)


main()
