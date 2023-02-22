from nornir.core.task import Result
from nornir.core.task import Task

from nornir_dispatch import NornirDispatchBaseDriver
from nornir_dispatch import Registry


def alwaystrue(task: Task) -> Result:
    return Result(host=None, result=True)


def alwaysfalse(task: Task) -> Result:
    return Result(host=None, result=False)


class AristaDriver(NornirDispatchBaseDriver):
    @staticmethod
    def action1(task: Task) -> Result:
        return Result(host=None, result=True)

    @staticmethod
    def action2(task: Task) -> Result:
        return Result(host=None, result="action2 Arista")


class CiscoDriver(NornirDispatchBaseDriver):
    @staticmethod
    def action1(task: Task) -> Result:
        return Result(host=None, result=False)

    @staticmethod
    def action2(task: Task) -> Result:
        return Result(host=None, result="action2 Cisco")


def test_registry_init() -> None:
    registry = Registry()
    assert registry


def test_register_task() -> None:
    registry = Registry()
    assert registry.register_task(
        platform="arista_eos", action="action1", task=alwaystrue
    )

    assert "arista_eos" in registry.tasks
    assert "action1" in registry.tasks["arista_eos"]
    assert registry.tasks["arista_eos"]["action1"].task == alwaystrue
    assert registry.tasks["arista_eos"]["action1"].origin is None


def test_register_tasks() -> None:
    registry = Registry()
    registry.register_tasks(platform="arista_eos", driver=AristaDriver)

    assert "arista_eos" in registry.tasks
    assert sorted(registry.tasks["arista_eos"].keys()) == ["action1", "action2"]
    assert callable(registry.tasks["arista_eos"]["action1"].task)
    assert registry.tasks["arista_eos"]["action1"].origin == "AristaDriver"


def test_get_task() -> None:
    registry = Registry()
    assert registry.register_task(
        platform="arista_eos", action="action1", task=alwaystrue
    )
    assert registry.register_task(
        platform="cisco_ios", action="action1", task=alwaysfalse
    )

    assert registry.get_task(platform="arista_eos", action="action1") == alwaystrue
    assert registry.get_task(platform="cisco_ios", action="action1") == alwaysfalse
