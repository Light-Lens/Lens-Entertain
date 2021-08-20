@ECHO OFF

title Compile Lens Entertain
echo Compiling Lens Entertain

pyinstaller.exe --icon=Logo.ico --noconsole "Lens Entertain.py"
move "dist\Lens Entertain" .\bin

rmdir /s /q dist
rmdir /s /q build
rmdir /s /q __pycache__

del "Lens Entertain.spec"

cls
if EXIST "bin\Lens Entertain.exe" goto Compiled
if NOT EXIST "bin\Lens Entertain.exe" goto NotCompiled

:Compiled
echo Lens Entertain Compiled Successfully!
echo Get ready to Entertain Yourself!
echo|set /p="Continue."
pause >nul
exit

:NotCompiled
echo Can't Compile Lens Entertain!
echo|set /p="Continue."
pause >nul
exit
