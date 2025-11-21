import streamlit as st
from utils.es_manager import ESManager
from utils.gemini_client import GeminiClient
from utils.research_agent import ResearchAgent
import os
from dotenv import load_dotenv
from utils.design_utils import load_design

# Load environment variables
load_dotenv()

st.set_page_config(page_title="ES作成", page_icon="✨", layout="wide")

# Load Design
load_design()

# Initialize
es_manager = ESManager()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.error("APIキーが設定されていません。.envファイルを確認してください。")
    st.stop()

gemini_client = GeminiClient(api_key)
research_agent = ResearchAgent(api_key)

st.title("✨ ES作成")
st.markdown("""
<div style="animation: fadeIn 1s ease-out;">
志望企業に合わせて、あなたの経験を最適化したESを生成します。
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("🎯 ターゲット設定")
    target_company = st.text_input("志望企業名", placeholder="例: 株式会社〇〇")
    
    st.markdown("**求める人物像 / 募集要項 (任意)**")
    st.caption("企業HPや募集要項の文章を貼り付けると、より精度が上がります。未入力でもAIが自動調査します。")
    manual_requirements = st.text_area("manual_req", label_visibility="collapsed", height=150)
        
    target_question = st.text_area("今回の設問", placeholder="例: 学生時代に最も力を入れたことは何ですか？", height=100)
    
    # Character Limit Selector
    char_options = [None, 200, 300, 400, 500, 600, 800, 1000]
    char_limit = st.selectbox(
        "文字数制限 (任意)", 
        char_options, 
        format_func=lambda x: "指定なし" if x is None else f"{x}文字以内"
    )
    
    generate_btn = st.button("✨ ESを生成する", type="primary", use_container_width=True)

with col2:
    st.subheader("📝 生成結果")
    
    if generate_btn:
        existing_es = es_manager.get_all_es()
        
        if not target_company or not target_question:
            st.error("企業名と設問は必須です。")
        elif not existing_es:
            st.error("「ESリスト管理」ページで、過去のESを少なくとも1つ追加してください。")
        else:
            # 1. Auto-Research (Always runs)
            researched_info = ""
            with st.spinner(f"{target_company} について調査中..."):
                researched_info = research_agent.search_company(target_company)
            
            # Combine Manual + Auto
            final_requirements = f"""
            [User Input Requirements]
            {manual_requirements if manual_requirements else "None provided."}
            
            [AI Researched Info]
            {researched_info}
            """
            
            # 2. Generate ES
            with st.spinner("あなたのスタイルを分析し、最適な回答を作成中..."):
                history_str = es_manager.get_formatted_history()
                generated_text = gemini_client.generate_es(
                    target_company, 
                    final_requirements, 
                    target_question, 
                    history_str,
                    char_limit=char_limit
                )
                
                st.markdown(f"""
                <div class="es-card">
                    <div class="es-card-title">生成された回答</div>
                    <div class="es-card-content">{generated_text}</div>
                </div>
                """, unsafe_allow_html=True)
                
                st.code(generated_text, language="text")
                st.caption("上のテキストをコピーして使用してください。")
