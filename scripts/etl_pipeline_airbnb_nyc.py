"""
ETL Pipeline — NYC Airbnb Dataset (2019)
Mirrors the Swiggy ETL structure for SectionA_Group18_AirbnbNYCAnalysis
Run: python etl_pipeline_airbnb_nyc.py
"""

import matplotlib
matplotlib.use('Agg')

from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import pandas as pd
import seaborn as sns
from scipy import stats


# ── Paths ────────────────────────────────────────────────────────────────────

PROJECT_ROOT   = Path(__file__).resolve().parent
RAW_PATH       = PROJECT_ROOT / 'data/raw/AB_NYC_2019.csv'
CLEANED_PATH   = PROJECT_ROOT / 'data/processed/airbnb_cleaned.csv'
FINAL_PATH     = PROJECT_ROOT / 'data/processed/airbnb_final.csv'
FIGURES_PATH   = PROJECT_ROOT / 'reports/figures'
STATS_PATH     = PROJECT_ROOT / 'reports/stats'

for p in [FIGURES_PATH, STATS_PATH, PROJECT_ROOT / 'data/processed', PROJECT_ROOT / 'data/raw']:
    p.mkdir(parents=True, exist_ok=True)

ALPHA    = 0.05
FIG_SIZE = (12, 5)
PALETTE  = ['#FF5A5F', '#FF7478', '#FF9396', '#FFB5B7', '#FFD6D7']
sns.set_theme(style='whitegrid')
plt.rcParams['font.family'] = 'DejaVu Sans'


# ── Logger ───────────────────────────────────────────────────────────────────

def log(message: str) -> None:
    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f'[{ts}] {message}')


# ── Step 1 — Extraction ──────────────────────────────────────────────────────

def step_extract(source_path: str = None) -> pd.DataFrame:
    """
    Load raw Airbnb CSV.
    Pass source_path to override RAW_PATH (useful when running from a notebook
    or providing the pre-processed file directly).
    """
    path = Path(source_path) if source_path else RAW_PATH
    df = pd.read_csv(path, parse_dates=['last_review'])
    log(f'✓ Step 1 — Extraction complete   ({len(df):,} rows loaded from {path.name})')
    return df


# ── Step 2 — Cleaning ────────────────────────────────────────────────────────

