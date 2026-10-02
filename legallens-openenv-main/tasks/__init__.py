"""
LegalLens 2.0 - Tasks package init.
"""

from .task_definitions import TaskDefinition
from .task_01_cyber_fraud import TASK_CYBER_FRAUD
from .task_02_bail import TASK_BAIL
from .task_03_consumer import TASK_CONSUMER
from .task_04_property import TASK_PROPERTY

_ALL_TASKS = {
    TASK_CYBER_FRAUD.id: TASK_CYBER_FRAUD,
    TASK_BAIL.id: TASK_BAIL,
    TASK_CONSUMER.id: TASK_CONSUMER,
    TASK_PROPERTY.id: TASK_PROPERTY,
}


def get_all_tasks():
    return _ALL_TASKS


def get_task(task_id: str) -> TaskDefinition:
    if task_id not in _ALL_TASKS:
        raise ValueError(f"Unknown task '{task_id}'. Available: {list(_ALL_TASKS.keys())}")
    return _ALL_TASKS[task_id]


__all__ = [
    "TaskDefinition",
    "TASK_CYBER_FRAUD",
    "TASK_BAIL",
    "TASK_CONSUMER",
    "TASK_PROPERTY",
    "get_all_tasks",
    "get_task",
]
