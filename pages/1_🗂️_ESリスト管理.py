import streamlit as st
from utils.es_manager import ESManager
import os

st.set_page_config(page_title="ESリスト管理", page_icon="🗂️", layout="wide")

from utils.design_utils import load_design

st.set_page_config(page_title="ESリスト管理", page_icon="🗂️", layout="wide")

# Load Design
load_design()

es_manager = ESManager()

st.title("🗂️ ESリスト管理")
st.markdown("""
<div style="animation: fadeIn 1s ease-out;">
過去のESを登録・管理します。
</div>
""", unsafe_allow_html=True)

# Add New ES Form
# Sidebar for Sync
with st.sidebar:
    st.markdown("### ☁️ GitHub同期")
    
    from utils.config import get_env_var
    github_token = get_env_var("GITHUB_TOKEN")
    if not github_token:
        st.warning("GitHubトークンが設定されていません。")
        st.info("`.env`ファイルに `GITHUB_TOKEN` を追加してください。")
    else:
        from utils.github_sync import GitHubSync
        syncer = GitHubSync(github_token)
        
        col_sync1, col_sync2 = st.columns(2)
        
        with col_sync1:
            if st.button("⬆️ 保存", help="現在のデータをGitHubにバックアップします"):
                with st.spinner("バックアップ中..."):
                    all_data = es_manager.get_all_es()
                    msg = syncer.upload_data(all_data)
                    if "✅" in msg:
                        st.success(msg)
                    else:
                        st.error(msg)
        
        with col_sync2:
            if st.button("⬇️ 復元", help="GitHubからデータを復元します（上書き注意）"):
                with st.spinner("復元中..."):
                    data, msg = syncer.download_data()
                    if data:
                        es_manager.save_all_es(data)
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)

# Main Content
with st.expander("➕ 新しいESを追加", expanded=True):
    st.subheader("ES登録")
    
    # Initialize Gemini Client for extraction
    from utils.gemini_client import GeminiClient
    from utils.config import get_env_var
    api_key = get_env_var("GOOGLE_API_KEY")
    
    existing_es = es_manager.get_all_es()
    existing_companies = sorted(list(set([es['company'] for es in existing_es])))
    
    input_mode = st.radio("企業選択", ["既存の企業から選ぶ", "新しい企業を追加"], horizontal=True)
    
    if input_mode == "既存の企業から選ぶ" and existing_companies:
        company = st.selectbox("企業名", existing_companies)
    else:
        company = st.text_input("企業名 (新規)")
    
    st.markdown("---")
    st.markdown("##### 📝 ESデータの入力")
    st.caption("設問と回答をまとめて貼り付けてください。AIが自動でペアを抽出します。")
    
    bulk_text = st.text_area("ESテキスト（設問と回答を含む全文）", height=200, placeholder="例：\n【設問】学生時代に力を入れたことは？\n【回答】私はサークル活動で...\n\n【設問】自己PR\n【回答】私の強みは...")
    
    analyze_btn = st.button("🤖 AI解析してペアを抽出")
    
    if analyze_btn and bulk_text and api_key:
        with st.spinner("AIが設問と回答を抽出中..."):
            client = GeminiClient(api_key)
            extracted_data = client.extract_qa_pairs(bulk_text)
            
            if extracted_data:
                st.session_state['extracted_es_data'] = extracted_data
                st.success(f"{len(extracted_data)} 件のペアを抽出しました！")
            else:
                st.error("抽出に失敗しました。テキスト形式を確認してください。")
    
    # Preview and Save
    if 'extracted_es_data' in st.session_state and st.session_state['extracted_es_data']:
        st.markdown("##### 👀 抽出結果の確認")
        
        # Editable Data Editor
        edited_data = st.data_editor(
            st.session_state['extracted_es_data'],
            num_rows="dynamic",
            column_config={
                "question": st.column_config.TextColumn("設問", width="medium"),
                "answer": st.column_config.TextColumn("回答", width="large"),
            }
        )
        
        if st.button("💾 この内容で登録する", type="primary"):
            if company:
                count = 0
                for item in edited_data:
                    if item['question'] and item['answer']:
                        es_manager.add_es(company, item['question'], item['answer'])
                        count += 1
                
                st.success(f"{company} に {count} 件のESを登録しました！")
                del st.session_state['extracted_es_data'] # Clear state
                st.rerun()
            else:
                st.error("企業名を入力してください。")

st.markdown("---")

# List Past ES (Grouped by Company)
st.subheader("登録済みES一覧")

if not existing_es:
    st.info("まだESが登録されていません。")

# Group by company
grouped_es = {}
for i, es in enumerate(existing_es):
    c = es['company']
    if c not in grouped_es:
        grouped_es[c] = []
    grouped_es[c].append((i, es))

for company_name, items in grouped_es.items():
    with st.expander(f"🏢 {company_name} ({len(items)}件)"):
        for idx, item in items:
            st.markdown(f"**Q:** {item['question']}")
            st.markdown(f"**A:** {item['answer']}")
            if st.button("削除", key=f"del_{idx}"):
                es_manager.delete_es(idx)
                st.rerun()
            st.markdown("---")
