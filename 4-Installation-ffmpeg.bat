:: 2.1 unzip ffmpeg to specific path (./software/)
:: 2.2 set ffmpeg System PATH
setx PATH -m "%PATH%;%~dp0\software\ffmpeg-20200515-b18fd2b-win64-static\bin"  

ffmpeg

pause
