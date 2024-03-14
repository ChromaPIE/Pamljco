@echo off
set "script_path=%~dp0process_zip.py"

:loop
if "%~1"=="" goto :eof
python "%script_path%" "%~1"
echo Processing complete. Press any key to exit...
pause > nul

:: Emulate Alt+Tab
:: sendkeys.bat
echo Set WshShell = WScript.CreateObject("WScript.Shell") > sendkeys.vbs
echo WshShell.SendKeys "%%{TAB}" >> sendkeys.vbs
echo WshShell.SendKeys "%%{TAB}" >> sendkeys.vbs
cscript /nologo sendkeys.vbs
del sendkeys.vbs

shift
goto loop
