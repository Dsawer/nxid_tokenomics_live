"""
NXID Enhanced Configuration Module 
========================================
Enhanced: Advanced Maturity Damping + Dynamic Staking + Real Circulating Supply + Price Velocity
"""

import json
import os
import streamlit as st
from dataclasses import dataclass, asdict
from typing import Dict, List, Tuple, Optional

@dataclass
class EnhancedNXIDConfig:
    """🔧 Enhanced NXID Tokenomics Configuration  - Advanced Maturity + Dynamic Systems"""
    
    # === TEMEL TOKEN PARAMETRELERİ ===
    total_supply: float = 100_000_000_000.0  # 100B NXID
    
    # === TOKEN DAĞITIMI ===
    team_allocation: float = 15.0           # Team %
    presale_staking_pool: float = 4.0       # Presale Staking Rewards %
    market_staking_pool: float = 25.0       # Post-Launch Staking %
    dao_treasury: float = 15.0              # DAO Treasury %
    marketing: float = 8.0                  # Marketing %
    liquidity: float = 7.0                  # Liquidity %
    presale_allocation: float = 26.0        # Presale Token Sale %
    
    # === PRESALE PARAMETRELERİ ===
    presale_days: int = 180                 # Presale Süresi
    start_price_usdt: float = 0.001         # Başlangıç Fiyatı USDT
    daily_price_increase: float = 0.05      # Günlük Fiyat Artışı % 
    
    # === PRESALE SIMPLE FAİZ TALEBİ ===
    base_daily_demand_usdt: float = 2000.0  # Temel Günlük Talep USDT
    demand_growth_rate: float = 1.01        # Günlük talep büyüme çarpanı
    demand_volatility: float = 0.05         # Talep volatilite faktörü
    
    # APY ETKİSİ
    apy_demand_multiplier: float = 1.5      # APY'nin talebi artırma çarpanı
    max_apy_boost: float = 3.0              # APY ile maksimum talep artışı
    
    # FİYAT ETKİSİ
    price_resistance_factor: float = 0.8    # Fiyatın talebi nasıl etkilediği
    early_bird_bonus: float = 1.3          # Erken yatırımcı bonusu
    
    # === SIMPLE FAİZ + DİNAMİK APY SİSTEMİ ===
    max_apy: float = 5000.0                 # Maksimum APY %
    minimum_staking_apy: float = 50.0       # Minimum Staking APY %
    
    # === HAFTALIK SIMPLE FAİZ ANALİZİ ===
    weekly_analysis: bool = True            # Haftalık analiz aktif mi
    weekly_investment_amount: float = 1000.0  # Sabit haftalık yatırım miktarı ($)
    
    # === YENİ: STARTING MCAP INPUT  ===
    starting_mcap_usdt: float = 8_000_000.0  # User input starting McAp
    
    # === ENHANCED MATURITY DAMPING SYSTEM  ===
    maturity_target_mcap: float = 1_000_000_000.0  # Target McAp for convergence
    maturity_damping_strength: float = 0.4     # Damping kuvveti (0-1)
    maturity_convergence_speed: float = 0.15   # YENİ: Yakınsama hızı
    maturity_boost_multiplier: float = 1.8     # YENİ: Boost çarpanı (target altında)
    maturity_damp_multiplier: float = 0.6      # YENİ: Damp çarpanı (target üstünde)
    enable_maturity_damping: bool = True       # Maturity damping aktif
    enable_maturity_analysis: bool = True      # YENİ: Maturity analizi aktif
    
    # === ENHANCED DYNAMIC STAKING SYSTEM  ===
    # Staking Participation Range
    base_staking_rate: float = 0.45           # Temel staking oranı (fiyat etkisi olmadan)
    min_staking_rate: float = 0.15            # Minimum staking oranı
    max_staking_rate: float = 0.75            # Maximum staking oranı
    
    # Enhanced Price Velocity System 
    price_velocity_impact: float = -0.6       # Fiyat hızının staking'e etkisi
    price_velocity_window: int = 7            # Fiyat hızı hesaplama penceresi (gün)
    price_velocity_smoothing: float = 0.3     # Fiyat hızı smoothing faktörü
    
    # Staking Dynamics 
    staking_momentum: float = 0.85            # Staking değişim momentum'u
    staking_entry_speed: float = 0.002        # Yeni staking giriş hızı
    staking_exit_speed: float = 0.005         # Staking çıkış hızı (daha hızlı)
    staking_transition_smoothness: float = 0.12  # Geçiş yumuşaklığı
    
    # === ENHANCED DYNAMIC APY SYSTEM  ===
    staking_pool_duration_years: int = 8     # Staking pool süresi
    base_staking_apy: float = 85.0           # Temel staking APY
    min_staking_apy: float = 15.0            # Minimum staking APY
    max_staking_apy: float = 250.0           # Maximum staking APY
    
    # APY Calculation Factors 
    pool_depletion_apy_factor: float = 0.8   # Pool tükenmesi APY etkisi
    staking_saturation_factor: float = 0.6   # Staking doygunluğu APY etkisi
    market_demand_apy_factor: float = 0.3    # Market talep APY etkisi
    
    # === ADVANCED MARKET DYNAMICS  ===
    market_volatility: float = 0.08          # Base volatility
    market_beta: float = 1.1                 # Market beta
    speculative_ratio: float = 0.6           # Spekülasyon oranı
    fundamental_growth_rate: float = 0.015   # Aylık temelli büyüme
    
    # Enhanced smoothing parameters
    price_smoothing_factor: float = 0.15     # Fiyat smoothing
    mcap_smoothing_factor: float = 0.12      # McAp smoothing
    volatility_damping: float = 0.7          # Volatilite azaltma
    
    # === CIRCULATING SUPPLY CALCULATION  ===
    include_staked_in_circulating: bool = False  # Staked tokenları circulating'den çıkar
    burn_effect_permanent: bool = True           # Yakılan tokenlar kalıcı olarak çıkarılır
    
    # === VESTING SCHEDULES ===
    # Staking Pool Vesting
    presale_staking_cliff_months: int = 0    # Anında serbest
    presale_staking_vesting_months: int = 1  # 1 ay vesting
    market_staking_cliff_months: int = 6     # 6 ay cliff
    market_staking_vesting_months: int = 24  # 24 ay vesting
    
    # Individual Vesting
    team_cliff_months: int = 12              # Team cliff
    team_vesting_months: int = 36            # Team vesting
    dao_cliff_months: int = 6                # DAO cliff
    dao_vesting_months: int = 24             # DAO vesting
    marketing_cliff_months: int = 0          # Marketing cliff
    marketing_vesting_months: int = 12       # Marketing vesting
    
    # === 16 ÇEYREK MAINNET SİSTEMİ ===
    bear_scenario_multipliers: List[float] = None  
    base_scenario_multipliers: List[float] = None  
    bull_scenario_multipliers: List[float] = None  
    market_beta_per_quarter: List[float] = None
    
    # === MAINNET TAX VE BURN SİSTEMİ ===
    mainnet_tax_period_months: int = 6       # Mainnet tax dönemi
    mainnet_tax_rate: float = 3.0            # Mainnet tax oranı %
    tax_to_staking_percentage: float = 60.0  # Tax'ın staking pool'a giden yüzdesi
    tax_to_burn_percentage: float = 40.0     # Tax'ın yakılan yüzdesi
    
    # Yakma mekanizması
    annual_burn_rate: float = 0.02           # %2 yıllık yakma oranı
    burn_duration_years: int = 3             # Yakma süresi (yıl)
    
    # === PROJECTION CONTROL ===
    projection_months: int = 48              # Projeksiyon süresi (ay) - 4 yıl
    vesting_analysis_months: int = 72        # Vesting analiz süresi (ay)
    
    # === SIMPLE FAİZ SİSTEM PARAMETRELERİ ===
    interest_calculation_method: str = "SIMPLE"  # Simple faiz sistemi
    enable_compounding: bool = False         # Compounding kapalı
    dynamic_apy_enabled: bool = True         # Dinamik APY aktif
    
    # === ESKI UYUMLULUK ===
    investor_count_simulation: int = 100
    min_investment_usdt: float = 100.0
    max_investment_usdt: float = 10000.0
    
    def __post_init__(self):
        """Default değerleri ayarla - 16 çeyrek için + Enhanced """
        if self.bear_scenario_multipliers is None:
            self.bear_scenario_multipliers = [
                0.7, 0.8, 0.75, 0.85,  # Yıl 1
                0.8, 0.9, 0.85, 0.95,  # Yıl 2  
                0.9, 1.0, 0.95, 1.05,  # Yıl 3
                1.0, 1.1, 1.05, 1.15   # Yıl 4
            ]
        if self.base_scenario_multipliers is None:
            self.base_scenario_multipliers = [
                1.0, 1.05, 1.1, 1.15,  # Yıl 1
                1.1, 1.2, 1.15, 1.25,  # Yıl 2
                1.2, 1.3, 1.25, 1.35,  # Yıl 3  
                1.3, 1.4, 1.35, 1.45   # Yıl 4
            ]
        if self.bull_scenario_multipliers is None:
            self.bull_scenario_multipliers = [
                1.5, 1.8, 1.6, 1.9,    # Yıl 1
                1.7, 2.0, 1.8, 2.1,    # Yıl 2
                1.9, 2.2, 2.0, 2.3,    # Yıl 3
                2.1, 2.4, 2.2, 2.5     # Yıl 4
            ]
        if self.market_beta_per_quarter is None:
            self.market_beta_per_quarter = [
                1.1, 1.0, 1.05, 0.95,  # Yıl 1
                1.0, 0.95, 1.0, 0.9,   # Yıl 2 
                0.95, 0.9, 0.95, 0.85, # Yıl 3 
                0.9, 0.85, 0.9, 0.8    # Yıl 4
            ]
    
    def validate_distribution(self) -> bool:
        """Token dağıtımının %100'e eşit olduğunu doğrula"""
        total = (self.team_allocation + self.presale_staking_pool + self.market_staking_pool +
                self.dao_treasury + self.marketing + self.liquidity + self.presale_allocation)
        return abs(total - 100.0) < 0.01
    
    def validate_tax_distribution(self) -> bool:
        """Tax dağıtımının %100'e eşit olduğunu doğrula"""
        total = self.tax_to_staking_percentage + self.tax_to_burn_percentage
        return abs(total - 100.0) < 0.01
    
    def validate_enhanced_parameters(self) -> bool:
        """Enhanced  parametrelerini doğrula"""
        # Starting McAp validation
        if self.starting_mcap_usdt <= 0:
            return False
        
        # Maturity target validation
        if self.maturity_target_mcap <= self.starting_mcap_usdt:
            return False
        
        # Staking range validation
        if not (0 <= self.min_staking_rate <= self.base_staking_rate <= self.max_staking_rate <= 1):
            return False
        
        # APY range validation
        if not (0 <= self.min_staking_apy <= self.base_staking_apy <= self.max_staking_apy):
            return False
        
        # Damping parameters validation
        if not (0 <= self.maturity_damping_strength <= 1):
            return False
        
        return True
    
    def get_maturity_params(self) -> dict:
        """Advanced Maturity parametrelerini döndür """
        return {
            "target_mcap": self.maturity_target_mcap,
            "starting_mcap": self.starting_mcap_usdt,
            "damping_strength": self.maturity_damping_strength,
            "convergence_speed": self.maturity_convergence_speed,
            "boost_multiplier": self.maturity_boost_multiplier,
            "damp_multiplier": self.maturity_damp_multiplier,
            "enabled": self.enable_maturity_damping,
            "target_ratio": self.maturity_target_mcap / self.starting_mcap_usdt
        }
    
    def get_staking_params(self) -> dict:
        """Enhanced Staking parametrelerini döndür """
        return {
            "base_rate": self.base_staking_rate,
            "min_rate": self.min_staking_rate,
            "max_rate": self.max_staking_rate,
            "price_velocity_impact": self.price_velocity_impact,
            "velocity_window": self.price_velocity_window,
            "velocity_smoothing": self.price_velocity_smoothing,
            "momentum": self.staking_momentum,
            "entry_speed": self.staking_entry_speed,
            "exit_speed": self.staking_exit_speed,
            "smoothness": self.staking_transition_smoothness
        }
    
    def get_apy_params(self) -> dict:
        """Enhanced APY parametrelerini döndür """
        return {
            "duration_years": self.staking_pool_duration_years,
            "base_apy": self.base_staking_apy,
            "min_apy": self.min_staking_apy,
            "max_apy": self.max_staking_apy,
            "pool_factor": self.pool_depletion_apy_factor,
            "saturation_factor": self.staking_saturation_factor,
            "market_factor": self.market_demand_apy_factor
        }
    
    def to_dict(self) -> dict:
        """Config'i dictionary'ye çevir"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: dict):
        """Dictionary'den config oluştur"""
        valid_fields = {field.name for field in cls.__dataclass_fields__.values()}
        filtered_data = {k: v for k, v in data.items() if k in valid_fields}
        return cls(**filtered_data)
    
    def save_to_json(self, filename: str = "nxid_config_enhanced_v6.json"):
        """Config'i JSON dosyasına kaydet"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.to_dict(), f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            st.error(f"Config kaydetme hatası: {e}")
            return False
    
    @classmethod
    def load_from_json(cls, filename: str = "nxid_config_enhanced_v6.json"):
        """JSON dosyasından config yükle"""
        try:
            if os.path.exists(filename):
                with open(filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                return cls.from_dict(data)
            else:
                # Fallback to older versions
                fallback_files = ["nxid_config_enhanced_v5.json", "nxid_config_enhanced_v46.json", "nxid_config.json"]
                for fallback in fallback_files:
                    if os.path.exists(fallback):
                        with open(fallback, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                        return cls.from_dict(data)
                
                st.info(f"Config dosyası bulunamadı ({filename}), default enhanced config  kullanılıyor.")
                return cls()
        except Exception as e:
            st.warning(f"Config yükleme hatası: {e}. Default enhanced config  kullanılıyor.")
            return cls()
    
    def get_system_info(self) -> dict:
        """Enhanced sistem bilgilerini döndür """
        return {
            "version": "6.0",
            "features": [
                "Advanced Maturity Damping",
                "Enhanced Dynamic Staking",
                "Price Velocity Impact",
                "Real Circulating Supply",
                "Dynamic APY with Pool Release"
            ],
            "calculation_method": self.interest_calculation_method,
            "starting_mcap": self.starting_mcap_usdt,
            "maturity_target": self.maturity_target_mcap
        }