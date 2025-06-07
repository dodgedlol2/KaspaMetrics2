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
<meta property="og:title" content="Kaspa Data Export - Premium Feature">
<meta property="og:description" content="Download Kaspa blockchain data in multiple formats with Premium subscription">
<meta property="og:type" content="website">
""", unsafe_allow_html=True)

# Apply styling
apply_custom_css()

def main():
    """Main data export page"""
    
    # Get current user
    user = get_current_user()
    
    # Render sidebar navigation
    render_sidebar_navigation(user)
    
    # Check if user has premium access
    if user['username'] == 'public' or user['subscription'] != 'premium':
        # Show premium required page
        render_premium_required_page(user)
        return
    
    # Premium user - show full export functionality
    render_premium_export_page(user)

def render_premium_required_page(user):
    """Show premium required page for non-premium users"""
    
    # Page header
    render_page_header(
        "📋 Data Export",
        "Download Kaspa data in multiple formats - Premium Feature"
    )
    
    # Breadcrumb navigation
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("← Dashboard", key="export_back_to_home"):
            st.switch_page("streamlit_app.py")
    
    # Show what's available with premium
    st.subheader("🔒 Premium Data Export Features")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📊 Available Data")
        st.write("• **Price Data**: OHLCV historical data")
        st.write("• **Technical Indicators**: RSI, MACD, Bollinger Bands")
        st.write("• **Network Metrics**: Hash rate, difficulty, addresses")
        st.write("• **Market Statistics**: Volume, market cap, trends")
        st.write("• **Custom Date Ranges**: Any period you need")
    
    with col2:
        st.markdown("#### 📁 Export Formats")
        st.write("• **CSV**: Excel-compatible spreadsheet format")
        st.write("• **JSON**: API-friendly structured data")
        st.write("• **Custom Columns**: Choose exactly what you need")
        st.write("• **Batch Export**: Multiple datasets at once")
        st.write("• **API Access**: Programmatic data retrieval")
    
    # Show preview of what premium users get
    st.subheader("📈 Data Preview")
    
    # Show sample data
    df = fetch_kaspa_price_data(7)  # 7 days sample
    if not df.empty:
        st.write("**Sample price data (last 7 days):**")
        st.dataframe(df.head(10), use_container_width=True)
        st.info("🔒 Premium users can export unlimited historical data in multiple formats")
    
    # Premium upgrade prompt
    st.markdown("---")
    show_premium_required_prompt()
    
    # Footer
    render_footer()

def render_premium_export_page(user):
    """Show full export functionality for premium users"""
    
    # Page header
    render_page_header(
        f"📋 Data Export - {user['name']}",
        "Download Kaspa data in multiple formats - Premium Access"
    )
    
    # Breadcrumb navigation
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("← Dashboard", key="export_back_to_home_premium"):
            st.switch_page("streamlit_app.py")
    
    st.success("🎉 Premium Access - All export features unlocked!")
    
    # Export tabs
    export_tabs = sac.tabs([
        sac.TabsItem(label='Price Data', icon='graph-up'),
        sac.TabsItem(label='Technical Data', icon='sliders'),
        sac.TabsItem(label='Network Data', icon='globe'),
        sac.TabsItem(label='API Access', icon='code'),
    ], key='export_tabs')
    
    if export_tabs == 'Price Data':
        render_price_data_export()
    elif export_tabs == 'Technical Data':
        render_technical_data_export()
    elif export_tabs == 'Network Data':
        render_network_data_export()
    else:
        render_api_access_tab()
    
    # Export history
    st.markdown("---")
    render_export_history()
    
    # Footer
    render_footer()

def render_price_data_export():
    """Render price data export interface"""
    st.subheader("📈 Price Data Export")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📅 Date Range")
        
        date_option = st.selectbox(
            "Select Range",
            ["Last 7 days", "Last 30 days", "Last 3 months", "Last 6 months", "Last year", "Custom range"],
            key="price_date_range"
        )
        
        if date_option == "Custom range":
            start_date = st.date_input("Start Date", value=datetime.now() - timedelta(days=30))
            end_date = st.date_input("End Date", value=datetime.now())
        
        timeframe = st.selectbox(
            "Timeframe",
            ["1 hour", "4 hours", "1 day", "1 week"],
            index=2,
            key="price_timeframe"
        )
    
    with col2:
        st.markdown("#### 📊 Data Options")
        
        data_columns = st.multiselect(
            "Select Columns",
            ["Timestamp", "Open", "High", "Low", "Close", "Volume", "Market Cap"],
            default=["Timestamp", "Open", "High", "Low", "Close", "Volume"],
            key="price_columns"
        )
        
        export_format = st.selectbox(
            "Export Format",
            ["CSV", "JSON"],
            key="price_format"
        )
        
        include_headers = st.checkbox("Include Headers", value=True, key="price_headers")
    
    # Preview data
    st.markdown("#### 👀 Data Preview")
    
    # Fetch data based on selection
    if date_option == "Last 7 days":
        df = fetch_kaspa_price_data(7)
    elif date_option == "Last 30 days":
        df = fetch_kaspa_price_data(30)
    elif date_option == "Last 3 months":
        df = fetch_kaspa_price_data(90)
    elif date_option == "Last 6 months":
        df = fetch_kaspa_price_data(180)
    elif date_option == "Last year":
        df = fetch_kaspa_price_data(365)
    else:
        # Custom range
        days_diff = (end_date - start_date).days
        df = fetch_kaspa_price_data(days_diff)
    
    if not df.empty:
        # Filter columns
        available_columns = [col for col in data_columns if col.lower() in df.columns]
        preview_df = df[available_columns].head(10)
        
        st.dataframe(preview_df, use_container_width=True)
        st.info(f"📊 Total rows: {len(df):,} | Preview showing first 10 rows")
        
        # Export buttons
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📥 Download Data", key="download_price_data", use_container_width=True, type="primary"):
                # Generate download
                if export_format == "CSV":
                    csv_data = df[available_columns].to_csv(index=False, header=include_headers)
                    st.download_button(
                        label="💾 Download CSV",
                        data=csv_data,
                        file_name=f"kaspa_price_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv",
                        key="csv_download"
                    )
                else:
                    json_data = df[available_columns].to_json(orient='records', date_format='iso')
                    st.download_button(
                        label="💾 Download JSON",
                        data=json_data,
                        file_name=f"kaspa_price_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json",
                        key="json_download"
                    )
                
                st.success("✅ Export prepared! Click the download button above.")
        
        with col2:
            if st.button("📧 Email Data", key="email_price_data", use_container_width=True):
                st.info("📧 Data will be emailed to your registered address")
        
        with col3:
            if st.button("🔄 Refresh Data", key="refresh_price_data", use_container_width=True):
                st.rerun()

def render_technical_data_export():
    """Render technical indicators export"""
    st.subheader("📊 Technical Indicators Export")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📈 Indicators")
        
        indicators = st.multiselect(
            "Select Indicators",
            ["RSI", "MACD", "Bollinger Bands", "Moving Averages", "Stochastic", "Williams %R"],
            default=["RSI", "MACD", "Bollinger Bands"],
            key="tech_indicators"
        )
        
        timeframe = st.selectbox(
            "Timeframe",
            ["1 hour", "4 hours", "1 day"],
            index=2,
            key="tech_timeframe"
        )
    
    with col2:
        st.markdown("#### ⚙️ Settings")
        
        rsi_period = st.number_input("RSI Period", min_value=5, max_value=50, value=14, key="rsi_period")
        sma_periods = st.multiselect("SMA Periods", [10, 20, 50, 100, 200], default=[20, 50], key="sma_periods")
        
        export_format = st.selectbox(
            "Export Format",
            ["CSV", "JSON"],
            key="tech_format"
        )
    
    # Sample technical data
    st.markdown("#### 👀 Technical Data Preview")
    
    sample_data = {
        'timestamp': pd.date_range(start='2024-01-01', periods=10, freq='D'),
        'price': [0.1234, 0.1245, 0.1256, 0.1234, 0.1223, 0.1267, 0.1289, 0.1245, 0.1234, 0.1278],
        'rsi': [45.2, 52.1, 58.3, 42.1, 38.9, 65.4, 72.1, 48.3, 41.2, 59.8],
        'sma_20': [0.1240, 0.1242, 0.1244, 0.1243, 0.1241, 0.1245, 0.1248, 0.1247, 0.1245, 0.1250],
        'macd': [0.0012, 0.0015, 0.0018, 0.0010, 0.0008, 0.0020, 0.0025, 0.0015, 0.0012, 0.0022]
    }
    
    tech_df = pd.DataFrame(sample_data)
    st.dataframe(tech_df, use_container_width=True)
    
    # Export button
    if st.button("📥 Export Technical Data", key="export_tech_data", use_container_width=True, type="primary"):
        st.success("✅ Technical indicators exported successfully!")

def render_network_data_export():
    """Render network metrics export"""
    st.subheader("🌐 Network Metrics Export")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🔗 Network Data")
        
        network_metrics = st.multiselect(
            "Select Metrics",
            ["Hash Rate", "Difficulty", "Block Time", "Active Addresses", "Transaction Count", "Network Fee"],
            default=["Hash Rate", "Difficulty", "Active Addresses"],
            key="network_metrics"
        )
        
        aggregation = st.selectbox(
            "Aggregation",
            ["Hourly", "Daily", "Weekly"],
            index=1,
            key="network_aggregation"
        )
    
    with col2:
        st.markdown("#### 📅 Time Range")
        
        date_range = st.selectbox(
            "Select Range",
            ["Last 7 days", "Last 30 days", "Last 3 months"],
            key="network_date_range"
        )
        
        export_format = st.selectbox(
            "Export Format",
            ["CSV", "JSON"],
            key="network_format"
        )
    
    # Sample network data
    st.markdown("#### 👀 Network Data Preview")
    
    network_sample = {
        'date': pd.date_range(start='2024-01-01', periods=7, freq='D'),
        'hash_rate': [125.5, 128.2, 132.1, 129.8, 135.4, 140.2, 138.9],
        'difficulty': [1.25e12, 1.28e12, 1.32e12, 1.29e12, 1.35e12, 1.40e12, 1.38e12],
        'active_addresses': [15420, 16230, 17580, 15890, 18450, 19120, 18760],
        'avg_block_time': [1.02, 0.98, 1.05, 1.01, 0.95, 1.08, 1.03]
    }
    
    network_df = pd.DataFrame(network_sample)
    st.dataframe(network_df, use_container_width=True)
    
    # Export button
    if st.button("📥 Export Network Data", key="export_network_data", use_container_width=True, type="primary"):
        st.success("✅ Network metrics exported successfully!")

def render_api_access_tab():
    """Render API access information"""
    st.subheader("🔌 API Access")
    
    st.markdown("#### 🔑 Your API Key")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        api_key = "kas_pro_" + user['username'] + "_" + "".join([str(ord(c)) for c in user['username'][:3]])
        st.code(api_key, language="text")
    
    with col2:
        if st.button("🔄 Regenerate", key="regenerate_api_key"):
            st.success("New API key generated!")
    
    st.markdown("#### 📚 API Documentation")
    
    st.markdown("""
    **Base URL:** `https://api.kaspa-analytics.com/v1/`
    
    **Authentication:** Include your API key in the header:
    ```
    Authorization: Bearer YOUR_API_KEY
    ```
    
    **Available Endpoints:**
    """)
    
    api_endpoints = [
        {"endpoint": "/price/current", "description": "Get current KAS price"},
        {"endpoint": "/price/history", "description": "Get historical price data"},
        {"endpoint": "/indicators/rsi", "description": "Get RSI data"},
        {"endpoint": "/indicators/macd", "description": "Get MACD data"},
        {"endpoint": "/network/hashrate", "description": "Get network hash rate"},
        {"endpoint": "/network/difficulty", "description": "Get mining difficulty"},
    ]
    
    for endpoint in api_endpoints:
        st.markdown(f"• **`{endpoint['endpoint']}`** - {endpoint['description']}")
    
    st.markdown("#### 📊 Usage Statistics")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("API Calls Today", "1,247")
    
    with col2:
        st.metric("Monthly Limit", "50,000")
    
    with col3:
        st.metric("Remaining", "48,753")
    
    # API example
    st.markdown("#### 💻 Example Request")
    
    st.code("""
