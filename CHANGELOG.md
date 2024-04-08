# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [v3.6.3] - 2024-04-08

### Fixed

- SpaceAPI return type for sensor values fixed (thanks @rechner)

## [v3.6.2] - 2024-02-02

### Fixed

- SpaceAPI return type for version number (thanks @rechner)

### Added

- New OIDC scope called `membershipinfo` and extra claims
- New GitHub Actions for checks and docker build on every PR

### Changed

- Cleaned up some old code/models
- Tidied up redundant staff/admin attributes

## [v3.6.1] - 2024-01-20

### Fixed

- Menulink translation bug

## [v3.6.0] - 2024-01-17

### Added

- SMS logging
- Send SMS notification to member feature

### Changed

- Some of the Django log_types options to be more brief/consistent
- Some of the GHA workflows to be more consistent
- The main readme to be more up to date/accurate

### Fixed

- #232 email sending bug (thanks @snoopen)
- Email template rendering bug with footer (thanks @snoopen)

## [v3.5.0] - 2024-01-06

### Removed

- Some unused Django constance settings
- Logged in route guard from webcams page so it's properly public
- All old interlock code from the http api days

### Added

- Moodle support / integration for onboarding induction as part of signup flow
- Proper api key support for various api endpoints with djangorestframework-api-key
- Auto commission new `AccessControlledDevice`s
- Manual device sync, reboot, bump buttons
- Support for websocket interlocks
- Support for vending machine debits via websocket
- Dynamic SpaceAPI endpoint based on new models (thanks @proffalken)
- More detailed email logging
- More detailed access system logging
- Device level loggins for connections, disconnections and authentications etc.
- Member is cancelling email notifications / logging
- Support for Google Analytics GA4 tags / google tag manager
- First subscribed date
- Auto refresh on devices page

### Changed

- Overhauled / refactored email system to be more reliable/reusable
- Member signing back up copy makes more sense
- Disconnect websockets if any packet received before auth packet
- Refactored swipe stats to use Django ORM rather than raw queries
- Optimised some queries to make some pages load faster
- All tab-based UIs to be more consistent
- Update MM users

### Fixed

- Some duplicated/strange translation strings
- Spaceapi constance fields updated to use floats for location lat/lng (thanks @proffalken)
- Card last 4 digits not showing on manage member screen
- Edge case that allowed some people to complete signup without subscription
- Order of logs displayed on admin pages to start with most recent
- A bug when members last seen is empty
- Member created date not visible in Django admin
- Various display bugs in manage member screen
- Some admin pages not showing useful names for entities
- Stripe webhook returning error if user has access to an interlock without a serial number
- Canvas not syncing due to another API change
- Fixed 404 in docs (thanks @plex3r)

## [v3.4.1] - 2023-09-01

### Added

- allow dev tools in prod builds of electron

### Changed

- refactored user logging and email system

### Fixed

- electron build failing
- electron build to handle SameSite attribute on session cookie

## [v3.4.0] - 2023-08-31

### Removed

- raw sql queries and replaced with Django ORM
- automatic loading of fixtures on first run
- db migrations that refer to now non-existent app

### Added

- oauth2 / openid connect (provider) support for SSO
- automatic door/interlock syncing on access changes
- access system status endpoint
- list of links as option for homepage cards
- added dedicated web socket sync/reboot commands
- option to enable discord swipe only on certain doors/interlocks
- automatically sync all rfid card changes to devices
- maintenance lockouts to devices
- flag to opt out accounts from email export
- check for invalid webcam/homepage cards config
- copy to clipboard feature for email export
- types for member objects
- support for postgres database backend

### Changed

- changed all environment variables to start with MM\_
- refactored web socket code
- refactored frontend code and moved to src-frontend folder
- moved to vite and added polyfills etc.
- login page to add background gradient and logo
- migrated lots of frontend code to typescript
- MM logo
- screenshots in docs folder
- updated dockerfile to node 18
- improved robustness of postmark integration
- increased size limit of some title/description fields
- caprover deployment example
- some API routes to be more consistent layout
- Dockerfile NGINX proxy_pass setup to work behind a second reverse proxy

### Fixed

- error messages for successful actions
- discord swipe log url
- manage member subscription data display
- reset access permissions for each member when “all_members” option is toggled off/on
- hide device from members feature
- homepage/welcome email cards and webcam examples
- missing translation strings
- minor bugs in manage member page
- GitHub actions
- dayjs imports
- registration requiring vehicle registration plate (should be optional)
- signals running in raw mode (ie when data importing)
- some frontend URLs in API requests (405 method not allowed errors)

## [v3.3.0] - 2022-10-10

### Added

- Door bump API for unlocking doors from a 3rd party system
- better webcam cache busting logic and documentation to configure webcams
- option to collect vehicle registration "rego" plates on a member's profile

### Fixed

- Don't initialise twilio if not enabled (thanks @rechner)

## [v3.2.0] - 2022-09-05

### Added

- Enable/disable Canvas induction via constance option
- Support memberbucks without Stripe enabled
- Support for a site wide currency format via the SITE_LOCALE_CURRENCY option
- NZD, USD, and EUR currency locale formats

