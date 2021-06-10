@ECHO OFF

title Compile Lens Entertain
echo Compiling Lens Entertain

pyinstaller.exe --icon=Logo.ico --noconsole --onefile "Lens Entertain.py"
cls

echo Done.
move "dist\Lens Entertain.exe" "Lens Entertain.exe"

rmdir dist
rmdir build
rmdir __pycache__

del "Lens Entertain.spec"

echo|set /p="Continue."
pause >nul
exit
