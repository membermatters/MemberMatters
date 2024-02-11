# Moodle Integration

[Moodle](https://moodle.org/) is an open-source Virtual Learning Environment (VLE) that can either be hosted by a thrid-party or on your own infrastructure.

The great thing about having a VLE as part of your space is that you can provide your members with access to online learning courses whenever it suits them rather than having to organise everyone to be in the same place at the same time.

MemberMatters can use Moodle as part of the sign-up process to provide an induction course that all new members must take before their accounts are activated.

## How does it work?

MemberMatters has an [OAuth2](https://oauth.net/2/) server built in that allows your members to log in to many other applications using their MemberMatters username and password.

We will use this centralised authentication option to connect to Moodle and create new users in Moodle as part of the sign-up process.

Members will then be able to access Moodle and any courses that you have created via their MemberMatters credentials.

## What do I need?

Installing and configuring Moodle (other than the authentication) is out of scope of these instructions however, the [Moodle installation guide](https://docs.moodle.org/403/en/Installing_Moodle) is a good place to start.

We assume the following:

   1. You have MemberMatters installed and running in production
   2. You have a Moodle installation running in production
   3. Moodle can connect to MemberMatters
   4. MemberMatters can connect to Moodle

In order to achieve (3) and (4), you may want to host these systems on the same server, on the same network inside your space, or on the public internet.  How to secure these platforms and keep them updated is also outside the scope of these instructions.

## Setting up the platform
