"""
Authentication utilities for Kaspa Analytics Pro
Handles user authentication, session management, and authorization
"""

import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import bcrypt
from datetime import datetime
import os
from pathlib import Path

def get_auth_config():
    """Get authentication configuration"""
    config_path = Path("config/user_config.yaml")
    
    # Default configuration if file doesn't exist
    default_config = {
        'credentials': {
            'usernames': {
                'admin': {
                    'email': 'admin@kaspalytics.com',
                    'first_name': 'Admin',
                    'last_name': 'User',
                    'password': 'admin123',
                    'subscription': 'premium',
                    'failed_login_attempts': 0,
                    'logged_in': False
                },
                'premium_user': {
                    'email': 'premium@example.com',
                    'first_name': 'Premium',
                    'last_name': 'User',
                    'password': 'premium123',
                    'subscription': 'premium',
                    'failed_login_attempts': 0,
                    'logged_in': False
                },
                'free_user': {
                    'email': 'free@example.com',
                    'first_name': 'Free',
                    'last_name': 'User',
                    'password': 'free123',
                    'subscription': 'free',
                    'failed_login_attempts': 0,
                    'logged_in': False
                }
            }
        },
        'cookie': {
            'name': 'kaspa_analytics_auth',
            'key': 'kaspa_secret_key_change_in_production',
            'expiry_days': 30
        },
        'preauthorized': [
            'admin@kaspalytics.com',
            'newuser@kaspalytics.com'
        ]
    }
    
    # Try to load from file, fallback to default
    try:
        if config_path.exists():
            with open(config_path, 'r') as file:
                config = yaml.load(file, Loader=SafeLoader)
        else:
            config = default_config
    except Exception:
        config = default_config
    
    # Store in session state for persistence
    if 'auth_config' not in st.session_state:
        st.session_state.auth_config = config
    
    return st.session_state.auth_config

def get_authenticator():
    """Initialize and return authenticator instance"""
    config = get_auth_config()
    
    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
        config['preauthorized'],
        auto_hash=True
    )
    
    return authenticator

def is_authenticated():
    """Check if user is currently authenticated"""
    return st.session_state.get('authentication_status') is True

def get_current_user():
    """Get current user information"""
    if is_authenticated():
        username = st.session_state.get('username')
        name = st.session_state.get('name')
        
        # Get subscription level
        config = get_auth_config()
        user_info = config['credentials']['usernames'].get(username, {})
        subscription = user_info.get('subscription', 'free')
        
        return {
            'name': name,
            'username': username,
            'subscription': subscription,
            'email': user_info.get('email', ''),
            'first_name': user_info.get('first_name', ''),
            'last_name': user_info.get('last_name', '')
        }
    else:
        return {
            'name': 'Public User',
            'username': 'public',
            'subscription': 'public',
            'email': '',
            'first_name': '',
            'last_name': ''
        }

def require_authentication_for_premium():
    """Require authentication and premium subscription for data export"""
    user = get_current_user()
    
    if user['username'] == 'public':
        st.error("🔐 This feature requires a Premium account")
        st.info("Please create an account and upgrade to Premium to access data export")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔑 Login", key="require_auth_login", use_container_width=True):
                st.switch_page("pages/5_⚙️_Authentication.py")
        with col2:
            if st.button("🚀 Sign Up", key="require_auth_signup", use_container_width=True, type="primary"):
                st.switch_page("pages/5_⚙️_Authentication.py")
        
        st.stop()
    
    if user['subscription'] != 'premium':
        st.error("🔒 This feature requires Premium subscription")
        st.info(f"Current plan: {user['subscription'].title()}")
        
        if st.button("⬆️ Upgrade to Premium", key="require_premium_upgrade", use_container_width=True, type="primary"):
            st.switch_page("pages/5_⚙️_Authentication.py")
        
        st.stop()
    
    return user

