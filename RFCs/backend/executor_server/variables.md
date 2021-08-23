# Variables

## Environment Variables

The executor uses the a bunch of environment variables to determine the content it serves. Every environment variable starts with `GE_` which is short for graphery executor. 

|       Variable       | Default Values |                         Description                          |
| :------------------: | :------------: | :----------------------------------------------------------: |
|     `SERVE_URL`      |  `127.0.0.1`   |         The URL used to access the executor server.          |
|     `SERVE_PORT`     |     `7590`     |         The port used to access the executor server.         |
|   `ALLOWED_ORIGIN`   |     `None`     |      The allowed origin to access the executor server.       |
| `EXECUTION_TIME_OUT` |      `5`       | The time in seconds during which the executor is allowed to run. |
|   `CONSOLE_OUTPUT`   |     `True`     | The used to indicate if the exeuctor should output the execution process to the stdout. |

## Custom Variables 

|     Variable     | Default Values |                         Description                          |
| :--------------: | :------------: | :----------------------------------------------------------: |
| `SERVER_VERSION` |    `3.0.0`     | The version of this server. The first digit of the server version matches the version of the result JSON API version. |

