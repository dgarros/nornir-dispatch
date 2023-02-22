from nornir.core.task import Result
from nornir.core.task import Task
from nornir_dispatcher import registry


def dispatcher(task: Task, action: str, *args, **kwargs) -> Result:
    """Helper Task to retrieve a given Nornir task for a given platform.

    Args:
        task (Nornir Task):  Nornir Task object.
        action (str):  The string value of the action to execute.

    Returns:
        Result: Nornir Task result.
    """

    task_to_run = registry.get_task(platform=task.host.platform, action=action)
    result = task.run(task=task_to_run, *args, **kwargs)

    return Result(
        host=task.host,
        result=result,
    )
