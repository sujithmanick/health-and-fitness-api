from flask import jsonify
import requests

def diet_plan_scraper(diet_plans_scrab_url):
    web_content = requests.get(diet_plans_scrab_url).content
    return str(web_content)