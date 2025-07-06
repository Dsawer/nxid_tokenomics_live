#main.py
"""
NXID Enhanced Tokenomics  - MAIN APPLICATION
===============================================
Enhanced: Simple Faiz + Smooth Mainnet + Maturity McAp + Average User Gains

YENİ ÖZELLİKLER :
- Simple Faiz Sistemi (Compounding YOK) ✅
- Smooth Mainnet Model (Volatility damping, price smoothing) ✅  
- Maturity McAp Target System ✅
- Average User Gains Analysis ($1000 yatırımcı) ✅
- Enhanced Staking Pool Vesting ✅
- Logo in Pie Chart ✅
- Circulating Supply Burn Effect ✅
- 16 Çeyrek Smooth Scenarios ✅
"""

import streamlit as st
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

# Enhanced modülleri import et
from config import EnhancedNXIDConfig
from models import EnhancedTokenomicsModel
from visualizations import EnhancedVisualizationManager
from sidebar import SidebarManager
from analytics import AnalyticsManager
from utils import load_enhanced_css, display_header

# Enhanced sayfa yapılandırması
st.set_page_config(
    page_title="NXID Enhanced Tokenomics ",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    """🎯 Enhanced Ana uygulama fonksiyonu """
    
    # Enhanced CSS ve header yükle
    load_enhanced_css()
    display_header()
    
    # Enhanced Sidebar yöneticisini başlat
    sidebar_manager = SidebarManager()
    config, config_valid = sidebar_manager.render_sidebar()
    
    # === ENHANCED SİMÜLASYON YÜRÜTME ===
    st.markdown("## 🎯 Enhanced Scenario Selection and Analysis ")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        scenario = st.selectbox("Enhanced Mainnet Scenario", 
                               ["base", "bear", "bull"], 
                               index=0,
                               help="Bear: Downtrend, Base: Normal, Bull: Uptrend (Enhanced Advanced Model)")
    
    with col2:
        st.markdown("### 🚀 Enhanced Scenario Information")
        if scenario == "bear":
            st.error("🐻 Enhanced Bear: Advanced damping + smooth downtrend")
        elif scenario == "bull":
            st.success("🐂 Enhanced Bull: Advanced acceleration + smooth uptrend")
        else:
            st.info("📊 Enhanced Base: Balanced growth + advanced maturity")
    
    with col3:
        st.markdown("### ⚡ Enhanced  Features")
        st.write("✅ Advanced Maturity Damping")
        st.write("✅ Price Velocity Staking") 
        st.write(f"✅ Starting McAp: ${config.starting_mcap_usdt/1e6:.1f}M")
        st.write(f"✅ Maturity Target: ${config.maturity_target_mcap/1e9:.1f}B")
        st.write("✅ Real Circulating Supply")
        st.write("✅ Enhanced Dynamic APY")
        st.write("✅ 16 quarter advanced scenarios")
    
    # Enhanced launch button
    if st.button(f"🚀 Enhanced NXID Tokenomics  Launch - {scenario.upper()} Advanced Scenario", 
                 type="primary", use_container_width=True) and config_valid:
        
        with st.spinner(f"🎯 Enhanced Advanced Maturity + Dynamic + Price Velocity simulation  running - {scenario.upper()} scenario..."):
            
            # Enhanced model ve yöneticileri başlat
            model = EnhancedTokenomicsModel(config)
            viz_manager = EnhancedVisualizationManager(config)
            analytics_manager = AnalyticsManager(config)
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # === PHASE 1: ENHANCED SIMPLE FAİZ PRESALE ===
            status_text.text("🔥 Phase 1: Enhanced Simple Interest presale simulation - Dynamic APY...")
            presale_df = model.simulate_presale_phase()
            progress_bar.progress(20)
            
            # === PHASE 1.5: ENHANCED HAFTALIK SIMPLE FAİZ ===
            status_text.text("📊 Phase 1.5: Enhanced weekly simple interest analysis...")
            weekly_token_df = model.generate_weekly_token_analysis(presale_df)
            progress_bar.progress(30)
            
            # === PHASE 2: ENHANCED VESTING (STAKING POOLS DAHİL) ===
            status_text.text("📅 Phase 2: Enhanced vesting schedules - staking pools included...")
            vesting_df = model.calculate_individual_vesting_schedules()
            progress_bar.progress(45)
            
            # === PHASE 3: ENHANCED ADVANCED MAINNET  ===
            status_text.text(f"🚀 Phase 3: Enhanced Advanced Mainnet + Maturity Damping - {scenario.upper()} scenario (16 quarters)...")
            mainnet_df = model.simulate_mainnet_phase(presale_df, vesting_df, scenario)
            progress_bar.progress(65)
            
            # === PHASE 4: ENHANCED GÖRSELLEŞTİRMELER  ===
            status_text.text("🎨 Phase 4: Enhanced visualizations  - advanced charts...")
            charts = viz_manager.create_enhanced_visualizations_v4(  # v4 fonksiyonunu kullan
                presale_df, weekly_token_df, vesting_df, mainnet_df, scenario
            )
            progress_bar.progress(85)
            
            # === PHASE 5: ENHANCED METRİKLER  ===
            status_text.text("📊 Phase 5: Enhanced metrics  + advanced maturity + dynamic systems...")
            metrics = model.calculate_enhanced_metrics(
                presale_df, weekly_token_df, vesting_df, mainnet_df
            )
            progress_bar.progress(100)
            
            status_text.text("🎯 Enhanced simulation  completed!")
            
            # Enhanced sonuçları sakla
            st.session_state['enhanced_results_v6'] = {
                'presale_df': presale_df,
                'weekly_token_df': weekly_token_df,
                'vesting_df': vesting_df,
                'mainnet_df': mainnet_df,
                'charts': charts,
                'metrics': metrics,
                'config': config,
                'scenario': scenario
            }
            
            # Enhanced config'i otomatik kaydet
            config.save_to_json("nxid_enhanced_config_v6.json")
        
        st.success(f"🎯 Enhanced simulation  successfully completed! - {scenario.upper()} advanced scenario")
    
    elif not config_valid:
        st.error("❌ Fix configuration before running enhanced simulation")
    
    # === ENHANCED SONUÇLARI GÖSTER ===
    if 'enhanced_results_v6' in st.session_state:
        results = st.session_state['enhanced_results_v6']
        charts = results['charts']
        metrics = results['metrics']
        scenario = results['scenario']
        
        # Enhanced Analytics yöneticisini başlat
        analytics_manager = AnalyticsManager(config)
        
        # === ENHANCED EXECUTIVE DASHBOARD  ===
        st.markdown(f'''
        <h2 style="font-family: Orbitron, monospace; font-size: 2.5rem; font-weight: 700; 
                   color: #1B8EF2; margin: 2.5rem 0 1.5rem 0; padding: 1rem 0 0.5rem 0; 
                   border-bottom: 3px solid transparent; text-align: center;
                   border-image: linear-gradient(90deg, #1B8EF2, #3effc8) 1;
                   text-shadow: 0 0 20px rgba(27, 142, 242, 0.6);">
            🎯 Enhanced Executive Dashboard  - {scenario.upper()} Advanced Scenario
        </h2>
        ''', unsafe_allow_html=True)
        
        analytics_manager.display_executive_dashboard_v6(metrics, scenario)
        
        # === ENHANCED BÜYÜK GÖRSELLEŞTİRMELER  ===
        st.markdown(f'''
        <h2 style="font-family: Orbitron, monospace; font-size: 2.2rem; font-weight: 700; 
                   color: #1B8EF2; margin: 2.5rem 0 1.5rem 0; padding: 1rem 0 0.5rem 0; 
                   border-bottom: 3px solid transparent; text-align: center;
                   border-image: linear-gradient(90deg, #1B8EF2, #3effc8) 1;
                   text-shadow: 0 0 20px rgba(27, 142, 242, 0.6);">
            🎯 Enhanced NXID Tokenomics Visualizations 
        </h2>
        ''', unsafe_allow_html=True)
        
        # === 1. ENHANCED TOKEN DAĞITIMI (LOGO İLE) ===
        st.markdown("## 1. Enhanced Token Dağıtımı - Logo İle")
        st.plotly_chart(charts['distribution'], use_container_width=True)
        
        # === 2. ENHANCED VESTING PROGRAMI (STAKING POOLS DAHİL) ===
        st.markdown("## 2. Enhanced Token Serbest Bırakma Programı (Staking Havuzları Dahil)")
        st.plotly_chart(charts['vesting'], use_container_width=True)
        
        # === 3. ENHANCED SIMPLE FAİZ PRESALE ANALIZ GRUBU ===
        st.markdown("## 3. Enhanced Basit Faiz Presale Analizi")
        
        # 3a. Presale temel analiz
        st.markdown("### 3a. Presale Temel Performans - Günlük Satış ve Fiyat")
        st.plotly_chart(charts['presale_basic'], use_container_width=True)
        
        # 3b. Enhanced Simple Faiz APY analizi
        st.markdown("### 3b. Enhanced Basit Faiz + Dinamik APY Sistemi")
        st.info("🎯 **Enhanced Basit Faiz Sistemi :** Bileşik faiz yok, sadece ana para üzerinden günlük faiz. APY havuz kullanımını optimize etmek için dinamik olarak ayarlanır. Şeffaf ve öngörülebilir.")
        st.plotly_chart(charts['presale_apy'], use_container_width=True)
        
        # 3c. USD ve Token satış analizi
        st.markdown("### 3c. Enhanced Presale USD ve Token Satış Analizi")
        st.plotly_chart(charts['presale_usd_tokens'], use_container_width=True)
        
        # 3d. Enhanced Haftalık Simple Faiz token tracking
        if 'weekly_tokens' in charts:
            st.markdown("### 3d. Enhanced Haftalık Basit Faiz Token Takibi")
            st.info(f"""
            🎯 **Enhanced Haftalık Basit Faiz Takibi :** 
            Her hafta ${config.weekly_investment_amount} yatırım yapan yatırımcı.
            Bileşik faiz olmadan günlük basit faiz kazanç analizi.
            Gelişmiş kontrol paneli tek hafta seçimi veya değişiklikleri görüntüleme imkanı sunar.
            Gelişmiş model daha tutarlı sonuçlar sağlar.
            """)
            st.plotly_chart(charts['weekly_tokens'], use_container_width=True)
        
        # === 4. YENİ: MARKET CAP EVRİM ANALİZİ ===
        st.markdown(f"## 4. Market Cap Evrim Analizi  - {scenario.upper()}")
        st.info(f"🎯 **Market Cap Evrim Analizi :** Başlangıç McAp'tan hedef McAp'a doğru gelişimi, büyüme oranları ve hedef ilerlemesi analizi.")
        if 'mcap_evolution' in charts:
            st.plotly_chart(charts['mcap_evolution'], use_container_width=True)
        
        # === 5. YENİ: TOPLAM ARZ vs MARKET CAP ANALİZİ ===
        st.markdown(f"## 5. Toplam Arz vs Market Cap Analizi  - {scenario.upper()}")
        st.info(f"🎯 **Arz-McAp İlişkisi :** Yakılan tokenların toplam arza etkisi, etkili dolaşım arzı ve token fiyat dinamikleri analizi.")
        if 'total_supply_mcap' in charts:
            st.plotly_chart(charts['total_supply_mcap'], use_container_width=True)
        
        # === 6. ENHANCED MAINNET MARKET CHART ===
        st.markdown(f"## 6. Enhanced Mainnet Market Analizi  - {scenario.upper()}")
        st.info(f"🎯 **Enhanced Market Analizi :** Hedef (${config.maturity_target_mcap/1e9:.1f}B) ile gelişmiş maturity damping sistemi, dinamik staking ve fiyat hızı etkisi.")
        st.plotly_chart(charts['mainnet_market'], use_container_width=True)
        
        # === 7. ENHANCED DYNAMIC STAKING WITH PRICE VELOCITY  ===
        st.markdown("## 7. Enhanced Dinamik Staking Sistemi  - Fiyat Hızı Etkisi")
        st.info(f"🎯 **Fiyat Hızı Staking :** Staking'in fiyat değişim hızına yanıt verdiği devrimci sistem. Hızlı fiyat artışları → insanlar unstake yapar (satış fırsatı). Hızlı fiyat düşüşleri → insanlar stake yapar (güvenlik + ödüller). {config.price_velocity_window} günlük hız penceresi ile %{config.price_velocity_smoothing:.0f} yumuşatma.")
        st.plotly_chart(charts['mainnet_staking'], use_container_width=True)
        
        # === 8. YENİ: ADVANCED MATURITY ANALYSIS  ===
        if 'maturity_analysis' in charts:
            st.markdown("## 8. YENİ: Gelişmiş Maturity Analizi ")
            st.info(f"🎯 **Gelişmiş Maturity Damping :** Market cap otomatik olarak ${config.maturity_target_mcap/1e9:.1f}B hedefe yakınsıyor. Hedefin altında → BOOST etkisi ({config.maturity_boost_multiplier:.1f}x). Hedefin üstünde → DAMP etkisi ({config.maturity_damp_multiplier:.1f}x). Yakınsama hızı: %{config.maturity_convergence_speed:.1f}.")
            st.plotly_chart(charts['maturity_analysis'], use_container_width=True)
        
        # === 9. ENHANCED TAX & BURN ANALYSIS ===
        st.markdown("## 9. Enhanced Vergi ve Yakma Analizi")
        st.info("🎯 **Enhanced Yakma Etkisi :** Yakılan tokenlar kalıcı olarak toplam arzdan çıkarılır, gerçek dolaşımdaki arz hesaplamalarını etkiler.")
        st.plotly_chart(charts['mainnet_tax_burn'], use_container_width=True)
        
        # === ENHANCED KAPSAMLI ANALİTİK RAPOR  ===
        analytics_manager.display_comprehensive_analytics_report_v6(metrics, scenario)
        
        # === ENHANCED EXPORT SECTION  ===
        analytics_manager.display_export_section_v6(results)
        
        # === ENHANCED FINAL PERFORMANCE SUMMARY  ===
        analytics_manager.display_final_performance_summary_v6(metrics, scenario)
        
        # === ENHANCED SİSTEM AÇIKLAMASI  ===
        st.markdown('''
        <h3 style="color: #1B8EF2; margin: 2rem 0 1rem 0; font-family: Orbitron;">
            🎯 Enhanced NXID Tokenomics  System Summary
        </h3>
        ''', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
            ### 🔥 Simple Interest System 
            
            **Enhanced Core Features:**
            - Principal tracking (NO compounding)
            - Daily interest = Principal × (APY% / 365)
            - Dynamic APY optimizes pool depletion
            - Transparent and predictable calculation
            - Enhanced interest tracking
            
            **Weekly Analysis:**
            - Fixed ${config.weekly_investment_amount} weekly investment
            - Simple interest token gains
            - Clean analysis without compounding
            """)
        
        with col2:
            st.markdown(f"""
            ### 🚀 Advanced Maturity + Dynamic Systems 
            
            **Advanced Maturity Damping:**
            - Target: ${config.maturity_target_mcap/1e9:.1f}B McAp
            - Convergence speed: {config.maturity_convergence_speed:.1%}
            - Boost multiplier: {config.maturity_boost_multiplier:.1f}x (below target)
            - Damp multiplier: {config.maturity_damp_multiplier:.1f}x (above target)
            - Automatic market cap convergence
            
            **Price Velocity Staking:**
            - {config.price_velocity_window}-day velocity window
            - {config.price_velocity_smoothing:.0%} smoothing factor
            - {abs(config.price_velocity_impact)*100:.0f}% staking sensitivity
            - Psychology-based behavior
            """)
        
        with col3:
            st.markdown(f"""
            ### 🎯 Revolutionary Features 
            
            **Real Circulating Supply:**
            - Staked tokens: {'Excluded' if not config.include_staked_in_circulating else 'Included'}
            - Burned tokens: {'Permanently removed' if config.burn_effect_permanent else 'Ignored'}
            - Price calculation: McAp ÷ Effective Supply
            - Realistic market dynamics
            
            **Enhanced Dynamic APY:**
            - Pool depletion factor: {config.pool_depletion_apy_factor:.1f}
            - Staking saturation factor: {config.staking_saturation_factor:.1f}
            - Market demand factor: {config.market_demand_apy_factor:.1f}
            - Duration: {config.staking_pool_duration_years} years
            
            **System Health:**
            - Enhanced validation ✅
            - Comprehensive export ✅
            - Real-time config management ✅
            - Advanced visualizations ✅
            """)
        
        # Enhanced özet performans metriği
        avg_user_peak_roi = metrics['mainnet']['ortalama_kullanici_zirve_roi']
        maturity_progress = metrics['mainnet']['max_maturity_progress'] if metrics['mainnet']['maturity_damping_aktif'] else 0
        
        if avg_user_peak_roi >= 10 and maturity_progress >= 75:
            st.success(f"🏆 **PHENOMENAL ENHANCED TOKENOMICS **: Average user {avg_user_peak_roi:.1f}x ROI + {maturity_progress:.1f}% maturity progress!")
        elif avg_user_peak_roi >= 5 and maturity_progress >= 50:
            st.info(f"📈 **EXCELLENT ENHANCED SYSTEM **: Average user {avg_user_peak_roi:.1f}x ROI + {maturity_progress:.1f}% maturity progress!")
        elif avg_user_peak_roi >= 2:
            st.warning(f"📊 **GOOD ENHANCED PERFORMANCE **: Average user {avg_user_peak_roi:.1f}x ROI - Maturity optimization may be needed")
        else:
            st.error(f"📉 **ENHANCED IMPROVEMENT NEEDED **: Average user {avg_user_peak_roi:.1f}x ROI - Review system parameters")

if __name__ == "__main__":
    main()