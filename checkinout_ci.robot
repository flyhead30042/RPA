*** Settings ***
Documentation    Clock in for CI
Resource         checkinout.robot


*** Variables ***
${ID}                                         c.i.hsiao@ericsson.com
${PWD}                                        brU4epC8

*** Test Cases ***
Check In
    [Setup]   Set Selenium Timeout   10.0
    Go to Apollo
    Login Apollo
    Recheck In
    [Teardown]  Close Browser


Check Out
    [Setup]   Set Selenium Timeout   10.0
    Go to Apollo
    Login Apollo
    Recheck Out
    [Teardown]  Close Browser


