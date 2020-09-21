# About i18n support
The default "base" language is Australian English. There is only very rudimentary support for
different languages. The MemberMatters Vue.js frontend was built with i18n support to
make it easier for others to add different languages because the maintainers only speak English. :)

## To add another language
1) Copy the `en-au` folder and rename it to the correct language code for your language.
2) Modify the index.js file inside your new folder with your translations.
3) Add an entry to the `i18n/index.js` file with your new language.
4) Open a pull request to submit your changes.
