import json
import requests
from bs4 import BeautifulSoup

def diet_plan_scraper(diet_plans_scrab_url):
    web_content = requests.get(diet_plans_scrab_url)
    web_content = web_content.text
    soup = BeautifulSoup(web_content, 'html.parser')
    data_container = soup.find_all(class_='container pt-4')[0].find_all(class_='row')[0].find_all(class_='col-lg-9 col-xl-6 px-4')[0]
    # macronutrient_totals = data_container.find_all(class_='bg-white rounded-4 shadow-lg px-2 pt-3 pb-0 row mb-3')
    foods =  data_container.find_all(class_='bg-white rounded-4 shadow-lg px-2 pt-3 pb-2 row mb-3')
    overall_plan = {}
    day_counter=1
    for food in range(0,len(foods),5):
        day=f'Day {day_counter}'
        all_food={}
        snack_flag = True
        for day_food in range(food,food+5):
            one_day_one_food = foods[day_food]
            heading = one_day_one_food.find('p').text
            foods[day_food].select('.fw-bold')[0].text
            t_meal_cal = {}
            meal_eng_data = one_day_one_food.select('.col-3 p')
            for meal_eng in range(0,len(meal_eng_data),2):
                t_meal_cal[meal_eng_data[meal_eng].text] = meal_eng_data[meal_eng+1].text

            meal_food_data = one_day_one_food.select('.align-items-center')
            t_mls = []
            for meal_food in range(len(meal_food_data)):
                t_meal_food_dict = {}
                t_meal_food_dict["href"] = meal_food_data[meal_food].find('img')['src']
                t_meal_food_dict["name"] = meal_food_data[meal_food].select('.mb-0')[0].text
                t_meal_food_dict["quantity"] = meal_food_data[meal_food].select('.mb-0')[1].text
                t_mls.append(t_meal_food_dict)

            t_meal_cal["food"] = t_mls
            if snack_flag and heading == 'Snack':
                all_food[heading+'1'] = t_meal_cal
                snack_flag=False
            elif snack_flag==False and heading == 'Snack':
                all_food[heading+'2'] = t_meal_cal
            else:
                all_food[heading] = t_meal_cal
            overall_plan[day] = all_food
        day_counter+=1
    return overall_plan
