#!/usr/bin/env python3
"""
NXID  Tokenomics - Streamlit Share Compatible Main App
============================================================
 Cyclical + Unlimited Parameters + Single Page Charts + Auto Balance + DEFAULT.JSON AUTO LOAD
"""

import streamlit as st
import sys
import os

# Streamlit Share için konfigürasyon
st.set_page_config(
    page_title="NXID  Tokenomics -  Cyclical",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import modülleri - Mevcut dosyalarla uyumlu
try:
    from config import NXIDConfig
    from models import TokenomicsModel  # ← Mevcut class adı
    from visualizations import VisualizationManager
    from analytics import AnalyticsManager
    from sidebar import SidebarManager
    from utils import load__css, display_header
except ImportError as e:
    st.error(f"Modül import hatası: {e}")
    st.error("Lütfen tüm dosyaların aynı dizinde olduğundan emin olun.")
    st.stop()

def main():
    """Ana uygulama fonksiyonu"""
    try:
        # CSS ve header yükle
        load__css()
        display_header()
        
        # 🎯 DEFAULT.JSON AUTO-LOAD NOTIFICATION
        st.info("🎯 **DEFAULT.JSON AUTO-LOAD**: Uygulama default.json dosyasından otomatik ayarları yüklüyor!")
        
        # Sidebar manager
        sidebar_manager = SidebarManager()
        config, config_valid = sidebar_manager.render_sidebar()
        
        if not config_valid:
            st.error("❌ Lütfen konfigürasyonu düzeltin!")
            return
        
        # Scenario seçimi
        st.markdown("### 🎯   Cyclical Market Scenario Selection")
        st.info("🔄 ** Cyclical System**: Market scenarios repeat every 20 quarters (5 years) infinitely!")
        
        scenario_col1, scenario_col2, scenario_col3 = st.columns(3)
        
        with scenario_col1:
            if st.button("🐻 BEAR Cyclical Analysis", use_container_width=True):
                st.session_state.selected_scenario = 'bear'
        
        with scenario_col2:
            if st.button("📊 BASE Cyclical Analysis", use_container_width=True):
                st.session_state.selected_scenario = 'base'
        
        with scenario_col3:
            if st.button("🐂 BULL Cyclical Analysis", use_container_width=True):
                st.session_state.selected_scenario = 'bull'
        
        # Default scenario
        if 'selected_scenario' not in st.session_state:
            st.session_state.selected_scenario = 'base'
        
        # Seçilen scenario'yu göster
        scenario = st.session_state.selected_scenario
        scenario_colors = {'bear': '#ef4444', 'base': '#1B8EF2', 'bull': '#22c55e'}
        scenario_color = scenario_colors[scenario]
        
        #  cycle information
        cycle_info = {
            'bear': "Downtrend with recovery cycles over 5 years",
            'base': "Balanced growth with normal market cycles", 
            'bull': "Aggressive growth with euphoric peaks"
        }
        
        st.markdown(f"""
        <div style="text-align: center; margin: 1.5rem 0; padding: 1rem; 
                    background: linear-gradient(135deg, {scenario_color}22, {scenario_color}11);
                    border: 2px solid {scenario_color}; border-radius: 15px;">
            <h3 style="color: {scenario_color}; margin: 0; font-family: Orbitron;">
                🔄 Selected: {scenario.upper()}  Cyclical Scenario
            </h3>
            <p style="color: {scenario_color}; margin: 0.5rem 0 0 0; font-size: 1rem;">
                {cycle_info[scenario]} • Repeats every 20 quarters
            </p>
            <p style="color: {scenario_color}aa; margin: 0.3rem 0 0 0; font-size: 0.9rem;">
                🎯 DEFAULT.JSON config loaded automatically
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Ana analiz butonu
        st.markdown("### 🚀 Launch   Cyclical Analysis")
        
        if st.button(f"🚀 Launch  NXID Tokenomics - {scenario.upper()} Cyclical", 
                    use_container_width=True, type="primary"):
            
            with st.spinner(f'🔮  {scenario.upper()}  cyclical tokenomics analizi yapılıyor...'):
                # Mevcut model class'ını kullan
                model = TokenomicsModel(config)
                viz_manager = VisualizationManager(config)
                analytics_manager = AnalyticsManager(config)
                
                # Progress göster
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                try:
                    # Presale analizi
                    status_text.text("🔥 Phase 1:  Simple Interest presale simulation...")
                    presale_df = model.simulate_presale_phase()
                    progress_bar.progress(25)
                    
                    # Weekly analizi
                    status_text.text("📊 Phase 2:  weekly simple interest analysis...")
                    weekly_token_df = model.generate_weekly_token_analysis(presale_df)
                    progress_bar.progress(45)
                    
                    # Vesting analizi
                    status_text.text("📅 Phase 3:  vesting schedules...")
                    vesting_df = model.calculate_individual_vesting_schedules()
                    progress_bar.progress(65)
                    
                    # Mainnet analizi
                    status_text.text(f"🚀 Phase 4:   Cyclical Mainnet {scenario.upper()} scenario...")
                    mainnet_df = model.simulate_mainnet_phase(presale_df, vesting_df, scenario)
                    progress_bar.progress(85)
                    
                    # Metrikleri hesapla
                    status_text.text("📊 Phase 5:  metrics calculation...")
                    metrics = model.calculate__metrics(presale_df, weekly_token_df, vesting_df, mainnet_df)
                    progress_bar.progress(100)
                    
                    status_text.text("✅   cyclical analysis completed!")
                    
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
                    
                    st.success(f"✅  {scenario.upper()}  cyclical analysis completed!")
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"❌ Analysis failed: {str(e)}")
                    st.exception(e)  # Debug için exception detaylarını göster
        
        # Sonuçları göster
        if st.session_state.get('analysis_completed', False):
            display_results_single_page()
    
    except Exception as e:
        st.error(f"Uygulama hatası: {e}")
        st.exception(e)  # Debug için exception detaylarını göster

def display_results_single_page():
    """Analiz sonuçlarını tek sayfada alt alta göster"""
    try:
        results = st.session_state.analysis_results
        scenario = results['scenario']
        scenario_colors = {'bear': '#ef4444', 'base': '#1B8EF2', 'bull': '#22c55e'}
        scenario_color = scenario_colors[scenario]
        
        # Analytics manager
        analytics = AnalyticsManager(results['config'])
        
        # === EXECUTIVE DASHBOARD ===
        st.markdown(f'''
        <h2 style="font-family: Orbitron, monospace; font-size: 2.5rem; font-weight: 700; 
                   color: {scenario_color}; margin: 2.5rem 0 1.5rem 0; padding: 1rem 0 0.5rem 0; 
                   border-bottom: 3px solid {scenario_color}; text-align: center;
                   text-shadow: 0 0 20px rgba(27, 142, 242, 0.6);">
            🎯 Executive Dashboard - {scenario.upper()}  Cyclical
        </h2>
        ''', unsafe_allow_html=True)
        
        analytics.display_executive_dashboard_v6(results['metrics'], scenario)
        
        # ===  VISUALIZATIONS - SINGLE PAGE ===
        st.markdown(f'''
        <h2 style="font-family: Orbitron, monospace; font-size: 2.2rem; font-weight: 700; 
                   color: {scenario_color}; margin: 3rem 0 1.5rem 0; padding: 1rem 0 0.5rem 0; 
                   border-bottom: 3px solid {scenario_color}; text-align: center;
                   text-shadow: 0 0 20px rgba(27, 142, 242, 0.6);">
            📊   Cyclical Visualizations - All Charts
        </h2>
        ''', unsafe_allow_html=True)
        
        # Visualizations oluştur
        viz_manager = VisualizationManager(results['config'])
        charts = viz_manager.create__visualizations_v4(
            results['presale_df'],
            results['weekly_token_df'],
            results['vesting_df'],
            results['mainnet_df'],
            scenario
        )
        
        # === 1. TOKEN DISTRIBUTION ===
        st.markdown("## 1. 📊  Token Distribution - With Logo")
        if 'distribution' in charts:
            st.plotly_chart(charts['distribution'], use_container_width=True)
        
        # === 2. VESTING SCHEDULE ===
        st.markdown("## 2. 📅  Token Release Schedule (Including Staking Pools)")
        if 'vesting' in charts:
            st.plotly_chart(charts['vesting'], use_container_width=True)
        
        # === 3. PRESALE CHARTS GROUP ===
        st.markdown("## 3. 🔥  Simple Interest Presale Analysis Group")
        
        # 3a. Presale Basic
        st.markdown("### 3a. 📈 Presale Basic Performance")
        if 'presale_basic' in charts:
            st.plotly_chart(charts['presale_basic'], use_container_width=True)
        
        # 3b. Presale USD & Tokens
        st.markdown("### 3b. 💰 Presale USD & Token Sales Analysis")
        if 'presale_usd_tokens' in charts:
            st.plotly_chart(charts['presale_usd_tokens'], use_container_width=True)
        
        # 3c. Presale APY & Staking
        st.markdown("### 3c. ⚡  Simple Interest + Dynamic APY System")
        st.info("🎯 ** Simple Interest System**: No compounding - only daily interest on principal. APY dynamically adjusts to optimize pool usage.")
        if 'presale_apy' in charts:
            st.plotly_chart(charts['presale_apy'], use_container_width=True)
        
        # 3d. Weekly Tracking
        if 'weekly_tokens' in charts:
            st.markdown("### 3d. 📊  Weekly Simple Interest Token Tracking")
            st.info(f"""
            🎯 ** Weekly Simple Interest Tracking**: 
            Investor making ${results['config'].weekly_investment_amount} weekly investment.
            Daily simple interest gains analysis without compounding.
             control panel for single week selection or viewing changes.
            """)
            st.plotly_chart(charts['weekly_tokens'], use_container_width=True)
        
        # === 4. MARKET CAP EVOLUTION ===
        st.markdown(f"## 4. 📈 Market Cap Evolution Analysis - {scenario.upper()}  Cyclical")
        st.info(f"🔄 ** Cyclical Evolution**: Market cap evolution from starting McAp to target McAp, growth rates and target progression analysis over repeating  cycles.")
        if 'mcap_evolution' in charts:
            st.plotly_chart(charts['mcap_evolution'], use_container_width=True)
        
        # === 5. TOTAL SUPPLY vs MARKET CAP ===
        st.markdown(f"## 5. 🔢 Total Supply vs Market Cap Analysis - {scenario.upper()}")
        st.info(f"🎯 **Supply-McAp Relationship**: Effect of burned tokens on total supply, effective circulating supply and token price dynamics analysis.")
        if 'total_supply_mcap' in charts:
            st.plotly_chart(charts['total_supply_mcap'], use_container_width=True)
        
        # === 6. SEPARATE MARKET CAP ANALYSIS ===
        st.markdown(f"## 6. 📊 Separate Market Cap Analysis - {scenario.upper()}")
        st.info(f"🎯 **Dedicated McAp Analysis**: Focused market cap analysis with maturity target (${results['config'].maturity_target_mcap/1e9:.1f}B) and  maturity damping system.")
        if 'separate_mcap' in charts:
            st.plotly_chart(charts['separate_mcap'], use_container_width=True)
        
        # === 7. CIRCULATING SUPPLY ANALYSIS ===
        st.markdown("## 7. 🔄 Circulating Supply Analysis")
        st.info("🎯 **Real Circulating Supply**: Proper exclusion of staked and burned tokens from calculations for realistic price modeling.")
        if 'circulating_supply' in charts:
            st.plotly_chart(charts['circulating_supply'], use_container_width=True)
        
        # === 8.  MAINNET MARKET ===
        st.markdown(f"## 8. 🚀  Mainnet Market Analysis - {scenario.upper()}  Cyclical")
        st.info(f"🔄 ** Cyclical Market**: Target (${results['config'].maturity_target_mcap/1e9:.1f}B) with advanced maturity damping system, dynamic staking and price velocity effect over repeating market cycles.")
        if 'mainnet_market' in charts:
            st.plotly_chart(charts['mainnet_market'], use_container_width=True)
        
        # === 9.  DYNAMIC STAKING ===
        st.markdown("## 9. ⚡  Dynamic Staking System - Price Velocity Effect")
        st.info(f"🚀 **Price Velocity Staking**: Revolutionary system where staking responds to price change speed. Fast price increases → people unstake (sell opportunity). Fast price decreases → people stake (safety + rewards). {results['config'].price_velocity_window}-day velocity window with {results['config'].price_velocity_smoothing:.0%} smoothing.")
        if 'mainnet_staking' in charts:
            st.plotly_chart(charts['mainnet_staking'], use_container_width=True)
        
        # === 10. ADVANCED MATURITY ANALYSIS ===
        if 'maturity_analysis' in charts:
            st.markdown("## 10. 🎯 Advanced Maturity Analysis")
            st.info(f"🎯 **Advanced Maturity Damping**: Market cap automatically converges toward ${results['config'].maturity_target_mcap/1e9:.1f}B target. Below target → BOOST effect ({results['config'].maturity_boost_multiplier:.1f}x). Above target → DAMP effect ({results['config'].maturity_damp_multiplier:.1f}x). Convergence speed: {results['config'].maturity_convergence_speed:.1%}.")
            st.plotly_chart(charts['maturity_analysis'], use_container_width=True)
        
        # === 11. TAX & BURN ANALYSIS ===
        st.markdown("## 11. 🔥  Tax & Burn Analysis")
        st.info("🔥 ** Burn Effect**: Burned tokens are permanently removed from total supply, affecting real circulating supply calculations.")
        if 'mainnet_tax_burn' in charts:
            st.plotly_chart(charts['mainnet_tax_burn'], use_container_width=True)
        
        # === COMPREHENSIVE ANALYTICS REPORT ===
        st.markdown(f'''
        <h2 style="font-family: Orbitron, monospace; font-size: 2.2rem; font-weight: 700; 
                   color: {scenario_color}; margin: 3rem 0 1.5rem 0; padding: 1rem 0 0.5rem 0; 
                   border-bottom: 3px solid {scenario_color}; text-align: center;
                   text-shadow: 0 0 20px rgba(27, 142, 242, 0.6);">
            📈 Comprehensive Analytics Report -  Cyclical
        </h2>
        ''', unsafe_allow_html=True)
        
        analytics.display_comprehensive_analytics_report_v6(results['metrics'], scenario)
        
        # === EXPORT SECTION ===
        st.markdown(f'''
        <h2 style="font-family: Orbitron, monospace; font-size: 2.2rem; font-weight: 700; 
                   color: {scenario_color}; margin: 3rem 0 1.5rem 0; padding: 1rem 0 0.5rem 0; 
                   border-bottom: 3px solid {scenario_color}; text-align: center;
                   text-shadow: 0 0 20px rgba(27, 142, 242, 0.6);">
            📁 Export & Download Section
        </h2>
        ''', unsafe_allow_html=True)
        
        analytics.display_export_section_v6(results)
        
        # === FINAL PERFORMANCE SUMMARY ===
        st.markdown(f'''
        <h2 style="font-family: Orbitron, monospace; font-size: 2.2rem; font-weight: 700; 
                   color: {scenario_color}; margin: 3rem 0 1.5rem 0; padding: 1rem 0 0.5rem 0; 
                   border-bottom: 3px solid {scenario_color}; text-align: center;
                   text-shadow: 0 0 20px rgba(27, 142, 242, 0.6);">
            🎯 Final Performance Summary -  Cyclical
        </h2>
        ''', unsafe_allow_html=True)
        
        analytics.display_final_performance_summary_v6(results['metrics'], scenario)
        
        # ===  SYSTEM SUMMARY ===
        st.markdown(f'''
        <h3 style="color: {scenario_color}; margin: 2rem 0 1rem 0; font-family: Orbitron;">
            🔄  NXID Tokenomics  Cyclical System Summary
        </h3>
        ''', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
            ### 🔥 Simple Interest System 
            
            ** Core Features:**
            - Principal tracking (NO compounding)
            - Daily interest = Principal × (APY% / 365)
            - Dynamic APY optimizes pool depletion
            - Transparent and predictable calculation
            -  interest tracking
            
            **Weekly Analysis:**
            - Fixed ${results['config'].weekly_investment_amount} weekly investment
            - Simple interest token gains
            - Clean analysis without compounding
            """)
        
        with col2:
            st.markdown(f"""
            ### 🔄  Cyclical + Advanced Systems 
            
            ** Cyclical Quarters:**
            - Target: ${results['config'].maturity_target_mcap/1e9:.1f}B McAp
            - 20 quarters per cycle (5 years)
            - Infinite repetition of market patterns
            - Bear/Base/Bull scenarios cycle forever
            - Realistic long-term market behavior
            
            **Price Velocity Staking:**
            - {results['config'].price_velocity_window}-day velocity window
            - {results['config'].price_velocity_smoothing:.0%} smoothing factor
            - {abs(results['config'].price_velocity_impact)*100:.0f}% staking sensitivity
            - Psychology-based behavior
            """)
        
        with col3:
            st.markdown(f"""
            ### 🎯 Revolutionary Features 
            
            **Unlimited Parameters:**
            - No min/max restrictions ✅
            - User can set any value ✅
            - Auto-balance distribution ✅
            - Real-time validation ✅
            
            ** Dynamic APY:**
            - Pool depletion factor: {results['config'].pool_depletion_apy_factor:.1f}
            - Staking saturation factor: {results['config'].staking_saturation_factor:.1f}
            - Market demand factor: {results['config'].market_demand_apy_factor:.1f}
            - Duration: {results['config'].staking_pool_duration_years} years
            
            **System Health:**
            -  cyclical validation ✅
            - Single page visualization ✅
            - Comprehensive export ✅
            - Advanced visualizations ✅
            - DEFAULT.JSON auto-load ✅
            """)
        
        #  özet performans metriği
        avg_user_peak_roi = results['metrics']['mainnet']['ortalama_kullanici_zirve_roi']
        maturity_progress = results['metrics']['mainnet']['max_maturity_progress'] if results['metrics']['mainnet']['maturity_damping_aktif'] else 0
        cycle_repetitions = results['metrics']['mainnet'].get('cycle_repetitions', 0)
        
        st.markdown(f"""
        ### 🏆  Cyclical Performance Summary
        
        **🔄 Cycle Information:**
        - Cycles completed: {cycle_repetitions} full cycles
        - Current scenario: {scenario.upper()}
        - Total quarters analyzed: {results['metrics']['mainnet'].get('total_quarters_analyzed', 0)}
        - Config source: DEFAULT.JSON
        
        **📊 Performance Metrics:**
        - Average user ROI: {avg_user_peak_roi:.1f}x peak
        - Maturity progress: {maturity_progress:.1f}%
        - System utilizes infinite  market cycles
        """)
        
        if avg_user_peak_roi >= 10 and maturity_progress >= 75:
            st.success(f"🏆 **PHENOMENAL  CYCLICAL TOKENOMICS**: Average user {avg_user_peak_roi:.1f}x ROI + {maturity_progress:.1f}% maturity progress with infinite cycles!")
        elif avg_user_peak_roi >= 5 and maturity_progress >= 50:
            st.info(f"📈 **EXCELLENT  CYCLICAL SYSTEM**: Average user {avg_user_peak_roi:.1f}x ROI + {maturity_progress:.1f}% maturity progress!")
        elif avg_user_peak_roi >= 2:
            st.warning(f"📊 **GOOD  CYCLICAL PERFORMANCE**: Average user {avg_user_peak_roi:.1f}x ROI - Maturity optimization may be needed")
        else:
            st.error(f"📉 ** CYCLICAL IMPROVEMENT NEEDED**: Average user {avg_user_peak_roi:.1f}x ROI - Review system parameters")

    except Exception as e:
        st.error(f"Results display error: {str(e)}")
        st.exception(e)

if __name__ == "__main__":
    main()