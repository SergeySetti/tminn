from agents import function_tool


@function_tool
def check_tasks_board(
    status: str = None,
    limit: int = 100,
    offset: int = 0,
    from_id: str = None,
    to_id: str = None
) -> list:
    """
    Check tasks board with optional filters.

    :param status: Filter tasks by status (e.g., 'pending', 'completed').
    :param limit: Maximum number of tasks to return.
    :param offset: Number of tasks to skip.
    :param from_id: Minimum task ID to include.
    :param to_id: Maximum task ID to include.
    :return: List of tasks matching the criteria.
    """
    from app.db import TasksRepository
    tasks_repo = TasksRepository()
    return tasks_repo.get_tasks(status, limit, offset, from_id, to_id)
