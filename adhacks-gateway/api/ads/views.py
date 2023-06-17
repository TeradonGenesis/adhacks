from flask import request, jsonify
from . import ads_blueprint
from .agents.copywriting_agent import CopywritingAgent
from .agents.market_research_agent import ResearchAgent

copywriting_agent = CopywritingAgent()
research_agent = ResearchAgent()

### list of companies
@ads_blueprint.route('/companies',methods=["GET"])
def get_companies():
    try:
        
        return jsonify({
            'companies': [{
                "company_id": "",
                "company_name": "",
                "company_industry_type":"",
                "total_campaigns":"",
            }]
        }), 200
        
    except Exception as e:
            error_message = str(e)
            return jsonify({"error": error_message}), 400
        
### get specific company
@ads_blueprint.route('/companies/<comp_id>',methods=["GET"])
def get_specific_company(comp_id):
    try:
    
        return jsonify(
            {
                "company_name": "",
                "company_website":"",
                "company_description":"",
                "company_industry_type":"",
                "company_unique_selling":"",
                "company_marketing_strategy":"",
                "competitor_unique_selling":"",
                "competitor_marketing_strategy":"",
            }
        ), 200
        
    except Exception as e:
            error_message = str(e)
            return jsonify({"error": error_message}), 400

### Generate a company profile
@ads_blueprint.route('/companies/create',methods=["POST"])
def create_company():
    try:
    
        company_name = request.json['co_name']
        company_website = request.json['co_url']
        company_description = request.json['co_description']
        company_industry_type = request.json['industry_type']
        
        ### after that the result of the generation would be 
        ### company's unique selling point, company's marketing strategy. competitors unique selling point, competitors marketing strategy
        
        return jsonify({
            'message': "Company is created"
        }), 200
        
    except Exception as e:
            error_message = str(e)
            return jsonify({"error": error_message}), 400
        
        
### Get list of campaigns associated with the company
@ads_blueprint.route('/companies/<comp_id>/campaigns',methods=["GET"])
def generate_campaign(comp_id):
    try:
        
        return jsonify({
            "campaigns":[{
                "id": "",
                "social_media": "",
                "tone": "",
                "city": "",
                "start_date": "",
                "end_date": "",
                "target_market": "",
                "objectives": "",
                "lead_conv_enabled": "",
                "link": ""
            }]
        }), 200
        
    except Exception as e:
            error_message = str(e)
            return jsonify({"error": error_message}), 400
        
### Generate a campaign
@ads_blueprint.route('/companies/<comp_id>/campaigns/generate',methods=["POST"])
def generate_campaign(comp_id):
    try:
    
        tone = request.json['tone']
        city = request.json['city']
        start_date = request.json['start_date']
        end_date = request.json['end_date']
        target_market = request.json['target_market']
        objectives = request.json['campaign_purpose']
        link = request.json['link']
        social_media = request.json['social_media']
        lead_conv_enabled = request.json['social_media']
        
        ### after that the result of the generation would be 
        ### day, time, social_post_text, hashtags
        
        return jsonify({
            "posts":[{
                "type": "instagram",
                "day": "",
                "time": "",
                "social_post_text": "",
                "hashtags": "",
                "ad_link": "",
                "lead_link": "",
                "duration": "",
            }]
        }), 200
        
    except Exception as e:
            error_message = str(e)
            return jsonify({"error": error_message}), 400