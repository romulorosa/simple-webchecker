from collections import namedtuple
from decouple import config


DATABASE_CONF = namedtuple(
    'DATABASE_CONF', ('hostname', 'port', 'database', 'username', 'password')
)

KAKFA_CONF = namedtuple(
    'KAFKA_CLUSTER_CONF', (
        'bootstrap_servers',
        'topic',
        'ssl_certfile',
        'ssl_cafile',
        'ssl_keyfile'
    )
)


DATABASE = DATABASE_CONF(
    config('DB_HOST', default=''),
    config('DB_PORT', default=''),
    config('DB_DATABASE_NAME', default=''),
    config('DB_USER', default=''),
    config('DB_PASSWORD', default=''),
)

KAFKA = KAKFA_CONF(
    config('KAFKA_BOOTSTRAPSERVER', default=''),
    config('KAFKA_TOPIC', default=''),
    config('KAFKA_CERT_FILE_PATH', default=''),
    config('KAFKA_CA_CERT_PATH', default=''),
    config('KAFKA_CERT_KEY_PATH', default=''),
)
