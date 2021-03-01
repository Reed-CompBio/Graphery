from os import getenv

_ENV_PREFIX = 'GRAPHERY_EXECUTOR_'

_DEFAULT_SERVE_URL_ENV_NAME = _ENV_PREFIX + 'DEFAULT_SERVE_URL'
DEFAULT_SERVE_URL: str = getenv(_DEFAULT_SERVE_URL_ENV_NAME, '127.0.0.1')

_DEFAULT_PORT_ENV_NAME = _ENV_PREFIX + 'DEFAULT_PORT'
DEFAULT_PORT: int = int(getenv(_DEFAULT_PORT_ENV_NAME, 7590))

_ORIGIN_ONLY_FLAG_ENV_NAME = _ENV_PREFIX + 'ORIGIN_ONLY_FLAG'
ONLY_ACCEPTED_ORIGIN: bool = bool(int(getenv(_ORIGIN_ONLY_FLAG_ENV_NAME, False)))
ACCEPTED_ORIGIN: str = ''

_EXECUTION_TIME_OUT_ENV_NAME = _ENV_PREFIX + 'TIMEOUT_SECONDS'
TIMEOUT_SECONDS: int = int(getenv(_EXECUTION_TIME_OUT_ENV_NAME, 5))

_ENTRY_PY_MODULE_ENV_NAME = _ENV_PREFIX + 'ENTRY_PY_MODULE_NAME'
ENTRY_PY_MODULE_NAME: str = getenv(_ENTRY_PY_MODULE_ENV_NAME, 'entry')
ENTRY_PY_FILE_NAME: str = f'{ENTRY_PY_MODULE_NAME}.py'

_MODULE_MAIN_FUNCTION_ENV_NAME = _ENV_PREFIX + 'MAIN_FUNCTION_NAME'
MAIN_FUNCTION_NAME: str = getenv(_MODULE_MAIN_FUNCTION_ENV_NAME, 'main')

GRAPH_OBJ_ANCHOR_NAME: str = 'graph_object'

REQUEST_CODE_NAME: str = 'code'
REQUEST_GRAPH_NAME: str = 'graph'

REQUEST_VERSION_NAME: str = 'version'
VERSION: str = '0.2.6'

SERVER_LOG = None

ENV_NAME_COLLECTION = [
    _DEFAULT_SERVE_URL_ENV_NAME,
    _DEFAULT_PORT_ENV_NAME,
    _ORIGIN_ONLY_FLAG_ENV_NAME,
    _EXECUTION_TIME_OUT_ENV_NAME,
    _ENTRY_PY_MODULE_ENV_NAME,
    _MODULE_MAIN_FUNCTION_ENV_NAME,
]
