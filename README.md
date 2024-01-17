# MemberMatters

MemberMatters is an open source membership, billing and access control solution for makerspaces and community groups.

### Main Features

* Supports all major browsers with mobile support and dark mode.
* Kiosk mode (electron) with site sign/sign out feature to restrict access to tools.
* Member registration system (signup, login, profile etc).
* Recurring membership payments via credit card with Stripe including:
  * Integration with Canvas or Moodle for a mandatory online induction course during sign up.
  * Support for manual account activation/deactivations for members without a Stripe subscription.
  * Self service billing (ie members can cancel their membership or update credit card themselves).
  * Automatic swipe card deactivation on overdue payments.
  * Automatic swipe card activation for returning members.
* Single Sign On (SSO) provider with support for both OIDC and the discourse protocol.
* Issue reporting form with Trello integration.
* Access Control system built in including:
  * Access permissions checking screen for members.
  * Default access permissions for new members.
  * Audit logs (including interlock time used and posts to Discord) for every successful/failed swipe.
  * Integration with our Access Control firmware which supports:
    * Communication over websockets for flexibility in placement (your MM server can be offsite!).
    * Offline cache that is updated automatically in realtime as permissions change.
    * Remote unlocking, syncing and rebooting of devices.
    * Controlling access to most types of doors and tools.
    * Memberbucks purchases via RFID and integration with some vending machines (MDB support coming soon).
* Integration with Sendgrid/Postmark for emails and Twilio for SMS notifications including:
  * SMS and email alerts for swipe card deactivation/failed swipes etc.
  * Manual SMS notifications to members for urgent issues (they can take a while to check emails)
* Admin Interface for managing all aspects of the system (and Django admin fills in the gaps).
* Show members Webcam snapshots, latest swipes, who's on site, and other member tools.
* Full "Memberbucks" Support for on site and in-portal payments.
* And many more! Feel free to open an issue or discussion if you see anything missing or want to suggest new features.

## Getting Started

See the [getting started](/docs/GETTING_STARTED.md) instructions for how to run the MemberMatters software for your organisation. Once you've finished installing MemberMatters, your should read the [post installation steps](/docs/POST_INSTALL_STEPS.md) for important instructions on setting up and configuring your instance.

MemberMatters is production quality software and has been used by several makerspaces for over 5 years. However, as an open source project, we focus our limited resources on features and bug fixes so our documentation can always be improved. Please open an issue if you have any suggestions to make it better.

### Compatibility

Officially, the only supported way to run MemberMatters is with the official Docker Hub image on a Ubuntu Server LTS host. Being Docker, you should be able to run it on various other platforms, but minimal support will be available. There is both an AMD64 and ARM64 build on Dockerhub for each release.

## Updates and Releases

