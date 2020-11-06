*** Settings ***
Library    Selenium2Library

*** Variables ***
${APOLLO_URL}                                      https://auth.mayohr.com/HRM/Account/Login
${LOGIN_ID}                                 //*[@id="root"]/div/div[2]/div[1]/div/div[2]/div/div/form/div[1]/input
${LOGIN_PWD}                                //*[@id="root"]/div/div[2]/div[1]/div/div[2]/div/div/form/div[2]/input
${LOGIN_SUBMIT}                             //*[@id="root"]/div/div[2]/div[1]/div/div[2]/div/div/form/button
#${ID}                                         c.i.hsiao@ericsson.com
#${PWD}                                        brU4epC8

#${ATTENDANCE}                               //*[@id="root"]/div/div/div/div[2]/div/ul/li[2]/a

${CHECKINOUT}                                //*[@id="root"]/div/div/div/div[3]/div/div/div/div/ul/li[3]/a/div/img
${CHECKINOUT_ONDUTY}                         //*[@id="root"]/div/div/div/div[3]/div/div/div/div[2]/div[3]/div/div[2]/div/div/div[1]/button

${RECHECKINOUT}                         //*[@id="root"]/div/div/div/div[3]/div/div/div/div/ul/li[4]/a/div/img

${RECHECKINOUT_TYPE_DROPDOWN}           //*[@id="root"]/div/div/div/div[3]/div/div/div/div[2]/div[3]/div/div[2]/form/div[1]/div[2]/div/div/div/div/div/span
${RECHECKINOUT_TYPE_ONDUTY}             //*[@id="root"]/div/div/div/div[3]/div/div/div/div[2]/div[3]/div/div[2]/form/div[1]/div[2]/div/div/div/div/div[2]/div/div[1]
${RECHECKINOUT_TYPE_OFFDUTY}            //*[@id="root"]/div/div/div/div[3]/div/div/div/div[2]/div[3]/div/div[2]/form/div[1]/div[2]/div/div/div/div/div[2]/div/div[2]
${RECHECKINOUT_TIME_DROPDOWN}           //*[@id="root"]/div/div/div/div[3]/div/div/div/div[2]/div[3]/div/div[2]/form/div[1]/div[3]/div/div[1]/div/div/div/span
${RECHECKINOUT_TIME_09}                 //*[@id="root"]/div/div/div/div[3]/div/div/div/div[2]/div[3]/div/div[2]/form/div[1]/div[3]/div/div[1]/div/div/div[2]/div/div[10]
${RECHECKINOUT_TIME_18}                 //*[@id="root"]/div/div/div/div[3]/div/div/div/div[2]/div[3]/div/div[2]/form/div[1]/div[3]/div/div[1]/div/div/div[2]/div/div[19]
${RECHECKINOUT_LOC_DROPDOWN}            //*[@id="root"]/div/div/div/div[3]/div/div/div/div[2]/div[3]/div/div[2]/form/div[1]/div[4]/div/div/div/div/div/span
${RECHECKINOUT_LOC_ERT}                 //*[@id="root"]/div/div/div/div[3]/div/div/div/div[2]/div[3]/div/div[2]/form/div[1]/div[4]/div/div/div/div/div[2]/div/div[1]
${RECHECKINOUT_OK}                      //*[@id="root"]/div/div/div/div[3]/div/div/div/div[2]/div[3]/div/div[2]/form/div[2]/button[1]
${RECHECKINOUT_CONFIRM}                //*[@id="root"]/div/div[2]/div/div[2]/button[1]



*** Keywords ***
### keywords ###
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
#    Wait Until Element Is Visible   ${ATTENDANCE}
#    Click Link                         ${ATTENDANCE}
    Wait Until Element Is Visible   ${func}
    Click Element                      ${func}

Should Be Presented
    [Arguments]        ${locator}
    Wait Until Page Contains Element   ${locator}

Click Element Until Visible
    [Arguments]        ${locator}
    Wait Until Element Is Visible    ${locator}
    Click Element                     ${locator}


### use cases ###
Go to Apollo
    Open Page    ${APOLLO_URL}  chrome
    Maximize Browser Window

Login Apollo
    Login With Valid Credentials    ${LOGIN_ID}  ${LOGIN_PWD}  ${LOGIN_SUBMIT}  ${ID}  ${PWD}


Check InOut
    Open Function          ${CHECKINOUT}
    Should Be Presented    ${CHECKINOUT_ONDUTY}
    Click Button           ${CHECKINOUT_ONDUTY}


Recheck In
    Recheck                 ${RECHECKINOUT_TYPE_ONDUTY}   ${RECHECKINOUT_TIME_09}

Recheck Out
    Recheck                 ${RECHECKINOUT_TYPE_OFFDUTY}   ${RECHECKINOUT_TIME_18}

Recheck
    [Arguments]             ${type}  ${time}
    Open Function           ${RECHECKINOUT}


    Click Element Until Visible          ${RECHECKINOUT_TYPE_DROPDOWN}
    Click Element Until Visible          ${type}

    Click Element Until Visible          ${RECHECKINOUT_TIME_DROPDOWN}
    Click Element Until Visible          ${time}

    Click Element Until Visible         ${RECHECKINOUT_LOC_DROPDOWN}
    Click Element Until Visible         ${RECHECKINOUT_LOC_ERT}

    Click Element Until Visible          ${RECHECKINOUT_OK}
    Click Element Until Visible          ${RECHECKINOUT_CONFIRM}