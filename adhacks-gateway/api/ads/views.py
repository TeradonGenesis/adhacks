from flask import request, jsonify
from . import ads_blueprint
from .agents.copywriting_agent import CopywritingAgent
from .agents.market_research_agent import ResearchAgent
from .vector_service import VectorService
import traceback
import os
from werkzeug.utils import secure_filename

from langchain.schema import Document
from langchain.vectorstores import Chroma

copywriting_agent = CopywritingAgent()
research_agent = ResearchAgent()
vector_service = VectorService()
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
        
        company_lowercase = company_name.lower()
        company_index_name = company_lowercase.replace(" ", "_")
        
        vector_service.create_company_profile(company_index_name, company_name, company_description, company_website, company_industry_type)
        description = research_agent.indexing(company_index_name, "Description of what the company is selling, what business does the company do and the location of the campaign")
        research_agent.scrape_competitor_data(company_index_name)
        strategies = research_agent.check_similar_marketing_strategies(company_index_name, description)
        unique = research_agent.create_unique_selling_points(company_index_name, description)
        
        ### after that the result of the generation would be 
        ### company's unique selling point, company's marketing strategy
        
        return jsonify({
            'message': "Company is created",
            'strategies': strategies,
            'unique': unique
        }), 200
        
    except Exception as e:
            error_message = str(e)
            print(traceback.format_exc())
            return jsonify({"error": error_message}), 400
        
        
### Get list of campaigns associated with the company
@ads_blueprint.route('/companies/<comp_id>/campaigns',methods=["GET"])
def get_specific_campaign(comp_id):
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
        lead_conv_enabled = request.json['lead_conv_enabled']
        
        company_index_name = "The Koi"
        company_lowercase = company_index_name.lower()
        company_index_name = company_lowercase.replace(" ", "_")
        general_copywriting = copywriting_agent.create_general_copywriting_chain(company_index_name, objectives, target_market, tone)
        
        hashtags = copywriting_agent.create_hashtags(general_copywriting)
        post_metadata = copywriting_agent.generate_instagram_content(general_copywriting)
        
        pic_link = copywriting_agent.find_photos(post_metadata["post"])
        
        ### after that the result of the generation would be 
        ### day, time, social_post_text, hashtags
        
        return jsonify({
            "posts":[{
                "type": "instagram",
                "day": post_metadata["day"],
                "time": post_metadata["time"],
                "social_post_text": post_metadata["post"],
                "hashtags": hashtags,
                "ad_link": "",
                "lead_link": "",
                "img_link": pic_link
            }]
        }), 200
        
    except Exception as e:
            error_message = str(e)
            print(traceback.format_exc())
            return jsonify({"error": error_message}), 400
        
@ads_blueprint.route('/docupload',methods=["POST"])
def upload_stories():
    try:
        
        file = request.files['file']
        index_name = request.form['index_name']

        #rename the title if theres spacing
        filename = secure_filename(file.filename)
        
        #check if it a file and file type is pdf
        is_pdf = '.' in filename and filename.rsplit('.',1)[1].lower() in ['pdf']
        
        if is_pdf is False:
            raise Exception(f'Cannot upload. {filename} is not a pdf')
        
        # Set the destination folder
        destination_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'docs')

        # Ensure that the destination folder exists
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)

        # Set the filename and save the file
        filepath = os.path.join(destination_folder, filename)
        
        file.save(filepath)

        vector_service.upload_doc(filename, index_name)

        return jsonify({
            'message': 'Stories uploaded',
            'index-name': index_name
        }), 201
        
    except Exception as e:
            error_message = str(e)
            return jsonify({"error": error_message}), 400
        
@ads_blueprint.route('/qa',methods=["POST"])
def qa_docs():
    try:
        
        query = request.json['query']
        index_name = request.json['index_name']

        data = copywriting_agent.question_answering_chain(index_name, query)
        
        return jsonify({
            'message': data,
        }), 200
        
    except Exception as e:
            error_message = str(e)
            return jsonify({"error": error_message}), 400
        
@ads_blueprint.route('/photo/generate',methods=["POST"])
def get_photo():
    try:
        
        copywriting = request.json['copywriting']

        data = copywriting_agent.find_photos(copywriting)
        
        return jsonify({
            'message': data,
        }), 200
        
    except Exception as e:
            error_message = str(e)
            return jsonify({"error": error_message}), 400