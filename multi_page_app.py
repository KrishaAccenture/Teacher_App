import streamlit as st
import openai
import docx
from docx.shared import Pt
from pptx import Presentation
from pptx.util import Pt as PptPt
from pptx.dml.color import RGBColor
import io
import os

openai.api_key = st.secrets["api_key"]

# Function to generate lesson plan content
def generate_lesson_plan(user_input):
    detailed_prompt = f"""Utilise the teacher's input from the [Teacher Input] widget to generate educational content, adhering to these detailed requirements:
Complete Understanding of UK National Curriculum: thoroughly analyze the UK National Curriculum document "The national curriculum in England - Framework document (publishing.service.gov.uk)" to fully grasp the educational structure and requirements of the UK. This understanding should be reflected in the content's alignment with the curriculum's objectives and standards.
Contextual Analysis of Teacher's Input: Fully comprehend the context of the teacher's request, including the subject, age of students this is targeted to, specific student needs, year group, subject focus, and any special requirements mentioned and also the number of lesson required. Based on all this Produce lesson plan which consists of:  
1.	Success Criteria: These are the specific standards or goals that students are expected to achieve by the end of the lesson. They should be clear, measurable, and achievable. For instance, "Students will be able to solve linear equations with one variable" is a clear success criterion.
2.	Learning Intention/Objective: This is a statement that describes what the students will learn or understand by the end of the lesson. It should be focused and aligned with the curriculum standards. Example: "To understand the life cycle of a butterfly."
3.	Starter Activity/Intro/Assessing Knowledge: This is an activity at the beginning of the lesson to engage students, assess their prior knowledge, and prepare them for the new content. It can be a short discussion, a brainstorming session, or a quick quiz. For example, asking students to list what they know about a topic.
4.	Main Teaching Lesson: This is the core part of the lesson where you present the new information. It should be structured, with clear explanations, examples, and opportunities for students to ask questions. Use varied teaching methods to cater to different learning styles.
5.	Activity: This is a task or set of tasks where students apply what they've learned. It should reinforce the learning intention and success criteria. Activities can be individual or group work, projects, experiments, etc.
6.	Plenary/Key Takeaways/Assessment for Learning Questions: This section is to summarize the lesson, reinforce key points, and assess students' understanding. It can include a group discussion, a reflective activity, or quick questions to gauge learning.
7.	Resources: List all materials and resources needed for the lesson. This includes textbooks, worksheets, technology, etc. Ensure they are accessible and appropriate for the lesson's objectives.
8.	Key Vocabulary: Identify essential terms related to the lesson topic and provide definitions. This helps to build students' subject-specific language and understanding. For example, in a science lesson on ecosystems, key terms might include 'habitat', 'biodiversity', etc.

Resource List: Include a list of materials, drawing inspiration from resources like Twinkl: https://twinkl.com
Language and Grammar Compliance: All generated content must be in British English, maintaining proper spelling and grammar. Ensure everything is in english british selling and grammar.

    Teacher Input: {user_input}"""
    chat_completion = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": detailed_prompt}],
        max_tokens=1000,
        temperature=1.0
    )
    messages = chat_completion['choices'][0]['message']['content']
    return messages

# Function to create a Word document
def create_word_document(content, file_name='document.docx'):
    doc = docx.Document()
    for paragraph in content.split('\n'):
        p = doc.add_paragraph(paragraph)
        p.style.font.size = Pt(12)
    file_stream = io.BytesIO()
    doc.save(file_stream)
    file_stream.seek(0)
    return file_stream

# Function to generate content for PowerPoint slides
def generate_ppt_slides(lesson_plan):
    
    prompt = f"""Ensure everything is in English british spelling and grammar. Create detailed content for an effective PowerPoint presentation based on the lesson plan generated in {lesson_plan}. Structure the slides to match the flow of the lesson, from the starter activity to the plenary questions. It has to have detailed and necessary points for each ppt slide, and it needs to have all the content for the plan - e.g any questions to ask the class, detailed information explaining the concepts, any example questions, the content for any quick games as part of the slide if included. For any images required on the slide it needs to say Image: and then have a concise description of the image required. number the images like Image 1, Image 2 so I can later use another model to create these images. This is the rough structure for it, it must have these slides, but if you feel another sections is required, feel free to add that in as well. there can be more than one slide for each section especially around the main teaching slides, create slides keeping in mind fact of the content tailored for mixed ability children, and special needs. Remember you have to actually write the deatiled content for each slides e.g bullet points, explanations, any questiosn for the children to work throguh in the styarter actviity/ main teaching slide etc… anywhere an image is required just put image and put the decription of the image required there as a bullet point. The teacher simply needs to copy and paste this information to a ppt to present. It needs to have all the information to teach the class, including questions to ask the class - everything/ detailed but also concise and to the point, targeted at the age group os kids mentioned in the teacher input previously. The slide titles needs to be based on what the content is and you do not to need to stick to the header of the section given. 1. Title Slide: (take information from the {lesson_plan}) • Content: Lesson title, date, and class • Tips: Keep it simple and clear. • List the criteria for success in this lesson from the lesson_plan • Clearly state the learning objectives. 2. Starter Activity Slide • Content: Brief instructions for the starter activity. • Tips: Include an engaging image or question to capture interest. 3. Main Teaching Slides • Write the key information, explanations, examples. • Tips: Use visuals like diagrams, charts, and minimal text. Break content into digestible chunks. 4. Activity Instructions Slide • Content: Detailed instructions for the activity. • Tips: Include clear steps and expected outcomes. 5. Plenary Questions Slide • Content: Questions or prompts for the plenary. • Tips: Encourage reflection on the lesson's objectives. 6. Key Vocabulary Slide • Content: List of key terms with definitions. • Tips: Use visual aids to associate words with their meanings. 7. Resources Slide • Content: List of resources used. • Tips: Provide links or references for further reading. 8. Closing Slide • Content: summary of the lesson • Tips: End with a positive note or a preview of the next lesson. there can be more than one slide for each section especially around the main teaching slides, create slides keeping in mind fact of the content tailored for mixed ability children, and special needs. Remember you have to actually write the content for each slides, I simply just want to copy and paste this information to a ppt to present. It needs to have all the information to teach the class, including questions to ask the class - everything."""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "Generate a PowerPoint presentation."},
                  {"role": "user", "content": prompt}],
        max_tokens=1000,
        temperature=0.7
    )
    return response['choices'][0]['message']['content']


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

