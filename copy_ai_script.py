import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pymongo
from pymongo import MongoClient
import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import DesiredCapabilities


def wait(t):

    time.sleep(t)

# "your copy.ai account login email here(between these quotation marks)"
mail = ""
descriptions = 0  # 1 = 7 descriptions, 2 = 14, 3 = 21, 4 = 28, and so on, it increases by seven with each number.

capabilities = DesiredCapabilities.CHROME.copy()
capabilities['acceptSslCerts'] = True
capabilities['acceptInsecureCerts'] = True
options = webdriver.ChromeOptions()
options.add_argument("--headless")
driver = webdriver.Chrome(ChromeDriverManager().install(), desired_capabilities=capabilities)
driver.get('https://www.copy.ai/app')
wait(15)

def log_in(mail):

    driver.find_element_by_id('email').send_keys(mail)

    wait(1)

    btn_sign_in = driver.find_element_by_id('login')
    driver.execute_script("arguments[0].click();", btn_sign_in)

    while driver.current_url != 'https://www.copy.ai/callback':
        wait(3)
        pass

    wait(3)
    try :

        driver.find_element_by_id('next-button-welcome').click()
        wait(10)
    
    except:

        driver.execute_script("window.history.go(-1)")
        wait(10)
        driver.refresh()
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, 'email')))
        driver.find_element_by_id('email').clear()
        wait(3)
        driver.find_element_by_id('email').send_keys(mail)
        wait(1)
        btn_sign_in = driver.find_element_by_id('login')
        driver.execute_script("arguments[0].click();", btn_sign_in)

        while driver.current_url != 'https://www.copy.ai/callback':
            wait(3)
            pass

        wait(3)

        driver.find_element_by_id('next-button-welcome').click()
        wait(10)


    prd_des_btn = driver.find_element_by_xpath(
        "//a[@data-type='product descriptions']")
    driver.execute_script("arguments[0].click();", prd_des_btn)

    wait(3)


def object_getter():

    try:
        # put your url here(between these quotation marks) with your password!!
        cluster = MongoClient("")
    except:
        print("Wrong URL")
    try:
        # put the name of your db here(between these quotation marks)
        db = cluster[""]
    except:
        print("Wrong Data Base name")
    try:
        # put the name of your collection here(between these quotation marks)
        collection = db[""]
    except:
        print("Wrong collection name")

    objects_list = collection.find({})

    prd_list = [i for i in objects_list]

    wait(3)

    cluster.close()

    return prd_list


def get_json_input(prd_object):

    new_json = {
        'Product': {'Name': '',
                    'Description': ''}
    }

    try:

        new_json['Product']['Name'] = prd_object['Introduction']['Brand']

        new_json['Product']['Description'] = prd_object['Model']

        return new_json

    except Exception as e:
        print(e)
        print('in get json input()')
        pass


def idea_getter(product, description, amount_descriptions):

    driver.find_element_by_id('product-name').clear()
    wait(1.2)
    driver.find_element_by_id('product-name').send_keys(product)
    wait(3)
    driver.find_element_by_id('product-description').clear()
    wait(1.2)
    driver.find_element_by_id('product-description').send_keys(description)
    wait(3)
    button = driver.find_element_by_id('create-button')
    driver.execute_script("arguments[0].click();", button)

    dic_ideas = {}
    idea_counter = 0

    for i in range(amount_descriptions):

        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, 'idea-0')))

        wait(0.5)

        for j in range(7):

            idea_element = driver.execute_script(
                "return document.getElementById('idea-%d');" % (j))
            print(idea_element)

            wait(1)

            print(idea_counter)

            str_idea = idea_element.get_attribute('original_text')

            print(str_idea)

            wait(0.5)
            idea_counter += 1
            dic_ideas['idea_n%d' % (idea_counter)] = str_idea

        wait(1)

        more_btn = driver.find_element_by_id('create-button-2')
        driver.execute_script("arguments[0].click();", more_btn)

    return dic_ideas


def organizer(descs, 
              Prefix_for_brand=None, 
              suffix_for_brand=None, 
              Prefix_for_description=None, 
              suffix_for_description=None): 

    Prd_list = object_getter() 
    for i in range(len(Prd_list)): 
        try: 
            new_Json = get_json_input(Prd_list[i]) 
            if Prefix_for_brand: 
                if suffix_for_brand: 
                    prd_name = str(Prefix_for_brand) + " " + new_Json['Product']['Name'] + " " + str(suffix_for_brand) 
                else: 
                    prd_name = str(Prefix_for_brand) + " " + new_Json['Product']['Name'] 
            elif suffix_for_brand: 
                prd_name = new_Json['Product']['Name'] + " " + str(suffix_for_brand) 
            else: 
                prd_name = new_Json['Product']['Name'] 
            if Prefix_for_description: 
                if suffix_for_description: 
                    description = str(Prefix_for_description) + " " + new_Json['Product']['Description'] + " " + str(suffix_for_description) 
                else: 
                    description = str(Prefix_for_description) + " " + new_Json['Product']['Description'] 
            elif suffix_for_description: 
                description = new_Json['Product']['Description'] + " " + str(suffix_for_description) 
            else: 
                description = new_Json['Product']['Description'] 

            if description.find('.') != -1:

                description = description.replace('.', '_')

            dic = idea_getter(prd_name, description, descs) 

            json_file_output = { 
                description: dic 
            } 

            print(description)

            wait(2)
            store_the_output(json_file_output)
            
        except Exception as e:
            print(e)
            print('in object getter()')
            pass

def store_the_output(json_output):

    # Copy and paste the URL from MongoDB with your password(between these quotation marks)
    Cluster = ""

    Db = ""  # Write the name of your Data Base(between these quotation marks)

    # Write the name of the Data Base's collection where you want to have your products' descriptions(between these quotation marks)
    Coll = ""

    try:
        cluster = MongoClient(Cluster)
    except:
        print("Wrong URL")
    try:
        db = cluster[Db]
    except:
        print("Wrong Data Base name")
    try:
        collection = db[Coll]
    except:
        print("Wrong collection name")

    wait(2.5)

    collection.insert_one(json_output)

    cluster.close()


if __name__ == "__main__":

    log_in(mail)
    organizer(descriptions, Prefix_for_brand='', suffix_for_brand='', Prefix_for_description='', suffix_for_description='')  # prefix = "", suffix= ""
