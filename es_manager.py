import json
import os
import streamlit as st
from typing import List, Dict, Optional

DATA_FILE = "es_data.json"

class ESManager:
    def __init__(self):
        self.data_file = DATA_FILE
        self._initialize_session_state()
        self.load_data()

    def _initialize_session_state(self):
        if "past_es" not in st.session_state:
            st.session_state.past_es = []

    def load_data(self):
        """Loads data from JSON file if it exists, otherwise uses session state."""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r", encoding="utf-8") as f:
                    st.session_state.past_es = json.load(f)
            except json.JSONDecodeError:
                st.session_state.past_es = []
        # If file doesn't exist, we rely on session state (which starts empty)

    def save_data(self):
        """Saves current session state data to JSON file."""
        try:
            with open(self.data_file, "w", encoding="utf-8") as f:
                json.dump(st.session_state.past_es, f, ensure_ascii=False, indent=2)
        except Exception as e:
            st.error(f"Failed to save data: {e}")

    def add_es(self, company: str, question: str, answer: str):
        """Adds a new ES record."""
        new_entry = {
            "company": company,
            "question": question,
            "answer": answer
        }
        st.session_state.past_es.append(new_entry)
        self.save_data()

    def delete_es(self, index: int):
        """Deletes an ES record by index."""
        if 0 <= index < len(st.session_state.past_es):
            st.session_state.past_es.pop(index)
            self.save_data()

    def get_all_es(self) -> List[Dict[str, str]]:
        """Returns all past ES records."""
        return st.session_state.past_es

    def get_formatted_history(self) -> str:
        """Formats past ES into a string for the LLM prompt."""
        if not st.session_state.past_es:
            return "No past ES data available."
        
        history_str = ""
        for i, es in enumerate(st.session_state.past_es):
            history_str += f"--- Example {i+1} ---\n"
            history_str += f"Company: {es['company']}\n"
            history_str += f"Question: {es['question']}\n"
            history_str += f"Answer: {es['answer']}\n\n"
        return history_str
