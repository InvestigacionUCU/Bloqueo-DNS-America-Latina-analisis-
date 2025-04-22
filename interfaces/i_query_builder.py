from abc import ABC, abstractmethod

from interfaces.i_query import IQuery
from utils.query import Query

class IQueryBuilder(ABC):
    @abstractmethod
    def set_base_url(self, base_url: str) -> 'IQueryBuilder':
        pass
    
    @abstractmethod
    def set_test_name(self, test_name: str) -> 'IQueryBuilder':
        pass
    
    @abstractmethod
    def set_probe_cc(self, probe_cc: str) -> 'IQueryBuilder':
        pass
    
    @abstractmethod
    def set_since(self, since: str) -> 'IQueryBuilder':
        pass
    
    @abstractmethod
    def set_until(self, until: str) -> 'IQueryBuilder':
        pass
    
    @abstractmethod
    def set_ooni_run_link_id(self, ooni_run_link_id: str) -> 'IQueryBuilder':
        pass
    
    @abstractmethod
    def set_probe_asn(self, asn: str) -> 'IQueryBuilder':
        pass
    
    @abstractmethod
    def set_domain(self, domain: str) -> 'IQueryBuilder':
        pass
    
    @abstractmethod
    def set_input(self, input_: str) -> 'IQueryBuilder':
        pass
    
    @abstractmethod
    def set_category_code(self, category_codes: str) -> 'IQueryBuilder':
        pass

    @abstractmethod
    def build(self) -> 'Query':
        pass
