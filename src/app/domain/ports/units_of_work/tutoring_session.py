import abc
from src.app.domain.ports.repositories.tutoring_session import TutoringSessionRepositoryInterface


class TutoringSessionUnitOfWorkInterface(abc.ABC):
    tutoring_sessions: TutoringSessionRepositoryInterface

    def __enter__(self) -> "TutoringSessionUnitOfWorkInterface":
        return self

    def __exit__(self, *args):
        self.rollback()

    def commit(self):
        self._commit()

    @abc.abstractmethod
    def _commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError