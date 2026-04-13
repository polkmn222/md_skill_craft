"""Progress bar utilities."""

from rich.progress import Progress as RichProgress, SpinnerColumn, BarColumn, TaskProgressColumn, TextColumn
from contextlib import contextmanager


@contextmanager
def progress_bar(description: str = "작업 중"):
    """Context manager for progress bar.

    Args:
        description: Description of the task

    Yields:
        Progress instance for manual updates
    """
    progress = RichProgress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
    )

    with progress:
        task_id = progress.add_task(description, total=100)
        yield progress, task_id


def step_progress(progress: RichProgress, task_id: int, advance: int = 10) -> None:
    """Advance progress bar.

    Args:
        progress: Progress instance
        task_id: Task ID
        advance: Number of steps to advance
    """
    progress.update(task_id, advance=advance)
