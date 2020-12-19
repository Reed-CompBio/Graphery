
# issues 

## Dec.19 2020
### UI 

- [ ] The editor is locked for users by default. But when the lock is on, there is no indication except inputted words are not showing on the screen. 

- [ ] CSS should be rewrite for the articles and the whole site. The fonts should be unified. The dark mode should be supported if the time is enough. _A guideline will be put into a different markdown file._

- [ ] Modify the default CSS for Cytoscape. The global CSS for graphs should be added when the graphs are loaded instead of when the data is processed. _The guideline for Cytoscape CSS will also be put into a different markdown file._

- [ ] There should be a custom CSS for the variable list. _More information are listed in the functionality section._

### Improvements

- [ ] There must be a user manage page on the admin panel. 

- [ ] Users should be represented by the first name and last name (which can be fake of course). So new fields should be added to the register page and the admin panel. 

- [ ] The code for the step controller must be tested. There are still some minor errors when dealing with edge cases. 

- [ ] Create an API for user server (the snooper) and the front end. The stepper works OK right now but some work should be done to make the experience of variable list better. It's are to see the variable names and variable detail right now. The user server should follow the API when sending information to the frontend. The frontend should have a tokenizer that interprets the information sent from the backend. 

- [ ] IP restriction should be imposed to reduce malicious requests. The execution time should be limited to 1 second. 

- [ ] Unify the server error response. _This will be another document._ 

- [ ] Wrap user server with docker and setup a portal environment. 

- [ ] Implement reading from env for global setting variables, like for user server for example. 

- [ ] Implement tooltips on graph elements to show their properties. (Fix #60). The tooltips should go away when any operation is taken on the Cytoscape. Also, there should be a disable showing graph tooltip option on the control strip. 

- [ ] Implement auto run in the step controller. 

- [ ] Add name to code snippets. 

- [ ] Add "run all code snippets" in the code list on the admin panel. 

- [ ] Add i18n to the error response. 

- [ ] More translations. 

- [ ] Change language when the accept-language is used in the request header. (I am not sure if the frontend can read the request header. This might not be possible without SSR). 

- [ ] (Optional) Reflect changes made in the separated settings page right away. 

- [ ] (Optional) The variable list can be popped up. 

- [ ] (Optional) Migrate to Quasar app and build PWA. 

- [ ] (Optional) Create editing lock so that no two people can edit on the same info on the admin panel. 
### Bugs 

- [ ] The images on the admin panel cannot be displayed. 

- [ ] Fix the tutorial layout overflow bug. 

- [ ] Fix the to the top button. 

- [ ] Fix the unsaved change notification always showing up in the admin panel. Probably by adding a wrapper function and all changes go through the wrapper. 

- [ ] The code editor on the admin panel sometimes respond "null event listener". 

### Features 

- [ ] (Optional) Step anchor. A specific token is created during the markdown tutorial article parsing. When user clicks on it, the token will make the step control jump to a specific step. More information will be proposed in a separated document. 

- [ ] (Optional) Banner system. Website admin can post notifications, or per-article tips, etc., though banner system. 

- [ ] (Optional) Advanced searching for articles or code snippets. Chinese, for example, searching is not supported yet. 

- [ ] (Optional) Invitation system. Visitor can register only if they have the right invitation code. 
