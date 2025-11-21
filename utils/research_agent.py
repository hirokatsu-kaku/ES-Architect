import google.generativeai as genai
from duckduckgo_search import DDGS
import time

class ResearchAgent:
    def __init__(self, api_key: str):
        self.api_key = api_key
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-pro')

    def search_company(self, company_name: str) -> str:
        """
        Searches for company information and returns a summary of the 'Target Persona'.
        """
        results = []
        queries = [
            f"{company_name} 企業理念",
            f"{company_name} 求める人物像",
            f"{company_name} 採用サイト"
        ]

        with DDGS() as ddgs:
            for query in queries:
                try:
                    # Fetch top 3 results for each query
                    search_results = list(ddgs.text(query, max_results=3))
                    for r in search_results:
                        results.append(f"Title: {r['title']}\nSnippet: {r['body']}")
                    time.sleep(1) # Be polite
                except Exception as e:
                    print(f"Search error for {query}: {e}")

        if not results:
            return "企業情報の検索に失敗しました。手動で入力してください。"

        # Synthesize with Gemini
        raw_text = "\n\n".join(results)
        prompt = f"""
You are an expert corporate analyst.
Analyze the following search results about "{company_name}" and extract the "Target Persona" (求める人物像) and "Corporate Culture" (社風).

[SEARCH RESULTS START]
{raw_text}
[SEARCH RESULTS END]

### Instructions
Summarize the findings into a concise paragraph (approx. 200 characters) describing what kind of person this company is looking for.
Focus on keywords like "Challenge", "Teamwork", "Innovation", "Grit", etc.
Output MUST be in Japanese.
"""
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"分析中にエラーが発生しました: {str(e)}"
