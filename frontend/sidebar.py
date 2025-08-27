import streamlit as st
from api_utils import upload_document, list_documents, delete_document
from datetime import datetime

# CSS
def add_custom_css():
    st.markdown("""
    <style>
        /* Sidebar layout */
        section[data-testid="stSidebar"] {
            background-color: #F9FAFB;
            padding: 20px;
            border-right: 2px solid #E5E7EB;
        }

        /* Headings */
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3 {
            font-weight: 700;
            color: #1F2937;
        }

        /* Persistent selectbox highlight */
        div[data-baseweb="select"] > div {
            border: 1px solid #2E7DFF !important;
            border-radius: 6px !important;
            box-shadow: 0 0 0 1px rgba(46,125,255,0.3);
        }

        /* File uploader */
        section[data-testid="stSidebar"] .stFileUploader {
            border: 2px dashed #CBD5E1;
            border-radius: 10px;
            padding: 10px;
            background-color: #FFFFFF;
        }

        /* Buttons */
        section[data-testid="stSidebar"] button {
            background-color: #2E7DFF;
            color: white;
            border-radius: 8px;
            padding: 8px 12px;
            font-weight: 600;
            border: none;
        }
        section[data-testid="stSidebar"] button:hover {
            background-color: #1D4ED8;
        }

        /* Document cards */
        .doc-card {
            background: #FFFFFF;
            border: 1px solid #E5E7EB;
            border-radius: 8px;
            padding: 8px;
            margin-bottom: 6px;
            font-size: 14px;
            line-height: 1.4;
        }
        .doc-title {
            display: flex;
            align-items: center;
            font-weight: 600;
            margin-bottom: 4px;
        }
        .doc-title img {
            margin-right: 6px;
        }
        small {
            color: #6B7280;
        }
    </style>
    """, unsafe_allow_html=True)

def humanize_ts(ts):
    # Accepts numeric epoch or preformatted string; returns display string
    try:
        # If epoch-like
        if isinstance(ts, (int, float)):
            return datetime.fromtimestamp(ts).strftime("%d %b %Y, %H:%M")
        # Try parse ISO
        return datetime.fromisoformat(str(ts)).strftime("%d %b %Y, %H:%M")
    except Exception:
        return str(ts)

# Sidebar
def display_sidebar():
    add_custom_css()
    # Model Selection 
    st.sidebar.markdown(
        """### <img src="https://cdn-icons-png.flaticon.com/512/4712/4712109.png" width="20" style="vertical-align:middle;margin-right:4px;"> Model Selection""",
        unsafe_allow_html=True
    )
    model_options = {
        "gemini-2.0-flash-lite": "Fast & lightweight",
        "gemini-2.5-flash-lite": "Balanced",
        "gemini-1.5-flash": "Higher accuracy but slower"
    }
    st.sidebar.selectbox(
        "Choose Model",
        options=list(model_options.keys()),
        format_func=lambda m: f"{m} – {model_options[m]}",
        key="model"
    )

    st.sidebar.markdown("---")

    # Upload Document
    st.sidebar.markdown("#### 📤 Upload Document")
    uploaded_file = st.sidebar.file_uploader(
        "Drop or select a file",
        type=["pdf", "docx", "html"],
        help="PDF, DOCX, HTML supported",
        label_visibility="collapsed"
    )
    if uploaded_file and st.sidebar.button("Upload Now"):
        with st.spinner("Uploading..."):
            resp = upload_document(uploaded_file)
            if resp:
                st.sidebar.success(f"✅ {uploaded_file.name} uploaded!")
                st.session_state.documents = list_documents()

    st.sidebar.markdown("---")

    # Uploaded Documents 
    st.sidebar.markdown("#### 📄 Uploaded Documents")
    if st.sidebar.button("Refresh List"):
        with st.spinner("Refreshing..."):
            st.session_state.documents = list_documents()

    if "documents" not in st.session_state:
        st.session_state.documents = list_documents()

    documents = st.session_state.documents
    if documents:
        for doc in documents:
            st.sidebar.markdown(
                f"""
                <div class='doc-card'>
                    <div class='doc-title'>
                        <img src='https://cdn-icons-png.flaticon.com/512/337/337946.png' width='16' height='16' alt='doc'>
                        {doc.get('filename','(no name)')}
                    </div>
                    <div class='doc-meta'>ID: <code>{doc.get('id','-')}</code></div>
                    <div class='doc-meta'>Uploaded: {humanize_ts(doc.get('upload_timestamp',''))}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        selected_file_id = st.sidebar.selectbox(
            "Select to delete",
            options=[doc['id'] for doc in documents],
            format_func=lambda x: next(doc['filename'] for doc in documents if doc['id'] == x)
        )
        if st.sidebar.button("🗑️ Delete Selected Documents"):
            # Get the filename before deletion
            deleted_doc_name = next(doc['filename'] for doc in documents if doc['id'] == selected_file_id)
            with st.spinner("Deleting..."):
                if delete_document(selected_file_id):
                    st.sidebar.success(f"✅ '{deleted_doc_name}' deleted!")
                    st.session_state.documents = list_documents()
                else:
                    st.sidebar.error("❌ Failed to delete document")
