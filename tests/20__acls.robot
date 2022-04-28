*** Settings ***
Resource    keywords.resource

*** Test Cases ***
Bad user logon fails
    ${out}  ${err}  ${rc} =    Execute Command    podman exec -i ldapclient ldapwhoami -H ${SURL} -x -D 'uid\=baduser,${DOMSUFFIX}' -w 'badpass'
    ...    return_stderr=${TRUE}    return_rc=${TRUE}
    Should Be Equal As Integers    ${rc}    49
    Should Be Equal    ${out}    ${EMPTY}
    Should Contain    ${err}    Invalid credentials

Admin read access is allowed
    ${out}  ${err}  ${rc} =    Execute Command    podman exec -i ldapclient ldapsearch -H ${SURL} -LLL -x -D '${admuser}@${DOMAIN}' -w '${admpass}' -b ${DOMSUFFIX} samaccountname=${admuser} sAMAccountName
    ...    return_stderr=${TRUE}    return_rc=${TRUE}
    Should Be Equal As Integers    ${rc}    0
    Should Contain    ${out}    sAMAccountName:

Anonymous read access is forbidden
    ${out}  ${err}  ${rc} =    Execute Command    podman exec -i ldapclient ldapsearch -H ${SURL} -LLL -x -D '' -w '' -b ${DOMSUFFIX} samaccountname=${admuser} sAMAccountName
    ...    return_stderr=${TRUE}    return_rc=${TRUE}
    Should Be Equal As Integers    ${rc}    1
    Should Contain    ${err}    Operation unavailable without authentication

Ldapservice read access is allowed
    ${ldap_svcdn}    ${ldap_svcpass} =     Get ldapservice credentials    ${MID1}
    ${out}  ${err}  ${rc} =    Execute Command    podman exec -i ldapclient ldapsearch -H ${SURL} -LLL -x -D '${ldap_svcdn}' -w '${ldap_svcpass}' -b ${DOMSUFFIX} samaccountname=${admuser} sAMAccountName
    ...    return_stderr=${TRUE}    return_rc=${TRUE}
    Should Be Equal As Integers    ${rc}    0
    Should Contain    ${out}    sAMAccountName:
