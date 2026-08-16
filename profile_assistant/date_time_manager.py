from datetime import datetime
from zoneinfo import ZoneInfo


class DateTimeManager:

    def __init__(self, timezone_name="America/Toronto"):
        self.tz = ZoneInfo(timezone_name)

    def get_current_datetime(self) -> datetime:
        return datetime.now(self.tz)

    def get_current_time(self) -> str:
        return self.get_current_datetime().strftime(
            "%I:%M %p %Z"
        ).lstrip("0")

    def get_current_date(self) -> str:
        return self.get_current_datetime().strftime(
            "%B %d, %Y"
        )

    def get_current_day(self) -> str:
        return self.get_current_datetime().strftime(
            "%A"
        )

    def get_day_part(self) -> str:
        hour = self.get_current_datetime().hour

        if 5 <= hour < 12:
            return "morning"
        elif 12 <= hour < 17:
            return "afternoon"
        elif 17 <= hour < 22:
            return "evening"
        else:
            return "night"