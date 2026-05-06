#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import io
import base64
from pathlib import Path

# Grafikleri saklamak için liste
chart_images = []

try:
    # Veriyi yükle
    df = pd.read_csv("Cleaned_Prisoners_Dataset.csv", sep=";")
    
    # Sütun isimlerini temizle
    df.columns = [col.strip() for col in df.columns]
    
    # Tüm sayısal sütunları numeric'e çevir
    for col in df.columns[2:]:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # NaN değerleri 0 ile doldur
    df = df.fillna(0)
    
    # Seaborn ayarları
    sns.set(style="whitegrid")
    
    print("📊 Grafikler oluşturuluyor...")
    
    # ------- GRAFIK 1: Yıllara Göre Toplam Mahkum Sayısı -------
    fig1, ax1 = plt.subplots(figsize=(12, 6))
    numeric_cols = df.iloc[:, 2:]
    yearly_total = df.groupby('Year')[numeric_cols.columns].sum().sum(axis=1)
    yearly_total.plot(kind='line', marker='o', linewidth=2.5, markersize=8, ax=ax1, color='#016480')
    ax1.set_title('Yıllara Göre Toplam Mahkum Sayısı', fontsize=16, fontweight='bold', color='#016480')
    ax1.set_xlabel('Yıl', fontsize=12)
    ax1.set_ylabel('Mahkum Sayısı', fontsize=12)
    ax1.grid(True, alpha=0.3)
    plt.tight_layout()
    
    # ------- GRAFIK 2: Suç Türlerine Göre Dağılım -------
    fig2, ax2 = plt.subplots(figsize=(12, 6))
    numeric_cols = df.iloc[:, 2:]
    crime_totals = df.groupby('Crime Type')[numeric_cols.columns].sum().sum(axis=1).sort_values(ascending=False).head(10)
    crime_totals.plot(kind='barh', ax=ax2, color='#D4A574')
    ax2.set_title('En Sık İşlenen 10 Suç Türü', fontsize=16, fontweight='bold', color='#016480')
    ax2.set_xlabel('Toplam Mahkum Sayısı', fontsize=12)
    ax2.grid(True, alpha=0.3, axis='x')
    plt.tight_layout()
    
    # ------- GRAFIK 3: Cinsiyet Dağılımı -------
    fig3, ax3 = plt.subplots(figsize=(10, 6))
    male_cols = [col for col in df.columns if 'Male' in col or 'male' in col]
    female_cols = [col for col in df.columns if 'Female' in col or 'female' in col]
    
    male_total = df[male_cols].sum().sum() if male_cols else 0
    female_total = df[female_cols].sum().sum() if female_cols else 0
    
    if male_total > 0 or female_total > 0:
        sizes = [male_total, female_total]
        labels = ['Erkek', 'Kadın']
        colors = ['#016480', '#D4A574']
        ax3.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90)
        ax3.set_title('Cinsiyete Göre Mahkum Dağılımı', fontsize=16, fontweight='bold', color='#016480')
    plt.tight_layout()
    
    # ------- GRAFIK 4: Yaş Gruplarına Göre Dağılım -------
    fig4, ax4 = plt.subplots(figsize=(12, 6))
    age_cols = [col for col in df.columns if any(age in col for age in ['12-14', '15-17', '18-24', '25-34', '35-44', '45-54', '55-64', '65'])]
    
    if age_cols:
        age_totals = df[age_cols].sum()
        age_totals = age_totals[age_totals > 0].sort_values(ascending=False)
        age_totals.plot(kind='bar', ax=ax4, color='#667eea')
        ax4.set_title('Yaş Gruplarına Göre Mahkum Dağılımı', fontsize=16, fontweight='bold', color='#016480')
        ax4.set_xlabel('Yaş Grupları', fontsize=12)
        ax4.set_ylabel('Mahkum Sayısı', fontsize=12)
        ax4.tick_params(axis='x', rotation=45)
        ax4.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    
    # ------- GRAFIK 5: Yıllar İçinde Suç Türü Değişimi -------
    fig5, ax5 = plt.subplots(figsize=(14, 7))
    numeric_cols = df.iloc[:, 2:]
    top_crimes = df.groupby('Crime Type')[numeric_cols.columns].sum().sum(axis=1).sort_values(ascending=False).head(5).index
    
    if len(top_crimes) > 0:
        for crime in top_crimes:
            crime_data = df[df['Crime Type'] == crime].groupby('Year')[numeric_cols.columns].sum().sum(axis=1)
            ax5.plot(crime_data.index, crime_data.values, marker='o', label=crime, linewidth=2)
        
        ax5.set_title('Yıllar İçinde En Sık 5 Suçun Değişimi', fontsize=16, fontweight='bold', color='#016480')
        ax5.set_xlabel('Yıl', fontsize=12)
        ax5.set_ylabel('Mahkum Sayısı', fontsize=12)
        ax5.legend(loc='best')
        ax5.grid(True, alpha=0.3)
    plt.tight_layout()
    
    print("✅ 5 grafik başarıyla oluşturuldu!")
    
    # Grafikleri topla
    figures = [fig1, fig2, fig3, fig4, fig5]
    chart_descriptions = [
        'Yıllara Göre Toplam Mahkum Sayısı',
        'En Sık İşlenen 10 Suç Türü',
        'Cinsiyete Göre Mahkum Dağılımı',
        'Yaş Gruplarına Göre Mahkum Dağılımı',
        'Yıllar İçinde En Sık 5 Suçun Değişimi'
    ]
    
    # Grafikleri PNG olarak kaydet
    for i, (fig, desc) in enumerate(zip(figures, chart_descriptions)):
        buf = io.BytesIO()
        fig.savefig(buf, format='png', bbox_inches='tight', dpi=100, facecolor='white')
        buf.seek(0)
        
        img_base64 = base64.b64encode(buf.read()).decode()
        chart_images.append({
            'title': desc,
            'image': img_base64
        })
        buf.close()
        plt.close(fig)
    
    # HTML'i oku ve grafiklerle güncelle
    with open('index.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Grafikleri HTML formatında hazırla
    charts_html = ""
    chart_icons = ['fa-chart-line', 'fa-bar-chart', 'fa-pie-chart', 'fa-users', 'fa-trending-up']
    
    for i, chart in enumerate(chart_images, 1):
        icon = chart_icons[i-1] if i-1 < len(chart_icons) else 'fa-chart-bar'
        charts_html += f"""            <div class="chart-section">
                <div class="chart-header">
                    <i class="fas {icon}"></i>
                    <h2 class="chart-title">Grafik {i}: {chart['title']}</h2>
                </div>
                <div class="chart-container">
                    <img src="data:image/png;base64,{chart['image']}" alt="{chart['title']}" loading="lazy">
                </div>
            </div>
"""
    
    # charts-container'a grafikleri ekle
    html_content = html_content.replace(
        '<div class="charts-grid" id="charts-container"></div>',
        f'<div class="charts-grid" id="charts-container">\n{charts_html}        </div>'
    )
    
    # HTML dosyasını kaydet
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("✅ Grafikler başarıyla index.html dosyasına kaydedildi!")
    print(f"📁 Dosya boyutu: {len(html_content) / 1024:.2f} KB")
    
except Exception as e:
    print(f"❌ Hata oluştu: {e}")
    import traceback
    traceback.print_exc()
