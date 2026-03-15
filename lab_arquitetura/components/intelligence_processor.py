import difflib
from interfaces.iintelligence_processor import IIntelligenceProcessor

class IntelligenceProcessor(IIntelligenceProcessor):
    """
    Componente: Processador de Inteligência
    Fornece a interface: IIntelligenceProcessor
    
    Responsável por normalizar os nomes dos produtos retornando se há correspondência.
    """
    def validar_similaridade(self, string_a: str, string_b: str) -> bool:
        # Implementação de Fuzzy Matching usando difflib do Python
        # Retorna True se a similaridade entre as strings for maior ou igual a 60%
        # ou se a string_a (termo de busca) estiver perfeitamente contida na string_b
        
        string_a_lower = string_a.strip().lower()
        string_b_lower = string_b.strip().lower()
        
        if string_a_lower in string_b_lower:
            return True
            
        ratio = difflib.SequenceMatcher(None, string_a_lower, string_b_lower).ratio()
        return ratio >= 0.60
