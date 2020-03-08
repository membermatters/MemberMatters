# MemberMatters
MemberMatters is an open source membership and access management solution.

### Features
* Member registration system (signup, login etc)
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
* Manage recurring membership payments via Stripe
* Edit member swipe in theme

## Getting started using MemberMatters
See the [getting started](/GETTING_STARTED.md) instructions for how to run the MemberMatters software for your 
organisation.

## Getting started (developers)
### Vue.js frontend 
Please see the [readme](https://github.com/membermatters/MemberMatters/blob/master/frontend/README.md) file inside the `frontend` folder. This folder contains all of the source
code and other assets needed by the frontend.

### Django backend
Please see the [readme](https://github.com/membermatters/MemberMatters/blob/master/memberportal/README.md) file inside the `memberportal` folder. This folder contains all of the source
code and other assets needed by the backend.
 
 
## Screenshots
[ Coming soon once the frontend rewrite is done ]

### Contributing guidelines
By contributing any code, asset or any other resource to this repository to you agree to license it
under the license in use by the project (currently MIT). Please use good coding practices, comment 
your code well and ensure compliance with any code formatting or linting that's in place. Also 
avoid "weird tricks" and optimisations that don't read easily - this is a web app not a high 
performance algorithm. Your contributions *will* be rejected if you do not follow these guidelines.

### Special note
This software used to be called "hsbneportal". It was written by 
[Jaimyn (@jabelone)](https://github.com/jabelone) and used by [HSBNE](https://hsbne.org) to manage 
their membership. It has since been rewritten to be organisation agnostic so others can use it too. 
If you find references to HSBNE, HSBNE Inc, or Space. this is why. :)