### Fixed

- Allow signup to succeed if access card requirement is true (commit #cb32009ef08ce21704231f577d61e50250f46463)

## [v3.1.0] - 2022-08-29

### Added

- Twilio integration for sending SMS alerts to members
- Version to config endpoint for easier debugging
- Basic celery setup (and container start script)
- Prometheus endpoint
- Locale detection and support for GBP currency

### Changed

- Split constance config into separate module
- Specified member's email as reply-to in issue card
- Bumped deps by github security bot

### Fixed

- Bug with database fixtures preventing fixtures from loading

## [v3.0.0] - 2022-05-27

### Removed

- All Xero support
- Legacy http API for door controllers
- Member Types (for use with Xero)
- Sentry (temporarily)
- Unnecessary environment variables

### Added

- Websocket API for access control devices (ping/pong, authorise, sync tags, log access, update device ip)
- Django pwned passwords
- Loading spinner while app / login page is loading
- Empty state to access permissions page
- Empty state to admin members list
- Some missing translation strings that were hardcoded in the app
- Redis support for Django channels
- Log failed door swipes to the database too
- User event, door and interlock logs to manage member screen

### Changed

- Upgraded to Vue 3, Qusar 2, all frontend dependencies updated
- Bumped backend dependencies
- Messaging around membership plan / payment plans to make it more clear
- References to "donate" to "make payment" as an exchange of money for goods/services is _not_ a donation
- Tidied up manage member UI and made it cleaner
- Export mailing list translation to make it clearer

### Fixed

- Logging so it's actually useful now that we've moved to daphne
- Redirect on loging sometimes getting stuck
- Some forms not saving after modification
- Bug where member tier/plan translation string was not showing properly sometimes
- made manage member/tier page always go back one level
- History router mode broke in some cases
- Missing short name getter causing warnings logged
- Redirect to original URL if user is not logged in (after login)
- Some UI bugs in the billing workflow
- Minor UI bug with side menu border / scrolling
- Double filter dropdown showing on mobile manage members page
- UI issues with tiers list
- Loading states for door unlock/reboot buttons
- Typo in first joined date on digital ID
- Door checkin via websocket overriding door object in database
-

## [v2.8.0] - 2021-10-20

### Removed

- Sendgrid integration for email sending

### Added

- Postmark integration for email sending
- Mailchimp integration

### Changed

- Made site sign in/users on site feature optional
- Made Dockerfile more development friendly (at expensive of slightly larger images)

### Fixed

- Inconsistent login bug on some browsers and iOS
- Not quite mobile friendly sign up page
- CSS and layout of membership plan/pricing pages

## [v2.7.0] - 2021-10-20

### Added

- Feature flag system
- Most optional features to feature flags
- Option for collecting access card instead of inputting it
- A site banner feature
- Generate Xero invoices on stripe invoice payments
- Xero configuration options to database config

### Fixed

- Canvas randomly failing to sync user induction progress (canvas have started including a random null user for some reason)
- Canvas api failure logic
- Sentry error logging
- Bug with canvas email being case sensitive
- Stripe invoice payment logic improvement
- Password reset bug
- Logout bug on mobile devices
- Sentry sdk old version causing issues
- Behaviour around Stripe subscription signups when they fail the first time
- Javascript floating point conversion error when making payment plan with decimal value
- Subscription status is not displayed correctly in member list
- Excessively wide credit card form during signup

### Removed

- Groups feature

### Deprecated

- Access device HTTP endpoints. In a future release the current HTTP endpoints for access control devices will be removed and replaced with the new websocket protocol.

## [v2.6.3] - 2021-09-27

### Fixed

- Enable stripe billing menu visibility race condition
- Sentry / stripe token race condition
- Removed excess console logging
- Django admin static css was excluded from docker image
- Handled incomplete subscription with error message
- Various minor bug fixes
- Unhandled error breaks admin UI when member subscription doesn't exist
- Date display issue on proxy form

### Changed

- Replaced momentjs with dayjs

### Added

- Caprover example template
- Basic read the docs website
- Build docker image GitHub action

## [v2.6.2] - 2021-09-06

### Fixed

- Can't override existing card during signup
- Occasional constance settings reset to default value

### Added

- Member billing and subscription info on admin page
- Support for sentry error logging

### Changed

- Upgraded base docker image to Alpine 3.14

## [v2.6.1] - 2021-07-11

### Fixed

- Fixed checking induction requirements being skipped during signup
- Added max width to credit card component
- Prevent clicking next during signup if saved card doesn’t exist
- Fixed various missing/wrong translations
- Added send grid not configured error to payment card component
- Added stripe not configured error to member bucks and manage billing components
- Fixed add payment plan not closing/resetting correctly
- Updated python dependencies
- Fixed Django warning by specifying explicit ID field in models

## [v2.6.0] - 2021-07-08

### Changed

- More work on usage statistics

### Fixed

- new signups not receiving induction email
- site sign in info box accent colour
- fixed i18n display issue on plan confirmation page
- improved reliability of stripe subscription creation with some new retry logic
- Various minor bug fixes to the strip subscription flow

## [v2.5.0] - 2021-05-13

### Added

- basic usage stats on each door/interlock
- more documentation on how to run linting checks manually
- configuration files for eslint github action and lint-staged/husky
- configuration and documentation for setting up MM on AWS with terraform/copilot

### Changed

- moved from font awesome to material design icons
- combined doors/interlocks into devices page
- updated some python dependencies

### Fixed

- Plan/Tier card interval string error

## [v2.4.2] - 2021-04-26

### Fixed

- some users can't login (SPA build mode trying to use JWTs)

## [v2.4.1] - 2021-04-20

### Fixed

- fixed short login sessions on iOS (jwt refresh logic)

## [v2.4.0] - 2021-04-17

### Added

- self site sign out feature (members can sign out from site using the portal)
- new warning and info banners throughout the site for inactive or account only profiles

### Fixed

- broken reset password functionality
- member tools link disappearing
- make member button bug with account only profiles
- manage member page doesn't refresh after changes

## [v2.3.2] - 2021-04-13

### Added

- auto login after email verification

### Fixed

- broken signup flow caused by renaming noobs to needs inductions
- fixed several bugs related to above

## [v2.3.1] - 2021-04-08

### Added

- ios version update script
- android capacitor build mode

### Fixed

- made capacitor build mode check if logged in before hiding splashscreen
- sending members to stripe flow if stripe flow is not enabled
- themeing on capacitor build mode

## [v2.3.0] - 2021-03-24

### Added

- better documentation for kiosk building

### Changed

- fixed linting on some files
- refactored all remaining (except for door/interlock controller endpoints) endpoints to use DRF in preparation for mobile app support
- Changed capacitor scheme and changed iOS build target to 13.0

### Fixed

- fixed typo on doors/interlocks page
- fixed some plurarls in django admin

## [v2.2.1] - 2021-03-06

### Added

- 𝔗𝔥𝔢𝔪𝔢𝔦𝔫𝔤 𝔰𝔲𝔭𝔭𝔬𝔯𝔱 🎨 (thanks @snoopen)

## [v2.2.0] - 2021-03-06

### Added

- stripe billing payments

## [v2.1.5] - 2021-03-06

### Fixed

- .dockerignore bug
- added note about nvm/ubuntu dependency

## [v2.1.4] - 2021-03-04

### Fixed

- documentation regarding font awesome icons
- free font awesome icon usage bugs

## [v2.1.3] - 2021-03-03

### Fixed

- out of date packge-lock.json
- minor dependency updates
- removed sentry configuration

## [v2.1.2] - 2021-02-26

### Added

- configurable dashboard stats card image.

### Changed

- updated default/example dashboard cards and icons.

## [v2.1.1] - 2021-02-22

### Changed

- made Dockerfile build more reliably and published armv7 image.

## [2.1.0] - 2021-02-17

### Added

- This CHANGELOG.md file!
- Google Analytics support (just specify your tracking id in the constance settings).
- Reboot and/or unlock buttons now appear on doors and interlocks.
- Implemented manage door and interlock pages.
- Screenshots of v2 to repo and added to readme.
- Initial typescript support.
- Added Alpha version of iOS app.
- Ground work (backend models, UI and endpoints) for Stripe billing.
- Python linter to GitHub actions.
- Configurable (via constance) site logo URL and sendgrid API key.
- Configurable (via constance) default member type for signups.

### Changed

- [BREAKING] reset database migrations - existing databases may need to be manually migrated across.
- Updated dockerfile to optimise for final image size. It went from ~2gb down to ~800mb.
- Split out manage member, doors and interlock components to separate page with dedicated route for easier navigation.
- Numerous UI tweaks for improvement to UI and formatting consistency.
- Upgraded to Quasar v2.
- Updated project dependencies.
- Update credit card component has been moved to a separate "Billing" page in anticipation of Stripe billing.
- Set cache header to 0 for index.html to assist with cache busting on frontend updates

### Deprecated

- Xero integration has been deprecated and will be removed in a future release once Stripe billing is stable.

### Fixed

- Typos in README.md.
- Electron-packager and other dependency conflicts.
- First run detection and fixture loading.
- Added a handful of missing translation definitions.
- Corner/border formatting with credit card component.
- <https://github.com/membermatters/MemberMatters/issues/90>
- <https://github.com/membermatters/MemberMatters/issues/91>
- <https://github.com/membermatters/MemberMatters/issues/92>
- <https://github.com/membermatters/MemberMatters/issues/93>
- <https://github.com/membermatters/MemberMatters/issues/101>

## Versions prior to v2.1.0 don't have changelog entries

- For these versions, please see the git commit history for changes.

# Template

## [vMajor.Minor.Patch] - 2021-02-17

### Added

- for new features.

### Changed

- for changes in existing functionality.

### Deprecated

- for soon-to-be removed features.

### Removed

- for now removed features.

### Fixed

- for any bug fixes.

### Security

- in case of vulnerabilities.
