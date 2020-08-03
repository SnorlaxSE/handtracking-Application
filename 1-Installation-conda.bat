:: Default: 'handtracking-Application' folder is at 'D:xxx'
d:
:: cd .bat filepath
cd %~dp0 

:: 1.1 install anaconda && 1.2 set anaconda PATH
cd software
start /wait "" Anaconda3-2020.02-Windows-x86_64.exe /AddToPath=1 /S /D=%UserProfile%\anaconda3

:: 1.3 change conda source
:: tsinghua 
CALL conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
CALL conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge 
CALL conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/msys2/

CALL conda config --set show_channel_urls yes

pause

conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge 
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/msys2/
conda config --set show_channel_urls yes