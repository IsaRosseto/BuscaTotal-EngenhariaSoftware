from abc import ABC, abstractmethod

class IStoreSearch(ABC):
    """
    Interface fornecida pelo componente StoreSearch.
    Define o contrato para buscar produtos nas lojas parceiras.
    """
    @abstractmethod
    def buscar_produtos(self, termo_busca: str) -> list:
        pass
