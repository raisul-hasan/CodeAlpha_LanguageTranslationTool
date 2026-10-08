
# 🌍 LinguaAI — Language Translation Tool

A multilingual AI-powered translation application developed for the CodeAlpha Artificial Intelligence Internship.

## 🚀 Features

- Translation between 20 languages
- Automatic source language detection
- Microsoft Azure Translator API integration
- Modern, colorful Streamlit interface
- 5,000-character input limit
- Clear text functionality
- User-friendly error handling

## 🛠️ Technologies Used

- Python
- Streamlit
- Microsoft Azure Translator API
- Requests
- Python Dotenv

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/CodeAlpha_LanguageTranslationTool.git
```

Install the required packages:

```bash
pip install -r requirements.txt
```

Create a `.env` file containing:

```env
AZURE_TRANSLATOR_KEY=your_api_key
AZURE_TRANSLATOR_REGION=your_region
AZURE_TRANSLATOR_ENDPOINT=https://api.cognitive.microsofttranslator.com
```

Run the application:

```bash
python -m streamlit run app.py
```

## 📌 Internship Information

**Organization:** CodeAlpha  
**Domain:** Artificial Intelligence  
**Task 1:** Language Translation Tool

## 🔐 Security

API credentials are stored in environment variables and excluded from GitHub using `.gitignore`.
