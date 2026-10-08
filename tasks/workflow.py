from .models import Task


ALLOWED_STATUS_TRANSITIONS = {
    Task.Status.TODO: {
        Task.Status.IN_PROGRESS,
    },
    Task.Status.IN_PROGRESS: {
        Task.Status.TODO,
        Task.Status.REVIEW,
    },
    Task.Status.REVIEW: {
        Task.Status.IN_PROGRESS,
        Task.Status.DONE,
    },
    Task.Status.DONE: {
        Task.Status.IN_PROGRESS,
    },
}

def can_transition(current_status, new_status):
    allowed_statuses = ALLOWED_STATUS_TRANSITIONS.get(
        current_status,
        set(),
    )

    return new_status in allowed_statuses