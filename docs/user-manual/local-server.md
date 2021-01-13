# Local Server

## Introduction 

Local server is used to generate step by step debug info for the front end. 

## Install 
 -  Go the [release page](https://github.com/FlickerSoul/Graphery/releases), and download the latest `user_server.zip` file. Extract everything in the zip file to a folder. 
    
 -  Or you can clone the repository if the version is not available on the release page: 
    
    ```bash
    git clone https://github.com/FlickerSoul/Graphery.git
    cd Graphery/backend
    ```

    Under this director, you can see a `bundle` folder and a `user_server.py` file. Those two will be the only thing you need. You can copy them in to a separate folder and delete the rest. 

## Usage 

No dependencies required. 

Python 3.7 and above is required to run this server. Check you python version using the following command first. 

```bash 
python --version
```


-   If you are a Unix user, please click on the `launch` file. If you are a Windows user, please click on the `launch.bat` file. 

-   You can also manually launch the server in a terminal if the script doesn't work. 

    Then run under the folder which contains `bundle` and `user_server.py` 

    ```bash
    python user_server.py
    ```

## More

The execution log file is located in `~/.graphery_cache/log/`. 

If you want the controller to output the log on the terminal, you can type the following shell command to your terminal: 
```bash
export SEEKER_LOG_OUTPUT_FLAG=0
```

If you also want to turn off the on-screen output, you also need the following shell command: 
```bash
export SEEKER_DEFAULT_OUTPUT_FLAG=0
```
