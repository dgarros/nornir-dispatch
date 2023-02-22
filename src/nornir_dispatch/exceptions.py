class Error(Exception):
    pass


class PlatformNotFoundError(Error):
    def __init__(self, platform, message=None):
        self.platform = platform
        self.message = message or f"No task registered for the platform: '{platform}'."
        super().__init__(self.message)


class TaskNotFoundError(Error):
    def __init__(self, action, platform, message=None):
        self.platform = platform
        self.action = action
        self.message = (
            message
            or f"No task registered for the action '{action}' for the platform: '{platform}'."
        )
        super().__init__(self.message)
