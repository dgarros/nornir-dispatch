from __future__ import annotations

import importlib
import logging
from collections import defaultdict
from dataclasses import dataclass
from dataclasses import field
from typing import Callable
from typing import Optional
from typing import Any
from typing import Dict

from nornir.core.task import Result

from nornir_dispatch.exceptions import PlatformNotFoundError
from nornir_dispatch.exceptions import TaskNotFoundError


LOGGER = logging.getLogger(__name__)


class NornirDispatchBaseDriver:
    platform: str

    @classmethod
    def get_tasks(cls) -> Dict[str, Callable[[Any], Result]]:
        """Return all the Nornir Task defined in this driver."""
        tasks = {}
        for key, value in cls.__dict__.items():
            if not isinstance(value, staticmethod):
                continue
            tasks[key] = getattr(cls, key)

        return tasks


@dataclass
class TaskElement:
    task: Callable[[Any], Result]
    origin: str | None


REGEX_VALID_FUNCTION_STRING = r"^.*\..*\..*$"


@dataclass
class Registry:
    tasks: dict[str, dict[str, TaskElement]] = field(
        default_factory=lambda: defaultdict(dict)
    )

    def _register_task_func(
        self,
        platform: str,
        action: str,
        task: Callable[[Any], Result],
        origin: str | None = None,
    ) -> bool:
        # TODO check if a task already exist for this task_name
        self.tasks[platform][action] = TaskElement(task=task, origin=origin)

        return True

    def register_task(
        self, platform: str, action: str, task: str | Callable[[Any], Result]
    ) -> bool:
        if callable(task):
            return self._register_task_func(platform=platform, action=action, task=task)

        elif isinstance(task, str):
            module_name, function_name = task.rsplit(".", 1)
            task_function = getattr(importlib.import_module(module_name), function_name)

            if not task_function:
                raise Exception(
                    f"Unable to locate the task function {task}, preemptively failed."
                )

            return self._register_task_func(
                platform=platform, action=action, task=task_function, origin=task
            )

    def register_tasks(
        self, driver: type[NornirDispatchBaseDriver], platform: str | None = None
    ) -> None:
        """Register multiple tasks at once in the registry.

        The tasks msut be defined as staticfunction as part of the same class.

        Args:
            platform (str): Name of the platform to associate with these tasks
            driver (type[object]): Driver Class containing one or multiple Nornir tasks defined as staticfunction

        """
        if not issubclass(driver, NornirDispatchBaseDriver):
            raise TypeError("driver must be a subclass of NornirDispatchBaseDriver")

        if not platform and not driver.platform:
            raise ValueError(
                "plaform must be defined at the driver level or it be defined explicitly"
            )

        for task_name, task in driver.get_tasks().items():
            self._register_task_func(
                platform=platform or driver.platform,
                action=task_name,
                task=task,
                origin=driver.__name__,
            )

    def get_task(self, platform: str | None, action: str) -> Callable[[Any], Result]:
        """Return the task associated with a given action for a specific platform.

        Args:
            platform (str | None): Name of the platform
            action (str): Name of the action

        Raises:
            ValueError: Platform must be defined to use nornir dispatch
            PlatformNotFoundError: Unable to find the platfor
            TaskNotFoundError: Unable to find the task associated with this platform

        Returns:
            Callable[[Any], Result]: Nornir Task associated with this action
        """
        if not platform:
            raise ValueError("Platform must be defined to use nornir dispatch")

        if platform not in self.tasks:
            raise PlatformNotFoundError(platform=platform)

        if action not in self.tasks[platform]:
            raise TaskNotFoundError(platform=platform, action=action)

        return self.tasks[platform][action].task

    def has_task(self, platform: str, action: str) -> bool:
        """Check if a given action for a specific platform is present in the registry."""
        if platform in self.tasks and action in self.tasks[platform]:
            return True

        return False


registry = Registry()
