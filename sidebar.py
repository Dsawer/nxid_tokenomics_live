"""
NXID Enhanced Sidebar Management Module 
============================================
Enhanced: Detailed Controls + Examples + Advanced Maturity + Dynamic Staking + Real Circulating Supply
"""

import streamlit as st
import json
import os
from config import EnhancedNXIDConfig
from utils import display_nxid_logo, NXID_COLORS

class SidebarManager:
    """Enhanced Sidebar yönetim sınıfı  - Advanced Controls with Examples"""
    
    def __init__(self):
        self.config = None
        
    def render_sidebar(self) -> EnhancedNXIDConfig:
        """Enhanced Ana sidebar'ı render et """
        
        # Logo ve başlık
        self._render_sidebar_header()
        
        # JSON Config Management
        self._render_config_management()
        
        # Config yükleme veya yeni oluşturma
        if 'current_config' not in st.session_state:
            st.session_state.current_config = EnhancedNXIDConfig.load_from_json()
        
        config = st.session_state.current_config
        
        # === ENHANCED CONFIGURATION SECTIONS  ===
        
        # 1. Basic Analysis Settings + Starting McAp
        config = self._render_basic_analysis_settings(config)
        
        # 2. Token Distribution  
        config = self._render_token_distribution(config)
        
        # 3. Presale Configuration
        config = self._render_presale_configuration(config)
        
        # 4. Advanced Maturity Damping System
        config = self._render_advanced_maturity_damping(config)
        
        # 5. Enhanced Dynamic Staking System
        config = self._render_enhanced_dynamic_staking(config)
        
        # 6. Enhanced Dynamic APY System
        config = self._render_enhanced_dynamic_apy(config)
        
        # 7. Market Dynamics & Smoothing
        config = self._render_market_dynamics(config)
        
        # 8. Tax & Burn System
        config = self._render_tax_burn_system(config)
        
        # 9. Vesting Schedules
        config = self._render_vesting_schedules(config)
        
        # 10. Advanced System Settings
        config = self._render_advanced_system_settings(config)
        
        # Update session state
        st.session_state.current_config = config
        
        # Enhanced Validation 
        config_valid = (config.validate_distribution() and 
                       config.validate_tax_distribution() and
                       config.validate_enhanced_parameters())
        
        if config_valid:
            st.sidebar.success("Gelişmiş Yapılandırma Geçerli ")
        else:
            st.sidebar.error("Yapılandırma düzeltilmeli")
            
            # Validation detayları
            if not config.validate_distribution():
                st.sidebar.error("Token dağıtımı 100% değil")
            if not config.validate_tax_distribution():
                st.sidebar.error("Vergi dağıtımı 100% değil")
            if not config.validate_enhanced_parameters():
                st.sidebar.error("Gelişmiş parametreler geçersiz")
        
        return config, config_valid
    
    def _render_sidebar_header(self):
        """Enhanced Sidebar başlığını render et """
        sidebar_logo = display_nxid_logo(80)
        st.sidebar.markdown(f'''
        <div style="text-align: center; margin-bottom: 2rem;">
            {sidebar_logo}
            <h2 style="color: {NXID_COLORS['primary']}; font-family: Orbitron; font-size: 1.4rem; margin: 1rem 0 0 0;">
                Enhanced NXID 
            </h2>
            <p style="color: {NXID_COLORS['gray']}; font-size: 0.9rem; margin: 0.5rem 0 0 0;">
                Gelişmiş Maturity + Dinamik Sistemler<br>
                Gerçek Dolaşımdaki Arz + Fiyat Hızı
            </p>
        </div>
        ''', unsafe_allow_html=True)
    
    def _render_config_management(self):
        """Enhanced JSON Config yönetimi """
        with st.sidebar.expander("Gelişmiş Config Yönetimi ", expanded=False):
            st.markdown("**Gelişmiş Config Dosya İşlemleri :**")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Kaydet ", use_container_width=True, 
                        help="Tüm gelişmiş özelliklerle birlikte enhanced  yapılandırmasını JSON dosyasına kaydet."):
                    if 'current_config' in st.session_state:
                        if st.session_state.current_config.save_to_json():
                            st.success("Enhanced Config  kaydedildi!")
                        else:
                            st.error("Kaydetme hatası!")
                    else:
                        st.warning("Önce config oluştur")
            
            with col2:
                if st.button("Yükle ", use_container_width=True,
                        help="Önceden kaydedilmiş enhanced JSON config  dosyasını yükle. Tüm ayarlar geri yüklenecek."):
                    try:
                        loaded_config = EnhancedNXIDConfig.load_from_json()
                        st.session_state.current_config = loaded_config
                        st.success("Enhanced Config  yüklendi!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Yükleme hatası: {e}")
                        st.session_state.current_config = EnhancedNXIDConfig()
            
            # Config file status
            config_files = ["nxid_config_enhanced_v6.json", "nxid_config_enhanced_v5.json", "nxid_config.json"]
            config_found = False
            
            for config_file in config_files:
                if os.path.exists(config_file):
                    st.info(f"{config_file} mevcut")
                    config_found = True
                    break
            
            if not config_found:
                st.warning("Config dosyası bulunamadı -  varsayılanları kullanılıyor")
    
    def _render_basic_analysis_settings(self, config: EnhancedNXIDConfig) -> EnhancedNXIDConfig:
        """Temel Analiz Ayarları + Başlangıç McAp """
        with st.sidebar.expander("Temel Analiz Ayarları", expanded=True):
            
            st.markdown("### Başlangıç Market Cap (Kullanıcı Girişi)")
            config.starting_mcap_usdt = st.number_input(
                "Başlangıç McAp ($)", 
                min_value=1_000_000.0, 
                max_value=100_000_000.0, 
                value=config.starting_mcap_usdt, 
                step=500_000.0,
                help="""
                Başlangıç Market Cap :
                
                Ne yapar: Mainnet lansmanında başlangıç market cap değerini belirler.
                
                Örnekler:
                • 5,000,000$ = Muhafazakar lansman
                • 10,000,000$ = Güçlü lansman  
                • 20,000,000$ = Agresif lansman
                
                Nasıl çalışır:
                • Başlangıç token fiyatı = Başlangıç McAp ÷ Dolaşımdaki Arz
                • Maturity damping bunu temel referans olarak kullanır
                • Tüm büyüme hesaplamaları bu noktadan başlar
                
                Optimizasyon ipuçları:
                • Presale ile toplanan fonlarla uyumlu olmalı
                • Yüksek = yüksek başlangıç token fiyatı
                • Market koşullarını ve beklentileri dikkate alın
                """
            )
            
            st.markdown("### Analiz Zaman Çerçeveleri")
            config.projection_months = st.number_input(
                "Mainnet Projeksiyonu (ay)", 
                min_value=12, 
                max_value=60, 
                value=config.projection_months, 
                step=3,
                help="""
                Mainnet Projeksiyon Dönemi:
                
                Örnekler:
                • 24 ay = Kısa vadeli analiz
                • 36 ay = Orta vadeli analiz
                • 48 ay = Uzun vadeli analiz (önerilen)
                
                İçerir: Market dinamikleri, staking, vergi/yakma, maturity ilerlemesi
                """
            )
            
            config.vesting_analysis_months = st.number_input(
                "Vesting Analizi (ay)", 
                min_value=24, 
                max_value=120, 
                value=config.vesting_analysis_months, 
                step=6,
                help="""
                Vesting Analiz Dönemi:
                
                Örnekler:
                • 60 ay = Standart vesting takibi
                • 72 ay = Genişletilmiş vesting analizi
                • 96 ay = Tam yaşam döngüsü analizi
                
                Kapsar: Staking havuzları dahil tüm token açılış takvimi
                """
            )
            
            starting_millions = config.starting_mcap_usdt / 1_000_000
            st.success(f"Başlangıç McAp: ${starting_millions:.1f}M")
        
        return config
    
    def _render_token_distribution(self, config: EnhancedNXIDConfig) -> EnhancedNXIDConfig:
        """Token Dağıtım Ayarları"""
        with st.sidebar.expander("Token Dağıtımı", expanded=False):
            
            st.markdown("### Satış ve Staking Havuzları")
            config.presale_allocation = st.number_input(
                "Presale Tahsisi (%)", 
                min_value=0.0, 
                max_value=50.0, 
                value=config.presale_allocation, 
                step=0.5,
                help="""
                Presale Token Tahsisi:
                
                Örnekler:
                • %20 = Muhafazakar presale (20B token)
                • %26 = Standart presale (26B token)  
                • %35 = Agresif presale (35B token)
                
                Etki: Yüksek % = daha fazla başlangıç likidite ama daha fazla satış baskısı
                """
            )
            
            config.presale_staking_pool = st.number_input(
                "Presale Staking Havuzu (%)", 
                min_value=0.0, 
                max_value=10.0, 
                value=config.presale_staking_pool, 
                step=0.1,
                help="""
                Presale Staking Ödül Havuzu:
                
                Örnekler:
                • %3 = Muhafazakar ödüller (3B token)
                • %4 = Standart ödüller (4B token)
                • %6 = Cömert ödüller (6B token)
                
                Kullanım: Presale aşamasında basit faiz ödülleri
                """
            )
            
            config.market_staking_pool = st.number_input(
                "Market Staking Havuzu (%)", 
                min_value=10.0, 
                max_value=40.0, 
                value=config.market_staking_pool, 
                step=0.5,
                help="""
                Lansman Sonrası Staking Havuzu:
                
                Örnekler:
                • %20 = Temel staking ödülleri (20B token)
                • %25 = Standart staking ödülleri (25B token)
                • %30 = Cömert staking ödülleri (30B token)
                
                Süre: Dinamik APY ile birkaç yıl boyunca serbest bırakılır
                """
            )
            
            config.liquidity = st.number_input(
                "Likidite (%)", 
                min_value=3.0, 
                max_value=15.0, 
                value=config.liquidity, 
                step=0.5,
                help="""
                DEX Likidite Tahsisi:
                
                Örnekler:
                • %5 = Minimal likidite (5B token)
                • %7 = Standart likidite (7B token)
                • %10 = Yüksek likidite (10B token)
                
                Kullanım: DEX işlem çiftleri için anında kullanılabilir
                """
            )
            
            st.markdown("### Takım ve Organizasyon")
            config.team_allocation = st.number_input(
                "Takım Tahsisi (%)", 
                min_value=10.0, 
                max_value=25.0, 
                value=config.team_allocation, 
                step=0.5,
                help="""
                Geliştirme Takımı Tahsisi:
                
                Örnekler:
                • %12 = Sade takım tahsisi (12B token)
                • %15 = Standart takım tahsisi (15B token)
                • %20 = Cömert takım tahsisi (20B token)
                
                Vesting: Cliff ve doğrusal vesting programına tabidir
                """
            )
            
            config.dao_treasury = st.number_input(
                "DAO Hazinesi (%)", 
                min_value=10.0, 
                max_value=25.0, 
                value=config.dao_treasury, 
                step=0.5,
                help="""
                DAO Hazine Tahsisi:
                
                Örnekler:
                • %12 = Muhafazakar yönetişim (12B token)
                • %15 = Standart yönetişim (15B token) 
                • %20 = Güçlü yönetişim (20B token)
                
                Kullanım: Topluluk önerileri, ekosistem geliştirme, ortaklıklar
                """
            )
            
            config.marketing = st.number_input(
                "Pazarlama (%)", 
                min_value=5.0, 
                max_value=15.0, 
                value=config.marketing, 
                step=0.5,
                help="""
                Pazarlama ve Büyüme Tahsisi:
                
                Örnekler:
                • %6 = Muhafazakar pazarlama (6B token)
                • %8 = Standart pazarlama (8B token)
                • %12 = Agresif pazarlama (12B token)
                
                Kullanım: Kampanyalar, ortaklıklar, topluluk teşvikleri, airdroplar
                """
            )
            
            # Dağıtım doğrulama
            total_allocation = (config.presale_allocation + config.presale_staking_pool + 
                              config.market_staking_pool + config.team_allocation + 
                              config.dao_treasury + config.marketing + config.liquidity)
            
            if abs(total_allocation - 100) < 0.1:
                st.success(f"Mükemmel! Toplam: {total_allocation:.1f}%")
            else:
                st.error(f"Toplam: {total_allocation:.1f}% (100% olmalı)")
        
        return config
    
    def _render_presale_configuration(self, config: EnhancedNXIDConfig) -> EnhancedNXIDConfig:
        """Presale Yapılandırması"""
        with st.sidebar.expander("Presale Yapılandırması", expanded=False):
            
            st.markdown("### Temel Presale Ayarları")
            config.presale_days = st.number_input(
                "Presale Süresi (gün)", 
                min_value=30, 
                max_value=365, 
                value=config.presale_days,
                help="""
                Presale Süresi:
                
                Örnekler:
                • 90 gün = Kısa presale (3 ay)
                • 180 gün = Standart presale (6 ay)
                • 270 gün = Uzun presale (9 ay)
                
                Etki: Uzun süre = daha kademeli token dağıtımı
                """
            )
            
            config.start_price_usdt = st.number_input(
                "Başlangıç Fiyatı ($)", 
                min_value=0.0001, 
                max_value=0.01, 
                value=config.start_price_usdt, 
                step=0.0001, 
                format="%.4f",
                help="""
                İlk Token Fiyatı:
                
                Örnekler:
                • $0.0005 = Çok düşük giriş fiyatı
                • $0.001 = Standart giriş fiyatı  
                • $0.002 = Premium giriş fiyatı
                
                Strateji: Düşük fiyat = daha erişilebilir, yüksek büyüme potansiyeli
                """
            )
            
            config.daily_price_increase = st.number_input(
                "Günlük Fiyat Artışı (%)", 
                min_value=0.0, 
                max_value=0.2, 
                value=config.daily_price_increase, 
                step=0.01,
                help="""
                Günlük Fiyat Büyümesi:
                
                Örnekler:
                • %0.03 = Yavaş büyüme (yıllık ~%11)
                • %0.05 = Standart büyüme (yıllık ~%18)
                • %0.10 = Hızlı büyüme (yıllık ~%36)
                
                Etki: Aciliyet yaratır ve erken yatırımcıları ödüllendirir
                """
            )
            
            st.markdown("### Talep Modellemesi")
            config.base_daily_demand_usdt = st.number_input(
                "Temel Günlük Talep ($)", 
                min_value=500.0, 
                max_value=10000.0, 
                value=config.base_daily_demand_usdt, 
                step=100.0,
                help="""
                İlk Günlük Yatırım Hacmi:
                
                Örnekler:
                • $1,000 = Muhafazakar başlangıç
                • $2,000 = Standart başlangıç
                • $5,000 = Güçlü başlangıç
                
                Büyüme: Bu miktar talep büyüme oranına göre günlük artar
                """
            )
            
            config.demand_growth_rate = st.number_input(
                "Talep Büyüme Oranı (günlük çarpan)", 
                min_value=1.001, 
                max_value=1.05, 
                value=config.demand_growth_rate, 
                step=0.001,
                help="""
                Günlük Talep Büyümesi:
                
                Örnekler:
                • 1.005 = %0.5 günlük büyüme (çok güçlü)
                • 1.01 = %1 günlük büyüme (agresif)
                • 1.02 = %2 günlük büyüme (patlayıcı)
                
                Hesaplama: Günlük talep × büyüme oranı^gün
                """
            )
            
            config.demand_volatility = st.number_input(
                "Talep Volatilitesi", 
                min_value=0.01, 
                max_value=0.2, 
                value=config.demand_volatility, 
                step=0.01,
                help="""
                Günlük Talep Volatilitesi:
                
                Örnekler:
                • 0.03 = Düşük volatilite (±%3 günlük değişim)
                • 0.05 = Standart volatilite (±%5 günlük değişim)
                • 0.10 = Yüksek volatilite (±%10 günlük değişim)
                
                Etki: Gerçek dünya talep dalgalanmalarını simüle eder
                """
            )
            
            st.markdown("### Basit Faiz APY Sistemi")
            config.max_apy = st.number_input(
                "Maksimum APY (%)", 
                min_value=100.0, 
                max_value=10000.0, 
                value=config.max_apy, 
                step=50.0,
                help="""
                Maksimum APY Sınırı:
                
                Örnekler:
                • %1000 = Muhafazakar maksimum
                • %5000 = Standart maksimum ( varsayılan)
                • %8000 = Agresif maksimum
                
                Not: Basit faiz kullanır - bileşik faiz yoktur
                Dinamik: APY havuz kullanımını optimize etmek için ayarlanır
                """
            )
            
            config.minimum_staking_apy = st.number_input(
                "Minimum APY (%)", 
                min_value=10.0, 
                max_value=200.0, 
                value=config.minimum_staking_apy, 
                step=5.0,
                help="""
                Minimum APY Tabanı:
                
                Örnekler:
                • %30 = Muhafazakar minimum
                • %50 = Standart minimum
                • %100 = Cömert minimum
                
                Güvenlik: Havuz tükense bile çekici getiriler sağlar
                """
            )
            
            # Haftalık analiz
            config.weekly_analysis = st.checkbox(
                "Haftalık Analizi Etkinleştir", 
                value=config.weekly_analysis,
                help="""
                Haftalık Yatırım Analizi:
                
                Her hafta sabit miktar yatırım yapan yatırımcıyı simüle eder.
                Bileşik faiz olmadan basit faiz kazançlarını gösterir.
                DCA (Dollar Cost Averaging) strateji analizi için kullanışlıdır.
                """
            )
            
            if config.weekly_analysis:
                config.weekly_investment_amount = st.number_input(
                    "Haftalık Yatırım ($)", 
                    min_value=100.0, 
                    max_value=5000.0, 
                    value=config.weekly_investment_amount, 
                    step=50.0,
                    help="""
                    Sabit Haftalık Yatırım:
                    
                    Örnekler:
                    • $500 = Muhafazakar DCA
                    • $1000 = Standart DCA
                    • $2000 = Agresif DCA
                    
                    Analiz: Basit faiz ile token birikimini gösterir
                    """
                )
            
            # Presale etkisini göster
            days = config.presale_days
            final_price = config.start_price_usdt * ((1 + config.daily_price_increase/100) ** days)
            price_growth = ((final_price / config.start_price_usdt) - 1) * 100
            
            st.info(f"""
            Presale Fiyat Etkisi:
            • Son Fiyat: ${final_price:.4f}
            • Toplam Büyüme: {price_growth:.1f}%
            • Günlük Basit Faiz Sistemi
            """)
        
        return config
    
    def _render_advanced_maturity_damping(self, config: EnhancedNXIDConfig) -> EnhancedNXIDConfig:
        """Gelişmiş Maturity Damping Sistemi """
        with st.sidebar.expander("Gelişmiş Maturity Damping ", expanded=False):
            
            st.markdown("### Maturity Hedef Sistemi")
            config.enable_maturity_damping = st.checkbox(
                "Maturity Damping Etkinleştir", 
                value=config.enable_maturity_damping,
                help="""
                Gelişmiş Maturity Damping :
                
                Devrimci Özellik: Market cap otomatik olarak hedefe yakınsıyor.
                
                Nasıl çalışır:
                • Hedefin altında → Market cap BOOST alır (hızlandırılmış büyüme)
                • Hedefin üstünde → Market cap DAMP edilir (azaltılmış büyüme)
                • Hedef etrafında doğal fiyat istikrarı yaratır
                
                Gerçek dünya benzeri: Market cap için termostat gibi
                """
            )
            
            if config.enable_maturity_damping:
                config.maturity_target_mcap = st.number_input(
                    "Hedef Market Cap ($)", 
                    min_value=100_000_000.0, 
                    max_value=10_000_000_000.0, 
                    value=config.maturity_target_mcap, 
                    step=50_000_000.0,
                    help="""
                    Maturity Hedef Market Cap:
                    
                    Örnekler:
                    • $500M = Orta ölçekli hedef
                    • $1B = Büyük ölçekli hedef (unicorn)
                    • $5B = Mega ölçekli hedef
                    
                    Strateji: Toplam adreslenebilir pazar ve hedeflere göre belirleyin
                    Etki: Sistem market cap'i bu değere doğru itecek
                    """
                )
                
                config.maturity_damping_strength = st.number_input(
                    "Damping Gücü", 
                    min_value=0.1, 
                    max_value=1.0, 
                    value=config.maturity_damping_strength, 
                    step=0.05,
                    help="""
                    Damping Kuvvet Gücü:
                    
                    Örnekler:
                    • 0.2 = Nazik damping (ince düzeltmeler)
                    • 0.4 = Standart damping (dengeli yaklaşım)
                    • 0.8 = Güçlü damping (agresif düzeltmeler)
                    
                    Yüksek değerler = güçlü yakınsama kuvveti
                    Düşük değerler = daha doğal market davranışı
                    """
                )
                
                config.maturity_convergence_speed = st.number_input(
                    "Yakınsama Hızı", 
                    min_value=0.05, 
                    max_value=0.5, 
                    value=config.maturity_convergence_speed, 
                    step=0.01,
                    help="""
                    Yakınsama Hızı:
                    
                    Örnekler:
                    • 0.10 = Yavaş yakınsama (kademeli ayar)
                    • 0.15 = Standart hız (dengeli)
                    • 0.25 = Hızlı yakınsama (hızlı düzeltmeler)
                    
                    Yüksek = hedefe doğru daha hızlı düzeltmeler
                    Düşük = daha yumuşak, uzun vadeli ayarlamalar
                    """
                )
                
                config.maturity_boost_multiplier = st.number_input(
                    "Boost Çarpanı (hedefin altında)", 
                    min_value=1.1, 
                    max_value=3.0, 
                    value=config.maturity_boost_multiplier, 
                    step=0.1,
                    help="""
                    Boost Etkisi (Hedefin Altında):
                    
                    Örnekler:
                    • 1.3 = Nazik boost (hedefin çok altındayken +%30 büyüme)
                    • 1.8 = Standart boost (hedefin çok altındayken +%80 büyüme)
                    • 2.5 = Güçlü boost (hedefin çok altındayken +%150 büyüme)
                    
                    Etki: Market cap hedefin altındayken büyüme boost alır
                    Uzaklık önemli: Daha uzakta = daha güçlü boost
                    """
                )
                
                config.maturity_damp_multiplier = st.number_input(
                    "Damp Çarpanı (hedefin üstünde)", 
                    min_value=0.3, 
                    max_value=0.9, 
                    value=config.maturity_damp_multiplier, 
                    step=0.05,
                    help="""
                    Damp Etkisi (Hedefin Üstünde):
                    
                    Örnekler:
                    • 0.7 = Nazik damping (normal büyümenin %70'i)
                    • 0.6 = Standart damping (normal büyümenin %60'ı)
                    • 0.4 = Güçlü damping (normal büyümenin %40'ı)
                    
                    Etki: Market cap hedefin üstündeyken büyüme azalır
                    Uzaklık önemli: Daha uzakta = daha güçlü damping
                    """
                )
                
                # Maturity etkisini göster
                target_billions = config.maturity_target_mcap / 1_000_000_000
                starting_millions = config.starting_mcap_usdt / 1_000_000
                target_ratio = config.maturity_target_mcap / config.starting_mcap_usdt
                
                st.success(f"""
                Maturity Sistemi Aktif:
                • Hedef: ${target_billions:.1f}B
                • Başlangıç: ${starting_millions:.1f}M
                • Gerekli büyüme: {target_ratio:.0f}x
                • Damping: {config.maturity_damping_strength:.1%} güç
                • Yakınsama: {config.maturity_convergence_speed:.1%} hız
                """)
            else:
                st.warning("Maturity damping devre dışı - saf market senaryoları")
        
        return config
    
    def _render_enhanced_dynamic_staking(self, config: EnhancedNXIDConfig) -> EnhancedNXIDConfig:
        """Gelişmiş Dinamik Staking Sistemi """
        with st.sidebar.expander("Gelişmiş Dinamik Staking ", expanded=False):
            
            st.markdown("### Staking Katılım Aralığı")
            config.min_staking_rate = st.number_input(
                "Minimum Staking Oranı", 
                min_value=0.05, 
                max_value=0.5, 
                value=config.min_staking_rate, 
                step=0.01,
                help="""
                Minimum Staking Katılımı:
                
                Örnekler:
                • 0.10 = %10 minimum (boğa piyasalarında bile)
                • 0.15 = %15 minimum (standart taban)
                • 0.25 = %25 minimum (yüksek taban)
                
                Kullanım: Fiyat artışları sırasında staking'in çok düşmesini önler
                Psikoloji: Bazı kullanıcılar her zaman staking ödüllerini spekulasyona tercih eder
                """
            )
            
            config.base_staking_rate = st.number_input(
                "Temel Staking Oranı", 
                min_value=config.min_staking_rate, 
                max_value=0.8, 
                value=config.base_staking_rate, 
                step=0.01,
                help="""
                Nötr Staking Katılımı:
                
                Örnekler:
                • 0.35 = %35 temel oran (muhafazakar)
                • 0.45 = %45 temel oran (standart)
                • 0.60 = %60 temel oran (yüksek taban)
                
                Bağlam: Fiyat hızı nötr olduğunda normal staking oranı
                Dalgalanmalar: Gerçek oran fiyat hareketlerine göre değişir
                """
            )
            
            config.max_staking_rate = st.number_input(
                "Maksimum Staking Oranı", 
                min_value=config.base_staking_rate, 
                max_value=0.95, 
                value=config.max_staking_rate, 
                step=0.01,
                help="""
                Maksimum Staking Katılımı:
                
                Örnekler:
                • 0.65 = %65 maksimum (muhafazakar sınır)
                • 0.75 = %75 maksimum (standart sınır)
                • 0.90 = %90 maksimum (agresif sınır)
                
                Sınır: Likiditeye zarar verebilecek aşırı staking'i önler
                Ayı piyasaları: Düşüş dönemlerinde staking bu seviyeye yaklaşır
                """
            )
            
            st.markdown("### Fiyat Hızı Etki Sistemi")
            config.price_velocity_impact = st.number_input(
                "Fiyat Hızı Etkisi", 
                min_value=-1.0, 
                max_value=0.0, 
                value=config.price_velocity_impact, 
                step=0.05,
                help="""
                Fiyat Hızı Hassasiyeti:
                
                Devrimci Özellik: Staking fiyat değişim hızına tepki veriyor!
                
                Örnekler:
                • -0.3 = Nazik tepki (%100 fiyat hızı başına %30 staking azalması)
                • -0.6 = Standart tepki (%60 azalma)
                • -0.9 = Güçlü tepki (%90 azalma)
                
                Gerçek davranış: Hızlı fiyat artışları → insanlar unstake yapar satmak için
                Hızlı fiyat düşüşleri → insanlar stake yapar güvenlik/ödüller için
                """
            )
            
            config.price_velocity_window = st.number_input(
                "Fiyat Hızı Penceresi (gün)", 
                min_value=3, 
                max_value=30, 
                value=config.price_velocity_window, 
                step=1,
                help="""
                Fiyat Hızı Hesaplama Penceresi:
                
                Örnekler:
                • 5 gün = Kısa vadeli hareketlere çok duyarlı
                • 7 gün = Haftalık hız (standart)
                • 14 gün = İki haftalık hız (daha yumuşak)
                
                Daha kısa = fiyat değişikliklerine daha reaktif
                Daha uzun = daha yumuşak, daha az değişken staking davranışı
                """
            )
            
            config.price_velocity_smoothing = st.number_input(
                "Fiyat Hızı Yumuşatma", 
                min_value=0.1, 
                max_value=0.8, 
                value=config.price_velocity_smoothing, 
                step=0.05,
                help="""
                Fiyat Hızı Yumuşatma Faktörü:
                
                Örnekler:
                • 0.2 = Hafif yumuşatma (daha reaktif)
                • 0.3 = Standart yumuşatma (dengeli)
                • 0.5 = Ağır yumuşatma (çok istikrarlı)
                
                Etki: Fiyat sıçramalarından ani staking değişikliklerini önler
                Yüksek = daha yumuşak staking geçişleri
                """
            )
            
            st.markdown("### Staking Dinamikleri")
            config.staking_momentum = st.number_input(
                "Staking Momentum", 
                min_value=0.5, 
                max_value=0.95, 
                value=config.staking_momentum, 
                step=0.05,
                help="""
                Staking Değişim Momentum:
                
                Örnekler:
                • 0.70 = Hızlı ayarlamalar (%30 yeni, %70 önceki)
                • 0.85 = Standart momentum (%15 yeni, %85 önceki)
                • 0.95 = Yavaş ayarlamalar (%5 yeni, %95 önceki)
                
                Gerçek davranış: İnsanlar staking kararlarını anında değiştirmez
                Yüksek = daha kademeli, gerçekçi staking değişiklikleri
                """
            )
            
            config.staking_entry_speed = st.number_input(
                "Staking Giriş Hızı", 
                min_value=0.001, 
                max_value=0.01, 
                value=config.staking_entry_speed, 
                step=0.0005,
                help="""
                Yeni Staking Giriş Oranı:
                
                Örnekler:
                • 0.001 = Yavaş giriş (günlük mevcut tokenların %0.1'i)
                • 0.002 = Standart giriş (günlük %0.2)
                • 0.005 = Hızlı giriş (günlük %0.5)
                
                Süreç: Kullanıcıların tokenları staking'e taşıma hızı
                Gerçekçi: İnsanlar kademeli olarak stake yapar, hepsini birden değil
                """
            )
            
            config.staking_exit_speed = st.number_input(
                "Staking Çıkış Hızı", 
                min_value=0.002, 
                max_value=0.02, 
                value=config.staking_exit_speed, 
                step=0.001,
                help="""
                Staking Çıkış Oranı:
                
                Örnekler:
                • 0.003 = Yavaş çıkış (günlük fazlanın %0.3'ü)
                • 0.005 = Standart çıkış (günlük %0.5)
                • 0.010 = Hızlı çıkış (günlük %1.0)
                
                Psikolojik: İnsanlar stake etmekten daha hızlı unstake yapar
                FOMO/Açgözlülük: Fiyat artışında unstake etmek için hızlı davranırlar
                """
            )
            
            # Staking aralığını göster
            staking_range = f"{config.min_staking_rate:.0%} - {config.max_staking_rate:.0%}"
            velocity_strength = abs(config.price_velocity_impact)
            
            st.success(f"""
            Dinamik Staking Aktif:
            • Aralık: {staking_range}
            • Temel: {config.base_staking_rate:.0%}
            • Hız Etkisi: {velocity_strength:.0%}
            • Pencere: {config.price_velocity_window} gün
            • Giriş/Çıkış: {config.staking_entry_speed:.1%}/{config.staking_exit_speed:.1%}
            """)
        
        return config
    
    def _render_enhanced_dynamic_apy(self, config: EnhancedNXIDConfig) -> EnhancedNXIDConfig:
        """Gelişmiş Dinamik APY Sistemi """
        with st.sidebar.expander("Gelişmiş Dinamik APY ", expanded=False):
            
            st.markdown("### APY Aralık Yapılandırması")
            config.min_staking_apy = st.number_input(
                "Minimum Staking APY (%)", 
                min_value=5.0, 
                max_value=50.0, 
                value=config.min_staking_apy, 
                step=1.0,
                help="""
                Minimum APY Tabanı:
                
                Örnekler:
                • %10 = Çok muhafazakar taban
                • %15 = Standart minimum ( varsayılan)
                • %25 = Cömert minimum
                
                Bağlam: Staking havuzu tükense bile kullanıcılar bu APY'yi alır
                Amaç: Uzun vadeli staking çekiciliğini korur
                """
            )
            
            config.base_staking_apy = st.number_input(
                "Temel Staking APY (%)", 
                min_value=config.min_staking_apy, 
                max_value=150.0, 
                value=config.base_staking_apy, 
                step=5.0,
                help="""
                Temel Staking APY:
                
                Örnekler:
                • %60 = Muhafazakar temel oran
                • %85 = Standart temel oran ( varsayılan)
                • %120 = Agresif temel oran
                
                Bağlam: Standart koşullar altında normal APY
                Dalgalanır: Havuz tükenmesi, staking doygunluğu, market talebi bazında
                """
            )
            
            config.max_staking_apy = st.number_input(
                "Maksimum Staking APY (%)", 
                min_value=config.base_staking_apy, 
                max_value=500.0, 
                value=config.max_staking_apy, 
                step=10.0,
                help="""
                Maksimum APY Tavanı:
                
                Örnekler:
                • %150 = Muhafazakar tavan
                • %250 = Standart tavan ( varsayılan)
                • %400 = Agresif tavan
                
                Güvenlik: Sürdürülemez APY seviyelerini önler
                Erken dönemler: Az kişi stake ettiğinde APY bu seviyeye ulaşabilir
                """
            )
            
            st.markdown("### APY Hesaplama Faktörleri")
            config.staking_pool_duration_years = st.number_input(
                "Staking Havuzu Süresi (yıl)", 
                min_value=3, 
                max_value=15, 
                value=config.staking_pool_duration_years, 
                step=1,
                help="""
                Staking Havuzu Serbest Bırakma Süresi:
                
                Örnekler:
                • 5 yıl = Daha hızlı tükenme, yüksek erken APY
                • 8 yıl = Standart süre ( varsayılan)
                • 12 yıl = Daha yavaş tükenme, daha istikrarlı APY
                
                Etki: Uzun süre = daha istikrarlı, düşük ortalama APY
                Kısa süre = yüksek erken APY, hızlı düşüş
                """
            )
            
            config.pool_depletion_apy_factor = st.number_input(
                "Havuz Tükenme APY Faktörü", 
                min_value=0.3, 
                max_value=1.5, 
                value=config.pool_depletion_apy_factor, 
                step=0.05,
                help="""
                Havuz Tükenmesinin APY'ye Etkisi:
                
                Örnekler:
                • 0.5 = Orta etki (havuz %50 tükendiğinde %50 APY artışı)
                • 0.8 = Standart etki (%80 artış) ( varsayılan)
                • 1.2 = Güçlü etki (%120 artış)
                
                Mantık: Havuz tükendikçe APY artar (kıtlık etkisi)
                Erken staking için teşvik yaratır
                """
            )
            
            config.staking_saturation_factor = st.number_input(
                "Staking Doygunluk Faktörü", 
                min_value=0.2, 
                max_value=1.0, 
                value=config.staking_saturation_factor, 
                step=0.05,
                help="""
                Staking Doygunluk Etkisi:
                
                Örnekler:
                • 0.4 = Orta etki (%100 staking'de %40 APY düşüşü)
                • 0.6 = Standart etki (%60 düşüş) ( varsayılan)
                • 0.8 = Güçlü etki (%80 düşüş)
                
                Ekonomik mantık: Yüksek staking katılımı = düşük APY
                Arz/talep: Daha fazla staker = staker başına daha az ödül
                """
            )
            
            config.market_demand_apy_factor = st.number_input(
                "Market Talep APY Faktörü", 
                min_value=0.1, 
                max_value=0.8, 
                value=config.market_demand_apy_factor, 
                step=0.05,
                help="""
                Market Büyümesinin APY'ye Etkisi:
                
                Örnekler:
                • 0.2 = Düşük korelasyon (%100 market büyümesi için %20 APY artışı)
                • 0.3 = Standart korelasyon (%30 artış) ( varsayılan)
                • 0.5 = Yüksek korelasyon (%50 artış)
                
                İnovasyon: Güçlü market performansı APY'yi hafifçe artırır
                Boğa piyasalarında daha fazla staker çeker
                """
            )
            
            # APY dinamikleri önizlemesi
            apy_range = f"{config.min_staking_apy:.0f}% - {config.max_staking_apy:.0f}%"
            duration = config.staking_pool_duration_years
            
            st.success(f"""
            Dinamik APY Sistemi:
            • Aralık: {apy_range}
            • Temel: {config.base_staking_apy:.0f}%
            • Süre: {duration} yıl
            • Havuz Faktörü: {config.pool_depletion_apy_factor:.1f}
            • Doygunluk Faktörü: {config.staking_saturation_factor:.1f}
            """)
        
        return config
    
    def _render_market_dynamics(self, config: EnhancedNXIDConfig) -> EnhancedNXIDConfig:
        """Market Dinamikleri ve Yumuşatma"""
        with st.sidebar.expander("Market Dinamikleri ve Yumuşatma", expanded=False):
            
            st.markdown("### Temel Market Parametreleri")
            config.market_volatility = st.number_input(
                "Market Volatilitesi", 
                min_value=0.02, 
                max_value=0.3, 
                value=config.market_volatility, 
                step=0.01,
                help="""
                Günlük Market Volatilitesi:
                
                Örnekler:
                • 0.05 = Düşük volatilite (±%5 günlük salınım)
                • 0.08 = Standart volatilite (±%8 salınım)
                • 0.15 = Yüksek volatilite (±%15 salınım)
                
                Bağlam: Damping uygulanmadan önceki temel seviye
                Gerçek kripto: Yerleşik tokenlar için %8-15 tipiktir
                """
            )
            
            config.market_beta = st.number_input(
                "Market Beta", 
                min_value=0.5, 
                max_value=2.0, 
                value=config.market_beta, 
                step=0.1,
                help="""
                Market Beta (kripto piyasasına karşı):
                
                Örnekler:
                • 0.8 = Piyasadan daha az değişken (savunma)
                • 1.1 = Standart korelasyon ( varsayılan)
                • 1.5 = Piyasadan daha değişken (agresif)
                
                Hisse senetleri gibi: Beta > 1 = daha değişken, Beta < 1 = daha az değişken
                """
            )
            
            config.speculative_ratio = st.number_input(
                "Spekülatif Oran", 
                min_value=0.3, 
                max_value=0.9, 
                value=config.speculative_ratio, 
                step=0.05,
                help="""
                Spekülasyon vs Temeller:
                
                Örnekler:
                • 0.4 = Çoğunlukla temel (%40 spekülasyon)
                • 0.6 = Dengeli (%60 spekülasyon) ( varsayılan)
                • 0.8 = Çoğunlukla spekülatif (%80 spekülasyon)
                
                Etki: Yüksek = daha değişken, senaryoya bağımlı büyüme
                Düşük = daha istikrarlı, temel tabanlı büyüme
                """
            )
            
            config.fundamental_growth_rate = st.number_input(
                "Aylık Temel Büyüme", 
                min_value=0.005, 
                max_value=0.05, 
                value=config.fundamental_growth_rate, 
                step=0.002,
                help="""
                Aylık Temel Büyüme:
                
                Örnekler:
                • 0.01 = %1 aylık (%12.7 yıllık)
                • 0.015 = %1.5 aylık (%19.6 yıllık) ( varsayılan)
                • 0.025 = %2.5 aylık (%34.5 yıllık)
                
                Temsil eder: Gerçek fayda, benimsenme, değer yaratımı
                Bağımsız: Spekülasyon veya senaryolardan etkilenmez
                """
            )
            
            st.markdown("### Yumuşatma Parametreleri")
            config.price_smoothing_factor = st.number_input(
                "Fiyat Yumuşatma Faktörü", 
                min_value=0.05, 
                max_value=0.5, 
                value=config.price_smoothing_factor, 
                step=0.01,
                help="""
                Fiyat Hareket Yumuşatması:
                
                Örnekler:
                • 0.10 = Hafif yumuşatma (%10 yeni, %90 önceki)
                • 0.15 = Standart yumuşatma ( varsayılan)
                • 0.25 = Ağır yumuşatma (%25 yeni, %75 önceki)
                
                Etki: Aşırı fiyat sıçramalarını önler
                Yüksek = daha yumuşak fiyat hareketleri
                """
            )
            
            config.mcap_smoothing_factor = st.number_input(
                "Market Cap Yumuşatma Faktörü", 
                min_value=0.05, 
                max_value=0.5, 
                value=config.mcap_smoothing_factor, 
                step=0.01,
                help="""
                Market Cap Yumuşatması:
                
                Örnekler:
                • 0.08 = Hafif yumuşatma
                • 0.12 = Standart yumuşatma ( varsayılan)
                • 0.20 = Ağır yumuşatma
                
                Amaç: Gerçekçi market cap geçişleri yaratır
                Önler: Ani market cap sıçramaları/çöküşleri
                """
            )
            
            config.volatility_damping = st.number_input(
                "Volatilite Damping", 
                min_value=0.3, 
                max_value=1.0, 
                value=config.volatility_damping, 
                step=0.05,
                help="""
                Volatilite Azaltma Faktörü:
                
                Örnekler:
                • 0.5 = Ağır damping (orijinal volatilitenin %50'si)
                • 0.7 = Standart damping (%70 korunur) ( varsayılan)
                • 0.9 = Hafif damping (%90 korunur)
                
                Yaratır: Daha gerçekçi, daha az aşırı fiyat hareketleri
                Profesyonel: Gerçek projelerin doğal dengeleyici kuvvetleri vardır
                """
            )
            
            # Market dinamikleri özeti
            annual_fundamental = ((1 + config.fundamental_growth_rate) ** 12 - 1) * 100
            effective_volatility = config.market_volatility * config.volatility_damping
            
            st.success(f"""
            Market Dinamikleri:
            • Volatilite: {effective_volatility:.1%} (damplenmiş)
            • Beta: {config.market_beta:.1f}
            • Spekülasyon: {config.speculative_ratio:.0%}
            • Temel: {annual_fundamental:.1f}% yıllık
            • Fiyat Yumuşatma: {config.price_smoothing_factor:.0%}
            """)
        
        return config
    
    def _render_tax_burn_system(self, config: EnhancedNXIDConfig) -> EnhancedNXIDConfig:
        """Vergi ve Yakma Sistemi"""
        with st.sidebar.expander("Vergi ve Yakma Sistemi", expanded=False):
            
            st.markdown("### Mainnet Vergi Sistemi")
            config.mainnet_tax_period_months = st.number_input(
                "Vergi Dönemi (ay)", 
                min_value=3, 
                max_value=24, 
                value=config.mainnet_tax_period_months, 
                step=1,
                help="""
                Mainnet Vergi Süresi:
                
                Örnekler:
                • 6 ay = Kısa vergi dönemi (erken likidite)
                • 12 ay = Standart dönem (dengeli)
                • 18 ay = Uzun dönem (daha fazla ödül/yakma)
                
                Amaç: Staking ödüllerini ve yakmaları başlatmak için başlangıç dönemi
                Dönem sonrası: Vergi sistemi otomatik olarak devre dışı kalır
                """
            )
            
            config.mainnet_tax_rate = st.number_input(
                "Vergi Oranı (%)", 
                min_value=1.0, 
                max_value=10.0, 
                value=config.mainnet_tax_rate, 
                step=0.5,
                help="""
                İşlem Hacmi Vergi Oranı:
                
                Örnekler:
                • %2 = Hafif vergi (işlem hacminin %2'si)
                • %3 = Standart vergi ( varsayılan)
                • %5 = Ağır vergi (önemli etki)
                
                Uygulandığı: Günlük işlem hacmi
                Toplanan: NXID tokenları (hacimden dönüştürülmüş)
                """
            )
            
            config.tax_to_staking_percentage = st.number_input(
                "Staking'e Vergi (%)", 
                min_value=40.0, 
                max_value=80.0, 
                value=config.tax_to_staking_percentage, 
                step=5.0,
                help="""
                Staking'e Vergi Tahsisi:
                
                Örnekler:
                • %50 = Dengeli tahsis
                • %60 = Standart tahsis ( varsayılan)
                • %70 = Yüksek staking artışı
                
                Etki: Staking havuzunu artırır, APY'yi yükseltir
                Staker'lara doğrudan fayda sağlar
                """
            )
            
            config.tax_to_burn_percentage = st.number_input(
                "Yakma'ya Vergi (%)", 
                min_value=20.0, 
                max_value=60.0, 
                value=config.tax_to_burn_percentage, 
                step=5.0,
                help="""
                Yakma'ya Vergi Tahsisi:
                
                Örnekler:
                • %30 = Düşük yakma oranı
                • %40 = Standart yakma ( varsayılan)
                • %50 = Yüksek yakma oranı
                
                Etki: Tokenları kalıcı olarak arzdan çıkarır
                Deflasyonist: Zaman içinde toplam arzı azaltır
                """
            )
            
            st.markdown("### Yakma Mekanizması")
            config.annual_burn_rate = st.number_input(
                "Yıllık Yakma Oranı", 
                min_value=0.01, 
                max_value=0.1, 
                value=config.annual_burn_rate, 
                step=0.005,
                help="""
                Yıllık Rutin Yakma Oranı:
                
                Örnekler:
                • 0.015 = Yıllık %1.5 (10 yılda 15B token)
                • 0.02 = Yıllık %2 (20B token) ( varsayılan)
                • 0.03 = Yıllık %3 (30B token)
                
                Bağımsız: Vergi yakmalarından ayrı
                Otomatik: İşlem aktivitesine bakılmaksızın gerçekleşir
                """
            )
            
            config.burn_duration_years = st.number_input(
                "Yakma Süresi (yıl)", 
                min_value=2, 
                max_value=10, 
                value=config.burn_duration_years, 
                step=1,
                help="""
                Rutin Yakma Süresi:
                
                Örnekler:
                • 3 yıl = Kısa yakma dönemi ( varsayılan)
                • 5 yıl = Standart dönem
                • 8 yıl = Uzun yakma dönemi
                
                Dönem sonrası: Rutin yakmalar durur (vergi yakmaları devam edebilir)
                Toplam yakılan: Yıllık oran × Süre × Toplam arz
                """
            )
            
            # Vergi dağıtım doğrulaması
            tax_total = config.tax_to_staking_percentage + config.tax_to_burn_percentage
            if abs(tax_total - 100) < 0.1:
                st.success(f"Vergi Dağıtımı: {tax_total:.1f}%")
            else:
                st.error(f"Vergi Dağıtımı: {tax_total:.1f}% (100% olmalı)")
            
            # Yakma etkisini göster
            total_routine_burn = config.annual_burn_rate * config.burn_duration_years * 100  # Toplam arzın yüzdesi
            
            st.info(f"""
            Yakma Etkisi Önizlemesi:
            • Vergi Dönemi: {config.mainnet_tax_period_months} ay
            • Vergi Oranı: %{config.mainnet_tax_rate}
            • Rutin Yakma: {config.burn_duration_years} yılda arzın %{total_routine_burn:.1f}'i
            • Bölünme: %{config.tax_to_staking_percentage:.0f} staking, %{config.tax_to_burn_percentage:.0f} yakma
            """)
        
        return config
    
    def _render_vesting_schedules(self, config: EnhancedNXIDConfig) -> EnhancedNXIDConfig:
        """Vesting Programları"""
        with st.sidebar.expander("Vesting Programları", expanded=False):
            
            st.markdown("### Staking Havuz Vesting")
            st.info("**Not:** Presale staking havuzu anında serbest bırakılır (0 cliff, 1 ay vesting)")
            
            config.market_staking_cliff_months = st.number_input(
                "Market Staking Cliff (ay)", 
                min_value=3, 
                max_value=24, 
                value=config.market_staking_cliff_months, 
                step=1,
                help="""
                Market Staking Havuzu Cliff:
                
                Örnekler:
                • 6 ay = Standart cliff ( varsayılan)
                • 12 ay = Muhafazakar cliff
                • 18 ay = Uzun cliff
                
                Etki: Market staking havuzu bu süre boyunca kilitli kalır
                Cliff sonrası: Vesting dönemi boyunca doğrusal serbest bırakma başlar
                """
            )
            
            config.market_staking_vesting_months = st.number_input(
                "Market Staking Vesting (ay)", 
                min_value=12, 
                max_value=60, 
                value=config.market_staking_vesting_months, 
                step=3,
                help="""
                Market Staking Havuzu Vesting:
                
                Örnekler:
                • 18 ay = Hızlı serbest bırakma
                • 24 ay = Standart serbest bırakma ( varsayılan)
                • 36 ay = Yavaş serbest bırakma
                
                Süreç: Cliff döneminden sonra doğrusal serbest bırakma
                Toplam süre: Cliff + Vesting = tam serbest bırakma süresi
                """
            )
            
            st.markdown("### Takım ve Organizasyon Vesting")
            config.team_cliff_months = st.number_input(
                "Takım Cliff (ay)", 
                min_value=6, 
                max_value=24, 
                value=config.team_cliff_months, 
                step=3,
                help="""
                Takım Token Cliff:
                
                Örnekler:
                • 12 ay = Standart cliff (bağlılık gösterir)
                • 18 ay = Uzun cliff (güçlü bağlılık)
                • 24 ay = Maksimum cliff (ultra muhafazakar)
                
                Amaç: Kritik erken dönemde takım bağlılığını sağlar
                """
            )
            
            config.team_vesting_months = st.number_input(
                "Takım Vesting (ay)", 
                min_value=24, 
                max_value=48, 
                value=config.team_vesting_months, 
                step=6,
                help="""
                Takım Vesting Süresi:
                
                Örnekler:
                • 24 ay = Hızlı vesting (2 yıl)
                • 36 ay = Standart vesting (3 yıl)
                • 48 ay = Uzun vesting (4 yıl)
                
                Endüstri standardı: Toplam 3-4 yıl (cliff dahil)
                """
            )
            
            config.dao_cliff_months = st.number_input(
                "DAO Cliff (ay)", 
                min_value=3, 
                max_value=18, 
                value=config.dao_cliff_months, 
                step=3,
                help="""
                DAO Hazine Cliff:
                
                Örnekler:
                • 6 ay = Hızlı DAO aktivasyonu
                • 12 ay = Standart aktivasyon
                • 18 ay = Gecikmiş aktivasyon
                
                Strateji: DAO yönetişiminin olgunlaşması için zaman
                """
            )
            
            config.dao_vesting_months = st.number_input(
                "DAO Vesting (ay)", 
                min_value=18, 
                max_value=48, 
                value=config.dao_vesting_months, 
                step=6,
                help="""
                DAO Hazine Vesting:
                
                Örnekler:
                • 24 ay = Hızlı yönetişim fonlaması
                • 30 ay = Standart fonlama
                • 36 ay = Muhafazakar fonlama
                
                Amaç: Ekosistem geliştirme için kademeli fonlama
                """
            )
            
            config.marketing_cliff_months = st.number_input(
                "Pazarlama Cliff (ay)", 
                min_value=0, 
                max_value=12, 
                value=config.marketing_cliff_months, 
                step=3,
                help="""
                Pazarlama Tahsis Cliff:
                
                Örnekler:
                • 0 ay = Anında kullanılabilirlik
                • 3 ay = Kısa gecikme  
                • 6 ay = Standart gecikme
                
                Gerekçe: Pazarlama genellikle lansmanında hemen gereklidir
                """
            )
            
            config.marketing_vesting_months = st.number_input(
                "Pazarlama Vesting (ay)", 
                min_value=6, 
                max_value=24, 
                value=config.marketing_vesting_months, 
                step=3,
                help="""
                Pazarlama Vesting Süresi:
                
                Örnekler:
                • 12 ay = Hızlı pazarlama harcaması
                • 18 ay = Dengeli yaklaşım
                • 24 ay = Muhafazakar yaklaşım
                
                Strateji: Sürdürülen büyüme için pazarlama bütçesini zamana yay
                """
            )
            
            # Vesting özeti
            total_team_time = config.team_cliff_months + config.team_vesting_months
            total_dao_time = config.dao_cliff_months + config.dao_vesting_months
            total_marketing_time = config.marketing_cliff_months + config.marketing_vesting_months
            total_market_staking_time = config.market_staking_cliff_months + config.market_staking_vesting_months
            
            st.success(f"""
            Vesting Zaman Çizelgesi Özeti:
            • Takım: {total_team_time} ay toplam
            • DAO: {total_dao_time} ay toplam
            • Pazarlama: {total_marketing_time} ay toplam
            • Market Staking: {total_market_staking_time} ay toplam
            • Presale ve Likidite: Anında
            """)
        
        return config
    
    def _render_advanced_system_settings(self, config: EnhancedNXIDConfig) -> EnhancedNXIDConfig:
        """Gelişmiş Sistem Ayarları"""
        with st.sidebar.expander("Gelişmiş Sistem Ayarları", expanded=False):
            
            st.markdown("### Dolaşımdaki Arz Hesaplama")
            config.include_staked_in_circulating = st.checkbox(
                "Stake Edilmiş Tokenları Dolaşımdaki Arza Dahil Et", 
                value=config.include_staked_in_circulating,
                help="""
                Dolaşımdaki Arz Tanımı:
                
                İşaretlenmemiş (Varsayılan): Stake edilmiş tokenlar dolaşımdaki arzdan hariç
                • Daha gerçekçi fiyat hesaplaması
                • Daha yüksek token fiyatları (daha küçük etkili arz)
                • Gerçek market davranışını yansıtır
                
                İşaretlenmiş: Stake edilmiş tokenlar dolaşımdaki arza dahil
                • Geleneksel hesaplama yöntemi
                • Daha düşük token fiyatları (daha büyük etkili arz)
                • Muhafazakar yaklaşım
                
                Öneri: Gerçekçi modelleme için işaretsiz bırakın
                """
            )
            
            config.burn_effect_permanent = st.checkbox(
                "Yakılan Tokenlar Kalıcı Olarak Çıkarıldı", 
                value=config.burn_effect_permanent,
                help="""
                Yakmanın Toplam Arz Üzerindeki Etkisi:
                
                İşaretlenmiş (Varsayılan): Yakılan tokenlar toplam arzı kalıcı olarak azaltır
                • Deflasyonist etki
                • Zaman içinde daha yüksek token fiyatları
                • Gerçekçi yakma mekanikleri
                
                İşaretlenmemiş: Yakılan tokenlar toplam arz hesaplamasını etkilemez
                • Muhafazakar modelleme
                • Yakmalardan düşük fiyat etkisi
                • Sadece akademik analiz için
                
                Gerçek projeler: Her zaman işaretlenmiş kullanın (gerçek yakma etkisi)
                """
            )
            
            st.markdown("### Analiz Yapılandırması")
            st.markdown("**Basit Faiz Sistemi:**")
            st.success(f"""
            Onaylanmış Ayarlar:
            • Faiz Yöntemi: {config.interest_calculation_method}
            • Bileşik Faiz: {'Devre Dışı' if not config.enable_compounding else 'Etkin'}
            • Dinamik APY: {'Etkin' if config.dynamic_apy_enabled else 'Devre Dışı'}
            """)
            
            st.markdown("### Sistem Versiyon Bilgisi")
            system_info = config.get_system_info()
            st.info(f"""
            Enhanced NXID v{system_info['version']}:
            
            **Aktif Özellikler:**
            • {system_info['features'][0]}
            • {system_info['features'][1]}
            • {system_info['features'][2]}
            • {system_info['features'][3]}
            • {system_info['features'][4]}
            
            **Yapılandırma:**
            • Başlangıç McAp: ${system_info['starting_mcap']/1_000_000:.1f}M
            • Maturity Hedefi: ${system_info['maturity_target']/1_000_000_000:.1f}B
            • Faiz: {system_info['calculation_method']}
            """)
        
        return config