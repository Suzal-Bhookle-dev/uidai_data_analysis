import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import glob
import os


# Merge all data of a category into one
def load_and_merge(folder_path: str, category_name: str) -> pd.DataFrame:
    # Get all the csv file
    all_files = glob.glob(os.path.join(folder_path, "*.csv"))
    print(f"Found {len(all_files)} files for {category_name}")

    # make iterable of dataframes
    df_list = []
    for file_name in all_files:
        df_list.append(pd.read_csv(file_name))

    # merge all dataframes
    merged_df = pd.concat(df_list, axis=0, ignore_index=True)
    print(f"Total row in {category_name}: {len(merged_df)}")

    return merged_df


# paths of all the dataset
basepath = "datasets"
biometric_path = os.path.join(basepath, "api_data_aadhar_biometric")
demographic_path = os.path.join(basepath, "api_data_aadhar_demographic")
enrolment_path = os.path.join(basepath, "api_data_aadhar_enrolment")

# dataframse of datasets
df_biometric = load_and_merge(biometric_path, "Biometric")
df_demographic = load_and_merge(demographic_path, "Demographic")
df_enrolment = load_and_merge(enrolment_path, "Enrolment")

# Cleaning Dataset
state_mapping = {
    "ORISSA": "ODISHA",
    "UTTARANCHAL": "UTTARAKHAND",
    "PONDICHERRY": "PUDUCHERRY",
    "WEST  BENGAL": "WEST BENGAL",
    "WESTBENGAL": "WEST BENGAL",
    "WEST BANGAL": "WEST BENGAL",
    "WEST BENGLI": "WEST BENGAL",
    "CHHATISGARH": "CHHATTISGARH",
    "JAMMU & KASHMIR": "JAMMU AND KASHMIR",
    "DAMAN & DIU": "DAMAN AND DIU",
    "DADRA & NAGAR HAVELI": "DADRA AND NAGAR HAVELI",
    "THE DADRA AND NAGAR HAVELI AND DAMAN AND DIU": "DADRA AND NAGAR HAVELI AND DAMAN AND DIU",
}

valid_states = {
    "ANDHRA PRADESH",
    "ARUNACHAL PRADESH",
    "ASSAM",
    "BIHAR",
    "CHHATTISGARH",
    "GOA",
    "GUJARAT",
    "HARYANA",
    "HIMACHAL PRADESH",
    "JHARKHAND",
    "KARNATAKA",
    "KERALA",
    "MADHYA PRADESH",
    "MAHARASHTRA",
    "MANIPUR",
    "MEGHALAYA",
    "MIZORAM",
    "NAGALAND",
    "ODISHA",
    "PUNJAB",
    "RAJASTHAN",
    "SIKKIM",
    "TAMIL NADU",
    "TELANGANA",
    "TRIPURA",
    "UTTAR PRADESH",
    "UTTARAKHAND",
    "WEST BENGAL",
    "DELHI",
    "CHANDIGARH",
    "PUDUCHERRY",
    "LADAKH",
    "JAMMU AND KASHMIR",
    "LAKSHADWEEP",
    "ANDAMAN AND NICOBAR ISLANDS",
    "DADRA AND NAGAR HAVELI AND DAMAN AND DIU",
}

dfs = [df_biometric, df_demographic, df_enrolment]

for i, df in enumerate(dfs):

    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], format="%d-%m-%Y", errors="coerce")

    if "district" in df.columns:
        df["district"] = df["district"].astype(str).str.strip().str.upper()

    if "state" in df.columns:
        df["state"] = (
            df["state"].astype(str).str.strip().str.upper().replace(state_mapping)
        )

        # remove numeric-only values
        df = df[~df["state"].str.fullmatch(r"\d+", na=False)]

        # keep only valid states
        df = df[df["state"].isin(valid_states)]

    dfs[i] = df

df_biometric, df_demographic, df_enrolment = dfs


# Analysis


# THE "DIGITAL vs PHYSICAL" UPDATE TREND
total_demo = df_demographic[["demo_age_5_17", "demo_age_17_"]].sum().sum()
total_bio = df_biometric[["bio_age_5_17", "bio_age_17_"]].sum().sum()
print(f"Raw Sums -> Demo: {total_demo}, Bio: {total_bio}")

plt.figure(figsize=(7, 5))
sns.barplot(
    x=["Demographic Updates", "Biometric Updates"],
    y=[total_demo, total_bio],
    palette="viridis",
)
plt.ticklabel_format(style="plain", axis="y")
plt.title("National Trend: Demographic vs. Biometric Demand")
plt.ylabel("Total Count")
plt.savefig("demo_vs_bio.png")


# THE CHILD COMPLIANCE GAP (MBU ANALYSIS)

# We compare age 0-5 enrolments vs age 5-17 Biometric Updates
state_child_enrol = df_enrolment.groupby("state")["age_0_5"].sum()
state_child_bio = df_biometric.groupby("state")["bio_age_5_17"].sum()

# Identify where child biometric updates are lagging behind enrolments
child_gap_ratio = (state_child_bio / state_child_enrol).sort_values(ascending=False)

plt.figure(figsize=(12, 6))
child_gap_ratio.head(10).plot(kind="bar", color="coral")
plt.title("States with Highest Child Biometric Update Compliance")
plt.ylabel("Update-to-Enrolment Ratio")
plt.savefig("child_compliance.png")


# ADULT DIGITAL ADOPTION TREND (Time-Series)

# Tracking demo_age_17_ (Adults updating mobile/address for digital services)
df_demographic.set_index("date", inplace=True)
adult_digital_trend = df_demographic.resample("M")["demo_age_17_"].sum()

plt.figure(figsize=(12, 5))
adult_digital_trend.plot(color="green", marker="o", linestyle="--")
plt.ticklabel_format(style="plain", axis="y")
plt.title("Adult Demographic Updates Over Time (Digital Maturation)")
plt.ylabel("Number of Updates")
plt.grid(True)
plt.savefig("adult_trend.png")
