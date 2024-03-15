@echo off
set "script_path=%~dp0process_zip.py"

:loop
if "%~1"=="" goto :eof
python "%script_path%" "%~1"
echo Processing complete. Press any key to exit...
pause > nul
shift
goto loop
