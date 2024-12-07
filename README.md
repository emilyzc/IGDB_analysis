# IGDB Analysis

Welcome to the **IGDB Analysis** repository! This project focuses on a comprehensive analysis of game data from the [IGDB (Internet Game Database)](https://www.igdb.com/) platform. The project aims to:

- **Preprocess** raw game data
- Perform **Exploratory Data Analysis (EDA)**
  -   Game Development & LocalizationStrategy (part one)
  -   Clustering & Community Insights (part two)
- Develop **Predictive Models** to forecast game ratings (part three)

This analysis can aid game developers, marketers, and researchers in understanding trends and making data-driven decisions.

## Features

- **Data Acquisition:** Automated scripts to download and update game data from IGDB.
- **Data Preprocessing:** Scripts to clean, transform, and prepare raw data for analysis.
- **Exploratory Data Analysis (EDA):** Visualizations and statistical analysis to uncover insights.
- **Predictive Modeling:** Machine learning models to predict game ratings.
- **Documentation:** Comprehensive guides and documentation for ease of use.

## Installation

### Prerequisites

Ensure you have the following installed:

- **Python 3.8+**
- **Git**

### Clone the Repository

```bash
git clone https://github.com/yourusername/IGDB_analysis.git
cd IGDB_analysis
```

### Create a Virtual Environment
```bash
python3 -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

### API Setup
- **IGDB API:** Obtain an API key from IGDB.
- **Environment Variables:** Add your API credentials.
```bash
IGDB_CLIENT_ID=your_client_id
IGDB_CLIENT_SECRET=your_client_secret
```

## Usage
### Data Preprocessing
Download and preprocess the data using the scripts in the data_preprocessing folder.

#### Fetch Data
Download game data from IGDB and save it to a specified file.
```bash
python data_preprocessing/fetch_data.py
```
#### Non-Numeric Processing
Clean and process non-numeric features in the dataset, including handling categorical variables and one-hot encoding.
```bash
python data_preprocessing/nonnumeric_processing.py
```
#### Numeric Processing
Process numeric features by handling missing values, normalizing data, and performing feature analysis.
```bash
python data_preprocessing/numeric_processing.py
```

## Exploratory Data Analysis (Part One and Part Two)
Generate EDA reports and visualizations.

**For part one visualization can be found at part one/GameAnalysis_Part1.ipynb**

**For part two visualization can be found at part two/task_1.ipynb**



## Predictive Modeling (Part Three)
Train and evaluate models to predict game ratings.
```bash
jupyter notebook part_three/rating_prediction.ipynb
```
This notebook contains code and analysis related to building and assessing predictive models for game ratings.
