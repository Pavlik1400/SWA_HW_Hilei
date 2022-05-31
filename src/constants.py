import os


FACADE = "facade"
LOGGING = "logging"
MESSAGES = "messages"
KAFKA = "kafka"

CONTROLLERS = {
    FACADE: "facade_controller",
    # LOGGING: "logging_service",
    LOGGING: "logging_service_hazelcast",
    MESSAGES: "messages_service",
}

DEFAULT_CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "services_config.yml")

KAFKA_CONFIG_KEY = "msg-q-config"
DEFAULT_KAFKA_CONFIG = {
    "topic": "msg-topic",
    "uri": "localhost:9092",
}
# DEFAULT_KAFKA_MSG_TOPIC = "msg-topic"
# DEFAULT_KAFKA_URI = "localhost:9092"
HAZELCAST_MAP_KEY = "logging-map-cnf"
DEFAULT_HAZELCAST_MAP_NAME = "logging-map"
