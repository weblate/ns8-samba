*** Settings ***
Library           SSHLibrary
Resource    keywords.resource
Suite Setup       Setup connection and test suite tools
Suite Teardown    Stop the client tool container

*** Variables ***
${SSH_KEYFILE}    %{HOME}/.ssh/id_ecdsa
${NODE_ADDR}      127.0.0.1

*** Keywords ***
Connect to the node
    Log    connecting to ${NODE_ADDR}
    Open Connection   ${NODE_ADDR}
    Login With Public Key    root    ${SSH_KEYFILE}
    ${output} =    Execute Command    systemctl is-system-running  --wait
    Should Be True    '${output}' == 'running' or '${output}' == 'degraded'

Setup connection and test suite tools
    Connect to the node
    Start the client tool container
