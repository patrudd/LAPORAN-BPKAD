import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import base64
from datetime import datetime
import time

# ==========================================
# PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="Analisis Biaya Kendaraan",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# CUSTOM CSS STYLING - DARK MODE OPTIMIZED
# ==========================================
def load_custom_css():
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700;800&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    /* Main Background with Gradient */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 0;
    }
    
    /* Sidebar Styling - DARK MODE FIX */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e3c72 0%, #2a5298 100%);
    }
    
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: white !important;
    }
    
    [data-testid="stSidebar"] label {
        color: white !important;
    }
    
    /* Header Animation */
    @keyframes slideInDown {
        from {
            transform: translateY(-100%);
            opacity: 0;
        }
        to {
            transform: translateY(0);
            opacity: 1;
        }
    }
    
    .main-header {
        animation: slideInDown 1s ease-out;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 40px;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 40px;
        box-shadow: 0 15px 40px rgba(0,0,0,0.4);
    }
    
    .main-header h1 {
        color: white !important;
        font-size: 3.5em;
        font-weight: 700;
        margin: 0;
        text-shadow: 3px 3px 6px rgba(0,0,0,0.5);
        animation: titlePulse 2s ease-in-out infinite;
    }
    
    @keyframes titlePulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.02); }
    }
    
    .main-header p {
        color: #f0f0f0 !important;
        font-size: 1.4em;
        margin: 15px 0 0 0;
        animation: fadeIn 1.5s ease-in;
    }
    
    /* IMPROVED Metric Card Styling - DARK MODE OPTIMIZED */
    .metric-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        margin: 15px 5px;
        border-left: 8px solid #667eea;
        border-bottom: 4px solid #764ba2;
        min-height: 180px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    
    .metric-card:hover {
        transform: translateY(-10px) scale(1.03);
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.4);
        border-left: 8px solid #764ba2;
        background: linear-gradient(135deg, #fff 0%, #e8eaf6 100%);
    }
    
    .metric-value {
        font-size: 3em;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 15px 0;
        animation: numberGlow 2s ease-in-out infinite;
    }
    
    @keyframes numberGlow {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.8; }
    }
    
    .metric-label {
        font-size: 1.1em;
        color: #333 !important;
        text-transform: uppercase;
        letter-spacing: 2px;
        font-weight: 600;
    }
    
    /* Alert Box Styling - DARK MODE FIX */
    .alert-box {
        padding: 25px;
        border-radius: 15px;
        margin: 20px 0;
        animation: fadeInUp 0.6s ease-in;
        box-shadow: 0 5px 20px rgba(0,0,0,0.15);
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    @keyframes fadeInUp {
        from { 
            opacity: 0;
            transform: translateY(30px);
        }
        to { 
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .alert-danger {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white !important;
        border-left: 6px solid #c0392b;
    }
    
    .alert-danger * {
        color: white !important;
    }
    
    .alert-warning {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        color: #333 !important;
        border-left: 6px solid #e67e22;
    }
    
    .alert-warning * {
        color: #333 !important;
    }
    
    .alert-success {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        color: #333 !important;
        border-left: 6px solid #27ae60;
    }
    
    .alert-success * {
        color: #333 !important;
    }
    
    .alert-info {
        background: linear-gradient(135deg, #a1c4fd 0%, #c2e9fb 100%);
        color: #333 !important;
        border-left: 6px solid #3498db;
    }
    
    .alert-info * {
        color: #333 !important;
    }
    
    /* Table Styling */
    .dataframe {
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 8px 20px rgba(0,0,0,0.15);
    }
    
    /* Button Styling - Enhanced */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none;
        padding: 15px 40px;
        border-radius: 30px;
        font-weight: 700;
        transition: all 0.4s ease;
        text-transform: uppercase;
        letter-spacing: 2px;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton>button:hover {
        transform: scale(1.08) translateY(-2px);
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.5);
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%) !important;
    }
    
    /* Loading Animation */
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    .loading {
        animation: pulse 1.5s ease-in-out infinite;
    }
    
    /* Section Headers - DARK MODE FIX */
    .section-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
        padding: 20px 30px;
        border-radius: 15px;
        margin: 30px 0 20px 0;
        font-size: 1.8em;
        font-weight: 700;
        box-shadow: 0 8px 20px rgba(0,0,0,0.3);
        animation: slideInLeft 0.8s ease-out;
    }
    
    /* Progress Bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Tabs Styling - DARK MODE FIX */
    .stTabs [data-baseweb="tab-list"] {
        gap: 15px;
        background-color: rgba(255,255,255,0.95);
        border-radius: 15px;
        padding: 15px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #f0f0f0;
        color: #333 !important;
        border-radius: 10px;
        padding: 12px 25px;
        font-weight: 700;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
        transform: scale(1.05);
    }
    
    /* Expander Styling */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
        border-radius: 10px;
        font-weight: 700;
    }
    
    /* Footer - DARK MODE FIX */
    .footer {
        text-align: center;
        padding: 40px;
        margin-top: 60px;
        background: rgba(255,255,255,0.15);
        border-radius: 20px;
        color: white !important;
        backdrop-filter: blur(10px);
    }
    
    .footer * {
        color: white !important;
    }
    
    /* Metric Container Animation */
    @keyframes slideInLeft {
        from {
            transform: translateX(-100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideInRight {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    .slide-left {
        animation: slideInLeft 0.8s ease-out;
    }
    
    .slide-right {
        animation: slideInRight 0.8s ease-out;
    }
    
    /* Card Grid */
    .card-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 25px;
        margin: 25px 0;
    }
    
    /* Sparkline Container */
    .sparkline-container {
        background: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        margin: 15px 0;
    }
    
    /* Badge Styling - Enhanced */
    .badge {
        display: inline-block;
        padding: 8px 20px;
        border-radius: 25px;
        font-size: 0.9em;
        font-weight: 700;
        margin: 5px;
        box-shadow: 0 3px 10px rgba(0,0,0,0.2);
        transition: transform 0.3s ease;
    }
    
    .badge:hover {
        transform: scale(1.1);
    }
    
    .badge-danger {
        background-color: #e74c3c;
        color: white !important;
    }
    
    .badge-warning {
        background-color: #f39c12;
        color: white !important;
    }
    
    .badge-success {
        background-color: #27ae60;
        color: white !important;
    }
    
    .badge-info {
        background-color: #3498db;
        color: white !important;
    }
    
    /* Tooltip */
    .tooltip {
        position: relative;
        display: inline-block;
        cursor: help;
    }
    
    /* Highlight Animation */
    @keyframes highlight {
        0% { background-color: transparent; }
        50% { background-color: rgba(255, 255, 0, 0.3); }
        100% { background-color: transparent; }
    }
    
    .highlight-row {
        animation: highlight 2s ease-in-out;
    }
    
    /* Scrollbar Styling */
    ::-webkit-scrollbar {
        width: 12px;
        height: 12px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #764ba2;
    }
    
    /* Chart Container - IMPROVED WITH BETTER MARGINS */
    .chart-container {
        background: white;
        padding: 25px;
        border-radius: 20px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        margin: 25px 0;
        animation: fadeInUp 0.6s ease-out;
    }
    
    /* Stats Box - DARK MODE FIX */
    .stats-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 8px 20px rgba(0,0,0,0.3);
        transition: transform 0.3s ease;
    }
    
    .stats-box:hover {
        transform: translateY(-5px);
    }
    
    .stats-box * {
        color: white !important;
    }
    
    .stats-number {
        font-size: 3.5em;
        font-weight: 800;
        margin: 15px 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        color: white !important;
    }
    
    .stats-label {
        font-size: 1.1em;
        opacity: 0.95;
        text-transform: uppercase;
        letter-spacing: 3px;
        font-weight: 600;
        color: white !important;
    }
    
    /* Divider - Enhanced */
    .divider {
        height: 4px;
        background: linear-gradient(90deg, transparent, #667eea, #764ba2, transparent);
        margin: 40px 0;
        border-radius: 2px;
        animation: dividerSlide 2s ease-in-out infinite;
    }
    
    @keyframes dividerSlide {
        0%, 100% { opacity: 0.5; }
        50% { opacity: 1; }
    }
    
    /* Info Box - DARK MODE FIX */
    .info-box {
        background: rgba(255, 255, 255, 0.98);
        padding: 25px;
        border-radius: 15px;
        border-left: 6px solid #667eea;
        margin: 20px 0;
        box-shadow: 0 5px 20px rgba(0,0,0,0.15);
        animation: fadeInUp 0.6s ease-out;
    }
    
    .info-box * {
        color: #333 !important;
    }
    
    /* Icon Container - Enhanced */
    .icon-container {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 60px;
        height: 60px;
        border-radius: 50%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
        font-size: 1.8em;
        margin-right: 20px;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        animation: iconRotate 3s ease-in-out infinite;
    }
    
    @keyframes iconRotate {
        0%, 100% { transform: rotate(0deg); }
        50% { transform: rotate(10deg); }
    }
    
    /* Data Quality Indicator */
    .quality-indicator {
        display: inline-block;
        width: 14px;
        height: 14px;
        border-radius: 50%;
        margin-right: 10px;
        animation: pulse 2s ease-in-out infinite;
        box-shadow: 0 0 10px rgba(0,0,0,0.3);
    }
    
    .quality-good { background-color: #27ae60; }
    .quality-warning { background-color: #f39c12; }
    .quality-danger { background-color: #e74c3c; }
    
    /* Rank Badge */
    .rank-badge {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 50px;
        height: 50px;
        border-radius: 50%;
        background: linear-gradient(135deg, #ffd700 0%, #ffed4e 100%);
        color: #333 !important;
        font-weight: 800;
        font-size: 1.2em;
        box-shadow: 0 5px 15px rgba(255, 215, 0, 0.4);
        animation: rankPulse 2s ease-in-out infinite;
    }
    
    @keyframes rankPulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.1); }
    }
    
    /* Vehicle Card - DARK MODE FIX */
    .vehicle-card {
        background: linear-gradient(135deg, #fff 0%, #f8f9fa 100%);
        padding: 20px;
        border-radius: 15px;
        margin: 15px 0;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        border-left: 5px solid #667eea;
    }
    
    .vehicle-card:hover {
        transform: translateX(10px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
    }
    
    .vehicle-card * {
        color: #333 !important;
    }
    
    /* Enhanced Number Animation */
    @keyframes countUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .animated-number {
        animation: countUp 1s ease-out;
    }
    
    /* Glassmorphism Effect - DARK MODE FIX */
    .glass-card {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 30px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        border: 1px solid rgba(255, 255, 255, 0.18);
    }
    
    .glass-card * {
        color: white !important;
    }
    
    /* Neon Glow Effect */
    .neon-text {
        color: #fff !important;
        text-shadow: 
            0 0 5px #667eea,
            0 0 10px #667eea,
            0 0 20px #667eea,
            0 0 40px #764ba2;
        animation: neonFlicker 2s ease-in-out infinite;
    }
    
    @keyframes neonFlicker {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.8; }
    }
    
    /* Data Table Row Hover */
    .dataframe tbody tr:hover {
        background-color: rgba(102, 126, 234, 0.1);
        transform: scale(1.01);
        transition: all 0.3s ease;
    }
    
    /* Chart Title Animation */
    @keyframes chartTitleSlide {
        from {
            opacity: 0;
            transform: translateX(-30px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    .chart-title {
        animation: chartTitleSlide 0.8s ease-out;
    }
    
    /* Floating Effect */
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    .floating {
        animation: float 3s ease-in-out infinite;
    }
    
    /* Shimmer Effect */
    @keyframes shimmer {
        0% { background-position: -1000px 0; }
        100% { background-position: 1000px 0; }
    }
    
    .shimmer {
        background: linear-gradient(to right, #f6f7f8 0%, #edeef1 20%, #f6f7f8 40%, #f6f7f8 100%);
        background-size: 1000px 100%;
        animation: shimmer 2s linear infinite;
    }
    
    /* Custom Alert with Icon */
    .custom-alert {
        display: flex;
        align-items: center;
        padding: 20px;
        border-radius: 15px;
        margin: 20px 0;
        animation: slideInRight 0.6s ease-out;
    }
    
    .custom-alert-icon {
        font-size: 2.5em;
        margin-right: 20px;
    }
    
    /* Enhanced Metric Grid */
    .metric-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 20px;
        margin: 30px 0;
    }
    
    /* Percentage Bar */
    .percentage-bar {
        height: 30px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        transition: width 1s ease-out;
        box-shadow: 0 3px 10px rgba(102, 126, 234, 0.3);
    }
    
    /* Status Indicator */
    .status-indicator {
        display: inline-block;
        width: 20px;
        height: 20px;
        border-radius: 50%;
        margin-right: 10px;
        animation: statusBlink 1.5s ease-in-out infinite;
    }
    
    @keyframes statusBlink {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.4; }
    }
    
    .status-active { background-color: #27ae60; }
    .status-inactive { background-color: #e74c3c; }
    .status-pending { background-color: #f39c12; }
    
    /* Skeleton Loader */
    .skeleton {
        background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
        background-size: 200% 100%;
        animation: loading 1.5s ease-in-out infinite;
        border-radius: 10px;
        height: 20px;
    }
    
    @keyframes loading {
        0% { background-position: 200% 0; }
        100% { background-position: -200% 0; }
    }
    
    /* Price Tag Effect */
    .price-tag {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
        padding: 10px 20px;
        border-radius: 8px;
        font-weight: 700;
        display: inline-block;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
        transform: rotate(-5deg);
        transition: transform 0.3s ease;
    }
    
    .price-tag:hover {
        transform: rotate(0deg) scale(1.1);
    }
    
    /* Info Card with Border Animation */
    .info-card-animated {
        position: relative;
        background: white;
        padding: 25px;
        border-radius: 15px;
        overflow: hidden;
    }
    
    .info-card-animated::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(102, 126, 234, 0.3), transparent);
        animation: borderSlide 3s linear infinite;
    }
    
    @keyframes borderSlide {
        0% { left: -100%; }
        100% { left: 100%; }
    }
    
    /* Streamlit Native Elements Dark Mode Fix */
    .stSelectbox label, .stMultiSelect label, .stRadio label {
        color: white !important;
    }
    
    /* File Uploader Dark Mode Fix */
    .stFileUploader label {
        color: white !important;
    }
    
    .stFileUploader div {
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# DATA LOADING AND PROCESSING
# ==========================================
@st.cache_data
def load_and_process_data(file_path=None):
    """Load and process vehicle maintenance data with error handling"""
    try:
        if file_path is None:
            file_path = 'Data_Kendaraan_Bersih.csv'
        
        # Try different encodings and separators
        try:
            df = pd.read_csv(file_path, sep=';')
        except Exception:
            try:
                df = pd.read_csv(file_path, sep=',')
            except Exception:
                df = pd.read_csv(file_path)
        
        # Clean column names
        df.columns = df.columns.str.strip()
        
        # Drop missing values in crucial columns
        df = df.dropna(subset=['Total Biaya', 'Nopol', 'Bulan', 'Tahun', 'Keterangan'])
        
        # Standardize text fields
        df['Bulan'] = df['Bulan'].str.strip().str.capitalize()
        df['Keterangan'] = df['Keterangan'].str.strip().str.upper()
        df['Nopol'] = df['Nopol'].str.strip().str.upper()
        
        # Handle Vendor_Clean column
        if 'Vendor_Clean' in df.columns:
            df['Vendor_Clean'] = df['Vendor_Clean'].fillna(df.get('Vendor', '')).str.strip().str.upper()
        elif 'Vendor' in df.columns:
            df['Vendor_Clean'] = df['Vendor'].str.strip().str.upper()
        else:
            df['Vendor_Clean'] = 'UNKNOWN'
        
        # Standardize month names
        df['Bulan'] = df['Bulan'].replace({'Nopember': 'November'})
        
        # Map month numbers for sorting
        month_map = {
            'Januari': 1, 'Februari': 2, 'Maret': 3, 'April': 4, 'Mei': 5, 'Juni': 6,
            'Juli': 7, 'Agustus': 8, 'September': 9, 'Oktober': 10, 'November': 11, 'Desember': 12
        }
        df['Month_Num'] = df['Bulan'].map(month_map)
        
        # Filter unrealistic costs
        df = df[df['Total Biaya'] >= 100000]
        
        # Ensure Tahun is integer
        df['Tahun'] = df['Tahun'].astype(int)
        
        # Type consistency per vehicle
        if 'Type' in df.columns:
            df['Type'] = df.groupby('Nopol')['Type'].transform(
                lambda x: x.mode()[0] if not x.mode().empty else "UNKNOWN"
            )
        else:
            df['Type'] = 'UNKNOWN'
        
        return df, None
    
    except FileNotFoundError:
        return None, "File tidak ditemukan. Silakan upload file CSV."
    except Exception as e:
        return None, f"Error saat memuat data: {str(e)}"

# ==========================================
# ANALYSIS FUNCTIONS
# ==========================================
def calculate_yearly_summary(df):
    """Calculate yearly financial summary"""
    summary = df.groupby('Tahun').agg({
        'Total Biaya': ['sum', 'mean', 'count']
    }).round(0)
    summary.columns = ['Total_Pengeluaran', 'Rata_Rata', 'Jumlah_Transaksi']
    return summary

def get_top_vendors(df, top_n=10):
    """Get top vendors by total cost"""
    return df.groupby('Vendor_Clean')['Total Biaya'].sum().sort_values(ascending=False).head(top_n)

def get_top_units(df, top_n=10):
    """Get most expensive units"""
    top_units = df.groupby(['Nopol', 'Type']).agg({
        'Total Biaya': 'sum',
        'Bulan': 'count'
    }).sort_values(by='Total Biaya', ascending=False).head(top_n)
    top_units.columns = ['Total_Biaya', 'Frekuensi_Servis']
    return top_units

def detect_cost_anomalies(df):
    """Detect cost anomalies using IQR method"""
    def get_upper_bound(group):
        q1 = group.quantile(0.25)
        q3 = group.quantile(0.75)
        iqr = q3 - q1
        return q3 + (1.5 * iqr)
    
    df_copy = df.copy()
    bounds = df_copy.groupby('Tahun')['Total Biaya'].apply(get_upper_bound).to_dict()
    df_copy['Batas_Wajar'] = df_copy['Tahun'].map(bounds)
    anomalies = df_copy[df_copy['Total Biaya'] > df_copy['Batas_Wajar']]
    return anomalies

def detect_logic_anomalies(df):
    """Detect logical inconsistencies in repair costs"""
    avg_berat = df[df['Keterangan'].str.contains('BERAT', na=False)]['Total Biaya'].mean()
    benchmark = avg_berat if not np.isnan(avg_berat) else df['Total Biaya'].quantile(0.9)
    
    logic_anomalies = df[
        (df['Keterangan'].str.contains('RINGAN', na=False)) & 
        (df['Total Biaya'] > benchmark)
    ]
    return logic_anomalies

def detect_duplicates(df):
    """Detect potential double billing"""
    duplicates = df[df.duplicated(
        subset=['Bulan', 'Tahun', 'Nopol', 'Total Biaya', 'Vendor_Clean'], 
        keep=False
    )]
    return duplicates

def calculate_monthly_trend(df):
    """Calculate monthly spending trend"""
    monthly = df.groupby(['Tahun', 'Month_Num', 'Bulan'])['Total Biaya'].sum().reset_index()
    monthly = monthly.sort_values(['Tahun', 'Month_Num'])
    return monthly

def calculate_category_distribution(df):
    """Calculate distribution by repair category"""
    return df.groupby('Keterangan')['Total Biaya'].agg(['sum', 'count']).sort_values('sum', ascending=False)

def calculate_vehicle_efficiency(df):
    """Calculate cost efficiency per vehicle"""
    efficiency = df.groupby(['Nopol', 'Type']).agg({
        'Total Biaya': ['sum', 'mean', 'count']
    })
    efficiency.columns = ['Total_Biaya', 'Rata_Rata', 'Frekuensi']
    efficiency['Cost_Per_Service'] = efficiency['Total_Biaya'] / efficiency['Frekuensi']
    return efficiency.sort_values('Total_Biaya', ascending=False)

def calculate_vendor_performance(df):
    """Calculate vendor performance metrics"""
    vendor_perf = df.groupby('Vendor_Clean').agg({
        'Total Biaya': ['sum', 'mean', 'count'],
        'Nopol': 'nunique'
    })
    vendor_perf.columns = ['Total_Biaya', 'Avg_Biaya', 'Transaksi', 'Jumlah_Kendaraan']
    return vendor_perf.sort_values('Total_Biaya', ascending=False)

def calculate_type_statistics(df):
    """Calculate statistics by vehicle type"""
    type_stats = df.groupby('Type').agg({
        'Total Biaya': ['sum', 'mean', 'count'],
        'Nopol': 'nunique'
    })
    type_stats.columns = ['Total_Biaya', 'Avg_Biaya', 'Transaksi', 'Jumlah_Unit']
    return type_stats.sort_values('Total_Biaya', ascending=False)

# ==========================================
# VISUALIZATION FUNCTIONS - IMPROVED WITH PROPER MARGINS
# ==========================================
def create_yearly_trend_chart(summary_df):
    """Create animated yearly trend chart with better margins - ALL TEXT VISIBLE"""
    if summary_df.empty:
        fig = go.Figure()
        fig.add_annotation(
            text="Tidak ada data untuk ditampilkan",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color='#333')
        )
        fig.update_layout(height=400, paper_bgcolor='white', plot_bgcolor='white')
        return fig
    
    fig = go.Figure()
    
    years = summary_df.index.tolist()
    costs = summary_df['Total_Pengeluaran'].tolist()
    
    # Add animated bar chart
    fig.add_trace(go.Bar(
        x=years,
        y=costs,
        marker=dict(
            color=costs,
            colorscale='Blues',
            showscale=False,
            line=dict(color='rgb(8,48,107)', width=2)
        ),
        text=[f'Rp {val:,.0f}' for val in costs],
        textposition='outside',
        textfont=dict(size=12, color='#333', family='Poppins', weight=600),
        hovertemplate='<b>Tahun %{x}</b><br>Total: Rp %{y:,.0f}<extra></extra>'
    ))
    
    # FIXED: Much better layout with proper margins - NO CUT OFF TEXT
    fig.update_layout(
        title=dict(
            text='Tren Pengeluaran Tahunan',
            font=dict(size=20, color='#333', family='Poppins', weight=700),
            x=0.5,
            xanchor='center'
        ),
        xaxis_title='Tahun',
        yaxis_title='Total Biaya (Rp)',
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(size=13, family='Poppins', color='#333'),
        height=500,
        showlegend=False,
        margin=dict(l=100, r=100, t=120, b=100),  # FIXED: Larger margins for all text
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            tickfont=dict(size=12, color='#333')
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(0,0,0,0.1)',
            zeroline=False,
            tickfont=dict(size=12, color='#333')
        )
    )
    
    return fig

def create_vendor_pie_chart(vendor_df):
    """Create vendor distribution pie chart with animation - ALL TEXT VISIBLE"""
    if vendor_df.empty or len(vendor_df) == 0:
        fig = go.Figure()
        fig.add_annotation(
            text="Tidak ada data vendor",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color='#333')
        )
        fig.update_layout(height=400, paper_bgcolor='white', plot_bgcolor='white')
        return fig
    
    # Prepare labels and values
    if len(vendor_df) > 8:
        labels = vendor_df.index[:8].tolist() + ['Others']
        values = vendor_df.values[:8].tolist() + [vendor_df.values[8:].sum()]
    else:
        labels = vendor_df.index.tolist()
        values = vendor_df.values.tolist()
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.4,
        marker=dict(
            colors=px.colors.qualitative.Set3,
            line=dict(color='white', width=3)
        ),
        textinfo='label+percent',
        textfont=dict(size=11, family='Poppins', color='#333'),
        hovertemplate='<b>%{label}</b><br>Rp %{value:,.0f}<br>%{percent}<extra></extra>',
        pull=[0.05 if i == 0 else 0 for i in range(len(labels))]
    )])
    
    fig.update_layout(
        title=dict(
            text='Distribusi Pengeluaran per Vendor',
            font=dict(size=20, color='#333', family='Poppins', weight=700),
            x=0.5,
            xanchor='center'
        ),
        height=500,
        paper_bgcolor='white',
        plot_bgcolor='white',
        showlegend=True,
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.02,
            font=dict(size=11, color='#333')
        ),
        margin=dict(l=20, r=200, t=100, b=20)  # FIXED: Even larger right margin for legend
    )
    
    return fig

def create_monthly_heatmap(df):
    """Create monthly cost heatmap with animation - ALL TEXT VISIBLE"""
    pivot_data = df.pivot_table(
        values='Total Biaya',
        index='Bulan',
        columns='Tahun',
        aggfunc='sum',
        fill_value=0
    )
    
    # Reorder months
    month_order = ['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni',
                   'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember']
    pivot_data = pivot_data.reindex([m for m in month_order if m in pivot_data.index])
    
    fig = go.Figure(data=go.Heatmap(
        z=pivot_data.values,
        x=pivot_data.columns,
        y=pivot_data.index,
        colorscale='RdYlGn_r',
        text=[[f'Rp {val:,.0f}' for val in row] for row in pivot_data.values],
        texttemplate='%{text}',
        textfont={"size": 10, "color": "#333"},
        hovertemplate='<b>%{y} %{x}</b><br>Total: Rp %{z:,.0f}<extra></extra>',
        colorbar=dict(title="Total Biaya (Rp)", titlefont=dict(color='#333'), tickfont=dict(color='#333'))
    ))
    
    fig.update_layout(
        title=dict(
            text='Heatmap Pengeluaran Bulanan',
            font=dict(size=20, color='#333', family='Poppins', weight=700),
            x=0.5,
            xanchor='center'
        ),
        xaxis_title='Tahun',
        yaxis_title='Bulan',
        height=600,
        paper_bgcolor='white',
        plot_bgcolor='white',
        font=dict(color='#333'),
        margin=dict(l=150, r=120, t=120, b=100),  # FIXED: Larger left margin for month names
        xaxis=dict(tickfont=dict(size=12, color='#333')),
        yaxis=dict(tickfont=dict(size=12, color='#333'))
    )
    
    return fig

def create_category_chart(category_df):
    """Create repair category distribution chart - ALL TEXT VISIBLE"""
    fig = go.Figure(data=[
        go.Bar(
            y=category_df.index,
            x=category_df['sum'],
            orientation='h',
            marker=dict(
                color=category_df['sum'],
                colorscale='Viridis',
                showscale=False,
                line=dict(color='white', width=1)
            ),
            text=[f'Rp {val:,.0f}' for val in category_df['sum']],
            textposition='outside',
            textfont=dict(size=11, color='#333', family='Poppins', weight=600),
            hovertemplate='<b>%{y}</b><br>Total: Rp %{x:,.0f}<br>Transaksi: %{customdata}<extra></extra>',
            customdata=category_df['count']
        )
    ])
    
    fig.update_layout(
        title=dict(
            text='Distribusi Biaya per Kategori Kerusakan',
            font=dict(size=20, color='#333', family='Poppins', weight=700),
            x=0.5,
            xanchor='center'
        ),
        xaxis_title='Total Biaya (Rp)',
        yaxis_title='Kategori',
        height=max(500, len(category_df) * 55),
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(color='#333'),
        margin=dict(l=250, r=150, t=120, b=100),  # FIXED: Much larger left margin for category names
        xaxis=dict(
            showgrid=True, 
            gridcolor='rgba(0,0,0,0.1)',
            tickfont=dict(size=12, color='#333')
        ),
        yaxis=dict(
            showgrid=False,
            tickfont=dict(size=11, color='#333')
        )
    )
    
    return fig

def create_scatter_plot(df):
    """Create scatter plot for cost vs frequency - ALL TEXT VISIBLE"""
    unit_stats = df.groupby('Nopol').agg({
        'Total Biaya': 'sum',
        'Bulan': 'count',
        'Type': 'first'
    }).reset_index()
    unit_stats.columns = ['Nopol', 'Total_Biaya', 'Frekuensi', 'Type']
    
    fig = px.scatter(
        unit_stats,
        x='Frekuensi',
        y='Total_Biaya',
        hover_data=['Nopol', 'Type'],
        color='Type',
        size='Total_Biaya',
        title='Analisis Frekuensi vs Total Biaya per Kendaraan',
        labels={'Frekuensi': 'Frekuensi Servis', 'Total_Biaya': 'Total Biaya (Rp)'},
        color_discrete_sequence=px.colors.qualitative.Vivid
    )
    
    fig.update_layout(
        height=600,
        font=dict(family='Poppins', color='#333'),
        title_font=dict(size=20, color='#333', weight=700),
        paper_bgcolor='white',
        plot_bgcolor='white',
        margin=dict(l=100, r=100, t=120, b=100),
        xaxis=dict(tickfont=dict(color='#333')),
        yaxis=dict(tickfont=dict(color='#333')),
        legend=dict(font=dict(color='#333'))
    )
    
    return fig

def create_timeline_chart(monthly_df):
    """Create timeline chart for monthly trends - ALL TEXT VISIBLE"""
    if monthly_df.empty:
        fig = go.Figure()
        fig.add_annotation(
            text="Tidak ada data bulanan",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color='#333')
        )
        fig.update_layout(height=400, paper_bgcolor='white', plot_bgcolor='white')
        return fig
    
    monthly_df = monthly_df.copy()
    monthly_df['Date'] = pd.to_datetime(
        monthly_df['Tahun'].astype(str) + '-' + monthly_df['Month_Num'].astype(str) + '-01'
    )
    
    fig = go.Figure()
    
    # Add line trace
    fig.add_trace(go.Scatter(
        x=monthly_df['Date'],
        y=monthly_df['Total Biaya'],
        mode='lines+markers',
        line=dict(color='#667eea', width=4),
        marker=dict(size=10, color='#764ba2', line=dict(color='white', width=2)),
        fill='tozeroy',
        fillcolor='rgba(102, 126, 234, 0.2)',
        hovertemplate='<b>%{x|%B %Y}</b><br>Total: Rp %{y:,.0f}<extra></extra>',
        name='Pengeluaran'
    ))
    
    fig.update_layout(
        title=dict(
            text='Timeline Pengeluaran Bulanan',
            font=dict(size=20, color='#333', family='Poppins', weight=700),
            x=0.5,
            xanchor='center'
        ),
        xaxis_title='Periode',
        yaxis_title='Total Biaya (Rp)',
        height=500,
        plot_bgcolor='white',
        paper_bgcolor='white',
        hovermode='x unified',
        font=dict(family='Poppins', color='#333'),
        margin=dict(l=100, r=100, t=120, b=100),
        xaxis=dict(
            showgrid=False,
            tickfont=dict(size=12, color='#333')
        ),
        yaxis=dict(
            showgrid=True, 
            gridcolor='rgba(0,0,0,0.1)',
            tickfont=dict(size=12, color='#333')
        )
    )
    
    return fig

def create_box_plot(df):
    """Create box plot for cost distribution - ALL TEXT VISIBLE"""
    fig = px.box(
        df,
        x='Tahun',
        y='Total Biaya',
        color='Tahun',
        title='Distribusi Biaya per Tahun (Box Plot)',
        labels={'Total Biaya': 'Biaya (Rp)', 'Tahun': 'Tahun'},
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    
    fig.update_layout(
        height=550,
        showlegend=False,
        font=dict(family='Poppins', color='#333'),
        title_font=dict(size=20, color='#333', weight=700),
        paper_bgcolor='white',
        plot_bgcolor='white',
        margin=dict(l=100, r=100, t=120, b=100),
        xaxis=dict(tickfont=dict(color='#333')),
        yaxis=dict(tickfont=dict(color='#333'))
    )
    
    return fig

def create_vendor_comparison_chart(vendor_df, top_n=10):
    """Create vendor comparison bar chart - ALL TEXT VISIBLE"""
    top_vendors = vendor_df.head(top_n)
    
    fig = go.Figure(data=[
        go.Bar(
            y=top_vendors.index,
            x=top_vendors.values,
            orientation='h',
            marker=dict(
                color=top_vendors.values,
                colorscale='Plasma',
                showscale=False,
                line=dict(color='white', width=2)
            ),
            text=[f'Rp {val:,.0f}' for val in top_vendors.values],
            textposition='outside',
            textfont=dict(size=11, color='#333', family='Poppins', weight=600),
            hovertemplate='<b>%{y}</b><br>Total: Rp %{x:,.0f}<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title=dict(
            text=f'Top {top_n} Vendor by Total Cost',
            font=dict(size=20, color='#333', family='Poppins', weight=700),
            x=0.5,
            xanchor='center'
        ),
        xaxis_title='Total Biaya (Rp)',
        yaxis_title='Vendor',
        height=max(550, top_n * 60),
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(color='#333'),
        margin=dict(l=350, r=180, t=120, b=100),  # FIXED: Much wider left margin for long vendor names
        xaxis=dict(
            showgrid=True, 
            gridcolor='rgba(0,0,0,0.1)',
            tickfont=dict(size=12, color='#333')
        ),
        yaxis=dict(
            showgrid=False,
            tickfont=dict(size=10, color='#333')
        )
    )
    
    return fig

def create_type_distribution_chart(type_stats):
    """Create vehicle type distribution pie chart - ALL TEXT VISIBLE"""
    fig = go.Figure(data=[go.Pie(
        labels=type_stats.index,
        values=type_stats['Total_Biaya'],
        hole=0.35,
        marker=dict(
            colors=px.colors.qualitative.Pastel,
            line=dict(color='white', width=3)
        ),
        textinfo='label+percent',
        textfont=dict(size=11, family='Poppins', color='#333'),
        hovertemplate='<b>%{label}</b><br>Total: Rp %{value:,.0f}<br>%{percent}<extra></extra>'
    )])
    
    fig.update_layout(
        title=dict(
            text='Distribusi Biaya per Tipe Kendaraan',
            font=dict(size=20, color='#333', family='Poppins', weight=700),
            x=0.5,
            xanchor='center'
        ),
        height=500,
        paper_bgcolor='white',
        plot_bgcolor='white',
        showlegend=True,
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.02,
            font=dict(size=11, color='#333')
        ),
        margin=dict(l=20, r=200, t=100, b=20)
    )
    
    return fig

def create_monthly_comparison_chart(df, years):
    """Create monthly comparison chart across years - ALL TEXT VISIBLE"""
    fig = go.Figure()
    
    colors = ['#667eea', '#764ba2', '#f093fb', '#4facfe']
    
    for idx, year in enumerate(years):
        year_data = df[df['Tahun'] == year]
        monthly_sum = year_data.groupby('Bulan')['Total Biaya'].sum()
        
        fig.add_trace(go.Bar(
            name=f'Tahun {year}',
            x=monthly_sum.index,
            y=monthly_sum.values,
            marker_color=colors[idx % len(colors)],
            text=[f'Rp {val:,.0f}' for val in monthly_sum.values],
            textposition='outside' if len(years) == 1 else 'auto',
            textfont=dict(size=10, color='#333'),
            hovertemplate='<b>%{x} %{fullData.name}</b><br>Total: Rp %{y:,.0f}<extra></extra>'
        ))
    
    fig.update_layout(
        title=dict(
            text='Perbandingan Pengeluaran Bulanan',
            font=dict(size=20, color='#333', family='Poppins', weight=700),
            x=0.5,
            xanchor='center'
        ),
        xaxis_title='Bulan',
        yaxis_title='Total Biaya (Rp)',
        barmode='group',
        height=550,
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family='Poppins', color='#333'),
        margin=dict(l=100, r=100, t=120, b=150),  # FIXED: More bottom margin for labels
        xaxis=dict(
            showgrid=False,
            tickfont=dict(size=11, color='#333'),
            tickangle=-45
        ),
        yaxis=dict(
            showgrid=True, 
            gridcolor='rgba(0,0,0,0.1)',
            tickfont=dict(size=12, color='#333')
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.35,
            xanchor="center",
            x=0.5,
            font=dict(color='#333')
        )
    )
    
    return fig

# ==========================================
# MAIN APPLICATION
# ==========================================
def main():
    # Load custom CSS
    load_custom_css()
    
    # Sidebar
    with st.sidebar:
        st.markdown("""
        <div style='text-align: center; padding: 20px;'>
            <h1 style='font-size: 3em; animation: float 3s ease-in-out infinite;'>🚗</h1>
            <h2 class='neon-text'>Dashboard Analisis</h2>
            <p style='font-size: 0.9em; opacity: 0.9; color: white;'>Pemeliharaan Kendaraan</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # File uploader
        st.subheader("📁 Upload Data")
        uploaded_file = st.file_uploader(
            "Upload file CSV",
            type=['csv'],
            help="Upload file data kendaraan dalam format CSV"
        )
        
        st.markdown("---")
        
        # Navigation
        st.subheader("🧭 Navigasi")
        page = st.radio(
            "Pilih Halaman:",
            ["Dashboard Utama", "Analisis Detail", "Deteksi Anomali", "Laporan Audit"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # Filter options
        st.subheader("🔍 Filter Data")
        
    # Load data
    if uploaded_file is not None:
        df, error = load_and_process_data(uploaded_file)
    else:
        df, error = load_and_process_data()
    
    # Error handling
    if error:
        st.error(f"❌ {error}")
        st.info("💡 Silakan upload file CSV yang valid atau pastikan file 'Data_Kendaraan_Bersih.csv' tersedia.")
        st.stop()
    
    if df is None or df.empty:
        st.warning("⚠️ Tidak ada data yang dimuat. Silakan upload file CSV.")
        st.stop()
    
    # Add filters to sidebar
    with st.sidebar:
        years = sorted(df['Tahun'].unique())
        selected_years = st.multiselect(
            "Tahun",
            options=years,
            default=years
        )
        
        if selected_years:
            df_filtered = df[df['Tahun'].isin(selected_years)]
        else:
            df_filtered = df
        
        # Additional filters
        vendors = ['Semua'] + sorted(df_filtered['Vendor_Clean'].unique().tolist())
        selected_vendor = st.selectbox("Vendor", vendors)
        
        if selected_vendor != 'Semua':
            df_filtered = df_filtered[df_filtered['Vendor_Clean'] == selected_vendor]
        
        st.markdown("---")
        
        # Data info with animation
        st.subheader("ℹ️ Info Data")
        st.markdown(f"""
        <div class='glass-card'>
            <div style='text-align: center;'>
                <div class='animated-number' style='font-size: 2em; font-weight: 800; color: white;'>{len(df_filtered):,}</div>
                <div style='color: rgba(255,255,255,0.9); margin-top: 5px;'>Total Transaksi</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class='glass-card' style='margin-top: 15px;'>
            <div style='text-align: center;'>
                <div class='animated-number' style='font-size: 2em; font-weight: 800; color: white;'>{df_filtered['Tahun'].min()}-{df_filtered['Tahun'].max()}</div>
                <div style='color: rgba(255,255,255,0.9); margin-top: 5px;'>Periode Data</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class='glass-card' style='margin-top: 15px;'>
            <div style='text-align: center;'>
                <div class='animated-number' style='font-size: 2em; font-weight: 800; color: white;'>{df_filtered['Nopol'].nunique()}</div>
                <div style='color: rgba(255,255,255,0.9); margin-top: 5px;'>Jumlah Kendaraan</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # ==========================================
    # PAGE: DASHBOARD UTAMA
    # ==========================================
    if page == "Dashboard Utama":
        # Header with animation
        st.markdown("""
        <div class="main-header floating">
            <h1>🚗 Dashboard Analisis Biaya Pemeliharaan Kendaraan</h1>
            <p>Monitoring dan Analisis Komprehensif</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Key metrics with IMPROVED animation
        st.markdown("<div class='section-header'>📊 Ringkasan Eksekutif</div>", unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        total_cost = df_filtered['Total Biaya'].sum()
        avg_cost = df_filtered['Total Biaya'].mean()
        total_transactions = len(df_filtered)
        total_vehicles = df_filtered['Nopol'].nunique()
        
        with col1:
            st.markdown(f"""
            <div class="metric-card slide-left">
                <div class="metric-label">💰 Total Pengeluaran</div>
                <div class="metric-value">{total_cost:,.0f}</div>
                <div style="font-size: 0.85em; color: #666; margin-top: 5px;">Rupiah</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card slide-left" style="animation-delay: 0.2s;">
                <div class="metric-label">📈 Rata-rata Biaya</div>
                <div class="metric-value">{avg_cost:,.0f}</div>
                <div style="font-size: 0.85em; color: #666; margin-top: 5px;">Per Transaksi</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card slide-right" style="animation-delay: 0.1s;">
                <div class="metric-label">📋 Total Transaksi</div>
                <div class="metric-value">{total_transactions:,}</div>
                <div style="font-size: 0.85em; color: #666; margin-top: 5px;">Transaksi</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="metric-card slide-right" style="animation-delay: 0.3s;">
                <div class="metric-label">🚗 Jumlah Kendaraan</div>
                <div class="metric-value">{total_vehicles}</div>
                <div style="font-size: 0.85em; color: #666; margin-top: 5px;">Unit</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        
        # Charts section with IMPROVED layout
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
            summary = calculate_yearly_summary(df_filtered)
            fig_yearly = create_yearly_trend_chart(summary)
            st.plotly_chart(fig_yearly, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
            vendors = get_top_vendors(df_filtered)
            fig_vendor = create_vendor_pie_chart(vendors)
            st.plotly_chart(fig_vendor, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Timeline chart
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        monthly_trend = calculate_monthly_trend(df_filtered)
        fig_timeline = create_timeline_chart(monthly_trend)
        st.plotly_chart(fig_timeline, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Monthly comparison if multiple years
        if len(selected_years) > 1:
            st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
            fig_monthly_comp = create_monthly_comparison_chart(df_filtered, selected_years)
            st.plotly_chart(fig_monthly_comp, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Top 10 units with enhanced design
        st.markdown("<div class='section-header'>🏆 10 Kendaraan Termahal</div>", unsafe_allow_html=True)
        
        top_units = get_top_units(df_filtered, 10)
        
        if not top_units.empty:
            for idx, ((nopol, vtype), row) in enumerate(top_units.iterrows(), 1):
                # Determine badge color
                if idx == 1:
                    badge_color = "linear-gradient(135deg, #ffd700 0%, #ffed4e 100%)"
                elif idx == 2:
                    badge_color = "linear-gradient(135deg, #c0c0c0 0%, #e8e8e8 100%)"
                elif idx == 3:
                    badge_color = "linear-gradient(135deg, #cd7f32 0%, #daa06d 100%)"
                else:
                    badge_color = "linear-gradient(135deg, #667eea 0%, #764ba2 100%)"
                
                st.markdown(f"""
                <div class="vehicle-card">
                    <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap;">
                        <div style="display: flex; align-items: center; flex: 1; min-width: 200px; margin: 10px;">
                            <div style="
                                width: 50px; 
                                height: 50px; 
                                border-radius: 50%; 
                                background: {badge_color}; 
                                display: flex; 
                                align-items: center; 
                                justify-content: center;
                                font-size: 1.5em;
                                font-weight: 800;
                                color: #333;
                                box-shadow: 0 5px 15px rgba(0,0,0,0.2);
                                margin-right: 20px;
                                flex-shrink: 0;
                            ">
                                #{idx}
                            </div>
                            <div style="flex: 1; min-width: 150px;">
                                <div style="font-size: 1.3em; font-weight: 700; color: #333;">{nopol}</div>
                                <div style="font-size: 0.9em; color: #666; margin-top: 3px;">{vtype}</div>
                            </div>
                        </div>
                        <div style="text-align: right; margin: 10px 30px;">
                            <div style="font-size: 0.85em; color: #666; text-transform: uppercase;">Total Biaya</div>
                            <div style="font-size: 1.5em; font-weight: 800; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                                Rp {row['Total_Biaya']:,.0f}
                            </div>
                        </div>
                        <div style="text-align: right; margin: 10px;">
                            <div style="font-size: 0.85em; color: #666; text-transform: uppercase;">Frekuensi</div>
                            <div style="font-size: 1.5em; font-weight: 800; color: #667eea;">
                                {int(row['Frekuensi_Servis'])}x
                            </div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Tidak ada data kendaraan untuk ditampilkan.")
    
    # ==========================================
    # PAGE: ANALISIS DETAIL
    # ==========================================
    elif page == "Analisis Detail":
        st.markdown("""
        <div class="main-header floating">
            <h1>📈 Analisis Detail</h1>
            <p>Eksplorasi Data Mendalam</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Tabs for different analyses
        tab1, tab2, tab3, tab4 = st.tabs([
            "📅 Analisis Temporal",
            "🏢 Analisis Vendor",
            "🚗 Analisis Kendaraan",
            "📊 Distribusi Biaya"
        ])
        
        with tab1:
            st.markdown("<div class='section-header'>Analisis Temporal</div>", unsafe_allow_html=True)
            
            # Heatmap
            st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
            fig_heatmap = create_monthly_heatmap(df_filtered)
            st.plotly_chart(fig_heatmap, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Yearly comparison
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
                fig_box = create_box_plot(df_filtered)
                st.plotly_chart(fig_box, use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)
            
            with col2:
                st.markdown("<div class='info-box'>", unsafe_allow_html=True)
                st.subheader("📊 Insight Temporal")
                
                monthly_data = calculate_monthly_trend(df_filtered)
                if not monthly_data.empty and len(monthly_data) > 0:
                    max_month = monthly_data.loc[monthly_data['Total Biaya'].idxmax()]
                    min_month = monthly_data.loc[monthly_data['Total Biaya'].idxmin()]
                    
                    st.markdown(f"""
                    <div style='padding: 15px; background: linear-gradient(135deg, #a1c4fd 0%, #c2e9fb 100%); border-radius: 10px; margin: 10px 0;'>
                        <div style='font-weight: 700; color: #333;'>🔝 Bulan Termahal</div>
                        <div style='font-size: 1.2em; color: #333; margin-top: 5px;'>{max_month['Bulan']} {int(max_month['Tahun'])}</div>
                        <div style='font-size: 1.5em; font-weight: 800; color: #667eea; margin-top: 5px;'>Rp {max_month['Total Biaya']:,.0f}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown(f"""
                    <div style='padding: 15px; background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%); border-radius: 10px; margin: 10px 0;'>
                        <div style='font-weight: 700; color: #333;'>📉 Bulan Termurah</div>
                        <div style='font-size: 1.2em; color: #333; margin-top: 5px;'>{min_month['Bulan']} {int(min_month['Tahun'])}</div>
                        <div style='font-size: 1.5em; font-weight: 800; color: #27ae60; margin-top: 5px;'>Rp {min_month['Total Biaya']:,.0f}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Calculate trend
                    yearly_sum = df_filtered.groupby('Tahun')['Total Biaya'].sum()
                    if len(yearly_sum) > 1:
                        trend = ((yearly_sum.iloc[-1] - yearly_sum.iloc[0]) / yearly_sum.iloc[0]) * 100
                        trend_icon = "📈" if trend > 0 else "📉"
                        trend_color = "#e74c3c" if trend > 0 else "#27ae60"
                        
                        st.markdown(f"""
                        <div style='padding: 15px; background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%); border-radius: 10px; margin: 10px 0;'>
                            <div style='font-weight: 700; color: #333;'>📊 Tren Tahunan</div>
                            <div style='font-size: 2em; font-weight: 800; color: {trend_color}; margin-top: 5px;'>{trend_icon} {abs(trend):.1f}%</div>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.info("Tidak cukup data untuk analisis temporal")
                
                st.markdown("</div>", unsafe_allow_html=True)
        
        with tab2:
            st.markdown("<div class='section-header'>Analisis Vendor</div>", unsafe_allow_html=True)
            
            vendors = get_top_vendors(df_filtered, 15)
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
                fig_vendor_bar = create_vendor_comparison_chart(vendors, 15)
                st.plotly_chart(fig_vendor_bar, use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)
            
            with col2:
                st.markdown("<div class='info-box'>", unsafe_allow_html=True)
                st.subheader("📊 Statistik Vendor")
                
                total_vendors = df_filtered['Vendor_Clean'].nunique()
                
                st.markdown(f"""
                <div class='stats-box' style='margin: 15px 0;'>
                    <div class='stats-label'>Total Vendor</div>
                    <div class='stats-number' style='font-size: 2.5em;'>{total_vendors}</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Vendor concentration
                top_3_pct = (vendors.head(3).sum() / vendors.sum()) * 100
                
                st.markdown(f"""
                <div class='stats-box' style='margin: 15px 0;'>
                    <div class='stats-label'>Konsentrasi Top 3</div>
                    <div class='stats-number' style='font-size: 2.5em;'>{top_3_pct:.1f}%</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Average per vendor
                avg_per_vendor = df_filtered.groupby('Vendor_Clean')['Total Biaya'].mean().mean()
                
                st.markdown(f"""
                <div class='stats-box' style='margin: 15px 0;'>
                    <div class='stats-label'>Rata-rata per Vendor</div>
                    <div class='stats-number' style='font-size: 1.8em;'>Rp {avg_per_vendor:,.0f}</div>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("</div>", unsafe_allow_html=True)
                
                # Top vendor detail
                st.markdown("<div class='info-box'>", unsafe_allow_html=True)
                st.subheader("🏆 Top 5 Vendor Detail")
                for idx, (vendor, cost) in enumerate(vendors.head(5).items(), 1):
                    pct = (cost / vendors.sum()) * 100
                    vendor_display = vendor[:40] + "..." if len(vendor) > 40 else vendor
                    st.markdown(f"**{idx}. {vendor_display}**")
                    st.progress(min(pct / 100, 1.0))
                    st.caption(f"Rp {cost:,.0f} ({pct:.1f}%)")
                    st.markdown("---")
                st.markdown("</div>", unsafe_allow_html=True)
        
        with tab3:
            st.markdown("<div class='section-header'>Analisis Kendaraan</div>", unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
                fig_scatter = create_scatter_plot(df_filtered)
                st.plotly_chart(fig_scatter, use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)
            
            with col2:
                st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
                type_stats = calculate_type_statistics(df_filtered)
                fig_type = create_type_distribution_chart(type_stats.head(10))
                st.plotly_chart(fig_type, use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)
            
            # Vehicle efficiency table
            st.markdown("<div class='section-header'>📊 Efisiensi Kendaraan</div>", unsafe_allow_html=True)
            
            efficiency = calculate_vehicle_efficiency(df_filtered).head(20)
            
            st.dataframe(
                efficiency.style.format({
                    'Total_Biaya': 'Rp {:,.0f}',
                    'Rata_Rata': 'Rp {:,.0f}',
                    'Frekuensi': '{:.0f}',
                    'Cost_Per_Service': 'Rp {:,.0f}'
                }).background_gradient(subset=['Total_Biaya'], cmap='Reds'),
                use_container_width=True,
                height=600
            )
        
        with tab4:
            st.markdown("<div class='section-header'>Distribusi Biaya</div>", unsafe_allow_html=True)
            
            # Category distribution
            category_dist = calculate_category_distribution(df_filtered)
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
                fig_category = create_category_chart(category_dist)
                st.plotly_chart(fig_category, use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)
            
            with col2:
                st.markdown("<div class='info-box'>", unsafe_allow_html=True)
                st.subheader("📋 Top 5 Kategori")
                
                for idx, (cat, row) in enumerate(category_dist.head(5).iterrows(), 1):
                    pct = (row['sum'] / category_dist['sum'].sum()) * 100
                    
                    st.markdown(f"""
                    <div style='padding: 12px; background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); border-radius: 10px; margin: 10px 0; border-left: 4px solid #667eea;'>
                        <div style='font-weight: 700; color: #333;'>{idx}. {cat}</div>
                        <div style='margin: 8px 0;'>
                            <div style='background: #e9ecef; height: 8px; border-radius: 4px; overflow: hidden;'>
                                <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); height: 100%; width: {pct}%; transition: width 1s ease;'></div>
                            </div>
                        </div>
                        <div style='display: flex; justify-content: space-between; font-size: 0.9em;'>
                            <span style='color: #666;'>{int(row['count'])}x transaksi</span>
                            <span style='font-weight: 700; color: #667eea;'>Rp {row['sum']:,.0f}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("</div>", unsafe_allow_html=True)
            
            # Cost distribution histogram
            st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
            fig_hist = px.histogram(
                df_filtered,
                x='Total Biaya',
                nbins=50,
                title='Distribusi Frekuensi Biaya',
                labels={'Total Biaya': 'Biaya (Rp)', 'count': 'Frekuensi'},
                color_discrete_sequence=['#667eea']
            )
            fig_hist.update_layout(
                height=500,
                font=dict(family='Poppins', color='#333'),
                title_font=dict(size=20, color='#333', weight=700),
                paper_bgcolor='white',
                plot_bgcolor='white',
                margin=dict(l=100, r=100, t=120, b=100),
                xaxis=dict(tickfont=dict(color='#333')),
                yaxis=dict(tickfont=dict(color='#333'))
            )
            st.plotly_chart(fig_hist, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
    
    # ==========================================
    # PAGE: DETEKSI ANOMALI
    # ==========================================
    elif page == "Deteksi Anomali":
        st.markdown("""
        <div class="main-header floating">
            <h1>🔍 Deteksi Anomali</h1>
            <p>Identifikasi Transaksi Mencurigakan</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Calculate anomalies
        with st.spinner('🔄 Menganalisis data untuk anomali...'):
            time.sleep(0.5)  # Simulate processing
            cost_anomalies = detect_cost_anomalies(df_filtered)
            logic_anomalies = detect_logic_anomalies(df_filtered)
            duplicates = detect_duplicates(df_filtered)
        
        # Summary cards with enhanced design
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class="alert-box alert-danger">
                <div style='text-align: center;'>
                    <div style='font-size: 3em;'>⚠️</div>
                    <h3 style='margin: 10px 0; color: white;'>Anomali Biaya</h3>
                    <div class="stats-number" style="font-size: 3em; color: white;">{len(cost_anomalies)}</div>
                    <p style='margin: 5px 0; color: white;'>Transaksi dengan biaya ekstrim</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="alert-box alert-warning">
                <div style='text-align: center;'>
                    <div style='font-size: 3em;'>🤔</div>
                    <h3 style='margin: 10px 0; color: #333;'>Anomali Logika</h3>
                    <div class="stats-number" style="font-size: 3em; color: #333;">{len(logic_anomalies)}</div>
                    <p style='margin: 5px 0; color: #333;'>Ketidaksesuaian kategori-biaya</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="alert-box alert-info">
                <div style='text-align: center;'>
                    <div style='font-size: 3em;'>📋</div>
                    <h3 style='margin: 10px 0; color: #333;'>Duplikasi</h3>
                    <div class="stats-number" style="font-size: 3em; color: #333;">{len(duplicates)}</div>
                    <p style='margin: 5px 0; color: #333;'>Potensi double billing</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        
        # Detailed anomaly sections
        tab1, tab2, tab3 = st.tabs([
            "⚠️ Anomali Biaya",
            "🤔 Anomali Logika",
            "📋 Duplikasi"
        ])
        
        with tab1:
            st.markdown("<div class='section-header'>Transaksi dengan Biaya Ekstrim (IQR Method)</div>", unsafe_allow_html=True)
            
            if not cost_anomalies.empty:
                st.markdown("<div class='custom-alert alert-danger'>", unsafe_allow_html=True)
                st.markdown(f"""
                <div style='display: flex; align-items: center;'>
                    <div class='custom-alert-icon'>⚠️</div>
                    <div>
                        <h3 style='margin: 0; color: white;'>Perhatian!</h3>
                        <p style='margin: 5px 0 0 0; color: white;'>Ditemukan {len(cost_anomalies)} transaksi dengan biaya di luar batas wajar!</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
                
                # Show statistics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown(f"""
                    <div class='stats-box'>
                        <div class='stats-label'>Total Anomali</div>
                        <div class='stats-number' style='font-size: 2em;'>Rp {cost_anomalies['Total Biaya'].sum():,.0f}</div>
                    </div>
                    """, unsafe_allow_html=True)
                with col2:
                    st.markdown(f"""
                    <div class='stats-box'>
                        <div class='stats-label'>Rata-rata Anomali</div>
                        <div class='stats-number' style='font-size: 2em;'>Rp {cost_anomalies['Total Biaya'].mean():,.0f}</div>
                    </div>
                    """, unsafe_allow_html=True)
                with col3:
                    st.markdown(f"""
                    <div class='stats-box'>
                        <div class='stats-label'>Max Anomali</div>
                        <div class='stats-number' style='font-size: 2em;'>Rp {cost_anomalies['Total Biaya'].max():,.0f}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Visualize anomalies
                st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
                fig_anom = px.scatter(
                    cost_anomalies.sort_values('Total Biaya', ascending=False).head(50),
                    x='Tahun',
                    y='Total Biaya',
                    color='Keterangan',
                    size='Total Biaya',
                    hover_data=['Nopol', 'Bulan', 'Vendor_Clean'],
                    title='Visualisasi Anomali Biaya (Top 50)',
                    color_discrete_sequence=px.colors.qualitative.Bold
                )
                fig_anom.add_hline(
                    y=cost_anomalies['Batas_Wajar'].mean(),
                    line_dash="dash",
                    line_color="red",
                    annotation_text="Batas Wajar Rata-rata",
                    annotation_position="top right",
                    annotation_font_color="#333"
                )
                fig_anom.update_layout(
                    height=600,
                    font=dict(family='Poppins', color='#333'),
                    title_font=dict(size=20, color='#333', weight=700),
                    paper_bgcolor='white',
                    plot_bgcolor='white',
                    margin=dict(l=100, r=100, t=120, b=100),
                    legend=dict(font=dict(color='#333')),
                    xaxis=dict(tickfont=dict(color='#333')),
                    yaxis=dict(tickfont=dict(color='#333'))
                )
                st.plotly_chart(fig_anom, use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)
                
                # Detailed table
                st.subheader("📋 Detail Transaksi Anomali")
                display_cols = ['Tahun', 'Bulan', 'Nopol', 'Type', 'Total Biaya', 'Batas_Wajar', 'Keterangan', 'Vendor_Clean']
                st.dataframe(
                    cost_anomalies[display_cols].sort_values('Total Biaya', ascending=False).head(20).style.format({
                        'Total Biaya': 'Rp {:,.0f}',
                        'Batas_Wajar': 'Rp {:,.0f}'
                    }).background_gradient(subset=['Total Biaya'], cmap='Reds'),
                    use_container_width=True,
                    height=400
                )
            else:
                st.markdown("<div class='alert-box alert-success'>", unsafe_allow_html=True)
                st.markdown("""
                <div style='text-align: center; padding: 20px;'>
                    <div style='font-size: 4em;'>✅</div>
                    <h3 style='color: #27ae60; margin: 15px 0;'>Tidak Ada Anomali</h3>
                    <p style='color: #333;'>Semua transaksi dalam batas wajar</p>
                </div>
                """, unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
        
        with tab2:
            st.markdown("<div class='section-header'>Ketidaksesuaian Kategori dan Biaya</div>", unsafe_allow_html=True)
            
            if not logic_anomalies.empty:
                st.markdown("<div class='custom-alert alert-warning'>", unsafe_allow_html=True)
                st.markdown(f"""
                <div style='display: flex; align-items: center;'>
                    <div class='custom-alert-icon'>⚠️</div>
                    <div>
                        <h3 style='margin: 0; color: #333;'>Peringatan Logika</h3>
                        <p style='margin: 5px 0 0 0; color: #333;'>Ditemukan {len(logic_anomalies)} transaksi dengan indikasi markup atau kesalahan input!</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
                
                st.info("💡 Transaksi berikut dikategorikan sebagai 'RINGAN' tetapi memiliki biaya melebihi rata-rata kerusakan 'BERAT'")
                
                # Statistics
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"""
                    <div class='stats-box'>
                        <div class='stats-label'>Total Nilai Anomali</div>
                        <div class='stats-number' style='font-size: 2.2em;'>Rp {logic_anomalies['Total Biaya'].sum():,.0f}</div>
                    </div>
                    """, unsafe_allow_html=True)
                with col2:
                    avg_heavy = df_filtered[df_filtered['Keterangan'].str.contains('BERAT', na=False)]['Total Biaya'].mean()
                    st.markdown(f"""
                    <div class='stats-box'>
                        <div class='stats-label'>Benchmark (Avg Berat)</div>
                        <div class='stats-number' style='font-size: 2.2em;'>Rp {avg_heavy:,.0f}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Detailed table
                st.subheader("📋 Detail Transaksi Anomali Logika")
                display_cols = ['Tahun', 'Bulan', 'Nopol', 'Type', 'Total Biaya', 'Keterangan', 'Vendor_Clean']
                st.dataframe(
                    logic_anomalies[display_cols].sort_values('Total Biaya', ascending=False).style.format({
                        'Total Biaya': 'Rp {:,.0f}'
                    }).background_gradient(subset=['Total Biaya'], cmap='YlOrRd'),
                    use_container_width=True,
                    height=400
                )
            else:
                st.markdown("<div class='alert-box alert-success'>", unsafe_allow_html=True)
                st.markdown("""
                <div style='text-align: center; padding: 20px;'>
                    <div style='font-size: 4em;'>✅</div>
                    <h3 style='color: #27ae60; margin: 15px 0;'>Logika Konsisten</h3>
                    <p style='color: #333;'>Tidak ditemukan ketidaksesuaian kategori dan biaya</p>
                </div>
                """, unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
        
        with tab3:
            st.markdown("<div class='section-header'>Potensi Double Billing</div>", unsafe_allow_html=True)
            
            if not duplicates.empty:
                st.markdown("<div class='custom-alert alert-info'>", unsafe_allow_html=True)
                st.markdown(f"""
                <div style='display: flex; align-items: center;'>
                    <div class='custom-alert-icon'>📋</div>
                    <div>
                        <h3 style='margin: 0; color: #333;'>Duplikasi Terdeteksi</h3>
                        <p style='margin: 5px 0 0 0; color: #333;'>Ditemukan {len(duplicates)} baris yang mencurigakan!</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
                
                st.info("💡 Transaksi berikut memiliki Nopol, Bulan, Tahun, Biaya, dan Vendor yang identik")
                
                # Group duplicates
                dup_groups = duplicates.groupby(['Nopol', 'Bulan', 'Tahun', 'Total Biaya', 'Vendor_Clean']).size().reset_index(name='Jumlah_Duplikat')
                dup_groups = dup_groups.sort_values('Jumlah_Duplikat', ascending=False)
                
                st.markdown(f"""
                <div class='stats-box' style='margin: 20px 0;'>
                    <div class='stats-label'>Total Grup Duplikasi</div>
                    <div class='stats-number' style='font-size: 3em;'>{len(dup_groups)}</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Show duplicate groups
                st.subheader("📊 Grup Transaksi Duplikat")
                st.dataframe(
                    dup_groups.style.format({'Total Biaya': 'Rp {:,.0f}'}),
                    use_container_width=True,
                    height=300
                )
                
                # Detailed view
                st.subheader("📋 Detail Transaksi Duplikat")
                display_cols = ['Tahun', 'Bulan', 'Nopol', 'Type', 'Total Biaya', 'Keterangan', 'Vendor_Clean']
                st.dataframe(
                    duplicates[display_cols].sort_values(['Nopol', 'Tahun', 'Bulan']).style.format({
                        'Total Biaya': 'Rp {:,.0f}'
                    }),
                    use_container_width=True,
                    height=400
                )
            else:
                st.markdown("<div class='alert-box alert-success'>", unsafe_allow_html=True)
                st.markdown("""
                <div style='text-align: center; padding: 20px;'>
                    <div style='font-size: 4em;'>✅</div>
                    <h3 style='color: #27ae60; margin: 15px 0;'>Data Bersih</h3>
                    <p style='color: #333;'>Tidak ditemukan duplikasi atau double billing</p>
                </div>
                """, unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
    
    # ==========================================
    # PAGE: LAPORAN AUDIT
    # ==========================================
    elif page == "Laporan Audit":
        st.markdown("""
        <div class="main-header floating">
            <h1>📋 Laporan Audit</h1>
            <p>Ringkasan Komprehensif untuk Stakeholder</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Generate report
        with st.spinner('📄 Menyusun laporan audit...'):
            time.sleep(0.5)
            # Calculate all necessary data
            summary = calculate_yearly_summary(df_filtered)
            vendors = get_top_vendors(df_filtered, 10)
            top_units = get_top_units(df_filtered, 10)
            cost_anomalies = detect_cost_anomalies(df_filtered)
            logic_anomalies = detect_logic_anomalies(df_filtered)
            duplicates = detect_duplicates(df_filtered)
            category_dist = calculate_category_distribution(df_filtered)
        
        # Executive Summary
        st.markdown("<div class='section-header'>📊 Ringkasan Eksekutif</div>", unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="stats-box">
                <div class="stats-label">Total Pengeluaran</div>
                <div class="stats-number" style="font-size: 2em;">Rp {df_filtered['Total Biaya'].sum():,.0f}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="stats-box">
                <div class="stats-label">Transaksi</div>
                <div class="stats-number" style="font-size: 2em;">{len(df_filtered):,}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="stats-box">
                <div class="stats-label">Kendaraan</div>
                <div class="stats-number" style="font-size: 2em;">{df_filtered['Nopol'].nunique()}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="stats-box">
                <div class="stats-label">Vendor</div>
                <div class="stats-number" style="font-size: 2em;">{df_filtered['Vendor_Clean'].nunique()}</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        
        # Yearly Trends
        st.markdown("<div class='section-header'>📈 Tren Tahunan</div>", unsafe_allow_html=True)
        
        st.markdown("<div class='info-box'>", unsafe_allow_html=True)
        for year, row in summary.iterrows():
            st.markdown(f"""
            <div style='display: flex; justify-content: space-between; align-items: center; padding: 15px; background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); border-radius: 10px; margin: 10px 0; border-left: 5px solid #667eea;'>
                <div>
                    <div style='font-size: 1.5em; font-weight: 800; color: #333;'>Tahun {int(year)}</div>
                    <div style='font-size: 0.9em; color: #666; margin-top: 5px;'>{int(row['Jumlah_Transaksi'])} transaksi</div>
                </div>
                <div style='text-align: right;'>
                    <div style='font-size: 0.85em; color: #666; text-transform: uppercase;'>Total Biaya</div>
                    <div style='font-size: 1.8em; font-weight: 800; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
                        Rp {row['Total_Pengeluaran']:,.0f}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Top Vendors
        st.markdown("<div class='section-header'>🏢 Top 10 Vendor</div>", unsafe_allow_html=True)
        
        vendor_data = []
        for idx, (vendor, cost) in enumerate(vendors.items(), 1):
            pct = (cost / vendors.sum()) * 100
            vendor_data.append({
                'Rank': f"#{idx}",
                'Vendor': vendor,
                'Total Biaya': f"Rp {cost:,.0f}",
                'Persentase': f"{pct:.1f}%"
            })
        
        st.table(pd.DataFrame(vendor_data))
        
        # Top Units
        st.markdown("<div class='section-header'>🚗 10 Kendaraan Termahal</div>", unsafe_allow_html=True)
        
        unit_data = []
        for idx, ((nopol, vtype), row) in enumerate(top_units.iterrows(), 1):
            unit_data.append({
                'Rank': f"#{idx}",
                'Nopol': nopol,
                'Type': vtype,
                'Total Biaya': f"Rp {row['Total_Biaya']:,.0f}",
                'Frekuensi': f"{int(row['Frekuensi_Servis'])}x"
            })
        
        st.table(pd.DataFrame(unit_data))
        
        # Audit Findings
        st.markdown("<div class='section-header'>🔍 Temuan Audit</div>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class="alert-box alert-danger">
                <div style='text-align: center;'>
                    <div style='font-size: 2.5em;'>⚠️</div>
                    <h4 style='margin: 10px 0; color: white;'>Anomali Biaya</h4>
                    <p style="font-size: 3em; font-weight: 800; margin: 10px 0; color: white;">{len(cost_anomalies)}</p>
                    <p style='color: white;'>transaksi ekstrim</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="alert-box alert-warning">
                <div style='text-align: center;'>
                    <div style='font-size: 2.5em;'>🤔</div>
                    <h4 style='margin: 10px 0; color: #333;'>Anomali Logika</h4>
                    <p style="font-size: 3em; font-weight: 800; margin: 10px 0; color: #333;">{len(logic_anomalies)}</p>
                    <p style='color: #333;'>ketidaksesuaian</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="alert-box alert-info">
                <div style='text-align: center;'>
                    <div style='font-size: 2.5em;'>📋</div>
                    <h4 style='margin: 10px 0; color: #333;'>Duplikasi</h4>
                    <p style="font-size: 3em; font-weight: 800; margin: 10px 0; color: #333;">{len(duplicates)}</p>
                    <p style='color: #333;'>potensi double billing</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Recommendations
        st.markdown("<div class='section-header'>💡 Rekomendasi</div>", unsafe_allow_html=True)
        
        recommendations = []
        
        if len(cost_anomalies) > 0:
            recommendations.append({
                'icon': '⚠️',
                'title': 'Review Transaksi Ekstrim',
                'desc': f'Terdapat {len(cost_anomalies)} transaksi dengan biaya di luar batas wajar. Perlu verifikasi dan investigasi lebih lanjut.',
                'priority': 'Tinggi'
            })
        
        if len(logic_anomalies) > 0:
            recommendations.append({
                'icon': '🔍',
                'title': 'Verifikasi Kategori Kerusakan',
                'desc': f'Ditemukan {len(logic_anomalies)} transaksi dengan ketidaksesuaian antara kategori dan biaya.',
                'priority': 'Sedang'
            })
        
        if len(duplicates) > 0:
            recommendations.append({
                'icon': '📋',
                'title': 'Cek Double Billing',
                'desc': f'{len(duplicates)} transaksi berpotensi duplikasi. Perlu cross-check dengan vendor.',
                'priority': 'Tinggi'
            })
        
        # Vendor concentration
        top_3_pct = (vendors.head(3).sum() / vendors.sum()) * 100
        if top_3_pct > 60:
            recommendations.append({
                'icon': '🏢',
                'title': 'Diversifikasi Vendor',
                'desc': f'Konsentrasi vendor terlalu tinggi ({top_3_pct:.1f}% pada 3 vendor teratas). Pertimbangkan diversifikasi.',
                'priority': 'Sedang'
            })
        
        # High maintenance vehicles
        if not top_units.empty:
            avg_cost = top_units['Total_Biaya'].mean()
            high_cost_units = top_units[top_units['Total_Biaya'] > avg_cost * 1.5]
            if not high_cost_units.empty:
                recommendations.append({
                    'icon': '🚗',
                    'title': 'Evaluasi Kendaraan Boros',
                    'desc': f'{len(high_cost_units)} kendaraan memiliki biaya pemeliharaan signifikan lebih tinggi. Pertimbangkan replacement.',
                    'priority': 'Sedang'
                })
        
        for rec in recommendations:
            priority_colors = {
                'Tinggi': 'alert-danger',
                'Sedang': 'alert-warning',
                'Rendah': 'alert-info'
            }
            alert_class = priority_colors.get(rec['priority'], 'alert-info')
            st.markdown(f"""
            <div class="alert-box {alert_class}">
                <div style='display: flex; align-items: flex-start;'>
                    <div style='font-size: 2.5em; margin-right: 20px;'>{rec['icon']}</div>
                    <div style='flex: 1;'>
                        <h4 style='margin: 0 0 10px 0;'>{rec['title']}</h4>
                        <p style='margin: 0 0 10px 0;'>{rec['desc']}</p>
                        <span class="badge badge-{rec['priority'].lower()}">{rec['priority']}</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Download report button
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        
        if st.button("📥 Download Laporan Excel", use_container_width=True):
            # Create Excel report
            with st.spinner('Menyiapkan file Excel...'):
                output_file = 'Laporan_Audit_Kendaraan.xlsx'
                
                with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
                    # Summary sheet
                    summary.to_excel(writer, sheet_name='Ringkasan Tahunan')
                    
                    # Vendors sheet
                    vendors.to_frame('Total Biaya').to_excel(writer, sheet_name='Top Vendors')
                    
                    # Units sheet
                    top_units.to_excel(writer, sheet_name='Kendaraan Termahal')
                    
                    # Anomalies sheets
                    if not cost_anomalies.empty:
                        cost_anomalies.to_excel(writer, sheet_name='Anomali Biaya', index=False)
                    
                    if not logic_anomalies.empty:
                        logic_anomalies.to_excel(writer, sheet_name='Anomali Logika', index=False)
                    
                    if not duplicates.empty:
                        duplicates.to_excel(writer, sheet_name='Duplikasi', index=False)
                
                st.success("✅ Laporan berhasil dibuat!")
                
                # Provide download link
                with open(output_file, 'rb') as f:
                    st.download_button(
                        label="⬇️ Download File Excel",
                        data=f,
                        file_name="Laporan_Audit_Kendaraan.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
    
    # Footer with animation - DARK MODE FIX
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div class="footer floating">
        <div style='font-size: 2em; margin-bottom: 15px;'>📊</div>
        <p style='font-size: 1.2em; font-weight: 700; margin: 10px 0; color: white;'>Dashboard Analisis Biaya Pemeliharaan Kendaraan</p>
        <p style="font-size: 0.95em; opacity: 0.9; margin: 5px 0; color: white;">Powered by Streamlit & Plotly</p>
        <p style="font-size: 0.85em; opacity: 0.8; color: white;">© 2025 - All Rights Reserved</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
