"""
NXID Enhanced Utilities Module 
===================================
Enhanced CSS, Logo, Renkler ve yardımcı fonksiyonlar - Smooth + Maturity + User Gains
"""

import streamlit as st
import os
import base64
from typing import Tuple

# Enhanced NXID Profesyonel Renkler 
NXID_COLORS = {
    'primary': '#1B8EF2',
    'secondary': '#3effc8', 
    'accent': '#7AC3FF',
    'dark': '#0B1426',
    'darker': '#050A14',
    'light': '#F8FAFC',
    'gray': '#64748B',
    'success': '#22c55e',
    'warning': '#f59e0b',
    'danger': '#ef4444',
    'purple': '#8B5CF6',
    'gold': '#F59E0B',
    'teal': '#14B8A6',
    'pink': '#EC4899',
    'indigo': '#6366F1',
    'orange': '#f97316',
    'emerald': '#10b981',
    'burn': '#ff4444',
    'tax': '#ff8800',
    
    # Enhanced  colors
    'bear': '#ef4444',
    'bull': '#22c55e',
    'base': '#1B8EF2',
    'presale': '#F59E0B',
    'mainnet': '#14B8A6',
    'maturity': '#8B5CF6',  # YENİ
    'smooth': '#7AC3FF',    # YENİ
    'user_gains': '#EC4899' # YENİ
}

