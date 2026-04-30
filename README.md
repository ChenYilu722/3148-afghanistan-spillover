# Project Overview: Afghanistan Conflict Spillover Analysis (2020-2021)

## Introduction
This repository contains an interactive political science report analyzing the spatial diffusion of political violence from Afghanistan to its neighboring countries. Contrary to conventional wisdom regarding conflict contagion, this project investigates whether instability in a central conflict node necessarily spreads to bordering regions.

## Data Sources
This study utilizes primary data from the **Armed Conflict Location & Event Data Project (ACLED)**. ACLED is a high-resolution, disaggregated database that records political violence and protest events worldwide. 
* **Temporal Scope:** A 13-month window from January 2020 to January 2021.
* **Geographic Scope:** Afghanistan (the primary conflict node) and its six neighboring states: Turkmenistan, Uzbekistan, Tajikistan, Iran, Pakistan, and China.

## Methodology
The analysis employs a **lagged Ordinary Least Squares (OLS) regression** methodology. The model is designed to isolate spillover impacts by testing whether the intensity of political violence in Afghanistan at a given month (time *t*) serves as a significant predictor of violence levels in its six neighboring states during the subsequent month (time *t+1*). This time-lagged design allows for the observation of how instability might slowly traverse borders.

## Key Findings
1. **The "V-Shape" Trajectory in Afghanistan:** In 2020, Afghanistan saw a sharp dip in violence during April and May (due to the US-Taliban Doha Agreement, COVID-19 lockdowns, and Ramadan/Eid ceasefires), flanked by intense fighting at the beginning and end of the year.
2. **The Spillover Paradox (Negative Correlation):** Surprisingly, the data reveals a negative correlation between violence in Afghanistan and its neighbors. For example, the Pearson correlation with Uzbekistan is -0.60, and -0.54 for both Tajikistan and China. 
3. **Implications:** Instead of a direct contagion effect, when fighting inside Afghanistan intensifies, neighbors tend to record *fewer* violent events in the following month. This may be due to neighboring states heightening border security and military alerts, or transnational armed groups temporarily concentrating their resources solely within the Afghan battlefield.

## Limitations
* **Sample Size:** The temporal scope of the study is limited to a 13-month period, providing a relatively small sample size for the regression model.
* **Lag Interval Sensitivity:** The one-month time lag utilized in the model might be either too short or too long to capture the true, complex dynamics of conflict diffusion across borders. 

## Author Information
**Chen Yilu**  
* **Course:** POLI3148: Data Science in Politics and Public Administration (25-26 Semester 2)  
* **Institution:** The University of Hong Kong (HKU)
