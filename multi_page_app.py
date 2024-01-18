import streamlit as st
import openai
import docx
from docx.shared import Pt
from pptx import Presentation
from pptx.util import Pt as PptPt
from pptx.dml.color import RGBColor
import io

# Initialize the OpenAI API key
openai.api_key = st.secrets["api_key"]

# Initialize session state variables for history
if 'history' not in st.session_state:
    st.session_state['history'] = []

# Function to update history
def update_history(session_details):
    st.session_state['history'].insert(0, session_details)

# Function to show history entry details
def show_history_entry_details(entry_index):
    entry = st.session_state['history'][entry_index]
    st.write(f"Subject: {entry['user_input']['subject']}, Lesson Topic: {entry['user_input']['lesson_topic']}")
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

# Function to reset user inputs
def reset_user_inputs():
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

# Function to create a Word document
def create_word_document(content):
    # Your code to create a word document from the content
    pass

# Function to create a PowerPoint presentation
def create_powerpoint(content):
    # Your code to create a PowerPoint presentation from the content
    pass

# Sidebar history functionality
def display_sidebar_history():
    with st.sidebar:
        st.header("History")
        if st.button('Start New', key='new_chat'):
            reset_user_inputs()
            st.experimental_rerun()
        
        for i, entry in enumerate(st.session_state['history']):
            if st.button(f"{entry['user_input']['subject']} - {entry['user_input']['lesson_topic']}", key=f"history_btn_{i}"):
                show_history_entry_details(i)

# Main app functionality
def main():
    st.title('Lesson and Presentation Generator')

    # Define user input variables
    user_input = {
        'subject': st.text_input("Subject", value=""),
        'year_group': st.text_input("Year Group", value=""),
        'lesson_topic': st.text_input("Lesson Topic", value=""),
        'number_of_lessons_required': st.number_input("Number of Lessons Required", min_value=1, value=1),
        'ability_of_students': st.text_input("Ability of Students", value=""),
        'special_education_requirements': st.text_area("Special Education Requirements from Children", value=""),
        'additional_comments': st.text_area("Additional Comments", value=""),
    }

    # File uploader (optional for additional inputs)
    uploaded_files = st.file_uploader("Upload Supporting Files", accept_multiple_files=True, type=['pdf', 'docx', 'xlsx', 'csv', 'ppt', 'pptx'])

    # Submit button to generate materials
    if st.button('Click here to generate lesson plan, ppt, and activity sheets'):
        with st.spinner('Creating the lesson plan...'):
            # Your code to generate lesson plan content
            lesson_plan = "Generated lesson plan content"  # Placeholder
            lesson_plan_file_stream = create_word_document(lesson_plan)
            
            # Your code to generate PowerPoint slides content
            ppt_content = "Generated PowerPoint content"  # Placeholder
            ppt_file_stream = create_powerpoint(ppt_content)
            
            # Your code to generate activity sheets content
            activity_sheet_content = "Generated activity sheet content"  # Placeholder
            activity_sheet_file_stream = create_word_document(activity_sheet_content)
            
            # Update history with the new entry
            update_history({
                'user_input': user_input,
                'lesson_plan': lesson_plan,
                'lesson_plan_file_stream': lesson_plan_file_stream,
                'ppt_content': ppt_content,
                'ppt_file_stream': ppt_file_stream,
                'activity_sheet_content': activity_sheet_content,
                'activity_sheet_file_stream': activity_sheet_file_stream
            })
            
            st.success('Materials ready for download!')

    # Check if materials are generated and ready for download
    if 'materials_generated' in st.session_state and st.session_state['materials_generated']:
        show_history_entry_details(0)

# Run the sidebar and main functions
if __name__ == "__main__":
    display_sidebar_history()
    main()
