import streamlit as st
import pandas as pd
import preprocessor
import helper
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.figure_factory as ff

# Load Data
df = pd.read_csv('athlete_events.csv')
df_region = pd.read_csv('noc_regions.csv')
df = preprocessor.preprocess(df, df_region)

# Sidebar Styling
st.sidebar.image(
    "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5c/Olympic_rings_with_transparent_rims.svg/250px-Olympic_rings_with_transparent_rims.svg.png",
    width=120)
st.sidebar.title("🏅 Olympic Analysis")
st.sidebar.markdown("---")

# Sidebar Menu
user_menu = st.sidebar.radio(
    "🔍 Select an Option",
    ("🏆 Medal Tally", "📊 Overall Analysis", "🌍 Country-wise Analysis", "🏃‍♂️ Athlete Analysis")
)

st.sidebar.markdown("---")

# Display Raw Data (Optional)
with st.expander("📂 View Raw Data"):
    st.dataframe(df)

# Medal Tally
if user_menu == "🏆 Medal Tally":
    st.sidebar.header("🥇 Medal Tally")

    year, country = helper.country_year_list(df)
    selected_year = st.sidebar.selectbox("📅 Select Year", year)
    selected_country = st.sidebar.selectbox("🌍 Select Country", country)

    medal_tally = helper.fetch_medal_tally(df, selected_year, selected_country)

    # Display Title
    st.title("🏅 Medal Tally")
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.subheader("Overall Medal Tally")
    elif selected_year != 'Overall' and selected_country == 'Overall':
        st.subheader(f"Medal Tally in {selected_year} Olympics")
    elif selected_year == 'Overall' and selected_country != 'Overall':
        st.subheader(f"{selected_country} Overall Performance")
    else:
        st.subheader(f"{selected_country} Performance in {selected_year} Olympics")

    st.table(medal_tally)

# Overall Analysis
if user_menu == "📊 Overall Analysis":
    st.title("📈 Olympic Statistics")

    col1, col2, col3 = st.columns(3)
    col4, col5, col6 = st.columns(3)

    col1.metric("🏟️ Editions", df['Year'].nunique() - 1)
    col2.metric("🏙️ Host Cities", df['City'].nunique())
    col3.metric("🏅 Sports", df['Sport'].nunique())
    col4.metric("🎽 Events", df['Event'].nunique())
    col5.metric("🌍 Nations", df['region'].nunique())
    col6.metric("👨‍🎓 Athletes", df['Name'].nunique())

    # Line Plots
    st.markdown("## 📊 Trends Over Time")

    fig = px.line(helper.data_over_time(df, 'region'), x="Edition", y="count", labels={"count": "Number of Nations"})
    st.plotly_chart(fig, use_container_width=True)

    fig = px.line(helper.data_over_time(df, 'Event'), x="Edition", y="count", labels={"count": "Number of Events"})
    st.plotly_chart(fig, use_container_width=True)

    fig = px.line(helper.data_over_time(df, 'Name'), x="Edition", y="count", labels={"count": "Number of Athletes"})
    st.plotly_chart(fig, use_container_width=True)

    # Heatmap
    st.markdown("## 🎯 Events Over Time (Per Sport)")
    fig, ax = plt.subplots(figsize=(16, 12))
    heatmap_data = df.drop_duplicates(['Year', 'Sport', 'Event']).pivot_table(index='Sport', columns='Year',
                                                                              values='Event', aggfunc='count').fillna(
        0).astype('int')
    sns.heatmap(heatmap_data, annot=True, cmap="coolwarm", linewidths=0.5, ax=ax)
    st.pyplot(fig)

# Country-wise Analysis
if user_menu == "🌍 Country-wise Analysis":
    st.sidebar.title("🌏 Country-wise Analysis")
    country_list = sorted(df['region'].dropna().unique().tolist())
    selected_country = st.sidebar.selectbox("🇺🇳 Select a Country", country_list)

    st.title(f"📊 {selected_country} - Medal Tally Over Time")
    country_df = helper.year_wise_medal(df, selected_country)
    fig = px.line(country_df, x="Year", y="Medal", title=f"{selected_country} Medal Performance Over Time")
    st.plotly_chart(fig, use_container_width=True)

    # Heatmap of top sports
    st.markdown(f"## 🏆 {selected_country} Excels In These Sports")
    pt = helper.country_event_heatmap(df, selected_country)
    fig, ax = plt.subplots(figsize=(16, 12))
    sns.heatmap(pt, annot=True, cmap="viridis", linewidths=0.5, ax=ax)
    st.pyplot(fig)

    # Top 10 Athletes
    st.markdown(f"## 🥇 Top 10 Athletes from {selected_country}")
    top10_df = helper.most_successful_countrywise(df, selected_country)
    st.table(top10_df)

# Athlete-wise Analysis
if user_menu == "🏃‍♂️ Athlete Analysis":
    st.title("👟 Athlete Analysis")

    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    # Age Distribution
    st.markdown("### 🎂 Age Distribution")
    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall', 'Gold Medalists', 'Silver Medalists', 'Bronze Medalists'],
                             show_hist=False, show_rug=False)
    fig.update_layout(width=900, height=500)
    st.plotly_chart(fig, use_container_width=True)

    # Age Distribution per Sport
    st.markdown("### 🏅 Age Distribution of Gold Medalists in Different Sports")
    famous_sports = ['Basketball', 'Judo', 'Football', 'Athletics', 'Swimming', 'Badminton', 'Gymnastics', 'Boxing']
    x = [athlete_df[athlete_df['Sport'] == sport][athlete_df['Medal'] == 'Gold']['Age'].dropna() for sport in
         famous_sports]

    fig = ff.create_distplot(x, famous_sports, show_hist=False, show_rug=False)
    fig.update_layout(width=900, height=500)
    st.plotly_chart(fig, use_container_width=True)
