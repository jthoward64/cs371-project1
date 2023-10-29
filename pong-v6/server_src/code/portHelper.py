# =================================================================================================
# Contributing Authors:	    Michael Stacy, Name Here, Name Here
# Email Addresses:          jmst231@uky.edu, Email Here, Email Here
# Date:                     October 29th, 2023
# Purpose:                  A simple way to detect if a port is in use or not
# Misc:                     Documentation: https://pypi.org/project/psutil/
# =================================================================================================

import psutil

def check_port(port:int) -> bool:
    '''Return True if Port is in Use'''
    for conn in psutil.net_connections(kind='inet'):
        if conn.laddr.port == port:
            return True
    
    return False