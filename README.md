# AI Customized Learning Recommendation Chatbot

## 🚧 Work in Progress 🚧

This project is actively being developed for the **Kathmandu University AI Education Innovation Bootcamp & Hackathon X Chunjae Education**. Please note that features are still being implemented and may be subject to change.

## 🚀 Project Overview
Welcome to our project, developed as part of the Kathmandu University AI Education Innovation Bootcamp & Hackathon X Chunjae Education!

This project is an AI-powered Customized Learning Recommendation Chatbot designed to help users master different topics. It provides personalized quizzes, instant feedback, and tailored study recommendations to help learners identify knowledge gaps, improve retention, and enhance their learning process.
The chatbot leverages Large Language Models (LLMs) to dynamically generate content and offers a conversational user interface for an engaging, adaptive learning experience.

## ✨ Key Features
- Interactive Chat-based UI: A simple, conversational interface for a natural learning experience.
- Dynamic Quiz Generation: Quizzes are created on the fly based on user-selected topics and their self-assessed skill level.
- Instant Feedback: Users receive immediate feedback on their answers, complete with explanations for better understanding.
- Personalized Recommendations: Based on quiz performance, the chatbot provides a customized study plan with suggestions for additional resources and practice tasks.

## 💻 Technology Stack
- Frontend: HTML, CSS, and JavaScript
- Backend: Flask (Python)
- LLM Framework: LangChain
- LLM Provider: Google Gemini or Groq

## 📋 Getting Started
<u>Prerequisites:</u>
- Python 3.9+
- A valid API key for either Google Gemini or Groq.

<u>Installation:</u>
1. Clone the repository:
    ```
    git clone https://github.com/AI-Learning-Chatbot/AI-Customized-Learning-Recommendation-Chatbot.git
    ```

2. Set up a Virtual Enviroment and activate it:
    ```
    python -m venv env
    ```
    ```
    env/scripts/activate
    #for linux
    source venv/bin/activate
    ```

3. Install the required libraries:
    ```
    pip install -r requirements.txt
    ```

4. Configure your Gemini API KEY:
    - Create a .env file in the root directory.
    - Add your Google API key in the following format:
    ```
    GOOGLE_API_KEY=YOUR_API_KEY_HERE
    ```