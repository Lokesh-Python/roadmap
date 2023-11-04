import streamlit as st

from utils import ui
st.set_page_config(page_title="Roadmap")

st.title("Roadmap")

if not "selected_roadmap_index" in st.session_state:
    ui.initialize_session_variables()
    st.session_state.roadmap_list = ui.generate_roadmap_list()
    st.markdown("**How to use**")
    st.markdown("- Select a roadmap from the dropdown in the sidebar")
    st.markdown("- A list of topic will appear")
    st.markdown("- Choose your level of expertise for each topic")
    st.markdown("- If you are clueless of what to choose, toggle **I want to test my knowledge** button")
    st.markdown("- A set of 5 questions will appear, answer all of them and based on your result your expertise will be selected")
    st.markdown("- Once done, Click on Generate Summary button to view the result")
    st.markdown("- All the best")
roadmap_list = st.session_state.roadmap_list
try:
    selected_roadmap = st.sidebar.selectbox("Select Roadmap", options=roadmap_list, index = None, disabled=st.session_state.selected_roadmap_disable)

    st.session_state.selected_roadmap = selected_roadmap

    if selected_roadmap and not st.session_state.roadmap_generated:  
        st.session_state.selected_roadmap_disable = True  
        roadmap = ui.generate_roadmap_topics(selected_roadmap)
        st.session_state.roadmap = roadmap
        st.session_state.roadmap_generated = True
        
except:
    print("Error while loading roadmap list")

if st.session_state.roadmap != []:
    st.session_state.summary = st.button("Generate Summary", disabled= st.session_state.summary_disabled)


if st.session_state.roadmap != [] and not st.session_state.summary :
    for ind_topic, topic in enumerate(st.session_state.roadmap):
        if not topic in st.session_state.selected_topic:
            st.session_state.selected_topic[topic] = 0
        if not topic in st.session_state.toggle_disable:
            st.session_state.toggle_disable[topic] = False
        st.write("---")
        test_me = st.toggle("I want to test my knowledge", key=topic, disabled=st.session_state.toggle_disable[topic])
        if test_me and not st.session_state.toggle_disable[topic]:
           submit_test_me = st.button("Double Click to Submit", key = ind_topic)
        if st.session_state.toggle_disable[topic]:
            st.write(f"Your score is {st.session_state.percentage[topic]}")
        try:
            st.session_state.result[topic] = st.selectbox(label=topic, options=["New to me", "Basic", "Intermediate", "Expert"], index=st.session_state.selected_topic[topic])
        except:
            print("Error while loading roadmap topics")
        if test_me and not st.session_state.toggle_disable[topic]:
            if not (topic in st.session_state.response_test_me):
                response_test_me = ui.generate_roadmap_topic_questions(topic)
                response_test_me.append({"selectedOptions" : {}})
                response_test_me.append({"status" : {}})
                st.session_state.response_test_me[topic] = response_test_me
            ques_and_ans = st.session_state.response_test_me[topic]
            level_value = 0
            for ind in range(0,5):
                try:
                    selectedOption = ques_and_ans[5]
                    if not ind in selectedOption:
                        selectedOption[ind] = None
                    st.write("---")
                    st.markdown(f"**{ques_and_ans[ind]['question']}**")
                    st.markdown(f"Level : **{ques_and_ans[ind]['level'].upper()}**")
                    Options = ques_and_ans[ind]['Options']
                    value = st.radio(label = "", key = topic + str(ind), options=Options, index = selectedOption[ind])
                    level_value = ui.calculate_level_value(ques_and_ans, level_value, ind)
                    if value:
                        ques_and_ans[6]["status"][ind] = ui.validate_answer(selectedOption, ques_and_ans, ind, value)
                    else:
                        ques_and_ans[6]["status"][ind] = 0
                except:
                    print("Error while loading roadmap topic questions")
            st.session_state.response_test_me[topic] = ques_and_ans
            if submit_test_me:
                st.session_state.toggle_disable[topic] = True
                ui.calculate_test_me_result(ques_and_ans, level_value, topic)



if st.session_state.summary:
    st.session_state.summary_disabled = True
    search = ui.search_key()
    summary_response = ui.summary_content(search)
    ui.print_summary(summary_response)