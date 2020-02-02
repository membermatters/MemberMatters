# MemberMatters Portal
The MemberMatters portal is an open source membership and access management solution.

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
 
 ### Coming Soon
 * Manage recurring membership payments via Stripe
 * Edit member swipe in theme
 
 ### Getting Started
 See [getting started](/GETTING_STARTED.md) for instructions on how to run the MemberMatters software for your 
 organisation.
 
 See [getting started (for developers)](/GETTING_STARTED_DEV.md) for instructions on how to setup your development 
 environment for the MemberMatters software.
 
 
 ## Screenshots

[Coming soon once the frontend rewrite is done]
 
 ### Contributing Guidelines
Please use best practices while contributing. This includes writing clean code (messy/hacky 
code will be rejected) and making sure it's well commented. Try to think of the next person who comes along so use 
variable names that make sense and avoid weird tricks that not everyone will understand.

Please work on existing issues (use comments to clarify/discuss things). If you want to fix undocumented 
bugs or add new things open an issue for discussion.

Once you are happy with your changes, please open a pull request to merge them into dev. Your changes will be reviewed 
and accepted/rejected.

Note to collaborators with push permission: Do not push directly to master. You should push all changes to a feature 
branch first (`feature/<feature_name>`). When you are happy with it submit a pull request for merging into dev. The 
`mater` should only contain the latest stable release.

### Special Note
This software used to be called "hsbneportal". It was written by Jaimyn (@jabelone) and used by HSBNE
to manage their membership. It has since been rewritten to be organisation agnostic so others can use it too.
If you find references to HSBNE, HSBNE Inc, or Space. this is why. :)