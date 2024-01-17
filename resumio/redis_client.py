import os
import redis

REDIS_CONN_TYPE = os.getenv('REDIS_CONN_TYPE', 'TCP')

if REDIS_CONN_TYPE is None:
    raise EnvironmentError("required REDIS_CONN_TYPE")

REDIS_DB = int(os.getenv('REDIS_DB', 0))
redis_client = None
if REDIS_CONN_TYPE == 'TCP':
    REDIS_HOST = str(os.getenv('REDIS_HOST', 'localhost'))
    REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
    pool = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
    redis_client = redis.Redis(connection_pool=pool)
elif REDIS_CONN_TYPE == 'UNIX':
    REDIS_UNIX_SOCKET_PATH = str(os.getenv('REDIS_UNIX_SOCKET_PATH', None))
    if REDIS_UNIX_SOCKET_PATH is None:
        raise EnvironmentError("required REDIS_UNIX_SOCKET_PATH")
    redis_client = redis.Redis(unix_socket_path='/tmp/redis.sock', db=REDIS_DB)
assert isinstance(redis_client, redis.Redis)