# Function to generate activity sheets content
def generate_activity_sheets(lesson_plan, parsed_ppt_content):
    
    prompt = f"""Ensure everything is in english british selling and grammar. Create the content for activity sheets for each lesson based on the following lesson plan and PowerPoint presentation content. The activity sheets should contain questions based on the topics covered, tailored for high, medium, and low ability students, including specific accommodations for special educational needs. The content should align with the lesson plan and the PowerPoint content.
    Lesson Plan:
    {lesson_plan}
    PowerPoint Content:
    {parsed_ppt_content}"""
    chat_completion = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1500,
        temperature=0.7
    )
    messages = chat_completion['choices'][0]['message']['content']
    return messages

# Initialize session state variables
if 'lesson_plan_file_stream' not in st.session_state:
    st.session_state['lesson_plan_file_stream'] = None

if 'ppt_file_stream' not in st.session_state:
    st.session_state['ppt_file_stream'] = None

if 'activity_sheet_file_stream' not in st.session_state:
    st.session_state['activity_sheet_file_stream'] = None

if 'lesson_plan_ready' not in st.session_state:
    st.session_state['lesson_plan_ready'] = False

if 'ppt_ready' not in st.session_state:
    st.session_state['ppt_ready'] = False

def main():
    st.title('Lesson and Presentation Generator')

    # Input fields for user details with placeholders
    subject = st.text_input("Subject", placeholder="Enter Subject")
    year_group = st.text_input("Year Group", placeholder="Enter Year Group")
    lesson_topic = st.text_input("Lesson Topic", placeholder="Enter Lesson Topic")
    number_of_lessons_required = st.number_input("Number of Lessons Required", min_value=0, format="%d")
    ability_of_students = st.text_input("Ability of Students", placeholder="Enter Ability of Students")
    special_education_requirements = st.text_area("Special Education Requirements from Children", placeholder="Enter any Special Educational Needs from your Students")
    additional_comments = st.text_area("Additional Comments", placeholder="Any additional comments")

    # File uploader (optional for additional inputs)
    uploaded_files = st.file_uploader("Upload Supporting Files", accept_multiple_files=True,
                                      type=['pdf', 'docx', 'xlsx', 'csv', 'ppt', 'pptx'])

    # Submit button
    if st.button('Click here to generate lesson plan, ppt and activity sheets'):
        # Combine user inputs into a single string
        user_input = f"Subject: {subject}, Year Group: {year_group}, Lesson Topic: {lesson_topic}, Number of Lessons Required: {number_of_lessons_required}, Ability of Students: {ability_of_students}, Special Education Requirements: {special_education_requirements}, Additional Comments: {additional_comments}"
    

        with st.spinner('Creating the lesson plan...'):
              
            lesson_plan = generate_lesson_plan(user_input)
            st.session_state['lesson_plan_file_stream'] = create_word_document(lesson_plan)

        with st.spinner('Generating the PowerPoint...'):
            ppt_content = generate_ppt_slides(lesson_plan)
            parsed_ppt_content = parse_ppt_content(ppt_content)
            st.session_state['ppt_file_stream'] = create_powerpoint(parsed_ppt_content)

        with st.spinner('Creating the activity sheets...'):
            activity_sheet_content = generate_activity_sheets(lesson_plan, parsed_ppt_content)
            st.session_state['activity_sheet_file_stream'] = create_word_document(activity_sheet_content)

        st.success('All materials ready for download!')

    # Download buttons for lesson plan, presentation, and activity sheets
    if st.session_state['lesson_plan_file_stream'] is not None:
        st.download_button(label="Download Lesson Plan",
                        data=st.session_state['lesson_plan_file_stream'],
                        file_name="lesson_plan.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")

    if st.session_state['ppt_file_stream'] is not None:
        st.download_button(label="Download PowerPoint Presentation",
                        data=st.session_state['ppt_file_stream'],
                        file_name="presentation.pptx",
                        mime="application/vnd.openxmlformats-officedocument.presentationml.presentation")

    if st.session_state['activity_sheet_file_stream'] is not None:
        st.download_button(label="Download Activity Sheets",
                        data=st.session_state['activity_sheet_file_stream'],
                        file_name="activity_sheets.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")

if __name__ == "__main__":
    main()

