:: Default: 'handtracking-Application' folder is at 'D:xxx'
d:
:: cd .bat filepath
cd %~dp0 

:: avtivate enc
CALL conda activate handtrack

:: run 
python detectVideo.py

pause