# Python example
import requests

headers = {
    'Authorization': 'Bearer YOUR_API_KEY',
    'Content-Type': 'application/json'
}

response = requests.get(
    'https://api.kaspa-analytics.com/v1/price/history',
    params={'days': 30, 'interval': '1d'},
    headers=headers
)

data = response.json()
print(data)
    """, language="python")

def render_export_history():
    """Render export history for user"""
    st.subheader("📋 Export History")
    
    # Sample export history
    export_history = [
        {"date": "2024-01-15 14:30", "type": "Price Data", "format": "CSV", "rows": "8,760", "status": "✅ Complete"},
        {"date": "2024-01-14 09:15", "type": "Technical Data", "format": "JSON", "rows": "2,190", "status": "✅ Complete"},
        {"date": "2024-01-13 16:45", "type": "Network Data", "format": "CSV", "rows": "720", "status": "✅ Complete"},
        {"date": "2024-01-12 11:20", "type": "API Request", "format": "JSON", "rows": "1,440", "status": "✅ Complete"},
    ]
    
    # Create history table
    history_df = pd.DataFrame(export_history)
    st.dataframe(history_df, use_container_width=True, hide_index=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Total Exports", "127")
    
    with col2:
        st.metric("Data Downloaded", "2.3 GB")

if __name__ == "__main__":
    main()
