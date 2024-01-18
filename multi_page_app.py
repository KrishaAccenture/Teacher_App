import streamlit as st
import openai
import docx
from docx.shared import Pt
from pptx import Presentation
from pptx.util import Pt as PptPt
from pptx.dml.color import RGBColor
import io

# Initialize the OpenAI API key
openai.api_key = st.secrets["openai_api_key"]

# Initialize session state variables for history
if 'history' not in st.session_state:
    st.session_state['history'] = []

# Function to update history
def update_history(session_details):
    st.session_state['history'].insert(0, session_details)

# Function to generate lesson plan, PowerPoint, and activity sheets
# Replace this with your actual OpenAI call and document generation
def generate_materials(user_input):
    lesson_plan = "Generated lesson plan content"  # Placeholder
    ppt_content = "Generated PowerPoint content"  # Placeholder
    activity_sheet_content = "Generated activity sheet content"  # Placeholder

    lesson_plan_file_stream = create_word_document(lesson_plan)
    ppt_file_stream = create_powerpoint(ppt_content)
    activity_sheet_file_stream = create_word_document(activity_sheet_content)

    return lesson_plan, lesson_plan_file_stream, ppt_content, ppt_file_stream, activity_sheet_content, activity_sheet_file_stream

# Function to show history entry details
def show_history_entry_details(entry):
    st.write(f"Subject: {entry['subject']}, Lesson Topic: {entry['lesson_topic']}")
    st.download_button(label="Download Lesson Plan",
                       data=entry['lesson_plan_file_stream'],
                       file_name="lesson_plan.docx",
                       mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
    st.download_button(label="Download PowerPoint Presentation",
                       data=entry['ppt_file_stream'],
                       file_name="presentation.pptx",
                       mime="application/vnd.openxmlformats-officedocument.presentationml.presentation")
    st.download_button(label="Download Activity Sheets",
                       data=entry['activity_sheet_file_stream'],
                       file_name="activity_sheets.docx",
                       mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")

# Main app functionality
def main():
    st.title('Lesson and Presentation Generator')

    # Input fields for user details with placeholders
    if 'user_input' not in st.session_state:
        st.session_state.user_input = {
            'subject': '',
            'year_group': '',
            'lesson_topic': '',
            'number_of_lessons_required': 1,
            'ability_of_students': '',
            'special_education_requirements': '',
            'additional_comments': '',
            'materials_generated': False
        }

    subject = st.text_input("Subject", st.session_state.user_input['subject'])
    year_group = st.text_input("Year Group", st.session_state.user_input['year_group'])
    lesson_topic = st.text_input("Lesson Topic", st.session_state.user_input['lesson_topic'])
    number_of_lessons_required = st.number_input("Number of Lessons Required", min_value=1, value=st.session_state.user_input['number_of_lessons_required'])
    ability_of_students = st.text_input("Ability of Students", st.session_state.user_input['ability_of_students'])
    special_education_requirements = st.text_area("Special Education Requirements from Children", st.session_state.user_input['special_education_requirements'])
    additional_comments = st.text_area("Additional Comments", st.session_state.user_input['additional_comments'])

    # File uploader (optional for additional inputs)
    uploaded_files = st.file_uploader("Upload Supporting Files", accept_multiple_files=True, type=['pdf', 'docx', 'xlsx', 'csv', 'ppt', 'pptx'])

    # Submit button to generate materials
    if st.button('Click here to generate lesson plan, ppt, and activity sheets'):
        with st.spinner('Creating the lesson plan...'):
            # Save user input in session state
            st.session_state.user_input = {
                'subject': subject,
                'year_group': year_group,
                'lesson_topic': lesson_topic,
                'number_of_lessons_required': number_of_lessons_required,
                'ability_of_students': ability_of_students,
                'special_education_requirements': special_education_requirements,
                'additional_comments': additional_comments,
                'materials_generated': True
            }

            # Generate materials
            materials = generate_materials(st.session_state.user_input)
            
            # Update history with the new entry
            update_history({
                'subject': subject,
                'year_group': year_group,
                'lesson_topic': lesson_topic,
                'lesson_plan': materials[0],
                'lesson_plan_file_stream': materials[1],
                'ppt_content': materials[2],
                'ppt_file_stream': materials[3],
                'activity_sheet_content': materials[4],
                'activity_sheet_file_stream': materials[5]
            })
            
            st.success('Materials ready for download!')
    
    # Show generated materials if available
    if st.session_state.user_input['materials_generated']:
        show_history_entry_details(st.session_state.history[0])

# Sidebar history functionality
def display_sidebar_history():
    with st.sidebar:
        st.header("History")
        if st.button('Start New', key='new_chat'):
            # Reset the session state for user input
            st.session_state.user_input = {
                'subject': '',
                'year_group': '',
                'lesson_topic': '',
                'number_of_lessons_required': 1,
                'ability_of_students': '',
                'special_education_requirements': '',
                'additional_comments': '',
                'materials_generated': False
            }
            st.experimental_rerun()
        
        for i, entry in enumerate(st.session_state['history']):
            if st.button(f"{entry['subject']} - {entry['lesson_topic']}", key=f"history_btn_{i}"):
                show_history_entry_details(entry)

# Run the sidebar and main functions
if __name__ == "__main__":
    display_sidebar_history()
    main()
