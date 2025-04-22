from abc import ABC, abstractmethod

class IQuery(ABC):
    @abstractmethod
    def build_query(self, parametros: dict) -> str:
        pass
    
    @abstractmethod
    def _delete_none_params(self, parametros: dict) -> dict:
        pass
