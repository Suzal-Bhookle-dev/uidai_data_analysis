# Unlocking Societal Trends in Aadhaar Enrolment and Updates

## Project Overview
As Aadhaar nears universal coverage in India, the challenge shifts from **Identity Creation** to **Identity Lifecycle Management**. This project analyzes millions of records across Enrolment, Demographic, and Biometric datasets to identify patterns of digital maturation and gaps in welfare compliance.

## Tech Stack & Methodology
- **Language:** Python
- **Package Manager:** [uv](https://github.com/astral-sh/uv)
- **Data Engineering:** Pandas, Glob
- **Visualization:** Matplotlib, Seaborn

### Data Cleaning Highlights
- **Geospatial Mapping:** Resolved variations like `WEST BANGAL` and `ORISSA` into a standardized valid list of 36 States/UTs.
- **Integrity Checks:** Implemented Regex filters to remove numeric-only artifacts from geographic columns.
- **Consolidation:** Merged 12 CSV partitions into a unified 3-tier data architecture.

## Key Analyses
1. **Digital vs. Physical Maturity:** Comparing Demographic (voluntary) vs. Biometric (mandatory) updates.
2. **Child Compliance Gap:** Tracking the transition of infants (0-5) to the Mandatory Biometric Update (5-17) phase.
3. **Temporal Trends:** Mapping surges in digital adoption for the adult population.

## Getting Started

### Prerequisites
Ensure you have Python 3.9+ installed.
### Installation
You can set up the environment using either the traditional `pip` method or the ultra-fast `uv` method.

#### Option A: Using pip (Standard)
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/aadhaar-analysis.git
   cd aadhaar-analysis
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
#### Option B: Using uv (Fastest)
If you have [uv](https://github.com/astral-sh/uv) installed:
1. Clone the repository and sync dependencies:
   ```bash
   git clone https://github.com/yourusername/aadhaar-analysis.git
   cd aadhaar-analysis
   uv sync
   ```

### Running the Analysis
Once installed, run the main script to generate the insights and charts:
```bash
# Using pip
python main.py

# Using uv
uv run main.py
```

