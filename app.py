"""
Harsh Project Scrapper - A Beautiful Multi-Source Project Idea Aggregator
Scrapes Reddit, LinkedIn, and GitHub for hardware and software project ideas
Built with Streamlit and the Pastel Dream aesthetic
"""

import streamlit as st
import feedparser
import pandas as pd
from ddgs import DDGS
import requests
import time
import os
from datetime import datetime
import json

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="Harsh Project Scrapper",
    layout="wide",
    page_icon="�",
    initial_sidebar_state="expanded"
)

# ============================================================================
# NETFLIX THEME - Custom CSS
# ============================================================================
NETFLIX_THEME_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Roboto:wght@300;400;500;700&display=swap');
    
    /* Global Styles - Netflix Black */
    .stApp {
        background: #141414;
        font-family: 'Roboto', sans-serif;
        color: #ffffff;
    }
    
    /* Sidebar Styling - Dark with Red Accent */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #000000 0%, #1a1a1a 100%);
        border-right: 2px solid #E50914;
    }
    
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: #E50914;
        font-weight: 700;
        font-family: 'Bebas Neue', cursive;
        letter-spacing: 2px;
    }
    
    /* Main Content Headers */
    h1 {
        color: #ffffff;
        font-family: 'Bebas Neue', cursive;
        font-weight: 700;
        font-size: 3.5rem;
        margin-bottom: 1rem;
        text-shadow: 3px 3px 8px rgba(229, 9, 20, 0.5);
        letter-spacing: 3px;
    }
    
    h2, h3 {
        color: #ffffff;
        font-family: 'Bebas Neue', cursive;
        font-weight: 600;
        letter-spacing: 2px;
    }
    
    /* Dark Cards with Netflix Hover Effect */
    div[data-testid="stVerticalBlock"] > div[style*="flex-direction: column;"] > div[data-testid="stVerticalBlock"] {
        background: linear-gradient(145deg, #1f1f1f 0%, #2a2a2a 100%);
        border-radius: 8px;
        padding: 24px;
        border: 1px solid #333333;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.7);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        margin-bottom: 16px;
    }
    
    div[data-testid="stVerticalBlock"] > div[style*="flex-direction: column;"] > div[data-testid="stVerticalBlock"]:hover {
        transform: scale(1.03);
        box-shadow: 0 8px 40px rgba(229, 9, 20, 0.4);
        border: 1px solid #E50914;
        background: linear-gradient(145deg, #2a2a2a 0%, #333333 100%);
    }
    
    /* Buttons - Netflix Red */
    .stButton > button {
        background: #E50914;
        color: white;
        border: none;
        border-radius: 4px;
        padding: 12px 28px;
        font-weight: 700;
        font-family: 'Roboto', sans-serif;
        text-transform: uppercase;
        letter-spacing: 1px;
        box-shadow: 0 4px 15px rgba(229, 9, 20, 0.4);
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: #f40612;
        transform: translateY(-2px);
        box-shadow: 0 6px 25px rgba(229, 9, 20, 0.6);
    }
    
    /* Secondary Buttons - Dark Gray */
    .stButton > button[kind="secondary"] {
        background: #333333;
        color: white;
        border: 1px solid #666666;
    }
    
    .stButton > button[kind="secondary"]:hover {
        background: #444444;
        border-color: #E50914;
    }
    
    /* Input Fields - Dark Theme */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select {
        background-color: #2a2a2a;
        border: 1px solid #444444;
        border-radius: 4px;
        padding: 12px;
        color: #ffffff;
        font-family: 'Roboto', sans-serif;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border: 2px solid #E50914;
        box-shadow: 0 0 0 3px rgba(229, 9, 20, 0.2);
        background-color: #1f1f1f;
    }
    
    /* Multiselect - Dark */
    .stMultiSelect > div > div {
        background-color: #2a2a2a;
        border-radius: 4px;
        border: 1px solid #444444;
    }
    
    /* Tabs - Netflix Style */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
        background-color: #000000;
        border-bottom: 2px solid #333333;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        border-radius: 0;
        padding: 12px 24px;
        font-weight: 600;
        color: #999999;
        border: none;
        border-bottom: 3px solid transparent;
        font-family: 'Roboto', sans-serif;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: transparent;
        color: #ffffff;
        border-bottom: 3px solid #E50914;
    }
    
    /* Expanders - Dark */
    .streamlit-expanderHeader {
        background-color: #2a2a2a;
        border-radius: 4px;
        font-weight: 500;
        color: #ffffff;
        border: 1px solid #444444;
    }
    
    .streamlit-expanderHeader:hover {
        background-color: #333333;
        border-color: #E50914;
    }
    
    /* Metrics - Netflix Red */
    [data-testid="stMetricValue"] {
        color: #E50914;
        font-size: 2.5rem;
        font-weight: 700;
        font-family: 'Bebas Neue', cursive;
    }
    
    /* Links - Netflix Red */
    a {
        color: #E50914 !important;
        text-decoration: none;
        font-weight: 500;
        transition: all 0.2s ease;
    }
    
    a:hover {
        color: #f40612 !important;
        text-decoration: underline;
    }
    
    /* Dataframe - Dark */
    .dataframe {
        border-radius: 4px;
        overflow: hidden;
        border: 1px solid #333333;
        background-color: #1f1f1f;
    }
    
    /* Success/Info/Warning Messages - Netflix Style */
    .stSuccess {
        background-color: rgba(0, 255, 0, 0.1);
        border-radius: 4px;
        border-left: 4px solid #00ff00;
        color: #ffffff;
    }
    
    .stInfo {
        background-color: rgba(229, 9, 20, 0.1);
        border-radius: 4px;
        border-left: 4px solid #E50914;
        color: #ffffff;
    }
    
    .stWarning {
        background-color: rgba(255, 165, 0, 0.1);
        border-radius: 4px;
        border-left: 4px solid #FFA500;
        color: #ffffff;
    }
    
    /* Progress Bar - Netflix Red */
    .stProgress > div > div > div > div {
        background: #E50914;
        border-radius: 2px;
    }
    
    /* Badges/Pills - Netflix Style */
    .badge {
        display: inline-block;
        padding: 6px 14px;
        border-radius: 3px;
        font-size: 0.75rem;
        font-weight: 700;
        margin: 4px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .badge-hardware {
        background: linear-gradient(135deg, #564d4d 0%, #3a3434 100%);
        color: #ffffff;
        border: 1px solid #666666;
    }
    
    .badge-software {
        background: linear-gradient(135deg, #E50914 0%, #b20710 100%);
        color: #ffffff;
    }
    
    .badge-score {
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
        color: #000000;
    }
    
    /* Divider - Netflix Red Accent */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, #E50914, transparent);
        margin: 24px 0;
    }
    
    /* Caption text */
    .caption, [data-testid="stCaption"] {
        color: #999999 !important;
    }
    
    /* Additional Netflix Touches */
    [data-testid="stMarkdownContainer"] p {
        color: #ffffff;
    }
    
    /* Download Button */
    .stDownloadButton > button {
        background: #2a2a2a;
        color: white;
        border: 1px solid #E50914;
    }
    
    .stDownloadButton > button:hover {
        background: #E50914;
        border-color: #E50914;
    }
</style>
"""

st.markdown(NETFLIX_THEME_CSS, unsafe_allow_html=True)

# ============================================================================
# STATE MANAGEMENT
# ============================================================================
def migrate_old_csv(df):
    """Migrate old CSV format to new schema"""
    # Define new schema columns
    new_columns = ['id', 'title', 'source', 'link', 'category', 
                   'description', 'keywords', 'status', 'notes', 'saved_date']
    
    # Map old column names to new ones
    column_mapping = {
        'Title': 'title',
        'Source': 'source',
        'Link': 'link',
        'Notes': 'notes',
        'Subreddit': 'source',
        'Description': 'description'
    }
    
    # Rename columns if they exist
    df = df.rename(columns=column_mapping)
    
    # Add missing columns with defaults
    if 'id' not in df.columns:
        df['id'] = range(1, len(df) + 1)
    if 'category' not in df.columns:
        df['category'] = 'General'
    if 'status' not in df.columns:
        df['status'] = 'To Do'
    if 'description' not in df.columns:
        df['description'] = ''
    if 'keywords' not in df.columns:
        df['keywords'] = ''
    if 'saved_date' not in df.columns:
        df['saved_date'] = datetime.now().strftime('%Y-%m-%d %H:%M')
    if 'notes' not in df.columns:
        df['notes'] = ''
    if 'title' not in df.columns and 'Title' in df.columns:
        df['title'] = df['Title']
    if 'source' not in df.columns and 'Source' in df.columns:
        df['source'] = df['Source']
    if 'link' not in df.columns and 'Link' in df.columns:
        df['link'] = df['Link']
    
    # Keep only new schema columns
    for col in new_columns:
        if col not in df.columns:
            df[col] = ''
    
    return df[new_columns]


def init_session_state():
    """Initialize all session state variables"""
    defaults = {
        'reddit_results': pd.DataFrame(),
        'linkedin_results': pd.DataFrame(),
        'github_results': pd.DataFrame(),
        'competitor_results': pd.DataFrame(),
        'saved_ideas': pd.DataFrame(columns=[
            'id', 'title', 'source', 'link', 'category', 
            'description', 'keywords', 'status', 'notes', 'saved_date'
        ]),
        'edit_mode': None,
        'next_id': 1
    }
    
    for key, default_value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default_value
    
    # Load saved ideas from CSV if exists
    if os.path.exists('saved_ideas.csv') and st.session_state['saved_ideas'].empty:
        try:
            old_df = pd.read_csv('saved_ideas.csv')
            # Migrate old format to new schema
            st.session_state['saved_ideas'] = migrate_old_csv(old_df)
            # Save migrated data back to CSV
            st.session_state['saved_ideas'].to_csv('saved_ideas.csv', index=False)
            if not st.session_state['saved_ideas'].empty:
                st.session_state['next_id'] = int(st.session_state['saved_ideas']['id'].max()) + 1
        except Exception as e:
            st.error(f"Error loading saved ideas: {e}")
            # Initialize with empty dataframe on error
            st.session_state['saved_ideas'] = pd.DataFrame(columns=[
                'id', 'title', 'source', 'link', 'category', 
                'description', 'keywords', 'status', 'notes', 'saved_date'
            ])

init_session_state()

# ============================================================================
# CORE SCRAPING FUNCTIONS
# ============================================================================

def scrape_reddit(subreddits, keywords, category_filter="All"):
    """
    Scrape Reddit RSS feeds with keyword scoring and category filtering
    """
    all_ideas = []
    progress_placeholder = st.empty()
    
    # Category-specific keywords for classification
    hardware_keywords = ['arduino', 'raspberry pi', 'esp32', 'sensor', 'iot', 'circuit', 
                         'hardware', '3d print', 'pcb', 'robot', 'embedded']
    software_keywords = ['app', 'website', 'api', 'algorithm', 'software', 'web', 
                         'mobile', 'code', 'python', 'javascript', 'ai', 'ml']
    
    for i, sub in enumerate(subreddits):
        rss_url = f"https://www.reddit.com/r/{sub}/new/.rss"
        try:
            progress_placeholder.progress((i) / len(subreddits), f"Scraping r/{sub}...")
            feed = feedparser.parse(rss_url)
            
            for entry in feed.entries[:25]:  # Limit to 25 most recent
                title = entry.title
                summary = entry.get('summary', '')
                content_text = (title + " " + summary).lower()
                
                # Keyword scoring
                keyword_score = sum([1 for k in keywords if k.lower() in content_text])
                
                if keyword_score == 0 and keywords:  # Skip if no keyword match
                    continue
                
                # Category classification
                hw_score = sum([1 for k in hardware_keywords if k in content_text])
                sw_score = sum([1 for k in software_keywords if k in content_text])
                
                if hw_score > sw_score:
                    category = "Hardware"
                elif sw_score > hw_score:
                    category = "Software"
                else:
                    category = "General"
                
                # Apply category filter
                if category_filter != "All" and category != category_filter:
                    continue
                
                all_ideas.append({
                    "Title": title,
                    "Source": f"r/{sub}",
                    "Link": entry.link,
                    "Description": summary[:300] + "..." if len(summary) > 300 else summary,
                    "Category": category,
                    "Score": keyword_score,
                    "Platform": "Reddit"
                })
                
        except Exception as e:
            st.warning(f"Error scraping r/{sub}: {str(e)}")
            continue
    
    progress_placeholder.empty()
    return pd.DataFrame(all_ideas)


def scrape_linkedin(query, search_type="Posts", max_results=15):
    """
    Scrape LinkedIn using DuckDuckGo X-Ray search
    """
    results = []
    
    try:
        # Construct X-Ray search queries
        if search_type == "Posts":
            ddg_query = f'site:linkedin.com/posts "{query}" ("I built" OR "project" OR "github" OR "demo")'
        elif search_type == "People":
            ddg_query = f'site:linkedin.com/in "{query}" "project" "portfolio"'
        else:  # Jobs
            ddg_query = f'site:linkedin.com/jobs "{query}"'
        
        with DDGS() as ddgs:
            search_results = ddgs.text(ddg_query, max_results=max_results)
            
            for r in search_results:
                results.append({
                    "Title": r['title'],
                    "Link": r['href'],
                    "Description": r['body'][:400] + "..." if len(r['body']) > 400 else r['body'],
                    "Source": "LinkedIn",
                    "Category": "Software",  # Default for LinkedIn
                    "Platform": "LinkedIn"
                })
                
    except Exception as e:
        st.error(f"LinkedIn scraping error: {str(e)}")
    
    return pd.DataFrame(results)


def scrape_github(topics, keywords, max_repos=20):
    """
    Scrape GitHub for trending repositories using GitHub API
    """
    results = []
    
    # GitHub API endpoint
    base_url = "https://api.github.com/search/repositories"
    
    # Construct search query
    topic_query = " OR ".join([f"topic:{topic}" for topic in topics])
    keyword_query = " ".join(keywords) if keywords else ""
    query = f"{keyword_query} {topic_query}".strip()
    
    params = {
        "q": query,
        "sort": "stars",
        "order": "desc",
        "per_page": max_repos
    }
    
    try:
        response = requests.get(base_url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            for repo in data.get('items', []):
                # Determine category from topics
                repo_topics = repo.get('topics', [])
                hw_topics = ['hardware', 'iot', 'arduino', 'raspberry-pi', 'embedded']
                category = "Hardware" if any(t in hw_topics for t in repo_topics) else "Software"
                
                results.append({
                    "Title": repo['full_name'],
                    "Description": repo.get('description', 'No description'),
                    "Link": repo['html_url'],
                    "Stars": repo['stargazers_count'],
                    "Language": repo.get('language', 'N/A'),
                    "Topics": ", ".join(repo_topics[:5]),
                    "Category": category,
                    "Source": "GitHub",
                    "Platform": "GitHub"
                })
        elif response.status_code == 403:
            st.warning("⚠️ GitHub API rate limit reached. Try again later.")
        else:
            st.error(f"GitHub API error: {response.status_code}")
            
    except Exception as e:
        st.error(f"GitHub scraping error: {str(e)}")
    
    return pd.DataFrame(results)


def competitor_check(idea_title, max_results=10):
    """
    Search for existing similar projects (competitor analysis)
    """
    results = []
    
    try:
        search_query = f'"{idea_title}" (project OR github OR "open source")'
        
        with DDGS() as ddgs:
            search_results = ddgs.text(search_query, max_results=max_results)
            
            for r in search_results:
                results.append({
                    "Title": r['title'],
                    "Link": r['href'],
                    "Description": r['body'][:300] + "..." if len(r['body']) > 300 else r['body'],
                    "Source": "Competitor"
                })
                
    except Exception as e:
        st.error(f"Competitor check error: {str(e)}")
    
    return pd.DataFrame(results)


# ============================================================================
# CRUD OPERATIONS
# ============================================================================

def save_idea(title, source, link, category, description="", keywords="", notes=""):
    """Create: Save a new idea to the vault"""
    new_id = st.session_state['next_id']
    st.session_state['next_id'] += 1
    
    new_entry = pd.DataFrame([{
        'id': new_id,
        'title': title,
        'source': source,
        'link': link,
        'category': category,
        'description': description,
        'keywords': keywords,
        'status': 'To Do',
        'notes': notes,
        'saved_date': datetime.now().strftime('%Y-%m-%d %H:%M')
    }])
    
    st.session_state['saved_ideas'] = pd.concat(
        [st.session_state['saved_ideas'], new_entry], 
        ignore_index=True
    )
    
    # Persist to CSV
    st.session_state['saved_ideas'].to_csv('saved_ideas.csv', index=False)
    st.toast("💾 Idea saved to vault!", icon="✅")


def update_idea(idea_id, notes, status):
    """Update: Modify an existing idea's notes and status"""
    idx = st.session_state['saved_ideas'][st.session_state['saved_ideas']['id'] == idea_id].index
    
    if len(idx) > 0:
        st.session_state['saved_ideas'].at[idx[0], 'notes'] = notes
        st.session_state['saved_ideas'].at[idx[0], 'status'] = status
        st.session_state['saved_ideas'].to_csv('saved_ideas.csv', index=False)
        st.toast("✏️ Idea updated!", icon="✅")


def delete_idea(idea_id):
    """Delete: Remove an idea from the vault"""
    st.session_state['saved_ideas'] = st.session_state['saved_ideas'][
        st.session_state['saved_ideas']['id'] != idea_id
    ]
    st.session_state['saved_ideas'].to_csv('saved_ideas.csv', index=False)
    st.toast("🗑️ Idea deleted!", icon="✅")


# ============================================================================
# UI COMPONENTS
# ============================================================================

def render_idea_card(row, idx, source_prefix, show_save_button=True):
    """Render a beautiful glassmorphism card for an idea"""
    with st.container():
        col1, col2 = st.columns([0.85, 0.15])
        
        with col1:
            # Title with category badge
            category_class = "badge-hardware" if row.get('Category', 'General') == "Hardware" else "badge-software"
            category_badge = f'<span class="badge {category_class}">{row.get("Category", "General")}</span>'
            
            score_badge = ""
            if 'Score' in row and row['Score'] > 0:
                score_badge = f'<span class="badge badge-score">🔥 Match: {row["Score"]}</span>'
            
            st.markdown(f"### {row['Title']}", unsafe_allow_html=True)
            st.markdown(f"{category_badge} {score_badge}", unsafe_allow_html=True)
            
            # Source info
            source_icon = {"Reddit": "📢", "LinkedIn": "👔", "GitHub": "⭐"}.get(row.get('Platform', 'Reddit'), "🔗")
            st.caption(f"{source_icon} **{row['Source']}**")
            
            # Description in expander
            with st.expander("📝 View Details"):
                st.markdown(row.get('Description', 'No description available'))
                st.markdown(f"🔗 [Open Link]({row['Link']})")
                
                # GitHub specific info
                if 'Stars' in row:
                    st.metric("⭐ Stars", f"{row['Stars']:,}")
                if 'Language' in row:
                    st.caption(f"**Language:** {row['Language']}")
                if 'Topics' in row and row['Topics']:
                    st.caption(f"**Topics:** {row['Topics']}")
        
        with col2:
            if show_save_button:
                if st.button("💾 Save", key=f"{source_prefix}_save_{idx}", use_container_width=True):
                    save_idea(
                        title=row['Title'],
                        source=row['Source'],
                        link=row['Link'],
                        category=row.get('Category', 'General'),
                        description=row.get('Description', ''),
                        keywords=""
                    )
                    st.rerun()
            
            # Competitor check
            if st.button("🔍 Check", key=f"{source_prefix}_comp_{idx}", use_container_width=True):
                with st.spinner("Checking competitors..."):
                    comp_results = competitor_check(row['Title'])
                    st.session_state['competitor_results'] = comp_results
        
        st.divider()


# ============================================================================
# SIDEBAR - CONFIGURATION & CONTROLS
# ============================================================================

with st.sidebar:
    st.markdown("# � Harsh Project Scrapper")
    st.caption("Cinematic Multi-Source Project Discovery")
    
    st.markdown("---")
    
    # Category Filter (Global)
    st.markdown("### 🎯 Project Type")
    category_filter = st.selectbox(
        "Filter by category",
        ["All", "Hardware", "Software"],
        key="global_category_filter"
    )
    
    # Keywords
    st.markdown("### 🔑 Keywords")
    keywords_input = st.text_input(
        "Enter keywords (comma-separated)",
        value="AI, Medical, Trading, IoT, Automation",
        help="Used for scoring and filtering results"
    )
    keywords = [k.strip() for k in keywords_input.split(",") if k.strip()]
    
    st.markdown("---")
    
    # Reddit Configuration
    st.markdown("### 📢 Reddit Settings")
    hardware_subs = ["Arduino", "RaspberryPi", "esp32", "3Dprinting", "robotics"]
    software_subs = ["SomebodyMakeThis", "AppIdeas", "Startup_Ideas", "Python", "webdev"]
    
    if category_filter == "Hardware":
        default_subs = hardware_subs
    elif category_filter == "Software":
        default_subs = software_subs
    else:
        default_subs = ["SomebodyMakeThis", "AppIdeas"]
    
    selected_subs = st.multiselect(
        "Subreddits to scrape",
        options=hardware_subs + software_subs,
        default=default_subs
    )
    
    if st.button("🚀 Mine Reddit", type="primary", use_container_width=True):
        if not selected_subs:
            st.warning("Please select at least one subreddit")
        else:
            with st.spinner("⛏️ Mining Reddit..."):
                results = scrape_reddit(selected_subs, keywords, category_filter)
                st.session_state['reddit_results'] = results
                st.rerun()
    
    st.markdown("---")
    
    # GitHub Configuration
    st.markdown("### ⭐ GitHub Settings")
    github_topics = st.multiselect(
        "Topics to search",
        ["machine-learning", "iot", "arduino", "medical", "trading", "automation", 
         "web-app", "mobile-app", "raspberry-pi", "ai"],
        default=["machine-learning", "iot"]
    )
    
    if st.button("⭐ Search GitHub", use_container_width=True):
        if not github_topics:
            st.warning("Please select at least one topic")
        else:
            with st.spinner("🔍 Searching GitHub..."):
                results = scrape_github(github_topics, keywords)
                st.session_state['github_results'] = results
                st.rerun()
    
    st.markdown("---")
    st.caption("🎬 Directed by Harsh")
    st.caption("⚡ Streaming via Streamlit")


# ============================================================================
# MAIN CONTENT - TABS
# ============================================================================

st.markdown("# � PROJECT IDEA VAULT")
st.markdown("Discover blockbuster hardware and software project ideas from across the web")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📢 Reddit Ideas", 
    "👔 LinkedIn Projects", 
    "⭐ GitHub Repos",
    "🔍 Competitor Check",
    "💾 Saved Vault"
])

# ---------- TAB 1: REDDIT ----------
with tab1:
    st.markdown("## 📢 Reddit Project Ideas")
    
    if not st.session_state['reddit_results'].empty:
        df = st.session_state['reddit_results']
        
        # Stats
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📊 Total Ideas", len(df))
        with col2:
            hw_count = len(df[df['Category'] == 'Hardware'])
            st.metric("🔧 Hardware", hw_count)
        with col3:
            sw_count = len(df[df['Category'] == 'Software'])
            st.metric("💻 Software", sw_count)
        
        st.markdown("---")
        
        # Render cards
        for idx, row in df.iterrows():
            render_idea_card(row, idx, "reddit")
    else:
        st.info("👈 Click **Mine Reddit** in the sidebar to start discovering ideas!")

# ---------- TAB 2: LINKEDIN ----------
with tab2:
    st.markdown("## 👔 LinkedIn Project Showcase")
    st.caption("Find people sharing their projects, demos, and GitHub links")
    
    # Search interface
    col1, col2, col3 = st.columns([3, 1.5, 1])
    
    with col1:
        li_query = st.text_input(
            "Search topic",
            placeholder="e.g., 'Medical AI', 'Trading Bot', 'IoT Sensor'",
            key="li_search_input"
        )
    
    with col2:
        li_search_type = st.selectbox(
            "Search for",
            ["Posts", "People", "Jobs"],
            key="li_search_type"
        )
    
    with col3:
        li_start = st.button("🔎 Search", use_container_width=True, key="li_search_btn")
    
    if li_start and li_query:
        with st.spinner(f"🔍 Searching LinkedIn {li_search_type}..."):
            results = scrape_linkedin(li_query, li_search_type)
            st.session_state['linkedin_results'] = results
            st.rerun()
    
    # Display results
    if not st.session_state['linkedin_results'].empty:
        df = st.session_state['linkedin_results']
        st.success(f"✅ Found {len(df)} results for '{li_query}'")
        st.markdown("---")
        
        for idx, row in df.iterrows():
            render_idea_card(row, idx, "linkedin")
    else:
        st.info("🔎 Enter a search query above to find LinkedIn projects")

# ---------- TAB 3: GITHUB ----------
with tab3:
    st.markdown("## ⭐ GitHub Trending Repositories")
    
    if not st.session_state['github_results'].empty:
        df = st.session_state['github_results']
        
        # Stats
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📦 Repositories", len(df))
        with col2:
            total_stars = df['Stars'].sum() if 'Stars' in df.columns else 0
            st.metric("⭐ Total Stars", f"{total_stars:,}")
        with col3:
            top_lang = df['Language'].mode()[0] if 'Language' in df.columns and not df.empty else "N/A"
            st.metric("🔥 Top Language", top_lang)
        
        st.markdown("---")
        
        # Render cards
        for idx, row in df.iterrows():
            render_idea_card(row, idx, "github")
    else:
        st.info("👈 Click **Search GitHub** in the sidebar to find trending repositories!")

# ---------- TAB 4: COMPETITOR CHECK ----------
with tab4:
    st.markdown("## 🔍 Competitor Analysis")
    st.caption("Check if similar projects already exist before building")
    
    # Manual search interface
    comp_query = st.text_input(
        "Enter project idea to check",
        placeholder="e.g., 'AI-powered medical diagnosis app'",
        key="comp_search_input"
    )
    
    if st.button("🔍 Search Competitors", key="comp_search_btn"):
        if comp_query:
            with st.spinner("🔍 Searching for similar projects..."):
                results = competitor_check(comp_query)
                st.session_state['competitor_results'] = results
                st.rerun()
        else:
            st.warning("Please enter a project idea")
    
    # Display results
    if not st.session_state['competitor_results'].empty:
        df = st.session_state['competitor_results']
        st.warning(f"⚠️ Found {len(df)} potentially similar projects")
        st.markdown("---")
        
        for idx, row in df.iterrows():
            with st.container():
                st.markdown(f"### {row['Title']}")
                st.markdown(row['Description'])
                st.markdown(f"🔗 [Visit Link]({row['Link']})")
                st.divider()
    else:
        st.info("💡 Search for your project idea to see if similar solutions exist")

# ---------- TAB 5: SAVED VAULT ----------
with tab5:
    st.markdown("## 💾 Your Saved Project Ideas")
    
    if not st.session_state['saved_ideas'].empty:
        df = st.session_state['saved_ideas']
        
        # Stats
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("📚 Total Saved", len(df))
        with col2:
            todo_count = len(df[df['status'] == 'To Do'])
            st.metric("📝 To Do", todo_count)
        with col3:
            in_progress = len(df[df['status'] == 'In Progress'])
            st.metric("⚙️ In Progress", in_progress)
        with col4:
            completed = len(df[df['status'] == 'Completed'])
            st.metric("✅ Completed", completed)
        
        st.markdown("---")
        
        # Filter options
        col1, col2 = st.columns([1, 1])
        with col1:
            status_filter = st.selectbox(
                "Filter by status",
                ["All", "To Do", "In Progress", "Completed"],
                key="vault_status_filter"
            )
        with col2:
            category_vault_filter = st.selectbox(
                "Filter by category",
                ["All", "Hardware", "Software", "General"],
                key="vault_category_filter"
            )
        
        # Apply filters
        filtered_df = df.copy()
        if status_filter != "All":
            filtered_df = filtered_df[filtered_df['status'] == status_filter]
        if category_vault_filter != "All":
            filtered_df = filtered_df[filtered_df['category'] == category_vault_filter]
        
        st.markdown(f"#### Showing {len(filtered_df)} ideas")
        
        # Export button
        if not filtered_df.empty:
            csv = filtered_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                "📥 Export to CSV",
                csv,
                "harsh_project_ideas.csv",
                "text/csv",
                use_container_width=False
            )
        
        st.markdown("---")
        
        # Render saved ideas with CRUD operations
        for idx, row in filtered_df.iterrows():
            with st.container():
                col1, col2 = st.columns([0.8, 0.2])
                
                with col1:
                    # Title and badges
                    category_class = f"badge-{row['category'].lower()}" if row['category'] in ['Hardware', 'Software'] else "badge-software"
                    st.markdown(f"### {row['title']}")
                    st.markdown(
                        f'<span class="badge {category_class}">{row["category"]}</span> '
                        f'<span class="badge badge-score">{row["status"]}</span>',
                        unsafe_allow_html=True
                    )
                    st.caption(f"📌 **Source:** {row['source']} | 📅 **Saved:** {row['saved_date']}")
                    
                    # Expandable details and edit
                    with st.expander("📝 View & Edit"):
                        st.markdown(f"**Description:** {row['description']}")
                        st.markdown(f"🔗 [Open Link]({row['link']})")
                        st.markdown("---")
                        
                        # Edit form
                        edit_notes = st.text_area(
                            "Notes",
                            value=row['notes'],
                            key=f"notes_{row['id']}",
                            height=100
                        )
                        
                        edit_status = st.selectbox(
                            "Status",
                            ["To Do", "In Progress", "Completed"],
                            index=["To Do", "In Progress", "Completed"].index(row['status']),
                            key=f"status_{row['id']}"
                        )
                        
                        if st.button("💾 Update", key=f"update_{row['id']}"):
                            update_idea(row['id'], edit_notes, edit_status)
                            st.rerun()
                
                with col2:
                    if st.button("🗑️ Delete", key=f"delete_{row['id']}", use_container_width=True):
                        delete_idea(row['id'])
                        st.rerun()
                
                st.divider()
    
    else:
        st.info("💡 Your vault is empty! Start saving ideas from the other tabs.")
        st.markdown("""
        ### How to use:
        1. 📢 **Browse Reddit ideas** - Discover project ideas from various subreddits
        2. 👔 **Search LinkedIn** - Find people sharing their projects
        3. ⭐ **Explore GitHub** - See trending open-source repositories
        4. 💾 **Save ideas** - Click the save button on any idea you like
        5. ✏️ **Manage** - Edit notes, update status, and delete ideas here
        """)

# ============================================================================
# FOOTER
# ============================================================================
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #E50914; padding: 20px;'>
    <p style='font-size: 1.3rem; font-weight: 700; font-family: "Bebas Neue", cursive; letter-spacing: 2px;'>
        🎬 HARSH PROJECT SCRAPPER - POWERED BY NETFLIX DESIGN 🎬
    </p>
    <p style='font-size: 0.95rem; opacity: 0.8; color: #999999;'>
        Aggregating blockbuster project ideas from Reddit, LinkedIn & GitHub
    </p>
    <p style='font-size: 0.8rem; opacity: 0.6; color: #666666; margin-top: 10px;'>
        Streaming the best ideas 24/7
    </p>
</div>
""", unsafe_allow_html=True)