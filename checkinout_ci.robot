*** Settings ***
Documentation    Clock in for CI
Resource         checkinout.robot


*** Variables ***
${ID}                                         c.i.hsiao@ericsson.com
${PWD}                                        brU4epC8

*** Test Cases ***
Check In
    Go to Apollo
    Login Apollo
    Recheck In


Check Out
    Go to Apollo
    Login Apollo
    Recheck Out