The official changelog is available on the website [here](/CHANGELOG.md). You will also find each release [here](https://github.com/membermatters/MemberMatters/releases) on GitHub.

## Door, Interlock & Vending Machine Hardware

As part of our access control system (including doors, tool interlocks & vending machine payments) @jabelone has developed a "mainboard" PCB and firmware that is compatible with MemberMatters. The second iteration of this PCB has proven quite reliable over the last ~2yrs, despite a handful of hardware bugs. This PCB will be published eventually as the "standard" access control hardware for use with MemberMatters once (if) this design reaches production ready quality. It will not be published before this to prevent issues/disappointment/support requests.

However, our Access Control Firmware should run on most ESP32 devices. It is also compatible with many off the shelf dev boards and peripherals including UART and Wiegand RFID readers, 16x2 i2c LCD screens, etc. To use this firmware, connect a compatible RFID reader, some sort of output (contactor for a tool interlock, electronic door strike, vend relay etc.) and configure it to connect to your MemberMatters instance. Once connected, you can authorise it and use it within MemberMatters.

You can read more about how to use the firmware in it's repo at [MemberMatters Access Control Firmware](https://github.com/membermatters/mainboard-firmware).

## Screenshots

### Mobile

<img src="screenshots/m1.png" width="200"> <img src="screenshots/m2.png" width="200"> <img src="screenshots/m3.png" width="200"> <img src="screenshots/m4.png" width="200"> <img src="screenshots/m5.png" width="200">

### Desktop

<img src="screenshots/1.png" width="500"> <img src="screenshots/2.png" width="500"> <img src="screenshots/3.png" width="500"> <img src="screenshots/4.png" width="500"> <img src="screenshots/5.png" width="500">

### Desktop (Dark Mode)

<img src="screenshots/d1.png" width="500"> <img src="screenshots/d2.png" width="500"> <img src="screenshots/d3.png" width="500">

See the [screenshots](screenshots) folder for more screenshots.

# Developers Information

## Getting Started
[![Build Docker Image (Prod)](https://github.com/membermatters/MemberMatters/actions/workflows/build_docker.yml/badge.svg?branch=main)](https://github.com/membermatters/MemberMatters/actions/workflows/build_docker.yml)

[![Build Docker Image (Dev Branch)](https://github.com/membermatters/MemberMatters/actions/workflows/build_docker.dev.yml/badge.svg)](https://github.com/membermatters/MemberMatters/actions/workflows/build_docker.dev.yml)


### Pre-Commit Hooks

We use husky and lint-staged to manage pre commit hooks. The first thing you should do is run `npm install` in this
directory. This installs and configures the pre commit hooks automatically. After doing this, you should see them run
when you try to commit a file (for example, with `git commit -m "update thing"`).

### Development tip (dev server proxy)

The Vue.js (Quasar) frontend and Django backend run different dev servers on different ports. Due to
this you will run into issues with sharing cookies etc across the different URIs. To get around
this, the webpack dev server has been setup to proxy all requests to `/api` to `localhost:8000` so
you'll need to make sure the django dev server is running there.

### Vue.js JavaScript frontend

Please see the [readme](src-frontend/README.md) file inside the `src-frontend` folder. This folder contains all of the source
code and other assets needed by the frontend.

### Django Python backend

Please see the [readme](memberportal/README.md) file inside the `memberportal` folder. This folder contains all of the source
code and other assets needed by the backend.

## Contributing guidelines

By contributing code, or any other resource to this repository, you agree to license it
under the open source MIT license. Please use good coding practices, comment
your code well and ensure compliance with any code formatting or linting that's in place. Also
avoid "weird tricks" and optimisations that don't read easily - this is a web app, not a high
performance algorithm. Your contributions *will* be rejected if you do not follow these guidelines so please be careful.

All PRs should be made from your own branch/fork into the `dev` branch. Every now and again we'll collect the changes in dev, do up a release, and push to `main`. The `main` branch should always contain the most recent release.

## Release Checklist

We use [semantic versioning](https://semver.org).

* Update package.json version.
* Update src-frontend/package.json version.
* Update CHANGELOG.md with all changes since the last version.
* Make a new commit with above changes and commit title in the format of e.g. `v3.4.5`.
* Once this is merged into the `main` branch, tag the merge commit with the same name and GHA will build/deploy the docker image.
* Create a [new release on GitHub](https://github.com/membermatters/MemberMatters/releases/new)
  * Choose the tag you just created.
  * For the title use the version number as above e.g. `v3.4.5`.
  * For the description use the new entries added to the changelog.
* Close out any issues fixed by this release (preferably after confirming that it fixes it).

# Organisations using MemberMatters

Feel free to add your organisation to this list (via a pull request) if you're actively using or trialling MemberMatters. Make sure to include a link to your website and the date you added it.

* [BMS (Brisbane Makerspace)](https://brisbanemaker.space) (October 2021) - Brisbane's friendliest community workshop based in Brisbane, QLD, Australia.
* [Make Monmouth](https://www.makemonmouth.co.uk/) (November 2023) - A community makerspace based in Monmouth, Wales, UK.
* [SparkCC](https://www.sparkcc.org) (September 2021) - A community of makers on the NSW Central Coast based in Palmdale, NSW, Australia.
