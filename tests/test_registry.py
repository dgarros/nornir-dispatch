from nornir.core.task import Result, Task

from nornir_dispatch import Registry


def alwaystrue(task: Task, logger, obj) -> Result:
    return True


def alwaysfalse(task: Task, logger, obj) -> Result:
    return False


class AristaDriver:
    @staticmethod
    def action1(task: Task, logger, obj) -> Result:
        return True

    @staticmethod
    def action2(task: Task, logger, obj) -> Result:
        return "action2 arista"


class CiscoDriver:
    @staticmethod
    def action1(task: Task, logger, obj) -> Result:
        return False

    @staticmethod
    def action2(task: Task, logger, obj) -> Result:
        return "action2 cisco"


def test_registry_init():
    registry = Registry()
    assert registry


def test_register_task():
    registry = Registry()
    assert registry.register_task(
        platform="arista_eos", action="action1", task=alwaystrue
    )

    assert "arista_eos" in registry.tasks
    assert "action1" in registry.tasks["arista_eos"]
    assert registry.tasks["arista_eos"]["action1"].task == alwaystrue
    assert registry.tasks["arista_eos"]["action1"].origin is None


def test_register_tasks():
    registry = Registry()
    registry.register_tasks(platform="arista_eos", driver=AristaDriver)

    assert "arista_eos" in registry.tasks
    assert sorted(registry.tasks["arista_eos"].keys()) == ["action1", "action2"]
    assert callable(registry.tasks["arista_eos"]["action1"].task)
    assert registry.tasks["arista_eos"]["action1"].origin == "AristaDriver"


def test_get_task():
    registry = Registry()
    assert registry.register_task(
        platform="arista_eos", action="action1", task=alwaystrue
    )
    assert registry.register_task(
        platform="cisco_ios", action="action1", task=alwaysfalse
    )

    assert registry.get_task(platform="arista_eos", action="action1") == alwaystrue
    assert registry.get_task(platform="cisco_ios", action="action1") == alwaysfalse
