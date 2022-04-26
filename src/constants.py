import os


FACADE = "facade"
LOGGING = "logging"
MESSAGES = "messages"

CONTROLLERS = {
    FACADE: "facade_controller",
    LOGGING: "logging_service",
    MESSAGES: "messages_service",
}

DEFAULT_CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "services_config.yml")