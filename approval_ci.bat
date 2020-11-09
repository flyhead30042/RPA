@ECHO OFF
@REM This batch file is to check in&out automatically

ECHO =========================================
ECHO
ECHO Auto approval script
ECHO
ECHO =========================================

cls
d:
cd "d:\workspace\citest\RPA"
ECHO "Change to %CD%"

ECHO "Initiate Anaconda"
CALL C:\Anaconda3\Scripts\activate.bat C:\Anaconda3
CALL conda activate RPA
robot.exe -v ID:c.i.hsiao@ericsson.com  -v PWD:brU4epC8  ./approval.robot


