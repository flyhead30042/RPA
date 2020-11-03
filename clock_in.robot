*** Settings ***
Library    Selenium2Library

*** Variables ***
${APOLLO_URL}                                      https://auth.mayohr.com/HRM/Account/Login
${LOGIN_ID}                                 //*[@id="root"]/div/div[2]/div[1]/div/div[2]/div/div/form/div[1]/input
${LOGIN_PWD}                                //*[@id="root"]/div/div[2]/div[1]/div/div[2]/div/div/form/div[2]/input
${LOGIN_SUBMIT}                             //*[@id="root"]/div/div[2]/div[1]/div/div[2]/div/div/form/button
${ID}                                         c.i.hsiao@ericsson.com
${PWD}                                        brU4epC8

${ATTENDANCE}                               //*[@id="root"]/div/div/div/div[2]/div/ul/li[2]/a

${CHECKINOUT_XXX}                            //*[@id="root"]/div/div/div/div[3]/div/div/div/div/ul/li[3]/a
${CHECKINOUT}                                //*[@id="root"]/div/div/div/div[3]/div/div/div/div[2]/div[1]/div/div[2]/div/img
${CHECKINOUT_ONDUTY}                         //*[@id="root"]/div/div/div/div[3]/div/div/div/div[2]/div[3]/div/div[2]/div/div/div[1]/button

*** Test Cases ***
Go to Apollo
    Open Page    ${APOLLO_URL}  chrome
    Maximize Browser Window

Login Apollo
    Login With Valid Credentials    ${LOGIN_ID}  ${LOGIN_PWD}  ${LOGIN_SUBMIT}  ${ID}  ${PWD}


Clock In
    Open Function          ${CHECKINOUT}
    Should Be Presented    ${CHECKINOUT_ONDUTY}
    Click Button           ${CHECKINOUT_ONDUTY}

Close Browser
    Close Browser

*** Keywords ***
Open Page
    [Arguments]     ${url}  ${browser}
    Open Browser    ${url}  ${browser}

Login With Valid Credentials
    [Arguments]        ${login_id}  ${login_pwd}  ${login_submit}   ${id}   ${pwd}
    Wait Until Page Contains Element   ${login_submit}
    Input Text         ${login_id}  ${id}
    Input Password     ${login_pwd}  ${pwd}
    Click Button       ${login_submit}

Open Function
    [Arguments]        ${func}
    Wait Until Page Contains Element   ${ATTENDANCE}
    Click Link                         ${ATTENDANCE}
    Wait Until Page Contains Element   ${func}
    Click Element                      ${func}

Should Be Presented
    [Arguments]        ${locator}
    Wait Until Page Contains Element   ${locator}