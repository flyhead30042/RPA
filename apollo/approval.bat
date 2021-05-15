@ECHO OFF
@REM This batch file is to approve all automatically

ECHO =========================================
ECHO
ECHO Auto Approval script
ECHO
ECHO =========================================

cls
d:
cd "d:\workspace\citest\RPA\apollo"
ECHO "Change to %CD%"

ECHO "Initiate Anaconda"
CALL C:\Anaconda3\Scripts\activate.bat C:\Anaconda3
CALL conda activate RPA

@REM Example: CALL python.exe D:/workspace/citest/RPA/apollo/approval.py -id=c.i.hsiao@ericsson.com -pwd=brU4epC8 -debug
CALL python.exe D:/workspace/citest/RPA/apollo/approval.py %1 %2 %3
