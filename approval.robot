*** Settings ***
Library    Selenium2Library    run_on_failure=Nothing

*** Variables ***
${ID}                                         c.i.hsiao@ericsson.com
${PWD}                                        brU4epC8

${APOLLO_URL}                                      https://auth.mayohr.com/HRM/Account/Login
${LOGIN_ID}                                 //*[@id="root"]/div/div[2]/div[1]/div/div[2]/div/div/form/div[1]/input
${LOGIN_PWD}                                //*[@id="root"]/div/div[2]/div[1]/div/div[2]/div/div/form/div[2]/input
${LOGIN_SUBMIT}                             //*[@id="root"]/div/div[2]/div[1]/div/div[2]/div/div/form/button

${ATTENDANCE}                            //*[@id="root"]/div/div/div/div[2]/div/ul/li[2]/a

${APPROVAL}                              //*[@id="root"]/div/div/div/div[3]/div/div/div/div[2]/div[1]/div/div[8]/a
${APPROVAL_SELECT_ALL}                 //*[@id="root"]/div/div/div/div[3]/div/div/div/div[2]/div[1]/div[3]/div[1]/table/tbody/tr/th[6]/input

${APPROVAL_BATCH}                      //*[@id="root"]/div/div/div/div[3]/div/div/div/div[2]/div[1]/div[2]/div/button
${APPROVAL_ITEM_1}                  //*[@id="root"]/div/div/div/div[3]/div/div/div/div[2]/div[1]/div[3]/div[2]/div[1]/table/tbody/tr[5]

${APPROVAL_CONFIRM}                   //*[@id="root"]/div/div/div/div[3]/div/div/div/div[2]/div[2]/div/div[2]/form/div[2]/button[1]
${APPROVAL_RESULT_CONFIRM}                   //*[@id="root"]/div/div/div/div[3]/div/div/div/div[2]/div[3]/div/div[2]/div[2]/button


*** Test Cases ***

Login Apollo
    Login ${APOLLO_URL} With Credentials ${ID} And ${PWD}

Show Approval List
    Open ${ATTENDANCE} Function
    Open ${APPROVAL} Function

Approve
    Approve Pending eForm

Close Browser
    Close Browser

*** Keywords ***
Open ${func} Function
    Wait Until Element Is Visible      ${func}   timeout=10.0
    Click Element                      ${func}


Login ${url} With Credentials ${id} And ${pwd}
    Open Browser    ${url}  chrome
    Maximize Browser Window
    Wait Until Page Contains Element   ${LOGIN_SUBMIT}
    Input Text         ${LOGIN_ID}  ${id}
    Input Password     ${LOGIN_PWD}  ${pwd}
    Click Button       ${LOGIN_SUBMIT}

Wait Until Page Not Contains ${expected}
  Wait Until Keyword Succeeds    Page Should Not Contain expected    ${expected}    timeout=10.0


Click Button Until Visible ${button}
    Wait Until Element Is Visible    ${button}
    Click Button                     ${button}


Approve Pending eForm
    Wait Until Element Is Visible    ${APPROVAL_ITEM_1}    timeout=10.0  error=No approval item found
    Wait Until Element Is Visible    ${APPROVAL_SELECT_ALL}    timeout=10.0
    Select Checkbox                  ${APPROVAL_SELECT_ALL}

    Click Button Until Visible     ${APPROVAL_BATCH}
    Click Button Until Visible     ${APPROVAL_CONFIRM}
    Click Button Until Visible     ${APPROVAL_RESULT_CONFIRM}




