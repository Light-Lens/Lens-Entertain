@ECHO OFF

title Compile Lens Entertain
echo Compiling Lens Entertain

pyinstaller.exe --icon=Logo.ico --noconsole --onefile "Lens Entertain.py"
cls

echo Done.
move "dist\Lens Entertain.exe" "Lens Entertain.exe"

rmdir /s /q dist
rmdir /s /q build
rmdir /s /q __pycache__

del "Lens Entertain.spec"

echo|set /p="Continue."
pause >nul
exit
