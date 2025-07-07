"""
NXID Enhanced Visualizations Module 
=========================================
Simplified Maturity + New Charts + Reduced Volatility + Turkish Sidebar
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from typing import Dict, List, Tuple
from utils import NXID_COLORS, hex_to_rgb, get_chart_template, display_nxid_logo
from config import EnhancedNXIDConfig
import base64
import os

class EnhancedVisualizationManager:
    """Enhanced Görselleştirme Yöneticisi  - New Charts + Simplified"""
    
    def __init__(self, config: EnhancedNXIDConfig):
        self.config = config
        self.chart_template = get_chart_template()
    
    def create_enhanced_visualizations_v4(self, presale_df: pd.DataFrame, 
                                        weekly_df: pd.DataFrame,
                                        vesting_df: pd.DataFrame,
                                        mainnet_df: pd.DataFrame,
                                        scenario: str) -> Dict[str, go.Figure]:
        """Enhanced Görselleştirmeler  - New Charts + Simplified Maturity"""
        
        charts = {}
        
        # 1. Token dağılımı (logo ile)
        charts['distribution'] = self._create_enhanced_distribution_pie_chart_with_logo()
        
        # 2. Enhanced vesting programı (staking pools ile)
        charts['vesting'] = self._create_enhanced_vesting_schedule_chart(vesting_df)
        
        # 3. Presale temel analiz
        charts['presale_basic'] = self._create_presale_basic_chart(presale_df)
        
        # 4. Presale USD ve Token analizi
        charts['presale_usd_tokens'] = self._create_presale_usd_tokens_chart(presale_df)
        
        # 5. Presale APY + Staking analizi
        charts['presale_apy'] = self._create_presale_apy_staking_analysis(presale_df)
        
        # 6. Haftalık token tracking
        if not weekly_df.empty:
            charts['weekly_tokens'] = self._create_weekly_daily_interest_tracking(weekly_df, presale_df)
        
        # 7. YENİ: Market Cap Evolution Analysis (maturity grafiklerinden ÖNCE)
        charts['mcap_evolution'] = self._create_mcap_evolution_analysis_chart(mainnet_df, scenario)
        
        # 8. YENİ: Total Supply vs Market Cap Analysis
        charts['total_supply_mcap'] = self._create_total_supply_mcap_analysis_chart(mainnet_df, scenario)
        
        # 9. YENİ: Separate Market Cap Analysis
        charts['separate_mcap'] = self._create_separate_mcap_analysis_chart(mainnet_df, scenario)
        
        # 10. YENİ: Circulating Supply Analysis
        charts['circulating_supply'] = self._create_circulating_supply_analysis_chart(mainnet_df, vesting_df)
        
        # 11. Enhanced mainnet market (simplified)
        charts['mainnet_market'] = self._create_enhanced_smooth_mainnet_market_chart(mainnet_df, scenario)
        
        # 12. Enhanced mainnet staking
        charts['mainnet_staking'] = self._create_enhanced_mainnet_staking_chart(mainnet_df)
        
        # 13. YENİ: Simplified Maturity Analysis Chart
        if self.config.enable_maturity_damping and self.config.enable_maturity_analysis:
            charts['maturity_analysis'] = self._create_simplified_maturity_analysis_chart(mainnet_df, scenario)
        
        # 14. Mainnet tax & burn
        charts['mainnet_tax_burn'] = self._create_mainnet_tax_burn_chart(mainnet_df)
        
        return charts
    
    def _create_enhanced_distribution_pie_chart_with_logo(self) -> go.Figure:
        """Token dağılımı - NXID logo ile enhanced"""
        labels = ['Presale Tahsisi', 'Market Staking Havuzu', 'Team', 'DAO Hazinesi', 
                 'Pazarlama', 'Likidite', 'Presale Staking Havuzu']
        values = [
            self.config.presale_allocation,
            self.config.market_staking_pool,
            self.config.team_allocation,
            self.config.dao_treasury,
            self.config.marketing,
            self.config.liquidity,
            self.config.presale_staking_pool
        ]
        
        colors = [
            NXID_COLORS['primary'],      # Presale tahsisi - mavi
            NXID_COLORS['teal'],         # Market staking - teal
            NXID_COLORS['purple'],       # Team - mor
            NXID_COLORS['indigo'],       # DAO - indigo
            NXID_COLORS['orange'],       # Marketing - turuncu
            NXID_COLORS['success'],      # Liquidity - yeşil
            NXID_COLORS['gold'],         # Presale staking - altın
        ]
        
        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=0.45,  # Daha büyük delik logo için
            textinfo='label+percent',
            textposition='outside',
            textfont=dict(size=13, color=NXID_COLORS['light'], family='Inter', weight='bold'),
            marker=dict(
                colors=colors,
                line=dict(width=2, color=NXID_COLORS['dark'])
            ),
            pull=[0.05 for _ in labels],  # Biraz daha çekili
            hovertemplate='<b>%{label}</b><br>%{percent}<br>%{value:.1f}%<br><b>%{customdata:.1f}B NXID</b><extra></extra>',
            customdata=[v * self.config.total_supply / 100 / 1e9 for v in values],
            rotation=90
        )])
        
        # Logo ekleme - SVG logo merkeze
        logo_svg = self._get_svg_logo_for_pie_chart()
        
        template_config = self.chart_template.copy()
        template_config.update({
            'title': dict(
                text='<b>NXID Token Dağılımı - 100B Toplam Arz</b>',
                x=0.5, y=0.95,
                font=dict(color=NXID_COLORS['primary'], size=28, family='Orbitron')
            ),
            'height': 650,
            'showlegend': True,
            'legend': dict(
                orientation="h",
                yanchor="top",
                y=-0.05,
                xanchor="center",
                x=0.5,
                font=dict(color=NXID_COLORS['light'], size=12, family='Inter')
            ),
            'annotations': [
                dict(
                    text=logo_svg,
                    x=0.5, y=0.5,
                    showarrow=False,
                    xanchor="center",
                    yanchor="middle",
                    font=dict(size=1)
                )
            ]
        })
        
        fig.update_layout(**template_config)
        return fig
    
    def _get_svg_logo_for_pie_chart(self) -> str:
        """NXID yazısını pie chart merkezi için hazırla"""
        return '''<span style="
            font-family: 'Orbitron', monospace;
            font-weight: 900;
            font-size: 32px;
            color: #1B8EF2;
            text-shadow: 0 0 15px rgba(27, 142, 242, 0.8);
            letter-spacing: 2px;
        ">NXID</span>'''
                  
    def _create_separate_mcap_analysis_chart(self, mainnet_df: pd.DataFrame, scenario: str) -> go.Figure:
        """YENİ: Separate Market Cap Analysis Chart"""
        scenario_color = NXID_COLORS['danger'] if scenario == 'bear' else (
            NXID_COLORS['success'] if scenario == 'bull' else NXID_COLORS['primary']
        )
        
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=[f'Market Cap Evolution - {scenario.upper()} Scenario', 
                           'Market Cap Components and Maturity Progress'],
            specs=[[{"secondary_y": True}], [{"secondary_y": True}]],
            vertical_spacing=0.15
        )
        
        # === 1. MARKET CAP EVOLUTION ===
        fig.add_trace(
            go.Scatter(x=mainnet_df['ay'], y=mainnet_df['mcap_usdt']/1e6,
                      name=f'Market Cap - {scenario.upper()} (M$)', 
                      line=dict(color=scenario_color, width=5),
                      fill='tonexty', fillcolor=f"rgba{hex_to_rgb(scenario_color) + (0.2,)}",
                      hovertemplate=f'<b>%{{x:.1f}}. Ay</b><br>McAp: $%{{y:.1f}}M<br>Senaryo: {scenario.upper()}<extra></extra>'),
            row=1, col=1
        )
        
        # Starting McAp line
        starting_mcap_line = [self.config.starting_mcap_usdt / 1e6] * len(mainnet_df)
        fig.add_trace(
            go.Scatter(x=mainnet_df['ay'], y=starting_mcap_line,
                      mode='lines', name=f'Starting McAp: ${self.config.starting_mcap_usdt/1e6:.1f}M',
                      line=dict(color=NXID_COLORS['accent'], width=3, dash='dash'),
                      hovertemplate=f'<b>Starting McAp</b><br>${self.config.starting_mcap_usdt/1e6:.1f}M<extra></extra>'),
            row=1, col=1
        )
        
        # Maturity Target line
        if 'maturity_target_mcap' in mainnet_df.columns:
            maturity_target = mainnet_df['maturity_target_mcap'].iloc[0] / 1e6
            target_line = [maturity_target] * len(mainnet_df)
            fig.add_trace(
                go.Scatter(x=mainnet_df['ay'], y=target_line,
                          mode='lines', name=f'Maturity Target: ${maturity_target:.0f}M',
                          line=dict(color=NXID_COLORS['gold'], width=4, dash='dot'),
                          hovertemplate=f'<b>Maturity Target</b><br>${maturity_target:.0f}M<extra></extra>'),
                row=1, col=1
            )
        
        # McAp Growth Rate
        if len(mainnet_df) > 30:
            mcap_growth_rate = ((mainnet_df['mcap_usdt'] / mainnet_df['mcap_usdt'].shift(30).fillna(mainnet_df['mcap_usdt'].iloc[0])) - 1) * 100
            fig.add_trace(
                go.Scatter(x=mainnet_df['ay'], y=mcap_growth_rate,
                          name='Monthly Growth Rate %', 
                          line=dict(color=NXID_COLORS['orange'], width=3),
                          hovertemplate='<b>%{x:.1f}. Ay</b><br>Growth: %{y:.1f}%<extra></extra>'),
                row=1, col=1, secondary_y=True
            )
        
        # === 2. MCAP COMPONENTS AND MATURITY ===
        # Maturity progress
        if 'maturity_progress_pct' in mainnet_df.columns:
            fig.add_trace(
                go.Scatter(x=mainnet_df['ay'], y=mainnet_df['maturity_progress_pct'],
                          name='Maturity Progress %', 
                          line=dict(color=NXID_COLORS['success'], width=4),
                          fill='tonexty', fillcolor=f"rgba{hex_to_rgb(NXID_COLORS['success']) + (0.3,)}",
                          hovertemplate='<b>%{x:.1f}}. Ay</b><br>Maturity: %{y:.1f}%<extra></extra>'),
                row=2, col=1
            )
        
        # Maturity effect multiplier
        if 'maturity_effect' in mainnet_df.columns:
            fig.add_trace(
                go.Scatter(x=mainnet_df['ay'], y=mainnet_df['maturity_effect'],
                          name='Maturity Effect Multiplier', 
                          line=dict(color=NXID_COLORS['purple'], width=3),
                          hovertemplate='<b>%{x:.1f}. Ay</b><br>Effect: %{y:.2f}x<extra></extra>'),
                row=2, col=1, secondary_y=True
            )
        
        # Target achievement line
        fig.add_hline(
            y=100,
            line_dash="solid",
            line_color=NXID_COLORS['gold'],
            line_width=3,
            annotation_text="Target Achievement (100%)",
            row=2, col=1
        )
        
        fig.update_xaxes(title_text="Mainnet Ayı", row=2, col=1)
        fig.update_yaxes(title_text="Market Cap (Milyon $)", row=1, col=1)
        fig.update_yaxes(title_text="Growth Rate (%)", secondary_y=True, row=1, col=1)
        fig.update_yaxes(title_text="Maturity Progress (%)", row=2, col=1)
        fig.update_yaxes(title_text="Effect Multiplier", secondary_y=True, row=2, col=1)
        
        template_config = self.chart_template.copy()
        template_config.update({
            'title': dict(text=f'<b>Market Cap Analysis - ${self.config.maturity_target_mcap/1e9:.1f}B Target</b>', x=0.5,
                        font=dict(size=26, color=scenario_color)),
            'height': 750,
            'hovermode': 'x unified'
        })
        
        fig.update_layout(**template_config)
        return fig
    
    def _create_circulating_supply_analysis_chart(self, mainnet_df: pd.DataFrame, vesting_df: pd.DataFrame) -> go.Figure:
        """YENİ: Circulating Supply Analysis Chart"""
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=['Circulating Supply Types Comparison', 
                           'Token Burn Impact and Supply Reduction'],
            specs=[[{"secondary_y": True}], [{"secondary_y": True}]],
            vertical_spacing=0.15
        )
        
        # === 1. CIRCULATING SUPPLY TYPES ===
        fig.add_trace(
            go.Scatter(x=mainnet_df['ay'], y=mainnet_df['gross_circulating_supply']/1e9,
                      name='Gross Circulating Supply (B)', 
                      line=dict(color=NXID_COLORS['primary'], width=4),
                      fill='tonexty', fillcolor=f"rgba{hex_to_rgb(NXID_COLORS['primary']) + (0.2,)}",
                      hovertemplate='<b>%{x:.1f}. Ay</b><br>Gross: %{y:.1f}B NXID<extra></extra>'),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Scatter(x=mainnet_df['ay'], y=mainnet_df['effective_circulating_supply']/1e9,
                      name='Effective Circulating Supply (B)', 
                      line=dict(color=NXID_COLORS['success'], width=4),
                      hovertemplate='<b>%{x:.1f}. Ay</b><br>Effective: %{y:.1f}B NXID<extra></extra>'),
            row=1, col=1
        )
        
        # Staked tokens (removed from effective)
        if 'kumulatif_staked' in mainnet_df.columns:
            fig.add_trace(
                go.Scatter(x=mainnet_df['ay'], y=mainnet_df['kumulatif_staked']/1e9,
                          name='Staked Tokens (B)', 
                          line=dict(color=NXID_COLORS['teal'], width=3, dash='dot'),
                          hovertemplate='<b>%{x:.1f}. Ay</b><br>Staked: %{y:.1f}B NXID<extra></extra>'),
                row=1, col=1
            )
        
        # Supply efficiency ratio
        supply_efficiency = (mainnet_df['effective_circulating_supply'] / mainnet_df['gross_circulating_supply'] * 100)
        fig.add_trace(
            go.Scatter(x=mainnet_df['ay'], y=supply_efficiency,
                      name='Supply Efficiency %', 
                      line=dict(color=NXID_COLORS['orange'], width=3),
                      hovertemplate='<b>%{x:.1f}. Ay</b><br>Efficiency: %{y:.1f}%<extra></extra>'),
            row=1, col=1, secondary_y=True
        )
        
        # === 2. BURN IMPACT ===
        fig.add_trace(
            go.Scatter(x=mainnet_df['ay'], y=mainnet_df['toplam_burned']/1e6,
                      name='Total Burned Tokens (M)', 
                      line=dict(color=NXID_COLORS['burn'], width=5),
                      fill='tonexty', fillcolor=f"rgba{hex_to_rgb(NXID_COLORS['burn']) + (0.3,)}",
                      hovertemplate='<b>%{x:.1f}. Ay</b><br>Burned: %{y:.1f}M NXID<extra></extra>'),
            row=2, col=1
        )
        
        # Tax burned vs routine burned
        if 'kumulatif_tax_burned' in mainnet_df.columns:
            fig.add_trace(
                go.Scatter(x=mainnet_df['ay'], y=mainnet_df['kumulatif_tax_burned']/1e6,
                          name='Tax Burned (M)', 
                          line=dict(color=NXID_COLORS['tax'], width=3),
                          hovertemplate='<b>%{x:.1f}. Ay</b><br>Tax Burn: %{y:.1f}M NXID<extra></extra>'),
                row=2, col=1
            )
        
        fig.add_trace(
            go.Scatter(x=mainnet_df['ay'], y=mainnet_df['kumulatif_rutin_burned']/1e6,
                      name='Routine Burned (M)', 
                      line=dict(color=NXID_COLORS['orange'], width=3),
                      hovertemplate='<b>%{x:.1f}. Ay</b><br>Routine Burn: %{y:.1f}M NXID<extra></extra>'),
            row=2, col=1
        )
        
        # Burn percentage of total supply
        fig.add_trace(
            go.Scatter(x=mainnet_df['ay'], y=mainnet_df['burn_orani_yuzdesi'],
                      name='Burn % of Total Supply', 
                      line=dict(color=NXID_COLORS['danger'], width=4),
                      hovertemplate='<b>%{x:.1f}. Ay</b><br>Burned: %{y:.2f}% of supply<extra></extra>'),
            row=2, col=1, secondary_y=True
        )
        
        fig.update_xaxes(title_text="Mainnet Ayı", row=2, col=1)
        fig.update_yaxes(title_text="Circulating Supply (Milyar NXID)", row=1, col=1)
        fig.update_yaxes(title_text="Efficiency (%)", secondary_y=True, row=1, col=1)
        fig.update_yaxes(title_text="Burned Tokens (Milyon NXID)", row=2, col=1)
        fig.update_yaxes(title_text="Burn Percentage (%)", secondary_y=True, row=2, col=1)
        
        template_config = self.chart_template.copy()
        template_config.update({
            'title': dict(text='<b>Circulating Supply & Burn Analysis </b>', x=0.5,
                        font=dict(size=26, color=NXID_COLORS['primary'])),
            'height': 750,
            'hovermode': 'x unified'
        })
        
        fig.update_layout(**template_config)
        return fig
    
    def _create_simplified_maturity_analysis_chart(self, mainnet_df: pd.DataFrame, scenario: str) -> go.Figure:
        """YENİ: Simplified Maturity Analysis Chart"""
        scenario_color = NXID_COLORS['danger'] if scenario == 'bear' else (
            NXID_COLORS['success'] if scenario == 'bull' else NXID_COLORS['primary']
        )
        
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=['Simplified Maturity Progress and Target Distance', 
                           'Maturity Boost/Damp Effect Over Time'],
            specs=[[{"secondary_y": True}], [{"secondary_y": True}]],
            vertical_spacing=0.15
        )
        
        # === 1. MATURITY PROGRESS ===
        if 'maturity_progress_pct' in mainnet_df.columns:
            fig.add_trace(
                go.Scatter(x=mainnet_df['ay'], y=mainnet_df['maturity_progress_pct'],
                          name='Maturity Progress %', 
                          line=dict(color=NXID_COLORS['success'], width=5),
                          fill='tonexty', fillcolor=f"rgba{hex_to_rgb(NXID_COLORS['success']) + (0.3,)}",
                          hovertemplate='<b>%{x:.1f}. Ay</b><br>Progress: %{y:.1f}%<extra></extra>'),
                row=1, col=1
            )
        
        # Target achievement line
        fig.add_hline(
            y=100,
            line_dash="solid",
            line_color=NXID_COLORS['gold'],
            line_width=3,
            annotation_text="Maturity Target (100%)",
            row=1, col=1
        )
        
        # Distance ratio (above/below target)
        if 'maturity_distance_ratio' in mainnet_df.columns:
            distance_pct = (mainnet_df['maturity_distance_ratio'] - 1.0) * 100
            fig.add_trace(
                go.Scatter(x=mainnet_df['ay'], y=distance_pct,
                          name='Distance from Target %', 
                          line=dict(color=NXID_COLORS['orange'], width=3),
                          hovertemplate='<b>%{x:.1f}. Ay</b><br>Distance: %{y:.1f}%<extra></extra>'),
                row=1, col=1, secondary_y=True
            )
            
            # Zero line for target
            fig.add_hline(
                y=0,
                line_dash="dash",
                line_color=NXID_COLORS['accent'],
                line_width=2,
                annotation_text="At Target",
                row=1, col=1, secondary_y=True
            )
        
        # === 2. MATURITY EFFECT ===
        if 'maturity_effect' in mainnet_df.columns:
            fig.add_trace(
                go.Scatter(x=mainnet_df['ay'], y=mainnet_df['maturity_effect'],
                          name='Maturity Effect Multiplier', 
                          line=dict(color=NXID_COLORS['purple'], width=5),
                          fill='tonexty', fillcolor=f"rgba{hex_to_rgb(NXID_COLORS['purple']) + (0.2,)}",
                          hovertemplate='<b>%{x:.1f}. Ay</b><br>Effect: %{y:.2f}x<extra></extra>'),
                row=2, col=1
            )
        
        # Neutral effect line (1.0x)
        fig.add_hline(
            y=1.0,
            line_dash="solid",
            line_color=NXID_COLORS['accent'],
            line_width=3,
            annotation_text="Neutral Effect (1.0x)",
            row=2, col=1
        )
        
        # Boost zone (above 1.0)
        fig.add_hrect(
            y0=1.0, y1=1.5,
            fillcolor=NXID_COLORS['success'], opacity=0.1,
            annotation_text="BOOST ZONE", annotation_position="top left",
            row=2, col=1
        )
        
        # Damp zone (below 1.0)
        fig.add_hrect(
            y0=0.7, y1=1.0,
            fillcolor=NXID_COLORS['danger'], opacity=0.1,
            annotation_text="DAMP ZONE", annotation_position="bottom left",
            row=2, col=1
        )
        
        # Current vs target McAp
        if 'maturity_target_mcap' in mainnet_df.columns:
            fig.add_trace(
                go.Scatter(x=mainnet_df['ay'], y=mainnet_df['mcap_usdt']/mainnet_df['maturity_target_mcap'],
                          name='Current/Target Ratio', 
                          line=dict(color=scenario_color, width=3),
                          hovertemplate=f'<b>%{{x:.1f}}. Ay</b><br>Ratio: %{{y:.2f}}<br>{scenario.upper()}<extra></extra>'),
                row=2, col=1, secondary_y=True
            )
        
        fig.update_xaxes(title_text="Mainnet Ayı", row=2, col=1)
        fig.update_yaxes(title_text="Progress (%)", row=1, col=1)
        fig.update_yaxes(title_text="Distance (%)", secondary_y=True, row=1, col=1)
        fig.update_yaxes(title_text="Effect Multiplier", row=2, col=1)
        fig.update_yaxes(title_text="Current/Target Ratio", secondary_y=True, row=2, col=1)
        
        template_config = self.chart_template.copy()
        template_config.update({
            'title': dict(text=f'<b>Simplified Maturity Analysis - ${self.config.maturity_target_mcap/1e9:.1f}B Target</b>', x=0.5,
                        font=dict(size=24, color=NXID_COLORS['gold'])),
            'height': 700,
            'hovermode': 'x unified'
        })
        
        fig.update_layout(**template_config)
        return fig
    
    def _create_enhanced_vesting_schedule_chart(self, vesting_df: pd.DataFrame) -> go.Figure:
        """Enhanced vesting programı - staking pools dahil"""
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=['Token Release Schedule (Including Staking Pools)', 
                           'Circulating Supply Growth'],
            specs=[[{"secondary_y": False}], [{"secondary_y": True}]],
            vertical_spacing=0.15
        )
        
        # Anında serbest bırakılan tokenlar
        aninda_serbest = (vesting_df.get('vested_presale', 0) + 
                         vesting_df.get('vested_liquidity', 0) + 
                         vesting_df.get('vested_presale_staking', 0))
        
        # Stacked area chart
        fig.add_trace(go.Scatter(
            x=vesting_df['ay'], 
            y=aninda_serbest/1e9,
            mode='lines', 
            name='Instant Release (Presale + Liquidity + Presale Staking)', 
            fill='tozeroy',
            line=dict(color=NXID_COLORS['primary'], width=2),
            fillcolor=f"rgba{hex_to_rgb(NXID_COLORS['primary']) + (0.7,)}",
            hovertemplate='<b>Instant Release</b><br>Month: %{x}<br>Released: %{y:.1f}B NXID<extra></extra>'
        ), row=1, col=1)
        
        # Market staking pool vesting
        cumulative = aninda_serbest
        if 'vested_market_staking' in vesting_df.columns:
            fig.add_trace(go.Scatter(
                x=vesting_df['ay'], 
                y=(cumulative + vesting_df['vested_market_staking'])/1e9,
                mode='lines', 
                name='Market Staking Pool (Vesting)', 
                fill='tonexty',
                line=dict(color=NXID_COLORS['teal'], width=2),
                fillcolor=f"rgba{hex_to_rgb(NXID_COLORS['teal']) + (0.7,)}",
                hovertemplate='<b>Market Staking Pool</b><br>Month: %{x}<br>Total: %{y:.1f}B NXID<extra></extra>'
            ), row=1, col=1)
            cumulative += vesting_df['vested_market_staking']
        
        # Marketing
        if 'vested_marketing' in vesting_df.columns:
            fig.add_trace(go.Scatter(
                x=vesting_df['ay'], 
                y=(cumulative + vesting_df['vested_marketing'])/1e9,
                mode='lines', 
                name='Marketing', 
                fill='tonexty',
                line=dict(color=NXID_COLORS['orange'], width=2),
                fillcolor=f"rgba{hex_to_rgb(NXID_COLORS['orange']) + (0.7,)}",
                hovertemplate='<b>Marketing</b><br>Month: %{x}<br>Total: %{y:.1f}B NXID<extra></extra>'
            ), row=1, col=1)
            cumulative += vesting_df['vested_marketing']
        
        # DAO Treasury
        if 'vested_dao' in vesting_df.columns:
            fig.add_trace(go.Scatter(
                x=vesting_df['ay'], 
                y=(cumulative + vesting_df['vested_dao'])/1e9,
                mode='lines', 
                name='DAO Treasury', 
                fill='tonexty',
                line=dict(color=NXID_COLORS['indigo'], width=2),
                fillcolor=f"rgba{hex_to_rgb(NXID_COLORS['indigo']) + (0.7,)}",
                hovertemplate='<b>DAO Treasury</b><br>Month: %{x}<br>Total: %{y:.1f}B NXID<extra></extra>'
            ), row=1, col=1)
            cumulative += vesting_df['vested_dao']
        
        # Team (en üstte)
        if 'vested_team' in vesting_df.columns:
            fig.add_trace(go.Scatter(
                x=vesting_df['ay'], 
                y=(cumulative + vesting_df['vested_team'])/1e9,
                mode='lines', 
                name='Team', 
                fill='tonexty',
                line=dict(color=NXID_COLORS['purple'], width=2),
                fillcolor=f"rgba{hex_to_rgb(NXID_COLORS['purple']) + (0.7,)}",
                hovertemplate='<b>Team</b><br>Month: %{x}<br>Total: %{y:.1f}B NXID<extra></extra>'
            ), row=1, col=1)
        
        # Dolaşımdaki arz
        fig.add_trace(go.Scatter(
            x=vesting_df['ay'], 
            y=vesting_df['circulating_supply']/1e9,
            mode='lines', 
            name='Circulating Supply (B)', 
            line=dict(color=NXID_COLORS['secondary'], width=4),
            hovertemplate='<b>Circulating Supply</b><br>Month: %{x}<br>Supply: %{y:.1f}B NXID<extra></extra>'
        ), row=2, col=1)
        
        # Dolaşım yüzdesi
        fig.add_trace(go.Scatter(
            x=vesting_df['ay'], 
            y=vesting_df['dolasim_yuzdesi'],
            mode='lines', 
            name='Circulation %', 
            line=dict(color=NXID_COLORS['accent'], width=3),
            hovertemplate='<b>Circulation Percentage</b><br>Month: %{x}<br>Percentage: %{y:.1f}%<extra></extra>'
        ), row=2, col=1, secondary_y=True)
        
        # Vesting başlangıcı
        fig.add_vline(
            x=6,
            line_dash="solid",
            line_color=NXID_COLORS['gold'],
            line_width=3,
            annotation_text="Vesting Start (Month 6)",
            annotation_position="top left"
        )
        
        # Market staking pool vesting başlangıcı
        fig.add_vline(
            x=6 + self.config.market_staking_cliff_months,
            line_dash="dash",
            line_color=NXID_COLORS['teal'],
            line_width=2,
            annotation_text="Market Staking Pool Start",
            annotation_position="top right"
        )
        
        fig.update_xaxes(title_text="Month", row=2, col=1)
        fig.update_yaxes(title_text="Released Tokens (Billion NXID)", row=1, col=1)
        fig.update_yaxes(title_text="Circulating Supply (Billion NXID)", row=2, col=1)
        fig.update_yaxes(title_text="Circulation Percentage (%)", secondary_y=True, row=2, col=1)
        
        template_config = self.chart_template.copy()
        template_config.update({
            'title': dict(text='<b>Enhanced Token Release Program </b>', x=0.5,
                        font=dict(size=26, color=NXID_COLORS['primary'])),
            'height': 750,
            'hovermode': 'x unified'
        })
        
        fig.update_layout(**template_config)
        return fig
    
    def _create_enhanced_smooth_mainnet_market_chart(self, mainnet_df: pd.DataFrame, scenario: str) -> go.Figure:
        """Enhanced smooth mainnet market chart + simplified maturity"""
        scenario_color = NXID_COLORS['danger'] if scenario == 'bear' else (
            NXID_COLORS['success'] if scenario == 'bull' else NXID_COLORS['primary']
        )
        
        fig = make_subplots(
            rows=3, cols=1,
            subplot_titles=[f'Smooth Token Fiyat - {scenario.upper()} + Simplified Maturity', 
                           f'Enhanced Market Dynamics - 16 Çeyrek',
                           'Volatilite ve Smooth Faktörleri (Reduced)'],
            specs=[[{"secondary_y": True}], [{"secondary_y": True}], [{"secondary_y": True}]],
            vertical_spacing=0.12
        )
        
        # === 1. SMOOTH FİYAT ===
        fig.add_trace(
            go.Scatter(x=mainnet_df['ay'], y=mainnet_df['token_fiyati'],
                      name=f'Smooth Token Fiyatı - {scenario.upper()}', 
                      line=dict(color=scenario_color, width=4),
                      fill='tonexty', fillcolor=f"rgba{hex_to_rgb(scenario_color) + (0.2,)}",
                      hovertemplate=f'<b>%{{x:.1f}}. Ay</b><br>Fiyat: $%{{y:.6f}}<br>Senaryo: {scenario.upper()}<extra></extra>'),
            row=1, col=1
        )
        
        # Moving average line
        if 'price_moving_average' in mainnet_df.columns:
            fig.add_trace(
                go.Scatter(x=mainnet_df['ay'], y=mainnet_df['price_moving_average'],
                          name='Price Moving Average', 
                          line=dict(color=NXID_COLORS['accent'], width=2, dash='dot'),
                          hovertemplate='<b>%{x:.1f}. Ay</b><br>MA Fiyat: $%{y:.6f}<extra></extra>'),
                row=1, col=1
            )
        
        # Presale karşılaştırması
        fig.add_trace(
            go.Scatter(x=mainnet_df['ay'], y=mainnet_df['presale_fiyat_orani'],
                      name='Presale Fiyat Oranı (x)', 
                      line=dict(color=NXID_COLORS['gold'], width=3),
                      hovertemplate='<b>%{x:.1f}. Ay</b><br>Presale\'e Göre: %{y:.1f}x<extra></extra>'),
            row=1, col=1, secondary_y=True
        )
        
        # === 2. MARKET DYNAMICS ===
        # Temelli büyüme
        fig.add_trace(
            go.Scatter(x=mainnet_df['ay'], y=mainnet_df['temelli_buyume'],
                      name='Fundamental Growth', 
                      line=dict(color=NXID_COLORS['success'], width=3),
                      hovertemplate='<b>%{x:.1f}. Ay</b><br>Fundamental: %{y:.2f}x<extra></extra>'),
            row=2, col=1
        )
        
        # Spekülatif büyüme
        fig.add_trace(
            go.Scatter(x=mainnet_df['ay'], y=mainnet_df['spekulatif_buyume'],
                      name='Speculative Growth', 
                      line=dict(color=NXID_COLORS['orange'], width=3),
                      hovertemplate='<b>%{x:.1f}. Ay</b><br>Speculative: %{y:.2f}x<extra></extra>'),
            row=2, col=1
        )
        
        # Maturity effect
        if 'maturity_effect' in mainnet_df.columns:
            fig.add_trace(
                go.Scatter(x=mainnet_df['ay'], y=mainnet_df['maturity_effect'],
                          name='Simplified Maturity Effect', 
                          line=dict(color=NXID_COLORS['purple'], width=4),
                          hovertemplate='<b>%{x:.1f}. Ay</b><br>Maturity: %{y:.2f}x<extra></extra>'),
                row=2, col=1, secondary_y=True
            )
        
        # === 3. REDUCED VOLATILITY FACTORS ===
        # Çeyrek çarpanları
        fig.add_trace(
            go.Scatter(x=mainnet_df['ay'], y=mainnet_df['ceyrek_carpani'],
                      name='Çeyrek Çarpanı', 
                      line=dict(color=NXID_COLORS['teal'], width=3),
                      hovertemplate='<b>%{x:.1f}. Ay</b><br>Çarpan: %{y:.2f}x<br>Çeyrek: %{customdata}<extra></extra>',
                      customdata=mainnet_df['ceyrek']),
            row=3, col=1
        )
        
        # Reduced volatilite etkisi
        fig.add_trace(
            go.Scatter(x=mainnet_df['ay'], y=mainnet_df['volatilite_etkisi'],
                      name='Reduced Volatilite Etkisi', 
                      line=dict(color=NXID_COLORS['orange'], width=2),
                      hovertemplate='<b>%{x:.1f}. Ay</b><br>Volatilite: %{y:.3f}<extra></extra>'),
            row=3, col=1, secondary_y=True
        )
        
        # Market beta
        if 'market_beta' in mainnet_df.columns:
            fig.add_trace(
                go.Scatter(x=mainnet_df['ay'], y=mainnet_df['market_beta'],
                          name='Market Beta', 
                          line=dict(color=NXID_COLORS['pink'], width=2, dash='dot'),
                          hovertemplate='<b>%{x:.1f}. Ay</b><br>Beta: %{y:.2f}<extra></extra>'),
                row=3, col=1, secondary_y=True
            )
        
        fig.update_xaxes(title_text="Mainnet Ayı", row=3, col=1)
        fig.update_yaxes(title_text="Token Fiyatı ($)", row=1, col=1)
        fig.update_yaxes(title_text="Presale Oranı (x)", secondary_y=True, row=1, col=1)
        fig.update_yaxes(title_text="Growth Multipliers", row=2, col=1)
        fig.update_yaxes(title_text="Maturity Effect", secondary_y=True, row=2, col=1)
        fig.update_yaxes(title_text="Çarpanlar", row=3, col=1)
        fig.update_yaxes(title_text="Volatilite & Beta", secondary_y=True, row=3, col=1)
        
        template_config = self.chart_template.copy()
        template_config.update({
            'title': dict(text=f'<b>Enhanced Smooth Mainnet + Simplified Maturity - {scenario.upper()}</b>', x=0.5,
                        font=dict(size=24, color=scenario_color)),
            'height': 900,
            'hovermode': 'x unified'
        })
        
        fig.update_layout(**template_config)
        return fig
    
    def _create_enhanced_mainnet_staking_chart(self, mainnet_df: pd.DataFrame) -> go.Figure:
        """Enhanced mainnet staking chart - smooth ile"""
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=['Smooth Price-Sensitive Staking Dynamics', 
                           'Enhanced Staking Rewards ve APY Evolution'],
            specs=[[{"secondary_y": True}], [{"secondary_y": True}]],
            vertical_spacing=0.15
        )
        
        # === 1. SMOOTH STAKING DYNAMİCS ===
        fig.add_trace(
            go.Scatter(x=mainnet_df['ay'], y=mainnet_df['staking_orani']*100,
                      name='Smooth Staking Ratio %', 
                      line=dict(color=NXID_COLORS['teal'], width=4),
                      fill='tonexty', fillcolor=f"rgba{hex_to_rgb(NXID_COLORS['teal']) + (0.3,)}",
                      hovertemplate='<b>%{x:.1f}. Ay</b><br>Staking: %{y:.1f}%<extra></extra>'),
            row=1, col=1
        )
        
        # Smooth staking moving average
        if 'staking_moving_average' in mainnet_df.columns:
            fig.add_trace(
                go.Scatter(x=mainnet_df['ay'], y=mainnet_df['staking_moving_average']*100,
                          name='Staking MA %', 
                          line=dict(color=NXID_COLORS['accent'], width=2, dash='dot'),
                          hovertemplate='<b>%{x:.1f}. Ay</b><br>Staking MA: %{y:.1f}%<extra></extra>'),
                row=1, col=1
            )
        
        # Token fiyatı (smooth)
        fig.add_trace(
            go.Scatter(x=mainnet_df['ay'], y=mainnet_df['token_fiyati'],
                      name='Smooth Token Price ($)', 
                      line=dict(color=NXID_COLORS['primary'], width=3),
                      hovertemplate='<b>%{x:.1f}. Ay</b><br>Fiyat: $%{y:.6f}<extra></extra>'),
            row=1, col=1, secondary_y=True
        )
        
        # Price velocity effect
        if 'velocity_effect' in mainnet_df.columns:
            fig.add_trace(
                go.Scatter(x=mainnet_df['ay'], y=mainnet_df['velocity_effect'],
                          name='Price Velocity Effect', 
                          line=dict(color=NXID_COLORS['orange'], width=2),
                          hovertemplate='<b>%{x:.1f}. Ay</b><br>Velocity Effect: %{y:.2f}x<extra></extra>'),
                row=1, col=1, secondary_y=True
            )
        
        # === 2. STAKING REWARDS ===
        fig.add_trace(
            go.Scatter(x=mainnet_df['ay'], y=mainnet_df['dagitilan_staking_odul']/1e9,
                      name='Distributed Staking Rewards (B)', 
                      line=dict(color=NXID_COLORS['success'], width=4),
                      fill='tonexty', fillcolor=f"rgba{hex_to_rgb(NXID_COLORS['success']) + (0.3,)}",
                      hovertemplate='<b>%{x:.1f}. Ay</b><br>Dağıtılan: %{y:.2f}B NXID<extra></extra>'),
            row=2, col=1
        )
        
        # Market APY (smooth)
        fig.add_trace(
            go.Scatter(x=mainnet_df['ay'], y=mainnet_df['guncel_market_apy'],
                      name='Smooth Market APY %', 
                      line=dict(color=NXID_COLORS['gold'], width=3),
                      hovertemplate='<b>%{x:.1f}. Ay</b><br>APY: %{y:.1f}%<extra></extra>'),
            row=2, col=1, secondary_y=True
        )
        
        # Staked token amount
        if 'kumulatif_staked' in mainnet_df.columns:
            fig.add_trace(
                go.Scatter(x=mainnet_df['ay'], y=mainnet_df['kumulatif_staked']/1e9,
                          name='Staked Tokens (B)', 
                          line=dict(color=NXID_COLORS['purple'], width=2, dash='dot'),
                          hovertemplate='<b>%{x:.1f}. Ay</b><br>Staked: %{y:.1f}B NXID<extra></extra>'),
                row=2, col=1
            )
        
        fig.update_xaxes(title_text="Mainnet Ayı", row=2, col=1)
        fig.update_yaxes(title_text="Staking Ratio (%)", row=1, col=1)
        fig.update_yaxes(title_text="Token Price ($) / Effects", secondary_y=True, row=1, col=1)
        fig.update_yaxes(title_text="Rewards & Staked (Milyar NXID)", row=2, col=1)
        fig.update_yaxes(title_text="APY (%)", secondary_y=True, row=2, col=1)
        
        template_config = self.chart_template.copy()
        template_config.update({
            'title': dict(text='<b>Enhanced Smooth Mainnet Staking Ecosystem</b>', x=0.5,
                        font=dict(size=24, color=NXID_COLORS['primary'])),
            'height': 750,
            'hovermode': 'x unified'
        })
        
        fig.update_layout(**template_config)
        return fig
    
    def _create_presale_basic_chart(self, presale_df: pd.DataFrame) -> go.Figure:
        """Presale temel analiz"""
        fig = make_subplots(
            rows=1, cols=1,
            specs=[[{"secondary_y": True}]],
        )
        
        fig.add_trace(
            go.Bar(x=presale_df['gun'], y=presale_df['gunluk_satilan_token']/1e6,
                   name='Günlük Satış (M Token)', 
                   marker_color=NXID_COLORS['primary'],
                   opacity=0.8,
                   hovertemplate='<b>%{x}. Gün</b><br>Satış: %{y:.2f}M NXID<extra></extra>')
        )
        
        fig.add_trace(
            go.Scatter(x=presale_df['gun'], y=presale_df['fiyat_usdt'],
                      name='Token Fiyatı ($)', 
                      line=dict(color=NXID_COLORS['gold'], width=4),
                      hovertemplate='<b>%{x}. Gün</b><br>Fiyat: $%{y:.6f}<extra></extra>'),
            secondary_y=True
        )
        
        fig.update_xaxes(title_text="Presale Günü")
        fig.update_yaxes(title_text="Günlük Satış (Milyon NXID)", secondary_y=False)
        fig.update_yaxes(title_text="Token Fiyatı ($)", secondary_y=True)
        
        template_config = self.chart_template.copy()
        template_config.update({
            'title': dict(text='<b>Presale Temel Performans</b>', x=0.5, 
                        font=dict(size=24, color=NXID_COLORS['primary'])),
            'height': 500,
            'hovermode': 'x unified'
        })
        
        fig.update_layout(**template_config)
        return fig
    
    def _create_presale_usd_tokens_chart(self, presale_df: pd.DataFrame) -> go.Figure:
        """USD ve Token satış analizi"""
        fig = make_subplots(
            rows=1, cols=1,
            specs=[[{"secondary_y": True}]],
        )
        
        fig.add_trace(
            go.Scatter(x=presale_df['gun'], y=presale_df['kumulatif_toplanan_usdt']/1e6,
                      name='Toplanan Para (M$)', 
                      line=dict(color=NXID_COLORS['success'], width=4),
                      fill='tonexty', fillcolor=f"rgba{hex_to_rgb(NXID_COLORS['success']) + (0.3,)}",
                      hovertemplate='<b>%{x}. Gün</b><br>Toplanan: $%{y:.1f}M<extra></extra>')
        )
        
        fig.add_trace(
            go.Scatter(x=presale_df['gun'], y=presale_df['kumulatif_satilan_token']/1e9,
                      name='Satılan Token (B)', 
                      line=dict(color=NXID_COLORS['primary'], width=4),
                      fill='tonexty', fillcolor=f"rgba{hex_to_rgb(NXID_COLORS['primary']) + (0.3,)}",
                      hovertemplate='<b>%{x}. Gün</b><br>Satılan: %{y:.1f}B NXID<extra></extra>'),
            secondary_y=True
        )
        
        fig.add_trace(
            go.Scatter(x=presale_df['gun'], y=presale_df['satilan_token_yuzdesi'],
                      name='Satılan %', 
                      line=dict(color=NXID_COLORS['gold'], width=3, dash='dot'),
                      hovertemplate='<b>%{x}. Gün</b><br>Satılan: %{y:.1f}%<extra></extra>'),
            secondary_y=True
        )
        
        fig.update_xaxes(title_text="Presale Günü")
        fig.update_yaxes(title_text="Toplanan Para (Milyon $)", secondary_y=False)
        fig.update_yaxes(title_text="Satılan Token (Milyar) / Yüzde (%)", secondary_y=True)
        
        template_config = self.chart_template.copy()
        template_config.update({
            'title': dict(text='<b>Presale USD & Token Satış Analizi</b>', x=0.5, 
                        font=dict(size=24, color=NXID_COLORS['primary'])),
            'height': 500,
            'hovermode': 'x unified'
        })
        
        fig.update_layout(**template_config)
        return fig
    
    def _create_presale_apy_staking_analysis(self, presale_df: pd.DataFrame) -> go.Figure:
        """APY + Staking analizi - Enhanced """
        fig = make_subplots(
            rows=3, cols=1,
            subplot_titles=['Dynamic APY Performance', 
                           'Staking Pool Status',
                           'Staked Token Analysis'],
            specs=[[{"secondary_y": False}], [{"secondary_y": True}], [{"secondary_y": False}]],
            vertical_spacing=0.12
        )
        
        # Dinamik APY
        fig.add_trace(
            go.Scatter(x=presale_df['gun'], y=presale_df['guncel_apy'],
                      name='Dynamic APY (%)', 
                      line=dict(color=NXID_COLORS['gold'], width=4),
                      fill='tonexty', fillcolor=f"rgba{hex_to_rgb(NXID_COLORS['gold']) + (0.3,)}",
                      hovertemplate='<b>Day %{x}</b><br>Dynamic APY: %{y:.1f}%<extra></extra>'),
            row=1, col=1
        )
        
        min_apy_line = [self.config.minimum_staking_apy] * len(presale_df)
        fig.add_trace(
            go.Scatter(x=presale_df['gun'], y=min_apy_line,
                      mode='lines', name=f'Minimum APY: {self.config.minimum_staking_apy}%',
                      line=dict(color=NXID_COLORS['danger'], width=2, dash='dash'),
                      hovertemplate=f'<b>Minimum APY</b><br>{self.config.minimum_staking_apy:.0f}%<extra></extra>'),
            row=1, col=1
        )
        
        # Staking pool durumu
        fig.add_trace(
            go.Scatter(x=presale_df['gun'], y=presale_df['kalan_odul_havuzu']/1e9,
                      name='Remaining Pool (B NXID)', 
                      line=dict(color=NXID_COLORS['teal'], width=4),
                      fill='tonexty', fillcolor=f"rgba{hex_to_rgb(NXID_COLORS['teal']) + (0.3,)}",
                      hovertemplate='<b>Day %{x}</b><br>Remaining Pool: %{y:.1f}B NXID<extra></extra>'),
            row=2, col=1
        )
        
        fig.add_trace(
            go.Scatter(x=presale_df['gun'], y=presale_df['havuz_tukenme_yuzdesi'],
                      name='Pool Depletion %', 
                      line=dict(color=NXID_COLORS['danger'], width=3),
                      hovertemplate='<b>Day %{x}</b><br>Depletion: %{y:.1f}%<extra></extra>'),
            row=2, col=1, secondary_y=True
        )
        
        # Stake edilmiş tokenlar
        if 'ana_para_tokens' in presale_df.columns:
            fig.add_trace(
                go.Scatter(x=presale_df['gun'], y=presale_df['ana_para_tokens']/1e9,
                          name='Staked Tokens (B)', 
                          line=dict(color=NXID_COLORS['primary'], width=4),
                          fill='tonexty', fillcolor=f"rgba{hex_to_rgb(NXID_COLORS['primary']) + (0.3,)}",
                          hovertemplate='<b>Day %{x}</b><br>Staked: %{y:.1f}B NXID<extra></extra>'),
                row=3, col=1
            )
        
        fig.add_trace(
            go.Scatter(x=presale_df['gun'], y=presale_df['toplam_dagitilan_odul']/1e9,
                      name='Distributed Rewards (B)', 
                      line=dict(color=NXID_COLORS['success'], width=3),
                      hovertemplate='<b>Day %{x}</b><br>Distributed: %{y:.1f}B NXID<extra></extra>'),
            row=3, col=1
        )
        
        fig.update_xaxes(title_text="Presale Day", row=3, col=1)
        fig.update_yaxes(title_text="APY (%)", row=1, col=1)
        fig.update_yaxes(title_text="Remaining Pool (Billion NXID)", row=2, col=1)
        fig.update_yaxes(title_text="Depletion (%)", secondary_y=True, row=2, col=1)
        fig.update_yaxes(title_text="Token Amount (Billion NXID)", row=3, col=1)
        
        template_config = self.chart_template.copy()
        template_config.update({
            'title': dict(text='<b>Simple Interest + Dynamic APY System </b>', x=0.5,
                        font=dict(size=24, color=NXID_COLORS['primary'])),
            'height': 800,
            'hovermode': 'x unified'
        })
        
        fig.update_layout(**template_config)
        return fig
    
    def _create_weekly_daily_interest_tracking(self, weekly_df: pd.DataFrame, presale_df: pd.DataFrame) -> go.Figure:
        """Haftalık tracking - Enhanced """
        
        # Haftalık tracking logic
        daily_tracking_data = []
        
        for _, week_row in weekly_df.iterrows():
            week = int(week_row['hafta'])
            week_start_day = (week - 1) * 7 + 1
            investment_amount = week_row['yatirim_miktari_usdt']
            week_price = week_row['hafta_fiyati']
            week_apy = week_row['hafta_apy']
            principal_tokens = investment_amount / week_price
            
            weekly_daily_data = {
                'week': week,
                'week_apy': week_apy,
                'principal': principal_tokens,
                'daily_interest': [],
                'cumulative_interest': [],
                'total_balance': [],
                'interest_percentage': [],
                'days': []
            }
            
            cumulative_interest = 0
            
            for day_offset in range(week_start_day, len(presale_df) + 1):
                if day_offset <= len(presale_df):
                    day_apy = presale_df.iloc[day_offset-1]['guncel_apy']
                    daily_rate = day_apy / 100 / 365
                    daily_interest = principal_tokens * daily_rate
                    cumulative_interest += daily_interest
                    total_balance = principal_tokens + cumulative_interest
                    interest_percentage = (cumulative_interest / principal_tokens * 100) if principal_tokens > 0 else 0
                    
                    weekly_daily_data['daily_interest'].append(daily_interest)
                    weekly_daily_data['cumulative_interest'].append(cumulative_interest)
                    weekly_daily_data['total_balance'].append(total_balance)
                    weekly_daily_data['interest_percentage'].append(interest_percentage)
                    weekly_daily_data['days'].append(day_offset)
            
            daily_tracking_data.append(weekly_daily_data)
        
        # Tüm haftaları göster
        weeks_to_show = daily_tracking_data
        title_suffix = f" - All {len(daily_tracking_data)} Weeks"
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=['Daily Interest Gain', 'Cumulative Interest Gain', 
                        'Total Balance', 'Interest Gain Percentage'],
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                [{"secondary_y": False}, {"secondary_y": False}]],
            vertical_spacing=0.15,
            horizontal_spacing=0.1
        )
        
        week_colors = [
            NXID_COLORS['primary'], NXID_COLORS['success'], NXID_COLORS['gold'], 
            NXID_COLORS['purple'], NXID_COLORS['teal'], NXID_COLORS['orange'],
            NXID_COLORS['indigo'], NXID_COLORS['pink'], NXID_COLORS['accent'],
            NXID_COLORS['burn'], NXID_COLORS['tax'], '#FF6B9D', '#4ECDC4', '#45B7D1',
            '#96CEB4', '#FFEAA7', '#DDA0DD', '#98D8C8', '#F7DC6F', '#BB8FCE',
            '#85C1E9', '#F8C471', '#82E0AA', '#F1948A', '#85929E', '#D7DBDD',
            '#FF9FF3', '#54A0FF', '#5F27CD', '#00D2D3', '#FF9F43', '#EE5A24'
        ]
        
        for i, week_data in enumerate(weeks_to_show):
            week = week_data['week']
            week_apy = week_data['week_apy']
            color_idx = (week - 1) % len(week_colors)
            color = week_colors[color_idx]
            
            legend_group = f"Week_{week}"
            
            # Charts ekleme - Her hafta için legend göster
            fig.add_trace(go.Scatter(
                x=week_data['days'],
                y=week_data['daily_interest'],
                mode='lines',
                name=f'Week {week} (APY: {week_apy:.1f}%)',
                line=dict(color=color, width=2),
                hovertemplate=f'<b>Week {week} (APY: {week_apy:.1f}%)</b><br>Day: %{{x}}<br>Daily Interest: %{{y:,.0f}} NXID<extra></extra>',
                showlegend=True,  # Her hafta için legend göster
                legendgroup=legend_group
            ), row=1, col=1)
            
            fig.add_trace(go.Scatter(
                x=week_data['days'],
                y=week_data['cumulative_interest'],
                mode='lines',
                name=f'Week {week} Cumulative',
                line=dict(color=color, width=2),
                hovertemplate=f'<b>Week {week} (APY: {week_apy:.1f}%)</b><br>Day: %{{x}}<br>Total Interest: %{{y:,.0f}} NXID<extra></extra>',
                showlegend=False,  # Sadece ilk trace'de legend
                legendgroup=legend_group
            ), row=1, col=2)
            
            fig.add_trace(go.Scatter(
                x=week_data['days'],
                y=week_data['total_balance'],
                mode='lines',
                name=f'Week {week} Balance',
                line=dict(color=color, width=2),
                hovertemplate=f'<b>Week {week} (APY: {week_apy:.1f}%)</b><br>Day: %{{x}}<br>Total: %{{y:,.0f}} NXID<extra></extra>',
                showlegend=False,
                legendgroup=legend_group
            ), row=2, col=1)
            
            fig.add_trace(go.Scatter(
                x=week_data['days'],
                y=week_data['interest_percentage'],
                mode='lines',
                name=f'Week {week} %',
                line=dict(color=color, width=2),
                hovertemplate=f'<b>Week {week} (APY: {week_apy:.1f}%)</b><br>Day: %{{x}}<br>Interest: %{{y:.1f}}%<extra></extra>',
                showlegend=False,
                legendgroup=legend_group
            ), row=2, col=2)
        
        fig.update_xaxes(title_text="Presale Day", row=2, col=1)
        fig.update_xaxes(title_text="Presale Day", row=2, col=2)
        fig.update_yaxes(title_text="Daily Interest (NXID)", row=1, col=1)
        fig.update_yaxes(title_text="Cumulative Interest (NXID)", row=1, col=2)
        fig.update_yaxes(title_text="Total Balance (NXID)", row=2, col=1)
        fig.update_yaxes(title_text="Interest Gain (%)", row=2, col=2)
        
        template_config = self.chart_template.copy()
        
        # Legend konfigürasyonu - scroll edilebilir
        legend_config = dict(
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="left",
            x=1.02,
            font=dict(color=NXID_COLORS['light'], size=10),
            bgcolor=f"rgba{hex_to_rgb(NXID_COLORS['dark']) + (0.8,)}",
            bordercolor=NXID_COLORS['primary'],
            borderwidth=1,
            itemsizing="constant",
            itemwidth=30
        )
        
        template_config.update({
            'title': dict(
                text=f'<b>Weekly Simple Interest Tracking (${self.config.weekly_investment_amount} Fixed Investment){title_suffix}</b>',
                x=0.5, font=dict(size=24, color=NXID_COLORS['primary'])
            ),
            'height': 700,
            'hovermode': 'x unified',
            'legend': legend_config,
            'showlegend': True
        })
        
        fig.update_layout(**template_config)
        
        return fig
    
    def _create_mainnet_tax_burn_chart(self, mainnet_df: pd.DataFrame) -> go.Figure:
        """Tax & burn chart - Enhanced """
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=['Tax Collection and Distribution', 
                           'Token Burn Analysis'],
            specs=[[{"secondary_y": True}], [{"secondary_y": True}]],
            vertical_spacing=0.15
        )
        
        if 'kumulatif_tax_toplam' in mainnet_df.columns:
            fig.add_trace(
                go.Scatter(x=mainnet_df['ay'], y=mainnet_df['kumulatif_tax_toplam']/1e6,
                          name='Collected Tax (M)', 
                          line=dict(color=NXID_COLORS['tax'], width=5),
                          fill='tonexty', fillcolor=f"rgba{hex_to_rgb(NXID_COLORS['tax']) + (0.2,)}",
                          hovertemplate='<b>Month %{x:.1f}</b><br>Tax: %{y:.1f}M NXID<extra></extra>'),
                row=1, col=1
            )
            
            fig.add_trace(
                go.Scatter(x=mainnet_df['ay'], y=mainnet_df['kumulatif_tax_staking']/1e6,
                          name='Tax→Staking (M)', 
                          line=dict(color=NXID_COLORS['success'], width=4),
                          hovertemplate='<b>Month %{x:.1f}</b><br>To Staking: %{y:.1f}M NXID<extra></extra>'),
                row=1, col=1
            )
        
        fig.add_trace(
            go.Scatter(x=mainnet_df['ay'], y=mainnet_df['kumulatif_rutin_burned']/1e6,
                      name='Routine Burn (M)', 
                      line=dict(color=NXID_COLORS['burn'], width=5),
                      fill='tonexty', fillcolor=f"rgba{hex_to_rgb(NXID_COLORS['burn']) + (0.2,)}",
                      hovertemplate='<b>Month %{x:.1f}</b><br>Routine Burn: %{y:.1f}M NXID<extra></extra>'),
            row=2, col=1
        )
        
        if 'kumulatif_tax_burned' in mainnet_df.columns:
            fig.add_trace(
                go.Scatter(x=mainnet_df['ay'], y=mainnet_df['kumulatif_tax_burned']/1e6,
                          name='Tax Burn (M)', 
                          line=dict(color=NXID_COLORS['orange'], width=4),
                          hovertemplate='<b>Month %{x:.1f}</b><br>Tax Burn: %{y:.1f}M NXID<extra></extra>'),
                row=2, col=1
            )
        
        fig.add_trace(
            go.Scatter(x=mainnet_df['ay'], y=mainnet_df['burn_orani_yuzdesi'],
                      name='Total Burn %', 
                      line=dict(color=NXID_COLORS['danger'], width=4),
                      hovertemplate='<b>Month %{x:.1f}</b><br>Burned: %{y:.2f}%<extra></extra>'),
            row=2, col=1, secondary_y=True
        )
        
        fig.update_xaxes(title_text="Mainnet Month", row=2, col=1)
        fig.update_yaxes(title_text="Tax Amount (Million NXID)", row=1, col=1)
        fig.update_yaxes(title_text="Burned Amount (Million NXID)", row=2, col=1)
        fig.update_yaxes(title_text="Burn Percentage (%)", secondary_y=True, row=2, col=1)
        
        template_config = self.chart_template.copy()
        template_config.update({
            'title': dict(text='<b>Mainnet Tax & Burn Analysis </b>', x=0.5,
                        font=dict(size=24, color=NXID_COLORS['primary'])),
            'height': 700,
            'hovermode': 'x unified'
        })
        
        fig.update_layout(**template_config)
        return fig
    
    
    def _create_mcap_evolution_analysis_chart(self, mainnet_df: pd.DataFrame, scenario: str) -> go.Figure:
        """YENİ: Market Cap Evolution Analysis Chart"""
        scenario_color = NXID_COLORS['danger'] if scenario == 'bear' else (
            NXID_COLORS['success'] if scenario == 'bull' else NXID_COLORS['primary']
        )
        
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=[f'Market Cap Evrim Analizi - {scenario.upper()}', 
                        'Market Cap Büyüme Oranları ve Hedefler'],
            specs=[[{"secondary_y": True}], [{"secondary_y": True}]],
            vertical_spacing=0.15
        )
        
        # === 1. MARKET CAP EVRİMİ ===
        fig.add_trace(
            go.Scatter(x=mainnet_df['ay'], y=mainnet_df['mcap_usdt']/1e6,
                    name=f'Market Cap - {scenario.upper()} (M$)', 
                    line=dict(color=scenario_color, width=5),
                    fill='tonexty', fillcolor=f"rgba{hex_to_rgb(scenario_color) + (0.2,)}",
                    hovertemplate=f'<b>%{{x:.1f}}. Ay</b><br>McAp: $%{{y:.1f}}M<br>Senaryo: {scenario.upper()}<extra></extra>'),
            row=1, col=1
        )
        
        # Başlangıç McAp çizgisi
        starting_mcap_line = [self.config.starting_mcap_usdt / 1e6] * len(mainnet_df)
        fig.add_trace(
            go.Scatter(x=mainnet_df['ay'], y=starting_mcap_line,
                    mode='lines', name=f'Başlangıç McAp: ${self.config.starting_mcap_usdt/1e6:.1f}M',
                    line=dict(color=NXID_COLORS['accent'], width=3, dash='dash'),
                    hovertemplate=f'<b>Başlangıç McAp</b><br>${self.config.starting_mcap_usdt/1e6:.1f}M<extra></extra>'),
            row=1, col=1
        )
        
        # Hedef McAp çizgisi
        if 'maturity_target_mcap' in mainnet_df.columns:
            target_mcap = mainnet_df['maturity_target_mcap'].iloc[0] / 1e6
            target_line = [target_mcap] * len(mainnet_df)
            fig.add_trace(
                go.Scatter(x=mainnet_df['ay'], y=target_line,
                        mode='lines', name=f'Hedef McAp: ${target_mcap:.0f}M',
                        line=dict(color=NXID_COLORS['gold'], width=4, dash='dot'),
                        hovertemplate=f'<b>Hedef McAp</b><br>${target_mcap:.0f}M<extra></extra>'),
                row=1, col=1
            )
        
        # McAp Büyüme Oranı
        if len(mainnet_df) > 30:
            mcap_growth_rate = ((mainnet_df['mcap_usdt'] / mainnet_df['mcap_usdt'].shift(30).fillna(mainnet_df['mcap_usdt'].iloc[0])) - 1) * 100
            fig.add_trace(
                go.Scatter(x=mainnet_df['ay'], y=mcap_growth_rate,
                        name='Aylık Büyüme Oranı %', 
                        line=dict(color=NXID_COLORS['orange'], width=3),
                        hovertemplate='<b>%{x:.1f}. Ay</b><br>Büyüme: %{y:.1f}%<extra></extra>'),
                row=1, col=1, secondary_y=True
            )
        
        # === 2. BÜYÜME ANALİZİ ===
        # Kümülatif büyüme
        cumulative_growth = ((mainnet_df['mcap_usdt'] / mainnet_df['mcap_usdt'].iloc[0]) - 1) * 100
        fig.add_trace(
            go.Scatter(x=mainnet_df['ay'], y=cumulative_growth,
                    name='Kümülatif Büyüme %', 
                    line=dict(color=NXID_COLORS['success'], width=4),
                    fill='tonexty', fillcolor=f"rgba{hex_to_rgb(NXID_COLORS['success']) + (0.3,)}",
                    hovertemplate='<b>%{x:.1f}. Ay</b><br>Kümülatif: %{y:.1f}%<extra></extra>'),
            row=2, col=1
        )
        
        # Hedef ilerleme
        if 'maturity_progress_pct' in mainnet_df.columns:
            fig.add_trace(
                go.Scatter(x=mainnet_df['ay'], y=mainnet_df['maturity_progress_pct'],
                        name='Hedef İlerleme %', 
                        line=dict(color=NXID_COLORS['purple'], width=3),
                        hovertemplate='<b>%{x:.1f}. Ay</b><br>Hedef: %{y:.1f}%<extra></extra>'),
                row=2, col=1, secondary_y=True
            )
        
        # Hedef başarı çizgisi
        fig.add_hline(
            y=100,
            line_dash="solid",
            line_color=NXID_COLORS['gold'],
            line_width=3,
            annotation_text="Hedef Başarı (100%)",
            row=2, col=1, secondary_y=True
        )
        
        fig.update_xaxes(title_text="Mainnet Ayı", row=2, col=1)
        fig.update_yaxes(title_text="Market Cap (Milyon $)", row=1, col=1)
        fig.update_yaxes(title_text="Büyüme Oranı (%)", secondary_y=True, row=1, col=1)
        fig.update_yaxes(title_text="Kümülatif Büyüme (%)", row=2, col=1)
        fig.update_yaxes(title_text="Hedef İlerleme (%)", secondary_y=True, row=2, col=1)
        
        template_config = self.chart_template.copy()
        template_config.update({
            'title': dict(text=f'<b>Market Cap Evrim Analizi - {scenario.upper()} Senaryo</b>', x=0.5,
                        font=dict(size=26, color=scenario_color)),
            'height': 750,
            'hovermode': 'x unified'
        })
        
        fig.update_layout(**template_config)
        return fig
    def _create_total_supply_mcap_analysis_chart(self, mainnet_df: pd.DataFrame, scenario: str) -> go.Figure:
        """YENİ: Total Supply vs Market Cap Analysis Chart"""
        scenario_color = NXID_COLORS['danger'] if scenario == 'bear' else (
            NXID_COLORS['success'] if scenario == 'bull' else NXID_COLORS['primary']
        )
        
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=['Toplam Arz vs Market Cap Analizi', 
                        'Token Fiyatı ve Arz Etkileşimi'],
            specs=[[{"secondary_y": True}], [{"secondary_y": True}]],
            vertical_spacing=0.15
        )
        
        # === 1. SUPPLY VS MCAP ===
        # Market Cap
        fig.add_trace(
            go.Scatter(x=mainnet_df['ay'], y=mainnet_df['mcap_usdt']/1e6,
                    name=f'Market Cap (M$) - {scenario.upper()}', 
                    line=dict(color=scenario_color, width=5),
                    fill='tonexty', fillcolor=f"rgba{hex_to_rgb(scenario_color) + (0.2,)}",
                    hovertemplate=f'<b>%{{x:.1f}}. Ay</b><br>McAp: $%{{y:.1f}}M<extra></extra>'),
            row=1, col=1
        )
        
        # Etkili Toplam Arz
        effective_total_supply = mainnet_df['etkili_toplam_arz'] / 1e9
        fig.add_trace(
            go.Scatter(x=mainnet_df['ay'], y=effective_total_supply,
                    name='Etkili Toplam Arz (B)', 
                    line=dict(color=NXID_COLORS['purple'], width=4),
                    hovertemplate='<b>%{x:.1f}. Ay</b><br>Etkili Arz: %{y:.1f}B NXID<extra></extra>'),
            row=1, col=1, secondary_y=True
        )
        
        # Başlangıç toplam arz çizgisi
        initial_supply_line = [self.config.total_supply / 1e9] * len(mainnet_df)
        fig.add_trace(
            go.Scatter(x=mainnet_df['ay'], y=initial_supply_line,
                    mode='lines', name=f'Başlangıç Toplam Arz: {self.config.total_supply/1e9:.0f}B',
                    line=dict(color=NXID_COLORS['accent'], width=2, dash='dash'),
                    hovertemplate=f'<b>Başlangıç Arz</b><br>{self.config.total_supply/1e9:.0f}B NXID<extra></extra>'),
            row=1, col=1, secondary_y=True
        )
        
        # === 2. TOKEN FİYAT ANALİZİ ===
        # Token fiyatı
        fig.add_trace(
            go.Scatter(x=mainnet_df['ay'], y=mainnet_df['token_fiyati'],
                    name='Token Fiyatı ($)', 
                    line=dict(color=NXID_COLORS['gold'], width=5),
                    fill='tonexty', fillcolor=f"rgba{hex_to_rgb(NXID_COLORS['gold']) + (0.2,)}",
                    hovertemplate='<b>%{x:.1f}. Ay</b><br>Fiyat: $%{y:.6f}<extra></extra>'),
            row=2, col=1
        )
        
        # Etkili dolaşımdaki arz
        fig.add_trace(
            go.Scatter(x=mainnet_df['ay'], y=mainnet_df['effective_circulating_supply']/1e9,
                    name='Etkili Dolaşım Arzı (B)', 
                    line=dict(color=NXID_COLORS['teal'], width=4),
                    hovertemplate='<b>%{x:.1f}. Ay</b><br>Etkili Dolaşım: %{y:.1f}B NXID<extra></extra>'),
            row=2, col=1, secondary_y=True
        )
        
        # Gross dolaşımdaki arz
        fig.add_trace(
            go.Scatter(x=mainnet_df['ay'], y=mainnet_df['gross_circulating_supply']/1e9,
                    name='Brüt Dolaşım Arzı (B)', 
                    line=dict(color=NXID_COLORS['primary'], width=3, dash='dot'),
                    hovertemplate='<b>%{x:.1f}. Ay</b><br>Brüt Dolaşım: %{y:.1f}B NXID<extra></extra>'),
            row=2, col=1, secondary_y=True
        )
        
        fig.update_xaxes(title_text="Mainnet Ayı", row=2, col=1)
        fig.update_yaxes(title_text="Market Cap (Milyon $)", row=1, col=1)
        fig.update_yaxes(title_text="Toplam Arz (Milyar NXID)", secondary_y=True, row=1, col=1)
        fig.update_yaxes(title_text="Token Fiyatı ($)", row=2, col=1)
        fig.update_yaxes(title_text="Dolaşım Arzı (Milyar NXID)", secondary_y=True, row=2, col=1)
        
        template_config = self.chart_template.copy()
        template_config.update({
            'title': dict(text=f'<b>Toplam Arz vs Market Cap Analizi - {scenario.upper()}</b>', x=0.5,
                        font=dict(size=26, color=scenario_color)),
            'height': 750,
            'hovermode': 'x unified'
        })
        
        fig.update_layout(**template_config)
        return fig