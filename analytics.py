"""
NXID  Analytics and Reporting Module 
=================================================
Advanced Maturity Damping + Dynamic Staking + Price Velocity + Real Circulating Supply Analytics
"""

import pandas as pd
import streamlit as st
import json
from typing import Dict, List, Tuple
from utils import NXID_COLORS, create_metric_card, format_number
from config import NXIDConfig

class AnalyticsManager:
    """📊  Analytics Manager  - Advanced Maturity + Dynamic Systems"""
    
    def __init__(self, config: NXIDConfig):
        self.config = config
    
    def display_executive_dashboard_v6(self, metrics: Dict, scenario: str):
        """ Tokenomics Dashboard"""
        
        # Senaryo rengini belirle
        scenario_color = NXID_COLORS['danger'] if scenario == 'bear' else (
            NXID_COLORS['success'] if scenario == 'bull' else NXID_COLORS['primary']
        )
        
        # ===  TOP-LEVEL METRICS  ===
        st.markdown("### 🎯 Key Performance Indicators ")
        
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        
        with col1:
            st.markdown(create_metric_card(
                "💰 Presale Raised",
                f"${metrics['presale']['toplam_toplanan_usdt']/1000000:.1f}M",
                "USDT (Simple Interest System)",
                NXID_COLORS['success']
            ), unsafe_allow_html=True)
        
        with col2:
            st.markdown(create_metric_card(
                "🚀 Starting McAp",
                f"${metrics['mainnet']['starting_mcap']/1000000:.1f}M",
                f"Peak: ${metrics['mainnet']['max_mcap']/1000000:.1f}M",
                NXID_COLORS['primary']
            ), unsafe_allow_html=True)
        
        with col3:
            st.markdown(create_metric_card(
                "⚡ Dynamic APY Avg",
                f"{metrics['presale']['ortalama_apy']:.1f}%",
                f"Type: {metrics['presale']['faiz_tipi']}",
                NXID_COLORS['gold']
            ), unsafe_allow_html=True)
        
        with col4:
            st.markdown(create_metric_card(
                f"📈 Peak Price ({scenario.upper()})",
                f"${metrics['mainnet']['max_tahmin_fiyat']:.4f}",
                f"Month {metrics['mainnet']['max_fiyat_zamani_ay']:.0f}",
                scenario_color
            ), unsafe_allow_html=True)
        
        with col5:
            st.markdown(create_metric_card(
                f"🎯 Peak ROI ({scenario.upper()})",
                f"{metrics['mainnet']['presale_fiyat_artisi']:.1f}x",
                "vs Presale Price",
                scenario_color
            ), unsafe_allow_html=True)
        
        with col6:
            st.markdown(create_metric_card(
                "🔥 Total Burned",
                f"{metrics['mainnet']['toplam_burned_token']/1e6:.1f}M",
                "NXID Tokens",
                NXID_COLORS['burn']
            ), unsafe_allow_html=True)
        
        # ===   ADVANCED FEATURES SECTION ===
        st.markdown("### 🚀 Advanced Features Dashboard ")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if metrics['mainnet']['maturity_damping_aktif']:
                maturity_target = metrics['mainnet']['maturity_target_mcap'] / 1e9
                max_progress = metrics['mainnet']['max_maturity_progress']
                st.markdown(create_metric_card(
                    "🎯 Maturity Damping",
                    f"${maturity_target:.1f}B",
                    f"Max Progress: {max_progress:.1f}%",
                    NXID_COLORS['gold']
                ), unsafe_allow_html=True)
            else:
                st.markdown(create_metric_card(
                    "🎯 Maturity Damping",
                    "DISABLED",
                    "Pure market scenarios",
                    NXID_COLORS['gray']
                ), unsafe_allow_html=True)
        
        with col2:
            max_velocity = metrics['mainnet'].get('max_price_velocity', 0) * 100
            min_velocity = metrics['mainnet'].get('min_price_velocity', 0) * 100
            st.markdown(create_metric_card(
                "🚀 Price Velocity Range",
                f"{min_velocity:.1f}% to {max_velocity:.1f}%",
                "Daily price change speed",
                NXID_COLORS['orange']
            ), unsafe_allow_html=True)
        
        with col3:
            max_staking = metrics['mainnet']['max_staking_orani'] * 100
            final_staking = metrics['mainnet'].get('final_staking_orani', 0) * 100
            st.markdown(create_metric_card(
                "⚡ Dynamic Staking Range",
                f"{final_staking:.1f}% → {max_staking:.1f}%",
                "Price-velocity responsive",
                NXID_COLORS['teal']
            ), unsafe_allow_html=True)
        
        with col4:
            avg_user_peak_roi = metrics['mainnet']['ortalama_kullanici_zirve_roi']
            avg_user_final_roi = metrics['mainnet']['ortalama_kullanici_final_roi']
            st.markdown(create_metric_card(
                "🏆 Average User ROI",
                f"{avg_user_peak_roi:.1f}x → {avg_user_final_roi:.1f}x",
                f"${metrics['mainnet']['ortalama_kullanici_yatirim']:.0f} investment",
                NXID_COLORS['success']
            ), unsafe_allow_html=True)
        
        # ===  PERFORMANCE ASSESSMENT  ===
        self._display__performance_assessment(metrics, scenario, avg_user_peak_roi, max_progress if metrics['mainnet']['maturity_damping_aktif'] else 0)
    
    def _display__performance_assessment(self, metrics: Dict, scenario: str, avg_user_peak_roi: float, maturity_progress: float):
        """ performance assessment with  features"""
        
        # Advanced scoring criteria
        advanced_score = 0
        
        # Maturity achievement (25 points)
        if metrics['mainnet']['maturity_damping_aktif']:
            if maturity_progress >= 100:
                advanced_score += 25
                maturity_status = "🎯 TARGET ACHIEVED!"
            elif maturity_progress >= 75:
                advanced_score += 20
                maturity_status = f"🎯 Near target ({maturity_progress:.1f}%)"
            elif maturity_progress >= 50:
                advanced_score += 15
                maturity_status = f"📊 Halfway there ({maturity_progress:.1f}%)"
            else:
                advanced_score += 5
                maturity_status = f"📉 Early stage ({maturity_progress:.1f}%)"
        else:
            advanced_score += 10  # Neutral score for disabled
            maturity_status = "❌ Disabled"
        
        # User ROI performance (25 points)
        if avg_user_peak_roi >= 20:
            advanced_score += 25
            roi_status = f"🚀 EXCEPTIONAL ({avg_user_peak_roi:.1f}x)"
        elif avg_user_peak_roi >= 10:
            advanced_score += 20
            roi_status = f"🎉 EXCELLENT ({avg_user_peak_roi:.1f}x)"
        elif avg_user_peak_roi >= 5:
            advanced_score += 15
            roi_status = f"📈 GOOD ({avg_user_peak_roi:.1f}x)"
        elif avg_user_peak_roi >= 2:
            advanced_score += 10
            roi_status = f"📊 MODERATE ({avg_user_peak_roi:.1f}x)"
        else:
            advanced_score += 5
            roi_status = f"📉 LOW ({avg_user_peak_roi:.1f}x)"
        
        # Dynamic staking effectiveness (25 points)
        max_staking = metrics['mainnet']['max_staking_orani']
        avg_staking = max_staking * 0.7  # Estimate average
        if avg_staking >= 0.5:
            advanced_score += 25
            staking_status = f"⚡ EXCELLENT ({max_staking:.0%} max)"
        elif avg_staking >= 0.35:
            advanced_score += 20
            staking_status = f"⚡ GOOD ({max_staking:.0%} max)"
        elif avg_staking >= 0.25:
            advanced_score += 15
            staking_status = f"📊 MODERATE ({max_staking:.0%} max)"
        else:
            advanced_score += 10
            staking_status = f"📉 LOW ({max_staking:.0%} max)"
        
        # System health (25 points)
        burn_percentage = (metrics['mainnet']['toplam_burned_token'] / self.config.total_supply) * 100
        tax_efficiency = metrics['mainnet']['toplam_tax_toplanan'] / 1e6  # Million tokens
        
        system_health = 0
        if burn_percentage >= 3:
            system_health += 10
        elif burn_percentage >= 1.5:
            system_health += 7
        else:
            system_health += 5
        
        if tax_efficiency >= 10:
            system_health += 10
        elif tax_efficiency >= 5:
            system_health += 7
        else:
            system_health += 5
        
        system_health += 5  #  bonus
        advanced_score += system_health
        
        # === DISPLAY ASSESSMENT ===
        if advanced_score >= 90:
            assessment_color = "success"
            assessment_text = f"🏆 **PHENOMENAL  SYSTEM** - Score: {advanced_score}/100"
        elif advanced_score >= 80:
            assessment_color = "success"
            assessment_text = f"🎉 **EXCELLENT  PERFORMANCE** - Score: {advanced_score}/100"
        elif advanced_score >= 70:
            assessment_color = "info"
            assessment_text = f"📈 **GOOD  SYSTEM** - Score: {advanced_score}/100"
        elif advanced_score >= 60:
            assessment_color = "warning"
            assessment_text = f"📊 **MODERATE  PERFORMANCE** - Score: {advanced_score}/100"
        else:
            assessment_color = "error"
            assessment_text = f"📉 **NEEDS  OPTIMIZATION** - Score: {advanced_score}/100"
        
        getattr(st, assessment_color)(assessment_text)
        
        # Detailed breakdown
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"**🎯 Maturity:** {maturity_status}")
        with col2:
            st.markdown(f"**🏆 User ROI:** {roi_status}")
        with col3:
            st.markdown(f"**⚡ Staking:** {staking_status}")
        with col4:
            st.markdown(f"**🔥 Burn:** {burn_percentage:.2f}% supply")
    
    def display_comprehensive_analytics_report_v6(self, metrics: Dict, scenario: str):
        """📊 Comprehensive  Analytics Report """
        st.markdown('''
        <h2 style="font-family: Orbitron, monospace; font-size: 2.2rem; font-weight: 700; 
                   color: #1B8EF2; margin: 2.5rem 0 1.5rem 0; padding: 1rem 0 0.5rem 0; 
                   border-bottom: 3px solid transparent; text-align: center;
                   border-image: linear-gradient(90deg, #1B8EF2, #3effc8) 1;
                   text-shadow: 0 0 20px rgba(27, 142, 242, 0.6);">
            Analitik Rapor
        </h2>
        ''', unsafe_allow_html=True)
        
        tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
            "🔥 Simple Interest Presale", 
            "📊 Weekly Simple Interest", 
            f"🚀 Mainnet {scenario.upper()}", 
            "⚡ Dynamic Staking ", 
            "🎯 Maturity Damping ",
            "🚀 Price Velocity ",
            "🔥 Tax & Burn", 
            "📅 Vesting Analysis"
        ])
        
        with tab1:
            self._display_simple_interest_presale_analytics_v6(metrics)
        
        with tab2:
            self._display_weekly_simple_interest_analytics(metrics)
        
        with tab3:
            self._display_mainnet_analytics_v6(metrics, scenario)
        
        with tab4:
            self._display_dynamic_staking_analytics_v6(metrics)
        
        with tab5:
            self._display_maturity_damping_analytics_v6(metrics, scenario)
        
        with tab6:
            self._display_price_velocity_analytics_v6(metrics)
        
        with tab7:
            self._display_mainnet_tax_burn_analytics_v6(metrics)
        
        with tab8:
            self._display_vesting_analytics_v6(metrics)
    
    def _display_simple_interest_presale_analytics_v6(self, metrics: Dict):
        """🔥 Simple Interest Presale Analytics """
        st.markdown("### 🔥 Simple Interest + Dynamic APY Presale Performance ")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 📊 Core Simple Interest Metrics")
            st.write(f"- **Duration**: {metrics['presale']['presale_gun_sayisi']} days")
            st.write(f"- **Raised Funds**: ${metrics['presale']['toplam_toplanan_usdt']/1e6:.1f}M USDT")
            st.write(f"- **Sold Tokens**: {metrics['presale']['satilan_token']/1e9:.1f}B NXID")
            st.write(f"- **Final Price**: ${metrics['presale']['final_presale_fiyati']:.4f}")
            st.write(f"- **Price Growth**: {metrics['presale']['presale_fiyat_artisi']:.1f}%")
            st.write(f"- **Interest System**: {metrics['presale']['faiz_tipi']}")
            
        with col2:
            st.markdown("#### ⚡ Dynamic APY + Simple Interest System")
            st.write(f"- **Average Dynamic APY**: {metrics['presale']['ortalama_apy']:.1f}%")
            st.write(f"- **APY Demand Effect**: {metrics['presale']['apy_talep_etkisi']:.2f}x average")
            st.write(f"- **Price Resistance Effect**: {metrics['presale']['fiyat_direnc_etkisi']:.2f}x average")
            st.write(f"- **Pool Depletion**: {metrics['presale']['havuz_tukenme_yuzdesi']:.1f}%")
            st.write(f"- **Total Interest Rewards**: {metrics['presale']['toplam_dagitilan_odul']/1e6:.1f}M NXID")
            st.write(f"- **Dynamic APY Usage**: {'✅ Active' if metrics['presale']['dinamik_apy_kullanimi'] else '❌ Passive'}")
            
            # Simple interest gain calculation
            if 'ana_para_tokens' in metrics['presale'] and 'toplam_balance' in metrics['presale']:
                ana_para = metrics['presale']['ana_para_tokens']
                toplam_balance = metrics['presale']['toplam_balance']
                faiz_kazanci = toplam_balance - ana_para
                faiz_orani = (faiz_kazanci / ana_para * 100) if ana_para > 0 else 0
                
                st.success(f"💰 **Simple Interest Gain**: {faiz_kazanci/1e6:.1f}M NXID ({faiz_orani:.1f}%)")
            
            st.info("""
            💡 **Gelişmiş Basit Faiz Sistemi**
            • Bileşik faiz YOK - sadece ana para üzerinden faiz
            • Dinamik APY havuz kullanımını optimize eder
            • Günlük faiz = Ana Para × (APY% / 365)
            • Şeffaf ve öngörülebilir hesaplamalar
            • Market dinamikleri ile geliştirildi
            """)
    def _display_weekly_simple_interest_analytics(self, metrics: Dict):
        """📊 Weekly Simple Interest Analytics"""
        st.markdown("### 📊 Haftalık Basit Faiz Analizi")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 📈 Haftalık Yatırım Performansı")
            st.write(f"- **Toplam Hafta Sayısı**: {metrics['haftalik_tokenlar']['toplam_hafta_sayisi']}")
            st.write(f"- **Sabit Haftalık Yatırım**: ${metrics['haftalik_tokenlar']['sabit_yatirim_miktari']:.0f}")
            st.write(f"- **Ortalama Haftalık Token**: {metrics['haftalik_tokenlar']['ortalama_haftalik_token']/1e6:.2f}M NXID")
            st.write(f"- **Ortalama Staking Kazancı**: {metrics['haftalik_tokenlar']['ortalama_staking_kazanci']/1e6:.2f}M NXID")
            st.write(f"- **En İyi Hafta**: {metrics['haftalik_tokenlar']['en_iyi_hafta']}. hafta")
            st.write(f"- **En Kötü Hafta**: {metrics['haftalik_tokenlar']['en_kotu_hafta']}. hafta")
            
        with col2:
            st.markdown("#### 💰 Basit Faiz Token Kazançları")
            st.write(f"- **Ortalama Toplam Token**: {metrics['haftalik_tokenlar']['ortalama_toplam_token']/1e6:.2f}M NXID")
            st.write(f"- **Ortalama Token Kazanç %**: {metrics['haftalik_tokenlar']['ortalama_token_kazanc_yuzdesi']:.1f}%")
            st.write(f"- **Ortalama Ana Para**: {metrics['haftalik_tokenlar']['ortalama_ana_para']/1e6:.2f}M NXID")
            st.write(f"- **Faiz Tipi**: {metrics['haftalik_tokenlar']['faiz_tipi']}")
            
            # Haftalık kazanç analizi
            if metrics['haftalik_tokenlar']['ortalama_token_kazanc_yuzdesi'] >= 100:
                st.success("✅ Mükemmel haftalık basit faiz performansı!")
            elif metrics['haftalik_tokenlar']['ortalama_token_kazanc_yuzdesi'] >= 50:
                st.info("ℹ️ İyi haftalık token kazancı")
            else:
                st.warning("⚠️ Düşük haftalık faiz getirisi")
            
            st.info(f"""
            💡 **Haftalık DCA Stratejisi**
            • Sabit ${metrics['haftalik_tokenlar']['sabit_yatirim_miktari']:.0f} haftalık yatırım
            • Basit faiz sistemi - bileşik faiz YOK
            • Ortalama {metrics['haftalik_tokenlar']['ortalama_token_kazanc_yuzdesi']:.1f}% token kazancı
            • Toplam {metrics['haftalik_tokenlar']['toplam_hafta_sayisi']} hafta analiz
            """)
        
    def _display_dynamic_staking_analytics_v6(self, metrics: Dict):
        """⚡  Dynamic Staking Analytics """
        st.markdown("### ⚡ Dinamik Staking")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 🚀 Price-Velocity Dynamic Staking")
            st.write(f"- **Max Staking Rate**: {metrics['mainnet']['max_staking_orani']*100:.1f}%")
            st.write(f"- **Final Staking Rate**: {metrics['mainnet'].get('final_staking_orani', 0)*100:.1f}%")
            st.write(f"- **Average Market APY**: {metrics['mainnet']['ortalama_market_apy']:.1f}%")
            st.write(f"- **Final Market APY**: {metrics['mainnet'].get('final_market_apy', 0):.1f}%")
            st.write(f"- **Staking Duration**: {self.config.staking_pool_duration_years} years")
            st.write(f"- **Price Velocity Impact**: {self.config.price_velocity_impact:.1f}")
            
        with col2:
            st.markdown("#### 🎯 Advanced Features ")
            st.write(f"- **Base Staking Rate**: {self.config.base_staking_rate*100:.1f}%")
            st.write(f"- **Min-Max Range**: {self.config.min_staking_rate*100:.1f}% - {self.config.max_staking_rate*100:.1f}%")
            st.write(f"- **Price Velocity Window**: {self.config.price_velocity_window} days")
            st.write(f"- **Staking Momentum**: {self.config.staking_momentum:.1%}")
            st.write(f"- **Entry/Exit Speed**: {self.config.staking_entry_speed:.1%}/{self.config.staking_exit_speed:.1%}")
            st.write(f"- **Total Unstaking Events**: {metrics['mainnet'].get('total_unstaking_events', 0)}")
            
            # Price velocity analytics
            max_velocity = metrics['mainnet'].get('max_price_velocity', 0) * 100
            min_velocity = metrics['mainnet'].get('min_price_velocity', 0) * 100
            avg_velocity = metrics['mainnet'].get('avg_smoothed_velocity', 0) * 100
            
            st.success(f"""
            🚀 **Price Velocity Analytics:**
            • Range: {min_velocity:.1f}% to {max_velocity:.1f}%
            • Average: {avg_velocity:.2f}%
            • Impact on staking: {abs(self.config.price_velocity_impact):.0%} sensitivity
            """)
            
            if metrics['mainnet']['max_staking_orani'] > 0.4:
                st.success("✅ Excellent dynamic staking participation!")
            elif metrics['mainnet']['max_staking_orani'] > 0.25:
                st.info("ℹ️ Good dynamic staking levels")
            else:
                st.warning("⚠️ Low staking - high price velocity impact?")
    
    def _display_maturity_damping_analytics_v6(self, metrics: Dict, scenario: str):
        """🎯 Maturity Damping Analytics """
        st.markdown("### 🎯 Advanced Maturity Damping Analysis ")
        
        if not metrics['mainnet']['maturity_damping_aktif']:
            st.warning("❌ Maturity damping is disabled - showing pure market scenarios")
            st.info("Enable maturity damping in configuration for advanced market cap convergence")
            return
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 🎯 Maturity Target Achievement")
            target_mcap = metrics['mainnet']['maturity_target_mcap'] / 1e9
            starting_mcap = metrics['mainnet']['starting_mcap'] / 1e6
            max_progress = metrics['mainnet']['max_maturity_progress']
            final_progress = metrics['mainnet'].get('final_maturity_progress', 0)
            
            st.write(f"- **Target Market Cap**: ${target_mcap:.1f}B")
            st.write(f"- **Starting Market Cap**: ${starting_mcap:.1f}M")
            st.write(f"- **Growth Needed**: {target_mcap*1000/starting_mcap:.0f}x")
            st.write(f"- **Max Progress Achieved**: {max_progress:.1f}%")
            st.write(f"- **Final Progress**: {final_progress:.1f}%")
            st.write(f"- **Damping Strength**: {self.config.maturity_damping_strength:.1%}")
            
        with col2:
            st.markdown("#### ⚡ Damping System Parameters")
            st.write(f"- **Convergence Speed**: {self.config.maturity_convergence_speed:.1%}")
            st.write(f"- **Boost Multiplier**: {self.config.maturity_boost_multiplier:.1f}x (below target)")
            st.write(f"- **Damp Multiplier**: {self.config.maturity_damp_multiplier:.1f}x (above target)")
            
            # Distance analytics
            max_distance = metrics['mainnet'].get('max_maturity_distance', 0)
            min_distance = metrics['mainnet'].get('min_maturity_distance', 0)
            
            st.write(f"- **Max Distance Above**: {max_distance*100:.1f}% (if positive)")
            st.write(f"- **Max Distance Below**: {abs(min_distance)*100:.1f}% (if negative)")
            
            # Achievement assessment
            if max_progress >= 100:
                st.success("🎉 **MATURITY TARGET ACHIEVED!**")
                st.balloons()
            elif max_progress >= 75:
                st.info("📈 **NEAR TARGET** - Excellent progress")
            elif max_progress >= 50:
                st.warning("📊 **HALFWAY THERE** - Good progress")
            elif max_progress >= 25:
                st.warning("📉 **EARLY STAGE** - Needs optimization")
            else:
                st.error("🔴 **FAR FROM TARGET** - Review parameters")
        
        # Scenario-specific analysis
        scenario_color = NXID_COLORS['danger'] if scenario == 'bear' else (
            NXID_COLORS['success'] if scenario == 'bull' else NXID_COLORS['primary']
        )
        
        st.markdown(f"#### 📊 Maturity Performance in {scenario.upper()} Scenario")
        if scenario == 'bear':
            st.markdown("🐻 **Bear Market**: Maturity damping provides stability during downturns")
        elif scenario == 'bull':
            st.markdown("🐂 **Bull Market**: Maturity damping prevents excessive speculation")
        else:
            st.markdown("📊 **Base Market**: Maturity damping provides balanced growth")
        
        progress_efficiency = max_progress / (metrics['mainnet']['analiz_ay_sayisi'] / 12)  # Progress per year
        st.info(f"""
        🎯 **Maturity Efficiency Analysis:**
        • Target: ${target_mcap:.1f}B in {self.config.projection_months} months
        • Progress efficiency: {progress_efficiency:.1f}% per year
        • Damping effect: {'Active convergence' if max_progress > 10 else 'Needs adjustment'}
        • System status: {'Optimal' if 50 <= max_progress <= 120 else 'Needs tuning'}
        """)
    
    def _display_price_velocity_analytics_v6(self, metrics: Dict):
        """🚀 Price Velocity Analytics """
        st.markdown("### 🚀 Price Velocity Impact Analysis ")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 📊 Price Velocity Metrics")
            max_velocity = metrics['mainnet'].get('max_price_velocity', 0) * 100
            min_velocity = metrics['mainnet'].get('min_price_velocity', 0) * 100
            avg_velocity = metrics['mainnet'].get('avg_smoothed_velocity', 0) * 100
            max_effect = metrics['mainnet'].get('max_velocity_effect', 1.0)
            
            st.write(f"- **Max Daily Velocity**: {max_velocity:.2f}%")
            st.write(f"- **Min Daily Velocity**: {min_velocity:.2f}%")
            st.write(f"- **Average Smoothed Velocity**: {avg_velocity:.2f}%")
            st.write(f"- **Max Velocity Effect**: {max_effect:.2f}x")
            st.write(f"- **Velocity Window**: {self.config.price_velocity_window} days")
            st.write(f"- **Velocity Smoothing**: {self.config.price_velocity_smoothing:.1%}")
            
        with col2:
            st.markdown("#### ⚡ Staking Response System")
            st.write(f"- **Velocity Impact Factor**: {self.config.price_velocity_impact:.1f}")
            st.write(f"- **Staking Sensitivity**: {abs(self.config.price_velocity_impact):.0%}")
            st.write(f"- **Response Speed**: {(1-self.config.staking_momentum)*100:.0f}%")
            st.write(f"- **Exit Speed Multiplier**: {self.config.staking_exit_speed/self.config.staking_entry_speed:.1f}x")
            
            # Behavior analysis
            if abs(avg_velocity) > 5:
                st.warning("⚠️ High average velocity - volatile market conditions")
            elif abs(avg_velocity) > 2:
                st.info("📊 Moderate velocity - normal market fluctuations")
            else:
                st.success("✅ Low velocity - stable market conditions")
            
            st.info(f"""
            🚀 **Price Velocity System :**
            
            **How it works:**
            • Fast price increases → People unstake (sell opportunity)
            • Fast price decreases → People stake (safety + rewards)
            • {self.config.price_velocity_window}-day velocity calculation window
            • {self.config.price_velocity_smoothing:.0%} smoothing prevents erratic behavior
            
            **Impact:**
            • {abs(self.config.price_velocity_impact)*100:.0f}% staking change per 100% velocity
            • Exit {self.config.staking_exit_speed/self.config.staking_entry_speed:.1f}x faster than entry (realistic psychology)
            """)
        
        # Velocity-staking correlation analysis
        st.markdown("#### 🔄 Velocity-Staking Correlation")
        if max_velocity > 10:
            st.markdown("📈 **High Velocity Periods**: Strong price movements triggered significant staking changes")
        if min_velocity < -10:
            st.markdown("📉 **Price Crash Periods**: Rapid declines increased staking (flight to safety)")
        if abs(avg_velocity) < 1:
            st.markdown("📊 **Stable Periods**: Low velocity maintained consistent staking rates")
    
    def _display_mainnet_analytics_v6(self, metrics: Dict, scenario: str):
        """🚀  Mainnet Analytics """
        st.markdown(f"### 🚀  Mainnet Analysis  - {scenario.upper()} Scenario")
        
        scenario_color = NXID_COLORS['danger'] if scenario == 'bear' else (
            NXID_COLORS['success'] if scenario == 'bull' else NXID_COLORS['primary']
        )
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"#### 🚀  {scenario.upper()} Market Performance")
            st.write(f"- **Starting Market Cap**: ${metrics['mainnet']['starting_mcap']/1e6:.1f}M")
            st.write(f"- **Launch Market Cap**: ${metrics['mainnet']['launch_mcap']/1e6:.1f}M")
            st.write(f"- **Peak Market Cap**: ${metrics['mainnet']['max_mcap']/1e6:.1f}M")
            st.write(f"- **Peak Price**: ${metrics['mainnet']['max_tahmin_fiyat']:.4f}")
            st.write(f"- **Peak Time**: Month {metrics['mainnet']['max_fiyat_zamani_ay']:.1f}")
            st.write(f"- **Presale ROI**: {metrics['mainnet']['presale_fiyat_artisi']:.1f}x")
            st.write(f"- **Final Price**: ${metrics['mainnet']['final_token_fiyati']:.4f}")
            
        with col2:
            st.markdown("#### 💎  Supply & Price Dynamics ")
            st.write(f"- **Final Gross Circulating**: {metrics['mainnet']['final_dolasim_arzi']/1e9:.1f}B")
            st.write(f"- **Final Effective Circulating**: {metrics['mainnet']['final_effective_circulating']/1e9:.1f}B")
            st.write(f"- **Total Burned**: {metrics['mainnet']['toplam_burned_token']/1e6:.1f}M NXID")
            st.write(f"- **Max Staking Rate**: {metrics['mainnet']['max_staking_orani']*100:.1f}%")
            st.write(f"- **Average Market APY**: {metrics['mainnet']['ortalama_market_apy']:.1f}%")
            st.write(f"- **Analysis Duration**: {metrics['mainnet']['analiz_ay_sayisi']} months")
            st.write(f"- **Quarter Count**: {metrics['mainnet']['ceyrek_sayisi']} quarters")
            
            #  circulating supply insight
            gross_vs_effective = (metrics['mainnet']['final_dolasim_arzi'] - metrics['mainnet']['final_effective_circulating']) / 1e9
            st.success(f"💡 **Real Impact**: {gross_vs_effective:.1f}B tokens removed from effective supply")
            
            st.markdown(f"<p style='color: {scenario_color}; font-weight: bold; font-size: 1.2rem;'>🚀 Peak ROI: {metrics['mainnet']['presale_fiyat_artisi']:.1f}x ({scenario.upper()})</p>", unsafe_allow_html=True)
    
    def _display_mainnet_tax_burn_analytics_v6(self, metrics: Dict):
        """🔥 Tax & Burn Analytics """
        st.markdown("### 🔥 Mainnet Tax & Burn Analysis ")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 🔥 Tax System (Mainnet Only)")
            st.write(f"- **Tax Period**: {self.config.mainnet_tax_period_months} months")
            st.write(f"- **Tax Rate**: {self.config.mainnet_tax_rate}%")
            st.write(f"- **Total Tax Collected**: {metrics['mainnet']['toplam_tax_toplanan']/1e6:.1f}M NXID")
            st.write(f"- **Tax→Staking**: {self.config.tax_to_staking_percentage}%")
            st.write(f"- **Tax→Burn**: {self.config.tax_to_burn_percentage}%")
            st.write(f"- **Tax Burned**: {metrics['mainnet']['toplam_tax_burned']/1e6:.1f}M NXID")
            
        with col2:
            st.markdown("#### 💨 Burn Mechanism")
            st.write(f"- **Annual Burn Rate**: {self.config.annual_burn_rate*100:.1f}%")
            st.write(f"- **Burn Duration**: {self.config.burn_duration_years} years")
            st.write(f"- **Routine Burned**: {metrics['mainnet']['toplam_rutin_burned']/1e6:.1f}M NXID")
            st.write(f"- **Total Burned**: {metrics['mainnet']['toplam_burned_token']/1e6:.1f}M NXID")
            st.write(f"- **Burn Sources**: Tax + Routine")
            
            total_burned = metrics['mainnet']['toplam_burned_token']
            burn_percentage = (total_burned / self.config.total_supply) * 100
            
            if burn_percentage > 5:
                st.success(f"✅ Significant burn impact: {burn_percentage:.2f}%")
            elif burn_percentage > 2:
                st.info(f"ℹ️ Moderate burn impact: {burn_percentage:.2f}%")
            else:
                st.warning(f"⚠️ Low burn impact: {burn_percentage:.2f}%")
            
            #  burn impact analysis
            supply_reduction = total_burned / self.config.total_supply
            effective_supply = self.config.total_supply - total_burned
            
            st.info(f"""
            🔥 ** Burn Impact :**
            • Supply reduction: {supply_reduction:.2%}
            • Effective supply: {effective_supply/1e9:.1f}B NXID
            • Price impact: Deflationary pressure
            • Real circulating: Staked tokens excluded
            """)
    
    def _display_vesting_analytics_v6(self, metrics: Dict):
        """📅  Vesting Analytics """
        st.markdown("### 📅  Token Release Analysis ")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 📅  Vesting Timeline")
            st.write(f"- **Team Full Vested**: {metrics['vesting']['team_tam_vested_ay']} months")
            st.write(f"- **DAO Full Vested**: {metrics['vesting']['dao_tam_vested_ay']} months")
            st.write(f"- **Marketing Full Vested**: {metrics['vesting']['marketing_tam_vested_ay']} months")
            st.write(f"- **Presale Staking Vested**: {metrics['vesting']['presale_staking_tam_vested_ay']} months")
            st.write(f"- **Market Staking Vested**: {metrics['vesting']['market_staking_tam_vested_ay']} months")
            st.write(f"- **Vesting Delay**: 6 months from launch")
            
        with col2:
            st.markdown("#### 🔥  Token Release Progress")
            st.write(f"- **24-Month Total Released**: {metrics['vesting']['yirmidort_ay_toplam_vested']/1e9:.1f}B NXID")
            st.write(f"- **24-Month Circulating**: {metrics['vesting']['yirmidort_ay_dolasim']/1e9:.1f}B NXID")
            st.write(f"- **Staking Pool Vesting**: ✅ Included")
            
            circulating_24m_pct = (metrics['vesting']['yirmidort_ay_dolasim'] / self.config.total_supply) * 100
            
            if circulating_24m_pct < 60:
                st.success("✅ Conservative  release schedule")
            elif circulating_24m_pct < 80:
                st.info("ℹ️ Moderate  release speed")
            else:
                st.warning("⚠️ Aggressive  release schedule")
            
            st.info(f"""
            📅 ** Vesting Features :**
            • Staking pools included in vesting analysis
            • Real circulating supply calculations
            • Burn effects on total supply
            • Dynamic APY affects staking pool release
            • {circulating_24m_pct:.1f}% circulating after 24 months
            """)
    
    def display_export_section_v6(self, results: Dict):
        """📁  Export & Configuration Management """
        st.markdown('''
        <h2 style="font-family: Orbitron, monospace; font-size: 2.2rem; font-weight: 700; 
                   color: #1B8EF2; margin: 2.5rem 0 1.5rem 0; padding: 1rem 0 0.5rem 0; 
                   border-bottom: 3px solid transparent; text-align: center;
                   border-image: linear-gradient(90deg, #1B8EF2, #3effc8) 1;
                   text-shadow: 0 0 20px rgba(27, 142, 242, 0.6);">
            📁  Export & Configuration Management 
        </h2>
        ''', unsafe_allow_html=True)
        
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        
        with col1:
            presale_csv = results['presale_df'].to_csv(index=False)
            st.download_button(
                label="📥  Presale ",
                data=presale_csv,
                file_name=f"nxid__presale_v6.csv",
                mime="text/csv"
            )
        
        with col2:
            if not results['weekly_token_df'].empty:
                weekly_csv = results['weekly_token_df'].to_csv(index=False)
                st.download_button(
                    label="📥 Weekly  ",
                    data=weekly_csv,
                    file_name=f"nxid_weekly__v6.csv",
                    mime="text/csv"
                )
        
        with col3:
            mainnet_csv = results['mainnet_df'].to_csv(index=False)
            st.download_button(
                label=f"📥 {results['scenario'].upper()} ",
                data=mainnet_csv,
                file_name=f"nxid__mainnet_{results['scenario']}_v6.csv",
                mime="text/csv"
            )
        
        with col4:
            vesting_csv = results['vesting_df'].to_csv(index=False)
            st.download_button(
                label="📥  Vesting ",
                data=vesting_csv,
                file_name="nxid__vesting_v6.csv",
                mime="text/csv"
            )
        
        with col5:
            metrics_json = json.dumps(results['metrics'], indent=2, default=str)
            st.download_button(
                label="📥 Metrics ",
                data=metrics_json,
                file_name=f"nxid__metrics_{results['scenario']}_v6.json",
                mime="application/json"
            )
        
        with col6:
            config_json = json.dumps(results['config'].to_dict(), indent=2)
            st.download_button(
                label="📥 Config ",
                data=config_json,
                file_name="nxid__config_v6.json",
                mime="application/json"
            )
    
    def calculate_performance_score_v6(self, metrics: Dict, scenario: str) -> float:
        """🎯  Performance Score """
        
        # Presale performance (20%)
        presale_score = (
            (100 if metrics['presale']['havuz_tukenme_yuzdesi'] > 90 else 70) * 0.4 +
            (100 if metrics['presale']['ortalama_apy'] > 100 else 80) * 0.3 +
            (100 if metrics['haftalik_tokenlar']['ortalama_token_kazanc_yuzdesi'] > 50 else 70) * 0.3
        )
        
        # Mainnet performance (25%) - scenario adjusted
        scenario_multiplier = 0.7 if scenario == 'bear' else (1.3 if scenario == 'bull' else 1.0)
        mainnet_score = (
            (100 if metrics['mainnet']['presale_fiyat_artisi'] > 10 else 70) * 0.4 +
            (100 if metrics['mainnet']['max_staking_orani'] > 0.4 else 60) * 0.3 +
            (100 if (metrics['mainnet']['toplam_burned_token']/self.config.total_supply)*100 > 2 else 70) * 0.3
        ) * scenario_multiplier
        
        # Maturity achievement (20%)
        maturity_score = 0
        if metrics['mainnet']['maturity_damping_aktif']:
            progress = metrics['mainnet']['max_maturity_progress']
            if progress >= 100:
                maturity_score = 100
            elif progress >= 75:
                maturity_score = 85
            elif progress >= 50:
                maturity_score = 70
            elif progress >= 25:
                maturity_score = 55
            else:
                maturity_score = 40
        else:
            maturity_score = 50  # Neutral if disabled
        
        # Average user gains (20%)
        avg_user_score = 0
        if 'ortalama_kullanici_zirve_roi' in metrics['mainnet']:
            peak_roi = metrics['mainnet']['ortalama_kullanici_zirve_roi']
            final_roi = metrics['mainnet']['ortalama_kullanici_final_roi']
            
            if peak_roi >= 20:
                peak_score = 100
            elif peak_roi >= 10:
                peak_score = 90
            elif peak_roi >= 5:
                peak_score = 80
            elif peak_roi >= 2:
                peak_score = 60
            else:
                peak_score = 40
            
            sustain_ratio = final_roi / peak_roi if peak_roi > 0 else 0
            if sustain_ratio >= 0.8:
                sustain_score = 100
            elif sustain_ratio >= 0.6:
                sustain_score = 80
            elif sustain_ratio >= 0.4:
                sustain_score = 60
            else:
                sustain_score = 40
            
            avg_user_score = (peak_score * 0.7 + sustain_score * 0.3)
        
        # Dynamic staking effectiveness (10%)
        staking_score = 0
        max_staking = metrics['mainnet']['max_staking_orani']
        if max_staking >= 0.6:
            staking_score = 100
        elif max_staking >= 0.4:
            staking_score = 85
        elif max_staking >= 0.25:
            staking_score = 70
        else:
            staking_score = 50
        
        # System health (5%)
        health_score = 85  # Base  bonus for advanced features
        
        final_score = (presale_score * 0.20 + 
                      mainnet_score * 0.25 + 
                      maturity_score * 0.20 +
                      avg_user_score * 0.20 +
                      staking_score * 0.10 +
                      health_score * 0.05)
        
        return min(100, max(0, final_score))
    
    def display_final_performance_summary_v6(self, metrics: Dict, scenario: str):
        """🎯  Final Performance Summary """
        st.markdown('''
        <h3 style="color: #1B8EF2; margin: 2rem 0 1rem 0; font-family: Orbitron;">
            🎯  Performance Score  - Advanced Maturity + Dynamic Systems
        </h3>
        ''', unsafe_allow_html=True)
        
        _score = self.calculate_performance_score_v6(metrics, scenario)
        scenario_color = NXID_COLORS['danger'] if scenario == 'bear' else (
            NXID_COLORS['success'] if scenario == 'bull' else NXID_COLORS['primary']
        )
        
        #  final summary metrics
        summary_col1, summary_col2, summary_col3, summary_col4 = st.columns(4)
        
        with summary_col1:
            st.markdown(f"""
            **🔥 Simple Interest Presale Success:**
            - Raised: ${metrics['presale']['toplam_toplanan_usdt']/1e6:.1f}M USDT
            - Dynamic APY Avg: {metrics['presale']['ortalama_apy']:.1f}%
            - Interest System: {metrics['presale']['faiz_tipi']}
            - Pool Efficiency: {metrics['presale']['havuz_tukenme_yuzdesi']:.1f}%
            - Weekly Analysis: {metrics['haftalik_tokenlar']['toplam_hafta_sayisi']} weeks
            """)
        
        with summary_col2:
            st.markdown(f"""
            **🚀  Mainnet {scenario.upper()} Performance:**
            - Starting McAp: ${metrics['mainnet']['starting_mcap']/1e6:.1f}M
            - Peak Price: ${metrics['mainnet']['max_tahmin_fiyat']:.4f}
            - Peak ROI: {metrics['mainnet']['presale_fiyat_artisi']:.1f}x
            - Max Staking: {metrics['mainnet']['max_staking_orani']*100:.1f}%
            - Tax Collected: {metrics['mainnet']['toplam_tax_toplanan']/1e6:.1f}M
            """)
        
        with summary_col3:
            st.markdown(f"""
            **🎯 Advanced Maturity System :**
            - Target: ${metrics['mainnet']['maturity_target_mcap']/1e9:.1f}B
            - Max Progress: {metrics['mainnet']['max_maturity_progress']:.1f}%
            - Damping: {'✅ Active' if metrics['mainnet']['maturity_damping_aktif'] else '❌ Disabled'}
            - Convergence: {self.config.maturity_convergence_speed:.1%} speed
            - Effect Range: {self.config.maturity_damp_multiplier:.1f}x - {self.config.maturity_boost_multiplier:.1f}x
            """)
        
        with summary_col4:
            st.markdown(f"""
            **⚡ Dynamic Staking :**
            - Velocity Impact: {self.config.price_velocity_impact:.1f}
            - Staking Range: {self.config.min_staking_rate:.0%}-{self.config.max_staking_rate:.0%}
            - Exit Speed: {self.config.staking_exit_speed/self.config.staking_entry_speed:.1f}x entry
            - Real Circulating: ✅ Staked excluded
            - Burn Effect: {(metrics['mainnet']['toplam_burned_token']/self.config.total_supply)*100:.2f}%
            """)
        
        #  final assessment
        if _score >= 95:
            st.success(f"🏆 **PHENOMENAL  TOKENOMICS** - Score: {_score:.0f}/100 - {scenario.upper()} scenario perfectly optimized!")
        elif _score >= 90:
            st.success(f"🎉 **EXCELLENT  SYSTEM** - Score: {_score:.0f}/100 - Advanced features working brilliantly!")
        elif _score >= 80:
            st.info(f"✅ **GOOD  TOKENOMICS** - Score: {_score:.0f}/100 - Solid {scenario.upper()} + advanced foundations!")
        elif _score >= 70:
            st.warning(f"⚠️ **MODERATE  PERFORMANCE** - Score: {_score:.0f}/100 - {scenario.upper()} + maturity optimization needed")
        else:
            st.error(f"❌ ** NEEDS IMPROVEMENT** - Score: {_score:.0f}/100 - Review {scenario.upper()} + advanced parameters")
        
        st.markdown(f"<p style='color: {scenario_color}; font-weight: bold; text-align: center; font-size: 1.3rem;'>🎯  : Advanced Maturity + Dynamic Staking + Price Velocity + Real Supply - {scenario.upper()} scenario</p>", unsafe_allow_html=True)
        
        #  system summary
        st.info("""
        💡 ** NXID Tokenomics  Revolutionary Features:**
        • **Advanced Maturity Damping**: Market cap converges toward target automatically
        • **Price Velocity Staking**: Staking responds to price change speed (psychological realism)
        • **Real Circulating Supply**: Staked and burned tokens properly excluded from calculations
        • **Dynamic APY with Pool Release**: APY adjusts based on pool depletion, staking saturation, and market growth
        • ** Simple Interest**: Transparent, predictable, no compounding complexity
        • **Separate McAp Visualization**: Dedicated chart for market cap analysis with maturity target
        """)
    
    # Wrapper methods for backward compatibility
    def display_executive_dashboard_v4(self, metrics: Dict, scenario: str):
        """Wrapper for """
        self.display_executive_dashboard_v6(metrics, scenario)
    
    def display_comprehensive_analytics_report_v4(self, metrics: Dict, scenario: str):
        """Wrapper for """
        self.display_comprehensive_analytics_report_v6(metrics, scenario)
    
    def display_export_section_v4(self, results: Dict):
        """Wrapper for """
        self.display_export_section_v6(results)
    
    def display_final_performance_summary_v4(self, metrics: Dict, scenario: str):
        """Wrapper for """
        self.display_final_performance_summary_v6(metrics, scenario)