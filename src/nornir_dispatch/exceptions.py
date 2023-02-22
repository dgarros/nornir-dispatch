"""Collection of Exception for nornir_dispatch"""


class PlatformNotFoundError(Exception):
    """Exception indicating the Platform requested hasn't been found."""

    def __init__(self, platform, message=None):
        self.platform = platform
        self.message = message or f"No task registered for the platform: '{platform}'."
        super().__init__(self.message)


class TaskNotFoundError(Exception):
    """Exception indicating the task associated with a specific action, for a given platform, hasn't been found."""

    def __init__(self, action, platform, message=None):
        self.platform = platform
        self.action = action
        self.message = (
            message
            or f"No task registered for the action '{action}' for the platform: '{platform}'."
        )
        super().__init__(self.message)
