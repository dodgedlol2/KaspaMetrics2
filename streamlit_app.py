"""
Kaspa Analytics Pro - Main Homepage
Entry point for the multi-page Streamlit application
"""

import streamlit as st
import streamlit_antd_components as sac
from datetime import datetime
import pandas as pd
import numpy as np

# Try to import Plotly, fallback gracefully
try:
    import plotly.graph_objects as go
    import plotly.express as px
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False

# Import utilities
from utils.auth import get_current_user, is_authenticated
from utils.data import fetch_kaspa_price_data, get_market_stats
from utils.ui import (
    render_page_header, 
    render_sidebar_navigation, 
    show_create_account_prompt,
    apply_custom_css,
    render_footer
)
from utils.config import get_app_config

# Configure page settings
st.set_page_config(
    page_title="Kaspa Analytics Pro - Professional Blockchain Analysis",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://kaspa-analytics.com/help',
        'Report a bug': 'https://kaspa-analytics.com/bug-report',
        'About': "# Kaspa Analytics Pro\nProfessional blockchain analysis platform"
    }
)

# SEO and Social Media Meta Tags
st.markdown("""
<meta name="description" content="Professional Kaspa blockchain analysis platform with advanced power law models, network metrics, and real-time price tracking.">
<meta name="keywords" content="Kaspa, KAS, blockchain, cryptocurrency, analysis, power law, price prediction, technical analysis">
<meta name="author" content="Kaspa Analytics Pro">

<!-- Open Graph / Facebook -->
<meta property="og:type" content="website">
<meta property="og:url" content="https://kaspa-analytics.com/">
<meta property="og:title" content="Kaspa Analytics Pro - Professional Blockchain Analysis">
<meta property="og:description" content="Advanced Kaspa blockchain analysis with power law models, network metrics, and professional trading tools.">
<meta property="og:image" content="https://kaspa-analytics.com/assets/social_preview.png">

<!-- Twitter -->
<meta property="twitter:card" content="summary_large_image">
<meta property="twitter:url" content="https://kaspa-analytics.com/">
<meta property="twitter:title" content="Kaspa Analytics Pro">
<meta property="twitter:description" content="Professional Kaspa blockchain analysis platform">
<meta property="twitter:image" content="https://kaspa-analytics.com/assets/social_preview.png">

<!-- Favicon -->
<link rel="icon" type="image/png" href="/assets/favicon.ico">
""", unsafe_allow_html=True)

# Apply custom CSS
apply_custom_css()

# Google Analytics (placeholder)
st.markdown("""
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_MEASUREMENT_ID');
</script>
""", unsafe_allow_html=True)

def main():
    """Main homepage function"""
    
    # Get current user and app config
    user = get_current_user()
    config = get_app_config()
    is_auth = is_authenticated()
    
    # Render sidebar navigation
    render_sidebar_navigation(user)
    
    # Main content
    if is_auth:
        render_authenticated_homepage(user)
    else:
        render_public_homepage()
    
    # Footer
    render_footer()

