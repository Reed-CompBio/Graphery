# Local Server

## Introduction 

Local server is used to generate step by step debug info for the front end. Please check out [utils](/user-manual/utils/index.html) before reading this. 

## Install 

```bash
git clone https://github.com/FlickerSoul/Graphery.git
cd Graphery/backend
```

Under this director, you can see a `bundle` folder and a `user_server.py` file. Those two will be the only thing you need. You can copy then in to a separated folder and delete the rest. 

## Usage 

Python 3.7 and above is required to run this server. Check you python version using the following command first. 

```bash 
python --version
```

Then run under the folder which contains `bundle` and `user_server.py` 

```bash
python user_server.py
```

No dependencies required. 