"""
NXID GELİŞMİŞ TOKENOMICS MODELİ - KOMPLE VERSİYON v3.1
========================================================

 TAM GELİŞMİŞ UYGULAMA:
1. Dinamik Presale ile Auto-Staking (Tüm satılan tokenlar otomatik stake)
2. APY Pool Tükenmesi Yönetimi + Minimum APY Sistemi
3. Gelişmiş Market Cap Tahmin Algoritması + Circulating Supply Tracking
4. Her Token Tahsisi için Ayrı Vesting Planları
5. Launch Sonrası Staking Mekanizması ile Fiyat Bağımlı Dinamikler
6. Dolaşımdaki Arz Etkili Fiyat Projeksiyon Modeli
7. Tax Sistemi ve Token Burning Mekanizması
8. JSON Config Yükleme/Kaydetme Sistemi
9. Günlük Satış Bar Chart + Random Investor ROI Analysis
10. Tam Özelleştirme için Kapsamlı Input Parametreleri

"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import math
import json
import os
import random
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from typing import Dict, List, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')

# Sayfa yapılandırması
st.set_page_config(
    page_title="NXID Gelişmiş Tokenomics v3.1",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# NXID Profesyonel Renkler
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
    'tax': '#ff8800'
}

@dataclass
class NXIDConfig:
    """🔧 Gelişmiş NXID Tokenomics Yapılandırması - Tam Input Kontrolü + JSON Support"""
    
    # === TEMEL TOKEN PARAMETRELERİ ===
    total_supply: float = 100_000_000_000  # 100B NXID
    
    # === TOKEN DAĞITIMI (Tüm Inputlar) ===
    team_allocation: float = 15.0           # Team %
    presale_staking_pool: float = 20.0      # Presale Staking Rewards %
    market_staking_pool: float = 25.0       # Post-Launch Staking %
    dao_treasury: float = 15.0              # DAO Treasury %
    marketing: float = 8.0                  # Marketing %
    liquidity: float = 7.0                  # Liquidity %
    presale_allocation: float = 10.0        # Presale Token Sale %
    
    # === PRESALE PARAMETRELERİ (Tüm Inputlar) ===
    presale_days: int = 180                 # Presale Süresi
    start_price_usdt: float = 0.001         # Başlangıç Fiyatı USDT
    daily_price_increase: float = 0.05      # Günlük Fiyat Artışı % 
    base_daily_demand_usdt: float = 2000    # Temel Günlük Talep USDT
    demand_growth_rate: float = 1.01        # Günlük talep büyüme çarpanı
    demand_volatility: float = 0.05         # Talep volatilite faktörü
    max_apy: float = 300.0                  # Maksimum APY %
    minimum_staking_apy: float = 50.0       # Minimum Staking APY % (YENİ)
    price_resistance_factor: float = 0.8    # Fiyatın talebi nasıl etkilediği (0-1)
    
    # === BİREYSEL VESTING PLANLARI ===
    # Team Vesting
    team_cliff_months: int = 12             # Team cliff dönemi
    team_vesting_months: int = 36           # Team toplam vesting
    
    # DAO Treasury Vesting
    dao_cliff_months: int = 6               # DAO cliff dönemi
    dao_vesting_months: int = 24            # DAO toplam vesting
    
    # Marketing Vesting
    marketing_cliff_months: int = 0         # Marketing cliff dönemi
    marketing_vesting_months: int = 12      # Marketing toplam vesting
    
    # Liquidity (Anında)
    liquidity_cliff_months: int = 0         # Liquidity cliff dönemi
    liquidity_vesting_months: int = 1       # Liquidity toplam vesting (anında)
    
    # === GELİŞMİŞ MARKET CAP TAHMİN ALGORİTMASI ===
    launch_mcap_multiplier: float = 12.0    # Launch mcap = presale_raised * çarpan
    adoption_curve_steepness: float = 1.5   # Benimsenme S-eğrisi dikliği
    market_maturity_months: float = 36.0    # Pazar olgunluğuna ulaşma ayları
    peak_mcap_multiplier: float = 120.0     # Zirve mcap = presale_raised * çarpan
    market_cycle_volatility: float = 0.001  # Pazar volatilite faktörü
    
    # === KOMPLEKS MARKET CAP FAKTÖRLERİ ===
    institutional_adoption_factor: float = 1.5  # Kurumsal benimsenme çarpanı
    retail_fomo_multiplier: float = 2.0         # Perakende FOMO çarpanı
    bear_market_resistance: float = 0.3         # Ayı piyasası direnci
    utility_growth_factor: float = 1.8          # Kullanım artış faktörü
    competition_factor: float = 0.85            # Rekabet azaltma faktörü
    
    # === LAUNCH SONRASI STAKING PARAMETRELERİ ===
    market_staking_years: int = 10          # Market staking süresi
    base_staking_participation: float = 0.45  # Temel staking oranı
    max_staking_participation: float = 0.8   # Maksimum staking oranı
    staking_price_sensitivity: float = 1.0   # Fiyatın staking'i nasıl etkilediği
    base_market_apy: float = 75.0           # Temel market staking APY
    min_market_apy: float = 10.0            # Minimum market APY
    
    # === TAX SİSTEMİ ===
    tax_period_months: int = 2              # Tax dönemi (ay)
    tax_rate_total: float = 2.0             # Toplam tax oranı %
    tax_to_staking_percentage: float = 50.0 # Tax'ın staking pool'a giden yüzdesi
    tax_to_burn_percentage: float = 50.0    # Tax'ın yakılan yüzdesi
    
    # === YAKMA MEKANİZMASI ===
    annual_burn_rate: float = 0.02          # %2 yıllık yakma oranı
    burn_duration_years: int = 3            # Yakma süresi (yıl)
    tax_burn_enabled: bool = True           # Tax burn'ü etkin mi
    
    # === PROJECTION CONTROL ===
    projection_months: int = 24             # Projeksiyon süresi (ay)
    vesting_analysis_months: int = 72       # Vesting analiz süresi (ay)
    
    def validate_distribution(self) -> bool:
        """Token dağıtımının %100'e eşit olduğunu doğrula"""
        total = (self.team_allocation + self.presale_staking_pool + self.market_staking_pool +
                self.dao_treasury + self.marketing + self.liquidity + self.presale_allocation)
        return abs(total - 100.0) < 0.01
    
    def validate_tax_distribution(self) -> bool:
        """Tax dağıtımının %100'e eşit olduğunu doğrula"""
        total = self.tax_to_staking_percentage + self.tax_to_burn_percentage
        return abs(total - 100.0) < 0.01
    
    def to_dict(self) -> dict:
        """Config'i dictionary'ye çevir"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: dict):
        """Dictionary'den config oluştur"""
        return cls(**data)
    
    def save_to_json(self, filename: str = "nxid_config.json"):
        """Config'i JSON dosyasına kaydet"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.to_dict(), f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            st.error(f"Config kaydetme hatası: {e}")
            return False
    
    @classmethod
    def load_from_json(cls, filename: str = "nxid_config.json"):
        """JSON dosyasından config yükle"""
        try:
            if os.path.exists(filename):
                with open(filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                return cls.from_dict(data)
            else:
                return cls()  # Default config döndür
        except Exception as e:
            st.error(f"Config yükleme hatası: {e}")
            return cls()  # Default config döndür

class TokenomicsModel:
    """ Tam Özelleştirme ile Gelişmiş NXID Tokenomics Modeli v3.1"""
    
    def __init__(self, config: NXIDConfig):
        self.config = config
        
    def simulate_presale_with_auto_staking(self) -> pd.DataFrame:
        """
         AUTO-STAKING İLE GELİŞMİŞ PRESALE SİMÜLASYONU + TAX SİSTEMİ + MİNİMUM APY SİSTEMİ
        
        YENİ ÖZELLİK: APY minimum'un altına düştüğünde presale tokenlerinden dağıt
        """
        np.random.seed(42)
        
        presale_tokens_for_sale = self.config.total_supply * (self.config.presale_allocation / 100)
        presale_staking_reward_pool = self.config.total_supply * (self.config.presale_staking_pool / 100)
        
        # Presale allocation ve staking pool'u birleştir
        combined_presale_pool = presale_tokens_for_sale + presale_staking_reward_pool
        
        st.info(f"""
        📊 ** Presale + Tax + Minimum APY Kurulumu:**
        - Satış İçin Tokenlar: {presale_tokens_for_sale/1e9:.1f}B NXID
        - Staking Ödül Havuzu: {presale_staking_reward_pool/1e9:.1f}B NXID
        - Birleşik Havuz: {combined_presale_pool/1e9:.1f}B NXID
        - Minimum APY: {self.config.minimum_staking_apy}%
        - Süre: {self.config.presale_days} gün
        - Tax Oranı: %{self.config.tax_rate_total} ({self.config.tax_period_months} ay)
        """)
        
        presale_data = []
        cumulative_raised_usdt = 0
        cumulative_sold_tokens = 0
        total_rewards_distributed = 0
        total_tax_collected = 0
        total_tax_to_staking = 0
        total_tax_burned = 0
        presale_tokens_used_for_rewards = 0  # YENİ: Minimum APY için kullanılan presale tokenlar
        
        for day in range(self.config.presale_days):
            # === FİYAT HESAPLAMA ===
            current_price_usdt = (self.config.start_price_usdt * 
                                ((1 + self.config.daily_price_increase/100) ** day))
            
            # === GELİŞMİŞ TALEP HESAPLAMA ===
            base_demand = (self.config.base_daily_demand_usdt * 
                          (self.config.demand_growth_rate ** day))
            
            price_effect = (self.config.start_price_usdt / current_price_usdt) ** self.config.price_resistance_factor
            volatility_factor = 1 + np.random.normal(0, self.config.demand_volatility)
            volatility_factor = max(0.98, min(1.02, volatility_factor))
            
            daily_demand_usdt = base_demand * price_effect * volatility_factor
            daily_tokens_sold = daily_demand_usdt / current_price_usdt
            
            # Mevcut satılabilir tokenları kontrol et
            remaining_sale_tokens = presale_tokens_for_sale - cumulative_sold_tokens - presale_tokens_used_for_rewards
            if daily_tokens_sold > remaining_sale_tokens:
                daily_tokens_sold = max(0, remaining_sale_tokens)
                daily_demand_usdt = daily_tokens_sold * current_price_usdt
                presale_ended = True
            else:
                presale_ended = False
            
            # === TAX HESAPLAMA ===
            months_passed = day / 30.44
            tax_active = months_passed <= self.config.tax_period_months
            
            if tax_active:
                daily_tax_usdt = daily_demand_usdt * (self.config.tax_rate_total / 100)
                daily_tax_tokens = daily_tax_usdt / current_price_usdt
                daily_tax_to_staking = daily_tax_tokens * (self.config.tax_to_staking_percentage / 100)
                daily_tax_to_burn = daily_tax_tokens * (self.config.tax_to_burn_percentage / 100)
            else:
                daily_tax_usdt = 0
                daily_tax_tokens = 0
                daily_tax_to_staking = 0
                daily_tax_to_burn = 0
            
            # === GELİŞMİŞ APY HESAPLAMA (YENİ SİSTEM) ===
            remaining_days = self.config.presale_days - day
            if cumulative_sold_tokens > 0 and remaining_days > 0:
                # Kalan staking pool'dan hesapla
                remaining_pool = presale_staking_reward_pool - total_rewards_distributed
                required_daily_rewards = remaining_pool / remaining_days
                daily_apy_needed = (required_daily_rewards / cumulative_sold_tokens) * 365 * 100
                
                # Normal APY hesapla
                normal_apy = min(daily_apy_needed, self.config.max_apy)
                
                # Minimum APY kontrolü
                if normal_apy < self.config.minimum_staking_apy:
                    # APY minimum'un altında - presale tokenlerinden dağıt
                    minimum_daily_rewards = (cumulative_sold_tokens * self.config.minimum_staking_apy / 100 / 365)
                    shortage = minimum_daily_rewards - required_daily_rewards
                    
                    # Presale tokenlerinden karşıla
                    remaining_presale_for_rewards = (presale_tokens_for_sale - cumulative_sold_tokens - 
                                                   presale_tokens_used_for_rewards)
                    
                    if shortage > 0 and remaining_presale_for_rewards > shortage:
                        presale_tokens_used_for_rewards += shortage
                        current_apy = self.config.minimum_staking_apy
                        using_presale_tokens = True
                    else:
                        current_apy = normal_apy
                        using_presale_tokens = False
                else:
                    current_apy = normal_apy
                    using_presale_tokens = False
            else:
                current_apy = self.config.max_apy
                using_presale_tokens = False
            
            # === AKÜMÜLATÖRLERI GÜNCELLE ===
            cumulative_raised_usdt += daily_demand_usdt
            cumulative_sold_tokens += daily_tokens_sold
            total_tax_collected += daily_tax_tokens
            total_tax_to_staking += daily_tax_to_staking
            total_tax_burned += daily_tax_to_burn
            
            # === GÜNLÜK STAKING ÖDÜLLERI ===
            daily_rewards = (cumulative_sold_tokens * current_apy / 100 / 365) if cumulative_sold_tokens > 0 else 0
            
            # Tax'dan gelen ek staking ödülü
            daily_rewards += daily_tax_to_staking
            total_rewards_distributed += daily_rewards
            
            # === HAVUZ DURUM TAKİBİ ===
            effective_reward_pool = presale_staking_reward_pool + presale_tokens_used_for_rewards
            remaining_reward_pool = max(0, effective_reward_pool - total_rewards_distributed)
            pool_depletion_percentage = min(100, (total_rewards_distributed / effective_reward_pool) * 100) if effective_reward_pool > 0 else 0
            
            presale_data.append({
                'day': day + 1,
                'price_usdt': current_price_usdt,
                'daily_demand_usdt': daily_demand_usdt,
                'daily_tokens_sold': daily_tokens_sold,
                'cumulative_raised_usdt': cumulative_raised_usdt,
                'cumulative_sold_tokens': cumulative_sold_tokens,
                'current_apy': current_apy,
                'daily_rewards': daily_rewards,
                'total_rewards_distributed': total_rewards_distributed,
                'remaining_reward_pool': remaining_reward_pool,
                'pool_depletion_percentage': pool_depletion_percentage,
                
                # Tax verileri
                'tax_active': tax_active,
                'daily_tax_usdt': daily_tax_usdt,
                'daily_tax_tokens': daily_tax_tokens,
                'daily_tax_to_staking': daily_tax_to_staking,
                'daily_tax_to_burn': daily_tax_to_burn,
                'total_tax_collected': total_tax_collected,
                'total_tax_to_staking': total_tax_to_staking,
                'total_tax_burned': total_tax_burned,
                
                # YENİ: Minimum APY sistemi
                'using_presale_tokens': using_presale_tokens,
                'presale_tokens_used_for_rewards': presale_tokens_used_for_rewards,
                'effective_reward_pool': effective_reward_pool,
                'minimum_apy_active': current_apy >= self.config.minimum_staking_apy,
                
                # Diğer metrikler
                'base_demand': base_demand,
                'price_effect': price_effect,
                'volatility_factor': volatility_factor,
                'presale_ended': presale_ended,
                'tokens_sold_percentage': (cumulative_sold_tokens / presale_tokens_for_sale) * 100,
                'price_appreciation': ((current_price_usdt / self.config.start_price_usdt) - 1) * 100,
                'months_passed': months_passed
            })
            
            if presale_ended:
                break
        
        return pd.DataFrame(presale_data)
    
    def calculate_individual_vesting_schedules(self, months_projection: int = None) -> pd.DataFrame:
        """📅 COMPLETE TOKEN RELEASE SCHEDULE - TÜM TOKEN ALLOCATION'LARI DAHİL"""
        
        if months_projection is None:
            months_projection = self.config.vesting_analysis_months
        
        vesting_data = []
        
        for month in range(months_projection):
            vesting_month = max(0, month - 6)  # 6 ay gecikme
            
            # === PRESALE ALLOCATION (ANINDA) ===
            presale_tokens = self.config.total_supply * (self.config.presale_allocation / 100)
            vested_presale = presale_tokens if month >= 0 else 0  # Anında release
            
            # === PRESALE STAKING POOL (ANINDA) ===
            presale_staking_tokens = self.config.total_supply * (self.config.presale_staking_pool / 100)
            vested_presale_staking = presale_staking_tokens if month >= 0 else 0  # Anında release
            
            # === MARKET STAKING POOL (ANINDA) ===
            market_staking_tokens = self.config.total_supply * (self.config.market_staking_pool / 100)
            vested_market_staking = market_staking_tokens if month >= 0 else 0  # Anında release
            
            # === TEAM VESTING ===
            team_tokens = self.config.total_supply * (self.config.team_allocation / 100)
            if vesting_month < self.config.team_cliff_months:
                vested_team = 0
            else:
                vesting_progress = min(1.0, (vesting_month - self.config.team_cliff_months) / 
                                     max(1, self.config.team_vesting_months - self.config.team_cliff_months))
                vested_team = team_tokens * vesting_progress
            
            # === DAO TREASURY VESTING ===
            dao_tokens = self.config.total_supply * (self.config.dao_treasury / 100)
            if vesting_month < self.config.dao_cliff_months:
                vested_dao = 0
            else:
                vesting_progress = min(1.0, (vesting_month - self.config.dao_cliff_months) / 
                                     max(1, self.config.dao_vesting_months - self.config.dao_cliff_months))
                vested_dao = dao_tokens * vesting_progress
            
            # === MARKETING VESTING ===
            marketing_tokens = self.config.total_supply * (self.config.marketing / 100)
            if vesting_month < self.config.marketing_cliff_months:
                vested_marketing = 0
            else:
                vesting_progress = min(1.0, (vesting_month - self.config.marketing_cliff_months) / 
                                     max(1, self.config.marketing_vesting_months - self.config.marketing_cliff_months))
                vested_marketing = marketing_tokens * vesting_progress
            
            # === LIQUIDITY (ANINDA) ===
            liquidity_tokens = self.config.total_supply * (self.config.liquidity / 100)
            vested_liquidity = liquidity_tokens if month >= 0 else 0
            
            # === TOTAL CALCULATIONS ===
            total_vested = (vested_presale + vested_presale_staking + vested_market_staking + 
                           vested_team + vested_dao + vested_marketing + vested_liquidity)
            
            vested_percentage_of_total_supply = (total_vested / self.config.total_supply * 100)
            
            # === CIRCULATING SUPPLY (vested olan her şey) ===
            circulating_supply = total_vested
            circulating_percentage = (circulating_supply / self.config.total_supply * 100)
            
            vesting_data.append({
                'month': month,
                'vesting_month': vesting_month,
                
                # Individual components
                'vested_presale': vested_presale,
                'vested_presale_staking': vested_presale_staking,
                'vested_market_staking': vested_market_staking,
                'vested_team': vested_team,
                'vested_dao': vested_dao,
                'vested_marketing': vested_marketing,
                'vested_liquidity': vested_liquidity,
                
                # Totals
                'total_vested': total_vested,
                'circulating_supply': circulating_supply,
                'vested_percentage_of_total_supply': vested_percentage_of_total_supply,
                'circulating_percentage': circulating_percentage,
                
                # Individual percentages
                'team_vested_pct': (vested_team / team_tokens * 100) if team_tokens > 0 else 0,
                'dao_vested_pct': (vested_dao / dao_tokens * 100) if dao_tokens > 0 else 0,
                'marketing_vested_pct': (vested_marketing / marketing_tokens * 100) if marketing_tokens > 0 else 0,
                'liquidity_vested_pct': (vested_liquidity / liquidity_tokens * 100) if liquidity_tokens > 0 else 0,
                
                # Token totals
                'team_tokens_total': team_tokens,
                'dao_tokens_total': dao_tokens,
                'marketing_tokens_total': marketing_tokens,
                'liquidity_tokens_total': liquidity_tokens,
                'presale_tokens_total': presale_tokens,
                'presale_staking_tokens_total': presale_staking_tokens,
                'market_staking_tokens_total': market_staking_tokens,
                
                # Status
                'vesting_started': month >= 6
            })
        
        return pd.DataFrame(vesting_data)
    
    def estimate_complex_market_cap_and_price(self, presale_df: pd.DataFrame, vesting_df: pd.DataFrame) -> pd.DataFrame:
        """ KOMPLEKS MARKET CAP TAHMİN ALGORİTMASI v3.1"""
        
        np.random.seed(123)
        
        final_presale_raised = presale_df['cumulative_raised_usdt'].iloc[-1]
        final_presale_tokens = presale_df['cumulative_sold_tokens'].iloc[-1]
        final_tax_burned = presale_df['total_tax_burned'].iloc[-1] if 'total_tax_burned' in presale_df.columns else 0
        
        # Kompleks market cap hesaplama
        base_launch_mcap = final_presale_raised * self.config.launch_mcap_multiplier
        institutional_boost = base_launch_mcap * self.config.institutional_adoption_factor
        launch_mcap = base_launch_mcap + (institutional_boost - base_launch_mcap) * 0.3
        
        base_peak_mcap = final_presale_raised * self.config.peak_mcap_multiplier
        retail_fomo_boost = base_peak_mcap * self.config.retail_fomo_multiplier
        peak_mcap = base_peak_mcap + (retail_fomo_boost - base_peak_mcap) * 0.8
        
        st.info(f"""
         **Kompleks Market Cap Tahmini v3.1:**
        - Launch Market Cap: ${launch_mcap/1e6:.1f}M (Kurumsal Faktör: +{self.config.institutional_adoption_factor:.1f}x)
        - Zirve Market Cap: ${peak_mcap/1e6:.1f}M (FOMO Faktör: +{self.config.retail_fomo_multiplier:.1f}x)
        - Utility Büyüme: +{self.config.utility_growth_factor:.1f}x
        - Rekabet Etkisi: -{(1-self.config.competition_factor)*100:.0f}%
        - Bear Market Direnci: {self.config.bear_market_resistance:.1f}x
        """)
        
        projection_days = int(self.config.projection_months * 30.44)
        projection_data = []
        
        for day in range(projection_days):
            months = day / 30.44
            years = day / 365.25
            
            # === KOMPLEKS BENIMSENME MODELLEMESİ ===
            adoption_progress = months / self.config.market_maturity_months
            adoption_factor = 1 / (1 + math.exp(-self.config.adoption_curve_steepness * (adoption_progress - 0.5)))
            
            # Kurumsal benimsenme etkisi
            institutional_effect = 1 + (self.config.institutional_adoption_factor - 1) * min(adoption_progress * 1.5, 1.0)
            
            # Utility büyüme etkisi
            utility_effect = 1 + (self.config.utility_growth_factor - 1) * adoption_progress ** 0.7
            
            # === PAZAR DÖNGÜSÜ SİMÜLASYONU ===
            # Ana pazar döngüsü (24 aylık)
            main_cycle = 1 + 0.3 * math.sin(2 * math.pi * months / 24 + math.pi/4)
            
            # FOMO döngüsü (6 aylık)
            fomo_cycle = 1 + 0.2 * math.sin(2 * math.pi * months / 6) if months > 3 else 1.0
            
            # Bear market etkisi (18 aylık döngü)
            bear_cycle = self.config.bear_market_resistance + (1 - self.config.bear_market_resistance) * (1 + math.sin(2 * math.pi * months / 18)) / 2
            
            # Rekabet etkisi (zamanla artar)
            competition_effect = 1 - (1 - self.config.competition_factor) * min(adoption_progress, 1.0)
            
            # === MARKET CAP HESAPLAMA ===
            if adoption_progress <= 1.0:
                # Büyüme aşaması
                mcap_progress = adoption_factor
                base_mcap = launch_mcap + (peak_mcap - launch_mcap) * mcap_progress
            else:
                # Olgunluk aşaması
                maturity_factor = 0.85 + 0.15 * math.exp(-(adoption_progress - 1) * 1.5)
                base_mcap = peak_mcap * maturity_factor
            
            # Tüm faktörleri uygula
            current_mcap = (base_mcap * institutional_effect * utility_effect * 
                          main_cycle * fomo_cycle * bear_cycle * competition_effect)
            
            # === DOLAŞIMDAKI ARZ HESAPLAMA ===
            month_index = min(len(vesting_df) - 1, int(months))
            
            # Presale tokenları (artık vesting_df'ten alıyoruz)
            if 'vested_presale' in vesting_df.columns and month_index < len(vesting_df):
                presale_supply = vesting_df.iloc[month_index]['vested_presale']
            else:
                presale_supply = final_presale_tokens
            
            # Vested tokenlar (artık sadece vesting olan kısımları)
            if month_index < len(vesting_df):
                vested_supply = (vesting_df.iloc[month_index]['vested_team'] + 
                               vesting_df.iloc[month_index]['vested_dao'] + 
                               vesting_df.iloc[month_index]['vested_marketing'] + 
                               vesting_df.iloc[month_index]['vested_liquidity'])
                
                # Staking pool'ları da dahil et
                if 'vested_presale_staking' in vesting_df.columns:
                    vested_supply += vesting_df.iloc[month_index]['vested_presale_staking']
                if 'vested_market_staking' in vesting_df.columns:
                    vested_supply += vesting_df.iloc[month_index]['vested_market_staking']
            else:
                vested_supply = 0
            
            # === TOKEN YAKMA ETKİLERİ ===
            # Rutin yakma
            if years <= self.config.burn_duration_years:
                routine_burned = self.config.total_supply * self.config.annual_burn_rate * years
            else:
                routine_burned = self.config.total_supply * self.config.annual_burn_rate * self.config.burn_duration_years
            
            # Tax yakma (presale'den)
            tax_burned = final_tax_burned
            
            # Toplam yakılan
            total_burned = routine_burned + tax_burned
            effective_total_supply = self.config.total_supply - total_burned
            
            # Circulating Supply
            circulating_supply = min(presale_supply + vested_supply, effective_total_supply)
            
            # === TOKEN FİYAT HESAPLAMA ===
            token_price = current_mcap / circulating_supply if circulating_supply > 0 else 0
            
            final_presale_price = presale_df['price_usdt'].iloc[-1]
            price_vs_presale = token_price / final_presale_price if final_presale_price > 0 else 1
            
            # === DETAYLI VERİ DEPOLAMA ===
            projection_data.append({
                'day': day,
                'months': months,
                'years': years,
                'mcap_usdt': current_mcap,
                'circulating_supply': circulating_supply,
                'token_price': token_price,
                'adoption_factor': adoption_factor,
                'institutional_effect': institutional_effect,
                'utility_effect': utility_effect,
                'main_cycle': main_cycle,
                'fomo_cycle': fomo_cycle,
                'bear_cycle': bear_cycle,
                'competition_effect': competition_effect,
                'presale_supply': presale_supply,
                'vested_supply': vested_supply,
                'routine_burned': routine_burned,
                'tax_burned': tax_burned,
                'total_burned': total_burned,
                'effective_total_supply': effective_total_supply,
                'price_vs_presale': price_vs_presale,
                'adoption_progress': adoption_progress,
                'mcap_vs_launch': current_mcap / launch_mcap,
                'burn_rate_percentage': (total_burned / self.config.total_supply) * 100,
                'circulating_percentage': (circulating_supply / effective_total_supply) * 100
            })
        
        return pd.DataFrame(projection_data)
    
    def simulate_post_launch_staking(self, projection_df: pd.DataFrame, presale_df: pd.DataFrame) -> pd.DataFrame:
        """⚡ LAUNCH SONRASI STAKING + TAX SİSTEMİ v3.1"""
        
        np.random.seed(456)
        
        market_staking_pool = self.config.total_supply * (self.config.market_staking_pool / 100)
        tax_to_staking_pool = presale_df['total_tax_to_staking'].iloc[-1] if 'total_tax_to_staking' in presale_df.columns else 0
        total_staking_pool = market_staking_pool + tax_to_staking_pool
        
        st.info(f"""
        ⚡ **Launch Sonrası Staking + Tax Kurulumu v3.1:**
        - Market Staking Havuzu: {market_staking_pool/1e9:.1f}B NXID
        - Tax'dan Ek Havuz: {tax_to_staking_pool/1e9:.1f}B NXID  
        - Toplam Staking Havuzu: {total_staking_pool/1e9:.1f}B NXID
        - Süre: {self.config.market_staking_years} yıl
        """)
        
        staking_data = []
        cumulative_staked = 0
        distributed_rewards = 0
        
        for idx, row in projection_df.iterrows():
            day = row['day']
            months = row['months']
            years = row['years']
            token_price = row['token_price']
            circulating_supply = row['circulating_supply']
            
            # === FİYAT BAĞIMLI STAKING KATILIMI ===
            if months < 3:
                price_incentive = 1.0
            else:
                price_incentive = min(2.0, 1 + (token_price / 0.001 - 1) ** 0.3)
            
            participation_rate = self.config.base_staking_participation * (
                1 + (price_incentive - 1) * self.config.staking_price_sensitivity * 0.3
            )
            participation_rate = min(self.config.max_staking_participation, participation_rate)
            
            # === STAKING HESAPLAMA ===
            available_for_staking = max(0, circulating_supply - cumulative_staked)
            daily_new_staking = available_for_staking * 0.005 * participation_rate
            cumulative_staked += daily_new_staking
            
            # Unstaking
            if cumulative_staked > 0:
                daily_unstaking = cumulative_staked * 0.002
                cumulative_staked = max(0, cumulative_staked - daily_unstaking)
            
            # === DİNAMİK APY HESAPLAMA ===
            staking_ratio = cumulative_staked / circulating_supply if circulating_supply > 0 else 0
            supply_adjustment = 1 - (staking_ratio * 0.5)
            years_remaining = max(0, self.config.market_staking_years - years)
            time_factor = years_remaining / self.config.market_staking_years
            
            current_market_apy = max(
                self.config.min_market_apy,
                self.config.base_market_apy * supply_adjustment * time_factor
            )
            
            # === GÜNLÜK ÖDÜL DAĞITIMI ===
            daily_rewards = (cumulative_staked * current_market_apy / 100 / 365) if cumulative_staked > 0 else 0
            
            if distributed_rewards + daily_rewards <= total_staking_pool:
                distributed_rewards += daily_rewards
            else:
                daily_rewards = max(0, total_staking_pool - distributed_rewards)
                distributed_rewards = total_staking_pool
                current_market_apy = 0
            
            effective_circulating = circulating_supply - cumulative_staked
            
            staking_data.append({
                'day': day,
                'months': months,
                'years': years,
                'token_price': token_price,
                'circulating_supply': circulating_supply,
                'price_incentive': price_incentive,
                'participation_rate': participation_rate,
                'daily_new_staking': daily_new_staking,
                'cumulative_staked': cumulative_staked,
                'staking_ratio': staking_ratio,
                'current_market_apy': current_market_apy,
                'daily_rewards': daily_rewards,
                'distributed_rewards': distributed_rewards,
                'remaining_staking_pool': total_staking_pool - distributed_rewards,
                'effective_circulating': effective_circulating,
                'supply_adjustment': supply_adjustment,
                'time_factor': time_factor,
                'total_staking_pool': total_staking_pool,
                'tax_contribution': tax_to_staking_pool
            })
        
        return pd.DataFrame(staking_data)
    
    def generate_random_investor_analysis(self, presale_df: pd.DataFrame, projection_df: pd.DataFrame) -> pd.DataFrame:
        """
        📊 YENİ: RASTGELE GÜNLERDE YATIRIM YAPMIŞ KULLANICILARIN ROI ANALİZİ
        """
        random.seed(42)  # Tutarlı sonuçlar için
        
        # 10-15 rastgele investor oluştur
        num_investors = 12
        investors_data = []
        
        for i in range(num_investors):
            # Rastgele yatırım günü seç (presale içinde)
            investment_day = random.randint(1, len(presale_df))
            investment_amount_usdt = random.uniform(100, 5000)  # $100-$5000 arası
            
            # O günkü fiyat
            investment_price = presale_df.iloc[investment_day-1]['price_usdt']
            tokens_bought = investment_amount_usdt / investment_price
            
            # Çeşitli zaman noktalarında ROI hesapla
            roi_data = []
            
            # Presale sonunda
            final_presale_price = presale_df['price_usdt'].iloc[-1]
            presale_end_value = tokens_bought * final_presale_price
            presale_roi = ((presale_end_value / investment_amount_usdt) - 1) * 100
            
            # Market projection'daki çeşitli noktalarda
            for month_check in [3, 6, 12, 18, 24]:
                if month_check * 30.44 < len(projection_df):
                    month_idx = int(month_check * 30.44)
                    market_price = projection_df.iloc[month_idx]['token_price']
                    market_value = tokens_bought * market_price
                    market_roi = ((market_value / investment_amount_usdt) - 1) * 100
                    
                    roi_data.append({
                        'investor_id': f"Investor_{i+1}",
                        'investment_day': investment_day,
                        'investment_amount_usdt': investment_amount_usdt,
                        'investment_price': investment_price,
                        'tokens_bought': tokens_bought,
                        'evaluation_point': f"Month_{month_check}",
                        'evaluation_price': market_price,
                        'evaluation_value': market_value,
                        'roi_percentage': market_roi,
                        'evaluation_type': 'Market'
                    })
            
            # Presale end data
            roi_data.append({
                'investor_id': f"Investor_{i+1}",
                'investment_day': investment_day,
                'investment_amount_usdt': investment_amount_usdt,
                'investment_price': investment_price,
                'tokens_bought': tokens_bought,
                'evaluation_point': "Presale_End",
                'evaluation_price': final_presale_price,
                'evaluation_value': presale_end_value,
                'roi_percentage': presale_roi,
                'evaluation_type': 'Presale'
            })
            
            investors_data.extend(roi_data)
        
        return pd.DataFrame(investors_data)
    
    def create__visualizations(self, presale_df: pd.DataFrame, 
                                     vesting_df: pd.DataFrame,
                                     projection_df: pd.DataFrame, 
                                     staking_df: pd.DataFrame,
                                     investor_analysis_df: pd.DataFrame) -> Dict[str, go.Figure]:
        """📊 Gelişmiş profesyonel görselleştirmeler v3.1 (YENİ GRAFİKLER EKLENDİ)"""
        
        charts = {}
        
        chart_template = {
            'paper_bgcolor': 'rgba(0,0,0,0)',
            'plot_bgcolor': f"rgba{hex_to_rgb(NXID_COLORS['dark']) + (0.4,)}",
            'font': {'color': NXID_COLORS['light'], 'family': 'Inter', 'size': 11},
            'xaxis': {
                'gridcolor': f"rgba{hex_to_rgb(NXID_COLORS['primary']) + (0.15,)}", 
                'linecolor': NXID_COLORS['primary'],
                'tickfont': {'size': 10}
            },
            'yaxis': {
                'gridcolor': f"rgba{hex_to_rgb(NXID_COLORS['primary']) + (0.15,)}", 
                'linecolor': NXID_COLORS['primary'],
                'tickfont': {'size': 10}
            }
        }
        
        # === 1. GELİŞMİŞ TOKEN DAĞITIMI PIE CHART (YENİ TASARIM) ===
        labels = ['Team', 'Presale Staking Pool', 'Market Staking Pool', 'DAO Treasury', 
                 'Marketing', 'Liquidity', 'Presale Allocation']
        values = [
            self.config.team_allocation,
            self.config.presale_staking_pool, 
            self.config.market_staking_pool,
            self.config.dao_treasury,
            self.config.marketing,
            self.config.liquidity,
            self.config.presale_allocation
        ]
        
        colors = [
            NXID_COLORS['purple'],       # Team
            NXID_COLORS['gold'],         # Presale Staking Pool
            NXID_COLORS['teal'],         # Market Staking Pool
            NXID_COLORS['indigo'],       # DAO Treasury
            NXID_COLORS['orange'],       # Marketing
            NXID_COLORS['success'],      # Liquidity
            NXID_COLORS['primary'],      # Presale Allocation
        ]
        
        fig_dist = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=0.5,  # Daha büyük hole
            textinfo='label+percent',
            textposition='outside',
            textfont=dict(size=12, color=NXID_COLORS['light'], family='Inter'),
            marker=dict(
                colors=colors,
                line=dict(color=NXID_COLORS['darker'], width=2)
            ),
            pull=[0.08 if 'Staking' in label else 0.04 for label in labels],
            hovertemplate='<b>%{label}</b><br>%{percent}<br>%{value:.1f}% of Supply<br><b>%{customdata:.1f}B NXID</b><extra></extra>',
            customdata=[v * self.config.total_supply / 100 / 1e9 for v in values],
            rotation=45
        )])
        
        # YENİ: Merkeze sadece NXID logosu ve temel bilgi
        fig_dist.add_annotation(
            text=f"<b style='font-family: Orbitron; font-size: 36px; color: {NXID_COLORS['primary']};'>NXID</b><br>" +
                 f"<span style='font-size: 24px; color: {NXID_COLORS['secondary']}; font-weight: 700;'>{self.config.total_supply/1e9:.0f}B</span><br>" +
                 f"<span style='font-size: 14px; color: {NXID_COLORS['accent']};'>Total Supply</span>",
            x=0.5, y=0.5,
            font=dict(size=20),
            showarrow=False,
            bgcolor='rgba(0,0,0,0)',  # Şeffaf arka plan
            borderwidth=0
        )
        
        fig_dist.update_layout(
            title=dict(
                text='<b style="font-family: Orbitron; font-size: 32px;">📊 NXID Token Distribution (Pie Chart)</b>',
                x=0.5, y=0.95,
                font=dict(color=NXID_COLORS['primary'])
            ),
            **chart_template,
            height=600,
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="top",
                y=-0.1,
                xanchor="center",
                x=0.5,
                font=dict(color=NXID_COLORS['light'], size=11)
            )
        )
        charts['distribution'] = fig_dist
        
        # === 2. COMPLETE TOKEN RELEASE SCHEDULE (FIXED & COMPREHENSIVE) ===
        fig_vesting = make_subplots(
            rows=2, cols=1,
            subplot_titles=['🔄 Complete Token Release Schedule - All Components (Stacked Area Chart)', 
                           '📊 Circulating Supply Growth Over Time (Line Chart)'],
            specs=[[{"secondary_y": True}], [{"secondary_y": True}]],
            vertical_spacing=0.2
        )
        
        # Stacked areas for ALL token components
        # 1. Presale Allocation (anında)
        fig_vesting.add_trace(go.Scatter(
            x=vesting_df['month'], y=vesting_df['vested_presale']/1e9,
            mode='lines', name='Presale Allocation (B)', fill='tozeroy', stackgroup='tokens',
            line=dict(color=NXID_COLORS['primary'], width=1),
            fillcolor=f"rgba{hex_to_rgb(NXID_COLORS['primary']) + (0.8,)}",
            hovertemplate='<b>Presale Allocation</b><br>Month: %{x}<br>Released: %{y:.1f}B NXID<extra></extra>'
        ), row=1, col=1)
        
        # 2. Presale Staking Pool (anında)
        fig_vesting.add_trace(go.Scatter(
            x=vesting_df['month'], y=vesting_df['vested_presale_staking']/1e9,
            mode='lines', name='Presale Staking Pool (B)', fill='tonexty', stackgroup='tokens',
            line=dict(color=NXID_COLORS['gold'], width=1),
            fillcolor=f"rgba{hex_to_rgb(NXID_COLORS['gold']) + (0.8,)}",
            hovertemplate='<b>Presale Staking Pool</b><br>Month: %{x}<br>Released: %{y:.1f}B NXID<extra></extra>'
        ), row=1, col=1)
        
        # 3. Market Staking Pool (anında)
        fig_vesting.add_trace(go.Scatter(
            x=vesting_df['month'], y=vesting_df['vested_market_staking']/1e9,
            mode='lines', name='Market Staking Pool (B)', fill='tonexty', stackgroup='tokens',
            line=dict(color=NXID_COLORS['teal'], width=1),
            fillcolor=f"rgba{hex_to_rgb(NXID_COLORS['teal']) + (0.8,)}",
            hovertemplate='<b>Market Staking Pool</b><br>Month: %{x}<br>Released: %{y:.1f}B NXID<extra></extra>'
        ), row=1, col=1)
        
        # 4. Liquidity (anında)
        fig_vesting.add_trace(go.Scatter(
            x=vesting_df['month'], y=vesting_df['vested_liquidity']/1e9,
            mode='lines', name='Liquidity (B)', fill='tonexty', stackgroup='tokens',
            line=dict(color=NXID_COLORS['success'], width=1),
            fillcolor=f"rgba{hex_to_rgb(NXID_COLORS['success']) + (0.8,)}",
            hovertemplate='<b>Liquidity</b><br>Month: %{x}<br>Released: %{y:.1f}B NXID<extra></extra>'
        ), row=1, col=1)
        
        # 5. Marketing (vesting)
        fig_vesting.add_trace(go.Scatter(
            x=vesting_df['month'], y=vesting_df['vested_marketing']/1e9,
            mode='lines', name='Marketing (B)', fill='tonexty', stackgroup='tokens',
            line=dict(color=NXID_COLORS['orange'], width=1),
            fillcolor=f"rgba{hex_to_rgb(NXID_COLORS['orange']) + (0.8,)}",
            hovertemplate='<b>Marketing</b><br>Month: %{x}<br>Vested: %{y:.1f}B NXID<extra></extra>'
        ), row=1, col=1)
        
        # 6. DAO Treasury (vesting)
        fig_vesting.add_trace(go.Scatter(
            x=vesting_df['month'], y=vesting_df['vested_dao']/1e9,
            mode='lines', name='DAO Treasury (B)', fill='tonexty', stackgroup='tokens',
            line=dict(color=NXID_COLORS['indigo'], width=1),
            fillcolor=f"rgba{hex_to_rgb(NXID_COLORS['indigo']) + (0.8,)}",
            hovertemplate='<b>DAO Treasury</b><br>Month: %{x}<br>Vested: %{y:.1f}B NXID<extra></extra>'
        ), row=1, col=1)
        
        # 7. Team (vesting)
        fig_vesting.add_trace(go.Scatter(
            x=vesting_df['month'], y=vesting_df['vested_team']/1e9,
            mode='lines', name='Team (B)', fill='tonexty', stackgroup='tokens',
            line=dict(color=NXID_COLORS['purple'], width=1),
            fillcolor=f"rgba{hex_to_rgb(NXID_COLORS['purple']) + (0.8,)}",
            hovertemplate='<b>Team</b><br>Month: %{x}<br>Vested: %{y:.1f}B NXID<extra></extra>'
        ), row=1, col=1)
        
        # Total percentage line (secondary y-axis)
        fig_vesting.add_trace(go.Scatter(
            x=vesting_df['month'], y=vesting_df['vested_percentage_of_total_supply'],
            mode='lines', name='Total Released (%)', 
            line=dict(color=NXID_COLORS['secondary'], width=4, dash='dash'),
            hovertemplate='<b>Total Released</b><br>Month: %{x}<br>Percentage: %{y:.1f}% of Total Supply<extra></extra>'
        ), row=1, col=1, secondary_y=True)
        
        # === CIRCULATING SUPPLY GROWTH (Row 2) ===
        fig_vesting.add_trace(go.Scatter(
            x=vesting_df['month'], y=vesting_df['circulating_supply']/1e9,
            mode='lines', name='Circulating Supply (B)', 
            line=dict(color=NXID_COLORS['primary'], width=4),
            fill='tonexty', fillcolor=f"rgba{hex_to_rgb(NXID_COLORS['primary']) + (0.3,)}",
            hovertemplate='<b>Circulating Supply</b><br>Month: %{x}<br>Supply: %{y:.1f}B NXID<extra></extra>'
        ), row=2, col=1)
        
        fig_vesting.add_trace(go.Scatter(
            x=vesting_df['month'], y=vesting_df['circulating_percentage'],
            mode='lines', name='Circulating %', 
            line=dict(color=NXID_COLORS['accent'], width=3),
            hovertemplate='<b>Circulating Percentage</b><br>Month: %{x}<br>Percentage: %{y:.1f}%<extra></extra>'
        ), row=2, col=1, secondary_y=True)
        
        # === IMPORTANT MILESTONES ===
        # Vesting start indicator
        fig_vesting.add_vline(
            x=6,
            line_dash="solid",
            line_color=NXID_COLORS['secondary'],
            line_width=3,
            annotation_text=" VESTING STARTS",
            annotation_position="top left",
            annotation_font=dict(color=NXID_COLORS['secondary'], size=14, family="Orbitron")
        )
        
        # Cliff indicators with offset
        cliff_data = [
            (6 + self.config.team_cliff_months, 'Team Cliff', NXID_COLORS['purple']),
            (6 + self.config.dao_cliff_months, 'DAO Cliff', NXID_COLORS['indigo']),
            (6 + self.config.marketing_cliff_months, 'Marketing Cliff', NXID_COLORS['orange']),
        ]
        
        for cliff_month, cliff_name, cliff_color in cliff_data:
            if cliff_month > 6 and cliff_month < self.config.vesting_analysis_months:
                fig_vesting.add_vline(
                    x=cliff_month, 
                    line_dash="dot", 
                    line_color=cliff_color,
                    line_width=2,
                    annotation_text=f"{cliff_name}",
                    annotation_position="top right",
                    annotation_font=dict(color=cliff_color, size=11)
                )
        
        # Update axes
        fig_vesting.update_yaxes(title_text="Released Tokens (Billions NXID)", secondary_y=False, row=1, col=1)
        fig_vesting.update_yaxes(title_text="Total Supply Percentage (%)", secondary_y=True, row=1, col=1)
        fig_vesting.update_yaxes(title_text="Circulating Supply (Billions NXID)", secondary_y=False, row=2, col=1)
        fig_vesting.update_yaxes(title_text="Circulating Percentage (%)", secondary_y=True, row=2, col=1)
        
        fig_vesting.update_layout(
            title=dict(text='<b>📊 Complete Token Release & Circulating Supply Analysis (Fixed)</b>', x=0.5,
                      font=dict(size=28, color=NXID_COLORS['primary'])),
            **chart_template, height=800,
            hovermode='x unified',
            showlegend=True,
            legend=dict(
                orientation="v",
                yanchor="top",
                y=1,
                xanchor="left",
                x=1.02,
                font=dict(size=10)
            )
        )
        charts['vesting'] = fig_vesting
        
        # === 3.  PRESALE COMPREHENSIVE DASHBOARD ===
        fig_presale = make_subplots(
            rows=3, cols=2,
            subplot_titles=[
                ' Daily Token Sales Volume (Bar Chart)', 
                '💰 Price Evolution & Cumulative Raised (Line Chart)',
                '⚡ APY System Performance (Area Chart)', 
                '🔥 Tax Collection & Distribution (Bar+Line Chart)',
                '📊 Cumulative Sales Progress (Line Chart)', 
                ' Pool Management & Efficiency (Line Chart)'
            ],
            specs=[
                [{"secondary_y": False}, {"secondary_y": True}],
                [{"secondary_y": True}, {"secondary_y": True}], 
                [{"secondary_y": True}, {"secondary_y": True}]
            ],
            vertical_spacing=0.12,
            horizontal_spacing=0.1
        )
        
        # === ROW 1: DAILY SALES & PRICE EVOLUTION ===
        # Daily sales bar chart
        fig_presale.add_trace(
            go.Bar(x=presale_df['day'], y=presale_df['daily_tokens_sold']/1e6,
                   name='Daily Sales (M)', marker_color=NXID_COLORS['primary'],
                   hovertemplate='<b>Day %{x}</b><br>Sold: %{y:.2f}M NXID<br><extra></extra>'),
            row=1, col=1
        )
        
        # Price evolution with cumulative raised
        fig_presale.add_trace(
            go.Scatter(x=presale_df['day'], y=presale_df['price_usdt'],
                      name='Price (USDT)', line=dict(color=NXID_COLORS['gold'], width=4),
                      hovertemplate='<b>Day %{x}</b><br>Price: $%{y:.6f}<extra></extra>'),
            row=1, col=2
        )
        fig_presale.add_trace(
            go.Scatter(x=presale_df['day'], y=presale_df['cumulative_raised_usdt']/1e6,
                      name='Cumulative Raised (M USDT)', line=dict(color=NXID_COLORS['success'], width=3),
                      fill='tonexty', fillcolor=f"rgba{hex_to_rgb(NXID_COLORS['success']) + (0.2,)}",
                      hovertemplate='<b>Day %{x}</b><br>Raised: $%{y:.1f}M<extra></extra>'),
            row=1, col=2, secondary_y=True
        )
        
        # === ROW 2: APY SYSTEM & TAX ANALYSIS ===
        # APY evolution with minimum APY reference
        fig_presale.add_trace(
            go.Scatter(x=presale_df['day'], y=presale_df['current_apy'],
                      name='Current APY (%)', line=dict(color=NXID_COLORS['gold'], width=4),
                      fill='tonexty', fillcolor=f"rgba{hex_to_rgb(NXID_COLORS['gold']) + (0.3,)}",
                      hovertemplate='<b>Day %{x}</b><br>APY: %{y:.1f}%<extra></extra>'),
            row=2, col=1
        )
        
        # Add minimum APY reference line
        min_apy_line = [self.config.minimum_staking_apy] * len(presale_df)
        fig_presale.add_trace(
            go.Scatter(x=presale_df['day'], y=min_apy_line,
                      mode='lines', name=f'Min APY: {self.config.minimum_staking_apy}%',
                      line=dict(color=NXID_COLORS['danger'], width=2, dash='dash'),
                      hovertemplate=f'<b>Minimum APY</b><br>%{self.config.minimum_staking_apy:.0f}%<extra></extra>'),
            row=2, col=1, secondary_y=True
        )
        
        # Tax system analysis
        if 'daily_tax_tokens' in presale_df.columns:
            fig_presale.add_trace(
                go.Bar(x=presale_df['day'], y=presale_df['daily_tax_tokens']/1e6,
                      name='Daily Tax (M)', marker_color=NXID_COLORS['tax'],
                      hovertemplate='<b>Day %{x}</b><br>Tax: %{y:.2f}M NXID<extra></extra>'),
                row=2, col=2
            )
            fig_presale.add_trace(
                go.Scatter(x=presale_df['day'], y=presale_df['total_tax_burned']/1e6,
                          name='Tax Burned (M)', line=dict(color=NXID_COLORS['burn'], width=3),
                          hovertemplate='<b>Day %{x}</b><br>Burned: %{y:.1f}M NXID<extra></extra>'),
                row=2, col=2, secondary_y=True
            )
        
        # === ROW 3: CUMULATIVE METRICS & POOL MANAGEMENT ===
        # Cumulative sales progress
        fig_presale.add_trace(
            go.Scatter(x=presale_df['day'], y=presale_df['cumulative_sold_tokens']/1e9,
                      name='Sold Tokens (B)', line=dict(color=NXID_COLORS['primary'], width=4),
                      fill='tonexty', fillcolor=f"rgba{hex_to_rgb(NXID_COLORS['primary']) + (0.2,)}",
                      hovertemplate='<b>Day %{x}</b><br>Sold: %{y:.2f}B NXID<extra></extra>'),
            row=3, col=1
        )
        fig_presale.add_trace(
            go.Scatter(x=presale_df['day'], y=presale_df['tokens_sold_percentage'],
                      name='Sold %', line=dict(color=NXID_COLORS['accent'], width=3),
                      hovertemplate='<b>Day %{x}</b><br>Sold: %{y:.1f}% of allocation<extra></extra>'),
            row=3, col=1, secondary_y=True
        )
        
        # Pool management efficiency
        fig_presale.add_trace(
            go.Scatter(x=presale_df['day'], y=presale_df['remaining_reward_pool']/1e9,
                      name='Remaining Pool (B)', line=dict(color=NXID_COLORS['teal'], width=4),
                      fill='tonexty', fillcolor=f"rgba{hex_to_rgb(NXID_COLORS['teal']) + (0.2,)}",
                      hovertemplate='<b>Day %{x}</b><br>Remaining: %{y:.1f}B NXID<extra></extra>'),
            row=3, col=2
        )
        fig_presale.add_trace(
            go.Scatter(x=presale_df['day'], y=presale_df['pool_depletion_percentage'],
                      name='Pool Depletion %', line=dict(color=NXID_COLORS['warning'], width=3),
                      hovertemplate='<b>Day %{x}</b><br>Depleted: %{y:.1f}%<extra></extra>'),
            row=3, col=2, secondary_y=True
        )
        
        # ===  ANNOTATIONS ===
        # Tax period highlight
        tax_end_day = self.config.tax_period_months * 30.44
        if tax_end_day < len(presale_df):
            # Add tax period rectangle to multiple subplots
            for row in [1, 2, 3]:
                for col in [1, 2]:
                    fig_presale.add_vrect(
                        x0=0, x1=tax_end_day,
                        fillcolor=NXID_COLORS['tax'], opacity=0.1,
                        row=row, col=col
                    )
        
        # Using presale tokens indicators
        if 'using_presale_tokens' in presale_df.columns:
            using_days = presale_df[presale_df['using_presale_tokens'] == True]['day']
            if len(using_days) > 0:
                for day in using_days:
                    fig_presale.add_vline(
                        x=day, line_dash="dot", line_color=NXID_COLORS['danger'], line_width=1,
                        annotation_text="Min APY Active" if day == using_days.iloc[0] else "",
                        annotation_position="top",
                        annotation_font=dict(color=NXID_COLORS['danger'], size=9)
                    )
        
        # Update axes labels
        fig_presale.update_xaxes(title_text="Presale Day", row=3, col=1)
        fig_presale.update_xaxes(title_text="Presale Day", row=3, col=2)
        
        fig_presale.update_yaxes(title_text="Daily Sales (M NXID)", row=1, col=1)
        fig_presale.update_yaxes(title_text="Price (USDT)", row=1, col=2)
        fig_presale.update_yaxes(title_text="Cumulative Raised (M USDT)", row=1, col=2, secondary_y=True)
        
        fig_presale.update_yaxes(title_text="APY (%)", row=2, col=1)
        fig_presale.update_yaxes(title_text="Daily Tax (M NXID)", row=2, col=2)
        fig_presale.update_yaxes(title_text="Tax Burned (M NXID)", row=2, col=2, secondary_y=True)
        
        fig_presale.update_yaxes(title_text="Sold Tokens (B NXID)", row=3, col=1)
        fig_presale.update_yaxes(title_text="Sold %", row=3, col=1, secondary_y=True)
        fig_presale.update_yaxes(title_text="Remaining Pool (B NXID)", row=3, col=2)
        fig_presale.update_yaxes(title_text="Pool Depletion %", row=3, col=2, secondary_y=True)
        
        fig_presale.update_layout(
            title=dict(text='<b>📊  Presale Comprehensive Dashboard (Multi-Chart)</b>', x=0.5, 
                      font=dict(size=32, color=NXID_COLORS['primary'])),
            **chart_template, height=1000, 
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.15,
                xanchor="center",
                x=0.5,
                font=dict(size=10)
            )
        )
        charts['presale'] = fig_presale
        
        # === 4. SEPARATE LARGE DAILY SALES CHART ===
        fig_daily_sales = go.Figure()
        
        # Main bar chart
        fig_daily_sales.add_trace(go.Bar(
            x=presale_df['day'],
            y=presale_df['daily_tokens_sold']/1e6,
            name='Daily Token Sales (Million NXID)',
            marker=dict(
                color=presale_df['price_usdt'],
                colorscale='Viridis',
                colorbar=dict(title="Price (USDT)", titleside="right"),
                line=dict(color=NXID_COLORS['light'], width=0.5)
            ),
            hovertemplate='<b>Day %{x}</b><br>Sales: %{y:.2f}M NXID<br>Price: $%{customdata:.6f}<br><extra></extra>',
            customdata=presale_df['price_usdt']
        ))
        
        # Add trend line
        fig_daily_sales.add_trace(go.Scatter(
            x=presale_df['day'],
            y=presale_df['daily_tokens_sold'].rolling(window=7, center=True).mean()/1e6,
            mode='lines',
            name='7-Day Average',
            line=dict(color=NXID_COLORS['secondary'], width=3),
            hovertemplate='<b>Day %{x}</b><br>7-Day Avg: %{y:.2f}M NXID<extra></extra>'
        ))
        
        # Tax period highlight
        if tax_end_day < len(presale_df):
            fig_daily_sales.add_vrect(
                x0=0, x1=tax_end_day,
                fillcolor=NXID_COLORS['tax'], opacity=0.15,
                annotation_text=f"Tax Period ({self.config.tax_rate_total}%)",
                annotation_position="top left",
                annotation_font=dict(color=NXID_COLORS['tax'], size=14)
            )
        
        fig_daily_sales.update_layout(
            title=dict(text='<b>📊 Daily Token Sales Volume - Detailed Analysis (Bar Chart)</b>', x=0.5,
                      font=dict(size=28, color=NXID_COLORS['primary'])),
            xaxis_title="Presale Day",
            yaxis_title="Daily Sales Volume (Million NXID)",
            **chart_template, height=600
        )
        charts['daily_sales'] = fig_daily_sales
        
        # === 4. YENİ: RASTGELE INVESTOR ROI ANALİZİ ===
        fig_investor_roi = make_subplots(
            rows=2, cols=1,
            subplot_titles=[' Random Investor ROI Timeline (Line Chart)', '📊 ROI Distribution by Investment Day (Scatter)'],
            vertical_spacing=0.15
        )
        
        # ROI timeline for different investors
        unique_investors = investor_analysis_df['investor_id'].unique()
        colors_cycle = [NXID_COLORS['primary'], NXID_COLORS['success'], NXID_COLORS['gold'], 
                       NXID_COLORS['purple'], NXID_COLORS['teal'], NXID_COLORS['orange']]
        
        for i, investor in enumerate(unique_investors[:6]):  # İlk 6 investor
            investor_data = investor_analysis_df[investor_analysis_df['investor_id'] == investor]
            market_data = investor_data[investor_data['evaluation_type'] == 'Market'].sort_values('evaluation_point')
            
            if len(market_data) > 0:
                fig_investor_roi.add_trace(
                    go.Scatter(
                        x=[int(pt.split('_')[1]) for pt in market_data['evaluation_point']],
                        y=market_data['roi_percentage'],
                        mode='lines+markers',
                        name=f"{investor} (Day {investor_data.iloc[0]['investment_day']})",
                        line=dict(color=colors_cycle[i % len(colors_cycle)], width=3),
                        hovertemplate=f'<b>{investor}</b><br>Month: %{{x}}<br>ROI: %{{y:.1f}}%<extra></extra>'
                    ), row=1, col=1
                )
        
        # ROI distribution scatter
        presale_end_data = investor_analysis_df[investor_analysis_df['evaluation_point'] == 'Presale_End']
        fig_investor_roi.add_trace(
            go.Scatter(
                x=presale_end_data['investment_day'],
                y=presale_end_data['roi_percentage'],
                mode='markers',
                name='Presale End ROI',
                marker=dict(
                    size=presale_end_data['investment_amount_usdt']/100,
                    color=presale_end_data['roi_percentage'],
                    colorscale='Viridis',
                    colorbar=dict(title="ROI %"),
                    line=dict(color=NXID_COLORS['light'], width=1)
                ),
                hovertemplate='<b>%{text}</b><br>Investment Day: %{x}<br>Investment: $%{customdata:.0f}<br>ROI: %{y:.1f}%<extra></extra>',
                text=presale_end_data['investor_id'],
                customdata=presale_end_data['investment_amount_usdt']
            ), row=2, col=1
        )
        
        fig_investor_roi.update_layout(
            title=dict(text='<b>📊 Random Investor ROI Analysis (Multi-Chart)</b>', x=0.5,
                      font=dict(size=28, color=NXID_COLORS['primary'])),
            **chart_template, height=700
        )
        charts['investor_roi'] = fig_investor_roi
        
        # === 5. PRESALE + TAX ANALİTİĞİ (GELİŞMİŞ) ===
        fig_presale = make_subplots(
            rows=2, cols=2,
            subplot_titles=[' Daily Sales & Price (Line+Area)', '💰 Cumulative Metrics (Line)', 
                          '🔥 Tax System Impact (Bar+Line)', '⚡  APY Evolution (Area+Line)'],
            specs=[[{"secondary_y": True}, {"secondary_y": True}],
                   [{"secondary_y": True}, {"secondary_y": True}]],
            vertical_spacing=0.15,
            horizontal_spacing=0.12
        )
        
        # Sales and price
        fig_presale.add_trace(
            go.Scatter(x=presale_df['day'], y=presale_df['daily_tokens_sold']/1e6,
                      name='Daily Sales (M)', line=dict(color=NXID_COLORS['success'], width=3),
                      fill='tonexty', fillcolor=f"rgba{hex_to_rgb(NXID_COLORS['success']) + (0.3,)}"),
            row=1, col=1
        )
        fig_presale.add_trace(
            go.Scatter(x=presale_df['day'], y=presale_df['price_usdt'],
                      name='Price (USDT)', line=dict(color=NXID_COLORS['warning'], width=2)),
            row=1, col=1, secondary_y=True
        )
        
        # Cumulative metrics
        fig_presale.add_trace(
            go.Scatter(x=presale_df['day'], y=presale_df['cumulative_raised_usdt']/1e6,
                      name='Raised (M USDT)', line=dict(color=NXID_COLORS['primary'], width=3)),
            row=1, col=2
        )
        fig_presale.add_trace(
            go.Scatter(x=presale_df['day'], y=presale_df['cumulative_sold_tokens']/1e9,
                      name='Sold (B NXID)', line=dict(color=NXID_COLORS['accent'], width=2)),
            row=1, col=2, secondary_y=True
        )
        
        # Tax system
        if 'daily_tax_tokens' in presale_df.columns:
            fig_presale.add_trace(
                go.Bar(x=presale_df['day'], y=presale_df['daily_tax_tokens']/1e6,
                      name='Daily Tax (M)', marker_color=NXID_COLORS['tax']),
                row=2, col=1
            )
            fig_presale.add_trace(
                go.Scatter(x=presale_df['day'], y=presale_df['total_tax_burned']/1e6,
                          name='Tax Burned (M)', line=dict(color=NXID_COLORS['burn'], width=3)),
                row=2, col=1, secondary_y=True
            )
        
        #  APY evolution with minimum APY line
        fig_presale.add_trace(
            go.Scatter(x=presale_df['day'], y=presale_df['current_apy'],
                      name='Current APY (%)', line=dict(color=NXID_COLORS['gold'], width=4),
                      fill='tonexty', fillcolor=f"rgba{hex_to_rgb(NXID_COLORS['gold']) + (0.2,)}"),
            row=2, col=2
        )
        
        # Minimum APY reference line
        fig_presale.add_hline(
            y=self.config.minimum_staking_apy,
            line_dash="dash", line_color=NXID_COLORS['danger'], line_width=2,
            annotation_text=f"Min APY: {self.config.minimum_staking_apy}%",
            annotation_position="top right"
        )
        
        # Using presale tokens indicator
        if 'using_presale_tokens' in presale_df.columns:
            using_days = presale_df[presale_df['using_presale_tokens'] == True]['day']
            if len(using_days) > 0:
                fig_presale.add_trace(
                    go.Scatter(x=using_days, y=[self.config.minimum_staking_apy] * len(using_days),
                              mode='markers', name='Using Presale Tokens', 
                              marker=dict(color=NXID_COLORS['danger'], size=8, symbol='star')),
                    row=2, col=2, secondary_y=True
                )
        
        fig_presale.update_layout(
            title=dict(text='<b>📊  Presale + Tax + Minimum APY Analytics (Multi-Chart)</b>', x=0.5, 
                      font=dict(size=28, color=NXID_COLORS['primary'])),
            **chart_template, height=700, showlegend=True
        )
        charts['presale'] = fig_presale
        
        # === 6. CIRCULATING SUPPLY & BURN ANALYSIS ===
        fig_supply = make_subplots(
            rows=2, cols=1,
            subplot_titles=[' Circulating Supply Evolution (Line Chart)', '🔥 Burn Analysis & Supply Reduction (Area Chart)'],
            specs=[[{"secondary_y": True}], [{"secondary_y": True}]],
            vertical_spacing=0.15
        )
        
        # Circulating supply
        fig_supply.add_trace(
            go.Scatter(x=projection_df['months'], y=projection_df['circulating_supply']/1e9,
                      name='Circulating Supply (B)', 
                      line=dict(color=NXID_COLORS['primary'], width=4),
                      fill='tonexty', fillcolor=f"rgba{hex_to_rgb(NXID_COLORS['primary']) + (0.2,)}"),
            row=1, col=1
        )
        
        # Circulating percentage
        fig_supply.add_trace(
            go.Scatter(x=projection_df['months'], y=projection_df['circulating_percentage'],
                      name='Circulating %', 
                      line=dict(color=NXID_COLORS['accent'], width=3)),
            row=1, col=1, secondary_y=True
        )
        
        # Burned tokens breakdown
        fig_supply.add_trace(
            go.Scatter(x=projection_df['months'], y=projection_df['routine_burned']/1e9,
                      name='Routine Burn (B)', 
                      line=dict(color=NXID_COLORS['burn'], width=3),
                      fill='tonexty', fillcolor=f"rgba{hex_to_rgb(NXID_COLORS['burn']) + (0.3,)}"),
            row=2, col=1
        )
        
        fig_supply.add_trace(
            go.Scatter(x=projection_df['months'], y=projection_df['tax_burned']/1e9,
                      name='Tax Burn (B)', 
                      line=dict(color=NXID_COLORS['tax'], width=3),
                      fill='tonexty', fillcolor=f"rgba{hex_to_rgb(NXID_COLORS['tax']) + (0.3,)}"),
            row=2, col=1
        )
        
        # Total burn percentage
        fig_supply.add_trace(
            go.Scatter(x=projection_df['months'], y=projection_df['burn_rate_percentage'],
                      name='Total Burned %', 
                      line=dict(color=NXID_COLORS['danger'], width=3)),
            row=2, col=1, secondary_y=True
        )
        
        fig_supply.update_layout(
            title=dict(text='<b>📊 Circulating Supply & Burn Analysis (Multi-Chart)</b>', x=0.5,
                      font=dict(size=28, color=NXID_COLORS['primary'])),
            **chart_template, height=700
        )
        charts['supply'] = fig_supply
        
        # === 7. KOMPLEKS MARKET CAP PROJEKSİYONU ===
        fig_market = make_subplots(
            rows=2, cols=2,
            subplot_titles=[' Token Price Evolution (Line)', '💎 Market Cap Growth (Area)', 
                          '🔄 Complex Market Factors (Line)', '📊 Supply Dynamics (Stacked Area)'],
            specs=[[{"secondary_y": True}, {"secondary_y": True}],
                   [{"secondary_y": False}, {"secondary_y": True}]],
            vertical_spacing=0.15,
            horizontal_spacing=0.12
        )
        
        # Price evolution
        fig_market.add_trace(
            go.Scatter(x=projection_df['months'], y=projection_df['token_price'],
                      name='Token Price', line=dict(color=NXID_COLORS['primary'], width=4)),
            row=1, col=1
        )
        fig_market.add_trace(
            go.Scatter(x=projection_df['months'], y=projection_df['price_vs_presale'],
                      name='vs Presale (x)', line=dict(color=NXID_COLORS['success'], width=3)),
            row=1, col=1, secondary_y=True
        )
        
        # Market cap
        fig_market.add_trace(
            go.Scatter(x=projection_df['months'], y=projection_df['mcap_usdt']/1e6,
                      name='Market Cap (M)', line=dict(color=NXID_COLORS['gold'], width=4),
                      fill='tonexty', fillcolor=f"rgba{hex_to_rgb(NXID_COLORS['gold']) + (0.2,)}"),
            row=1, col=2
        )
        
        # Complex market factors
        fig_market.add_trace(
            go.Scatter(x=projection_df['months'], y=projection_df['institutional_effect'],
                      name='Institutional', line=dict(color=NXID_COLORS['indigo'], width=2)),
            row=2, col=1
        )
        fig_market.add_trace(
            go.Scatter(x=projection_df['months'], y=projection_df['fomo_cycle'],
                      name='FOMO Cycle', line=dict(color=NXID_COLORS['pink'], width=2)),
            row=2, col=1
        )
        fig_market.add_trace(
            go.Scatter(x=projection_df['months'], y=projection_df['bear_cycle'],
                      name='Bear Resistance', line=dict(color=NXID_COLORS['warning'], width=2)),
            row=2, col=1
        )
        
        # Supply dynamics
        fig_market.add_trace(
            go.Scatter(x=projection_df['months'], y=projection_df['presale_supply']/1e9,
                      name='Presale Supply', fill='tonexty', stackgroup='supply',
                      line=dict(color=NXID_COLORS['primary'], width=1)),
            row=2, col=2
        )
        fig_market.add_trace(
            go.Scatter(x=projection_df['months'], y=projection_df['vested_supply']/1e9,
                      name='Vested Supply', fill='tonexty', stackgroup='supply',
                      line=dict(color=NXID_COLORS['teal'], width=1)),
            row=2, col=2
        )
        
        fig_market.update_layout(
            title=dict(text='<b>📊 Complex Market Cap & Price Projection v3.1 (Multi-Chart)</b>', x=0.5,
                      font=dict(size=28, color=NXID_COLORS['primary'])),
            **chart_template, height=800
        )
        charts['market'] = fig_market
        
        # === 8. STAKING ECOSYSTEM ===
        fig_staking = make_subplots(
            rows=2, cols=1,
            subplot_titles=['⚡ Staking Participation & APY (Line+Area)', '🏆  Reward Distribution (Line+Bar)'],
            specs=[[{"secondary_y": True}], [{"secondary_y": True}]],
            vertical_spacing=0.15
        )
        
        # Staking participation
        fig_staking.add_trace(
            go.Scatter(x=staking_df['months'], y=staking_df['staking_ratio']*100,
                      name='Staking Ratio (%)', 
                      line=dict(color=NXID_COLORS['teal'], width=4),
                      fill='tonexty', fillcolor=f"rgba{hex_to_rgb(NXID_COLORS['teal']) + (0.2,)}"),
            row=1, col=1
        )
        fig_staking.add_trace(
            go.Scatter(x=staking_df['months'], y=staking_df['current_market_apy'],
                      name='Market APY (%)', 
                      line=dict(color=NXID_COLORS['gold'], width=3)),
            row=1, col=1, secondary_y=True
        )
        
        #  reward distribution
        fig_staking.add_trace(
            go.Scatter(x=staking_df['months'], y=staking_df['distributed_rewards']/1e9,
                      name='Distributed (B)', 
                      line=dict(color=NXID_COLORS['success'], width=4)),
            row=2, col=1
        )
        fig_staking.add_trace(
            go.Scatter(x=staking_df['months'], y=staking_df['remaining_staking_pool']/1e9,
                      name='Remaining Pool (B)', 
                      line=dict(color=NXID_COLORS['danger'], width=3)),
            row=2, col=1, secondary_y=True
        )
        
        # Tax contribution indicator
        if 'tax_contribution' in staking_df.columns and staking_df['tax_contribution'].iloc[0] > 0:
            fig_staking.add_hline(
                y=staking_df['tax_contribution'].iloc[0]/1e9,
                line_dash="dot", line_color=NXID_COLORS['tax'], line_width=2,
                annotation_text=f"Tax Contribution: {staking_df['tax_contribution'].iloc[0]/1e6:.1f}M",
                annotation_position="top left"
            )
        
        fig_staking.update_layout(
            title=dict(text='<b>📊 Post-Launch Staking Ecosystem v3.1 (Multi-Chart)</b>', x=0.5,
                      font=dict(size=28, color=NXID_COLORS['primary'])),
            **chart_template, height=700
        )
        charts['staking'] = fig_staking
        
        return charts
    
    def calculate__metrics(self, presale_df: pd.DataFrame, 
                                 vesting_df: pd.DataFrame,
                                 projection_df: pd.DataFrame, 
                                 staking_df: pd.DataFrame,
                                 investor_analysis_df: pd.DataFrame) -> Dict:
        """📊 Kapsamlı gelişmiş metrikleri hesapla v3.1"""
        
        try:
            # Presale Performance Metrikleri
            presale_metrics = {
                'total_raised_usdt': float(presale_df['cumulative_raised_usdt'].iloc[-1]),
                'tokens_sold': float(presale_df['cumulative_sold_tokens'].iloc[-1]),
                'final_presale_price': float(presale_df['price_usdt'].iloc[-1]),
                'price_appreciation_during_presale': float(presale_df['price_appreciation'].iloc[-1]),
                'presale_duration_days': len(presale_df),
                'pool_depletion_percentage': float(presale_df['pool_depletion_percentage'].iloc[-1]),
                'average_apy': float(presale_df['current_apy'].mean()),
                'final_apy': float(presale_df['current_apy'].iloc[-1]),
                'total_rewards_distributed': float(presale_df['total_rewards_distributed'].iloc[-1]),
                'tokens_sold_percentage': float(presale_df['tokens_sold_percentage'].iloc[-1]),
                
                # Tax metrics
                'total_tax_collected': float(presale_df['total_tax_collected'].iloc[-1]) if 'total_tax_collected' in presale_df.columns else 0,
                'total_tax_to_staking': float(presale_df['total_tax_to_staking'].iloc[-1]) if 'total_tax_to_staking' in presale_df.columns else 0,
                'total_tax_burned': float(presale_df['total_tax_burned'].iloc[-1]) if 'total_tax_burned' in presale_df.columns else 0,
                'tax_effectiveness': float((presale_df['total_tax_collected'].iloc[-1] / presale_df['cumulative_sold_tokens'].iloc[-1]) * 100) if 'total_tax_collected' in presale_df.columns and presale_df['cumulative_sold_tokens'].iloc[-1] > 0 else 0,
                
                # YENİ: Minimum APY sistemi metrikleri
                'presale_tokens_used_for_rewards': float(presale_df['presale_tokens_used_for_rewards'].iloc[-1]) if 'presale_tokens_used_for_rewards' in presale_df.columns else 0,
                'minimum_apy_usage_days': int(presale_df['using_presale_tokens'].sum()) if 'using_presale_tokens' in presale_df.columns else 0,
                'effective_reward_pool_final': float(presale_df['effective_reward_pool'].iloc[-1]) if 'effective_reward_pool' in presale_df.columns else 0
            }
            
            # Pazar Projeksiyon Metrikleri
            max_price_idx = projection_df['token_price'].idxmax()
            max_mcap_idx = projection_df['mcap_usdt'].idxmax()
            
            projection_metrics = {
                'launch_mcap': float(projection_df['mcap_usdt'].iloc[0]),
                'max_projected_price': float(projection_df['token_price'].iloc[max_price_idx]),
                'max_price_timing_months': float(projection_df['months'].iloc[max_price_idx]),
                'max_mcap': float(projection_df['mcap_usdt'].iloc[max_mcap_idx]),
                'max_mcap_timing_months': float(projection_df['months'].iloc[max_mcap_idx]),
                'price_appreciation_vs_presale': float(projection_df['price_vs_presale'].iloc[max_price_idx]),
                'final_circulating_supply': float(projection_df['circulating_supply'].iloc[-1]),
                'total_burned_tokens': float(projection_df['total_burned'].iloc[-1]),
                'final_token_price': float(projection_df['token_price'].iloc[-1]),
                'mcap_growth_vs_launch': float(projection_df['mcap_vs_launch'].iloc[max_mcap_idx]),
                'max_burn_percentage': float(projection_df['burn_rate_percentage'].max()),
                'final_circulating_percentage': float(projection_df['circulating_percentage'].iloc[-1])
            }
            
            # Staking Ekosistem Metrikleri
            staking_metrics = {
                'max_staking_ratio': float(staking_df['staking_ratio'].max()),
                'average_market_apy': float(staking_df['current_market_apy'].mean()),
                'total_market_rewards': float(staking_df['distributed_rewards'].iloc[-1]),
                'final_staked_tokens': float(staking_df['cumulative_staked'].iloc[-1]),
                'peak_staking_participation': float(staking_df['participation_rate'].max()),
                'staking_pool_depletion': float((staking_df['distributed_rewards'].iloc[-1] / staking_df['total_staking_pool'].iloc[0]) * 100) if staking_df['total_staking_pool'].iloc[0] > 0 else 0,
                'tax_staking_contribution': float(staking_df['tax_contribution'].iloc[0]) if 'tax_contribution' in staking_df.columns else 0
            }
            
            # Vesting Analiz Metrikleri
            vesting_metrics = {
                'team_fully_vested_month': self.config.team_cliff_months + self.config.team_vesting_months,
                'dao_fully_vested_month': self.config.dao_cliff_months + self.config.dao_vesting_months,
                'marketing_fully_vested_month': self.config.marketing_cliff_months + self.config.marketing_vesting_months,
                'total_released_at_24_months': float(vesting_df.iloc[min(23, len(vesting_df)-1)]['total_vested']) if len(vesting_df) > 23 else 0,
                'circulating_at_24_months': float(vesting_df.iloc[min(23, len(vesting_df)-1)]['circulating_supply']) if len(vesting_df) > 23 else 0,
                'vesting_completion_percentage_24m': float(vesting_df.iloc[min(23, len(vesting_df)-1)]['vested_percentage_of_total_supply']) if len(vesting_df) > 23 else 0,
                'circulating_percentage_24m': float(vesting_df.iloc[min(23, len(vesting_df)-1)]['circulating_percentage']) if len(vesting_df) > 23 else 0
            }
            
            # YENİ: Investor Analiz Metrikleri
            investor_metrics = {
                'average_presale_end_roi': float(investor_analysis_df[investor_analysis_df['evaluation_point'] == 'Presale_End']['roi_percentage'].mean()),
                'max_presale_end_roi': float(investor_analysis_df[investor_analysis_df['evaluation_point'] == 'Presale_End']['roi_percentage'].max()),
                'min_presale_end_roi': float(investor_analysis_df[investor_analysis_df['evaluation_point'] == 'Presale_End']['roi_percentage'].min()),
                'best_investment_day': int(investor_analysis_df[investor_analysis_df['evaluation_point'] == 'Presale_End'].loc[investor_analysis_df[investor_analysis_df['evaluation_point'] == 'Presale_End']['roi_percentage'].idxmax()]['investment_day']),
                'worst_investment_day': int(investor_analysis_df[investor_analysis_df['evaluation_point'] == 'Presale_End'].loc[investor_analysis_df[investor_analysis_df['evaluation_point'] == 'Presale_End']['roi_percentage'].idxmin()]['investment_day']),
                'total_simulated_investors': len(investor_analysis_df['investor_id'].unique())
            }
            
            return {
                'presale': presale_metrics,
                'projection': projection_metrics,
                'staking': staking_metrics,
                'vesting': vesting_metrics,
                'investor': investor_metrics
            }
            
        except Exception as e:
            st.error(f"Gelişmiş metrik hesaplama hatası: {e}")
            return {'error': str(e)}

