# SectionA_Group18_AirbnbNYCAnalysis

---

## Project Overview

| Field | Details |
|---|---|
| **Project Title** | NYC Airbnb Smart Booking Intelligence |
| **Sector** | Hospitality / Short-Term Rental |
| **Team ID** | SectionA_Group18|
| **Section** | A|
| **Faculty Mentor** ||
| **Institute** | Newton School of Technology |
| **Submission Date** |29/04/2026|

### Team Members

| Role | Name | GitHub Username |
|---|---|---|
| Project Lead | _Name_ | `github-handle` |
| Data Lead | _Name_ | `github-handle` |
| ETL Lead | _Name_ | `github-handle` |
| Analysis Lead | _Name_ | `github-handle` |
| Visualization Lead | _Name_ | `github-handle` |
| Strategy Lead | _Name_ | `github-handle` |
| PPT and Quality Lead | _Name_ | `github-handle` |

---

## Business Problem

The short-term rental market in New York City is large, fragmented, and difficult for travellers to navigate. With over 45,000 active listings spread across five boroughs, guests face significant challenges in identifying listings that offer the best combination of price, location, availability, and quality. Without structured analysis, travellers often overpay or make suboptimal booking decisions based on incomplete information.

This project analyses the Inside Airbnb NYC 2019 dataset to surface patterns in pricing, neighbourhood performance, room type distributions, demand signals, and guest satisfaction that are otherwise invisible in raw listing data.

**Core Business Question**

> Which NYC Airbnb listings and neighbourhoods offer the best value, availability, and demand profile — and what factors should guide a guest's booking decision?

**Decision Supported**

> This analysis enables guests and platform strategists to make smarter booking and inventory decisions by identifying high-value neighbourhoods, optimal price brackets, and room types with the strongest occupancy and review performance.

---

## Dataset

| Attribute | Details |
|---|---|
| **Source Name** | Inside Airbnb / Kaggle — AB_NYC_2019 |
| **Direct Access Link** | https://www.kaggle.com/datasets/dgomonov/new-york-city-airbnb-open-data |
| **Row Count** | 48,000+ |
| **Column Count** | 16 |
| **Time Period Covered** | 2019 (last review dates up to July 2019) |
| **Format** | CSV |

**Key Columns Used**

| Column Name | Description | Role in Analysis |
|---|---|---|
| `neighbourhood_group` | NYC borough (Manhattan, Brooklyn, Queens, Bronx, Staten Island) | Primary geographic segmentation and filter |
| `room_type` | Type of listing — Entire home/apt, Private room, Shared room | Room-level segmentation, price stratification |
| `price` | Nightly listing price in USD | Core KPI; used in price distribution, value scoring, and demand scoring |
| `availability_365` | Number of days the listing is available in a year | Availability categorisation, occupancy rate computation |
| `number_of_reviews` | Total reviews received by the listing | Proxy for booking volume and demand |
| `reviews_per_month` | Average monthly review rate | Demand signal; used in demand score calculation |
| `minimum_nights` | Minimum stay requirement set by the host | Stay preference filter; used in average price vs minimum nights analysis |
| `price_per_person` | Derived: price divided by a normalisation factor | Value-for-money score component |

For full column definitions, see [`docs/data_dictionary.md`](docs/data_dictionary.md).

---

## KPI Framework

| KPI | Definition | Formula / Computation |
|---|---|---|
| **Average Price** | Mean nightly price across filtered listings | `df['price'].mean()` — ref: `notebooks/04_statistical_analysis.ipynb` |
| **Occupancy Rate** | Estimated share of the year a listing is booked | `(365 - availability_365) / 365` — ref: `notebooks/03_eda.ipynb` |
| **Value Score** | Price-adjusted quality signal combining reviews and price per person | `reviews_per_month / price_per_person` (normalised) — ref: `notebooks/04_statistical_analysis.ipynb` |
| **Demand Score** | Composite demand signal based on review frequency and availability | `reviews_per_month * (1 - availability_365/365)` — ref: `notebooks/04_statistical_analysis.ipynb` |
| **Price per Person** | Effective nightly cost per guest | `price / calculated_host_listings_count` (proxy) — ref: `notebooks/02_cleaning.ipynb` |
| **Reviews per Month** | Average monthly booking proxy | Raw column `reviews_per_month` — ref: `notebooks/03_eda.ipynb` |

Document KPI logic clearly in `notebooks/04_statistical_analysis.ipynb` and `notebooks/05_final_load_prep.ipynb`.

---

## Tableau Dashboard

| Item | Details |
|---|---|
| **Dashboard URL** | https://public.tableau.com/app/profile/jashvitha.omkaram/viz/BNBnycalmostfinal/Dashboard1|
| **Executive View (Dashboard 1)** | High-level KPI summary — avg price ($119.1), total listings (45,739), avg reviews (23.92), availability (109.2 days), price per person ($33.37), occupancy rate (70.07%). Includes price distribution histogram, room type pie chart, value-for-money by borough, and listing count by neighbourhood. |
| **Price Analysis View (Dashboard 2)** | Drill-down into pricing — avg price by room type, price by neighbourhood group, avg price vs minimum nights trend, and reviews vs price scatter by room type. |
| **Location Analysis View (Dashboard 3)** | Geographic distribution of listings by price and demand on a NYC map, top 10 best-value listings bubble chart, availability category by neighbourhood stacked bar, and occupancy rate by neighbourhood. |
| **Demand Analysis View (Dashboard 4)** | Demand score by neighbourhood, price category vs demand score, high-demand premium zones scatter (price vs demand), and reviews per month by neighbourhood. |
| **Main Filters** | Neighbourhood Group, Room Type, Availability Category, Price Category |

