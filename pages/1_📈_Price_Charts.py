"""
Price Charts Page - Kaspa Analytics Pro
Advanced price charting and technical analysis - Available to all users
"""

import streamlit as st
import streamlit_antd_components as sac
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# Import utilities
from utils.auth import get_current_user
from utils.data import (
    fetch_kaspa_price_data, 
    get_technical_indicators,
    get_market_stats
)
from utils.ui import (
    render_page_header, 
    render_sidebar_navigation,
    show_create_account_prompt,
    apply_custom_css,
    render_chart_controls,
    render_footer
)

# Configure page
st.set_page_config(
    page_title="Price Charts - Kaspa Analytics Pro",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# SEO Meta Tags
st.markdown("""
<meta name="description" content="Advanced Kaspa price charts with technical analysis tools, indicators, and real-time data visualization.">
<meta name="keywords" content="Kaspa price charts, KAS technical analysis, cryptocurrency charts, blockchain price data">
<meta property="og:title" content="Kaspa Price Charts - Advanced Technical Analysis">
<meta property="og:description" content="Professional Kaspa price analysis with advanced charting tools and technical indicators">
<meta property="og:type" content="website">
""", unsafe_allow_html=True)

# Apply styling
apply_custom_css()

def main():
    """Main price charts page"""
    
    # Get current user
    user = get_current_user()
    
    # Render sidebar navigation
    render_sidebar_navigation(user)
    
    # Page header
    render_page_header(
        "📈 Advanced Price Charts",
        "Professional Kaspa price analysis with technical indicators - Free for everyone!"
    )
    
    # Breadcrumb navigation
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("← Dashboard", key="charts_back_to_home"):
            st.switch_page("streamlit_app.py")
    
    # Show user status
    if user['username'] == 'public':
        st.info("📊 You're viewing as a public user - all charts and indicators are free! Consider creating an account to track your usage.")
    else:
        st.success(f"📊 Welcome, {user['name']}! All charting features are available in your {user['subscription']} account.")
    
    # Main charting interface
    render_advanced_charts(user)
    
    # Account suggestion for public users
    if user['username'] == 'public':
        st.markdown("---")
        show_create_account_prompt()
    
    # Footer
    render_footer()

def render_advanced_charts(user):
    """Render full advanced charting interface for all users"""
    
    # Fetch full historical data for everyone
    df = fetch_kaspa_price_data(365 * 2)  # 2 years of data for all
    
    if df.empty:
        st.error("Unable to load price data")
        return
    
    # Advanced chart controls in tabs
    chart_tabs = sac.tabs([
        sac.TabsItem(label='Chart', icon='graph-up'),
        sac.TabsItem(label='Indicators', icon='sliders'),
        sac.TabsItem(label='Analysis', icon='search'),
        sac.TabsItem(label='Settings', icon='gear'),
    ], key='chart_tabs')
    
    if chart_tabs == 'Chart':
        render_main_chart_tab(df, user)
    elif chart_tabs == 'Indicators':
        render_indicators_tab(df)
    elif chart_tabs == 'Analysis':
        render_analysis_tab(df)
    else:
        render_settings_tab()

def render_main_chart_tab(df, user):
    """Main charting interface"""
    
    # Chart controls
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        chart_type = st.selectbox(
            "Chart Type",
            ["Line", "Candlestick", "Area", "OHLC"],
            index=1,  # Default to candlestick
            key="chart_type"
        )
    
    with col2:
        time_range = st.selectbox(
            "Time Range",
            ["7D", "30D", "3M", "6M", "1Y", "2Y", "All"],
            index=2,  # Default to 3M
            key="time_range"
        )
    
    with col3:
        timeframe = st.selectbox(
            "Timeframe",
            ["1H", "4H", "1D", "1W"],
            index=2,  # Default to 1D
            key="timeframe"
        )
    
    with col4:
        chart_style = st.selectbox(
            "Style",
            ["Light", "Dark", "Colorful"],
            key="chart_style"
        )
    
    # Filter data based on time range
    if time_range == "7D":
        chart_data = df.tail(7 * 24)
    elif time_range == "30D":
        chart_data = df.tail(30 * 24)
    elif time_range == "3M":
        chart_data = df.tail(90 * 24)
    elif time_range == "6M":
        chart_data = df.tail(180 * 24)
    elif time_range == "1Y":
        chart_data = df.tail(365 * 24)
    elif time_range == "2Y":
        chart_data = df.tail(730 * 24)
    else:
        chart_data = df
    
    # Advanced indicators selection
    col1, col2 = st.columns(2)
    
    with col1:
        overlay_indicators = st.multiselect(
            "Overlay Indicators",
            ["SMA 20", "SMA 50", "EMA 12", "EMA 26", "Bollinger Bands", "VWAP"],
            default=["SMA 20", "Bollinger Bands"],
            key="overlay_indicators"
        )
    
    with col2:
        oscillator_indicators = st.multiselect(
            "Oscillator Indicators",
            ["RSI", "MACD", "Stochastic", "Williams %R"],
            default=["RSI", "MACD"],
            key="oscillator_indicators"
        )
    
    # Additional options
    col1, col2, col3 = st.columns(3)
    
    with col1:
        show_volume = st.checkbox("Show Volume", value=True, key="show_volume")
    
    with col2:
        show_events = st.checkbox("Show Events", value=False, key="show_events")
    
    with col3:
        auto_scale = st.checkbox("Auto Scale", value=True, key="auto_scale")
    
    # Create professional chart
    fig = create_professional_chart(
        chart_data, 
        chart_type, 
        overlay_indicators, 
        oscillator_indicators,
        show_volume,
        show_events,
        chart_style,
        f"{time_range} Kaspa Price Analysis"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Market statistics
    render_market_statistics(chart_data)

def create_professional_chart(df, chart_type, overlay_indicators, oscillator_indicators, 
                            show_volume, show_events, chart_style, title):
    """Create professional chart for all users"""
    from plotly.subplots import make_subplots
    
    # Determine number of subplots
    subplot_count = 1
    if show_volume:
        subplot_count += 1
    if oscillator_indicators:
        subplot_count += len(oscillator_indicators)
    
    # Create subplots
    subplot_titles = [title]
    if show_volume:
        subplot_titles.append("Volume")
    for indicator in oscillator_indicators:
        subplot_titles.append(indicator)
    
    fig = make_subplots(
        rows=subplot_count,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.02,
        subplot_titles=subplot_titles,
        row_heights=[0.6] + [0.2] * (subplot_count - 1)
    )
    
    # Main price chart
    if chart_type == "Line":
        fig.add_trace(go.Scatter(
            x=df['timestamp'],
            y=df['price'],
            mode='lines',
            name='KAS Price',
            line=dict(color='#70C7BA', width=2)
        ), row=1, col=1)
    elif chart_type == "Candlestick":
        fig.add_trace(go.Candlestick(
            x=df['timestamp'],
            open=df['open'],
            high=df['high'],
            low=df['low'],
            close=df['close'],
            name='KAS Price'
        ), row=1, col=1)
    elif chart_type == "Area":
        fig.add_trace(go.Scatter(
            x=df['timestamp'],
            y=df['price'],
            mode='lines',
            fill='tonexty',
            name='KAS Price',
            line=dict(color='#70C7BA')
        ), row=1, col=1)
    elif chart_type == "OHLC":
        fig.add_trace(go.Ohlc(
            x=df['timestamp'],
            open=df['open'],
            high=df['high'],
            low=df['low'],
            close=df['close'],
            name='KAS Price'
        ), row=1, col=1)
    
    # Add overlay indicators
    current_row = 1
    
    for indicator in overlay_indicators:
        if indicator == "SMA 20":
            sma_20 = df['price'].rolling(window=20).mean()
            fig.add_trace(go.Scatter(
                x=df['timestamp'],
                y=sma_20,
                mode='lines',
                name='SMA 20',
                line=dict(color='orange', dash='dash')
            ), row=current_row, col=1)
        
        elif indicator == "SMA 50":
            sma_50 = df['price'].rolling(window=50).mean()
            fig.add_trace(go.Scatter(
                x=df['timestamp'],
                y=sma_50,
                mode='lines',
                name='SMA 50',
                line=dict(color='red', dash='dash')
            ), row=current_row, col=1)
        
        elif indicator == "EMA 12":
            ema_12 = df['price'].ewm(span=12).mean()
            fig.add_trace(go.Scatter(
                x=df['timestamp'],
                y=ema_12,
                mode='lines',
                name='EMA 12',
                line=dict(color='blue', dash='dot')
            ), row=current_row, col=1)
        
        elif indicator == "EMA 26":
            ema_26 = df['price'].ewm(span=26).mean()
            fig.add_trace(go.Scatter(
                x=df['timestamp'],
                y=ema_26,
                mode='lines',
                name='EMA 26',
                line=dict(color='purple', dash='dot')
            ), row=current_row, col=1)
        
        elif indicator == "Bollinger Bands":
            bb_middle = df['price'].rolling(window=20).mean()
            bb_std = df['price'].rolling(window=20).std()
            bb_upper = bb_middle + (bb_std * 2)
            bb_lower = bb_middle - (bb_std * 2)
            
            fig.add_trace(go.Scatter(
                x=df['timestamp'],
                y=bb_upper,
                mode='lines',
                name='BB Upper',
                line=dict(color='gray', dash='dash'),
                showlegend=False
            ), row=current_row, col=1)
            
            fig.add_trace(go.Scatter(
                x=df['timestamp'],
                y=bb_lower,
                mode='lines',
                name='BB Lower',
                line=dict(color='gray', dash='dash'),
                fill='tonexty',
                fillcolor='rgba(128,128,128,0.1)',
                showlegend=False
            ), row=current_row, col=1)
            
            fig.add_trace(go.Scatter(
                x=df['timestamp'],
                y=bb_middle,
                mode='lines',
                name='BB Middle',
                line=dict(color='gray')
            ), row=current_row, col=1)
    
    # Add volume
    if show_volume:
        current_row += 1
        fig.add_trace(go.Bar(
            x=df['timestamp'],
            y=df['volume'],
            name='Volume',
            marker_color='lightblue',
            opacity=0.7
        ), row=current_row, col=1)
    
    # Add oscillator indicators
    indicators_data = get_technical_indicators(df)
    
    for indicator in oscillator_indicators:
        current_row += 1
        
        if indicator == "RSI" and indicators_data:
            rsi_data = indicators_data.get('rsi', [])
            if rsi_data:
                fig.add_trace(go.Scatter(
                    x=df['timestamp'],
                    y=rsi_data,
                    mode='lines',
                    name='RSI',
                    line=dict(color='purple')
                ), row=current_row, col=1)
                
                # Add RSI levels
                fig.add_hline(y=70, line_dash="dash", line_color="red", 
                             annotation_text="Overbought", row=current_row, col=1)
                fig.add_hline(y=30, line_dash="dash", line_color="green", 
                             annotation_text="Oversold", row=current_row, col=1)
        
        elif indicator == "MACD" and indicators_data:
            macd_line = indicators_data.get('macd_line', [])
            macd_signal = indicators_data.get('macd_signal', [])
            macd_histogram = indicators_data.get('macd_histogram', [])
            
            if macd_line:
                fig.add_trace(go.Scatter(
                    x=df['timestamp'],
                    y=macd_line,
                    mode='lines',
                    name='MACD',
                    line=dict(color='blue')
                ), row=current_row, col=1)
            
            if macd_signal:
                fig.add_trace(go.Scatter(
                    x=df['timestamp'],
                    y=macd_signal,
                    mode='lines',
                    name='Signal',
                    line=dict(color='red')
                ), row=current_row, col=1)
            
            if macd_histogram:
                fig.add_trace(go.Bar(
                    x=df['timestamp'],
                    y=macd_histogram,
                    name='Histogram',
                    marker_color='gray',
                    opacity=0.6
                ), row=current_row, col=1)
    
    # Apply chart style
    template = "plotly_white"
    if chart_style == "Dark":
        template = "plotly_dark"
    elif chart_style == "Colorful":
        template = "ggplot2"
    
    fig.update_layout(
        height=800,
        template=template,
        showlegend=True,
        xaxis_rangeslider_visible=False
    )
    
    return fig

def render_indicators_tab(df):
    """Technical indicators detailed view"""
    st.subheader("📊 Technical Indicators Analysis")
    
    # Get technical indicators
    indicators = get_technical_indicators(df)
    
    if not indicators:
        st.warning("Unable to calculate technical indicators")
        return
    
    # Current indicator values
    current_values = indicators.get('current_values', {})
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        rsi_value = current_values.get('rsi')
        if rsi_value:
            rsi_color = "red" if rsi_value > 70 else "green" if rsi_value < 30 else "orange"
            st.metric("RSI (14)", f"{rsi_value:.1f}", help="Relative Strength Index")
            st.markdown(f"<span style='color: {rsi_color}'>{'Overbought' if rsi_value > 70 else 'Oversold' if rsi_value < 30 else 'Neutral'}</span>", unsafe_allow_html=True)
    
    with col2:
        macd_value = current_values.get('macd')
        if macd_value:
            st.metric("MACD", f"{macd_value:.6f}", help="Moving Average Convergence Divergence")
    
    with col3:
        bb_position = current_values.get('bb_position')
        if bb_position:
            st.metric("BB Position", f"{bb_position:.2f}", help="Position within Bollinger Bands")
    
    # Detailed indicator charts
    indicator_tabs = sac.tabs([
        sac.TabsItem(label='RSI', icon='activity'),
        sac.TabsItem(label='MACD', icon='trending-up'),
        sac.TabsItem(label='Bollinger Bands', icon='layers'),
    ], key='indicator_detail_tabs')
    
    if indicator_tabs == 'RSI':
        render_rsi_chart(df, indicators)
    elif indicator_tabs == 'MACD':
        render_macd_chart(df, indicators)
    else:
        render_bollinger_chart(df, indicators)

def render_analysis_tab(df):
    """Market analysis and insights"""
    st.subheader("🔍 Market Analysis")
    
    # Price action analysis
    stats = get_market_stats(df)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📈 Price Action")
        
        # Support and resistance levels
        recent_data = df.tail(100)
        resistance = recent_data['high'].max()
        support = recent_data['low'].min()
        current_price = df['price'].iloc[-1]
        
        st.write(f"**Resistance:** ${resistance:.4f}")
        st.write(f"**Current:** ${current_price:.4f}")
        st.write(f"**Support:** ${support:.4f}")
        
        # Price position
        position = (current_price - support) / (resistance - support)
        st.progress(position)
        st.write(f"Price position: {position:.1%} of range")
    
    with col2:
        st.markdown("#### 📊 Volume Analysis")
        
        avg_volume = df['volume'].tail(30).mean()
        current_volume = df['volume'].iloc[-1]
        volume_ratio = current_volume / avg_volume
        
        st.metric("Volume vs 30D Avg", f"{volume_ratio:.2f}x")
        
        if volume_ratio > 1.5:
            st.success("High volume - Strong interest")
        elif volume_ratio < 0.5:
            st.warning("Low volume - Weak interest")
        else:
            st.info("Normal volume levels")

def render_settings_tab():
    """Chart settings and preferences"""
    st.subheader("⚙️ Chart Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🎨 Appearance")
        
        theme = st.selectbox(
            "Chart Theme",
            ["Light", "Dark", "Auto"],
            key="chart_theme_setting"
        )
        
        color_scheme = st.selectbox(
            "Color Scheme",
            ["Default", "Colorblind Friendly", "High Contrast"],
            key="chart_color_scheme"
        )
        
        show_grid = st.checkbox("Show Grid", value=True, key="chart_show_grid")
        show_crosshair = st.checkbox("Show Crosshair", value=True, key="chart_show_crosshair")
    
    with col2:
        st.markdown("#### 📊 Data")
        
        auto_refresh = st.checkbox("Auto Refresh", value=False, key="chart_auto_refresh")
        
        if auto_refresh:
            refresh_interval = st.selectbox(
                "Refresh Interval",
                ["30 seconds", "1 minute", "5 minutes"],
                key="chart_refresh_interval"
            )
        
        data_source = st.selectbox(
            "Data Source",
            ["Primary", "Backup", "Aggregated"],
            key="chart_data_source"
        )
    
    # Save settings
    if st.button("💾 Save Settings", key="save_chart_settings"):
        st.success("Settings saved successfully!")

def render_market_statistics(df):
    """Render comprehensive market statistics"""
    st.subheader("📊 Market Statistics")
    
    stats = get_market_stats(df)
    
    # Main statistics
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            "Current Price", 
            f"${stats.get('current_price', 0):.4f}",
            delta=f"{stats.get('price_change_24h', 0):+.2f}%"
        )
    
    with col2:
        st.metric("24h High", f"${stats.get('high_24h', 0):.4f}")
    
    with col3:
        st.metric("24h Low", f"${stats.get('low_24h', 0):.4f}")
    
    with col4:
        st.metric("24h Volume", f"${stats.get('volume_24h', 0)/1000000:.1f}M")
    
    with col5:
        st.metric("Market Cap", f"${stats.get('market_cap', 0):.1f}B")

def render_rsi_chart(df, indicators):
    """Render RSI indicator chart"""
    st.markdown("#### RSI (Relative Strength Index)")
    
    rsi_data = indicators.get('rsi', [])
    if not rsi_data:
        st.warning("RSI data not available")
        return
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df['timestamp'],
        y=rsi_data,
        mode='lines',
        name='RSI',
        line=dict(color='purple', width=2)
    ))
    
    # Add reference lines
    fig.add_hline(y=70, line_dash="dash", line_color="red", annotation_text="Overbought (70)")
    fig.add_hline(y=50, line_dash="dash", line_color="gray", annotation_text="Neutral (50)")
    fig.add_hline(y=30, line_dash="dash", line_color="green", annotation_text="Oversold (30)")
    
    # Color areas
    fig.add_hrect(y0=70, y1=100, fillcolor="red", opacity=0.1)
    fig.add_hrect(y0=0, y1=30, fillcolor="green", opacity=0.1)
    
    fig.update_layout(
        title="RSI Indicator",
        xaxis_title="Date",
        yaxis_title="RSI",
        height=300,
        yaxis=dict(range=[0, 100])
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_macd_chart(df, indicators):
    """Render MACD indicator chart"""
    st.markdown("#### MACD (Moving Average Convergence Divergence)")
    
    macd_line = indicators.get('macd_line', [])
    macd_signal = indicators.get('macd_signal', [])
    macd_histogram = indicators.get('macd_histogram', [])
    
    if not macd_line:
        st.warning("MACD data not available")
        return
    
    fig = go.Figure()
    
    # MACD line
    fig.add_trace(go.Scatter(
        x=df['timestamp'],
        y=macd_line,
        mode='lines',
        name='MACD',
        line=dict(color='blue', width=2)
    ))
    
    # Signal line
    if macd_signal:
        fig.add_trace(go.Scatter(
            x=df['timestamp'],
            y=macd_signal,
            mode='lines',
            name='Signal',
            line=dict(color='red', width=2)
        ))
    
    # Histogram
    if macd_histogram:
        colors = ['green' if h > 0 else 'red' for h in macd_histogram]
        fig.add_trace(go.Bar(
            x=df['timestamp'],
            y=macd_histogram,
            name='Histogram',
            marker_color=colors,
            opacity=0.6
        ))
    
    fig.add_hline(y=0, line_dash="dash", line_color="gray")
    
    fig.update_layout(
        title="MACD Indicator",
        xaxis_title="Date",
        yaxis_title="MACD",
        height=300
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_bollinger_chart(df, indicators):
    """Render Bollinger Bands chart"""
    st.markdown("#### Bollinger Bands")
    
    bb_upper = indicators.get('bb_upper', [])
    bb_middle = indicators.get('bb_middle', [])
    bb_lower = indicators.get('bb_lower', [])
    
    if not bb_upper:
        st.warning("Bollinger Bands data not available")
        return
    
    fig = go.Figure()
    
    # Price
    fig.add_trace(go.Scatter(
        x=df['timestamp'],
        y=df['price'],
        mode='lines',
        name='Price',
        line=dict(color='blue', width=2)
    ))
    
    # Upper band
    fig.add_trace(go.Scatter(
        x=df['timestamp'],
        y=bb_upper,
        mode='lines',
        name='Upper Band',
        line=dict(color='red', dash='dash')
    ))
    
    # Lower band
    fig.add_trace(go.Scatter(
        x=df['timestamp'],
        y=bb_lower,
        mode='lines',
        name='Lower Band',
        line=dict(color='green', dash='dash'),
        fill='tonexty',
        fillcolor='rgba(128,128,128,0.1)'
    ))
    
    # Middle band
    fig.add_trace(go.Scatter(
        x=df['timestamp'],
        y=bb_middle,
        mode='lines',
        name='Middle Band (SMA 20)',
        line=dict(color='orange')
    ))
    
    fig.update_layout(
        title="Bollinger Bands",
        xaxis_title="Date",
        yaxis_title="Price (USD)",
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()