def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    """Hex rengi RGB tuple'a dönüştür"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def display_nxid_logo(width: int = 120) -> str:
    """Enhanced NXID logosu göster """
    try:
        # Önce PNG dosyasını dene
        if os.path.exists("nxid-logo.png"):
            with open("nxid-logo.png", "rb") as f:
                img_data = base64.b64encode(f.read()).decode()
            return f'<img src="data:image/png;base64,{img_data}" width="{width}" height="{width}" alt="Enhanced NXID Logo " style="border-radius: 50%; box-shadow: 0 0 30px rgba(27, 142, 242, 0.5);">'
        
        # Sonra SVG dosyasını dene
        elif os.path.exists("NXID-logo.svg"):
            with open("NXID-logo.svg", "r", encoding="utf-8") as f:
                svg_content = f.read()
            svg_base64 = base64.b64encode(svg_content.encode('utf-8')).decode('utf-8')
            return f'<img src="data:image/svg+xml;base64,{svg_base64}" width="{width}" height="{width}" alt="Enhanced NXID Logo " style="border-radius: 50%; box-shadow: 0 0 30px rgba(27, 142, 242, 0.5);">'
        
        # Dosya yoksa Enhanced SVG fallback 
        else:
            svg_content = f'''
            <svg width="{width}" height="{width}" viewBox="0 0 120 120" fill="none" xmlns="http://www.w3.org/2000/svg">
                <defs>
                    <linearGradient id="enhancedNxidGradientV46" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" style="stop-color:#1B8EF2;stop-opacity:1" />
                        <stop offset="25%" style="stop-color:#7AC3FF;stop-opacity:1" />
                        <stop offset="50%" style="stop-color:#3effc8;stop-opacity:1" />
                        <stop offset="75%" style="stop-color:#14B8A6;stop-opacity:1" />
                        <stop offset="100%" style="stop-color:#8B5CF6;stop-opacity:0.8" />
                    </linearGradient>
                    <filter id="enhancedGlowV46">
                        <feGaussianBlur stdDeviation="5" result="coloredBlur"/>
                        <feMerge> 
                            <feMergeNode in="coloredBlur"/>
                            <feMergeNode in="SourceGraphic"/>
                        </feMerge>
                    </filter>
                    <pattern id="enhancedDots" patternUnits="userSpaceOnUse" width="8" height="8">
                        <circle cx="4" cy="4" r="1" fill="#3effc8" opacity="0.4"/>
                    </pattern>
                </defs>
                <circle cx="60" cy="60" r="55" fill="url(#enhancedNxidGradientV46)" stroke="#1B8EF2" stroke-width="3" filter="url(#enhancedGlowV46)"/>
                <circle cx="60" cy="60" r="45" fill="none" stroke="#3effc8" stroke-width="1" opacity="0.6"/>
                <circle cx="60" cy="60" r="35" fill="url(#enhancedDots)" opacity="0.4"/>
                <text x="60" y="68" font-family="Orbitron, monospace" font-size="18" font-weight="900" 
                      fill="#0B1426" text-anchor="middle" dominant-baseline="middle">NXID</text>
                <text x="60" y="85" font-family="Inter, sans-serif" font-size="8" font-weight="600" 
                      fill="#8B5CF6" text-anchor="middle" dominant-baseline="middle"></text>
            </svg>
            '''
            
            svg_base64 = base64.b64encode(svg_content.encode('utf-8')).decode('utf-8')
            return f'<img src="data:image/svg+xml;base64,{svg_base64}" width="{width}" height="{width}" alt="Enhanced NXID Logo " style="border-radius: 50%; box-shadow: 0 0 30px rgba(27, 142, 242, 0.5);">'
            
    except Exception as e:
        # Final CSS fallback 
        return f'''<div style="width: {width}px; height: {width}px; background: linear-gradient(135deg, #1B8EF2, #7AC3FF, #3effc8, #14B8A6, #8B5CF6); border-radius: 50%; display: flex; flex-direction: column; align-items: center; justify-content: center; box-shadow: 0 0 30px rgba(27, 142, 242, 0.5); border: 3px solid #1B8EF2;">
                      <span style="font-family: Orbitron, monospace; font-weight: 900; color: #0B1426; font-size: {width//5}px;">NXID</span>
                      <span style="font-family: Inter, sans-serif; font-weight: 600; color: #8B5CF6; font-size: {width//12}px;"></span>
                   </div>'''

def load_enhanced_css():
    """Enhanced NXID markalaması ile gelişmiş özel CSS yükle """
    primary_rgb = hex_to_rgb(NXID_COLORS['primary'])
    secondary_rgb = hex_to_rgb(NXID_COLORS['secondary'])
    presale_rgb = hex_to_rgb(NXID_COLORS['presale'])
    mainnet_rgb = hex_to_rgb(NXID_COLORS['mainnet'])
    maturity_rgb = hex_to_rgb(NXID_COLORS['maturity'])
    
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Orbitron:wght@400;500;600;700;900&display=swap');
    
    .stApp {{
        background: linear-gradient(135deg, {NXID_COLORS['darker']} 0%, {NXID_COLORS['dark']} 40%, #1e293b 100%);
        font-family: 'Inter', sans-serif;
    }}
    
    h1 {{
        text-align: center !important;
        font-family: 'Orbitron', monospace !important;
        font-size: 3.5rem !important;
        font-weight: 900 !important;
        background: linear-gradient(135deg, {NXID_COLORS['primary']}, {NXID_COLORS['secondary']}, {NXID_COLORS['maturity']}) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
        margin-bottom: 1rem !important;
        text-shadow: 0 0 30px rgba({primary_rgb[0]}, {primary_rgb[1]}, {primary_rgb[2]}, 0.5) !important;
    }}
    
    h2 {{
        font-family: 'Orbitron', monospace !important;
        background: linear-gradient(90deg, {NXID_COLORS['primary']}, {NXID_COLORS['maturity']}) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
    }}
    
    .metric-card {{
        background: linear-gradient(145deg, 
            rgba({primary_rgb[0]}, {primary_rgb[1]}, {primary_rgb[2]}, 0.18), 
            rgba({secondary_rgb[0]}, {secondary_rgb[1]}, {secondary_rgb[2]}, 0.12));
        border: 2px solid rgba({primary_rgb[0]}, {primary_rgb[1]}, {primary_rgb[2]}, 0.4);
        border-radius: 20px;
        padding: 1.8rem;
        margin: 0.8rem 0;
        backdrop-filter: blur(20px);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.5);
        transition: all 0.4s ease;
        position: relative;
        overflow: hidden;
    }}
    
    .metric-card::before {{
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba({primary_rgb[0]}, {primary_rgb[1]}, {primary_rgb[2]}, 0.1), transparent);
        transition: left 0.5s;
    }}
    
    .metric-card:hover::before {{
        left: 100%;
    }}
    
    .metric-card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 20px 60px rgba({primary_rgb[0]}, {primary_rgb[1]}, {primary_rgb[2]}, 0.3);
        border-color: {NXID_COLORS['maturity']};
    }}
    
    /* Enhanced : Phase indicators */
    .phase-presale {{
        border-left: 5px solid {NXID_COLORS['presale']} !important;
        background: linear-gradient(145deg, 
            rgba({presale_rgb[0]}, {presale_rgb[1]}, {presale_rgb[2]}, 0.1), 
            rgba({primary_rgb[0]}, {primary_rgb[1]}, {primary_rgb[2]}, 0.05)) !important;
    }}
    
    .phase-mainnet {{
        border-left: 5px solid {NXID_COLORS['mainnet']} !important;
        background: linear-gradient(145deg, 
            rgba({mainnet_rgb[0]}, {mainnet_rgb[1]}, {mainnet_rgb[2]}, 0.1), 
            rgba({primary_rgb[0]}, {primary_rgb[1]}, {primary_rgb[2]}, 0.05)) !important;
    }}
    
    .phase-maturity {{
        border-left: 5px solid {NXID_COLORS['maturity']} !important;
        background: linear-gradient(145deg, 
            rgba({maturity_rgb[0]}, {maturity_rgb[1]}, {maturity_rgb[2]}, 0.1), 
            rgba({primary_rgb[0]}, {primary_rgb[1]}, {primary_rgb[2]}, 0.05)) !important;
    }}
    
    /* Enhanced scenario colors */
    .scenario-bear {{
        border-color: {NXID_COLORS['bear']} !important;
        color: {NXID_COLORS['bear']} !important;
    }}
    
    .scenario-bull {{
        border-color: {NXID_COLORS['bull']} !important;
        color: {NXID_COLORS['bull']} !important;
    }}
    
    .scenario-base {{
        border-color: {NXID_COLORS['base']} !important;
        color: {NXID_COLORS['base']} !important;
    }}
    
    .enhanced-smooth {{
        border-color: {NXID_COLORS['smooth']} !important;
        color: {NXID_COLORS['smooth']} !important;
    }}
    
    .stSidebar {{
        background: linear-gradient(180deg, rgba({primary_rgb[0]}, {primary_rgb[1]}, {primary_rgb[2]}, 0.1), rgba({maturity_rgb[0]}, {maturity_rgb[1]}, {maturity_rgb[2]}, 0.1));
        border-right: 2px solid rgba({primary_rgb[0]}, {primary_rgb[1]}, {primary_rgb[2]}, 0.3);
    }}
    
    .stButton > button {{
        background: linear-gradient(135deg, {NXID_COLORS['primary']}, {NXID_COLORS['maturity']});
        color: {NXID_COLORS['darker']};
        border: none;
        border-radius: 15px;
        font-weight: 700;
        font-family: 'Orbitron', monospace;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: all 0.3s ease;
        box-shadow: 0 8px 25px rgba({primary_rgb[0]}, {primary_rgb[1]}, {primary_rgb[2]}, 0.4);
    }}
    
    .stButton > button:hover {{
        transform: translateY(-3px);
        box-shadow: 0 12px 35px rgba({maturity_rgb[0]}, {maturity_rgb[1]}, {maturity_rgb[2]}, 0.6);
        background: linear-gradient(135deg, {NXID_COLORS['maturity']}, {NXID_COLORS['secondary']});
    }}
    
    /* Enhanced  styling */
    .stSelectbox > div > div {{
        background: rgba({primary_rgb[0]}, {primary_rgb[1]}, {primary_rgb[2]}, 0.1);
        border: 1px solid rgba({maturity_rgb[0]}, {maturity_rgb[1]}, {maturity_rgb[2]}, 0.3);
        border-radius: 10px;
    }}
    
    .stNumberInput > div > div > input {{
        background: rgba({primary_rgb[0]}, {primary_rgb[1]}, {primary_rgb[2]}, 0.05);
        border: 1px solid rgba({maturity_rgb[0]}, {maturity_rgb[1]}, {maturity_rgb[2]}, 0.2);
        border-radius: 8px;
        color: {NXID_COLORS['light']};
    }}
    
    .stSlider > div > div > div > div {{
        background: linear-gradient(90deg, {NXID_COLORS['primary']}, {NXID_COLORS['maturity']});
    }}
    
    /* Streamlit markasını gizle */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    .stDeployButton {{visibility: hidden;}}
    .stDecoration {{visibility: hidden;}}
    
    .stTabs [data-baseweb="tab-list"] {{
        gap: 24px;
        background: rgba({primary_rgb[0]}, {primary_rgb[1]}, {primary_rgb[2]}, 0.1);
        border-radius: 15px;
        padding: 10px;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        height: 50px;
        background: rgba({primary_rgb[0]}, {primary_rgb[1]}, {primary_rgb[2]}, 0.2);
        border-radius: 10px;
        color: {NXID_COLORS['light']};
        font-weight: 600;
        border: 2px solid transparent;
        transition: all 0.3s ease;
    }}
    
    .stTabs [aria-selected="true"] {{
        background: linear-gradient(135deg, {NXID_COLORS['primary']}, {NXID_COLORS['maturity']});
        color: {NXID_COLORS['darker']};
        border-color: {NXID_COLORS['accent']};
    }}
    
    /* Enhanced expander styling */
    .streamlit-expanderHeader {{
        background: rgba({primary_rgb[0]}, {primary_rgb[1]}, {primary_rgb[2]}, 0.1);
        border-radius: 10px;
        border: 1px solid rgba({maturity_rgb[0]}, {maturity_rgb[1]}, {maturity_rgb[2]}, 0.3);
    }}
    
    /* Enhanced progress bar styling */
    .stProgress > div > div > div > div {{
        background: linear-gradient(90deg, {NXID_COLORS['primary']}, {NXID_COLORS['maturity']});
    }}
    
    /* Enhanced checkbox styling */
    .stCheckbox > label > div {{
        background: rgba({primary_rgb[0]}, {primary_rgb[1]}, {primary_rgb[2]}, 0.1);
        border: 1px solid rgba({maturity_rgb[0]}, {maturity_rgb[1]}, {maturity_rgb[2]}, 0.3);
    }}
    
    /* Enhanced version badge */
    .version-badge {{
        position: fixed;
        bottom: 20px;
        right: 20px;
        background: linear-gradient(135deg, {NXID_COLORS['primary']}, {NXID_COLORS['maturity']});
        color: {NXID_COLORS['darker']};
        padding: 8px 16px;
        border-radius: 20px;
        font-family: 'Orbitron', monospace;
        font-weight: 600;
        font-size: 12px;
        z-index: 1000;
        box-shadow: 0 4px 15px rgba({maturity_rgb[0]}, {maturity_rgb[1]}, {maturity_rgb[2]}, 0.4);
    }}
    
    /* Enhanced smooth indicators */
    .smooth-indicator {{
        background: linear-gradient(90deg, {NXID_COLORS['smooth']}, {NXID_COLORS['teal']});
        border-radius: 10px;
        padding: 5px 10px;
        color: {NXID_COLORS['darker']};
        font-weight: 600;
        display: inline-block;
        margin: 2px;
    }}
    
    /* Enhanced maturity indicators */
    .maturity-indicator {{
        background: linear-gradient(90deg, {NXID_COLORS['maturity']}, {NXID_COLORS['purple']});
        border-radius: 10px;
        padding: 5px 10px;
        color: {NXID_COLORS['light']};
        font-weight: 600;
        display: inline-block;
        margin: 2px;
    }}
    </style>
    """, unsafe_allow_html=True)

