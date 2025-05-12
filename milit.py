import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader
import re

# Configure Gemini API
genai.configure(api_key="AIzaSyDC_0JvqvbhsKvI1YNeeTp_TPjJyMvm2XI")
model = genai.GenerativeModel('gemini-1.5-flash')

class MilitaryDocAnalyzer:
    def __init__(self):
        self.key_sections = {
            'enemy_activity': ['enemy movement', 'troop activity', 'UAV', 'drone'],
            'breach_reports': ['ceasefire violation', 'sniper fire', 'infiltration'],
            'mission_log': ['mission report', 'operation details'],
            'intel_data': ['spy report', 'reconnaissance', 'surveillance'],
        }

    def extract_text(self, uploaded_file):
        if uploaded_file.name.endswith('.pdf'):
            reader = PdfReader(uploaded_file)
            return '\n'.join([page.extract_text() for page in reader.pages])
        else:
            raise ValueError("Unsupported file format. Only PDFs are allowed.")

    def find_sections(self, text):
        results = {}
        for section, keywords in self.key_sections.items():
            pattern = r'(?i)({}).*?(?=\n\s*\n|$)'.format('|'.join(keywords))
            match = re.search(pattern, text, re.DOTALL)
            if match:
                results[section] = match.group(0).strip()
        return results

    def analyze_text(self, text, prompt):
        return model.generate_content(prompt + text).text

    def summarize_doc(self, text):
        prompt = "Summarize this military document in 4 bullet points with military terminology:\n"
        return self.analyze_text(text, prompt)

    def identify_threats(self, text):
        prompt = "List potential threats, enemy movements, drone activity, or breaches found in this report:\n"
        return self.analyze_text(text, prompt)

    def suggest_responses(self, text):
        prompt = "Suggest military response actions based on this report:\n"
        return self.analyze_text(text, prompt)

# Streamlit UI
st.set_page_config(page_title="🪖 MILINT AI – Military Intelligence Analyzer", layout="wide")
st.title("🪖 MILINT AI Agent – Military Intelligence Document Analyzer")
st.write("Upload military reports or intercepted documents for threat assessment and summarization")

uploaded_file = st.file_uploader("📄 Upload PDF Military Document", type=['pdf'])

if uploaded_file:
    analyzer = MilitaryDocAnalyzer()
    
    with st.spinner("🛰️ Analyzing Document..."):
        try:
            text = analyzer.extract_text(uploaded_file)
            sections = analyzer.find_sections(text)

            st.success("✅ Analysis Complete!")
            st.subheader("📌 Document Summary")
            st.write(analyzer.summarize_doc(text))

            st.subheader("⚠️ Identified Threats")
            st.write(analyzer.identify_threats(text))

            st.subheader("🛡️ Suggested Responses")
            st.write(analyzer.suggest_responses(text))

            st.divider()
            st.subheader("📂 Raw Sections")
            for sec, content in sections.items():
                st.markdown(f"**{sec.upper()}**")
                st.code(content)

        except Exception as e:
            st.error(f"Error during analysis: {str(e)}")
