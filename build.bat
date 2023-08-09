@echo off

set "project_path=%~dp0"

Title nulzo's epic django tool
cls
echo:
echo ---------- Django Template Creation Tool -----------
echo:

set /p "build_path=Build path (i.e. C:\Users\Me\Desktop) OR [enter] to build in current directory: "
if [%build_path%] == [] (set "build_path=%~dp0")
echo:
echo BUILDING IN: %build_path%
echo:

:name
set /p "project_name=Name of the Django project: "
if [%project_name%] == [] (
    echo:
    echo ERROR: Project must have a name!
    echo:
    goto :name
    )
echo:
echo BUILDING PROJECT: %project_name%
echo:

:author
set /p "project_author=Author for the project: "
if [%project_author%] == [] (
    echo:
    echo ERROR: Project must have an author!
    echo:
    goto :author
    )
echo:
echo PROJECT AUTHOR: %project_author%
echo:

:email
set /p "project_email=Email for the project [For Poetry]: "
if [%project_email%] == [] (
    echo:
    echo ERROR: Project must have an email!
    echo:
    goto :author
    )
echo:
echo PROJECT EMAIL: %project_email%
echo:

echo:
echo CONFIRM BUILD: "%project_name%" will be built at "%project_path%" with the author "%project_author%" with email "%project_email%"
:confirmation
set /p "confirm=Enter [Y] to build, or [N] to terminate: "

if NOT %confirm% == Y (
    if NOT %confirm% == y (
    if NOT %confirm% == N (
        if NOT %confirm% == n (
        echo:
        echo ERROR: You must enter [Y] or [N]!
        echo:
        goto :confirmation
    )))
)

if %confirm% == N (
        echo:
        echo TERMINATING PROCESS...
        echo:
    )

if %confirm% == n (
        echo:
        echo TERMINATING PROCESS...
        echo:
    )

if %confirm% == Y (
    cls
    python "%~dp0\build.py" %project_name% %build_path% %project_author% %project_email% %project_path% 
    cd %build_path%
    cd %project_name%
    echo SECRET_KEY=SECRET_KEY
    DEBUG=TRUE > .env
    pip install poetry
    poetry install
    poetry shell
    python "manage.py" migrate
)

if %confirm% == y (
    cls
    python "%~dp0\build.py" %project_name% %build_path% %project_author% %project_email% %project_path% 
    cd %build_path%
    cd %project_name%
    echo SECRET_KEY=SECRET_KEY
    DEBUG=TRUE > .env
    pip install poetry
    poetry install
    poetry shell
    python "manage.py" migrate
)
