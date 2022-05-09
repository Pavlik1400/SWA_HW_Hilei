import os


FACADE = "facade"
LOGGING = "logging"
MESSAGES = "messages"
KAFKA= "kafka"

CONTROLLERS = {
    FACADE: "facade_controller",
    # LOGGING: "logging_service",
    LOGGING: "logging_service_hazelcast",
    MESSAGES: "messages_service",
}

DEFAULT_CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "services_config.yml")

KAFKA_MSG_TOPIC = "msg-topic"
KAFKA_URI = "localhost:9092"
