from flask import request, jsonify
from . import ads_blueprint
from .agents.copywriting_agent import CopywritingAgent
from .agents.market_research_agent import ResearchAgent
from .services import CompanyService, CampaignService

copywriting_agent = CopywritingAgent()
research_agent = ResearchAgent()
coService = CompanyService()
campService = CampaignService()
adService = AdvertService()

### list of companies
@ads_blueprint.route('/companies',methods=["GET"])
def get_companies():
    try:
        companies = get_all_companies()
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
        company = coService.get_company_by_id(comp_id)
    
        return jsonify(
            {
                "company_name": company.CO_NAME,
                "company_description": company.CO_DESCRIPTION,
                "company_industry_type": company.CO_INDUSTRY_TYPE,
                "company_unique_selling": company.CO_SELLING_POINTS,
                "company_marketing_strategy": company.CO_BEST_STRATEGIES,
                "competitor_unique_selling": company.CO_COMPETITOR_SELLING_POINTS,
                "competitor_marketing_strategy": company.CO_COMPETITOR_BEST_STRATEGIES
            }
        ), 200
        
    except Exception as e:
            error_message = str(e)
            return jsonify({"error": error_message}), 400

### Generate a company profile
@ads_blueprint.route('/companies/create',methods=["POST"])
def create_company():
    try:
    
        company_name = request.json['company_name']
        company_description = request.json['company_description']
        company_website = request.json['company_website']
        company_industry_type = request.json['company_industry_type']
        
        company = coService.create_company(company_name, company_description, company_website, company_industry_type)

        ### after that the result of the generation would be 
        ### company's unique selling point, company's marketing strategy. competitors unique selling point, competitors marketing strategy
        
        coService.update_company(company, unique_sell, market_strat, compet_unique_sell, compet_market_strat)

        return jsonify({
            'message': "Company is created"
        }), 200
        
    except Exception as e:
            error_message = str(e)
            return jsonify({"error": error_message}), 400
        
        
### Get list of campaigns associated with the company
@ads_blueprint.route('/companies/<comp_id>/campaigns',methods=["GET"])
def fetch_campaign(comp_id):
    try:
        campaigns = campService.get_campaign_by_co_id(comp_id)

        data = []
        for row in campaigns:
             item = {
                'id': row['CA_ID'],
                "social_media": row['CA_SOCIAL_MEDIA'],
                "tone": row['CA_TONE'],
                "city": row['CA_CITY'],
                "start_date": row['CA_START_DATE'],
                "end_date": row['CA_END_DATE'],
                "target_market": row['CA_TARGET_MARKET'],
                "objectives": row['CA_PURPOSE'],
                "link": row['CA_URL']
             }
             data.append(item)

        return jsonify({
            data
        }), 200
        
    except Exception as e:
            error_message = str(e)
            return jsonify({"error": error_message}), 400
        
### Generate a campaign
@ads_blueprint.route('/companies/<comp_id>/campaigns/generate',methods=["POST"])
def generate_campaign(comp_id):
    try:
    
        company = coService.get_company_by_id(comp_id)

        id = company.CO_ID
        tone = request.json['tone']
        start_date = request.json['start_date']
        end_date = request.json['end_date']
        target_market = request.json['target_market']
        objectives = request.json['campaign_purpose']
        link = request.json['link']
        social_media = request.json['social_media']
        company_campaign_info = ''
        company_copy = ''
        city = request.json['city']
        
        campaign = campService.create_campaign(id, start_date, end_date, company_campaign_info, company_copy, link, target_market, social_media, tone, objectives, city)

        ### after that the result of the generation would be 
        ### day, time, social_post_text, hashtags

        Advertisments = adService.create_advert(type, day, time, copy, hashtags, link, campaign.CA_ID)
        
        data = []
        for row in Advertisments:
            item = {
                'type': row['AD_TYPE'],
                "day": row['AD_DAY'],
                "time": row['AD_TIME'],
                "social_post_text": row['AD_COPY'],
                "hashtags": row['AD_HASHTAGS'],
                "ad_link": row['AD_LEAD_LINK'],
                "lead_link": row['CA_PURPOSE']
            }
            data.append(item)

        return jsonify({
            data
        }), 200
        
    except Exception as e:
            error_message = str(e)
            return jsonify({"error": error_message}), 400