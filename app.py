import streamlit as st
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

st.set_page_config(
    page_title="ES Architect",
    page_icon="✍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

from utils.design_utils import load_design

# Load environment variables
load_dotenv()

st.set_page_config(
    page_title="ES Architect",
    page_icon="✍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load Design (CSS + JS)
load_design()

# Hero Section
col1, col2 = st.columns([1.2, 1])

with col1:
    st.title("ES Architect")
    st.markdown("""
    <div class="hero-text">
    あなたの「文体」と「経験」を資産化し、<br>
    最強のエントリーシートを生成するAIアシスタント。
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("""
    <div style="animation: slideUp 0.8s ease-out 0.4s forwards; opacity: 0;">
    
    ### 🚀 はじめに
    
    **1. 資産を貯める**  
    サイドバーの **「🗂️ ESリスト管理」** から、過去に書いたESを登録してください。
    
    **2. ESを作る**  
    サイドバーの **「✨ ES作成」** から、志望企業と設問を入力してください。
    AIが企業情報を自動で調査し、あなたの経験を最適化して出力します。
    
    </div>
    """, unsafe_allow_html=True)

with col2:
    # Display Hero Image
    st.image("assets/hero_main.png", use_container_width=True)

st.markdown("---")

# Features Section with Images
st.subheader("✨ 主な機能")
f_col1, f_col2 = st.columns(2)

with f_col1:
    st.image("assets/feature_assets.png", use_container_width=True)
    st.markdown("""
    ### 🗂️ 資産管理
    過去のESをデータベース化。企業ごとに整理し、あなたの「勝ちパターン」を蓄積します。
    """)

with f_col2:
    st.image("assets/feature_generator.png", use_container_width=True)
    st.markdown("""
    ### ⚡️ AI生成
    志望企業の「求める人物像」を自動分析。あなたの経験を最適な文脈で再構成します。
    """)

st.markdown("---")
st.caption("ES Architect © 2025 | Powered by Google Gemini")
