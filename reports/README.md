Project Report: NYC Airbnb Client-Centric Analytics Dashboard
1. Cover Page

Project Title: NYC Airbnb Client-Centric Analytics Dashboard 
+1

Sector: Hospitality and Travel Analytics

Team ID and Team Members: Section A, Group 18

Faculty Mentor: Ayushi Mam

Institute: [User to specify]

Submission Date: April 27, 2026

2. Executive Summary
Problem: Clients struggle to navigate the high-density NYC Airbnb market to find listings that balance cost, safety, and popularity.


Approach: Cleaned a dataset of 48,000+ records via Python, engineered value metrics, and built a 4-tier interactive Tableau dashboard.
+1


Key Insights: Budget listings (<$100) are predominantly in specific boroughs, and high availability does not always correlate with high popularity .


Key Recommendations: Utilize "Value Scores" to identify high-quality, lower-cost stays in emerging neighborhoods.
+2

3. Sector and Business Context

Sector Overview: The short-term rental market in NYC is highly competitive and price-volatile.

Decision-maker / Stakeholder: Individual travelers and potential Airbnb guests (Client-side).

Why this problem matters: Travelers need transparent data to avoid overpaying and to ensure their chosen location meets stay requirements.

4. Problem Statement and Objectives
Formal Problem Definition: Empower users to identify the most suitable Airbnb listings in NYC by analyzing pricing, neighborhood trends, and reviews.


Scope: 2019 NYC Airbnb data covering five borough groups and various room types.
+1


Success Criteria: Delivery of a professional dashboard suite providing actionable market snapshots and booking intelligence.

5. Data Description
Source Citation and Access Link: Inside Airbnb; GitHub Repository.

Dataset Size and Coverage: Original dataset ~48,895 rows; cleaned version contains 45,739 rows across 17 columns.


Key Columns: price, neighbourhood_group, room_type, number_of_reviews, availability_365, and minimum_nights .

Data Quality Issues: Missing values in host names/titles and significant price outliers.

6. Cleaning and Transformation
Major Cleaning Steps: Imputed "Unknown" for missing names, converted last_review to datetime, and removed duplicate entries.

Assumptions Made: Listings with zero price or extreme high-end outliers (calculated via IQR) were removed to prevent skewing averages.


Output Dataset Description: processed_AB_NYC_2019.csv featuring standardized lowercase headers and a new price_per_person metric.

7. KPI Framework

KPI 1: Average Price: AVG(price) – Measures the baseline cost for the market .


KPI 2: Demand Score: [number_of_reviews] / [availability_365] – Measures listing popularity vs. vacancy.
+1


KPI 3: Value Score: [number_of_reviews] / [price] – Identifies listings providing the most feedback (satisfaction) for the lowest cost.
+1

8. Exploratory Analysis

Major Trends: Price varies significantly by room_type, with Entire Homes commanding a premium.
+1


Segment-level Insights: Manhattan dominates the luxury segment, while Brooklyn offers a higher concentration of "Mid-Range" value listings.
+2


Visual Summaries: Treemaps for borough volume and Histograms for price distribution.
+2

9. Statistical Analysis

Method Used: Interquartile Range (IQR) for outlier detection and Bivariate analysis (Scatter plots) for price/review correlations.
+1

Results: Removal of outliers reduced data noise, highlighting a clear concentration of listings in the $50-$200 range.


Business Interpretation: Most "high value" listings fall within the $100-$300 "Mid-Range" category.
+1

10. Dashboard Walkthrough

Dashboard Objective: Guide a user from market awareness to a specific booking decision.


Executive View: Market Overview (Dashboard 1) showing total listings and average costs.


Operational View: Location and Demand Dashboards (3 & 4) for granular map-based filtering.
+1


Filters and Interactivity: Global filters for Neighborhood, Room Type, and Price Category applied across all views .
+1

11. Key Insights

Borough Popularity: Brooklyn and Manhattan hold the highest listing volume.


Price Skew: The market is heavily weighted toward "Budget" and "Mid-Range" categories.


Value Hotspots: Specific neighborhoods yield higher Value Scores despite lower total review counts.


Stay Duration: Higher minimum_nights often correlates with lower nightly prices.
+1


Room Type Preference: Entire homes are the most reviewed, suggesting higher demand despite cost.


Availability Gap: Many high-demand listings have low availability_365.
+1

12. Recommendations

Target Mid-Range: Clients should focus on the $100-$300 range to maximize the Value Score.
+1


Borough Selection: Use the Map view to find "Budget" clusters in Queens for proximity to Manhattan without the price premium.


Booking Lead Time: Prioritize listings with a high Demand Score but moderate availability for the best quality experience.

13. Limitations and Next Steps
Data Limitations: 2019 data does not reflect post-pandemic pricing shifts or newer NYC short-term rental regulations.

Method Limitations: IQR may exclude legitimate high-end luxury penthouses that are part of the market reality.

Suggested Future Work: Integrate sentiment analysis of review text and real-time pricing APIs for 2026 trends.

14. Contribution Matrix
Team ID and Team Members: Section A, Group 18

Data Cleaning (Python/Colab): Akhil Mishra
Project Report & Documentation: Abhishek Sharma
PPT: Chaitanya Kumar
Visualisation/ Dashboard: Jashvitha Lakshmi Omkaram

GitHub Repository Management: jash1910