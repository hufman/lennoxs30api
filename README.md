# PyPI - lennoxs30api
### API Wrapper for www.lennoxicomfort.com

By Pete Sage ()  

This asyncio module connects to the Lennox Cloud API to retrieve data from S30 / E30 thermostats.  This API does not work for older models that use a different API.  Those models are
supported by this project:  https://github.com/thevoltagesource/myicomfort


This module is currently in test and prototype mode; as such it is not recommended at this time to build an application on-top of the API, as the API may change.

This module provides a command line test program; that can be used to exercise the main functions and create diagnostic output files to futher enhance and fix issues with the API

Current state - Tested with a single Zone S30 Air Coniditioning System

Known Issues - None

Prerequistes:

1. Python version 3.8.6 or later

2. A Lennox sign-on (email address and password)

3. You may need to install aiohttp https://docs.aiohttp.org/en/stable/

Install Instructions:

1. Grab the repo

2. Edit the test_async.py program to supply the following
 
    LOG_PATH = '/home/pete/lennoxs30api'    #  Directoy to stash the log file in

    EMAIL_ADDRESS = 'myemail@myemail.com'

    PASSWORD = 'mypassword'

Command Line Program Instructions:

The command line program uses asyncio and runs 3 different tasks

- Task 1 (runner) - this task connects to the cloud API and periodically polls it at a 10 second interval

- Task 2 (poller) - this task runs on a 15 second interval and prints out information from Zone 1

- Task 3 (prompt) - this task reads from the command line and executes commands on behalf of the user to enabling API testing.  Cmd List

        cool, heat, off - sets the HVAC mode to cool, heat or off.  usage - just type the word followed by enter eg cool

        auto, on, circulate - sets the Fan mocde to auto, on, or ciruclate

        csp <TempF> - sets the cool setpoint in F.  example  csp 76

        hsp <TempF> - sets the heat setpoint in F.  example hsp 65

To exit the program hit crtl-c


