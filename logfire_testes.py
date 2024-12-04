import logfire
from opentelemetry.metrics import CallbackOptions, Observation
from typing import Iterable

logfire.configure()


def cpu_time_callback(options: CallbackOptions) -> Iterable[Observation]:
    observations = []
    with open("/proc/stat") as procstat:
        procstat.readline()  # skip the first line
        for line in procstat:
            if not line.startswith("cpu"):
                break
            cpu, user_time, nice_time, system_time = line.split()
            observations.append(
                Observation(int(user_time) // 100, {"cpu": cpu, "state": "user"})
            )
            observations.append(
                Observation(int(nice_time) // 100, {"cpu": cpu, "state": "nice"})
            )
            observations.append(
                Observation(int(system_time) // 100, {"cpu": cpu, "state": "system"})
            )
    return observations

logfire.metric_counter_callback(
    'system.cpu.time',
    unit='s',
    callbacks=[cpu_time_callback],
    description='CPU time',
)

cpu_time_callback()