def format_number(num: float, unit: str = "") -> str:
    """Enhanced sayıları düzgün formatlı şekilde göster """
    if num >= 1e9:
        return f"{num/1e9:.1f}B {unit}".strip()
    elif num >= 1e6:
        return f"{num/1e6:.1f}M {unit}".strip()
    elif num >= 1e3:
        return f"{num/1e3:.1f}K {unit}".strip()
    else:
        return f"{num:.2f} {unit}".strip()

def create_metric_card(title: str, value: str, subtitle: str = "", color: str = None, phase: str = "") -> str:
    """Enhanced Metric card HTML oluştur """
    if color is None:
        color = NXID_COLORS['primary']
    
    phase_class = ""
    if phase == "presale":
        phase_class = "phase-presale"
    elif phase == "mainnet":
        phase_class = "phase-mainnet"
    elif phase == "maturity":
        phase_class = "phase-maturity"
    
    return f"""
    <div class="metric-card {phase_class}">
        <h4 style="color: {color}; margin: 0; font-size: 0.9rem; font-family: 'Orbitron', monospace;">{title}</h4>
        <p style="font-size: 1.4rem; margin: 0.5rem 0 0 0; color: {color}; font-weight: 800; font-family: 'Inter', sans-serif;">
            {value}
        </p>
        <small style="color: {NXID_COLORS['gray']}; font-family: 'Inter', sans-serif;">{subtitle}</small>
    </div>
    """

