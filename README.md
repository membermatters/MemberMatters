# HSBNE Member Portal
The HSBNE member portal is how HSBNE members manage their membership.

### Features
* Member registration system (signup, login etc)
* Profile - members can update all their info in one place
    * Personal details like name, email etc.
    * Cause membership
* Access system built in
    * Activate new members
    * Enable/Disable existing members
    * Doors and tools/machinary permissions
    * API so readers/interlocks can check access
* Member overview for executive
    * Search for members
    * Sort members by status, etc
    * Change a member's details/membership type
* Space webcam integration
* Swipe Statistics
    * Last seen (last time a member swipes)
    * Recent swipes (last x swipes at any door)
* Basic Spacebucks Support
    * Members can see a transaction list
    * Can see current balance
    * Can't add funds, must be manually done right now - stripe integration planned shortly.
 
 ### Coming Soon
 * Integration with xero or direct debit service for billing management
    * Manage membership costs and recurring invoices
    * Spacebucks payment processing
    * Let Xero or direct debit service handle payment details
 * Edit member swipe in theme
 
 ### Getting Started
 First step is to grab a copy of this repository. You will need to make sure you have python installed, preferably
 3.6 or newer as that's the only version it has been tested on. Make sure you also install pip so that you can install
 all of the dependencies.
 
 To install python 3/pip and the requirements run these commands from within this folder:
 ##### Linux (Ubuntu)
 
 ```bash
 sudo apt install python3 python3-pip
 sudo -H pip3 install -r requirements.txt
 ```
 
 ##### Linux (Fedora)
 ```
sudo dnf install python3 python3-pip
sudo -H pip3 install -r requirements.txt
```
 
 ##### Mac (Tested by nog3 w/python 3.7)
 You will need to install and use virtualenv on Mac in order to get your environment correct as there are conflicts with built in python on OSX.
 
 ```bash
brew install python3
pip3 install virtualenv
virtualenv hsbneportal
source hsbneportal\bin\activate
pip3 install -r requirements.txt

You should see (<environment_name>) $ at your command prompt, letting you know that you’re running the proper virtualenv install. To deactivate, you can just run the following to come out of the environment.

```deactivate
```
 
 ##### Windows
 Please add instructions if you use windows.
 
 #### Running the dev server
 In production, we have an nginx reverse proxy setup. For development however, it's useful to use the built in development
 server. Navigate to the memberportal folder. (`cd memberportal` on bash) First we need
 to make sure we have a local sqlite database with the correct migrations applied so run this:
 
 
 `python3 manage.py migrate`
 
 After running that you should see something like this:
 ```angular2html
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, portal, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  ...
```

If that completes with no errors run the command below to start the development server.

```
python3 manage.py runserver
```

You should see something like this:

```
Django version 2.0.7, using settings 'memberportal.settings'
Starting development server at http://127.0.0.1:8000/
```
Take note of the IP and port. In this case, open your favourite browser and go to `http://127.0.0.1:8000/`. You should
be presented with the home page of the web app. If you want to contribute any changes to the portal please see below.
 
 ### Contributing
 If you're able to write python (django) or JavaScript please contribute. It's a lot of work to write something like  this properly from scratch. Check with Jaimyn before working on something, then make a pull request when you are happy with your changes. 
 ##### note: no iframes of existing php member pages allowed. All features must be implemented properly in python.
 
 ## Screenshots

 ![screenshot](https://raw.githubusercontent.com/jabelone/hsbneportal/master/screenshots/screenshot.png)
 ![screenshot2](https://raw.githubusercontent.com/jabelone/hsbneportal/master/screenshots/screenshot2.png)
 ![screenshot3](https://raw.githubusercontent.com/jabelone/hsbneportal/master/screenshots/screenshot3.png)
 ![screenshot4](https://raw.githubusercontent.com/jabelone/hsbneportal/master/screenshots/screenshot4.png)
<img src="https://raw.githubusercontent.com/jabelone/hsbneportal/master/screenshots/screenshot5.png" width="400">
<img src="https://raw.githubusercontent.com/jabelone/hsbneportal/master/screenshots/screenshot6.png" width="400">
<img src="https://raw.githubusercontent.com/jabelone/hsbneportal/master/screenshots/screenshot7.png" width="300">
<img src="https://raw.githubusercontent.com/jabelone/hsbneportal/master/screenshots/screenshot8.png" width="300">
