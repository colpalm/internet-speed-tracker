from enum import Enum


class TimeOfDay(Enum):
    MORNING = "Morning"
    AFTERNOON = "Afternoon"
    EVENING = "Evening"
    ALL = "All"


class SpeedTestServer(Enum):
    NYC_CLOUVIDER = (52, "New York, Clouvider")
    ATLANTA_CLOUVIDER = (53, "Atlanta, Clouvider")
    CHICAGO_SHARKTECH = (93, "Chicago, Shark Tech")

    def __init__(self, server_id, location):
        self.server_id = server_id
        self.location = location
