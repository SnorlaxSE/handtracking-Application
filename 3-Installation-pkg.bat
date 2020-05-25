:: 1.5 change pip source 
c:
cd %UserProfile%
mkdir pip
cd pip
cd.>pip.ini
echo [global] >> pip.ini
echo index-url=https://pypi.douban.com/simple  >> pip.ini
echo extra-index-url=http://pypi.mirrors.ustc.edu.cn/simple/  >> pip.ini

echo [install] >> pip.ini
echo trusted-host=pypi.mirrors.ustc.edu.cn  >> pip.ini

:: 1.6 install Dependency
d:
cd %~dp0 
CALL conda activate handtrack
pip install -r requirement.txt

pause
