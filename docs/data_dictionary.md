# Data Dictionary — NYC Airbnb Smart Booking Intelligence

> **Newton School of Technology | Data Visualization & Analytics | Capstone 2**

---

## How To Use This File

- Add one row for each column used in analysis or dashboarding.
- Explains what the field means in plain language.
- Mentions any cleaning or standardization applied.
- Flags nullable columns, derived fields, and known quality issues.

---

## Dataset Summary

| Item | Details |
|---|---|
| **Dataset Name** | NYC Airbnb Open Data 2019 (processed) |
| **Source** | Inside Airbnb / Kaggle — [AB_NYC_2019](https://www.kaggle.com/datasets/dgomonov/new-york-city-airbnb-open-data) |
| **Raw File Name** | `AB_NYC_2019.csv` |
| **Processed File Name** | `processed_AB_NYC_2019.csv` |
| **Last Updated** | 2019 (data reflects listings active up to July 2019) |
| **Granularity** | One row per unique Airbnb listing in New York City |
| **Total Rows (processed)** | 45,739 |
| **Total Columns** | 17 (16 source + 1 derived) |

---

## Column Definitions

| Column Name | Data Type | Description | Example Value | Used In | Cleaning Notes |
|---|---|---|---|---|---|
| `id` | integer | Unique identifier for each Airbnb listing | `2539` | EDA | No nulls. Not used in analysis — identifier only. |
| `name` | string | Listing title as set by the host | `"Clean & quiet apt home by the park"` | Tableau (Top 10 Best Value bubble chart) | No nulls in processed file. Used for display labelling only. |
| `host_id` | integer | Unique identifier for the host | `2787` | EDA | No nulls. Used to count multi-listing hosts via `calculated_host_listings_count`. |
| `host_name` | string | First name of the host | `"John"` | EDA | No nulls. Not used in KPIs or dashboards. |
| `neighbourhood_group` | string | NYC borough the listing belongs to | `"Brooklyn"` | EDA / KPI / Tableau | No nulls. 5 distinct values: Manhattan, Brooklyn, Queens, Bronx, Staten Island. Primary geographic filter in all 4 dashboards. |
| `neighbourhood` | string | Specific neighbourhood within the borough | `"Kensington"` | EDA / Tableau | No nulls. Used for granular neighbourhood-level breakdowns. |
| `latitude` | float | GPS latitude coordinate of the listing | `40.64749` | Tableau (map) | No nulls. Used in geographic distribution map on Dashboard 3. |
| `longitude` | float | GPS longitude coordinate of the listing | `-73.97237` | Tableau (map) | No nulls. Used in geographic distribution map on Dashboard 3. |
| `room_type` | string | Category of accommodation offered | `"Private room"` | EDA / KPI / Tableau | No nulls. 3 distinct values: Entire home/apt, Private room, Shared room. Used as a filter and segmentation dimension across all dashboards. |
| `price` | float | Nightly listing price in USD | `149.0` | KPI / EDA / Tableau | No nulls. 11 listings have price = $0 (flagged as data quality issue — likely test or inactive listings). Max capped at $323 in processed file (outliers >$500 removed). Used in price distribution, KPI averages, and demand/value scoring. |
| `minimum_nights` | integer | Minimum number of nights required per booking | `1` | EDA / Tableau | No nulls. Range: 1–1250. 13 listings have minimum_nights > 365 (retained but noted as anomalous). Used in "Average Price vs Minimum Nights" chart on Dashboard 2. |
| `number_of_reviews` | integer | Total number of reviews the listing has received | `9` | EDA / KPI / Tableau | No nulls. Range: 0–629. Listings with 0 reviews may be new or inactive. Used as a proxy for historical booking volume. |
| `last_review` | date | Date of the most recent guest review | `2018-10-19` | EDA | **8,971 nulls** — listings with no reviews have no last_review date. Nulls filled with "No Reviews" label for categorical analysis. Not used directly in KPIs. |
| `reviews_per_month` | float | Average number of reviews received per month | `0.21` | KPI / EDA / Tableau | **8,971 nulls** (same listings as `last_review` nulls). Nulls filled with `0` for scoring purposes. Used in Demand Score and Reviews per Month KPIs. |
| `calculated_host_listings_count` | integer | Total number of listings the host has on Airbnb | `6` | EDA / KPI | No nulls. Used as denominator in `price_per_person` calculation. Indicates professional/multi-property hosts vs individual hosts. |
| `availability_365` | integer | Number of days the listing is available for booking in the next 365 days | `365` | KPI / EDA / Tableau | No nulls. Range: 0–365. Used to compute Occupancy Rate and Availability Category. 0 = fully booked or blocked; 365 = always available. |
| `price_per_person` | float | Derived: effective nightly cost per person (see Derived Columns) | `74.5` | KPI / Tableau | No nulls in processed file. Range: $0–$161.5. 11 records show $0 (tied to zero-price listings). Used in Value Score and Price per Person KPI tile. |

---

## Derived Columns

| Derived Column | Logic | Business Meaning |
|---|---|---|
| `price_per_person` | `price / calculated_host_listings_count` | Normalises nightly price by the host's total listing count, producing a per-person cost proxy that enables fairer value comparisons across multi-listing and single-listing hosts. |
| `occupancy_rate` *(computed in notebook)* | `(365 - availability_365) / 365` | Estimates the proportion of the year a listing is booked. A listing available 0 days has an occupancy rate of 1.0 (fully booked); one available all 365 days has 0.0. Used in Dashboard 3 (Occupancy Rate by Neighbourhood). |
| `value_score` *(computed in notebook)* | `reviews_per_month / price_per_person` *(normalised)* | Combines guest engagement (review frequency) with affordability (price per person) into a single value-for-money index. Higher scores indicate better guest satisfaction per dollar spent. Used in Dashboard 1 (Value for Money by Borough). |
| `demand_score` *(computed in notebook)* | `reviews_per_month × (1 - availability_365 / 365)` | Captures booking pressure by combining how frequently a listing is reviewed (demand signal) with how unavailable it is (scarcity signal). Higher scores indicate high-demand, frequently booked listings. Used in Dashboard 4 (Demand Score by Neighbourhood, High Demand Premium Zones). |
| `price_category` *(computed in notebook)* | Budget: price ≤ $75 / Mid-Range: $75–$175 / Luxury: > $175 | Segments listings into three tiers for demand and availability analysis. Used in Dashboard 4 (Price Category vs Demand Score). |
| `availability_category` *(computed in notebook)* | Low: availability_365 ≤ 90 / Medium: 91–270 / High: > 270 | Groups listings by booking pressure based on days available. Used in Dashboard 3 (Availability Category by Neighbourhood). |

---

## Data Quality Notes

1. **Zero-price listings (11 records):** Eleven listings have `price = $0`. These are likely test entries, placeholder listings, or data entry errors. They were retained in the processed file but should be excluded from any price-based KPI computation by applying a `price > 0` filter.

2. **Null reviews (8,971 records):** Listings with no reviews have null values in both `last_review` and `reviews_per_month`. These represent approximately 19.6% of all listings and likely correspond to new or inactive listings. `reviews_per_month` nulls were filled with `0` for scoring; `last_review` nulls were labelled "No Reviews" for categorical use.

3. **Extreme minimum_nights values (13 records):** Thirteen listings have `minimum_nights > 365`, which is logically impossible for a standard annual availability window. These were retained but flagged — they may represent long-term rental listings misclassified as short-term.

4. **Price outliers:** The original raw dataset contained listings priced above $10,000/night. The processed file caps prices at $323 (the 99th percentile or dataset maximum post-cleaning), removing extreme outliers that would skew average price KPIs.

5. **Geographic coverage:** The dataset covers all five NYC boroughs but is heavily skewed toward Manhattan (~21,600 listings) and Brooklyn (~20,100 listings), which together represent ~90% of total supply. Bronx, Queens, and Staten Island are underrepresented and should be interpreted with this context.

6. **2019 snapshot only:** This dataset is a static snapshot from 2019. It does not reflect post-pandemic shifts in short-term rental behaviour, regulatory changes, or current pricing. All insights should be contextualised as 2019 market conditions.

7. **`calculated_host_listings_count` as proxy:** This column reflects the host's total platform-wide listing count at the time of data collection, not confirmed simultaneous availability. It is used as a proxy denominator for `price_per_person` and should be treated as approximate.

---

*Newton School of Technology - Data Visualization & Analytics | Capstone 2*
