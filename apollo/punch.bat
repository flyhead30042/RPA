@ECHO OFF
@REM This batch file is to check in&out automatically

ECHO =========================================
ECHO
ECHO Auto Check in/out script
ECHO
ECHO =========================================

cls
d:
cd "d:\workspace\citest\RPA\apollo"
ECHO "Change to %CD%"

ECHO "Initiate Anaconda"
CALL C:\Anaconda3\Scripts\activate.bat C:\Anaconda3
CALL conda activate RPA
@REM Example: CALL python.exe D:/workspace/citest/RPA/apollo/punch.py -id=c.i.hsiao@ericsson.com -pwd=brU4epC8 -punch=all -dt=2021/2/25
CALL python D:/workspace/citest/RPA/apollo/punch.py %1 %2 %3 %4 %5
