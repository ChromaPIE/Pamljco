@echo off
set "script_path=%~dp0process_zip.py"

:loop
if "%~1"=="" goto :eof
python "%script_path%" "%~1"
echo DONE! Press any key to exit...
pause > nul

start "" "%~dp0converted\scracherry\assets"

shift
goto loop
