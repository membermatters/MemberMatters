# MemberMatters Portal
The MemberMatters portal is an open source membership and access management solution.

### Features
* Member registration system (signup, login etc)
* Profile - members can update all their info in one place
    * Personal details like name, email, group membership
    * Members can see their current access restrictions
* Issue reporting tool
* Access system built in
    * Activate new members & enable/disable existing members
    * Granular door and tool/machines permissions
    * API so readers/interlocks can check access
    * Swipe statistics (last seen and recent swipes)
* Member overview for admins
    * Search for members and sort by name, status, etc
    * Change a member's profile
* Groups
    * List of all groups
    * List of members in each group and quorum
* Admin Interface
    * View, add and edit the following:
        * Groups, doors and interlocks
* Webcam integration with Unifi Video
* Full "Memberbucks" Support
    * Debit API for vending machines etc. 
    * Members can see a transaction history (credits & debits) and current balance
    * Stripe integration
        * Members can add/remove a card to their profile
        * Can charge card to add memberbucks to profile
* Automatically create a xero contact and create invoice when a new person is made into a member

 
 ### Coming Soon
 * Manage recurring membership fees via Stripe
 * Edit member swipe in theme
 
 ### Getting Started
 See the [GETTING_STARTED.md](/GETTING_STARTED.md) file in this repo
 for instructions on how to setup your development environment and run the MemberMatters software.
 
 ### Contributing Guidelines
Please use best practices while contributing. This includes writing clean code (messy/hacky 
code will be rejected) and making sure it's well commented. Try to think of the next person who comes along so use 
variable names that make sense and avoid weird tricks that not everyone will understand.

Please work on existing issues (use comments to clarify/discuss things). If you want to fix undocumented 
bugs or add new things open an issue for discussion.


## Screenshots

[Coming soon once the frontend rewrite is done]

### Special Note
This software used to be called "hsbneportal". It was written by Jaimyn (@jabelone) and used by HSBNE
to manage their membership. It has since been rewritten to be organisation agnostic so others can use it too.
If you find references to HSBNE, HSBNE Inc, or Space. this is why. :)