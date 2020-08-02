# Graphery

Dev: [![Build Status](https://travis-ci.com/FlickerSoul/Graphery.svg?token=iGoqjTdG7SFLHQyLfgoz&branch=dev)](https://travis-ci.com/FlickerSoul/Graphery)

Master: [![Build Status](https://travis-ci.com/FlickerSoul/Graphery.svg?token=iGoqjTdG7SFLHQyLfgoz&branch=master)](https://travis-ci.com/FlickerSoul/Graphery)

Graphery is a web-based graph algorithm tutorial that is designed for biological researchers. It is organized around the concept of a tutorial, which describes and provides code for a classic graph algorithm (Figure 1). A tutorial contains three parts: text-based content, interactive graphs, and a code editor. The editor enables users to step forward and back in the code and see changes applied to the corresponding graph. The editor also allows more programming-savvy users to edit the existing code and see their modifications applied on the graphs. Users can run code in the editor locally or in the cloud. Together, these three panels allow users to gain a deeper understanding of the algorithm described.

For each tutorial, users may select one of multiple real-world biological networks to better understand the implications of the algorithm described. These small graphs will come from from biological applications such as animal social networks, ecology food webs, molecular interaction networks, and phylogenetic trees.

Build the frontend:

```bash
cd graphery
npm i && npm run build
```

Prepare the backend: 

```bash
cd backend
pip install -r requirements.txt
# or you can user `pipenv install`
cd server 
python manage.py makemigrations
python manage.py migrate 
python manage.py runserver
```

To activate users' local server:

```bash
cd backend
python user_server.py
```
