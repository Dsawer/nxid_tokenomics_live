"""
NXID Enhanced Tokenomics Models 
=====================================
Enhanced: Simplified Maturity Damping + Dynamic Staking + Real Circulating Supply + Price Velocity
"""

import pandas as pd
import numpy as np
import math
import random
import streamlit as st
from typing import Dict, List, Tuple, Optional
from config import EnhancedNXIDConfig

class EnhancedTokenomicsModel:
    """Enhanced NXID Tokenomics Model  - Simplified Maturity + Dynamic Systems"""
    
    def __init__(self, config: EnhancedNXIDConfig):
        self.config = config
        # Enhanced tracking için historiler
        self.price_history = []
        self.mcap_history = []
        self.staking_history = []
        self.price_velocity_history = []
        self.maturity_distance_history = []
        
    def simulate_presale_phase(self) -> pd.DataFrame:
        """PRESALE PHASE - Simple Faiz + Dinamik APY () - AYNI"""
        np.random.seed(42)
        
        presale_tokens_for_sale = self.config.total_supply * (self.config.presale_allocation / 100)
        presale_staking_reward_pool = self.config.total_supply * (self.config.presale_staking_pool / 100)
        
        presale_data = []
        cumulative_raised_usdt = 0
        cumulative_sold_tokens = 0
        remaining_reward_pool = presale_staking_reward_pool
        total_distributed_rewards = 0
        cumulative_principal_tokens = 0
        
        for day in range(self.config.presale_days):
            # Fiyat hesaplama
            current_price_usdt = (self.config.start_price_usdt * 
                                ((1 + self.config.daily_price_increase/100) ** day))
            
            # Stabilize edilmiş talep modeli
            base_demand = (self.config.base_daily_demand_usdt * 
                          (self.config.demand_growth_rate ** day))
            
            # Dinamik APY hesaplama
            remaining_days = max(1, self.config.presale_days - day)
            current_principal = cumulative_principal_tokens
            
            if current_principal > 0 and remaining_reward_pool > 0:
                total_daily_rewards_needed = remaining_reward_pool / remaining_days
                required_daily_rate = total_daily_rewards_needed / current_principal
                dynamic_apy = required_daily_rate * 365 * 100
                dynamic_apy = min(dynamic_apy, self.config.max_apy)
                dynamic_apy = max(dynamic_apy, self.config.minimum_staking_apy)
                current_apy = dynamic_apy
            else:
                current_apy = self.config.max_apy if day == 0 else self.config.minimum_staking_apy
            
            # Talep faktörleri
            apy_normalized = current_apy / self.config.max_apy
            apy_effect = 1 + (apy_normalized * (self.config.apy_demand_multiplier - 1))
            apy_effect = min(apy_effect, self.config.max_apy_boost)
            
            price_ratio = current_price_usdt / self.config.start_price_usdt
            price_effect = max(0.3, min(2.0, (1 / price_ratio) ** self.config.price_resistance_factor))
            
            early_bonus = self.config.early_bird_bonus if day < 30 else 1.0
            
            volatility_factor = 1 + np.random.normal(0, self.config.demand_volatility * 0.5)
            volatility_factor = max(0.98, min(1.02, volatility_factor))
            
            # Toplam talep
            daily_demand_usdt = (base_demand * apy_effect * price_effect * 
                                early_bonus * volatility_factor)
            
            daily_tokens_sold = daily_demand_usdt / current_price_usdt
            
            # Token limiti kontrolü
            remaining_sale_tokens = presale_tokens_for_sale - cumulative_sold_tokens
            if daily_tokens_sold > remaining_sale_tokens:
                daily_tokens_sold = max(0, remaining_sale_tokens)
                daily_demand_usdt = daily_tokens_sold * current_price_usdt
                presale_ended = True
            else:
                presale_ended = False
            
            # Simple faiz ile günlük ödül hesaplama
            cumulative_principal_tokens += daily_tokens_sold
            
            if cumulative_principal_tokens > 0 and remaining_reward_pool > 0:
                daily_rate = current_apy / 100 / 365
                daily_rewards = cumulative_principal_tokens * daily_rate
                
                if daily_rewards <= remaining_reward_pool:
                    daily_rewards_paid = daily_rewards
                    remaining_reward_pool -= daily_rewards
                    total_distributed_rewards += daily_rewards
                else:
                    daily_rewards_paid = remaining_reward_pool
                    total_distributed_rewards += remaining_reward_pool
                    remaining_reward_pool = 0
            else:
                daily_rewards_paid = 0
            
            # Akümülatörleri güncelle
            cumulative_raised_usdt += daily_demand_usdt
            cumulative_sold_tokens += daily_tokens_sold
            
            pool_depletion_percentage = (total_distributed_rewards / presale_staking_reward_pool) * 100
            
            if cumulative_principal_tokens > 0 and remaining_days > 1:
                verification_daily_rate = current_apy / 100 / 365
                projected_total_rewards = cumulative_principal_tokens * verification_daily_rate * (remaining_days - 1)
                pool_sufficiency_ratio = remaining_reward_pool / projected_total_rewards if projected_total_rewards > 0 else 1
            else:
                projected_total_rewards = 0
                pool_sufficiency_ratio = 1
            
            current_total_balance = cumulative_principal_tokens + total_distributed_rewards
            
            presale_data.append({
                'gun': day + 1,
                'fiyat_usdt': current_price_usdt,
                'gunluk_talep_usdt': daily_demand_usdt,
                'gunluk_satilan_token': daily_tokens_sold,
                'kumulatif_toplanan_usdt': cumulative_raised_usdt,
                'kumulatif_satilan_token': cumulative_sold_tokens,
                'guncel_apy': current_apy,
                'dinamik_apy': current_apy,
                'ana_para_tokens': cumulative_principal_tokens,
                'gunluk_oduller': daily_rewards_paid,
                'toplam_dagitilan_odul': total_distributed_rewards,
                'toplam_balance': current_total_balance,
                'kalan_odul_havuzu': remaining_reward_pool,
                'havuz_tukenme_yuzdesi': pool_depletion_percentage,
                'kalan_gun_sayisi': remaining_days,
                'tahmin_edilen_toplam_odul': projected_total_rewards,
                'havuz_yeterlilik_orani': pool_sufficiency_ratio,
                'gunluk_faiz_orani': current_apy / 100 / 365,
                'faiz_tipi': 'SIMPLE',
                'temel_talep': base_demand,
                'apy_etkisi': apy_effect,
                'fiyat_etkisi': price_effect,
                'erken_bonus': early_bonus,
                'volatilite_faktoru': volatility_factor,
                'presale_bitti': presale_ended,
                'satilan_token_yuzdesi': (cumulative_sold_tokens / presale_tokens_for_sale) * 100,
                'fiyat_artisi': ((current_price_usdt / self.config.start_price_usdt) - 1) * 100,
                'fiyat_orani': price_ratio
            })
            
            if presale_ended:
                break
        
        return pd.DataFrame(presale_data)
    
    def generate_weekly_token_analysis(self, presale_df: pd.DataFrame) -> pd.DataFrame:
        """Haftalık token analizi - AYNI """
        weekly_data = []
        weeks = len(presale_df) // 7
        
        for week in range(1, min(weeks + 1, 26)):
            week_start_day = (week - 1) * 7
            week_day_index = min(week_start_day, len(presale_df) - 1)
            
            week_price = presale_df.iloc[week_day_index]['fiyat_usdt']
            week_apy = presale_df.iloc[week_day_index]['guncel_apy']
            
            investment_amount = self.config.weekly_investment_amount
            tokens_bought = investment_amount / week_price
            principal_tokens = tokens_bought
            total_staking_rewards = 0
            
            for day_offset in range(week_start_day, len(presale_df)):
                if day_offset < len(presale_df):
                    daily_apy = presale_df.iloc[day_offset]['guncel_apy']
                    daily_rate = daily_apy / 100 / 365
                    daily_reward = principal_tokens * daily_rate
                    
                    if 'kalan_odul_havuzu' in presale_df.columns:
                        remaining_pool = presale_df.iloc[day_offset]['kalan_odul_havuzu']
                        if remaining_pool <= 0:
                            daily_reward = 0
                        else:
                            initial_pool = self.config.total_supply * (self.config.presale_staking_pool / 100)
                            pool_health = remaining_pool / initial_pool
                            daily_reward = daily_reward * max(0.1, pool_health)
                    
                    total_staking_rewards += daily_reward
            
            current_balance = principal_tokens + total_staking_rewards
            token_gain_percentage = (total_staking_rewards / tokens_bought) * 100 if tokens_bought > 0 else 0
            
            weekly_data.append({
                'hafta': week,
                'yatirim_gunu': week_start_day + 1,
                'hafta_fiyati': week_price,
                'hafta_apy': week_apy,
                'yatirim_miktari_usdt': investment_amount,
                'alinan_token': tokens_bought,
                'ana_para_tokens': principal_tokens,
                'staking_kazanci': total_staking_rewards,
                'toplam_token': current_balance,
                'token_kazanc_yuzdesi': token_gain_percentage,
                'gun_sayisi': len(presale_df) - week_start_day,
                'faiz_tipi': 'SIMPLE'
            })
        
        return pd.DataFrame(weekly_data)
    
    def simulate_mainnet_phase(self, presale_df: pd.DataFrame, vesting_df: pd.DataFrame, 
                              scenario: str = "base") -> pd.DataFrame:
        """🚀 ENHANCED MAINNET PHASE  - Simplified Maturity + Dynamic Systems"""
        np.random.seed(123)
        
        # Presale verileri
        final_presale_raised = presale_df['kumulatif_toplanan_usdt'].iloc[-1]
        final_presale_tokens = presale_df['kumulatif_satilan_token'].iloc[-1]
        final_presale_price = presale_df['fiyat_usdt'].iloc[-1]
        
        # Starting McAp (user input)
        starting_mcap = self.config.starting_mcap_usdt
        
        # Senaryo çarpanları
        if scenario == "bear":
            scenario_multipliers = self.config.bear_scenario_multipliers
        elif scenario == "bull":
            scenario_multipliers = self.config.bull_scenario_multipliers
        else:
            scenario_multipliers = self.config.base_scenario_multipliers
        
        projection_days = int(self.config.projection_months * 30.44)
        mainnet_data = []
        
        # Enhanced parametreler 
        maturity_params = self.config.get_maturity_params()
        staking_params = self.config.get_staking_params()
        apy_params = self.config.get_apy_params()
        
        # Market staking pool
        market_staking_pool = self.config.total_supply * (self.config.market_staking_pool / 100)
        
        # Enhanced akümülatörler 
        cumulative_tax_collected = 0
        cumulative_tax_to_staking = 0
        cumulative_tax_burned = 0
        cumulative_routine_burned = 0
        cumulative_staked = 0
        distributed_staking_rewards = 0
        previous_price = final_presale_price
        
        # Enhanced moving averages
        mcap_ma = starting_mcap
        price_ma = final_presale_price
        staking_ma = staking_params['base_rate']
        staking_momentum = staking_params['base_rate']
        
        for day in range(projection_days):
            months = day / 30.44
            years = day / 365.25
            quarter = int(months // 3) % 16
            quarter_year = quarter // 4 + 1
            quarter_in_year = quarter % 4 + 1
            
            # === SIMPLIFIED MATURITY DAMPING CALCULATION  ===
            
            # 1. Çeyreklik senaryo etkisi
            if quarter < len(scenario_multipliers):
                quarter_multiplier = scenario_multipliers[quarter]
            else:
                quarter_multiplier = scenario_multipliers[-1]
            
            # 2. Market beta
            if quarter < len(self.config.market_beta_per_quarter):
                current_beta = self.config.market_beta_per_quarter[quarter]
            else:
                current_beta = self.config.market_beta_per_quarter[-1]
            
            # 3. SIMPLIFIED MATURITY DAMPING 
            if maturity_params['enabled']:
                target_mcap = maturity_params['target_mcap']
                current_mcap_estimate = mcap_ma
                
                # Simple distance ratio calculation
                distance_ratio = current_mcap_estimate / target_mcap
                
                # Simple maturity effect based on distance
                if distance_ratio < 1.0:  # Below target -> BOOST
                    # Further below = stronger boost
                    boost_strength = (1.0 - distance_ratio)  # 0 to 1
                    maturity_effect = 1.0 + boost_strength * 0.5  # Max 1.5x boost
                else:  # Above target -> DAMP
                    # Further above = stronger damping
                    excess_ratio = distance_ratio - 1.0
                    damp_strength = min(excess_ratio, 1.0)  # Cap at 1.0
                    maturity_effect = 1.0 - damp_strength * 0.3  # Max 0.7x damping
                
                # Smooth maturity effect transitions
                maturity_effect = max(0.7, min(1.5, maturity_effect))
                
                # Track distance for analysis
                self.maturity_distance_history.append(distance_ratio - 1.0)
            else:
                maturity_effect = 1.0
                distance_ratio = current_mcap_estimate / target_mcap if 'target_mcap' in locals() else 1.0
            
            # 4. Base growth calculation - SIMPLIFIED
            fundamental_growth = (1 + self.config.fundamental_growth_rate) ** months
            
            # Simplified speculative growth - NO testere pattern
            base_speculative = quarter_multiplier * maturity_effect
            speculative_growth = base_speculative
            
            base_growth = (
                self.config.speculative_ratio * speculative_growth + 
                (1 - self.config.speculative_ratio) * fundamental_growth
            )
            
            # 5. REDUCED Volatilite  - Less testere
            daily_volatility = np.random.normal(0, self.config.market_volatility * 0.3)  # Reduced volatility
            volatility_effect = 1 + daily_volatility * current_beta * 0.5  # Reduced impact
            volatility_effect = max(0.95, min(1.05, volatility_effect))  # Tighter bounds
            
            # Raw McAp
            raw_mcap = starting_mcap * base_growth * volatility_effect
            
            # STRONGER Smooth McAp - Less testere
            mcap_ma = mcap_ma * (1 - self.config.mcap_smoothing_factor * 2) + raw_mcap * (self.config.mcap_smoothing_factor * 2)
            current_mcap = mcap_ma
            
            # === ENHANCED CIRCULATING SUPPLY WITH REAL CALCULATION  ===
            month_index = min(len(vesting_df) - 1, int(months))
            if month_index < len(vesting_df):
                base_circulating = vesting_df.iloc[month_index]['circulating_supply']
            else:
                base_circulating = final_presale_tokens
            
            # Tax sistemi
            tax_active = months <= self.config.mainnet_tax_period_months
            if tax_active and current_mcap > 0:
                daily_volume = current_mcap * 0.003
                daily_tax_usdt = daily_volume * (self.config.mainnet_tax_rate / 100)
                current_price_estimate = current_mcap / base_circulating if base_circulating > 0 else final_presale_price
                daily_tax_tokens = daily_tax_usdt / current_price_estimate
                
                daily_tax_to_staking = daily_tax_tokens * (self.config.tax_to_staking_percentage / 100)
                daily_tax_to_burn = daily_tax_tokens * (self.config.tax_to_burn_percentage / 100)
                
                cumulative_tax_collected += daily_tax_tokens
                cumulative_tax_to_staking += daily_tax_to_staking
                cumulative_tax_burned += daily_tax_to_burn
            else:
                daily_tax_tokens = 0
                daily_tax_to_staking = 0
                daily_tax_to_burn = 0
            
            # Rutin burn
            if years <= self.config.burn_duration_years:
                daily_routine_burn = (self.config.total_supply * self.config.annual_burn_rate) / 365
                cumulative_routine_burned += daily_routine_burn
            else:
                daily_routine_burn = 0
            
            # TOTAL BURNED TOKENS
            total_burned = cumulative_tax_burned + cumulative_routine_burned
            
            # REAL CIRCULATING SUPPLY 
            gross_circulating = max(1, base_circulating - total_burned)
            
            # === ENHANCED DYNAMIC STAKING SYSTEM  ===
            
            # Price estimation for staking calculations
            current_price_estimate = current_mcap / gross_circulating if gross_circulating > 0 else final_presale_price
            
            # ENHANCED PRICE VELOCITY CALCULATION 
            price_velocity = (current_price_estimate - previous_price) / max(previous_price, 0.00001)
            self.price_velocity_history.append(price_velocity)
            
            # Price velocity smoothing
            if len(self.price_velocity_history) > staking_params['velocity_window']:
                self.price_velocity_history.pop(0)
            
            # Smoothed price velocity
            velocity_smoothing = staking_params['velocity_smoothing']
            if len(self.price_velocity_history) > 1:
                raw_avg_velocity = np.mean(self.price_velocity_history[-staking_params['velocity_window']:])
                if hasattr(self, 'smoothed_velocity'):
                    self.smoothed_velocity = self.smoothed_velocity * (1 - velocity_smoothing) + raw_avg_velocity * velocity_smoothing
                else:
                    self.smoothed_velocity = raw_avg_velocity
            else:
                self.smoothed_velocity = 0
            
            # ENHANCED PRICE VELOCITY IMPACT ON STAKING 
            velocity_impact = staking_params['price_velocity_impact']
            velocity_effect = 1 + self.smoothed_velocity * velocity_impact
            velocity_effect = max(0.3, min(2.0, velocity_effect))
            
            # Target staking rate calculation
            base_rate = staking_params['base_rate']
            target_staking_rate = base_rate * velocity_effect
            target_staking_rate = max(staking_params['min_rate'], 
                                    min(staking_params['max_rate'], target_staking_rate))
            
            # ENHANCED STAKING MOMENTUM 
            momentum = staking_params['momentum']
            staking_momentum = staking_momentum * momentum + target_staking_rate * (1 - momentum)
            
            # Smooth staking transition
            smoothness = staking_params['smoothness']
            staking_ma = staking_ma * (1 - smoothness) + staking_momentum * smoothness
            smooth_staking_rate = staking_ma
            
            # ENHANCED STAKING DYNAMICS 
            current_staking_ratio = cumulative_staked / gross_circulating if gross_circulating > 0 else 0
            available_for_staking = gross_circulating - cumulative_staked
            
            if smooth_staking_rate > current_staking_ratio:
                # Staking artıyor
                entry_speed = staking_params['entry_speed']
                daily_new_staking = available_for_staking * entry_speed * smooth_staking_rate
                daily_unstaking = 0
            else:
                # Staking azalıyor
                exit_speed = staking_params['exit_speed']
                target_staked = gross_circulating * smooth_staking_rate
                excess_staked = max(0, cumulative_staked - target_staked)
                daily_unstaking = excess_staked * exit_speed
                daily_new_staking = 0
            
            # Update staking
            cumulative_staked = max(0, cumulative_staked + daily_new_staking - daily_unstaking)
            cumulative_staked = min(cumulative_staked, gross_circulating * staking_params['max_rate'])
            
            # === ENHANCED DYNAMIC STAKING APY  ===
            
            # Pool depletion progress
            pool_progress = min(1.0, years / apy_params['duration_years'])
            pool_remaining_ratio = 1 - pool_progress
            
            # Current staking ratio
            current_staking_ratio = cumulative_staked / gross_circulating if gross_circulating > 0 else 0
            
            # ENHANCED APY CALCULATION 
            base_apy = apy_params['base_apy']
            min_apy = apy_params['min_apy']
            max_apy = apy_params['max_apy']
            
            # Pool depletion factor
            pool_factor = apy_params['pool_factor']
            pool_apy_multiplier = 1 + (1 - pool_remaining_ratio) * pool_factor
            
            # Staking saturation factor (ters korelasyon)
            saturation_factor = apy_params['saturation_factor']
            saturation_apy_multiplier = 1 - current_staking_ratio * saturation_factor
            
            # Market demand factor (basit market cap growth rate)
            market_growth_rate = (current_mcap / starting_mcap) ** (1 / max(0.1, months)) - 1 if months > 0.1 else 0
            market_factor = apy_params['market_factor']
            market_apy_multiplier = 1 + market_growth_rate * market_factor
            
            # Combined APY
            current_market_apy = base_apy * pool_apy_multiplier * saturation_apy_multiplier * market_apy_multiplier
            current_market_apy = max(min_apy, min(max_apy, current_market_apy))
            
            # Enhanced Staking rewards calculation 
            total_staking_pool = market_staking_pool + cumulative_tax_to_staking
            
            # Pool release calculation
            if pool_remaining_ratio > 0 and years < apy_params['duration_years']:
                daily_pool_release = (market_staking_pool * pool_remaining_ratio) / (apy_params['duration_years'] * 365)
                max_daily_rewards_from_pool = daily_pool_release
            else:
                max_daily_rewards_from_pool = 0
            
            # APY based daily rewards
            apy_based_daily_rewards = (cumulative_staked * current_market_apy / 100 / 365) if cumulative_staked > 0 else 0
            
            # Actual distributed rewards (limited by pool)
            daily_staking_rewards = min(apy_based_daily_rewards, max_daily_rewards_from_pool)
            daily_staking_rewards += daily_tax_to_staking  # Add tax rewards
            
            # Update distributed rewards
            if distributed_staking_rewards + daily_staking_rewards <= total_staking_pool:
                distributed_staking_rewards += daily_staking_rewards
            else:
                daily_staking_rewards = max(0, total_staking_pool - distributed_staking_rewards)
                distributed_staking_rewards = total_staking_pool
            
            # === REAL EFFECTIVE CIRCULATING SUPPLY  ===
            if self.config.include_staked_in_circulating:
                effective_circulating = gross_circulating  # Staked dahil
            else:
                effective_circulating = max(1, gross_circulating - cumulative_staked)  # Staked hariç
            
            # ENHANCED TOKEN PRICE (SMOOTH) 
            raw_token_price = current_mcap / effective_circulating if effective_circulating > 0 else final_presale_price
            price_ma = price_ma * (1 - self.config.price_smoothing_factor * 2) + raw_token_price * (self.config.price_smoothing_factor * 2)
            token_price = price_ma
            
            price_vs_presale = token_price / final_presale_price
            
            # Store for next iteration
            previous_price = current_price_estimate
            
            mainnet_data.append({
                'gun': day,
                'ay': months,
                'yil': years,
                'ceyrek': quarter + 1,
                'ceyrek_yil': quarter_year,
                'yil_ici_ceyrek': quarter_in_year,
                'mcap_usdt': current_mcap,
                'gross_circulating_supply': gross_circulating,
                'effective_circulating_supply': effective_circulating,
                'token_fiyati': token_price,
                'presale_fiyat_orani': price_vs_presale,
                
                # Enhanced McAp faktörleri 
                'starting_mcap': starting_mcap,
                'ceyrek_carpani': quarter_multiplier,
                'temelli_buyume': fundamental_growth,
                'spekulatif_buyume': speculative_growth,
                'maturity_effect': maturity_effect,
                'maturity_distance_ratio': distance_ratio,
                'toplam_buyume': base_growth,
                'volatilite_etkisi': volatility_effect,
                'market_beta': current_beta,
                'mcap_moving_average': mcap_ma,
                'price_moving_average': price_ma,
                
                # Enhanced Maturity analizi  - SIMPLIFIED
                'maturity_target_mcap': maturity_params['target_mcap'],
                'maturity_progress_pct': (current_mcap / maturity_params['target_mcap']) * 100,
                'maturity_damping_enabled': maturity_params['enabled'],
                'maturity_convergence_speed': maturity_params['convergence_speed'],
                
                # Tax ve burn
                'tax_aktif': tax_active,
                'gunluk_tax_token': daily_tax_tokens,
                'gunluk_tax_staking': daily_tax_to_staking,
                'gunluk_tax_burn': daily_tax_to_burn,
                'kumulatif_tax_toplam': cumulative_tax_collected,
                'kumulatif_tax_staking': cumulative_tax_to_staking,
                'kumulatif_tax_burned': cumulative_tax_burned,
                'gunluk_rutin_burn': daily_routine_burn,
                'kumulatif_rutin_burned': cumulative_routine_burned,
                'toplam_burned': total_burned,
                'etkili_toplam_arz': self.config.total_supply - total_burned,
                
                # Enhanced Staking 
                'price_velocity': price_velocity,
                'smoothed_price_velocity': self.smoothed_velocity,
                'velocity_effect': velocity_effect,
                'target_staking_rate': target_staking_rate,
                'staking_momentum': staking_momentum,
                'smooth_staking_orani': smooth_staking_rate,
                'gunluk_yeni_staking': daily_new_staking,
                'gunluk_unstaking': daily_unstaking,
                'kumulatif_staked': cumulative_staked,
                'staking_orani': current_staking_ratio,
                'staking_moving_average': staking_ma,
                
                # Enhanced Dynamic APY 
                'pool_remaining_ratio': pool_remaining_ratio,
                'pool_apy_multiplier': pool_apy_multiplier,
                'saturation_apy_multiplier': saturation_apy_multiplier,
                'market_apy_multiplier': market_apy_multiplier,
                'max_daily_pool_rewards': max_daily_rewards_from_pool,
                'apy_based_rewards': apy_based_daily_rewards,
                'guncel_market_apy': current_market_apy,
                'gunluk_staking_odul': daily_staking_rewards,
                'dagitilan_staking_odul': distributed_staking_rewards,
                'toplam_staking_havuzu': total_staking_pool,
                
                # Diğer
                'senaryo': scenario,
                'burn_orani_yuzdesi': (total_burned / self.config.total_supply) * 100,
                'dolasim_yuzdesi': (gross_circulating / (self.config.total_supply - total_burned)) * 100,
                'staked_dolasim_yuzdesi': (cumulative_staked / gross_circulating) * 100 if gross_circulating > 0 else 0,
                'effective_dolasim_yuzdesi': (effective_circulating / (self.config.total_supply - total_burned)) * 100
            })
        
        return pd.DataFrame(mainnet_data)
    
    def calculate_individual_vesting_schedules(self, months_projection: int = None) -> pd.DataFrame:
        """📅 Enhanced Vesting Schedules  - AYNI"""
        
        if months_projection is None:
            months_projection = self.config.vesting_analysis_months
        
        vesting_data = []
        
        for month in range(months_projection):
            vesting_month = max(0, month - 6)  # 6 ay gecikme
            
            # === PRESALE ALLOCATION (ANINDA) ===
            presale_tokens = self.config.total_supply * (self.config.presale_allocation / 100)
            vested_presale = presale_tokens if month >= 0 else 0
            
            # === PRESALE STAKING POOL VESTING ===
            presale_staking_tokens = self.config.total_supply * (self.config.presale_staking_pool / 100)
            if vesting_month < self.config.presale_staking_cliff_months:
                vested_presale_staking = 0
            else:
                vesting_progress = min(1.0, (vesting_month - self.config.presale_staking_cliff_months) / 
                                     max(1, self.config.presale_staking_vesting_months - self.config.presale_staking_cliff_months))
                vested_presale_staking = presale_staking_tokens * vesting_progress
            
            # === MARKET STAKING POOL VESTING ===
            market_staking_tokens = self.config.total_supply * (self.config.market_staking_pool / 100)
            if vesting_month < self.config.market_staking_cliff_months:
                vested_market_staking = 0
            else:
                vesting_progress = min(1.0, (vesting_month - self.config.market_staking_cliff_months) / 
                                     max(1, self.config.market_staking_vesting_months - self.config.market_staking_cliff_months))
                vested_market_staking = market_staking_tokens * vesting_progress
            
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
            
            # === CIRCULATING SUPPLY ===
            circulating_supply = total_vested
            circulating_percentage = (circulating_supply / self.config.total_supply * 100)
            
            vesting_data.append({
                'ay': month,
                'vesting_ay': vesting_month,
                
                # Individual components
                'vested_presale': vested_presale,
                'vested_presale_staking': vested_presale_staking,
                'vested_market_staking': vested_market_staking,
                'vested_team': vested_team,
                'vested_dao': vested_dao,
                'vested_marketing': vested_marketing,
                'vested_liquidity': vested_liquidity,
                
                # Totals
                'toplam_vested': total_vested,
                'circulating_supply': circulating_supply,
                'vested_toplam_arz_yuzdesi': vested_percentage_of_total_supply,
                'dolasim_yuzdesi': circulating_percentage,
                
                # Individual percentages
                'presale_staking_vested_pct': (vested_presale_staking / presale_staking_tokens * 100) if presale_staking_tokens > 0 else 0,
                'market_staking_vested_pct': (vested_market_staking / market_staking_tokens * 100) if market_staking_tokens > 0 else 0,
                'team_vested_pct': (vested_team / team_tokens * 100) if team_tokens > 0 else 0,
                'dao_vested_pct': (vested_dao / dao_tokens * 100) if dao_tokens > 0 else 0,
                'marketing_vested_pct': (vested_marketing / marketing_tokens * 100) if marketing_tokens > 0 else 0,
                'liquidity_vested_pct': (vested_liquidity / liquidity_tokens * 100) if liquidity_tokens > 0 else 0,
                
                # Status
                'vesting_basladi': month >= 6
            })
        
        return pd.DataFrame(vesting_data)
    
    def calculate_enhanced_metrics(self, presale_df: pd.DataFrame, 
                                 weekly_df: pd.DataFrame,
                                 vesting_df: pd.DataFrame,
                                 mainnet_df: pd.DataFrame) -> Dict:
        """📊 Enhanced metrikleri hesapla  - AYNI"""
        
        try:
            # Presale Metrics - AYNI
            presale_metrics = {
                'toplam_toplanan_usdt': float(presale_df['kumulatif_toplanan_usdt'].iloc[-1]),
                'satilan_token': float(presale_df['kumulatif_satilan_token'].iloc[-1]),
                'final_presale_fiyati': float(presale_df['fiyat_usdt'].iloc[-1]),
                'presale_fiyat_artisi': float(presale_df['fiyat_artisi'].iloc[-1]),
                'presale_gun_sayisi': len(presale_df),
                'havuz_tukenme_yuzdesi': float(presale_df['havuz_tukenme_yuzdesi'].iloc[-1]),
                'ortalama_apy': float(presale_df['guncel_apy'].mean()),
                'toplam_dagitilan_odul': float(presale_df['toplam_dagitilan_odul'].iloc[-1]),
                'apy_talep_etkisi': float(presale_df['apy_etkisi'].mean()) if 'apy_etkisi' in presale_df.columns else 1.0,
                'fiyat_direnc_etkisi': float(presale_df['fiyat_etkisi'].mean()) if 'fiyat_etkisi' in presale_df.columns else 1.0,
                'ana_para_tokens': float(presale_df['ana_para_tokens'].iloc[-1]) if 'ana_para_tokens' in presale_df.columns else 0,
                'toplam_balance': float(presale_df['toplam_balance'].iloc[-1]) if 'toplam_balance' in presale_df.columns else 0,
                'faiz_tipi': 'SIMPLE',
                'dinamik_apy_kullanimi': True
            }
            
            # Weekly Token Analysis Metrics - AYNI
            weekly_metrics = {
                'toplam_hafta_sayisi': len(weekly_df),
                'ortalama_haftalik_token': float(weekly_df['alinan_token'].mean()) if len(weekly_df) > 0 else 0,
                'ortalama_staking_kazanci': float(weekly_df['staking_kazanci'].mean()) if len(weekly_df) > 0 else 0,
                'ortalama_toplam_token': float(weekly_df['toplam_token'].mean()) if len(weekly_df) > 0 else 0,
                'ortalama_token_kazanc_yuzdesi': float(weekly_df['token_kazanc_yuzdesi'].mean()) if len(weekly_df) > 0 else 0,
                'en_iyi_hafta': int(weekly_df.loc[weekly_df['toplam_token'].idxmax()]['hafta']) if len(weekly_df) > 0 else 1,
                'en_kotu_hafta': int(weekly_df.loc[weekly_df['toplam_token'].idxmin()]['hafta']) if len(weekly_df) > 0 else 1,
                'sabit_yatirim_miktari': self.config.weekly_investment_amount,
                'ortalama_ana_para': float(weekly_df['ana_para_tokens'].mean()) if 'ana_para_tokens' in weekly_df.columns and len(weekly_df) > 0 else 0,
                'faiz_tipi': 'SIMPLE'
            }
            
            # Enhanced Mainnet Metrics 
            max_price_idx = mainnet_df['token_fiyati'].idxmax()
            max_mcap_idx = mainnet_df['mcap_usdt'].idxmax()
            
            # Enhanced: Average User Gains Calculation 
            avg_user_presale_investment = 1000  # $1000 ortalama yatırım
            avg_tokens_bought = avg_user_presale_investment / presale_metrics['final_presale_fiyati']
            peak_value = avg_tokens_bought * float(mainnet_df['token_fiyati'].iloc[max_price_idx])
            avg_user_peak_roi = peak_value / avg_user_presale_investment
            
            # Final değer hesabı
            final_value = avg_tokens_bought * float(mainnet_df['token_fiyati'].iloc[-1])
            avg_user_final_roi = final_value / avg_user_presale_investment
            
            # Enhanced metrics 
            mainnet_metrics = {
                'starting_mcap': self.config.starting_mcap_usdt,
                'launch_mcap': float(mainnet_df['mcap_usdt'].iloc[0]),
                'max_tahmin_fiyat': float(mainnet_df['token_fiyati'].iloc[max_price_idx]),
                'max_fiyat_zamani_ay': float(mainnet_df['ay'].iloc[max_price_idx]),
                'max_mcap': float(mainnet_df['mcap_usdt'].iloc[max_mcap_idx]),
                'presale_fiyat_artisi': float(mainnet_df['presale_fiyat_orani'].iloc[max_price_idx]),
                'final_dolasim_arzi': float(mainnet_df['gross_circulating_supply'].iloc[-1]),
                'final_effective_circulating': float(mainnet_df['effective_circulating_supply'].iloc[-1]),
                'toplam_burned_token': float(mainnet_df['toplam_burned'].iloc[-1]),
                'final_token_fiyati': float(mainnet_df['token_fiyati'].iloc[-1]),
                'max_staking_orani': float(mainnet_df['staking_orani'].max()),
                'final_staking_orani': float(mainnet_df['staking_orani'].iloc[-1]),
                'max_staked_tokens': float(mainnet_df['kumulatif_staked'].max()),
                'ortalama_market_apy': float(mainnet_df['guncel_market_apy'].mean()),
                'final_market_apy': float(mainnet_df['guncel_market_apy'].iloc[-1]),
                'toplam_tax_toplanan': float(mainnet_df['kumulatif_tax_toplam'].iloc[-1]),
                'toplam_tax_burned': float(mainnet_df['kumulatif_tax_burned'].iloc[-1]),
                'toplam_rutin_burned': float(mainnet_df['kumulatif_rutin_burned'].iloc[-1]),
                'senaryo': mainnet_df['senaryo'].iloc[0] if 'senaryo' in mainnet_df.columns else 'base',
                'ceyrek_sayisi': 16,
                'analiz_ay_sayisi': self.config.projection_months,
                
                # Enhanced: Simplified Maturity Metrics 
                'maturity_target_mcap': float(mainnet_df['maturity_target_mcap'].iloc[0]) if 'maturity_target_mcap' in mainnet_df.columns else 0,
                'max_maturity_progress': float(mainnet_df['maturity_progress_pct'].max()) if 'maturity_progress_pct' in mainnet_df.columns else 0,
                'final_maturity_progress': float(mainnet_df['maturity_progress_pct'].iloc[-1]) if 'maturity_progress_pct' in mainnet_df.columns else 0,
                'max_maturity_distance_ratio': float(mainnet_df['maturity_distance_ratio'].max()) if 'maturity_distance_ratio' in mainnet_df.columns else 1.0,
                'min_maturity_distance_ratio': float(mainnet_df['maturity_distance_ratio'].min()) if 'maturity_distance_ratio' in mainnet_df.columns else 1.0,
                'maturity_damping_aktif': self.config.enable_maturity_damping,
                
                # Enhanced: Advanced Dynamic Staking Metrics 
                'max_price_velocity': float(mainnet_df['price_velocity'].max()) if 'price_velocity' in mainnet_df.columns else 0,
                'min_price_velocity': float(mainnet_df['price_velocity'].min()) if 'price_velocity' in mainnet_df.columns else 0,
                'avg_smoothed_velocity': float(mainnet_df['smoothed_price_velocity'].mean()) if 'smoothed_price_velocity' in mainnet_df.columns else 0,
                'max_velocity_effect': float(mainnet_df['velocity_effect'].max()) if 'velocity_effect' in mainnet_df.columns else 1.0,
                'final_pool_remaining': float(mainnet_df['pool_remaining_ratio'].iloc[-1]) if 'pool_remaining_ratio' in mainnet_df.columns else 0,
                'total_unstaking_events': len(mainnet_df[mainnet_df['gunluk_unstaking'] > 0]) if 'gunluk_unstaking' in mainnet_df.columns else 0,
                
                # Enhanced: Average User Gains 
                'ortalama_kullanici_yatirim': avg_user_presale_investment,
                'ortalama_kullanici_token': avg_tokens_bought,
                'ortalama_kullanici_zirve_roi': avg_user_peak_roi,
                'ortalama_kullanici_final_roi': avg_user_final_roi,
                'ortalama_kullanici_zirve_deger': peak_value,
                'ortalama_kullanici_final_deger': final_value,
                
                # System health 
                'system_version': '6.0',
                'simplified_maturity_damping': True,
                'enhanced_dynamic_staking': True,
                'price_velocity_system': True,
                'real_circulating_supply': True
            }
            
            # Vesting Metrics - AYNI
            vesting_metrics = {
                'team_tam_vested_ay': self.config.team_cliff_months + self.config.team_vesting_months,
                'dao_tam_vested_ay': self.config.dao_cliff_months + self.config.dao_vesting_months,
                'marketing_tam_vested_ay': self.config.marketing_cliff_months + self.config.marketing_vesting_months,
                'presale_staking_tam_vested_ay': self.config.presale_staking_cliff_months + self.config.presale_staking_vesting_months,
                'market_staking_tam_vested_ay': self.config.market_staking_cliff_months + self.config.market_staking_vesting_months,
                'yirmidort_ay_toplam_vested': float(vesting_df.iloc[min(23, len(vesting_df)-1)]['toplam_vested']) if len(vesting_df) > 23 else 0,
                'yirmidort_ay_dolasim': float(vesting_df.iloc[min(23, len(vesting_df)-1)]['circulating_supply']) if len(vesting_df) > 23 else 0
            }
            
            return {
                'presale': presale_metrics,
                'haftalik_tokenlar': weekly_metrics,
                'mainnet': mainnet_metrics,
                'vesting': vesting_metrics
            }
            
        except Exception as e:
            st.error(f"Enhanced metrik hesaplama hatası : {e}")
            return {'error': str(e)}