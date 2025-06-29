import streamlit as st
from pdfminer.high_level import extract_text
from transformers import pipeline
import nltk

# Download punkt tokenizer if not present
try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt")

from nltk.tokenize import sent_tokenize

st.set_page_config(page_title="Smart Document Assistant", layout="wide")
st.title("📄 Smart Document Assistant")

uploaded_file = st.file_uploader("Upload a PDF or TXT document", type=["pdf", "txt"])

def extract_pdf_text(file_obj):
    return extract_text(file_obj)

@st.cache_resource(show_spinner=False)
def load_models():
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    qa_pipeline = pipeline("question-answering", model="distilbert-base-cased-distilled-squad")
    question_generator = pipeline("text-generation", model="gpt2")
    return summarizer, qa_pipeline, question_generator

if uploaded_file is not None:
    st.success("✅ File uploaded successfully!")

    if uploaded_file.type == "application/pdf":
        text = extract_pdf_text(uploaded_file)
    elif uploaded_file.type == "text/plain":
        text = uploaded_file.read().decode("utf-8")
    else:
        st.error("Unsupported file type!")
        st.stop()

    st.subheader("📜 Extracted Text Preview")
    st.text_area("Text Content", text[:3000], height=300)

    summarizer, qa_pipeline, question_generator = load_models()

    st.subheader("📝 Document Summary")
    if len(text) > 500:
        summary = summarizer(text[:2000], max_length=150, min_length=50, do_sample=False)
        st.success(summary[0]["summary_text"])
    else:
        st.warning("Text too short to summarize.")

    # === Ask Anything Section ===
    st.subheader("❓ Ask Anything")
    user_question = st.text_input("Ask a question based on the document:")
    if user_question:
        try:
            answer = qa_pipeline(question=user_question, context=text)
            st.write("**Answer:**", answer["answer"])
        except Exception as e:
            st.error(f"Error getting answer: {e}")

    # === Challenge Me Section ===
    st.subheader("🧠 Challenge Me")

    if "questions" not in st.session_state:
        st.session_state.questions = []
    if "correct_answers" not in st.session_state:
        st.session_state.correct_answers = []
    if "user_answers" not in st.session_state:
        st.session_state.user_answers = [""] * 3
    if "evaluation_done" not in st.session_state:
        st.session_state.evaluation_done = False

    def generate_questions_and_answers():
        prompt = f"Generate 3 logic or comprehension questions from this document:\n{text[:1000]}"
        result = question_generator(prompt, max_length=300, num_return_sequences=1)
        generated_text = result[0]["generated_text"]

        try:
            questions = sent_tokenize(generated_text)
        except Exception:
            questions = []

        questions = questions[:3]

        st.session_state.questions = questions
        st.session_state.correct_answers = []
        for q in questions:
            try:
                answer = qa_pipeline(question=q, context=text)["answer"]
            except Exception:
                answer = "N/A"
            st.session_state.correct_answers.append(answer)
        st.session_state.user_answers = [""] * len(questions)
        st.session_state.evaluation_done = False

    if st.button("Generate Questions"):
        generate_questions_and_answers()

    if st.session_state.questions:
        for i, question in enumerate(st.session_state.questions, 1):
            st.markdown(f"**Q{i}: {question}**")
            st.session_state.user_answers[i-1] = st.text_input(f"Your answer to Q{i}", value=st.session_state.user_answers[i-1], key=f"answer_{i}")

        if st.button("Evaluate Answers"):
            st.session_state.evaluation_done = True

    if st.session_state.evaluation_done:
        st.markdown("### 🧪 Evaluation Results")
        for i, (q, user_ans, correct_ans) in enumerate(zip(st.session_state.questions, st.session_state.user_answers, st.session_state.correct_answers), 1):
            user_ans_clean = user_ans.strip().lower()
            correct_ans_clean = correct_ans.strip().lower()
            if user_ans_clean == correct_ans_clean:
                st.success(f"Q{i}: ✅ Correct!")
            else:
                st.error(f"Q{i}: ❌ Incorrect!")
            st.write(f"**Correct Answer:** {correct_ans}")

else:
    st.info("Please upload a document to begin.")