def create_scenario_badge(scenario: str) -> str:
    """Enhanced Senaryo badge'i oluştur """
    scenario_colors = {
        'bear': NXID_COLORS['bear'],
        'bull': NXID_COLORS['bull'],
        'base': NXID_COLORS['base'],
        'smooth': NXID_COLORS['smooth'],
        'maturity': NXID_COLORS['maturity']
    }
    
    scenario_emojis = {
        'bear': '🐻',
        'bull': '🐂', 
        'base': '📊',
        'smooth': '🌊',
        'maturity': '🎯'
    }
    
    color = scenario_colors.get(scenario, NXID_COLORS['primary'])
    emoji = scenario_emojis.get(scenario, '📊')
    
    return f"""
    <span style="background: {color}; color: white; padding: 4px 12px; border-radius: 15px; 
                 font-family: 'Orbitron', monospace; font-weight: 600; font-size: 0.9rem;">
        {emoji} {scenario.upper()}
    </span>
    """

def get_chart_template() -> dict:
    """Enhanced Plotly chart'lar için standart template """
    return {
        'paper_bgcolor': 'rgba(0,0,0,0)',
        'plot_bgcolor': f"rgba{hex_to_rgb(NXID_COLORS['dark']) + (0.4,)}",
        'font': {'color': NXID_COLORS['light'], 'family': 'Inter', 'size': 11},
        'xaxis': {
            'gridcolor': f"rgba{hex_to_rgb(NXID_COLORS['primary']) + (0.15,)}", 
            'linecolor': NXID_COLORS['maturity'],
            'tickfont': {'size': 10, 'family': 'Inter'},
            'title': {'font': {'size': 12, 'family': 'Orbitron'}}
        },
        'yaxis': {
            'gridcolor': f"rgba{hex_to_rgb(NXID_COLORS['primary']) + (0.15,)}", 
            'linecolor': NXID_COLORS['maturity'],
            'tickfont': {'size': 10, 'family': 'Inter'},
            'title': {'font': {'size': 12, 'family': 'Orbitron'}}
        },
        'legend': {
            'font': {'family': 'Inter', 'size': 10, 'color': NXID_COLORS['light']},
            'bgcolor': f"rgba{hex_to_rgb(NXID_COLORS['dark']) + (0.8,)}",
            'bordercolor': NXID_COLORS['maturity'],
            'borderwidth': 1
        }
    }

