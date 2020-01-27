 ### Getting Started
 This documentation is in progress and is missing some sections so please read with caution.
 MemberMatters runs in a docker container and is designed to be easy to deploy and customise.
 
 > Note: MemberMatters only supports running in Docker on Linux. Installing Docker is outside the scope of this guide, 
>please consult your favourite search engine for tips.
 
 To get started, download the latest version from docker hub using the following command:
 ```bash
docker pull jabelone/membermatters
```

Once you've downloaded the docker image, you'll need to create a container:
```bash
docker create ...
```

Once your container is running, you will be able to login with the default admin account details:
```
Email: default@example.com
Password: MemberMatters!
```

The first thing you should do is change the email address and password of the default admin account. You can do that 
by navigating to `http://<instance_url>/admin/profile/user` and clicking on the user on that list.

Once you've done this, your MemberMatters instance is ready for use. Read on below for instructions on customising it.
 
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