def step_clean(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the raw dataframe:
      - Fill missing host_name / name with 'Unknown'
      - Fill missing reviews_per_month (no-review listings) with 0
      - Drop rows still containing nulls
      - Remove zero-price listings
      - Flag price outliers via IQR (but keep them in the data; drop only
        zero-price entries)
      - Compute KPI columns: demand_score, value_score
    """
    initial_rows = len(df)

    # Impute known-safe nulls
    df['name']              = df['name'].fillna('Unknown')
    df['host_name']         = df['host_name'].fillna('Unknown')
    df['reviews_per_month'] = df['reviews_per_month'].fillna(0)

    # Drop remaining nulls
    df = df.dropna()

    # Remove zero or negative prices
    df = df[df['price'] > 0]

    # Remove duplicates
    df = df.drop_duplicates()

    # IQR-based outlier flag for price
    Q1  = df['price'].quantile(0.25)
    Q3  = df['price'].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    df['is_price_outlier'] = ~df['price'].between(lower, upper)

    # ── KPI Engineering ──────────────────────────────────────────────────────
    # Demand Score: reviews / availability (avoid div-by-zero)
    df['demand_score'] = df.apply(
        lambda r: r['number_of_reviews'] / r['availability_365']
        if r['availability_365'] > 0 else 0,
        axis=1
    ).round(4)

    # Value Score: reviews / price
    df['value_score'] = (df['number_of_reviews'] / df['price']).round(4)

    # Price per person (already present in processed file, recalculate for raw)
    if 'price_per_person' not in df.columns:
        df['price_per_person'] = (df['price'] / 2).round(2)   # assume 2-person default

    # Occupancy Rate proxy: (365 - availability_365) / 365
    df['occupancy_rate'] = ((365 - df['availability_365']) / 365).round(4)

    # Price category buckets matching dashboard labels
    df['price_category'] = pd.cut(
        df['price'],
        bins=[0, 100, 300, float('inf')],
        labels=['Budget', 'Mid-Range', 'Luxury'],
        right=False
    )

    df.to_csv(CLEANED_PATH, index=False)
    removed = initial_rows - len(df)
    log(f'✓ Step 2 — Cleaning complete     ({len(df):,} rows remaining; {removed:,} removed)')
    return df


# ── Step 3 — EDA ─────────────────────────────────────────────────────────────

def step_eda(df: pd.DataFrame) -> None:
    """Generate 10 exploratory plots saved to reports/figures/."""

    df_no_outlier = df[~df['is_price_outlier']]
    BOROUGH_ORDER = ['Manhattan', 'Brooklyn', 'Queens', 'Bronx', 'Staten Island']

    # 01 Price Distribution (outliers excluded)
    fig, ax = plt.subplots(figsize=FIG_SIZE)
    sns.histplot(df_no_outlier['price'], bins=50, kde=True, color=PALETTE[0], ax=ax)
    ax.set_title('Price Distribution of Airbnb Listings (Outliers Excluded)')
    ax.set_xlabel('Price (USD)')
    ax.set_ylabel('Count')
    plt.tight_layout()
    fig.savefig(FIGURES_PATH / '01_price_distribution.png', dpi=150)
    plt.close(fig)

    # 02 Room Type Distribution (pie)
    rt_counts = df['room_type'].value_counts()
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.pie(rt_counts.values, labels=rt_counts.index, autopct='%1.1f%%',
           colors=PALETTE[:len(rt_counts)], startangle=140)
    ax.set_title('Room Type Distribution')
    plt.tight_layout()
    fig.savefig(FIGURES_PATH / '02_room_type_distribution.png', dpi=150)
    plt.close(fig)

    # 03 Listings by Neighbourhood Group
    ng_counts = df['neighbourhood_group'].value_counts()
    fig, ax = plt.subplots(figsize=FIG_SIZE)
    sns.barplot(x=ng_counts.index, y=ng_counts.values, palette=PALETTE, ax=ax)
    ax.set_title('Listing Count by Borough')
    ax.set_xlabel('Borough')
    ax.set_ylabel('Count')
    plt.tight_layout()
    fig.savefig(FIGURES_PATH / '03_listings_by_borough.png', dpi=150)
    plt.close(fig)

    # 04 Average Price by Borough
    avg_price = df.groupby('neighbourhood_group')['price'].mean().reindex(BOROUGH_ORDER)
    fig, ax = plt.subplots(figsize=FIG_SIZE)
    sns.barplot(x=avg_price.index, y=avg_price.values, palette=PALETTE, ax=ax)
    ax.set_title('Average Price by Borough')
    ax.set_xlabel('Borough')
    ax.set_ylabel('Avg Price (USD)')
    plt.tight_layout()
    fig.savefig(FIGURES_PATH / '04_avg_price_by_borough.png', dpi=150)
    plt.close(fig)

    # 05 Average Price by Room Type
    avg_price_rt = df.groupby('room_type')['price'].mean().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=FIG_SIZE)
    sns.barplot(x=avg_price_rt.index, y=avg_price_rt.values, palette=PALETTE, ax=ax)
    ax.set_title('Average Price by Room Type')
    ax.set_xlabel('Room Type')
    ax.set_ylabel('Avg Price (USD)')
    plt.tight_layout()
    fig.savefig(FIGURES_PATH / '05_avg_price_by_room_type.png', dpi=150)
    plt.close(fig)

    # 06 Occupancy Rate by Borough
    occ_by_ng = df.groupby('neighbourhood_group')['occupancy_rate'].mean().reindex(BOROUGH_ORDER)
    fig, ax = plt.subplots(figsize=FIG_SIZE)
    sns.barplot(x=occ_by_ng.values, y=occ_by_ng.index, palette=PALETTE, ax=ax)
    ax.set_title('Average Occupancy Rate by Borough')
    ax.set_xlabel('Avg Occupancy Rate')
    ax.set_ylabel('Borough')
    ax.xaxis.set_major_formatter(mticker.PercentFormatter(xmax=1))
    plt.tight_layout()
    fig.savefig(FIGURES_PATH / '06_occupancy_by_borough.png', dpi=150)
    plt.close(fig)

    # 07 Demand Score by Borough
    demand_by_ng = df.groupby('neighbourhood_group')['demand_score'].mean().reindex(BOROUGH_ORDER)
    fig, ax = plt.subplots(figsize=FIG_SIZE)
    sns.barplot(x=demand_by_ng.values, y=demand_by_ng.index, palette=PALETTE, ax=ax)
    ax.set_title('Average Demand Score by Borough (Reviews / Availability)')
    ax.set_xlabel('Avg Demand Score')
    ax.set_ylabel('Borough')
    plt.tight_layout()
    fig.savefig(FIGURES_PATH / '07_demand_score_by_borough.png', dpi=150)
    plt.close(fig)

    # 08 Value Score by Borough
    value_by_ng = df.groupby('neighbourhood_group')['value_score'].mean().reindex(BOROUGH_ORDER)
    fig, ax = plt.subplots(figsize=FIG_SIZE)
    sns.barplot(x=value_by_ng.values, y=value_by_ng.index, palette=PALETTE, ax=ax)
    ax.set_title('Average Value Score by Borough (Reviews / Price)')
    ax.set_xlabel('Avg Value Score')
    ax.set_ylabel('Borough')
    plt.tight_layout()
    fig.savefig(FIGURES_PATH / '08_value_score_by_borough.png', dpi=150)
    plt.close(fig)

    # 09 Top 10 Neighbourhoods by Listing Count
    top_neigh = df['neighbourhood'].value_counts().head(10)
    fig, ax = plt.subplots(figsize=FIG_SIZE)
    sns.barplot(x=top_neigh.values, y=top_neigh.index, color=PALETTE[0], ax=ax)
    ax.set_title('Top 10 Neighbourhoods by Listing Count')
    ax.set_xlabel('Count')
    ax.set_ylabel('Neighbourhood')
    plt.tight_layout()
    fig.savefig(FIGURES_PATH / '09_top10_neighbourhoods.png', dpi=150)
    plt.close(fig)

    # 10 Correlation Heatmap
    corr_cols   = ['price', 'number_of_reviews', 'availability_365',
                   'minimum_nights', 'demand_score', 'value_score', 'occupancy_rate']
    corr_matrix = df[corr_cols].corr()
    fig, ax = plt.subplots(figsize=(9, 7))
    sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='RdBu_r',
                center=0, linewidths=0.5, ax=ax)
    ax.set_title('Correlation Heatmap — Key Metrics')
    plt.tight_layout()
    fig.savefig(FIGURES_PATH / '10_correlation_heatmap.png', dpi=150)
    plt.close(fig)

    log('✓ Step 3 — EDA complete          (10 plots saved to reports/figures/)')


# ── Step 4 — Statistical Analysis ────────────────────────────────────────────

def step_stats(df: pd.DataFrame) -> None:
    """Run grouped stats and hypothesis tests; save CSVs to reports/stats/."""

    # Grouped stats by Borough
    grouped_borough = (
        df.groupby('neighbourhood_group')[['price', 'number_of_reviews',
                                           'availability_365', 'demand_score',
                                           'value_score', 'occupancy_rate']]
        .agg(['mean', 'median', 'std', 'min', 'max'])
        .round(4)
    )
    grouped_borough.columns = ['_'.join(c) for c in grouped_borough.columns]
    grouped_borough.reset_index().to_csv(STATS_PATH / 'grouped_stats_by_borough.csv', index=False)

    # Grouped stats by Room Type
    grouped_room = (
        df.groupby('room_type')[['price', 'number_of_reviews',
                                  'availability_365', 'demand_score',
                                  'value_score', 'occupancy_rate']]
        .agg(['mean', 'median', 'std', 'min', 'max'])
        .round(4)
    )
    grouped_room.columns = ['_'.join(c) for c in grouped_room.columns]
    grouped_room.reset_index().to_csv(STATS_PATH / 'grouped_stats_by_room_type.csv', index=False)

    # Grouped stats by Price Category
    grouped_price_cat = (
        df.groupby('price_category', observed=True)[['price', 'demand_score',
                                                      'value_score', 'occupancy_rate']]
        .agg(['mean', 'median', 'std'])
        .round(4)
    )
    grouped_price_cat.columns = ['_'.join(c) for c in grouped_price_cat.columns]
    grouped_price_cat.reset_index().to_csv(STATS_PATH / 'grouped_stats_by_price_category.csv', index=False)

    # Avg Price by Neighbourhood (top 20)
    (
        df.groupby('neighbourhood')['price']
        .mean().round(2).reset_index()
        .rename(columns={'price': 'avg_price_usd'})
        .sort_values('avg_price_usd', ascending=False)
        .head(20)
        .to_csv(STATS_PATH / 'avg_price_by_neighbourhood_top20.csv', index=False)
    )

    # Top 10 Best-Value Listings (highest value_score, excluding outlier prices)
    (
        df[~df['is_price_outlier']]
        .nlargest(10, 'value_score')
        [['id', 'name', 'neighbourhood_group', 'neighbourhood',
          'room_type', 'price', 'number_of_reviews', 'value_score', 'demand_score']]
        .to_csv(STATS_PATH / 'top10_best_value_listings.csv', index=False)
    )

    # ── Hypothesis Tests ─────────────────────────────────────────────────────

    # ANOVA — Price by Borough
    borough_groups   = [g['price'].dropna().values for _, g in df.groupby('neighbourhood_group')]
    f_boro, p_boro   = stats.f_oneway(*borough_groups)

    # ANOVA — Price by Room Type
    rt_groups        = [g['price'].dropna().values for _, g in df.groupby('room_type')]
    f_rt, p_rt       = stats.f_oneway(*rt_groups)

    # ANOVA — Demand Score by Borough
    dem_groups       = [g['demand_score'].dropna().values for _, g in df.groupby('neighbourhood_group')]
    f_dem, p_dem     = stats.f_oneway(*dem_groups)

    # Spearman — Price vs Demand Score
    sp_data          = df[['price', 'demand_score']].dropna()
    r_pd, p_pd       = stats.spearmanr(sp_data['price'], sp_data['demand_score'])

    # Spearman — Price vs Value Score
    sp_data2         = df[['price', 'value_score']].dropna()
    r_pv, p_pv       = stats.spearmanr(sp_data2['price'], sp_data2['value_score'])

    # Spearman — Availability vs Number of Reviews
    sp_data3         = df[['availability_365', 'number_of_reviews']].dropna()
    r_av, p_av       = stats.spearmanr(sp_data3['availability_365'], sp_data3['number_of_reviews'])

    pd.DataFrame([
        {'Test': 'One-Way ANOVA',        'Description': 'Price by Borough',                    'Statistic': round(f_boro, 4), 'p-value': round(p_boro, 6), 'Significant (α=0.05)': p_boro < ALPHA},
        {'Test': 'One-Way ANOVA',        'Description': 'Price by Room Type',                  'Statistic': round(f_rt, 4),   'p-value': round(p_rt, 6),   'Significant (α=0.05)': p_rt < ALPHA},
        {'Test': 'One-Way ANOVA',        'Description': 'Demand Score by Borough',             'Statistic': round(f_dem, 4),  'p-value': round(p_dem, 6),  'Significant (α=0.05)': p_dem < ALPHA},
        {'Test': 'Spearman Correlation', 'Description': 'Price vs Demand Score',               'Statistic': round(r_pd, 4),   'p-value': round(p_pd, 6),   'Significant (α=0.05)': p_pd < ALPHA},
        {'Test': 'Spearman Correlation', 'Description': 'Price vs Value Score',                'Statistic': round(r_pv, 4),   'p-value': round(p_pv, 6),   'Significant (α=0.05)': p_pv < ALPHA},
        {'Test': 'Spearman Correlation', 'Description': 'Availability vs Number of Reviews',   'Statistic': round(r_av, 4),   'p-value': round(p_av, 6),   'Significant (α=0.05)': p_av < ALPHA},
    ]).to_csv(STATS_PATH / 'hypothesis_test_results.csv', index=False)

    log('✓ Step 4 — Stats complete        (6 CSVs saved to reports/stats/)')


# ── Step 5 — Final Load Prep ─────────────────────────────────────────────────

def step_final_load(df: pd.DataFrame) -> pd.DataFrame:
    """
    Final transformations and validation before persisting the analytics-ready dataset.
    """
    # Drop internal flag column
    df = df.drop(columns=['is_price_outlier'], errors='ignore')

    # Standardise column names to snake_case (already done for Airbnb dataset)
    rename_map = {
        'neighbourhood_group': 'borough',
    }
    df = df.rename(columns=rename_map)

    # Validation
    assert df.isnull().sum().sum() == 0, 'Nulls found in final dataset!'
    assert df.duplicated().sum()   == 0, 'Duplicates found in final dataset!'
    assert (df['price'] > 0).all(), 'Zero/negative prices in final dataset!'

    df.to_csv(FINAL_PATH, index=False)
    log(f'✓ Step 5 — Final Load complete   ({len(df):,} rows → {FINAL_PATH})')
    return df


# ── Step 6 — Summary Report ──────────────────────────────────────────────────

def step_summary(df: pd.DataFrame) -> None:
    """Print and save a human-readable summary of key metrics."""
    lines = [
        '═══ NYC Airbnb ETL — Pipeline Summary ═══',
        f'Total Listings          : {len(df):,}',
        f'Boroughs Covered        : {df["borough"].nunique()} ({", ".join(sorted(df["borough"].unique()))})',
        f'Neighbourhoods          : {df["neighbourhood"].nunique()}',
        f'Room Types              : {", ".join(df["room_type"].unique())}',
        '',
        '── Price KPIs ─────────────────────────',
        f'Avg Price (USD)         : ${df["price"].mean():.2f}',
        f'Median Price (USD)      : ${df["price"].median():.2f}',
        f'Price per Person (avg)  : ${df["price_per_person"].mean():.2f}',
        '',
        '── Demand & Value KPIs ────────────────',
        f'Avg Demand Score        : {df["demand_score"].mean():.4f}',
        f'Avg Value Score         : {df["value_score"].mean():.4f}',
        f'Avg Occupancy Rate      : {df["occupancy_rate"].mean():.2%}',
        f'Total Reviews           : {df["number_of_reviews"].sum():,}',
        f'Avg Reviews per Listing : {df["number_of_reviews"].mean():.2f}',
        '',
        '── Price Category Breakdown ───────────',
    ]
    cat_counts = df['price_category'].value_counts()
    for cat, cnt in cat_counts.items():
        lines.append(f'  {str(cat):<12} : {cnt:,} ({cnt/len(df)*100:.1f}%)')

    lines += [
        '',
        '── Avg Price by Borough ───────────────',
    ]
    for boro, val in df.groupby('borough')['price'].mean().sort_values(ascending=False).items():
        lines.append(f'  {boro:<15}: ${val:.2f}')

    report = '\n'.join(lines)
    print('\n' + report)
    (STATS_PATH / 'pipeline_summary.txt').write_text(report)
    log('✓ Step 6 — Summary saved to reports/stats/pipeline_summary.txt')


# ── Main ─────────────────────────────────────────────────────────────────────

def main(source_path: str = None) -> None:
    """
    Run the full ETL pipeline.

    Args:
        source_path: Optional path to the raw/processed CSV.
                     Defaults to data/raw/AB_NYC_2019.csv.
    """
    log('═══ NYC Airbnb ETL Pipeline Started ═══')

    try:
        df = step_extract(source_path)
    except FileNotFoundError as e:
        log(f'✗ Step 1 — Extraction failed: {e}')
        log('  Tip: set source_path=<your CSV path> or place the file at data/raw/AB_NYC_2019.csv')
        return

    try:
        df = step_clean(df)
    except Exception as e:
        log(f'✗ Step 2 — Cleaning failed: {e}')
        return

    try:
        step_eda(df)
    except Exception as e:
        log(f'✗ Step 3 — EDA failed: {e}')
        return

    try:
        step_stats(df)
    except Exception as e:
        log(f'✗ Step 4 — Statistical Analysis failed: {e}')
        return

    try:
        df = step_final_load(df)
    except Exception as e:
        log(f'✗ Step 5 — Final Load failed: {e}')
        return

    try:
        step_summary(df)
    except Exception as e:
        log(f'✗ Step 6 — Summary failed: {e}')

    log('═══ NYC Airbnb ETL Pipeline Completed Successfully ═══')


if __name__ == '__main__':
    import sys
    src = sys.argv[1] if len(sys.argv) > 1 else None
    main(source_path=src)
