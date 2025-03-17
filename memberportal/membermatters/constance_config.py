from collections import OrderedDict

CONSTANCE_CONFIG = {
    # General site info
    "SITE_NAME": (
        "MemberMatters Portal",
        "The title shown at the top of the page and as the tab title.",
    ),
    "SITE_OWNER": (
        "MemberMatters",
        "The name of the legal entity/association/club that is running this site.",
    ),
    "SITE_LOCALE_CURRENCY": (
        "en-AU",
        "The locale to use on the frontend JUST FOR CURRENCY. Please check "
        "https://membermatters.org/en/latest/POST_INSTALL_STEPS.html#locale-language-configuration for IMPORTANT considerations "
        "and supported locales before configuring.",
    ),
    "SITE_BANNER": (
        "",
        "A site wide banner that can display useful information. Leave empty to turn off.",
    ),
    # Email config
    "EMAIL_SYSADMIN": (
        "example@example.com",
        "The default sysadmin email that should receive technical errors etc.",
    ),
    "EMAIL_ADMIN": (
        "example@example.com",
        "The default admin email that should receive administrative notifications.",
    ),
    "EMAIL_DEFAULT_FROM": (
        '"MemberMatters Portal" <example@example.org>',
        "The default email that outbound messages are sent from.",
    ),
    "SITE_MAIL_ADDRESS": (
        "123 Example St, Nowhere",
        "This address is used in the footer of all emails for anti spam.",
    ),
    # URLs
    "SITE_URL": (
        "https://membermatters.org",
        "The publicly accessible URL of your MemberMatters instance.",
    ),
    "MAIN_SITE_URL": ("https://membermatters.org", "The URL of your main website."),
    "POST_INDUCTION_URL": (
        "https://eventbrite.com.au",
        "The URL members should visit to book in for a site induction after finishing the online induction."
        " (displayed during signup if REQUIRE_ACCESS_CARD == False)",
    ),
    # Logo and favicon
    "SITE_LOGO": (
        "https://brisbanemaker.space/wp-content/uploads/2021/10/BMS-Logo-ONLY.png",
        "Site logo (rectangular)",
    ),
    "SITE_FAVICON": (
        "https://brisbanemaker.space/wp-content/uploads/2021/10/favicon.png",
        "Site favicon (square)",
    ),
    "STATS_CARD_IMAGE": (
        "https://brisbanemaker.space/wp-content/uploads/2021/09/cool-students-studying-with-books-in-classroom-Y2DA4MC.jpg.webp",
        "Image to use for the site statistics card.",
    ),
    "MENU_BACKGROUND": (
        "",
        "[Optional] Image to use as the background in the menu. Leave blank for the default background image.",
    ),
    # Custom theme colors
    "THEME_PRIMARY": ("#278ab0", "Custom primary theme colour"),
    "THEME_TOOLBAR": ("#0461b1", "Custom toolbar theme colour"),
    "THEME_ACCENT": ("#189ab4", "Custom accent theme colour"),
    # Localisation of terminology
    "MEMBERBUCKS_NAME": (
        "Memberbucks",
        "You can customise the name of the built in currency.",
    ),
    "WEBCAM_PAGE_URLS": (
        """[["Example", "https://brisbanemaker.space/wp-content/uploads/2021/10/BMS-Logo-ONLY.png"]]""",
        "A JSON serialised array of URLs to pull webcam images from.",
    ),
    "HOME_PAGE_CARDS": (
        """[
            {
                "title": "Example Card",
                "description": "Tap below to see a calendar with all of our upcoming events and workshops.",
                "icon": "mdi-calendar-multiselect",
                "url": "https://brisbanemaker.space",
                "btn_text": "View Calendar"
            },
            {
                "title": "Example 2",
                "description": "This is an example card with an icon! And it links to another page using a Vue route!",
                "icon": "mdi-link-variant",
                "routerLink": {
                "name": "reportIssue"
                },
                "btn_text": "Go to route"
            }
           ]
        """,
        "You can specify cards that go on the home page with JSON. See https://github.com/MemberMatters/MemberMatters/blob/master/GETTING_STARTED.md.",
    ),
    "WELCOME_EMAIL_CARDS": (
        "[]",
        "Same syntax as HOME_PAGE_CARDS but icons are not used. If nothing is specified we will use HOME_PAGE_CARDS.",
    ),
    # Stripe config
    "ENABLE_STRIPE": (True, "Enable use of Stripe for payments."),
    "STRIPE_PUBLISHABLE_KEY": ("", "Set this to your Stripe PUBLIC API key."),
    "STRIPE_SECRET_KEY": ("", "Set this to your Stripe PRIVATE API key."),
    "STRIPE_WEBHOOK_SECRET": (
        "",
        "Set this to a secret value to verify that a webhook came from Stripe.",
    ),
    "STRIPE_MEMBERBUCKS_TOPUP_OPTIONS": (
        "[1000, 2000, 3000]",
        "This is a JSON array of top-up amounts in cents.",
    ),
    "ENABLE_STRIPE_MEMBERSHIP_PAYMENTS": (
        False,
        "Enable integration with stripe for membership payments.",
    ),
    # ==== Report Issue Services ====
    # Email config
    "REPORT_ISSUE_ENABLE_EMAIL": (
        True,
        "Enable the submit issue to email integration.",
    ),
    # Discord config
    "REPORT_ISSUE_ENABLE_DISCORD": (
        False,
        "Enable the submit issue to Discord integration.",
    ),
    # Vikunja config
    "REPORT_ISSUE_ENABLE_VIKUNJA": (
        False,
        "Enable the submit issue to Vikunja integration.",
    ),
    "VIKUNJA_API_URL": ("", "Set this to your Vikunja instance public URL."),
    "VIKUNJA_API_TOKEN": ("", "Set this to your Vikunja API token."),
    "VIKUNJA_DEFAULT_PROJECT_ID": (
        "",
        "Set this to the ID of your default project to create issues in.",
    ),
    "VIKUNJA_DEFAULT_LABEL_ID": (
        "",
        "[optional] Set this to the ID of your default label if you want new issues to be tagged.",
    ),
    "VIKUNJA_TEAMS": (
        '[{"name": "Members", "oidcID": "members", "description": "The default team for all members.", "isPublic": false}]',
        "A JSON array of Vikunja teams to add users to when they login via SSO. Returned as an OIDC claim with the 'vikunja_teams' scope. Check Vikunja docs for syntax.",
    ),
    # Trello config
    "REPORT_ISSUE_ENABLE_TRELLO": (
        False,
        "Enable the submit issue to trello integration.",
    ),
    "TRELLO_API_KEY": ("", "Set this to your Trello API key."),
    "TRELLO_API_TOKEN": ("", "Set this to your Trello API token."),
    "TRELLO_ID_LIST": (
        "",
        "Set this to the ID of your card list you want issue " "to go to.",
    ),
    # Space API config
    "ENABLE_SPACE_DIRECTORY": (
        False,
        "Turn on the space directory API available at /api/spacedirectory.",
    ),
    "SPACE_DIRECTORY_OPEN": (False, "Sets the open state."),
    "SPACE_DIRECTORY_MESSAGE": (
        "This is the default MemberMatters (membermatters.org) space directory message.",
        "Sets the message.",
    ),
    "SPACE_DIRECTORY_ICON_OPEN": ("", "Sets the icon shown while in the open state."),
    "SPACE_DIRECTORY_ICON_CLOSED": (
        "",
        "Sets the icon shown while in the closed state.",
    ),
    "SPACE_DIRECTORY_LOCATION_ADDRESS": (
        "123 Setme St",
        "Sets the snail mail address.",
    ),
    "SPACE_DIRECTORY_LOCATION_LAT": (0.0, "Sets the latitude."),
    "SPACE_DIRECTORY_LOCATION_LON": (0.0, "Sets the longitude."),
    "SPACE_DIRECTORY_FED_SPACENET": (False, "Sets support for spacenet."),
    "SPACE_DIRECTORY_FED_SPACESAML": (False, "Sets support for spacesaml."),
    "SPACE_DIRECTORY_FED_SPACEPHONE": (False, "Sets support for spacephone."),
    "SPACE_DIRECTORY_CAMS": (
        "[]",
        "A JSON list of strings (URLs) that webcam snapshots of the space can be found.",
    ),
    "SPACE_DIRECTORY_CONTACT_EMAIL": (
        "notset@example.com",
        "Sets the general contact email.",
    ),
    "SPACE_DIRECTORY_CONTACT_TWITTER": ("", "Sets the twitter handle."),
    "SPACE_DIRECTORY_CONTACT_FACEBOOK": ("", "Sets the Facebook page URL."),
    "SPACE_DIRECTORY_CONTACT_PHONE": (
        "",
        "Sets the general contact phone number, include country code with a leading +.",
    ),
    "SPACE_DIRECTORY_PROJECTS": (
        "[]",
        "A JSON list of strings (URLs) to project sites like wikis, GitHub, etc.",
    ),
    "ENABLE_MEMBERBUCKS": (False, "Enable the spacebucks / memberbucks functionality."),
    "MEMBERBUCKS_MAX_TOPUP": ("50", "The maximum topup allowed in dollars."),
    "MEMBERBUCKS_CURRENCY": (
        "aud",
        "The currency to charge cards in - see Stripe documentation.",
    ),
    "ENABLE_THEME_SWIPE": (
        False,
        "Enable playing a member's theme song on a card swipe.",
    ),
    "THEME_SWIPE_URL": (
        "http://10.0.1.50/playmp3.php?nickname={}",
        "The URL to send a GET request to on a swipe if enabled.",
    ),
    "ENABLE_DOOR_BUMP_API": (
        False,
        "Enable an API endpoint that 'bumps' (temporarily unlocks) a door for third party integration.",
    ),
    "ENABLE_DISCORD_INTEGRATION": (
        False,
        "Enable posting a notification to the discord channel on a card swipe.",
    ),
    "DISCORD_DOOR_WEBHOOK": (
        "https://discordapp.com/api/webhooks/<token>",
        "Discord URL to send webhook notifications to.",
    ),
    "DISCORD_INTERLOCK_WEBHOOK": (
        "https://discordapp.com/api/webhooks/<token>",
        "Discord URL to send webhook notifications to.",
    ),
    "DISCORD_MEMBERBUCKS_PURCHASE_WEBHOOK": (
        "https://discordapp.com/api/webhooks/<token>",
        "Discord URL to send webhook notifications to for vending/memberbucks purchases.",
    ),
    "DISCORD_REPORT_ISSUE_WEBHOOK": (
        "https://discordapp.com/api/webhooks/<token>",
        "Discord URL to send webhook notifications to when reporting issues.",
    ),
    "ENABLE_DISCOURSE_SSO_PROTOCOL": (
        False,
        "Enable support for the discourse SSO protocol.",
    ),
    "DISCOURSE_SSO_PROTOCOL_SECRET_KEY": (
        "",
        "Secret key for the discourse SSO protocol (if enabled).",
    ),
    "GOOGLE_ANALYTICS_MEASUREMENT_ID": (
        "",
        "Enter your measurement ID to enable Google analytics. Only the new GA4 measurement IDs are supported. It should look something like G-XXXXXXXXXX.",
    ),
    "SENTRY_DSN_FRONTEND": (
        "https://577dc95136cd402bb273d00f46c2a017@sentry.serv02.binarydigital.com.au/5/",
        "Enter a Sentry DSN to enable sentry logging of frontend errors.",
    ),
    "SENTRY_DSN_BACKEND": (
        "https://8ba460796a9a40d4ac2584e0e8dca59a@sentry.serv02.binarydigital.com.au/4",
        "Enter a Sentry DSN to enable sentry logging of backend errors.",
    ),
    "POSTMARK_API_KEY": (
        "PLEASE_CHANGE_ME",
        "The API key used to send email with Postmark.",
    ),
    # Induction
    "MOODLE_INDUCTION_ENABLED": (
        True,
        "Whether induction is performed via the Moodle platform or not. This setting overrides the Canvas settings below. If both are enabled, Moodle will be used.",
    ),
    "MOODLE_API_BASE_URL": (
        "PLEASE_CHANGE_ME",
        "The base URL for your Moodle instance without trailing slash (ie https://learn.example.com).",
    ),
    "MOODLE_API_TOKEN": (
        "PLEASE_CHANGE_ME",
        "Moodle API token.",
    ),
    "MOODLE_INDUCTION_COURSE_ID": (
        "",
        "Moodle course id for the induction.",
    ),
    "CANVAS_INDUCTION_ENABLED": (
        False,
        "Whether induction is performed via the Canvas platform or not. This setting is overriden by the Moodle settings above. If both are enabled, Moodle will be used.",
    ),
    "CANVAS_API_TOKEN": (
        "PLEASE_CHANGE_ME",
        "Canvas API token.",
    ),
    "CANVAS_INDUCTION_COURSE_ID": (
        "",
        "Canvas course id for the induction.",
    ),
    "INDUCTION_ENROL_LINK": (
        "",
        "The link that a member can use to enrol into an induction.",
    ),
    "MAX_INDUCTION_DAYS": (
        180,
        "The maximum amount of days since a member was last inducted before they have to complete another induction (0 to disable).",
    ),
    "MIN_INDUCTION_SCORE": (
        99,
        "The minimum score to consider an induction as passed (0-100).",
    ),
    "REQUIRE_ACCESS_CARD": (
        True,
        "If an access card is required to be added to a members profile before signup.",
    ),
    "COLLECT_VEHICLE_REGISTRATION_PLATE": (
        False,
        "Display a field that collects the member's vehicle registration plate on signup & in the profile page.",
    ),
    "ENABLE_PROXY_VOTING": (False, "Enables the proxy voting management feature."),
    "ENABLE_WEBCAMS": (
        False,
        "Enables a webcams page in the portal. Configure with the WEBCAM_PAGE_URLS setting.",
    ),
    "ENABLE_PORTAL_SITE_SIGN_IN": (
        False,
        "Enable if you want to allow members to sign into site via the portal.",
    ),
    "ENABLE_PORTAL_MEMBERS_ON_SITE": (
        False,
        "Enable if you want to see the members signed into site on the portal dashboard.",
    ),
    "MAILCHIMP_API_KEY": ("", "Enable Mailchimp sync by specifying an API key."),
    "MAILCHIMP_SERVER": ("", "Required if enabling the Mailchimp integration."),
    "MAILCHIMP_LIST_ID": ("", "Required if enabling the Mailchimp integration."),
    "MAILCHIMP_TAG": ("Member", "Add this tag to all members synced to mailchimp."),
    "TWILIO_ACCOUNT_SID": (
        "",
        "The account SID (not api key SID) to use for the twilio integration.",
    ),
    "TWILIO_AUTH_TOKEN": (
        "",
        "The auth token (not an api token) to use for the twilio integration.",
    ),
    "ENABLE_SLACK_INTEGRATION": (
        False,
        "Enable posting a notification to the slack channel on a card swipe.",
    ),
    "SLACK_DOOR_WEBHOOK": (
        "https://hooks.slack.com/services/T00000000/B00000000/<token>",
        "Slack URL to send webhook notifications to.",
    ),
    "SLACK_INTERLOCK_WEBHOOK": (
        "https://hooks.slack.com/services/T00000000/B00000000/<token>",
        "Slack URL to send webhook notifications to.",
    ),
    "SLACK_MEMBERBUCKS_PURCHASE_WEBHOOK": (
        "https://hooks.slack.com/services/T00000000/B00000000/<token>",
        "Slack URL to send webhook notifications to for vending/memberbucks purchases.",
    ),
    "SLACK_REPORT_ISSUE_WEBHOOK": (
        "https://hooks.slack.com/services/T00000000/B00000000/<token>",
        "Slack URL to send webhook notifications to when reporting issues.",
    ),
    "SMS_ENABLE": (
        False,
        "If SMS functionality should be enabled (please configure below).",
    ),
    "SMS_DEFAULT_COUNTRY_CODE": (
        "+61",
        "The country code to prepend to phone numbers that don't have one.",
    ),
    "SMS_SENDER_ID": (
        "",
        "The sender ID (either a phone number or alpha numeric sender ID you can send from).",
    ),
    "SMS_FOOTER": (
        "From Example Makerspace.",
        "An optional footer to append to all SMS messages (such as 'from xyz org.'",
    ),
    "SMS_MESSAGES": (
        '{"inactive_swipe": "Hi! Your swipe was just declined due to inactive membership. Please contact us if you need assistance.",             "deactivated_access": "Hi! Your site access was just turned off. Please check your email and contact us if you need assistance.",             "activated_access": "Hi! Your site access was just turned on. Please make sure you stay up to date with our policies and rules by visiting our website.",             "locked_out_swipe": "Hi! Your swipe was just declined due to a temporary maintenance lockout. Please contact us if you need assistance."}',
        "The SMS messages to send when a user attempts to swipe with an inactive card.",
    ),
    "METRICS_INTERVAL": (
        3600,
        "The interval in seconds to calculate and store application level metrics data like member count and door swipes.",
    ),
    "ENABLE_STATS_PAGE": (
        True,
        "Enable the stats page that shows member counts and other metrics.",
    ),
    "STATS_MAX_DAYS": (
        365,
        "The maximum number of days to show on the stats page.",
    ),
    "ENABLE_DOCUSEAL_INTEGRATION": (
        False,
        "Use DocuSeal to manage user agreements",
    ),
    "DOCUSEAL_API_KEY": (
        "API_KEY",
        "Your DocuSeal API key",
    ),
    "DOCUSEAL_URL": (
        "https://api.docuseal.com",
        "URL of the DocuSeal instance in use",
    ),
    "DOCUSEAL_TEMPLATE_ID": (
        1,
        "DocuSeal template ID to send as part of induction",
    ),
}

