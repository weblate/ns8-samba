*** Settings ***
Resource    keywords.resource

*** Test Cases ***
Remove the modules from the cluster
    Remove a module instance    ${MID1}