def display_header():
    """Enhanced Ana sayfa başlığını göster """
    nxid_logo = display_nxid_logo(120)
    st.markdown(f'''
    <div style="text-align: center; margin-bottom: 3rem;">
        <div style="margin: 0 auto 1.5rem auto;">
            {nxid_logo}
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    st.markdown(f'''
    <h1 style="text-align: center; font-family: Orbitron, monospace; font-size: 3.5rem; font-weight: 900; 
               background: linear-gradient(135deg, {NXID_COLORS['primary']}, {NXID_COLORS['secondary']}, {NXID_COLORS['maturity']}); 
               -webkit-background-clip: text; -webkit-text-fill-color: transparent; 
               margin-bottom: 1rem;">ENHANCED NXID TOKENOMICS </h1>
    ''', unsafe_allow_html=True)
    
    st.markdown(f'''
    <div style="text-align: center; margin: 1.5rem 0; padding: 1rem; 
                background: rgba({hex_to_rgb(NXID_COLORS['primary'])[0]}, {hex_to_rgb(NXID_COLORS['primary'])[1]}, {hex_to_rgb(NXID_COLORS['primary'])[2]}, 0.1); 
                border-radius: 15px; border: 1px solid rgba({hex_to_rgb(NXID_COLORS['maturity'])[0]}, {hex_to_rgb(NXID_COLORS['maturity'])[1]}, {hex_to_rgb(NXID_COLORS['maturity'])[2]}, 0.3);">
        <p style="color: {NXID_COLORS['light']}; font-family: Inter; margin: 0; font-size: 1.1rem; font-weight: 500;">
            <strong style="color: {NXID_COLORS['secondary']};">Enhanced Next Digital ID (NXID)</strong> • 
            <span style="color: {NXID_COLORS['accent']};">BNB Chain (BEP-20)</span> • 
            <strong style="color: {NXID_COLORS['gold']};">100B Toplam Arz</strong>
        </p>
        <p style="color: {NXID_COLORS['gray']}; font-family: Inter; margin: 0.5rem 0 0 0; font-size: 1rem;">
            <span style="color: {NXID_COLORS['presale']};"> Simple Faiz Presale</span> + 
            <span style="color: {NXID_COLORS['smooth']};"> Smooth Mainnet</span> + 
            <span style="color: {NXID_COLORS['maturity']};"> Maturity Target</span> + 
            <span style="color: {NXID_COLORS['user_gains']};"> User Gains</span>
        </p>
        <p style="color: {NXID_COLORS['gray']}; font-family: Inter; margin: 0.5rem 0 0 0; font-size: 0.9rem;">
            <span style="color: {NXID_COLORS['bear']};">🐻 Bear</span> / 
            <span style="color: {NXID_COLORS['base']};">📊 Base</span> / 
            <span style="color: {NXID_COLORS['bull']};">🐂 Bull</span> Enhanced Scenarios
        </p>
    </div>
    ''', unsafe_allow_html=True)
    
    st.markdown(f'''
    <p style="text-align: center; color: {NXID_COLORS['gray']}; font-size: 1.3rem; 
               font-family: Inter; margin-bottom: 2rem; font-weight: 500;">
        Enhanced Demand Model • Smooth Price Model • Maturity McAp Target • Average User ROI • 
    </p>
    <div style="width: 100%; height: 3px; background: linear-gradient(90deg, {NXID_COLORS['primary']}, {NXID_COLORS['secondary']}, {NXID_COLORS['maturity']}); 
                margin: 2rem auto; border-radius: 2px;"></div>
    ''', unsafe_allow_html=True)
    
    # Enhanced version badge
    st.markdown(f'''
    <div class="version-badge">
        Enhanced NXID 
    </div>
    ''', unsafe_allow_html=True)

def get_phase_color(phase: str) -> str:
    """Enhanced Phase rengini al """
    phase_colors = {
        'presale': NXID_COLORS['presale'],
        'mainnet': NXID_COLORS['mainnet'],
        'vesting': NXID_COLORS['purple'],
        'overall': NXID_COLORS['primary'],
        'maturity': NXID_COLORS['maturity'],
        'smooth': NXID_COLORS['smooth'],
        'user_gains': NXID_COLORS['user_gains']
    }
    return phase_colors.get(phase, NXID_COLORS['primary'])

def format_currency(amount: float, currency: str = "USDT") -> str:
    """Enhanced Para birimini formatla """
    if currency == "USDT" or currency == "$":
        if amount >= 1e9:
            return f"${amount/1e9:.1f}B"
        elif amount >= 1e6:
            return f"${amount/1e6:.1f}M"
        elif amount >= 1e3:
            return f"${amount/1e3:.1f}K"
        else:
            return f"${amount:.2f}"
    else:
        return format_number(amount, currency)

def format_percentage(value: float, decimal_places: int = 1) -> str:
    """Enhanced Yüzde formatla """
    return f"{value:.{decimal_places}f}%"

def format_multiplier(value: float, decimal_places: int = 1) -> str:
    """Enhanced Çarpan formatla """
    return f"{value:.{decimal_places}f}x"

def create_smooth_indicator(value: str, label: str = "Smooth") -> str:
    """Enhanced Smooth indicator oluştur """
    return f'<span class="smooth-indicator">{label}: {value}</span>'

def create_maturity_indicator(value: str, label: str = "Maturity") -> str:
    """Enhanced Maturity indicator oluştur """
    return f'<span class="maturity-indicator">{label}: {value}</span>'

def get_enhanced_colors() -> dict:
    """Enhanced renk paletini döndür """
    return NXID_COLORS

def calculate_user_roi_summary(investment: float, peak_value: float, final_value: float) -> dict:
    """Enhanced Kullanıcı ROI özetini hesapla """
    peak_roi = peak_value / investment if investment > 0 else 0
    final_roi = final_value / investment if investment > 0 else 0
    sustain_rate = final_roi / peak_roi if peak_roi > 0 else 0
    
    return {
        'investment': investment,
        'peak_value': peak_value,
        'final_value': final_value,
        'peak_roi': peak_roi,
        'final_roi': final_roi,
        'sustain_rate': sustain_rate,
        'gain_peak': peak_value - investment,
        'gain_final': final_value - investment
    }