# Post Installation Steps
Once you have completed the [Getting Started](/docs/GETTING_STARTED.md) instructions, you should complete the following steps to setup and customise your instance of MemberMatters.

## Postmark
The first step is to set up a [Postmark](https://www.postmarkapp.com) account to enable the sending of emails.  Postmark has a free trial (100 emails/mth) which should be more than enough for testing, however we recommend upgrading to a paid tier before use in production.

Currently, a valid Postmark API token is required for MemberMatters to function correctly. Emails are sent on various tasks like sign ups, MemberBucks actions etc. You will receive errors if you try to use these functions without a correctly configured Postmark API key. 

Initially when Postmark account is created in "test mode" you can only send emails to the same domain as your Member Matters domain. This domain limitation may create problems if your test account emails use a different domain.  You can add the ability to send from a specific domain to an arbitrary domains by adding a domain "sender signature" in the Postmark account.  Errors in Member Matters caused by Postmark misconfiguration can present themselves as "Sorry, we're having trouble performing that action. Please try again later." or other ambiguous messages.  Check the [Django logs](#logs) for more details on the cause of an error.

Aftert creating the [Postmark](https://www.postmarkapp.com) account see the section [Postmark (Email) Integration](#postmark-email-integration) to set the Postmark "Server API token" in the Member Matters configuration.

## Logs
The default settings for the Django logs are configured in the Docker *container* in the file /usr/src/app/memberportal/membermatters/settings.py (if you installed as suggested by the  [Getting Started](/docs/GETTING_STARTED.md) instructions). The distributed settings.py places the logs in /usr/src/logs/django.log.  If you run into problems these logs are a good first place to look.

Logs are also available via the command `docker logs membermatters` from the Docker *host*.

## Set up a reverse proxy
MemberMatters is designed to run behind some form of reverse proxy, or at the minimum, an SSL terminating CDN like Cloudflare (not recommended). You *should not ever* run MemberMatters in production without some form of HTTPS. The recommended way is with an nginx reverse proxy as explained below. Unfortunately, reverse proxy configurations are highly dependant on your specific environment, so only general guidance can be given. Please consult your favourite search engine if you have any trouble and only open a GitHub issue if you think you've found a bug or way to improve this documentation.

### Setting up an nginx reverse proxy on Ubuntu
Note that the any updated DNS records for your server will need to have propagated prior to certificate being issued. 
From your Docker *host* command line do the following:
1. You should first install nginx. On Ubuntu, you can install nginx with `sudo apt install nginx`.
2. Configure your nginx instance to proxy traffic through to the MemberMatters docker container on port `8000`.
3. A sample configuration file is included below, but you should configure this to your needs. You should create this file at `/etc/nginx/sites-available/portal.example.com`, where `portal.example.com` is the name of our domain.
```
server {
  server_name example.com;

	location / {
		proxy_set_header Host              $host;
		proxy_set_header X-Real-IP         $remote_addr;
		proxy_set_header X-Forwarded-For   $proxy_add_x_forwarded_for;
		proxy_set_header X-Forwarded-Proto $scheme;
		proxy_set_header X-Forwarded-Host  $host;
		proxy_set_header X-Forwarded-Port  $server_port;
        	proxy_set_header Upgrade           $http_upgrade;
        	proxy_set_header Connection        "upgrade";
        
		proxy_redirect off;
		proxy_pass http://localhost:8000;
	}
	listen 80 default_server;
  listen [::]:80 default_server;
}
```
4. Disable the default configuration: `sudo rm /etc/nginx/sites-enabled/default`.
5. Enable your new configuration file by running this command `sudo ln -s /etc/nginx/sites-available/portal.example.com /etc/nginx/sites-enabled/`.
6. Check the configuration that you added is valid by running this command, there should be no errors: `sudo nginx -t`.
7. Restart nginx to apply your new changes with `sudo systemctl restart nginx`.
8. Configure your firewall to allow Nginx.  For servers running UFW - Uncomplicated Firewall, the following command will work after Nginx is installed: `sudo ufw allow "Nginx Full"`
9. Note that this process does not include a configuration for HTTPS. We recommend that you use the Let's Encrypt Certbot tool as it will automatically modify your configuration to enable HTTPS and manage certificates for you. [Click here](https://certbot.eff.org/instructions) Select "Nginx" and your OS and then follow the instructions to install certbot on your system. Once installed, run certbot as per that link and follow the prompts to enable HTTPS for your system.
10. Check that you can access your instance of MemberMatters via HTTPS at the URL that you configured.

## Customisation
The primary way to customise MemberMatters is via the database settings. Once your instance is up and running,
navigate to `https://<instance_url>/admin` and login with an admin account. Then click on "Config" under "Constance".
On this page you'll see a variety of settings. You should customise these settings with your own details.

A summary of the settings is available below. Most settings have a more detailed description and an example of the format required on the settings page itself.

> NOTE: You *must* configure the POSTMARK_API_KEY setting or else you will have problems processing new signups.

### Locale / Language Configuration
MemberMatters has out of the box support for different locales (a combination of language and number/currency/date 
formatting). Currently, only the following locales are supported. If you want to add or improve support for a new locale
then please file an issue, we'd love to help make it available in your language.

MemberMatters will auto-detect the locale setting the user's browser is set to, and use that translation if available.
However, as noted below, currencies will use a hardcoded value set by a configuration option.

> NOTE: the `SITE_LOCALE_CURRENCY` option is what determines how the currency is displayed. This is "hardcoded" as a 
> config option to prevent a currency/billing amount being displayed incorrectly. If your locale isn't directly 
> supported, please open an issue or check below as your currency may already be supported under a different locale.o

> NOTE: If you want to set the *server* timezone and language, export `MM_TIME_ZONE=<your area>/<your country>` and 
> `MM_LANGAUGE_CODE=<your-language-code>` before launching the server component.  If you do not set these variables,
> the server logs will default to `Australia/Brisbane` as the timezone and `en-au` as the default language.
 
#### Locale Options
* `en-AU` - full translation available, currency format `$12.50`.
* `en-NZ` - no translation available (fall back to `en-AU`), currency format `$12.50`.
* `en-US` - no translation available (fall back to `en-AU`), currency format `$12.50`.
* `en-GB` - no translation available (fall back to `en-AU`), currency format `£12.50`.
* `en-IE` - no translation available (fall back to `en-AU`), currency format `€12.50`.

### General
  * "SITE_NAME" - Name of the website.
  * "SITE_OWNER" - Name of the organisation running this website.
  * "GOOGLE_ANALYTICS_MEASUREMENT_ID" - Enter your measurement ID to enable Google analytics. Only the new GA4 measurement IDs are supported. It should look something like G-XXXXXXXXXX.

### Signup
  * "INDUCTION_ENROL_LINK" - URL to enrol in the Canvas LMS induction course.
  * "INDUCTION_COURSE_ID" - ID of the Canvas LMS induction course (usually found in the course URL on the settings page).
  * "MAX_INDUCTION_DAYS" -  Maximum number of days since they were inducted before they require another induction. Set 
    to `0` to disable induction requirement.
  * "MIN_INDUCTION_SCORE" - The minimum score considered a "pass" for the induction course.
  * "REQUIRE_ACCESS_CARD" - Require the member to submit their RFID access card number during signup.
  * "COLLECT_VEHICLE_REGISTRATION_PLATE" - Allow the portal to collect vehicle registration plate number(s).

### Canvas Integration
  * "CANVAS_API_TOKEN" - the API token for the Canvas LMS integration.

### Postmark (Email) Integration
* "POSTMARK_API_KEY" - the "Server API token" from your [Postmark](#postmark) account. NOTE: required for basic MemberMatters functionality.

### Twilio (SMS) Integration
* `SMS_ENABLE` - Enables sending of SMS messages on some events. See below for a current list of events.
* `TWILIO_ACCOUNT_SID` - The **account SID** (_not api key SID_) to use for the twilio integration.
* `TWILIO_AUTH_TOKEN` - The **auth token** (_not an api token_) to use for the twilio integration.
* `SMS_DEFAULT_COUNTRY_CODE` - If the user's number does not start with a `+`, this default country code will be 
  prepended to it. This allows support for international numbers, while allowing local users to skip specifying one. 
* `SMS_SENDER_ID` - The sender ID (either a phone number or alpha numeric sender ID). Some countries
  support an "alpha numeric" send ID such as a business name. See [this page](https://support.twilio.com/hc/en-us/articles/223133967-Change-the-From-number-or-Sender-ID-for-Sending-SMS-Messages) for more info.
* `SMS_MESSAGES` - The SMS templates / messages to use.
* `SMS_FOOTER` - An optional footer to append to all SMS messages (such as 'from xyz org.'). Please make sure your
  organisation is identifiable and check the laws around this in your jurisdiction!

#### List of SMS events currently supported
You cannot currently enable specific events, you either get "all or nothing".
* Swipe Access Enabled
* Swipe Access Disabled
* Swipe Attempt (e.g. swiped at a door) Denied

### Contact Information
  * "EMAIL_SYSADMIN" - email address used for sysadmin related notifications.
  * "EMAIL_ADMIN" - email address used for general notifcations.
  * "EMAIL_DEFAULT_FROM" - default "from" address that emails from MM will be sent as. NOTE: must be authenticated / approved in Postmark to use.
  * "SITE_MAIL_ADDRESS" - the physical address of the organisation for inclusion in the email footer to comply with anti spam requirements.

### Discourse SSO Protocol
  * "ENABLE_DISCOURSE_SSO_PROTOCOL" - enable the SSO Discoure protocol.
  * "DISCOURSE_SSO_PROTOCOL_SECRET_KEY" - secret key for the SSO Discourse protocol.

### URLs
  * "SITE_URL" - publicly accessible URL this instance of MM is available on.
  * "MAIN_SITE_URL" - the main website of the organisation.
  * "POST_INDUCTION_URL" - where to send members after they've completed the online induction (typically used to book appointment to collect swipe card).

### Memberbucks
  * "MEMBERBUCKS_MAX_TOPUP" - a hard limit on the maxmimum amount a member can add in one go to their MemberBucks account.
  * "MEMBERBUCKS_CURRENCY" - the currency to use when processing MemberBucks top ups.

### Images
  * "SITE_LOGO" - a link to a logo for use around the site.
  * "SITE_FAVICON" - a link to a square favicon style logo for use around the site.
  * "STATS_CARD_IMAGE" - a link to an image used as the background on the dashboard's statistics card.

### Group Localisation
  * "MEMBERBUCKS_NAME" - [Deprecated]
  * "GROUP_NAME" - [Deprecated]
  * "ADMIN_NAME" - [Deprecated]
  * "WEBCAM_PAGE_URLS" - a JSON array of URLs to be used as the source for each webcam on the webcams page.
    * You should use an array of arrays like to specify the webcam snapshot title & locations like so: 
  ```
    [
    ["Main Room", "https://example.com/mainroom.jpg"],
    ["Digital Fabrication", "https://example.com/digifab.jpg"],
    ]
```
  * "HOME_PAGE_CARDS" - a JSON array of cards to be used on the hompeage (see below for more info).
  * "WELCOME_EMAIL_CARDS" - a JSON array of cards to be used in the welcome email (see below for more info).

### "Stripe Integration"
  * "STRIPE_PUBLISHABLE_KEY" - the publishable Stripe key.
  * "STRIPE_SECRET_KEY" - the secret Stripe key.
  * "STRIPE_WEBHOOK_SECRET" - the webhook secret to authenticate webhook requests are really from Stripe.
  * "ENABLE_STRIPE_MEMBERSHIP_PAYMENTS" - enable the "Membership Plan" menu page on the front end so members can sign up with the Stripe billing integration. NOTE: make sure you configure these first from the "Admin Tools" > "Membership Plans" page.
  * "STRIPE_MEMBERBUCKS_TOPUP_OPTIONS" - the options a member can see when on the MemberBucks top up page (in cents).

### Trello Integration
  * "ENABLE_TRELLO_INTEGRATION" - [Deprecated]
  * "TRELLO_API_KEY" - [Deprecated]
  * "TRELLO_API_TOKEN" - [Deprecated]
  * "TRELLO_ID_LIST" - [Deprecated]

### Space Directory
  * "ENABLE_SPACE_DIRECTORY" - enable a [space directory compliant API](https://spaceapi.io). The various configuration options in this section should be self explanatory, however there is also an [API Endpoint](/docs/SPACEDIRECTORY) to update certain fields.

### Theme Swipe Integration
  * "THEME_SWIPE_URL" - a URL to hit on each door/interlock swipe that can trigger a theme song played over your intercom system, or something else.
  * "ENABLE_THEME_SWIPE" - enable the theme song swipe webhook.

### Door Bump API
  * "ENABLE_DOOR_BUMP_API" - Enable an API endpoint that 'bumps' (temporarily unlocks) a door for third party integration.
  * "DOOR_BUMP_API_KEY" - The API key used to authenticate requests to the door bump API endpoint. MUST be set or the endpoint is automatically disabled.

To use the door bump API, you can send a `POST` request in the format below:
With Authorization header:
```
Authorization: Bearer <DOOR_BUMP_API_KEY>
...
POST /api/access/doors/DOOR_ID/bump/
```

With Query parameter:
```
POST /api/access/doors/DOOR_ID/bump/?secret=DOOR_BUMP_API_KEY
```

Where `DOOR_ID` is the ID of the door you wish to bump (can be found in the URL of the door's admin page). The request 
must be authenticated with an `Authorization` header set to the value of `DOOR_BUMP_API_KEY` or as a query parameter 
as above (NOT recommended for security).

### Discord Integration
  * "ENABLE_DISCORD_INTEGRATION" - enable the post to Discord channel feature when an interlock or door swipe is recorded.
  * "DISCORD_DOOR_WEBHOOK" - URL for the door webhook.
  * "DISCORD_INTERLOCK_WEBHOOK" - URL for the interlock webhook.
  * "DISCORD_MEMBERBUCKS_PURCHASE_WEBHOOK" - URL for the vending/product purchase webhook.

### Home Page and Welcome Email Cards

The settings called "HOME_PAGE_CARDS" and "WELCOME_EMAIL_CARDS" control the content that is displayed on the
MemberMatters home page, and the content in the welcome email each user receives when they are converted to a member.
These options are configured with a JSON object specifying the content. You can add as many cards as you want, but we
recommend 6 as a maximum for the homepage, and 4 for the email. You can find the icon names on
[this page](https://fontawesome.com/icons?d=gallery&p=1). Absolute and relative URLs, and vue routes are supported.

An example with 3 cards is below:

```json
[
  {
    "title": "Brisbane Makerspace Wiki",
    "description": "Our wiki is like the rule book for BMS. It contains all the information about our tools, processes and other helpful tips.",
    "icon": "class",
    "url": "https://bms.wiki",
    "btn_text": "Read Wiki"
  },
  {
    "title": "Member Bucks",
    "description": "If you need to make a payment for tool usage or something else, tap here.",
    "icon": "mdi-alert",
    "routerLink": {
      "name": "memberbucks"
    },
    "btn_text": "Member Bucks"
  },
  {
    "title": "Discord Server",
	"description": "Discord is an instant messaging platform that allows you to connect with other BMS members to share you skills, knowledge and projects. You can also get realtime support from staff/other members.",
	"icon": "mdi-chat",
	"links": [
		{
			"url": "https://s.bms.wiki/discord",
			"btn_text": "Join Discord",
                        "newLine": true
		},
		{
			"url": "https://s.bms.wiki/discord",
			"btn_text": "Join Discord 2"
		}
	]
  }
]
```
### OpenID Connect - Relying Party

MemberMatters can be configured to use your OIDC-enabled Identity provider.  You *must* set the following values from your Idp via their corresponding environment variables:
- OIDC_RP_CLIENT_ID (`MM_OIDC_CLIENT_ID` environment variable)
- OIDC_RP_CLIENT_SECRET (`MM_OIDC_CLIENT_SECRET`)
- OIDC_OP_AUTHORIZATION_ENDPOINT (`MM_OIDC_OP_AUTHORIZATION_ENDPOINT`)
- OIDC_OP_TOKEN_ENDPOINT (`MM_OIDC_OP_TOKEN_ENDPOINT`)
- OIDC_OP_USER_ENDPOINT (`MM_OIDC_OP_USER_ENDPOINT`)

Optionally set the following to override default functionality:
- MM_OIDC_CREATE_USER: Default value is `True`.  Set to `False` if you prefer that your MemberMatters admin create or import new users manually before the account can authenticate using OIDC
- MM_OIDC_TOKEN_EXPIRY: Default value is 3600.  Override to extend or shorten the validity window of the user's authentication token (time in seconds).

Finally, enable the `ENABLE_OIDC_RP` toggle in the Django constance config panel.  Now, when presented with the login screen a user would click "Login with OAuth" to authenticate via OIDC.
