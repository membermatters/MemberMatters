 ### Getting Started
 > Note: MemberMatters only supports running in Docker on Linux. Installing Docker is outside the scope of this guide, 
>please consult your favourite search engine for tips.
 
 To get started, download the latest version from docker hub using the following command:
 ```bash
docker pull jaimynmayer/membermatters
```

Create a file to contain all of your environment variables. This file contains sensitive information so treat it like a 
password! Place it somewhere you won't forget like `/usr/app/env.list`. This file is where Docker gets the environment 
variables from.
```
PORTAL_DOMAIN=https://demo.membermatters.org
PORTAL_ENV=Production

PORTAL_LOG_LOCATION=[optional - remove line if not used]
PORTAL_DB_LOCATION=[optional - remove line if not used]

PORTAL_SENDGRID_API_KEY=sg.xxxx

PORTAL_XERO_CONSUMER_KEY=
PORTAL_XERO_RSA_FILE=/path/to/xerkey.pem

PORTAL_STRIPE_SECRET_KEY=<stripe>
PORTAL_STRIPE_PUBLIC_KEY=<stripe>

PORTAL_TRELLO_API_KEY=<trello>
PORTAL_TRELLO_API_TOKEN=<trello>

PORTAL_DISCORD_INTERLOCK_WEBHOOK=https://discordapp.com/api/webhooks/xxxx/xxxxxx
PORTAL_DISCORD_DOOR_WEBHOOK=https://discordapp.com/api/webhooks/xxxx/xxxxxx
```

Once you've downloaded the docker image and configured your environment variables, you'll need to create a container:
```bash
docker create -p 8000:8000 --name membermatters --restart always --detach --env-file /usr/app/env.list -v /usr/app/:/usr/src/data jaimynmayer/membermatters
```

Once your container is running, you will be able to login with the default admin account details:
```
Email: default@example.com
Password: MemberMatters!
```

The first thing you should do is change the email address and password of the default admin account. You can do that 
by navigating to `http://<instance_url>/admin/profile/user` and clicking on the user on that list.

Once you've done all this, your MemberMatters instance is ready for use. Read on below for tips on customising 
and deploying it.

### Deployment Tips
* MemberMatters runs on port 8000 by default. You should run a reverse proxy in front of it
so you can protect all traffic with HTTPS. Please consult your favourite search engine on how to setup a reverse proxy. 
We recommend that you use nginx with let's encrypt.
* MemberMatters is designed to run on site if you have any door, interlock or memberbucks devices. However, some parts
need reliable networking and internet to function. Please keep this in mind and make sure you perform thorough
testing before relying on it.


### Updating your instance
Docker containers are meant to be disposable, so you'll need to delete it and make a fresh one from the latest image. 
We suggest writing a bash script like the one below:

```bash
echo "checking for new docker image"
docker pull jaimynmayer/membermatters
echo "Stopping the docker container"
docker stop membermatters
echo "Removing the old docker container"
docker rm membermatters
echo "Creating new docker container"
docker create -p 8000:8000 --name membermatters --restart always --detach --env-file /usr/app/env.list -v /usr/app/:/usr/src/data jaimynmayer/membermatters
echo "Running new docker container"
docker start membermatters
``` 

### Customisation
The primary way to customise MemberMatters is via the database settings. Once your instance is up and running, 
navigate to `http://<instance_url>/admin` and login with an admin account. Then click on "Config" under "Constance". 
On this page you'll see a variety of settings. You should customise these settings with your own details.

A summary of the most important settings is included below with the default in brackets:

`EMAIL_SYSADMIN` (`example@example.com`) - The default sysadmin email that should receive errors etc.

`EMAIL_ADMIN` (`example@example.com`) - The default admin email that should receive administrative notifications.

`EMAIL_DEFAULT_FROM` (`"MemberMatters Portal" <example@example.org>`) - The default email that outbound messages are sent from.

`SITE_MAIL_ADDRESS` (`123 Example St, Nowhere`) - This address is used in the footer of all emails for anti spam.

`SITE_NAME` (`MemberMatters Portal`) - The title shown at the top of the page and as the tab title.

`SITE_OWNER` (`MemberMatters`) - The name of the legal entity/association/club that is running this site.

`ENTITY_TYPE` (`Association`) - This is the type of group you are such as an association, club, etc.

`SITE_URL` (`https://membermatters.org`) - The publicly accessible URL of your MemberMatters instance.

`INDUCTION_URL` (`https://eventbrite.com.au`) - The URL members should visit to book in for a site induction.

`MEMBERBUCKS_NAME` (`Memberbucks`) - You can customise the name of the portals currency.

`GROUP_NAME` (`Group`) - You can customise what the portal calls a group.

`ADMIN_NAME` (`Administrators`) - You can specify a different name for your admin group like exec or leaders

#### Home Page and Welcome Email Cards
The settings called "HOME_PAGE_CARDS" and "WELCOME_EMAIL_CARDS" control the content that is displayed on the 
MemberMatters home page, and the content in the welcome email each user receives when they are converted to a member.
These options are configured with a JSON object specifying the content. You can add as many cards as you want, but we
recommend 6 as a maximum for the homepage, and 4 for the email. You can find the icon names on 
[this page](https://materializecss.com/icons.html). Absolute and relative URLs are supported.

An example with 3 cards is below:
```json
[{
	"title": "HSBNE Wiki",
	"description": "Our wiki is like the rule book for HSBNE. It contains all the information about our tools, processes and other helpful tips.",
	"icon": "class",
	"url": "https://wiki.hsbne.org",
	"btn_text": "Read Wiki"
},
{
	"title": "Trello",
	"description": "We use Trello for task management. If you want to help out around the space check out Trello for stuff to fix and improve.",
	"icon": "view_list",
	"url": "https://trello.com/b/xxxxxxx/inbox",
	"btn_text": "Visit Trello"
},
{
	"title": "Report Issue",
	"description": "Found something broken at HSBNE that you don't have the time or skills to fix? You can submit an issue report.",
	"icon": "bug_report",
	"url": "/issue/report/",
	"btn_text": "Report Issue"
}]
```
