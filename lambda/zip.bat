@echo off
setlocal enabledelayedexpansion

set outputFolder=lambda-zip
if not exist "!outputFolder!" (
    mkdir "!outputFolder!"
)

for %%f in (*.py) do (
    :: 압축 파일 이름 생성
    set fileName=%%~nf
    set zipFile="!outputFolder!\!fileName!.zip"
    
    :: 해당 .py 파일을 ZIP으로 압축
    powershell -Command "Compress-Archive -Path '%%f' -DestinationPath !zipFile!"
)

echo 모든 .py 파일이 압축되었습니다.
pause