def display_nxid_logo(width=120):
    """NXID logosu göster - dosya bazlı approach"""
    try:
        # Önce PNG dosyasını dene
        if os.path.exists("nxid-logo.png"):
            import base64
            with open("nxid-logo.png", "rb") as f:
                img_data = base64.b64encode(f.read()).decode()
            return f'<img src="data:image/png;base64,{img_data}" width="{width}" height="{width}" alt="NXID Logo" style="border-radius: 50%; box-shadow: 0 0 30px rgba(27, 142, 242, 0.5);">'
        
        # Sonra SVG dosyasını dene
        elif os.path.exists("NXID-logo.svg"):
            with open("NXID-logo.svg", "r", encoding="utf-8") as f:
                svg_content = f.read()
            import base64
            svg_base64 = base64.b64encode(svg_content.encode('utf-8')).decode('utf-8')
            return f'<img src="data:image/svg+xml;base64,{svg_base64}" width="{width}" height="{width}" alt="NXID Logo" style="border-radius: 50%; box-shadow: 0 0 30px rgba(27, 142, 242, 0.5);">'
        
        # Dosya yoksa SVG fallback
        else:
            svg_content = f'''
            <svg width="{width}" height="{width}" viewBox="0 0 120 120" fill="none" xmlns="http://www.w3.org/2000/svg">
                <defs>
                    <linearGradient id="nxidGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" style="stop-color:#1B8EF2;stop-opacity:1" />
                        <stop offset="30%" style="stop-color:#7AC3FF;stop-opacity:1" />
                        <stop offset="70%" style="stop-color:#3effc8;stop-opacity:1" />
                        <stop offset="100%" style="stop-color:#1B8EF2;stop-opacity:0.8" />
                    </linearGradient>
                    <filter id="glow">
                        <feGaussianBlur stdDeviation="4" result="coloredBlur"/>
                        <feMerge> 
                            <feMergeNode in="coloredBlur"/>
                            <feMergeNode in="SourceGraphic"/>
                        </feMerge>
                    </filter>
                </defs>
                <circle cx="60" cy="60" r="55" fill="url(#nxidGradient)" stroke="#1B8EF2" stroke-width="3" filter="url(#glow)"/>
                <circle cx="60" cy="60" r="45" fill="none" stroke="#3effc8" stroke-width="1" opacity="0.5"/>
                <text x="60" y="72" font-family="Orbitron, monospace" font-size="24" font-weight="900" 
                      fill="#0B1426" text-anchor="middle" dominant-baseline="middle">NXID</text>
            </svg>
            '''
            
            import base64
            svg_base64 = base64.b64encode(svg_content.encode('utf-8')).decode('utf-8')
            return f'<img src="data:image/svg+xml;base64,{svg_base64}" width="{width}" height="{width}" alt="NXID Logo" style="border-radius: 50%; box-shadow: 0 0 30px rgba(27, 142, 242, 0.5);">'
            
    except Exception as e:
        # Final CSS fallback
        return f'''<div style="width: {width}px; height: {width}px; background: linear-gradient(135deg, #1B8EF2, #7AC3FF, #3effc8); border-radius: 50%; display: flex; align-items: center; justify-content: center; box-shadow: 0 0 30px rgba(27, 142, 242, 0.5); border: 3px solid #1B8EF2;">
                      <span style="font-family: Orbitron, monospace; font-weight: 900; color: #0B1426; font-size: {width//4}px;">NXID</span>
                   </div>'''

