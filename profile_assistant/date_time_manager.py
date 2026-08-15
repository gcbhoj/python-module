from datetime import datetime, timezone


class DateTimeManager:

    def get_current_time(self):
        return datetime.now(timezone.utc).strftime("%H:%M GMT")

    def get_current_date(self):
        return datetime.now(timezone.utc).strftime("%B %d, %Y")

    def get_current_day(self):
        return datetime.now(timezone.utc).strftime("%A")