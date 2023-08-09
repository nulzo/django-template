import sys
import os 
import re
import time
import random

def open_or_create(out_name: str) -> str:
    os.makedirs(os.path.dirname(out_name), exist_ok=True)
    return out_name

def ellipses(string: str):
    diff = 120 - len(string)
    for _ in range(diff):
        time.sleep(random.random() / random.randint(50, 100))
        print(".", end="")

def main():

    YELLOW = "\033[1;33m"
    RED = "\033[1;31m"
    LIGHT_BLUE = "\033[1;34m"
    END = "\033[0m"
    LIGHT_GREEN = "\033[1;32m"

    if len(sys.argv) < 1:
        print(f"{RED}ERROR: Something catastrophic happened... Close the window and start over.\n{END}")
        sys.exit()

    if len(sys.argv) <= 4:
        print(f"{RED}ERROR: Project data not received properly. Terminating.\n{END}")
        sys.exit()
    
    PROJECT_NAME = sys.argv[1]
    BUILD_PATH = sys.argv[2]
    PROJECT_AUTHOR = sys.argv[3]
    PROJECT_EMAIL = sys.argv[4]
    TEMPLATE_PATH = sys.argv[5]
        
    print(f"\n{YELLOW}STARTING BUILD PROCESS OF PROJECT: {LIGHT_BLUE}{TEMPLATE_PATH}{END}")

    for root, _, file_names in os.walk(TEMPLATE_PATH):
        for file in file_names:
            ROOT = os.path.join(root, file)
            print(f"\nPARSING FILE:\t{YELLOW}{ROOT}{END}", end=" ")
            ellipses(ROOT)
            print(f" {LIGHT_GREEN}SUCCESS{END}")
            START_IDX = ROOT.find("PROJECTNAME")
            DIR_NAMES = re.sub("PROJECTNAME", PROJECT_NAME, ROOT[START_IDX:])

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

    print(f"\n{LIGHT_GREEN}SUCCESSFULLY WROTE FILES ... THIS WINDOW WILL CLOSE AND PROCESS WILL CONTINUE{END}")
    time.sleep(5)

main()