def hex_to_rgb(hex_color):
    """Hex rengi RGB tuple'a dönüştür"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def load__css():
    """NXID markalaması ile gelişmiş özel CSS yükle v3.1"""
    primary_rgb = hex_to_rgb(NXID_COLORS['primary'])
    secondary_rgb = hex_to_rgb(NXID_COLORS['secondary'])
    
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
        background: linear-gradient(135deg, {NXID_COLORS['primary']}, {NXID_COLORS['secondary']}) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
        margin-bottom: 1rem !important;
        text-shadow: 0 0 30px rgba({primary_rgb[0]}, {primary_rgb[1]}, {primary_rgb[2]}, 0.5) !important;
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
        border-color: {NXID_COLORS['secondary']};
    }}
    
    .stSidebar {{
        background: linear-gradient(180deg, rgba({primary_rgb[0]}, {primary_rgb[1]}, {primary_rgb[2]}, 0.1), rgba(0,0,0,0.3));
        border-right: 2px solid rgba({primary_rgb[0]}, {primary_rgb[1]}, {primary_rgb[2]}, 0.3);
    }}
    
    .stButton > button {{
        background: linear-gradient(135deg, {NXID_COLORS['primary']}, {NXID_COLORS['secondary']});
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
        box-shadow: 0 12px 35px rgba({primary_rgb[0]}, {primary_rgb[1]}, {primary_rgb[2]}, 0.6);
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
        background: linear-gradient(135deg, {NXID_COLORS['primary']}, {NXID_COLORS['secondary']});
        color: {NXID_COLORS['darker']};
        border-color: {NXID_COLORS['accent']};
    }}
    
    /* JSON config styling */
    .config-section {{
        background: rgba({primary_rgb[0]}, {primary_rgb[1]}, {primary_rgb[2]}, 0.1);
        border: 1px solid rgba({primary_rgb[0]}, {primary_rgb[1]}, {primary_rgb[2]}, 0.3);
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
    }}
    </style>
    """, unsafe_allow_html=True)

