from abc import ABC, abstractmethod

class IIntelligenceProcessor(ABC):
    """
    Interface fornecida pelo componente IntelligenceProcessor.
    Requerida pelo componente StoreSearch.
    Define o contrato para validação de similaridade de strings.
    """
    @abstractmethod
    def validar_similaridade(self, string_a: str, string_b: str) -> bool:
        pass