def render_public_homepage():
    """Public homepage for non-authenticated users"""
    
    # Hero section
    render_page_header(
        "💎 Kaspa Analytics Pro",
        "Professional blockchain analysis platform for Kaspa (KAS) - Free for everyone!",
        show_auth_buttons=True
    )
    
    # Key metrics showcase
    st.subheader("📊 Live Market Data")
    
    col1, col2, col3, col4 = st.columns(4)
    
    # Get market data
    df = fetch_kaspa_price_data()
    stats = get_market_stats(df) if not df.empty else {}
    
    with col1:
        st.metric(
            "KAS Price", 
            f"${stats.get('current_price', 0):.4f}",
            delta=f"{stats.get('price_change_7d', 0):+.2f}%"
        )
    
    with col2:
        st.metric(
            "24h Volume", 
            f"${stats.get('volume_24h', 0):,.0f}"
        )
    
    with col3:
        st.metric(
            "Market Cap", 
            f"${stats.get('market_cap', 0):.1f}B"
        )
    
    with col4:
        st.metric(
            "Network Hash Rate", 
            f"{stats.get('hash_rate', 0):.2f} EH/s"
        )
    
    # Quick chart preview
    if not df.empty:
        st.subheader("📈 Price Chart Preview")
        chart_data = df.tail(30)  # 30 days for public preview
        
        if PLOTLY_AVAILABLE:
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=chart_data['timestamp'], 
                y=chart_data['price'],
                mode='lines',
                name='KAS Price',
                line=dict(color='#70C7BA', width=3)
            ))
            
            fig.update_layout(
                title="Kaspa Price - Last 30 Days (Free Access)",
                xaxis_title="Date",
                yaxis_title="Price (USD)",
                height=400,
                template="plotly_white",
                showlegend=False
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            # Fallback to basic line chart
            st.line_chart(chart_data.set_index('timestamp')['price'])
        
        st.info("📊 All charts and analysis tools are free! Only data export requires Premium.")
    
    # Feature showcase
    st.subheader("🚀 What's Available")
    
    feature_tabs = sac.tabs([
        sac.TabsItem(label='Free Features', icon='check-circle'),
        sac.TabsItem(label='Premium Features', icon='star'),
        sac.TabsItem(label='Getting Started', icon='play'),
    ], key='feature_showcase')
    
    if feature_tabs == 'Free Features':
        render_free_features_showcase()
    elif feature_tabs == 'Premium Features':
        render_premium_features_showcase()
    else:
        render_getting_started_showcase()
    
    # Pricing
    st.subheader("💰 Simple Pricing")
    
    pricing_cols = st.columns(2)
    
    with pricing_cols[0]:
        with st.container():
            st.markdown("### 🆓 Free Forever")
            st.markdown("**$0/month**")
            st.write("• ✅ All price charts & analysis")
            st.write("• ✅ Power law models")
            st.write("• ✅ Network metrics")
            st.write("• ✅ Technical indicators")
            st.write("• ✅ Full historical data")
            st.write("• ✅ Real-time updates")
            
            if st.button("🚀 Start Free", key="pricing_free", use_container_width=True, type="primary"):
                st.info("You're already using it! All features above are free. Create an account to track usage.")
    
    with pricing_cols[1]:
        with st.container():
            st.markdown("### ⭐ Premium")
            st.markdown("**$29/month**")
            st.write("• ✅ Everything in Free")
            st.write("• 📋 Data export (CSV/JSON)")
            st.write("• 🔌 API access")
            st.write("• 📧 Email support")
            st.write("• 🎯 Priority features")
            st.write("• 📊 Advanced analytics")
            
            if st.button("⭐ Upgrade to Premium", key="pricing_premium", use_container_width=True):
                st.switch_page("pages/5_⚙️_Authentication.py")
    
    # Call to action for account creation
    st.markdown("---")
    show_create_account_prompt()

def render_authenticated_homepage(user):
    """Authenticated user dashboard"""
    
    subscription = user['subscription']
    
    # Welcome header
    render_page_header(
        f"👋 Welcome back, {user['name']}!",
        f"Your {subscription.title()} Dashboard",
        show_auth_buttons=False
    )
    
    # Quick stats dashboard
    col1, col2, col3, col4 = st.columns(4)
    
    df = fetch_kaspa_price_data()
    stats = get_market_stats(df) if not df.empty else {}
    
    with col1:
        st.metric(
            "KAS Price", 
            f"${stats.get('current_price', 0):.4f}",
            delta=f"{stats.get('price_change_24h', 0):+.2f}%"
        )
    
    with col2:
        st.metric("Your Plan", subscription.title())
    
    with col3:
        st.metric("All Features", "✅ Unlocked")
    
    with col4:
        if subscription == 'premium':
            st.metric("Data Export", "✅ Available")
        else:
            st.metric("Data Export", "⭐ Upgrade to Premium")
    
    # Enhanced chart for authenticated users
    if not df.empty:
        st.subheader("📈 Price Analysis Dashboard")
        
        chart_data = df.tail(365)  # 1 year for all users
        st.success(f"📊 {subscription.title()} account: Full access to all analytics tools")
        
        # Create advanced chart
        fig = go.Figure()
        
        # Price line
        fig.add_trace(go.Scatter(
            x=chart_data['timestamp'], 
            y=chart_data['price'],
            mode='lines',
            name='KAS Price',
            line=dict(color='#70C7BA', width=2)
        ))
        
        # Add volume
        if PLOTLY_AVAILABLE:
            fig.add_trace(go.Scatter(
                x=chart_data['timestamp'],
                y=chart_data['volume'] / 1000000,  # Scale volume
                mode='lines',
                name='Volume (M)',
                yaxis='y2',
                opacity=0.6,
                line=dict(color='orange')
            ))
            
            # Add secondary y-axis
            fig.update_layout(
                yaxis2=dict(
                    title="Volume (Millions)",
                    overlaying='y',
                    side='right',
                    showgrid=False
                )
            )
        
        if PLOTLY_AVAILABLE:
            fig.update_layout(
                title=f"Kaspa Price Analysis - {subscription.title()} View",
                xaxis_title="Date",
                yaxis_title="Price (USD)",
                height=500,
                template="plotly_white"
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            # Fallback to basic chart
            st.line_chart(chart_data.set_index('timestamp')['price'])
    
    # Quick actions dashboard
    st.subheader("⚡ Quick Actions")
    
    action_cols = st.columns(4)
    
    with action_cols[0]:
        if st.button("📈 Price Charts", key="dash_charts", use_container_width=True):
            st.switch_page("pages/1_📈_Price_Charts.py")
    
    with action_cols[1]:
        if st.button("📊 Power Law Analysis", key="dash_powerlaw", use_container_width=True):
            st.switch_page("pages/2_📊_Power_Law.py")
    
    with action_cols[2]:
        if st.button("🌐 Network Metrics", key="dash_network", use_container_width=True):
            st.switch_page("pages/3_🌐_Network_Metrics.py")
    
    with action_cols[3]:
        if subscription == 'premium':
            if st.button("📋 Data Export", key="dash_export", use_container_width=True):
                st.switch_page("pages/4_📋_Data_Export.py")
        else:
            if st.button("⭐ Get Premium", key="dash_premium", use_container_width=True):
                st.switch_page("pages/5_⚙️_Authentication.py")
    
    # Recent activity (placeholder)
    st.subheader("📋 Recent Activity")
    
    activity_data = [
        {"time": "2 hours ago", "action": "Viewed price charts", "status": "✅"},
        {"time": "1 day ago", "action": "Analyzed power law model", "status": "✅"},
        {"time": "3 days ago", "action": "Checked network metrics", "status": "✅"},
    ]
    
    for activity in activity_data:
        with st.container():
            col1, col2, col3 = st.columns([2, 4, 1])
            with col1:
                st.write(activity["time"])
            with col2:
                st.write(activity["action"])
            with col3:
                st.write(activity["status"])

def render_free_features_showcase():
    """Show what's available for free"""
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📈 Price Analysis")
        st.write("• **Advanced Charts**: Candlestick, OHLC, Area charts")
        st.write("• **Technical Indicators**: RSI, MACD, Bollinger Bands")
        st.write("• **Multiple Timeframes**: 1H, 4H, 1D, 1W")
        st.write("• **Full History**: Complete price data")
        st.write("• **Real-time Updates**: Live market data")
        
        if st.button("📈 Try Price Charts", key="try_charts", use_container_width=True):
            st.switch_page("pages/1_📈_Price_Charts.py")
    
    with col2:
        st.markdown("#### 🔬 Advanced Analytics")
        st.write("• **Power Law Models**: Mathematical predictions")
        st.write("• **Network Metrics**: Hash rate, difficulty, addresses")
        st.write("• **Market Analysis**: Support/resistance levels")
        st.write("• **Trend Analysis**: Moving averages, signals")
        st.write("• **Volume Analysis**: Trading volume insights")
        
        if st.button("📊 Try Power Law", key="try_powerlaw", use_container_width=True):
            st.switch_page("pages/2_📊_Power_Law.py")

def render_premium_features_showcase():
    """Show premium features"""
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📋 Data Export")
        st.write("• **CSV/JSON Export**: Download any dataset")
        st.write("• **Custom Date Ranges**: Export exactly what you need")
        st.write("• **Bulk Downloads**: Multiple datasets at once")
        st.write("• **Automated Reports**: Scheduled exports")
    
    with col2:
        st.markdown("#### 🔌 API Access")
        st.write("• **REST API**: Programmatic data access")
        st.write("• **Real-time Feeds**: Live data streams")
        st.write("• **50k Requests/Month**: Generous limits")
        st.write("• **Email Support**: Priority assistance")
    
    st.markdown("---")
    if st.button("⭐ Upgrade to Premium - $29/month", key="upgrade_premium_showcase", use_container_width=True, type="primary"):
        st.switch_page("pages/5_⚙️_Authentication.py")

def render_getting_started_showcase():
    """Show getting started guide"""
    st.markdown("#### 🚀 Getting Started")
    
    steps = [
        "1️⃣ **Explore Free**: Start with our price charts and analysis tools",
        "2️⃣ **Analyze Data**: Use power law models and technical indicators", 
        "3️⃣ **Monitor Network**: Check hash rate and network health",
        "4️⃣ **Create Account**: Track your usage and preferences",
        "5️⃣ **Upgrade Premium**: Get data export when you need it"
    ]
    
    for step in steps:
        st.markdown(step)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📈 Start with Charts", key="start_charts", use_container_width=True, type="primary"):
            st.switch_page("pages/1_📈_Price_Charts.py")
    
    with col2:
        if st.button("🚀 Create Account", key="start_account", use_container_width=True):
            st.switch_page("pages/5_⚙️_Authentication.py")

if __name__ == "__main__":
    main()