def main():
    """ Gelişmiş Ana Uygulama v3.1"""
    
    load__css()
    
    # NXID Logo ile başlık
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
               background: linear-gradient(135deg, {NXID_COLORS['primary']}, {NXID_COLORS['secondary']}); 
               -webkit-background-clip: text; -webkit-text-fill-color: transparent; 
               margin-bottom: 1rem;">NXID ADVANCED TOKENOMICS v3.1</h1>
    ''', unsafe_allow_html=True)
    
    st.markdown(f'''
    <div style="text-align: center; margin: 1.5rem 0; padding: 1rem; 
                background: rgba({hex_to_rgb(NXID_COLORS['primary'])[0]}, {hex_to_rgb(NXID_COLORS['primary'])[1]}, {hex_to_rgb(NXID_COLORS['primary'])[2]}, 0.1); 
                border-radius: 15px; border: 1px solid rgba({hex_to_rgb(NXID_COLORS['primary'])[0]}, {hex_to_rgb(NXID_COLORS['primary'])[1]}, {hex_to_rgb(NXID_COLORS['primary'])[2]}, 0.3);">
        <p style="color: {NXID_COLORS['light']}; font-family: Inter; margin: 0; font-size: 1.1rem; font-weight: 500;">
            <strong style="color: {NXID_COLORS['secondary']};">Next Digital ID (NXID)</strong> • 
            <span style="color: {NXID_COLORS['accent']};">BNB Chain (BEP-20)</span> • 
            <strong style="color: {NXID_COLORS['gold']};">100B Toplam Arz</strong>
        </p>
    </div>
    ''', unsafe_allow_html=True)
    
    st.markdown(f'''
    <p style="text-align: center; color: {NXID_COLORS['gray']}; font-size: 1.3rem; 
               font-family: Inter; margin-bottom: 2rem; font-weight: 500;">
         Minimum APY • Daily Sales Analytics • Random Investor ROI • JSON Config • v3.1
    </p>
    <div style="width: 100%; height: 3px; background: linear-gradient(90deg, {NXID_COLORS['primary']}, {NXID_COLORS['secondary']}); 
                margin: 2rem auto; border-radius: 2px;"></div>
    ''', unsafe_allow_html=True)
    
    # === JSON CONFIG YÖNETİMİ ===
    sidebar_logo = display_nxid_logo(80)
    st.sidebar.markdown(f'''
    <div style="text-align: center; margin-bottom: 2rem;">
        {sidebar_logo}
        <h2 style="color: {NXID_COLORS['primary']}; font-family: Orbitron; font-size: 1.4rem; margin: 1rem 0 0 0;">
            NXID Config v3.1
        </h2>
        <p style="color: {NXID_COLORS['gray']}; font-size: 0.9rem; margin: 0.5rem 0 0 0;">
            Next Digital ID (NXID)<br>
             JSON Configuration
        </p>
    </div>
    ''', unsafe_allow_html=True)
    
    # JSON Config Management
    with st.sidebar.expander("📁 JSON Config Yönetimi", expanded=True):
        st.markdown("**Config Dosya İşlemleri:**")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 Config Kaydet", use_container_width=True):
                if 'current_config' in st.session_state:
                    if st.session_state.current_config.save_to_json():
                        st.success("✅ Config kaydedildi!")
                    else:
                        st.error("❌ Kaydetme hatası!")
                else:
                    st.warning("⚠️ Önce config oluşturun")
        
        with col2:
            if st.button("📁 Config Yükle", use_container_width=True):
                try:
                    loaded_config = NXIDConfig.load_from_json()
                    st.session_state.current_config = loaded_config
                    st.success("✅ Config yüklendi!")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Yükleme hatası: {e}")
        
        # Config dosyası var mı kontrol et
        if os.path.exists("nxid_config.json"):
            st.info("📄 Config dosyası mevcut")
            try:
                with open("nxid_config.json", "r") as f:
                    config_data = json.load(f)
                st.markdown(f"**Son değişiklik**: Min APY: {config_data.get('minimum_staking_apy', 0):.0f}%")
            except:
                pass
        else:
            st.warning("📄 Config dosyası bulunamadı")
    
    # Config yükleme veya yeni oluşturma
    if 'current_config' not in st.session_state:
        st.session_state.current_config = NXIDConfig.load_from_json()
    
    config = st.session_state.current_config
    
    # === PROJECTION CONTROL ===
    with st.sidebar.expander("📊 Analiz Zaman Çerçeveleri"):
        config.projection_months = st.slider("Market Projeksiyon (ay)", 12, 60, config.projection_months, 3)
        config.vesting_analysis_months = st.slider("Vesting Analiz (ay)", 12, 120, config.vesting_analysis_months, 6)
        
        if st.button("📊 Zaman Çerçevelerini Kaydet"):
            config.save_to_json()
            st.success("✅ Zaman ayarları kaydedildi!")
    
    # === TOKEN DAĞITIMI ===
    with st.sidebar.expander("💰 Token Dağıtımı", expanded=True):
        config.presale_allocation = st.number_input("Presale Tahsisi %", 0.0, 100.0, config.presale_allocation, 0.1)
        config.presale_staking_pool = st.number_input("Presale Staking Pool %", 0.0, 100.0, config.presale_staking_pool, 0.1)
        config.market_staking_pool = st.number_input("Market Staking Pool %", 0.0, 100.0, config.market_staking_pool, 0.1)
        config.team_allocation = st.number_input("Team Tahsisi %", 0.0, 100.0, config.team_allocation, 0.1)
        config.dao_treasury = st.number_input("DAO Treasury %", 0.0, 100.0, config.dao_treasury, 0.1)
        config.marketing = st.number_input("Marketing %", 0.0, 100.0, config.marketing, 0.1)
        config.liquidity = st.number_input("Liquidity %", 0.0, 100.0, config.liquidity, 0.1)
        
        total_allocation = (config.presale_allocation + config.presale_staking_pool + 
                          config.market_staking_pool + config.team_allocation + 
                          config.dao_treasury + config.marketing + config.liquidity)
        
        if abs(total_allocation - 100) < 0.1:
            st.success(f"✅ Mükemmel! Toplam: {total_allocation:.1f}%")
        else:
            st.error(f"❌ Toplam: {total_allocation:.1f}% (100% olmalı)")
    
    # ===  APY SİSTEMİ ===
    with st.sidebar.expander("⚡  APY Sistemi", expanded=True):
        config.max_apy = st.number_input("Maximum APY %", 100.0, 5000.0, config.max_apy, 10.0)
        config.minimum_staking_apy = st.number_input("Minimum Staking APY % (YENİ)", 10.0, 500.0, config.minimum_staking_apy, 5.0)
        
        st.info(f"""
        💡 ** APY Sistemi:**
        APY {config.minimum_staking_apy}%'nin altına düştüğünde,
        presale tokenlerinden otomatik dağıtım yapılır.
        """)
    
    # === TAX SİSTEMİ ===
    with st.sidebar.expander("🔥 Tax Sistemi & Burn"):
        config.tax_period_months = st.number_input("Tax Dönemi (ay)", 1, 12, config.tax_period_months)
        config.tax_rate_total = st.number_input("Toplam Tax Oranı %", 0.0, 10.0, config.tax_rate_total, 0.1)
        config.tax_to_staking_percentage = st.number_input("Tax → Staking %", 0.0, 100.0, config.tax_to_staking_percentage, 1.0)
        config.tax_to_burn_percentage = st.number_input("Tax → Burn %", 0.0, 100.0, config.tax_to_burn_percentage, 1.0)
        
        tax_total = config.tax_to_staking_percentage + config.tax_to_burn_percentage
        if abs(tax_total - 100) < 0.1:
            st.success(f"✅ Tax dağıtımı: {tax_total:.1f}%")
        else:
            st.error(f"❌ Tax dağıtımı: {tax_total:.1f}% (100% olmalı)")
        
        config.annual_burn_rate = st.number_input("Yıllık Burn Oranı", 0.001, 0.1, config.annual_burn_rate, 0.001)
        config.burn_duration_years = st.number_input("Burn Süresi (yıl)", 1, 10, config.burn_duration_years)
    
    # === PRESALE PARAMETRELERİ ===
    with st.sidebar.expander(" Presale Yapılandırması"):
        config.presale_days = st.number_input("Presale Süresi (Gün)", 1, 1000, config.presale_days)
        config.start_price_usdt = st.number_input("Başlangıç Fiyatı", 0.00001, 1.0, config.start_price_usdt, 0.00001, format="%.5f")
        config.daily_price_increase = st.number_input("Günlük Fiyat Artışı %", 0.0, 10.0, config.daily_price_increase, 0.001)
        config.base_daily_demand_usdt = st.number_input("Günlük Talep USDT", 100.0, 100000.0, float(config.base_daily_demand_usdt))
        config.demand_growth_rate = st.number_input("Talep Büyüme Oranı", 1.0, 2.0, config.demand_growth_rate, 0.001)
        config.demand_volatility = st.number_input("Talep Volatilitesi", 0.0, 1.0, config.demand_volatility, 0.001)
    
    # === KOMPLEKS MARKET CAP ===
    with st.sidebar.expander(" Kompleks Market Cap Algoritması"):
        config.launch_mcap_multiplier = st.number_input("Launch McAp Çarpanı", 5.0, 50.0, config.launch_mcap_multiplier, 0.5)
        config.peak_mcap_multiplier = st.number_input("Zirve McAp Çarpanı", 50.0, 500.0, config.peak_mcap_multiplier, 10.0)
        config.institutional_adoption_factor = st.number_input("Kurumsal Faktör", 1.0, 3.0, config.institutional_adoption_factor, 0.1)
        config.retail_fomo_multiplier = st.number_input("FOMO Çarpanı", 1.0, 5.0, config.retail_fomo_multiplier, 0.1)
        config.bear_market_resistance = st.number_input("Bear Market Direnci", 0.1, 1.0, config.bear_market_resistance, 0.05)
        config.utility_growth_factor = st.number_input("Utility Büyüme", 1.0, 3.0, config.utility_growth_factor, 0.1)
        config.competition_factor = st.number_input("Rekabet Faktörü", 0.5, 1.0, config.competition_factor, 0.05)
    
    # === STAKING PARAMETRELERİ ===
    with st.sidebar.expander("⚡ Staking Yapılandırması"):
        config.market_staking_years = st.number_input("Staking Süresi (yıl)", 5, 20, config.market_staking_years)
        config.base_staking_participation = st.number_input("Temel Staking Oranı", 0.1, 0.8, config.base_staking_participation, 0.05)
        config.max_staking_participation = st.number_input("Max Staking Oranı", 0.6, 0.95, config.max_staking_participation, 0.05)
        config.base_market_apy = st.number_input("Temel Market APY %", 10.0, 200.0, config.base_market_apy, 5.0)
        config.min_market_apy = st.number_input("Min Market APY %", 1.0, 50.0, config.min_market_apy, 1.0)
    
    # === VESTING PLANLARI ===
    with st.sidebar.expander("📅 Vesting Planları"):
        st.markdown("**Team Vesting:**")
        config.team_cliff_months = st.number_input("Team Cliff (ay)", 0, 60, config.team_cliff_months)
        config.team_vesting_months = st.number_input("Team Vesting (ay)", 1, 120, config.team_vesting_months)
        
        st.markdown("**DAO Vesting:**")
        config.dao_cliff_months = st.number_input("DAO Cliff (ay)", 0, 48, config.dao_cliff_months)
        config.dao_vesting_months = st.number_input("DAO Vesting (ay)", 1, 96, config.dao_vesting_months)
        
        st.markdown("**Marketing Vesting:**")
        config.marketing_cliff_months = st.number_input("Marketing Cliff (ay)", 0, 36, config.marketing_cliff_months)
        config.marketing_vesting_months = st.number_input("Marketing Vesting (ay)", 1, 60, config.marketing_vesting_months)
    
    # Update session state
    st.session_state.current_config = config
    
    # Validation
    config_valid = config.validate_distribution() and config.validate_tax_distribution()
    
    if config_valid:
        st.sidebar.success("✅ Yapılandırma Geçerli")
    else:
        st.sidebar.error("❌ Yapılandırmayı düzeltin")
    
    # === SİMÜLASYON YÜRÜTME ===
    if st.button("  Simülasyonu Çalıştır v3.1", type="primary", use_container_width=True) and config_valid:
        
        with st.spinner(" tokenomics simülasyonu v3.1 çalıştırılıyor..."):
            
            model = TokenomicsModel(config)
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Adım 1:  Presale + Tax + Minimum APY Simülasyonu
            status_text.text("  Presale + Tax + Min APY sistemi simüle ediliyor...")
            presale_df = model.simulate_presale_with_auto_staking()
            progress_bar.progress(15)
            
            # Adım 2: Vesting Planları
            status_text.text("📅 Comprehensive vesting planları hesaplanıyor...")
            vesting_df = model.calculate_individual_vesting_schedules()
            progress_bar.progress(30)
            
            # Adım 3: Kompleks Market Cap Tahmini
            status_text.text(" Complex market cap tahmini çalıştırılıyor...")
            projection_df = model.estimate_complex_market_cap_and_price(presale_df, vesting_df)
            progress_bar.progress(50)
            
            # Adım 4: Launch Sonrası Staking + Tax
            status_text.text("⚡ Post-launch staking + tax sistemi simüle ediliyor...")
            staking_df = model.simulate_post_launch_staking(projection_df, presale_df)
            progress_bar.progress(70)
            
            # Adım 5: YENİ - Random Investor Analysis
            status_text.text("📊 Random investor ROI analizi oluşturuluyor...")
            investor_analysis_df = model.generate_random_investor_analysis(presale_df, projection_df)
            progress_bar.progress(85)
            
            # Adım 6:  Görselleştirmeler
            status_text.text("📊  professional görselleştirmeler oluşturuluyor...")
            charts = model.create__visualizations(presale_df, vesting_df, projection_df, staking_df, investor_analysis_df)
            progress_bar.progress(95)
            
            # Adım 7: Comprehensive Metrikler
            status_text.text("🧮 Comprehensive metrikler hesaplanıyor...")
            metrics = model.calculate__metrics(presale_df, vesting_df, projection_df, staking_df, investor_analysis_df)
            progress_bar.progress(100)
            
            status_text.text("✅  simülasyon v3.1 tamamlandı!")
            
            # Sonuçları sakla
            st.session_state['_results'] = {
                'presale_df': presale_df,
                'vesting_df': vesting_df,
                'projection_df': projection_df,
                'staking_df': staking_df,
                'investor_analysis_df': investor_analysis_df,
                'charts': charts,
                'metrics': metrics,
                'config': config
            }
            
            # Config'i otomatik kaydet
            config.save_to_json()
        
        st.success("🎉  simülasyon v3.1 başarıyla tamamlandı!")
    
    elif not config_valid:
        st.error("❌ Simülasyonu çalıştırmadan önce yapılandırmayı düzeltin")
    
    # === SONUÇLARI GÖSTER (BELİRLİ SIRADA) ===
    if '_results' in st.session_state:
        results = st.session_state['_results']
        charts = results['charts']
        metrics = results['metrics']
        
        # === YÖNETİCİ KONTROL PANELİ v3.1 ===
        st.markdown('''
        <h2 style="font-family: Orbitron, monospace; font-size: 2.5rem; font-weight: 700; 
                   color: #1B8EF2; margin: 2.5rem 0 1.5rem 0; padding: 1rem 0 0.5rem 0; 
                   border-bottom: 3px solid transparent; text-align: center;
                   border-image: linear-gradient(90deg, #1B8EF2, #3effc8) 1;
                   text-shadow: 0 0 20px rgba(27, 142, 242, 0.6);">
             Executive Dashboard v3.1
        </h2>
        ''', unsafe_allow_html=True)
        
        # Üst seviye metrikler
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <h4 style="color: {NXID_COLORS['primary']}; margin: 0; font-size: 0.9rem;">💰 Total Raised</h4>
                <p style="font-size: 1.4rem; margin: 0.5rem 0 0 0; color: {NXID_COLORS['success']}; font-weight: 800;">
                    ${metrics['presale']['total_raised_usdt']/1000000:.1f}M
                </p>
                <small style="color: {NXID_COLORS['gray']};">USDT (Presale)</small>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <h4 style="color: {NXID_COLORS['primary']}; margin: 0; font-size: 0.9rem;">🔥 Tax Collected</h4>
                <p style="font-size: 1.4rem; margin: 0.5rem 0 0 0; color: {NXID_COLORS['tax']}; font-weight: 800;">
                    {metrics['presale']['total_tax_collected']/1000000:.1f}M
                </p>
                <small style="color: {NXID_COLORS['gray']};">NXID (Tax)</small>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <h4 style="color: {NXID_COLORS['primary']}; margin: 0; font-size: 0.9rem;">⚡ Min APY Used</h4>
                <p style="font-size: 1.4rem; margin: 0.5rem 0 0 0; color: {NXID_COLORS['gold']}; font-weight: 800;">
                    {metrics['presale']['minimum_apy_usage_days']}
                </p>
                <small style="color: {NXID_COLORS['gray']};">Days</small>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="metric-card">
                <h4 style="color: {NXID_COLORS['primary']}; margin: 0; font-size: 0.9rem;"> Peak Price</h4>
                <p style="font-size: 1.4rem; margin: 0.5rem 0 0 0; color: {NXID_COLORS['gold']}; font-weight: 800;">
                    ${metrics['projection']['max_projected_price']:.4f}
                </p>
                <small style="color: {NXID_COLORS['gray']};"> at {metrics['projection']['max_price_timing_months']:.0f} months</small>
            </div>
            """, unsafe_allow_html=True)
        
        with col5:
            st.markdown(f"""
            <div class="metric-card">
                <h4 style="color: {NXID_COLORS['primary']}; margin: 0; font-size: 0.9rem;"> Peak ROI</h4>
                <p style="font-size: 1.4rem; margin: 0.5rem 0 0 0; color: {NXID_COLORS['success']}; font-weight: 800;">
                    {metrics['projection']['price_appreciation_vs_presale']:.1f}x
                </p>
                <small style="color: {NXID_COLORS['gray']};">vs Presale</small>
            </div>
            """, unsafe_allow_html=True)
        
        with col6:
            st.markdown(f"""
            <div class="metric-card">
                <h4 style="color: {NXID_COLORS['primary']}; margin: 0; font-size: 0.9rem;">📊 Avg Investor ROI</h4>
                <p style="font-size: 1.4rem; margin: 0.5rem 0 0 0; color: {NXID_COLORS['purple']}; font-weight: 800;">
                    {metrics['investor']['average_presale_end_roi']:.1f}%
                </p>
                <small style="color: {NXID_COLORS['gray']}"> Presale End</small>
            </div>
            """, unsafe_allow_html=True)
        
        # === BELİRLİ SIRADA GÖRSELLEŞTİRMELER (DÜZELTİLMİŞ SIRA) ===
        st.markdown('''
        <h2 style="font-family: Orbitron, monospace; font-size: 2.2rem; font-weight: 700; 
                   color: #1B8EF2; margin: 2.5rem 0 1.5rem 0; padding: 1rem 0 0.5rem 0; 
                   border-bottom: 3px solid transparent; text-align: center;
                   border-image: linear-gradient(90deg, #1B8EF2, #3effc8) 1;
                   text-shadow: 0 0 20px rgba(27, 142, 242, 0.6);">
            📊 Professional Analytics Suite v3.1 (Fixed Order)
        </h2>
        ''', unsafe_allow_html=True)
        
        # 1. Önce Pie Chart (Token Dağıtımı)
        st.markdown("### 📊 1. Token Distribution Overview")
        st.plotly_chart(charts['distribution'], use_container_width=True)
        
        # 2. Sonra Complete Vesting (Düzeltilmiş - Tüm bileşenler dahil)
        st.markdown("### 🔄 2. Complete Token Release Schedule (All Components)")
        st.plotly_chart(charts['vesting'], use_container_width=True)
        
        # 3. Presale ile ilgili her şey
        st.markdown("###  3.  Presale Analytics Suite")
        
        # 3a. Comprehensive Presale Dashboard
        st.markdown("#### 📊 3a. Presale Comprehensive Dashboard")
        st.plotly_chart(charts['presale'], use_container_width=True)
        
        # 3b. Daily Sales Detailed Chart
        st.markdown("#### 📊 3b. Daily Sales Volume Analysis")
        st.plotly_chart(charts['daily_sales'], use_container_width=True)
        
        # 3c. Random Investor ROI Analysis
        st.markdown("#### 📊 3c. Random Investor ROI Analysis")
        st.plotly_chart(charts['investor_roi'], use_container_width=True)
        
        # 4. Supply ve Market
        st.markdown("###  4. Market & Supply Analysis")
        
        # 4a. Supply Analysis
        st.markdown("#### 💧 4a. Circulating Supply & Burn Analysis")
        st.plotly_chart(charts['supply'], use_container_width=True)
        
        # 4b. Market Projection
        st.markdown("####  4b. Complex Market Cap Projection")
        st.plotly_chart(charts['market'], use_container_width=True)
        
        # 5. Staking Ecosystem
        st.markdown("### ⚡ 5. Post-Launch Staking Ecosystem")
        st.plotly_chart(charts['staking'], use_container_width=True)
        
        # === DETAYLI ANALİTİK RAPORU v3.1 ===
        st.markdown('''
        <h2 style="font-family: Orbitron, monospace; font-size: 2.2rem; font-weight: 700; 
                   color: #1B8EF2; margin: 2.5rem 0 1.5rem 0; padding: 1rem 0 0.5rem 0; 
                   border-bottom: 3px solid transparent; text-align: center;
                   border-image: linear-gradient(90deg, #1B8EF2, #3effc8) 1;
                   text-shadow: 0 0 20px rgba(27, 142, 242, 0.6);">
            📊 Comprehensive Analytics Report v3.1
        </h2>
        ''', unsafe_allow_html=True)
        
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["  Presale", " Market Projection", "⚡ Staking Ecosystem", "📅 Vesting Analysis", "🔥 Burn & Supply", "📊 Investor Analysis"])
        
        with tab1:
            st.markdown("###   Presale Performance")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("#### 📊 Presale Core Metrics")
                st.write(f"- **Duration**: {metrics['presale']['presale_duration_days']} days")
                st.write(f"- **Total Raised**: ${metrics['presale']['total_raised_usdt']/1e6:.1f}M USDT")
                st.write(f"- **Tokens Sold**: {metrics['presale']['tokens_sold']/1e9:.1f}B NXID ({metrics['presale']['tokens_sold_percentage']:.1f}%)")
                st.write(f"- **Final Price**: ${metrics['presale']['final_presale_price']:.4f}")
                st.write(f"- **Price Appreciation**: {metrics['presale']['price_appreciation_during_presale']:.1f}%")
                st.write(f"- **Average APY**: {metrics['presale']['average_apy']:.1f}%")
                
            with col2:
                st.markdown("#### ⚡  APY System")
                st.write(f"- **Minimum APY**: {config.minimum_staking_apy}%")
                st.write(f"- **Min APY Usage Days**: {metrics['presale']['minimum_apy_usage_days']} days")
                st.write(f"- **Presale Tokens Used**: {metrics['presale']['presale_tokens_used_for_rewards']/1e6:.1f}M NXID")
                st.write(f"- **Effective Pool Size**: {metrics['presale']['effective_reward_pool_final']/1e9:.1f}B NXID")
                st.write(f"- **Pool Depletion**: {metrics['presale']['pool_depletion_percentage']:.1f}%")
                
                if metrics['presale']['minimum_apy_usage_days'] > 0:
                    st.success(f"✅ Minimum APY sistemi {metrics['presale']['minimum_apy_usage_days']} gün aktif oldu!")
                else:
                    st.info("ℹ️ Minimum APY sistemi kullanılmadı - normal pool yeterli")
            
            st.markdown("#### 🔥 Tax System Impact")
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"- **Total Tax Collected**: {metrics['presale']['total_tax_collected']/1e6:.1f}M NXID")
                st.write(f"- **Tax → Staking Pool**: {metrics['presale']['total_tax_to_staking']/1e6:.1f}M NXID")
                st.write(f"- **Tax → Burn**: {metrics['presale']['total_tax_burned']/1e6:.1f}M NXID")
            with col2:
                st.write(f"- **Tax Effectiveness**: {metrics['presale']['tax_effectiveness']:.2f}%")
                st.write(f"- **Tax Period**: {config.tax_period_months} months")
                st.write(f"- **Tax Rate**: {config.tax_rate_total}%")
        
        with tab2:
            st.markdown("###  Complex Market Projection Analysis")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("####  Market Performance")
                st.write(f"- **Launch Market Cap**: ${metrics['projection']['launch_mcap']/1e6:.1f}M")
                st.write(f"- **Peak Market Cap**: ${metrics['projection']['max_mcap']/1e6:.1f}M")
                st.write(f"- **Peak Price**: ${metrics['projection']['max_projected_price']:.4f}")
                st.write(f"- **Peak Timing**: {metrics['projection']['max_price_timing_months']:.1f} months")
                st.write(f"- **Market Cap Growth**: {metrics['projection']['mcap_growth_vs_launch']:.1f}x")
                st.write(f"- **ROI vs Presale**: {metrics['projection']['price_appreciation_vs_presale']:.1f}x")
                
            with col2:
                st.markdown("#### 💎 Supply & Price Dynamics")
                st.write(f"- **Final Token Price**: ${metrics['projection']['final_token_price']:.4f}")
                st.write(f"- **Final Circulating**: {metrics['projection']['final_circulating_supply']/1e9:.1f}B")
                st.write(f"- **Total Burned**: {metrics['projection']['total_burned_tokens']/1e6:.1f}M")
                st.write(f"- **Max Burn Rate**: {metrics['projection']['max_burn_percentage']:.2f}%")
                st.write(f"- **Final Circulating %**: {metrics['projection']['final_circulating_percentage']:.1f}%")
                
                roi_color = NXID_COLORS['success'] if metrics['projection']['price_appreciation_vs_presale'] > 10 else NXID_COLORS['warning']
                st.markdown(f"<p style='color: {roi_color}; font-weight: bold; font-size: 1.2rem;'> Peak ROI: {metrics['projection']['price_appreciation_vs_presale']:.1f}x</p>", unsafe_allow_html=True)
        
        with tab3:
            st.markdown("### ⚡ Post-Launch Staking Ecosystem")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("#### ⚡ Staking Dynamics")
                st.write(f"- **Max Staking Ratio**: {metrics['staking']['max_staking_ratio']*100:.1f}%")
                st.write(f"- **Peak Participation**: {metrics['staking']['peak_staking_participation']*100:.1f}%")
                st.write(f"- **Average Market APY**: {metrics['staking']['average_market_apy']:.1f}%")
                st.write(f"- **Final Staked Tokens**: {metrics['staking']['final_staked_tokens']/1e9:.1f}B NXID")
                st.write(f"- **Duration**: {config.market_staking_years} years")
                
            with col2:
                st.markdown("#### 🏆 Reward Distribution")
                st.write(f"- **Total Distributed**: {metrics['staking']['total_market_rewards']/1e9:.1f}B NXID")
                st.write(f"- **Pool Depletion**: {metrics['staking']['staking_pool_depletion']:.1f}%")
                st.write(f"- **Tax Contribution**: {metrics['staking']['tax_staking_contribution']/1e6:.1f}M NXID")
                
                if metrics['staking']['max_staking_ratio'] > 0.4:
                    st.success("✅ High staking participation - Healthy ecosystem!")
                elif metrics['staking']['max_staking_ratio'] > 0.25:
                    st.info("ℹ️ Moderate staking - Consider APY optimizations")
                else:
                    st.warning("⚠️ Low staking participation - APY adjustment needed")
        
        with tab4:
            st.markdown("### 📅 Complete Token Release Analysis")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("#### 📅 Vesting Timeline")
                st.write(f"- **Team Full Vested**: {metrics['vesting']['team_fully_vested_month']} months")
                st.write(f"- **DAO Full Vested**: {metrics['vesting']['dao_fully_vested_month']} months")
                st.write(f"- **Marketing Full Vested**: {metrics['vesting']['marketing_fully_vested_month']} months")
                st.write(f"- **Vesting Delay**: 6 months post-launch")
                st.write(f"- **Immediate Release**: Presale + Staking Pools + Liquidity")
                
            with col2:
                st.markdown("####  Token Release Progress")
                st.write(f"- **24-Month Total Released**: {metrics['vesting']['total_released_at_24_months']/1e9:.1f}B NXID")
                st.write(f"- **24-Month Circulating**: {metrics['vesting']['circulating_at_24_months']/1e9:.1f}B NXID")
                st.write(f"- **24-Month Release %**: {metrics['vesting']['vesting_completion_percentage_24m']:.1f}%")
                st.write(f"- **24-Month Circulating %**: {metrics['vesting']['circulating_percentage_24m']:.1f}%")
                
                if metrics['vesting']['circulating_percentage_24m'] < 60:
                    st.success("✅ Conservative release schedule - Great for price stability")
                elif metrics['vesting']['circulating_percentage_24m'] < 80:
                    st.info("ℹ️ Moderate release pace - Balanced approach")
                else:
                    st.warning("⚠️ Aggressive release schedule - Monitor sell pressure")
        
        with tab5:
            st.markdown("### 🔥 Burn Mechanism & Supply Analysis")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("#### 🔥 Burn Metrics")
                st.write(f"- **Total Burned**: {metrics['projection']['total_burned_tokens']/1e6:.1f}M NXID")
                st.write(f"- **Max Burn Rate**: {metrics['projection']['max_burn_percentage']:.2f}%")
                st.write(f"- **Tax Burned**: {metrics['presale']['total_tax_burned']/1e6:.1f}M NXID")
                st.write(f"- **Burn Duration**: {config.burn_duration_years} years")
                st.write(f"- **Annual Burn Rate**: {config.annual_burn_rate*100:.1f}%")
                
            with col2:
                st.markdown("#### 💧 Supply Dynamics")
                st.write(f"- **Original Supply**: {config.total_supply/1e9:.0f}B NXID")
                st.write(f"- **Final Circulating**: {metrics['projection']['final_circulating_supply']/1e9:.1f}B NXID")
                st.write(f"- **Circulating %**: {metrics['projection']['final_circulating_percentage']:.1f}%")
                st.write(f"- **Supply Reduction**: {(1 - metrics['projection']['final_circulating_supply']/config.total_supply)*100:.1f}%")
                
                if metrics['projection']['max_burn_percentage'] > 5:
                    st.success("✅ Significant deflationary pressure")
                elif metrics['projection']['max_burn_percentage'] > 2:
                    st.info("ℹ️ Moderate burn impact")
                else:
                    st.warning("⚠️ Low burn impact - consider increasing")
        
        with tab6:
            st.markdown("### 📊 Random Investor ROI Analysis")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("#### 📊 Investor Performance Summary")
                st.write(f"- **Total Simulated Investors**: {metrics['investor']['total_simulated_investors']}")
                st.write(f"- **Average Presale End ROI**: {metrics['investor']['average_presale_end_roi']:.1f}%")
                st.write(f"- **Maximum ROI Achieved**: {metrics['investor']['max_presale_end_roi']:.1f}%")
                st.write(f"- **Minimum ROI**: {metrics['investor']['min_presale_end_roi']:.1f}%")
                
            with col2:
                st.markdown("####  Investment Timing Analysis")
                st.write(f"- **Best Investment Day**: Day {metrics['investor']['best_investment_day']}")
                st.write(f"- **Worst Investment Day**: Day {metrics['investor']['worst_investment_day']}")
                st.write(f"- **ROI Range**: {metrics['investor']['max_presale_end_roi'] - metrics['investor']['min_presale_end_roi']:.1f}%")
                
                if metrics['investor']['average_presale_end_roi'] > 100:
                    st.success("✅ Excellent investor returns - Very attractive presale!")
                elif metrics['investor']['average_presale_end_roi'] > 50:
                    st.info("ℹ️ Good investor returns - Solid presale performance")
                else:
                    st.warning("⚠️ Moderate returns - Consider presale optimization")
        
        # === DIŞA AKTARMA & CONFIG YÖNETİMİ ===
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
                label="📥  Presale Data",
                data=presale_csv,
                file_name="nxid__presale_v31.csv",
                mime="text/csv"
            )
        
        with col2:
            vesting_csv = results['vesting_df'].to_csv(index=False)
            st.download_button(
                label="📥 Vesting Data",
                data=vesting_csv,
                file_name="nxid_vesting_schedules_v31.csv",
                mime="text/csv"
            )
        
        with col3:
            projection_csv = results['projection_df'].to_csv(index=False)
            st.download_button(
                label="📥 Market Projection",
                data=projection_csv,
                file_name="nxid_market_projection_v31.csv",
                mime="text/csv"
            )
        
        with col4:
            staking_csv = results['staking_df'].to_csv(index=False)
            st.download_button(
                label="📥 Staking Data",
                data=staking_csv,
                file_name="nxid_staking_ecosystem_v31.csv",
                mime="text/csv"
            )
        
        with col5:
            investor_csv = results['investor_analysis_df'].to_csv(index=False)
            st.download_button(
                label="📥 Investor Analysis",
                data=investor_csv,
                file_name="nxid_investor_analysis_v31.csv",
                mime="text/csv"
            )
        
        with col6:
            config_json = json.dumps(config.to_dict(), indent=2)
            st.download_button(
                label="📥 Config JSON v3.1",
                data=config_json,
                file_name="nxid_config_v31.json",
                mime="application/json"
            )
        
        # === FINAL PERFORMANCE SCORE ===
        st.markdown('''
        <h3 style="color: #1B8EF2; margin: 2rem 0 1rem 0; font-family: Orbitron;">
              Performance Score v3.1
        </h3>
        ''', unsafe_allow_html=True)
        
        # Gelişmiş scoring sistemi
        _score = (
            (100 if abs(metrics['presale']['pool_depletion_percentage'] - 100) < 5 else 80) * 0.15 +  # Pool efficiency
            (100 if metrics['projection']['price_appreciation_vs_presale'] > 10 else 70) * 0.25 +      # Price performance
            (100 if metrics['staking']['max_staking_ratio'] > 0.4 else 60) * 0.20 +                   # Staking health
            (100 if metrics['projection']['max_burn_percentage'] > 2 else 70) * 0.15 +                # Burn impact
            (100 if metrics['investor']['average_presale_end_roi'] > 100 else 70) * 0.15 +            # Investor returns
            (100 if metrics['presale']['minimum_apy_usage_days'] == 0 else 90) * 0.10                 # APY system efficiency
        )
        
        # Final summary metrics
        summary_col1, summary_col2, summary_col3 = st.columns(3)
        
        with summary_col1:
            st.markdown(f"""
            **  Presale Success:**
            - Raised: ${metrics['presale']['total_raised_usdt']/1e6:.1f}M USDT
            - ROI Potential: {metrics['projection']['price_appreciation_vs_presale']:.1f}x
            - Tax Collection: {metrics['presale']['total_tax_collected']/1e6:.1f}M NXID
            - Min APY Usage: {metrics['presale']['minimum_apy_usage_days']} days
            """)
        
        with summary_col2:
            st.markdown(f"""
            ** Market & Ecosystem:**
            - Peak Market Cap: ${metrics['projection']['max_mcap']/1e6:.0f}M
            - Max Staking: {metrics['staking']['max_staking_ratio']*100:.1f}%
            - Supply Burned: {metrics['projection']['max_burn_percentage']:.2f}%
            - 24M Circulating: {metrics['vesting']['circulating_at_24_months']/1e9:.1f}B
            """)
        
        with summary_col3:
            st.markdown(f"""
            **📊 Investor Experience:**
            - Avg ROI: {metrics['investor']['average_presale_end_roi']:.1f}%
            - Best Day: Day {metrics['investor']['best_investment_day']}
            - Investors Simulated: {metrics['investor']['total_simulated_investors']}
            - Tax to Staking: {metrics['presale']['total_tax_to_staking']/1e6:.1f}M NXID
            """)
        
        #  final assessment
        if _score >= 95:
            st.success(f"🏆 **OUTSTANDING TOKENOMICS DESIGN** - Score: {_score:.0f}/100 - Industry Leading!")
        elif _score >= 90:
            st.success(f"🎉 **EXCELLENT TOKENOMICS DESIGN** - Score: {_score:.0f}/100 - Highly Optimized!")
        elif _score >= 80:
            st.info(f"✅ **GOOD TOKENOMICS DESIGN** - Score: {_score:.0f}/100 - Well Balanced!")
        elif _score >= 70:
            st.warning(f"⚠️ **FAIR TOKENOMICS DESIGN** - Score: {_score:.0f}/100 - Consider optimizations")
        else:
            st.error(f"❌ **NEEDS IMPROVEMENT** - Score: {_score:.0f}/100 - Significant changes required")

if __name__ == "__main__":
    main()