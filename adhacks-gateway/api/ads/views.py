from flask import request, jsonify
from . import ads_blueprint
from .agents.copywriting_agent import CopywritingAgent
from .agents.market_research_agent import ResearchAgent

copywriting_agent = CopywritingAgent()
research_agent = ResearchAgent()
@ads_blueprint.route('/research',methods=["POST"])
def run_process():
    try:
        
        query = request.json['query']
        company_index_name = ""
        
        result = research_agent.indexing(company_index_name, "Description of what the company is selling, what business does the company do and the location of the campaign")

        return jsonify({
            'message': result
        }), 200
        
    except Exception as e:
            error_message = str(e)
            return jsonify({"error": error_message}), 400