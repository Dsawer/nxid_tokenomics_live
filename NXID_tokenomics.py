#!/usr/bin/env python3
"""
NXID Enhanced Tokenomics - Streamlit Share Compatible Main App
============================================================
Ana uygulama dosyası - Streamlit Share için optimize edildi
"""

import streamlit as st
import sys
import os

# Streamlit Share için konfigürasyon
st.set_page_config(
    page_title="NXID Enhanced Tokenomics",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import modülleri - Mevcut dosyalarla uyumlu
try:
    from config import EnhancedNXIDConfig
    from models import EnhancedTokenomicsModel  # ← Mevcut class adı
    from visualizations import EnhancedVisualizationManager
    from analytics import AnalyticsManager
    from sidebar import SidebarManager
    from utils import load_enhanced_css, display_header
except ImportError as e:
    st.error(f"Modül import hatası: {e}")
    st.error("Lütfen tüm dosyaların aynı dizinde olduğundan emin olun.")
    st.stop()

def main():
    """Ana uygulama fonksiyonu"""
    try:
        # CSS ve header yükle
        load_enhanced_css()
        display_header()
        
        # Sidebar manager
        sidebar_manager = SidebarManager()
        config, config_valid = sidebar_manager.render_sidebar()
        
        if not config_valid:
            st.error("❌ Lütfen konfigürasyonu düzeltin!")
            return
        
        # Scenario seçimi
        st.markdown("### 🎯 Enhanced Market Scenario Selection")
        scenario_col1, scenario_col2, scenario_col3 = st.columns(3)
        
        with scenario_col1:
            if st.button("🐻 BEAR Market Analysis", use_container_width=True):
                st.session_state.selected_scenario = 'bear'
        
        with scenario_col2:
            if st.button("📊 BASE Market Analysis", use_container_width=True):
                st.session_state.selected_scenario = 'base'
        
        with scenario_col3:
            if st.button("🐂 BULL Market Analysis", use_container_width=True):
                st.session_state.selected_scenario = 'bull'
        
        # Default scenario
        if 'selected_scenario' not in st.session_state:
            st.session_state.selected_scenario = 'base'
        
        # Seçilen scenario'yu göster
        scenario = st.session_state.selected_scenario
        scenario_colors = {'bear': '#ef4444', 'base': '#1B8EF2', 'bull': '#22c55e'}
        scenario_color = scenario_colors[scenario]
        
        st.markdown(f"""
        <div style="text-align: center; margin: 1rem 0; padding: 1rem; 
                    background: linear-gradient(135deg, {scenario_color}22, {scenario_color}11);
                    border: 2px solid {scenario_color}; border-radius: 15px;">
            <h3 style="color: {scenario_color}; margin: 0; font-family: Orbitron;">
                🎯 Selected: {scenario.upper()} Market Scenario
            </h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Ana analiz butonu
        st.markdown("### 🚀 Launch Enhanced Analysis")
        
        if st.button(f"🚀 Launch Enhanced NXID Tokenomics - {scenario.upper()}", 
                    use_container_width=True, type="primary"):
            
            with st.spinner(f'🔮 Enhanced {scenario.upper()} tokenomics analizi yapılıyor...'):
                # Mevcut model class'ını kullan
                model = EnhancedTokenomicsModel(config)
                viz_manager = EnhancedVisualizationManager(config)
                analytics_manager = AnalyticsManager(config)
                
                # Progress göster
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                try:
                    # Presale analizi
                    status_text.text("🔥 Phase 1: Enhanced Simple Interest presale simulation...")
                    presale_df = model.simulate_presale_phase()
                    progress_bar.progress(25)
                    
                    # Weekly analizi
                    status_text.text("📊 Phase 2: Enhanced weekly simple interest analysis...")
                    weekly_token_df = model.generate_weekly_token_analysis(presale_df)
                    progress_bar.progress(45)
                    
                    # Vesting analizi
                    status_text.text("📅 Phase 3: Enhanced vesting schedules...")
                    vesting_df = model.calculate_individual_vesting_schedules()
                    progress_bar.progress(65)
                    
                    # Mainnet analizi
                    status_text.text(f"🚀 Phase 4: Enhanced Mainnet {scenario.upper()} scenario...")
                    mainnet_df = model.simulate_mainnet_phase(presale_df, vesting_df, scenario)
                    progress_bar.progress(85)
                    
                    # Metrikleri hesapla
                    status_text.text("📊 Phase 5: Enhanced metrics calculation...")
                    metrics = model.calculate_enhanced_metrics(presale_df, weekly_token_df, vesting_df, mainnet_df)
                    progress_bar.progress(100)
                    
                    status_text.text("✅ Enhanced analysis completed!")
                    
                    # Session state'e kaydet
                    st.session_state.analysis_results = {
                        'scenario': scenario,
                        'config': config,
                        'presale_df': presale_df,
                        'weekly_token_df': weekly_token_df,
                        'vesting_df': vesting_df,
                        'mainnet_df': mainnet_df,
                        'metrics': metrics
                    }
                    st.session_state.analysis_completed = True
                    
                    st.success(f"✅ Enhanced {scenario.upper()} analysis completed!")
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"❌ Analysis failed: {str(e)}")
                    st.exception(e)  # Debug için exception detaylarını göster
        
        # Sonuçları göster
        if st.session_state.get('analysis_completed', False):
            display_results()
    
    except Exception as e:
        st.error(f"Uygulama hatası: {e}")
        st.exception(e)  # Debug için exception detaylarını göster

def display_results():
    """Analiz sonuçlarını göster"""
    try:
        results = st.session_state.analysis_results
        scenario = results['scenario']
        
        # Analytics manager
        analytics = AnalyticsManager(results['config'])
        
        # Executive dashboard
        st.markdown("## 🎯 Executive Dashboard")
        analytics.display_executive_dashboard_v6(results['metrics'], scenario)
        
        # Visualizations
        st.markdown("## 📊 Enhanced Visualizations")
        viz_manager = EnhancedVisualizationManager(results['config'])
        charts = viz_manager.create_enhanced_visualizations_v4(
            results['presale_df'],
            results['weekly_token_df'],
            results['vesting_df'],
            results['mainnet_df'],
            scenario
        )
        
        # Chart display tabs
        tab_names = [
            "📊 Token Distribution",
            "📅 Vesting Schedule", 
            "🔥 Presale Basic",
            "💰 Presale USD & Tokens",
            "⚡ Presale APY & Staking",
            "📈 Weekly Tracking",
            "🚀 McAp Evolution",
            "📊 Total Supply vs McAp",
            "🎯 Market Cap Analysis",
            "🔄 Circulating Supply",
            "💎 Mainnet Market",
            "⚡ Mainnet Staking",
            "🎯 Maturity Analysis",
            "🔥 Tax & Burn"
        ]
        
        # Create tabs
        tabs = st.tabs(tab_names)
        
        chart_keys = [
            'distribution', 'vesting', 'presale_basic', 'presale_usd_tokens',
            'presale_apy', 'weekly_tokens', 'mcap_evolution', 'total_supply_mcap',
            'separate_mcap', 'circulating_supply', 'mainnet_market', 
            'mainnet_staking', 'maturity_analysis', 'mainnet_tax_burn'
        ]
        
        for i, (tab, chart_key) in enumerate(zip(tabs, chart_keys)):
            with tab:
                if chart_key in charts:
                    st.plotly_chart(charts[chart_key], use_container_width=True)
                else:
                    st.info(f"Chart '{chart_key}' not available for this scenario")
        
        # Analytics report
        st.markdown("## 📈 Comprehensive Analytics Report")
        analytics.display_comprehensive_analytics_report_v6(results['metrics'], scenario)
        
        # Export section
        st.markdown("## 📁 Export & Download")
        analytics.display_export_section_v6(results)
        
        # Final summary
        st.markdown("## 🎯 Final Performance Summary")
        analytics.display_final_performance_summary_v6(results['metrics'], scenario)
        
    except Exception as e:
        st.error(f"Results display error: {str(e)}")
        st.exception(e)

if __name__ == "__main__":
    main()  # ← Parantez eklendi!