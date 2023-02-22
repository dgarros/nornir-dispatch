# Nornir Dispatch

[![PyPI](https://img.shields.io/pypi/v/nornir-dispatch.svg)][pypi_]
[![Status](https://img.shields.io/pypi/status/nornir-dispatch.svg)][status]
[![Python Version](https://img.shields.io/pypi/pyversions/nornir-dispatch)][python version]
[![License](https://img.shields.io/pypi/l/nornir-dispatch)][license]

[![Read the documentation at https://dgarros.github.io/nornir-dispatch/](https://dgarros.github.io/nornir-dispatch/)][Doc]
[![Tests](https://github.com/dgarros/nornir-dispatch/workflows/Tests/badge.svg)][tests]

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]

[pypi_]: https://pypi.org/project/nornir-dispatch/
[status]: https://pypi.org/project/nornir-dispatch/
[python version]: https://pypi.org/project/nornir-dispatch
[Documentation]: https://dgarros.github.io/nornir-dispatch/
[tests]: https://github.com/dgarros/nornir-dispatch/actions?workflow=Tests
[pre-commit]: https://github.com/pre-commit/pre-commit
[black]: https://github.com/psf/black

## Features

Nornir Dispatch is a utility for Nornir to simplify how to run multi-vendor workflows.

Nornir Dispatch allows you to register some tasks per platform and execute them seamlessly based on each host's characteristics.

## Installation

You can install _Nornir Dispatch_ via [pip] from [PyPI]:

```console
$ pip install nornir-dispatch
```

## Usage

```python
from nornir import InitNornir
from nornir.core.task import Result, Task

from nornir_dispatch import registry
from nornir_dispatch.plugins.tasks.dispatcher import dispatcher

def get_config_pyez(task: Task) -> Result:
    # Retrieve the config with Pyez for Junos devices
    config = None
    Result(host=task.host, result=config)

def get_config_netmiko(task: Task) -> Result:
    # Retrieve the config with Netmiko for other devices
    config = None
    Result(host=task.host, result=config)


def main():
    nr = InitNornir(
            inventory={
                "plugin": "SimpleInventory",
                "options": {
                    "host_file": "inventory.yml",
                },
            }
        )

    registry.register_tasks(platform="juniper_junos", action="get_config", task=get_config_pyez)
    registry.register_tasks(platform="cisco_ios", action="get_config", task=get_config_netmiko)

    results = nr.run(task=dispatcher, action="get_config")

if __name__ == "__main__":
    main()
```

## Contributing

Contributions are very welcome.
To learn more, see the [Contributor Guide].

## License

Distributed under the terms of the [Apache 2.0 license][license],
_Nornir Dispatch_ is free and open source software.

## Issues

If you encounter any problems,
please [file an issue] along with a detailed description.

## Credits

This project was generated from [@cjolowicz]'s [Hypermodern Python Cookiecutter] template.

[@cjolowicz]: https://github.com/cjolowicz
[pypi]: https://pypi.org/
[hypermodern python cookiecutter]: https://github.com/cjolowicz/cookiecutter-hypermodern-python
[file an issue]: https://github.com/dgarros/nornir-dispatch/issues
[pip]: https://pip.pypa.io/

<!-- github-only -->

[license]: https://github.com/dgarros/nornir-dispatch/blob/main/LICENSE
[contributor guide]: https://github.com/dgarros/nornir-dispatch/blob/main/CONTRIBUTING.md
[command-line reference]: https://nornir-dispatch.readthedocs.io/en/latest/usage.html
