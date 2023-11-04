import streamlit as st
import requests
import json
from config import settings 
from requests.auth import HTTPBasicAuth

def initialize_session_variables():
    st.session_state.selected_roadmap_index = None
    st.session_state.roadmap_generated = False
    st.session_state.roadmap = []
    st.session_state.selected_roadmap_disable = False
    st.session_state.summary = False
    st.session_state.summary_disabled = False
    st.session_state.result = {}
    st.session_state.response_test_me = {}
    st.session_state.selected_topic = {}
    st.session_state.toggle_disable = {}
    st.session_state.percentage = {}

def generate_roadmap_list():
    try:
        roadmap_list_url = settings.api_host + settings.api_roadmap_path
        return (requests.request("GET", roadmap_list_url, auth=HTTPBasicAuth(str(settings.api_username), str(settings.api_password)))).json()["items"]
    except:
        st.error("chatGpt results are inconsistent, Refresh the page to restart")
def generate_roadmap_topics(selected_roadmap):
    try:
        roadmap_url = settings.api_host + settings.api_roadmap_path + f"/{selected_roadmap}"
        result = (requests.request("GET", roadmap_url, auth=HTTPBasicAuth(settings.api_username, settings.api_password))).json()["items"]
        return result
    except:
        st.error("chatGpt results are inconsistent, Refresh the page to restart")

def generate_roadmap_topic_questions(topic):
    try:
        test_me_url = settings.api_host + settings.api_questions_path + f"?topic={topic}"
        return (requests.request("GET", test_me_url, auth=HTTPBasicAuth(settings.api_username, settings.api_password))).json()["questions"]
    except:
        st.error("chatGpt results are inconsistent, Refresh the page to restart")

def calculate_level_value(ques_and_ans,level_value, ind):
    level = ques_and_ans[ind]["level"].upper()
    if level == "BASIC":
        level_value = level_value + 10
    elif level == "INTERMEDIATE":
        level_value = level_value + 20
    elif level == "HARD":
        level_value = level_value + 30
    return level_value

def validate_answer(selectedOption, ques_and_ans, ind, value):
    selectedOption[ind] = ques_and_ans[ind]["Options"].index(value)
    correct_answer = ques_and_ans[ind]["Options"].index(ques_and_ans[ind]["Answer"])
    status = 0
    level = ques_and_ans[ind]["level"].upper()
    if selectedOption[ind] == correct_answer:
        if level == "BASIC":
           status = 10
        elif level == "INTERMEDIATE":
            status = 20
        elif level == "HARD":
            status = 30
    else:
        status = 0
    return status

def calculate_test_me_result(ques_and_ans, level_value, topic):
    result = 0
    for ind in range(0,5):
        result = result + ques_and_ans[6]["status"][ind]
    percentage = ( result / level_value ) * 100
    st.session_state.percentage[topic] = percentage
    if percentage >= 70:
        st.session_state.result[topic] = "Expert"
        st.session_state.selected_topic[topic] = 3
    elif 70 > percentage >= 30 :
        st.session_state.result[topic] = "Intermediate"
        st.session_state.selected_topic[topic] = 2
    elif 30 > percentage > 20 :
        st.session_state.result[topic] = "Basic"
        st.session_state.selected_topic[topic] = 1
    else:
        st.session_state.result[topic] = "New to me"
        st.session_state.selected_topic[topic] = 0

def search_key():
    search = ""
    for key, value in list(st.session_state.result.items()):
        if value != "New to me":
            search = search + key + " in " + value + " level, "
    return search

def summary_content(search):
    try:
        roadmap_summary_url = settings.api_host + settings.api_roadmap_path + "/summary"
        payload = json.dumps({
        "expertise": search,
        "role": st.session_state.selected_roadmap
        })
        headers = {
        'Content-Type': 'application/json'
        }
        response = requests.request("POST", roadmap_summary_url, headers=headers, data=payload, auth=HTTPBasicAuth(settings.api_username, settings.api_password))
        print(payload)
        print(response)
        return response.json()
    except:
        st.error("chatGpt results are inconsistent, Refresh the page to restart")

def print_summary(response):
    try:
        st.write("**Your Advantages**")
        for adv in response["Advantages"]:
            st.markdown(f"- {adv}")
        st.write("**Where to Concentrate**")
        for con in response["Concentrate"]:
            st.markdown(f"- {con}")
        st.write("**Overall Summary**")
        st.write(response["summary"])
    except:
        print("Error while loading summary")