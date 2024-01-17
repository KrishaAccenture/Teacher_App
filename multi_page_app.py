import streamlit as st
import openai
import docx
from docx.shared import Pt
from pptx import Presentation
from pptx.util import Pt as PptPt
from pptx.dml.color import RGBColor
import io
import fitz 

# Initialize the OpenAI API key
openai.api_key = st.secrets["api_key"]

# Initialize session state variables for history
if 'history' not in st.session_state:
    st.session_state['history'] = []

# Function to update history
def update_history(user_input, lesson_plan, ppt_content, activity_sheet_content, lesson_plan_file_stream, ppt_file_stream, activity_sheet_file_stream):
    st.session_state['history'].append({
        'user_input': user_input,
        'lesson_plan': lesson_plan,
        'ppt_content': ppt_content,
        'activity_sheet_content': activity_sheet_content,
        'lesson_plan_file_stream': lesson_plan_file_stream,
        'ppt_file_stream': ppt_file_stream,
        'activity_sheet_file_stream': activity_sheet_file_stream
    })

# Function to show history entry details
def show_history_entry_details(entry):
    st.write(f"Subject: {entry['user_input']['subject']}, Lesson Topic: {entry['user_input']['lesson_topic']}")
    st.write("Lesson Plan:")
    st.write(entry['lesson_plan'])
    st.write("PowerPoint Content:")
    st.write(entry['ppt_content'])
    st.write("Activity Sheet Content:")
    st.write(entry['activity_sheet_content'])
    
    # File download functionality tied to history entries
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

# Function to create a Word document
def create_word_document(content):
    doc = docx.Document()
    for paragraph in content.split('\n'):
        p = doc.add_paragraph(paragraph)
        p.style.font.size = Pt(12)
    file_stream = io.BytesIO()
    doc.save(file_stream)
    file_stream.seek(0)
    return file_stream

# Function to create a PowerPoint presentation
def create_powerpoint(ppt_content):
    prs = Presentation()
    title_font_size = PptPt(30)
    content_font_size = PptPt(15)
    title_font_color = RGBColor(0, 51, 102)  # Dark blue
    content_font_color = RGBColor(77, 77, 77)  # Gray
    for slide_info in ppt_content:
        slide_layout = prs.slide_layouts[1]
        slide = prs.slides.add_slide(slide_layout)
        title, content = slide_info['title'], slide_info['content']
        title_shape = slide.shapes.title
        title_shape.text = title
        for paragraph in title_shape.text_frame.paragraphs:
            paragraph.font.size = title_font_size
            paragraph.font.bold = True
            paragraph.font.color.rgb = title_font_color
        content_box = slide.placeholders[1]
        content_box.text = content
        for paragraph in content_box.text_frame.paragraphs:
            paragraph.font.size = content_font_size
            paragraph.font.color.rgb = content_font_color
    file_stream = io.BytesIO()
    prs.save(file_stream)
    file_stream.seek(0)
    return file_stream

# Function to parse the generated content for PowerPoint
def parse_ppt_content(raw_content):
    slides = []
    raw_slides = raw_content.split("\n\n")
    for raw_slide in raw_slides:
        lines = raw_slide.strip().split("\n")
        if len(lines) >= 2:
            title = lines[0].strip()
            content = "\n".join(lines[1:])
            slides.append({'title': title, 'content': content})
    return slides

# Functions for generating lesson plan, PowerPoint slides, and activity sheets
# These are placeholders for your own implementation of these functions.
# They should call the OpenAI API or perform other logic as needed.

# Main app functionality
def main():
    st.title('Lesson and Presentation Generator')

    # "New Page" functionality
    if st.button('Start New'):
        st.session_state['history'] = []
        st.experimental_rerun()

    # Input fields for user details with placeholders
    subject = st.text_input("Subject", placeholder="Enter Subject")
    year_group = st.text_input("Year Group", placeholder="Enter Year Group")
    lesson_topic = st.text_input("Lesson Topic", placeholder="Enter Lesson Topic")
    number_of_lessons_required = st.number_input("Number of Lessons Required", min_value=1, format="%d")
    ability_of_students = st.text_input("Ability of Students", placeholder="Enter Ability of Students")
    special_education_requirements = st.text_area("Special Education Requirements from Children", placeholder="Enter any Special Educational Needs from your Students")
    additional_comments = st.text_area("Additional Comments", placeholder="Any additional comments")

    # File uploader (optional for additional inputs)
    uploaded_files = st.file_uploader("Upload Supporting Files", accept_multiple_files=True,
                                      type=['pdf', 'docx', 'xlsx', 'csv', 'ppt', 'pptx'])

    # Combine user inputs into a dictionary
    user_input = {
        'subject': subject,
        'year_group': year_group,
        'lesson_topic': lesson_topic,
        'number_of_lessons_required': number_of_lessons_required,
        'ability_of_students': ability_of_students,
        'special_education_requirements': special_education_requirements,
        'additional_comments': additional_comments
    }

    # Submit button
    if st.button('Click here to generate lesson plan, ppt, and activity sheets'):
        with st.spinner('Creating the lesson plan...'):
            # Generate lesson plan content
            lesson_plan = "Generated lesson plan content"  # Placeholder for actual content
            lesson_plan_file_stream = create_word_document(lesson_plan)

        with st.spinner('Generating the PowerPoint...'):
            # Generate PowerPoint slides content
            ppt_content = "Generated PowerPoint slides content"  # Placeholder for actual content
            parsed_ppt_content = parse_ppt_content(ppt_content)
            ppt_file_stream = create_powerpoint(parsed_ppt_content)

        with st.spinner('Creating the activity sheets...'):
            # Generate activity sheets content
            activity_sheet_content = "Generated activity sheets content"  # Placeholder for actual content
            activity_sheet_file_stream = create_word_document(activity_sheet_content)

        # Update history with generated content
        update_history(user_input, lesson_plan, ppt_content, activity_sheet_content, lesson_plan_file_stream, ppt_file_stream, activity_sheet_file_stream)
        st.success('All materials ready for download!')

# Display history in the sidebar
def display_sidebar_history():
    with st.sidebar:
        st.header("History")
        for i, entry in enumerate(st.session_state['history']):
            subj = entry['user_input']['subject']
            topic = entry['user_input']['lesson_topic']
            if st.button(f"{subj} - {topic}", key=f"history_btn_{i}"):
                show_history_entry_details(entry)

# Run the sidebar and main functions
if __name__ == "__main__":
    display_sidebar_history()
    main()
