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
                "company_id": "1323",
                "company_name": "The Koi",
                "company_industry_type":"Food & Beverages",
                "total_campaigns":"0",
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
                "company_name": "The Koi",
                "company_website":"https://www.koithe.com/en",
                "company_description":"Hailing from Taiwan, KOI THÉ embraces its origins by infusing its tea products with cultural perfection and impeccable quality. The refined taste of brewed tea has brought about a huge following, with customers lining up in throngs to taste it! The refreshing lineup of teas include traditional varieties of green and black tea. This is then mixed with fun toppings such as golden bubbles, grass jelly, and even aloe vera! Each sip has a fresh, delicate flavour with a soothing aftertaste––a perfect accompaniment to a day of shopping",
                "company_industry_type":"Food & Beverages",
                "company_unique_selling":"As a business owner, it's important to keep an eye on your competitors and their marketing strategies. By doing so, you can learn from their successes and failures and apply those lessons to your own business. In the case of The Koi, a Taiwanese tea company, there are a few marketing strategies that could be emulated from their competitors.\n\nFirstly, The Koi could consider partnering with influencers or celebrities to promote their products. Many of their competitors have successfully used this strategy to increase brand awareness and drive sales. By partnering with someone who has a large following on social media, The Koi could reach a wider audience and potentially attract new customers.\n\nAnother strategy that The Koi could adopt is offering limited-time promotions or discounts. This is a common tactic used by many of their competitors to incentivize customers to make a purchase. By offering a discount or promotion for a limited time, The Koi could create a sense of urgency and encourage customers to act quickly.\n\nLastly, The Koi could consider expanding their product line to include more unique and innovative flavors. Many of their competitors have successfully differentiated themselves by offering unique and exciting flavors that customers can't find elsewhere. By offering a wider variety of flavors, The Koi could attract new customers and keep existing ones coming back for more.\n\nIn conclusion, by keeping an eye on their competitors and adopting some of their successful marketing strategies, The Koi could increase brand awareness, drive sales, and attract new customers. It's important to remember that not every strategy will work for every business, so it's important to experiment and find what works best for your specific brand and audience.",
                "company_marketing_strategy":"When it comes to the food and beverage industry, competition is fierce. Every company is trying to stand out and attract customers with their unique selling points. One of the competitors in this industry is known for their use of fresh, organic ingredients, while another is known for their innovative and creative menu offerings. But what about The Koi?\n\nThe Koi is a company that hails from Taiwan and prides itself on infusing its tea products with cultural perfection and impeccable quality. Their refined taste of brewed tea has brought about a huge following, with customers lining up in throngs to taste it! The refreshing lineup of teas includes traditional varieties of green and black tea, mixed with fun toppings such as golden bubbles, grass jelly, and even aloe vera! Each sip has a fresh, delicate flavor with a soothing aftertaste––a perfect accompaniment to a day of shopping.\n\nSo, how does The Koi stand out from its competitors? While other companies may focus on organic ingredients or creative menu offerings, The Koi focuses on the cultural significance of tea and the art of brewing it to perfection. They also offer a unique and refreshing twist on traditional tea by adding fun and exciting toppings. This sets them apart from their competitors and gives customers a reason to choose The Koi over other tea shops.\n\nIn conclusion, while other companies may have their own unique selling points, The Koi stands out by focusing on the cultural significance of tea and offering a refreshing twist on traditional tea. By continuing to emphasize these aspects of their brand, The Koi can continue to attract customers and stand out in the competitive food and beverage industry.",
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
                "id": "1",
                "social_media": ['instagram'],
                "tone": "friendly",
                "start_date": "12/03/2023",
                "end_date": "16/03/2023",
                "target_market": "Youth adults between the age of 15 to 25",
                "objectives": "To advertise a limited edition drink, Cheesey Foam Black Team with Pearls",
                "lead_conv_enabled": "N",
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
            'link': data,
        }), 200
        
    except Exception as e:
            error_message = str(e)
            return jsonify({"error": error_message}), 400
        
# @ads_blueprint.route('/video/generate',methods=["POST"])
# def get_video():
#     try:
        
#         copywriting = request.json['copywriting']

#         data = copywriting_agent.find_videos(copywriting)
        
#         return jsonify({
#             'link': data,
#         }), 200
        
#     except Exception as e:
#             error_message = str(e)
#             return jsonify({"error": error_message}), 400