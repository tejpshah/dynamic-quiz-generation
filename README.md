# Dynamic Quiz Generation System
This project was created during HackRU Fall 2023.

## Overview
Dive deep into your course materials and unlock tailored quizzes designed just for you. Simply upload your PDF content and let the magic begin. Here's what you'll get:

📄 Bespoke quizzes paired with comprehensive answer keys.
📘 A meticulously crafted study guide, outlining the core content.
💡 An interactive test JSON, perfect for your Streamlit sessions.

At the heart of our system is the mighty GPT-3.5. Harnessing its power, combined with a diverse range of prompts, we ensure quizzes that are challenging, dependable, and finely tuned to your study materials.

Say goodbye to the hassle of manually creating quizzes, passive learning, or the tedium of juggling between multiple AI responses in LLMs. Dive into a study experience that's personalized, efficient, and engineered for success! 🎓🌟

## How to Use the Automated Quiz Generator

Follow these step-by-step instructions to seamlessly generate quizzes from your course materials:

1. **Set Up Your Project**: 
    - Navigate to the `data` directory.
    - Create a new folder named `your-project-name` (replace `your-project-name` with a suitable name for your project).

2. **Add Your PDF Materials**:
    - Place all the relevant course materials in PDF format into the `your-project-name` folder you just created. 
    - Note: Be mindful of the context length limits when adding materials.

3. **Generate Quizzes**:
    - Open your terminal or command prompt.
    - Execute the following command to start generating quizzes:
    ```
    python questionGenerator.py --data_directory data/your-project-name
    ```

4. **Retrieve Generated Outputs**:
    - Once the generation is complete, all the deliverables, including quizzes, answers, and study guides, will be stored in the `output` directory.

5. **Interactive Quiz Experience with Streamlit**:
    - For an interactive quiz-taking experience, run the following command:
    ```
    streamlit run questionInterface.py
    ```