from flask import Flask, render_template, request, jsonify
from components.intelligence_processor import IntelligenceProcessor
from components.store_search import StoreSearch

app = Flask(__name__)

# Configuração da Injeção de Dependência no nível da Aplicação
processor = IntelligenceProcessor()
store_search = StoreSearch(processor)

@app.route('/')
def index():
    """Renderiza a página inicial (Frontend)."""
    return render_template('index.html')

@app.route('/api/search', methods=['GET'])
def search():
    """
    Endpoint consumido pelo Frontend.
    Recebe o termo de busca e retorna o JSON estruturado após 
    passar pela arquitetura de Injeção de Dependências.
    """
    termo = request.args.get('q', '')
    if not termo:
        return jsonify({"error": "Termo de busca não fornecido."}), 400
        
    try:
        # Aciona o fluxo da arquitetura
        resultados = store_search.buscar_produtos(termo)
        return jsonify({
            "query": termo,
            "count": len(resultados),
            "results": resultados
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Roda o servidor web na porta 5000
    app.run(debug=True, port=5001)
