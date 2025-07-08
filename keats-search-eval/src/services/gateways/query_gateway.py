import abc


class QueryGateway(abc.ABC):

    abc.abstractmethod

    def add(self, data: list[dict[str, str]]) -> None:
        pass

    abc.abstractmethod

    def get(self) -> list[dict[str, str]]:
        pass
