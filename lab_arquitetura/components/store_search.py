import requests
from bs4 import BeautifulSoup
from interfaces.istore_search import IStoreSearch
from interfaces.iintelligence_processor import IIntelligenceProcessor

class StoreSearch(IStoreSearch):
    """
    Componente: Busca em Lojas
    Fornece a interface: IStoreSearch
    Requer a interface: IIntelligenceProcessor
    """
    
    # INJEÇÃO DE DEPENDÊNCIA: 
    # StoreSearch não instancia o IntelligenceProcessor, 
    # ele o recebe no construtor através de sua interface IIntelligenceProcessor.
    def __init__(self, processor: IIntelligenceProcessor):
        print("\n[PROVA DE INJEÇÃO DE DEPENDÊNCIA]")
        print("-> Componente StoreSearch recebeu a Interface IIntelligenceProcessor com sucesso no construtor!")
        self._processor = processor
    
    def buscar_produtos(self, termo_busca: str) -> list:
        # Integração via Web Scraping (Mercado Livre API retorna 403)
        termo_formatado = termo_busca.replace(' ', '-')
        url = f"https://lista.mercadolivre.com.br/{termo_formatado}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
        }
        
        resultados_brutos = []
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            items = soup.select('.ui-search-result__wrapper')
            
            for item in items[:25]:  # Limit to 25 items to process
                link_elem = item.select_one('a')
                if not link_elem:
                    continue
                    
                titulo = link_elem.text.strip()
                link = link_elem.get('href', '#')
                
                # Fetch Image
                img_elem = item.select_one('img')
                thumbnail = ''
                if img_elem:
                    thumbnail = img_elem.get('src', '')
                    if thumbnail.startswith('data:image'):
                        thumbnail = img_elem.get('data-src', thumbnail)
                
                # Fetch Price String and parse it
                preco = 0.0
                price_elem = item.select_one('.andes-money-amount__fraction')
                if price_elem:
                    preco_texto = price_elem.text.replace('.', '').replace(',', '.')
                    try:
                        preco = float(preco_texto)
                    except ValueError:
                        preco = 0.0
                        
                resultados_brutos.append({
                    'title': titulo,
                    'price': preco,
                    'permalink': link,
                    'thumbnail': thumbnail,
                    'condition': 'new',
                    'currency_id': 'BRL'
                })
        except Exception as e:
            print(f"Erro ao capturar dados: {e}")
            resultados_brutos = []
            
        resultados_normalizados = []
        
        for produto in resultados_brutos:
            titulo = produto.get('title', '')
            
            # Comunicação OCORRE SOMENTE PELA INTERFACE REQUERIDA (IIntelligenceProcessor)
            # Aplicamos a regra de inteligência para filtrar se o produto realmente é relevante
            if self._processor.validar_similaridade(termo_busca, titulo):
                print(f" -> [IntelligenceProcessor] Aprovado por similaridade: {titulo}")
                # Estruturamos os dados para o Frontend
                item_formatado = {
                    'title': titulo,
                    'price': produto.get('price', 0.0),
                    'currency': produto.get('currency_id', 'BRL'),
                    'thumbnail': produto.get('thumbnail', ''),
                    'permalink': produto.get('permalink', '#'),
                    'condition': produto.get('condition', 'new')
                }
                resultados_normalizados.append(item_formatado)
                
        return resultados_normalizados
