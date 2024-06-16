# Github_Scrapping
This repository contains the code for extracting the URL's of the public repositories of a github account and then storing them in a .CSV file.

## How to run the code:
### .env file:
Enter the username and password of your github account in the 'usn' and 'pass' fields respectively.
Enter the gmail account and password of your gmail account linked with your github account in the 'usn2' and 'pass2' field respectively.
Now save the file in the same directory as of the project.
### chromedriver file:
Setup the webdriver for google chrome from: https://googlechromelabs.github.io/chrome-for-testing/#stable
Extract the zip folder and save the 'chromedriver.exe' file in the same directory as of the project. You can delete the remaining files!

Remember to disable the two-factor authentiacation for your github account!

## How the code will run:
When you will execute the 'Github-Scrapping.py' file, a temporary chrome browser window will open and it will show the login page for your github account. The code will extract the login credentials from the .env file and will automatically fill the credentials in the login fields of the github login page.
Once this is done, you will be logged in, into your github account and the home page of your github account will show up. Then the temporary chrome window will get closed.
You can now see a .CSV file in the same directory as of the project named 'Repositories.csv' which will contain the URL's of all the public repositories of your github account.