def add_user(username, email, first_name, last_name, password, subscription='free'):
    """Add new user to the system"""
    config = get_auth_config()
    
    if username in config['credentials']['usernames']:
        return False, "Username already exists"
    
    # Validate email format
    if '@' not in email:
        return False, "Invalid email format"
    
    # Hash password
    try:
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    except Exception as e:
        return False, f"Password hashing error: {e}"
    
    # Add user to config
    config['credentials']['usernames'][username] = {
        'email': email,
        'first_name': first_name,
        'last_name': last_name,
        'password': hashed_password,
        'subscription': subscription,
        'failed_login_attempts': 0,
        'logged_in': False,
        'created_at': datetime.now().isoformat()
    }
    
    # Update session state
    st.session_state.auth_config = config
    
    return True, "User created successfully"

def update_user_subscription(username, new_subscription):
    """Update user subscription level"""
    config = get_auth_config()
    
    if username not in config['credentials']['usernames']:
        return False, "User not found"
    
    config['credentials']['usernames'][username]['subscription'] = new_subscription
    st.session_state.auth_config = config
    
    return True, f"Subscription updated to {new_subscription}"

def logout_user():
    """Log out current user"""
    # Clear authentication session state
    auth_keys = [
        'authentication_status', 
        'name', 
        'username', 
        'logout'
    ]
    
    for key in auth_keys:
        if key in st.session_state:
            del st.session_state[key]
    
    # Try authenticator logout
    try:
        authenticator = get_authenticator()
        authenticator.logout()
    except:
        pass
    
    # Clear any page-specific session state
    page_keys = [
        'show_profile', 
        'show_auth', 
        'auth_tab',
        'current_page'
    ]
    
    for key in page_keys:
        if key in st.session_state:
            del st.session_state[key]

def get_subscription_features(subscription_level):
    """Get features available for subscription level"""
    features = {
        'public': {
            'data_days': 0,  # unlimited for all
            'charts': ['basic', 'technical', 'advanced'],
            'export': False,
            'api': False,
            'support': 'community'
        },
        'free': {
            'data_days': 0,  # unlimited
            'charts': ['basic', 'technical', 'advanced'],
            'export': False,
            'api': False,
            'support': 'community'
        },
        'premium': {
            'data_days': 0,  # unlimited
            'charts': ['basic', 'technical', 'advanced'],
            'export': True,  # Only premium gets export
            'api': True,
            'support': 'email'
        }
    }
    
    return features.get(subscription_level, features['public'])

def check_feature_access(feature_name, user_subscription):
    """Check if user has access to specific feature"""
    feature_requirements = {
        # All features available to everyone except data export
        'price_charts': ['public', 'free', 'premium'],
        'power_law': ['public', 'free', 'premium'],
        'network_metrics': ['public', 'free', 'premium'],
        'technical_indicators': ['public', 'free', 'premium'],
        'advanced_charts': ['public', 'free', 'premium'],
        # Only data export requires premium
        'data_export': ['premium'],
        'api_access': ['premium'],
    }
    
    required_subscriptions = feature_requirements.get(feature_name, ['public', 'free', 'premium'])
    return user_subscription in required_subscriptions

def save_auth_config():
    """Save authentication configuration to file"""
    try:
        config_path = Path("config/user_config.yaml")
        config_path.parent.mkdir(exist_ok=True)
        
        config = st.session_state.get('auth_config', {})
        
        with open(config_path, 'w') as file:
            yaml.dump(config, file, default_flow_style=False)
        
        return True
    except Exception as e:
        st.error(f"Error saving configuration: {e}")
        return False

def get_user_stats(username):
    """Get user statistics and activity"""
    # This would typically come from a database
    # For demo purposes, return mock data
    return {
        'login_count': 42,
        'last_login': '2024-01-15',
        'features_used': ['price_charts', 'power_law', 'network_metrics'],
        'subscription_start': '2024-01-01',
        'data_exports': 15,
        'api_calls': 1250
    }
