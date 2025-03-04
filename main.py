import streamlit as st
from profiles import get_profile,get_notes,create_profile
from formsubmit import update_personal_info,add_new_note,delete_note
from ask_ai import get_macros,ask_ai
st.title("Personal Fitness tool")

@st.fragment
def personal_data_form():
    with st.form("personal_data"):
        st.header("Personal Data")

        profile=st.session_state.profile
        Name = st.text_input("Name",value=profile["general"]["name"])
        Age = st.number_input("Age",min_value=1,max_value=120,step=1,value=profile["general"]["age"])
        Weight = st.number_input("Weight (kg)",min_value=1.0,max_value=300.0,step=0.1,value=float(profile["general"]["weight"]))
        height = st.number_input("Height (cm)",min_value=1.0,max_value=250.0,step=0.1,value=float(profile["general"]["height"]))
        
        genders=['Male','Female','other']
        gender=st.radio("Gender",genders,genders.index(profile["general"].get("gender","Male")))
        activities=(
            "Sedentary",
            "Lightly active",
            "Moderately Active",
            "Very active",
            "Super active"
        )
        activity_level=st.selectbox("Activity Level",activities,activities.index(profile["general"].get("activity_level","Sedentary")),)

        personal_data_form=st.form_submit_button("Save")

        if personal_data_form:
            if all([Name,Age,Weight,height,gender,activity_level]):
                with st.spinner("Saving your data..."):
                    st.session_state.profile=update_personal_info(profile,"general",name=Name,age=Age,weight=Weight,height=height,gender=gender,activity_level=activity_level)

                    st.success("Data saved successfully")
            
            else:
                st.warning("Please fill all the fields")

@st.fragment
def goals_form():
    profile=st.session_state.profile
    with st.form("goals"):
        st.header("Goals")
        goals=st.multiselect("Select your goals",["Muscle Gain","Fat Loss","Maintain Weight"],
                             default=profile.get("goals",["Maintain Weight"]))
        goals_form=st.form_submit_button("Save")
        if goals_form:
            if goals:
                with st.spinner("Saving your goals..."):
                    st.session_state.profile=update_personal_info(profile,"goals",goals=goals)
                    st.success("Goals saved successfully")
            else:
                st.warning("Please select at least one goal")

st.fragment()
def macros():
    profile=st.session_state.profile
    nutrition=st.container(border=True)
    nutrition.header("Macros")
    if nutrition.button('GenerateWithAI'):
        result=get_macros(profile=profile.get('general'),goals=profile.get('goals'))
        profile["nutrition"]=result
        nutrition.success("AI has generated the results.")
    
    with nutrition.form("nutrition_form",border=False):
        col1,col2,col3,col4=st.columns(4)
        with col1:
            calories=st.number_input("Calories",min_value=0,step=1,value=profile["nutrition"].get("calories",0))
        with col2:
            protein=st.number_input("Protein",min_value=0,step=1,value=profile["nutrition"].get("protein",0))
        with col3:
            fat=st.number_input("Fat",min_value=0,step=1,value=profile["nutrition"].get("fat",0))
        with col4:
            carbs=st.number_input("Carbs",min_value=0,step=1,value=profile["nutrition"].get("carbs",0))
        
        if st.form_submit_button("Save"):
            with st.spinner():
                st.session_state.profile=update_personal_info(profile,"nutrition",protein=protein,calories=calories,fat=fat,carbs=carbs)
                st.success("Info saved")
st.fragment
def notes():
    st.subheader("notes")
    for i,note in enumerate(st.session_state.notes):
        cols=st.columns([5,1])
        with cols[0]:
            st.text(note.get('text'))
        with cols[1]:
            if st.button("Delete",key=i):
                delete_note(note.get("_id"))
                st.session_state.notes.pop(i)
                st.rerun()
    new_note=st.text_input("Add a new note:")
    if st.button("Add note"):
        if new_note:
            note=add_new_note(new_note,st.session_state.profile_id)
            st.session_state.notes.append(note)
            st.rerun()

@st.fragment
def ask_ai_func():
    st.subheader("Ask AI")
    user_question=st.text_input("Ask AI a question")
    if st.button("Ask AI"):
        with st.spinner():
            result=ask_ai(st.session_state.profile,user_question)
            st.write(result)

def forms():
    if "profile" not in st.session_state:
        profile_id=1
        profile=get_profile(profile_id)
        if not profile:
            profile_id,profile=create_profile(profile_id)
        st.session_state.profile=profile
        st.session_state.profile_id=profile_id

    if "notes" not in st.session_state:
        st.session_state.notes=get_notes(st.session_state.profile_id)
  
    personal_data_form()
    goals_form()
    macros()
    notes()
    ask_ai_func()

if __name__ == "__main__":
    forms()