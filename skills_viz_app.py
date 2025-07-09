import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Streamlit page setup
st.set_page_config(page_title="Skill Trends by Location and Company", layout="wide")
st.title("📊 Top In-Demand Skills for Data Science Roles")

# Load exploded dataset from GitHub
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/Syedboo/job-skills-dashboard/main/exploded_skills.csv"
    return pd.read_csv(url)

df = load_data()

# Drop NA skills and fill missing company names
df = df.dropna(subset=['extracted_skills'])
df['companyName'] = df['companyName'].fillna("Unknown")

# Sidebar filters
st.sidebar.header("🔍 Filters")

# Location filter
locations = sorted(df['location'].dropna().unique().tolist())
locations.insert(0, "All")  # Add 'All' option
selected_location = st.sidebar.selectbox("Select a Location", locations)

# Company filter
companies = sorted(df['companyName'].unique().tolist())
companies.insert(0, "All")  # Add 'All' option
selected_company = st.sidebar.selectbox("Select a Company", companies)

# Top N filter
top_n = st.sidebar.slider("Top N Skills", min_value=5, max_value=50, value=15, step=1)

# Apply filters
filtered_df = df.copy()

if selected_location != "All":
    filtered_df = filtered_df[filtered_df['location'] == selected_location]

if selected_company != "All":
    filtered_df = filtered_df[filtered_df['companyName'] == selected_company]

# Count top skills
top_skills = (
    filtered_df['extracted_skills']
    .value_counts()
    .head(top_n)
    .reset_index()
)
top_skills.columns = ['skill', 'count']

# Dynamic subtitle
loc_label = selected_location if selected_location != "All" else "All Locations"
comp_label = selected_company if selected_company != "All" else "All Companies"
st.subheader(f"Top {top_n} Skills in 📍 {loc_label} at 🏢 {comp_label}")

# Plotting
fig, ax = plt.subplots(figsize=(10, max(6, 0.4 * len(top_skills))))
sns.barplot(data=top_skills, y='skill', x='count', palette='crest', ax=ax)

# Add value labels
for p in ax.patches:
    ax.text(p.get_width() + 1, p.get_y() + p.get_height() / 2,
            int(p.get_width()), ha='left', va='center', fontsize=9)

ax.set_xlabel("Number of Mentions")
ax.set_ylabel("Skill")
ax.set_title(f"Top {top_n} Skills in {loc_label} at {comp_label}", fontsize=14)
st.pyplot(fig)

# Optional: View raw data table
with st.expander("📄 View Raw Skill Count Table"):
    st.dataframe(top_skills)

# Optional: Download filtered skill data
csv = top_skills.to_csv(index=False).encode('utf-8')
st.download_button(
    label="⬇️ Download Skill Counts as CSV",
    data=csv,
    file_name=f"skills_{loc_label}_{comp_label}.csv",
    mime='text/csv',
)
