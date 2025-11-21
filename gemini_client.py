import google.generativeai as genai
import os
from typing import Optional

class GeminiClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-pro')

    def extract_qa_pairs(self, text: str) -> list[dict]:
        """
        Extracts Q&A pairs from raw text using Gemini.
        Returns a list of dictionaries: [{'question': '...', 'answer': '...'}]
        """
        prompt = f"""
You are a data extraction assistant.
Your task is to extract "Question" and "Answer" pairs from the following text.
The text may contain multiple Q&A pairs.

[TEXT START]
{text}
[TEXT END]

### Instructions
1. Identify every distinct Question and its corresponding Answer.
2. If a question is implied but not explicitly stated, infer it from the answer (e.g., "Self-PR").
3. Return the result as a JSON list of objects. Each object must have "question" and "answer" keys.
4. Output ONLY the raw JSON string. No markdown formatting (like ```json).

Example Output:
[
    {{"question": "学生時代に力を入れたこと", "answer": "私は..."}},
    {{"question": "自己PR", "answer": "私の強みは..."}}
]
"""
        try:
            response = self.model.generate_content(prompt)
            import json
            # Clean up potential markdown formatting
            cleaned_text = response.text.replace("```json", "").replace("```", "").strip()
            return json.loads(cleaned_text)
        except Exception as e:
            print(f"Extraction Error: {e}")
            return []

    def generate_es(self, target_company: str, requirements: str, question: str, past_es_history: str, char_limit: Optional[int] = None) -> str:
        """
        Generates a new ES answer based on past history and target requirements.
        """
        
        length_instruction = "Keep it concise and within standard ES limits (approx. 300-400 Japanese characters)."
        if char_limit:
            min_chars = int(char_limit * 0.9)
            length_instruction = f"STRICTLY adhere to the character limit. The output MUST be between {min_chars} and {char_limit} Japanese characters. Do NOT exceed {char_limit} characters."

        prompt = f"""
You are a professional career coach and an expert ghostwriter.
Your task is to write a high-quality Entry Sheet (ES) answer for a job application.

### 1. Context & Assets
Here are the user's past ES answers. Analyze them to understand their:
- **Writing Style**: Tone (assertive/humble), sentence structure, vocabulary, connection logic.
- **Experience Material**: The concrete episodes, skills, and achievements they possess.

[PAST ES DATA START]
{past_es_history}
[PAST ES DATA END]

### 2. Target Information
- **Target Company**: {target_company}
- **Requirements / Persona**: {requirements}
- **Question to Answer**: {question}

### 3. Instructions
Write an answer to the "Question to Answer" that meets the following criteria:
1.  **Style Cloning**: Mimic the user's writing style found in [PAST ES DATA]. Do NOT use generic AI phrases like "It is important to..." or "I would like to contribute...". Write as if the user wrote it.
2.  **Experience Adaptation**: Use the episodes/facts from [PAST ES DATA] but adapt the "angle" or "framing" to fit the {target_company} and {requirements}.
    - If the target values "innovation", frame the experience to highlight creativity.
    - If the target values "grit", frame the same experience to highlight persistence.
3.  **Length**: {length_instruction}
4.  **Language**: MUST be in natural, professional Japanese.

### 4. Output
Output ONLY the generated answer text in Japanese. Do not include explanations or headers.
"""
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating content: {str(e)}"