CONSTANCE_CONFIG_FIELDSETS = OrderedDict(
    [
        (
            "General",
            (
                "SITE_NAME",
                "SITE_OWNER",
                "SITE_LOCALE_CURRENCY",
                "GOOGLE_ANALYTICS_MEASUREMENT_ID",
                "SITE_BANNER",
                "METRICS_INTERVAL",
            ),
        ),
        (
            "Features",
            (
                "ENABLE_WEBCAMS",
                "ENABLE_PROXY_VOTING",
                "ENABLE_STRIPE",
                "ENABLE_STRIPE_MEMBERSHIP_PAYMENTS",
                "ENABLE_MEMBERBUCKS",
                "ENABLE_DISCOURSE_SSO_PROTOCOL",
                "ENABLE_DISCORD_INTEGRATION",
                "ENABLE_SLACK_INTEGRATION",
                "ENABLE_SPACE_DIRECTORY",
                "ENABLE_THEME_SWIPE",
                "ENABLE_PORTAL_SITE_SIGN_IN",
                "ENABLE_PORTAL_MEMBERS_ON_SITE",
                "ENABLE_DOOR_BUMP_API",
            ),
        ),
        ("Stats Settings", ("ENABLE_STATS_PAGE", "STATS_MAX_DAYS")),
        (
            "Sentry Error Reporting",
            (
                "SENTRY_DSN_FRONTEND",
                "SENTRY_DSN_BACKEND",
            ),
        ),
        (
            "Signup",
            (
                "INDUCTION_ENROL_LINK",
                "MAX_INDUCTION_DAYS",
                "MIN_INDUCTION_SCORE",
                "REQUIRE_ACCESS_CARD",
                "COLLECT_VEHICLE_REGISTRATION_PLATE",
            ),
        ),
        (
            "Moodle (LMS) Integration",
            (
                "MOODLE_INDUCTION_ENABLED",
                "MOODLE_API_TOKEN",
                "MOODLE_API_BASE_URL",
                "MOODLE_INDUCTION_COURSE_ID",
            ),
        ),
        (
            "Canvas (LMS) Integration",
            (
                "CANVAS_INDUCTION_ENABLED",
                "CANVAS_API_TOKEN",
                "CANVAS_INDUCTION_COURSE_ID",
            ),
        ),
        ("Postmark (EMAIL) Integration", ("POSTMARK_API_KEY",)),
        (
            "Twilio (SMS) Integration",
            (
                "SMS_ENABLE",
                "TWILIO_ACCOUNT_SID",
                "TWILIO_AUTH_TOKEN",
                "TWILIO_AUTH_TOKEN",
                "SMS_DEFAULT_COUNTRY_CODE",
                "SMS_SENDER_ID",
                "SMS_MESSAGES",
                "SMS_FOOTER",
            ),
        ),
        (
            "Stripe (PAYMENT GATEWAY) Integration",
            (
                "STRIPE_PUBLISHABLE_KEY",
                "STRIPE_SECRET_KEY",
                "STRIPE_WEBHOOK_SECRET",
                "STRIPE_MEMBERBUCKS_TOPUP_OPTIONS",
                "MEMBERBUCKS_CURRENCY",
            ),
        ),
        (
            "Report Issue Services",
            (
                "REPORT_ISSUE_ENABLE_EMAIL",
                "REPORT_ISSUE_ENABLE_DISCORD",
                "REPORT_ISSUE_ENABLE_VIKUNJA",
                "REPORT_ISSUE_ENABLE_TRELLO",
            ),
        ),
        (
            "Vikunja Integration",
            (
                "VIKUNJA_TEAMS",
                "VIKUNJA_API_URL",
                "VIKUNJA_API_TOKEN",
                "VIKUNJA_DEFAULT_PROJECT_ID",
                "VIKUNJA_DEFAULT_LABEL_ID",
            ),
        ),
        (
            "Trello Integration",
            (
                "TRELLO_API_KEY",
                "TRELLO_API_TOKEN",
                "TRELLO_ID_LIST",
            ),
        ),
        (
            "Mailchimp (EMAIL MARKETING)",
            (
                "MAILCHIMP_API_KEY",
                "MAILCHIMP_SERVER",
                "MAILCHIMP_LIST_ID",
                "MAILCHIMP_TAG",
            ),
        ),
        ("Theme Swipe Integration", ("THEME_SWIPE_URL",)),
        (
            "Contact Information",
            (
                "EMAIL_SYSADMIN",
                "EMAIL_ADMIN",
                "EMAIL_DEFAULT_FROM",
                "SITE_MAIL_ADDRESS",
            ),
        ),
        (
            "Discourse SSO Protocol",
            ("DISCOURSE_SSO_PROTOCOL_SECRET_KEY",),
        ),
        ("URLs", ("SITE_URL", "MAIN_SITE_URL", "POST_INDUCTION_URL")),
        ("Memberbucks", ("MEMBERBUCKS_MAX_TOPUP",)),
        (
            "Images",
            ("SITE_LOGO", "SITE_FAVICON", "STATS_CARD_IMAGE", "MENU_BACKGROUND"),
        ),
        ("Theme", ("THEME_PRIMARY", "THEME_TOOLBAR", "THEME_ACCENT")),
        (
            "Group Localisation",
            (
                "MEMBERBUCKS_NAME",
                "WEBCAM_PAGE_URLS",
                "HOME_PAGE_CARDS",
                "WELCOME_EMAIL_CARDS",
            ),
        ),
        (
            "Space Directory",
            (
                "SPACE_DIRECTORY_OPEN",
                "SPACE_DIRECTORY_MESSAGE",
                "SPACE_DIRECTORY_ICON_OPEN",
                "SPACE_DIRECTORY_ICON_CLOSED",
                "SPACE_DIRECTORY_LOCATION_ADDRESS",
                "SPACE_DIRECTORY_LOCATION_LAT",
                "SPACE_DIRECTORY_LOCATION_LON",
                "SPACE_DIRECTORY_FED_SPACENET",
                "SPACE_DIRECTORY_FED_SPACESAML",
                "SPACE_DIRECTORY_CAMS",
                "SPACE_DIRECTORY_CONTACT_EMAIL",
                "SPACE_DIRECTORY_FED_SPACEPHONE",
                "SPACE_DIRECTORY_CONTACT_TWITTER",
                "SPACE_DIRECTORY_CONTACT_FACEBOOK",
                "SPACE_DIRECTORY_CONTACT_PHONE",
                "SPACE_DIRECTORY_PROJECTS",
            ),
        ),
        (
            "Discord Integration",
            (
                "DISCORD_DOOR_WEBHOOK",
                "DISCORD_INTERLOCK_WEBHOOK",
                "DISCORD_MEMBERBUCKS_PURCHASE_WEBHOOK",
                "DISCORD_REPORT_ISSUE_WEBHOOK",
            ),
        ),
        (
            "DocuSeal Integration",
            (
                "ENABLE_DOCUSEAL_INTEGRATION",
                "DOCUSEAL_URL",
                "DOCUSEAL_API_KEY",
                "DOCUSEAL_TEMPLATE_ID",
            ),
        ),
        (
            "Slack Integration",
            (
                "SLACK_DOOR_WEBHOOK",
                "SLACK_INTERLOCK_WEBHOOK",
                "SLACK_MEMBERBUCKS_PURCHASE_WEBHOOK",
                "SLACK_REPORT_ISSUE_WEBHOOK",
            ),
        ),
    ]
)
