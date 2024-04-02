@echo off
 :: BatchGotAdmin
 :-------------------------------------
 REM  --> Check for permissions
 >nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"

REM --> If error flag set, we do not have admin.
 if '%errorlevel%' NEQ '0' (
     echo Requesting administrative privileges...
     goto UACPrompt
 ) else ( goto gotAdmin )

:UACPrompt
     echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
     echo UAC.ShellExecute "%~s0", "", "", "runas", 1 >> "%temp%\getadmin.vbs"

    "%temp%\getadmin.vbs"
     exit /B

:gotAdmin
     if exist "%temp%\getadmin.vbs" ( del "%temp%\getadmin.vbs" )
     pushd "%CD%"
     CD /D "%~dp0"

python get-pip.py
pip install pydicom

mkdir %userprofile%\\dcm2png
copy dcm2png.py %userprofile%\\dcm2png

reg add "HKCR\Folder\shell\ConvertDICOMtoPNG" /f /ve /t REG_SZ /d "Convert DICOM to PNG" 
reg add "HKCR\Folder\shell\ConvertDICOMtoPNG\command" /f /ve /t REG_SZ /d "cmd /c python \"%userprofile%\dcm2png\dcm2png.py\" -i \"%%1\" -o \"%%1\png\" -c -v"

taskkill /im explorer.exe /f
start explorer.exe
echo Install Complete. File explorer will restart shortly.
timeout /t 10