# HSBNE Member Portal
The HSBNE member portal is how HSBNE members manage their membership.

### Features
* Member registration system (signup, login etc)
* Profile - members can update all their info in one place
    * Personal details like name, email etc.
    * Cause membership
    * Members can see their current access restrictions
* Spacebug reporting tool (issue reporting form)
* Access system built in
    * Activate new members
    * Enable/Disable existing members
    * Doors and tools/machinery permissions
    * API so readers/interlocks can check access
    * Swipe Statistics
        * Last seen (last time a member swipes)
        * Recent swipes (last x swipes at any door/interlock)
* Member overview for executive
    * Search for members
    * Sort members by status, etc
    * Change a member's details/membership type
* Causes
    * List of all causes
    * List of members in each cause and quorum
* Admin Interface
    * View, add and edit the following:
        * Causes
        * Doors
        * Interlocks
* Space webcam integration
* Full Spacebucks Support
    * Debit API for vending machines etc. 
    * Members can see a transaction history (credits & debits)
    * Can see current balance
    * Stripe integration
        * Members can save a card to their profile
        * Can view and remove saved card info
        * Can charge card to add spacebucks
* Automatically create a xero contact when a noob is made into a member

 
 ### Coming Soon
 * Manage recurring membership fees via direct debit service
 * Manage recurring membership via xero invoices
 * Edit member swipe in theme
 
 ### Getting Started
 See the [GETTING_STARTED.md](/GETTING_STARTED.md) file in this repo
 for instructions on how to setup your development environment and run the portal software.
 
 ### Contributing Guidelines
If you're able to write python (django) or JavaScript please contribute. It's a lot of work to write something like 
this properly from scratch. Please use best practices while contributing. This includes writing clean code (messy/hacky 
code will be rejected) and making sure it's well commented. Try to think of the next person who comes along so use 
variable names that make sense and avoid weird tricks that not everyone will understand.

**HSBNE members:** Check with Jaimyn (@jabelone) before working on something, then make a pull request when you are happy with your 
changes.

**Other people:** Work on existing issues (use comments to clarify/discuss things). If you want to fix undocumented 
bugs or add new things open an issue and ask how it should be done.


## Screenshots

![screenshot](https://raw.githubusercontent.com/jabelone/hsbneportal/master/screenshots/screenshot.png)
![screenshot2](https://raw.githubusercontent.com/jabelone/hsbneportal/master/screenshots/screenshot2.png)
![screenshot3](https://raw.githubusercontent.com/jabelone/hsbneportal/master/screenshots/screenshot3.png)
![screenshot4](https://raw.githubusercontent.com/jabelone/hsbneportal/master/screenshots/screenshot4.png)
<img src="https://raw.githubusercontent.com/jabelone/hsbneportal/master/screenshots/screenshot5.png" width="400">
<img src="https://raw.githubusercontent.com/jabelone/hsbneportal/master/screenshots/screenshot6.png" width="400">
<img src="https://raw.githubusercontent.com/jabelone/hsbneportal/master/screenshots/screenshot7.png" width="300">
<img src="https://raw.githubusercontent.com/jabelone/hsbneportal/master/screenshots/screenshot8.png" width="300">
