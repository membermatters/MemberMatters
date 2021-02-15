# MemberMatters
MemberMatters is an open source membership and access management solution.

### Updates
The official place for updates on the MemberMatters software is on the HSBNE Inc. forum. You can access the specific thread [here](https://forum.hsbne.org/t/membermatters-hsbne-portal-updates/3514). You will also find a changelog under each release [here](https://github.com/membermatters/MemberMatters/releases) on GitHub.

### Features
* Supports all major browser versions released within the last few years
* First class mobile support with native mobile app (capacitor)
* Kiosk mode with site sign/sign out feature (electron)
* Dark mode support with native OS detection and switching
* Member registration system (signup, login, profile etc)
* Manage recurring membership payments via Stripe
* Single Sign On (SSO) system implemented with the discourse protocol (more coming soon)
* Profile - members can update all their info in one place
* Issue reporting tool
* Access system built in
    * Activate new members & enable/disable existing members
    * Granular door and tool/machines permissions
    * API so readers/interlocks can check access
    * Swipe statistics (last seen and recent swipes)
* Member overview for admins
* Groups / Causes / Areas
* Admin Interface
* Webcam integration with Unifi Video
* Full "Memberbucks" Support
    * Debit API for vending machines etc. 
    * Members can see a transaction history (credits & debits) and current balance
    * Stripe integration
* Automatically create a xero contact and create invoice when a new person is made into a member
 
### Coming soon
* Edit member swipe in theme

### Deprecation Warning
The following features have now been deprecated and will be removed in a future release:
* Xero integration

## Getting started using MemberMatters
See the [getting started](/GETTING_STARTED.md) instructions for how to run the MemberMatters software for your 
organisation.

## Getting started (developers)
### Development tip (dev server proxy)
The Vue.js (Quasar) frontend and Django backend run different dev servers on different ports. Due to
this you will run into issues with sharing cookies etc across the different URIs. To get around 
this, the webpack dev server has been setup to proxy all requests to `/api` to `localhost:8000` so 
you'll need to make sure the django dev server is running there.

### Vue.js JavaScript frontend 
Please see the [readme](frontend/README.md) file inside the `frontend` folder. This folder contains all of the source
code and other assets needed by the frontend.

### Django Python backend
Please see the [readme](memberportal/README.md) file inside the `memberportal` folder. This folder contains all of the source
code and other assets needed by the backend.

## Door, Interlock & Vending Machine Resources
This software was developed out of HSBNE Inc (Australia's largest hackerspace!). As part of our access control system (including doors and machine interlocks) we have developed a set of standard hardware components and firmware that is compatible with MemberMatters. Below is a list of useful resources for building your own hardware using off the shelf components. Once the hardware is built and firmware flashed, you can add them to MemberMatters for a complete access system and/or billing system for physical purchases.

* [HSBNE Access Control Firmware](https://github.com/HSBNE/AccessControl) - Arduino based software that runs on ESPxx devices that are the brains of our interlocks/door controllers.
* [HSBNE Access Control Hardware BOM](https://docs.google.com/spreadsheets/d/1sQvaxc8gp7CUdddq65luUwCwQNSQK4HCsXnodN-CSEk/edit#gid=0) - A list of materials that go into our access control system hardware.
* [HSBNE Inc Access Control Wiki Page](https://wiki.hsbne.org/infrastructure/services/accesscontrol) - Information about our current and past access control hardware.
* [Vending Machine RFID Panel Firmware](https://github.com/HSBNE/VendingMachine) - Arduino based software that powers our Spacebucks enabled vending machines.
 
 
## Screenshots
### Mobile
<img src="screenshots/m1.png" width="200"> <img src="screenshots/m2.png" width="200"> <img src="screenshots/m3.png" width="200"> <img src="screenshots/m4.png" width="200"> <img src="screenshots/m5.png" width="200">

### Desktop
<img src="screenshots/1.png" width="500"> <img src="screenshots/2.png" width="500"> <img src="screenshots/3.png" width="500"> <img src="screenshots/4.png" width="500"> <img src="screenshots/5.png" width="500">

### Desktop (Dark Mode)
<img src="screenshots/d1.png" width="500"> <img src="screenshots/d2.png" width="500"> <img src="screenshots/d3.png" width="500">

See the [screenshots](screenshots) folder for more screenshots.

## Contributing guidelines
By contributing any code, asset or any other resource to this repository to you agree to license it
under the license in use by the project (currently MIT). Please use good coding practices, comment 
your code well and ensure compliance with any code formatting or linting that's in place. Also 
avoid "weird tricks" and optimisations that don't read easily - this is a web app not a high 
performance algorithm. Your contributions *will* be rejected if you do not follow these guidelines so please be careful.

## Organisations using MemberMatters
Feel free to add your organisation to this list (via a pull request) if you're actively using MemberMatters and are a not for profit or similar. Make sure to include a link to your website and the date you added it.

* [HSBNE Inc](https://hsbne.org) (January 2020) - Australia's largest makerspace based in Brisbane, QLD.
