Docx_flask_app
==============

Smart Document Assistant

A Python-based smart assistant that allows users to upload a PDF or TXT document and interact with it using natural language. The app can extract content, summarize it, answer user questions based on the document, and generate logical questions for self-evaluation.

Features
--------

1. Upload a document (PDF or TXT)
2. Automatically extract and preview the text
3. Generate a concise summary using AI
4. Ask questions based on the document content
5. Automatically generate 3 logic/comprehension questions from the content
6. Evaluate your answers against correct ones using NLP models

Technologies Used
-----------------

- Python
- Streamlit (UI)
- Hugging Face Transformers:
  - facebook/bart-large-cnn (summarization)
  - distilbert-base-cased-distilled-squad (question answering)
  - gpt2 (question generation)
- nltk (tokenization)
- pdfminer.six (PDF text extraction)

Project Structure
-----------------

Docx_flask_app/
├── app.py              # Main application code
├── requirements.txt    # List of dependencies
├── .gitignore          # Ignore unnecessary files like venv/
└── README.txt          # This file

How to Run the App
------------------

1. Clone the repository and move into the project folder

2. Create and activate a virtual environment:
   - For Windows:
     python -m venv venv
     venv\Scripts\activate

   - For macOS/Linux:
     python3 -m venv venv
     source venv/bin/activate

3. Install dependencies:
   pip install -r requirements.txt

4. Run the app:
   streamlit run app.py

Best Practices
--------------

- I Didn't NOT upload the virtual environment (venv) folder.


Credits
-------

Developed by Gsm Ravi Charan using Hugging Face models and open-source tools.
