
# issues 

## Dec.19 2020
### UI 

- [ ] The editor is locked for users by default. But when the lock is on, there is no indication except inputted words are not showing on the screen. 

- [ ] CSS should be rewrite for the articles and the whole site. The fonts should be unified. The dark mode should be supported if the time is enough. _A guideline will be put into a different markdown file._

- [ ] Modify the default CSS for Cytoscape. The global CSS for graphs should be added when the graphs are loaded instead of when the data is processed. _The guideline for Cytoscape CSS will also be put into a different markdown file._

- [ ] There should be a custom CSS for the variable list. More information are listed in the functionality section. 

### Improvements

- [ ] The code for the step controller should be tested. There are still some minor errors when dealing with edge cases. 

- [ ] Create an API for user server (the snooper) and the front end. The stepper works OK right now but some work should be done to make the experience of variable list better. It's are to see the variable names and variable detail right now. The user server should follow the API when sending information to the frontend. The frontend should have a tokenizer that interprets the information sent from the backend. 

- [ ] (Optional) The variable list can be popped up. 

- [ ] Wrap user server with docker and setup a portal environment. 

- [ ] Add name to code snippets. 

- [ ] Add "run all code snippets" in the code list on the admin panel. 

- [ ] (Optional) Create editing lock so that no two people can edit on the same info on the admin panel. 

- [ ] Implement auto run in the step controller. 

- [ ] Implement tooltips on graph elements to show their properties. (Fix #60). The tooltips should go away when any operation is taken on the Cytoscape. Also, there should be a disable showing graph tooltip option on the control strip. 

- [ ] Unify the server error response. _This will be another document._ 

- [ ] Add i18n to the error response. 

- [ ] Change language when the accept-language is used in the request header. (I am not sure if the frontend can read the request header. This might not be possible without SSR). 

- [ ] (Optional) Migrate to Quasar app and build PWA. 

- [ ] More translations. 
### Bugs 

- [ ] The images on the admin panel cannot be displayed. 

- [ ] The code editor on the admin panel sometimes respond "null event listener". 

- [ ] Fix the unsaved change notification always showing up in the admin panel. Probably by adding a wrapper function and all changes go through the wrapper. 

- [ ] Fix the tutorial layout overflow bug. 

- [ ] Fix the to the top button. 

### Features 