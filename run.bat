:: Default: 'handtracking-Application' folder is at 'D:xxx'
d:
:: cd .bat filepath
cd %~dp0 

:: avtivate enc
CALL conda activate handtrack

:: run 
start /b python detectVideo.py

pause
