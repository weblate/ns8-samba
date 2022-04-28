*** Settings ***
Resource        keywords.resource

Suite Setup     Add test groups
Suite Teardown  Remove test groups

*** Keywords ***
Add test groups
    Run task    module/${MID1}/add-group    {"group":"g1","users":[]}
    Run task    module/${MID1}/add-group    {"group":"g2","users":[]}

Remove test groups
    Run task    module/${MID1}/remove-group    {"group":"g1"}
    Run task    module/${MID1}/remove-group    {"group":"g2"}

*** Test Cases ***
Add user first.user
    Run task    module/${MID1}/add-user    {"user":"first.user","full_name":"First User","locked":false,"groups":["g1"]}

    ${out}  ${err}  ${rc} =    Execute Command    podman exec ${MID1} pdbedit -Lv first.user
    ...    return_stderr=${TRUE}    return_rc=${TRUE}
    Should Be Equal As Integers    ${rc}    0
    Should Contain    ${out}    first.user
    Should Contain    ${out}    First User
    Should Not Contain    ${out}    [DU

    ${out}  ${err}  ${rc} =    Execute Command    podman exec ${MID1} samba-tool group listmembers g1
    ...    return_stderr=${TRUE}    return_rc=${TRUE}
    Should Be Equal As Integers    ${rc}    0
    Should Contain    ${out}    first.user

Alter user first.user
    Run task    module/${MID1}/alter-user    {"user":"first.user","full_name":"Changed full name","locked":true,"groups":["g2"]}

    ${out}  ${err}  ${rc} =    Execute Command    podman exec ${MID1} pdbedit -Lv first.user
    ...    return_stderr=${TRUE}    return_rc=${TRUE}
    Should Be Equal As Integers    ${rc}    0
    Should Contain    ${out}    first.user
    Should Not Contain    ${out}    First User
    Should Contain    ${out}    Changed full name
    Should Contain    ${out}    [DU
    Should Not Contain    ${out}    [U

    ${out}  ${err}  ${rc} =    Execute Command    podman exec ${MID1} samba-tool group listmembers g1
    ...    return_stderr=${TRUE}    return_rc=${TRUE}
    Should Be Equal As Integers    ${rc}    0
    Should Not Contain    ${out}    first.user

    ${out}  ${err}  ${rc} =    Execute Command    podman exec ${MID1} samba-tool group listmembers g2
    ...    return_stderr=${TRUE}    return_rc=${TRUE}
    Should Be Equal As Integers    ${rc}    0
    Should Contain    ${out}    first.user

Alter non-existing user
    Run task    module/${MID1}/alter-user    {"user":"bad-user","full_name":"First User","locked":false,"groups":["g1"]}
    ...    rc_expected=1

Remove user first.user
    Run task    module/${MID1}/remove-user    {"user":"first.user"}

    ${out}  ${err}  ${rc} =    Execute Command    podman exec ${MID1} pdbedit -Lv first.user
    ...    return_stderr=${TRUE}    return_rc=${TRUE}
    Should Not Be Equal As Integers    ${rc}    0
