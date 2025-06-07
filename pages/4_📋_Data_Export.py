"""
Data Export Page - Kaspa Analytics Pro
Data export functionality - Premium subscription required
"""

import streamlit as st
import streamlit_antd_components as sac
import pandas as pd
import json
from datetime import datetime, timedelta
import io

# Import utilities
from utils.auth import get_current_user, require_authentication_for_premium
from utils.data import fetch_kaspa_price_data, get_market_stats
from utils.ui import (
    render_page_header, 
    render_sidebar_navigation,
    apply_custom_css,
    render_footer,
    show_premium_required_prompt
)

# Configure page
st.set_page_config(
    page_title="Data Export - Kaspa Analytics Pro",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# SEO Meta Tags
st.markdown("""
<meta name="description" content="Export Kaspa price data, network metrics, and technical indicators in CSV or JSON format. Premium feature.">
<meta name="keywords" content="Kaspa data export, KAS price data download, cryptocurrency data API">
<meta property="og:title" content="Kaspa Data Export - Premium
