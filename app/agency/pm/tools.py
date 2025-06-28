from agents import function_tool

# This is a workaround to allow dependency injection for tools
# without exposing injected dependencies in the function signature
# which causes Pydantic schema generation errors with the agents library.
_tasks_repository = None

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
    if _tasks_repository is None:
        raise RuntimeError("TasksRepository not initialized for tools.")
    return _tasks_repository.get_tasks(status, limit, offset, from_id, to_id)

@function_tool
def do_nothing():
    """
    A placeholder function that does nothing.
    :return: None
    """
    print("This function intentionally does nothing.")
    return None