Higadiff2 is written for python 2. 

---------------
Start
---------------
When the script is run it will first ask for a URL from your "control" site. and updated site.
This designates the root domain of the two sites to be compared.

The next step gives the user an option to enter login credentials, it works with basic auth by appending the login 
to the beginning of each domain and sending the password if/when an authentication popup appears.


--------------------
Headcode and loopcode
---------------------
It might be necessary to login or take other action before the driver begins navigating to each url in the csv. 
The user may create a file called headcode.txt in the script directory. The script will execute any python syntax
in that file.

Similarly, the user can also designate code to be run immediately after selenium tries to find a url.
This could be useful for adding wait time or telling the webdriver to take other actions.

---------------------
Comparison
---------------------
As the script runs it will use the imagechops library to create a difference map between black and white versions of both versions of the page.
difference map between each image by matching pixels from first top to bottom as well as upside down.
The reason it is checked upside down is to prevent the tool from reporting false negatives if the page heights do not match.


--------------------
Threaded execution
--------------------
The comparison tool will operate using multiple threads in order to visit and compare each page faster than if it had to visit every page one at a time.

--------------------
Slack integration
--------------------
When the comparison has completed an update will be posted in your organizations Automation_Log slack channel.