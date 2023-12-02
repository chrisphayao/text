import streamlit as st
from txtai.pipeline import Summary, Textractor
from PyPDF2 import PdfReader

st.set_page_config(layout="wide")

@st.cache_resource
def text_summary(text,minL=None,maxL=None):
    #create summary instance
    summary = Summary()
    text = (text)
    result = summary(text, minlength=minL, maxlength=maxL)
    # result = summary(text)
    return result

def extract_text_from_pdf(file_path):
    # Open the PDF file using PyPDF2
    with open(file_path, "rb") as f:
        reader = PdfReader(f)
        page = reader.pages[0]
        text_p1 = page.extract_text()
        # Initialize an empty string to store concatenated text
        all_text = ""

       # Loop through all pages and extract text
        for page_number in range(len(reader.pages)):
           page = reader.pages[page_number]
           all_text += page.extract_text()
    return text_p1,all_text

def countWords(text):
    # Split the text into words
    words = text.split()
    # Count the number of words
    return len(words)

choice = st.sidebar.selectbox("Select your choice", ["Summarize Text", "Summarize Document"])

if choice == "Summarize Text":
    st.subheader("Summarize Text using txtai")
    input_text = st.text_area("Enter your text here")
    if input_text is not None:
        if st.button("Summarize Text"):
            col1, col2 = st.columns([1,1])
            with col1:
                st.markdown("**Your Input Text**")
                st.info(input_text)
            with col2:
                st.markdown("**Summary Result**")
                result = text_summary(input_text)
                st.success(result)

elif choice == "Summarize Document":
    st.subheader("Summarize Document using txtai")
    input_file = st.file_uploader("Upload your document here", type=['pdf'])
    if input_file is not None:
        if st.button("Summarize Document"):
            with open("doc_file.pdf", "wb") as f:
                f.write(input_file.getbuffer())

            st.info("File uploaded successfully")
            text1,extracted_text = extract_text_from_pdf("doc_file.pdf")
            word_count = countWords(extracted_text)

            st.markdown("**Extracted Text: "+str(word_count)+" words**")
            # show only first page
            st.info(text1)
           
            st.markdown("**Summary Result**")
            doc_summary = text_summary(extracted_text,int(word_count/10),int(word_count/3))
            # word_count = countWords(doc_summary)
            # st.markdown(str(word_count)+" words in summary")
            doc_summary = doc_summary.replace('\n',' ')
            st.success(doc_summary)
