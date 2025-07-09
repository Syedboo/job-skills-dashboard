import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Streamlit page setup
st.set_page_config(page_title="Skill Trends by Location", layout="wide")
st.title("📊 Top In-Demand Skills for Data Science roles by Location")

# Load exploded dataset
@st.cache_data
def load_data():
    return pd.read_csv("C:/Users/tabu9/PycharmProjects/pythonProject/exploded_skills.csv")  # <-- Replace with your actual path

df = load_data()

# Drop NA skills just in case
df = df.dropna(subset=['extracted_skills'])

# Sidebar filters
st.sidebar.header("🔍 Filters")

# Location filter
locations = sorted(df['location'].dropna().unique().tolist())
locations.insert(0, "All")  # Add 'All' to top of list
selected_location = st.sidebar.selectbox("Select a Location", locations)


# Top N filter
top_n = st.sidebar.slider("Top N Skills", min_value=5, max_value=50, value=15, step=1)

if selected_location == "All":
    filtered_df = df.copy()
else:
    filtered_df = df[df['location'] == selected_location]


# Count top skills
top_skills = (
    filtered_df['extracted_skills']
    .value_counts()
    .head(top_n)
    .reset_index()
)
top_skills.columns = ['skill', 'count']

# Visualization
st.subheader(f"Top {top_n} Skills in 📍 {selected_location}")

fig, ax = plt.subplots(figsize=(10, max(6, 0.4 * top_n)))
sns.barplot(data=top_skills, y='skill', x='count', palette='crest', ax=ax)

# Add count labels
for p in ax.patches:
    ax.text(p.get_width() + 1, p.get_y() + p.get_height() / 2,
            int(p.get_width()), ha='left', va='center', fontsize=9)

ax.set_title(f"Top {top_n} Skills in {selected_location}", fontsize=14)
ax.set_xlabel("Number of Job Mentions")
ax.set_ylabel("Skill")
st.pyplot(fig)

# Optional: show raw table
with st.expander("📄 View Raw Skill Count Table"):
    st.dataframe(top_skills)
