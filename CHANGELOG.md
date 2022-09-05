# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
- References to "donate" to "make payment" as an exchange of money for goods/services is *not* a donation
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
- https://github.com/membermatters/MemberMatters/issues/90
- https://github.com/membermatters/MemberMatters/issues/91
- https://github.com/membermatters/MemberMatters/issues/92
- https://github.com/membermatters/MemberMatters/issues/93
- https://github.com/membermatters/MemberMatters/issues/101

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