Store dashboard screenshots in [`tableau/screenshots/`](tableau/screenshots/) and document the public links in [`tableau/dashboard_links.md`](tableau/dashboard_links.md).

---

## Key Insights

1. **Manhattan commands the highest prices** at an average of $144.74/night — nearly double the Bronx ($77.13) — reflecting premium location demand.
2. **Entire home/apt listings price significantly higher** (~$160/night) than private rooms (~$80) and shared rooms (~$60), confirming room type as the strongest price driver.
3. **Staten Island offers the best value for money** with a value score of 0.5094, followed by the Bronx (0.4398), suggesting underutilised affordable boroughs.
4. **Brooklyn and Manhattan dominate listing volume**, each with ~20,000 listings, accounting for the majority of NYC's Airbnb supply.
5. **Overall occupancy rate is 70.07%**, indicating strong market utilisation, with Brooklyn and Manhattan leading borough-level occupancy.
6. **Queens leads in reviews per month** (1.95), suggesting it has the highest booking frequency relative to listing count.
7. **Minimum night requirements above 25 nights correlate with higher average prices** ($168.6), pointing to a long-stay premium segment.
8. **Mid-range price category generates the highest average demand score**, outperforming both budget and luxury segments — indicating sweet-spot pricing.
9. **Manhattan and Brooklyn are high-demand premium zones**, sitting at the top-right of the demand-price scatter, making them attractive for hosts seeking revenue maximisation.
10. **Shared rooms receive fewer reviews per unit despite lower prices**, suggesting travellers prefer private rooms for comparable savings with better privacy.
11. **Top 10 best-value listings are concentrated in Queens and Brooklyn**, reinforcing these boroughs as the primary value destinations for budget-conscious guests.
12. **Availability patterns vary significantly by borough** — Staten Island has more listings in the high-availability tier, while Manhattan skews toward low-availability (high-demand) listings.

---

## Recommendations

| # | Insight | Recommendation | Expected Impact |
|---|---|---|---|
| 1 | Staten Island and Bronx offer best value scores but low listing counts | Platform and hosts should actively promote these boroughs to value-seeking travellers through targeted campaigns | Reduced demand pressure on Manhattan; improved occupancy and revenue for underserved boroughs |
| 2 | Mid-range pricing drives the highest demand scores | Hosts in budget or luxury tiers should reconsider pricing strategy to move toward the $80–$130 range where demand is strongest | Higher booking rates and improved occupancy for repriced listings |
| 3 | Queens leads in reviews per month, indicating high booking velocity | Travellers on a budget should prioritise Queens listings for best availability and booking ease; hosts should increase supply in Queens | Improved guest satisfaction and reduced booking friction |
| 4 | Minimum night requirements above 25 nights correlate with higher prices | Hosts targeting long-stay or corporate travellers should differentiate listings with 25+ night minimums and adjust pricing to the $140–$170 range | Higher per-stay revenue from long-stay segment |
| 5 | Shared rooms underperform on reviews despite low prices | Hosts operating shared rooms should consider converting to private rooms where feasible, or invest in amenity upgrades to improve review velocity | Improved value score, higher bookings, and better platform ranking |

---

## Analytical Pipeline

The project follows a structured 7-step workflow:

1. **Define** - Sector selected, problem statement scoped, mentor approval obtained.
2. **Extract** - Raw dataset sourced and committed to `data/raw/`; data dictionary drafted.
3. **Clean and Transform** - Cleaning pipeline built in `notebooks/02_cleaning.ipynb` and optionally `scripts/etl_pipeline.py`.
4. **Analyze** - EDA and statistical analysis performed in notebooks `03` and `04`.
5. **Visualize** - Interactive Tableau dashboard built and published on Tableau Public.
6. **Recommend** - 3-5 data-backed business recommendations delivered.
7. **Report** - Final project report and presentation deck completed and exported to PDF in `reports/`.

---
## Contribution Matrix
| Team Member | Dataset and Sourcing | ETL and Cleaning | EDA and Analysis | Statistical Analysis | Tableau Dashboard | Report Writing | PPT and Viva |
|---|---|---|---|---|---|---|---|
|Jashvitha| Support |Support | Support |Support | Owner |Support | Support |
|Aditya|Support | Support | Owner| Support | Support |Support |Support  |
|Chaitanya|Support | Support |Support  | Support  | Support  | Support | Owner |
|Akhil| Support  |Owner | Support  | Support  | Support  | Support  | Support  |
|Abhishek| Support  |Support  | Support  | Support  | Support  | Owner| Support  |
|Krish| Owner | Support  | Support  | Support  | Support  | Support  | Support  |

_Declaration: We confirm that the above contribution details are accurate and verifiable through GitHub Insights, PR history, and submitted artifacts._

**Team Lead Name:** Jashvitha Lakshmi Omkaram
**Date:** 29/04/2026

---
