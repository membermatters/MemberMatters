 ### Getting Started
 First step is to grab a copy of this repository. You will need to make sure you have python installed, preferably
 3.6 or newer as that's the only version it has been tested on. Make sure you also install pip so that you can install
 all of the dependencies.
 
 To install python 3/pip and the requirements run these commands from within this folder:
 #### Linux (Ubuntu)
 
 ```bash
 sudo apt install python3 python3-pip
 sudo -H pip3 install -r requirements.txt
 ```
 
 #### Linux (Fedora)
```
sudo dnf install python3 python3-pip
sudo -H pip3 install -r requirements.txt
```
 
 #### Mac (Tested by nog3 w/python 3.7)
 You will need to install and use virtualenv on Mac in order to get your environment correct as there are conflicts with built in python on OSX.
 
```bash
brew install python3
pip3 install virtualenv
virtualenv venv 
source venv\bin\activate
pip3 install -r requirements.txt
```

You should see (venv) $ at your command prompt, letting you know that you’re running the proper virtualenv install. To deactivate, you can just run the following to come out of the environment.

```bash
deactivate
```

#### Windows
Please follow the instructions below to setup dev environment in Windows (tested in Windows 7 & 10).
* Download & install Python 3.6+ from [here](https://www.python.org/downloads/)
* CD into the cloned repository.
* Assuming `pip` and `virtualenv` is already installed as part of the package, execute: `py -3 -m venv venv` 
* Activate the venv by running: `venv\Scripts\activate`
* Install dependencies by running: `pip install -r requirements-win.txt`
* You're all set up. Follow the instructions below to start the dev server.
 
### Running the dev server
In production, we have an apache reverse proxy setup. For development however, it's useful to use the built in 
development server. Navigate to the memberportal folder. (`cd memberportal` on bash or cmd) First we need to make 
sure we have a local sqlite database with the correct migrations applied, and default database. 

To do this run the following:

```bash
python3 manage.py migrate
```
 
After running that you should see something like this:
```bash
Operations to perform:
  Apply all migrations: access, admin, auth, causes, contenttypes, profile, sessions, memberbucks
Running migrations:
  Applying causes.0001_initial... OK
  Applying auth.0001_initial... OK
  ...
```

Now load some initial data into the database:
```bash
python3 manage.py loaddata fixtures/initial.json
```

If that completes with no errors run the command below to start the development server.

```bash
python3 manage.py runserver
```

You should see something like this:

```bash
Django version 2.0.7, using settings 'membermatters.settings'
Starting development server at http://127.0.0.1:8000/
```

Take note of the IP and port. In this case, open your favourite browser and go to `http://127.0.0.1:8000/`. You should 
be presented with the home page of the web app. You can login with the username "default@example.com" and password 
"MemberMatters!". You should create a new account, then use the default account to give your new account admin rights. You 
should change the password of the default admin account.

##### Notes for HSBNE infrastructure maintainers
On porthack01 you can find the mapped volumes at `/usr/app` and there's an update script at `/usr/app/update_portal.sh`. You will need to rebuild and push to docker hub the docker image.

##### NOTE
You will need to re-run the database migration every time the db models change. You may see random database related errors such as column does not exist if you forget to do this. You can do that by running:

`python3 manage.py migrate`

To test all of the features you will need some api keys. Define these as environment variables:
* PORTAL_SENDGRID_API_KEY
* PORTAL_TRELLO_API_KEY
* PORTAL_TRELLO_API_TOKEN
* PORTAL_STRIPE_PUBLIC_KEY
* PORTAL_STRIPE_SECRET_KEY
* PORTAL_XERO_CONSUMER_KEY
* PORTAL_XERO_RSA_FILE (path to the rsa key)
* PORTAL_DISCORD_INTERLOCK_WEBHOOK
* PORTAL_DISCORD_DOOR_WEBHOOK
