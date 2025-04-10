import streamlit as st
import pandas as pd
import altair as alt
import requests
import io

st.set_page_config(page_title="Splunk-Style Log Analyzer", layout="wide")
st.title("🔍 Log Analytics Dashboard")

st.sidebar.header("Upload Logs")

uploaded_file = st.sidebar.file_uploader("Upload a CSV log file", type=["csv"])

if uploaded_file:
    with st.spinner("Classifying logs..."):
        # Send file to FastAPI
        response = requests.post(
            "http://localhost:8000/classify/",  # update if deployed elsewhere
            files={"file": (uploaded_file.name, uploaded_file, "text/csv")},
        )

        if response.status_code != 200:
            st.error("Failed to classify logs: " + response.json().get("detail", "Unknown error"))
        else:
            df = pd.read_csv(io.BytesIO(response.content))

            st.success("Logs classified successfully!")

            st.subheader("📊 Log Classification Summary")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Logs", len(df))
            with col2:
                st.metric("Unique Labels", df['target_label'].nunique())

            label_counts = df['target_label'].value_counts().reset_index()
            label_counts.columns = ['Label', 'Count']

            chart = alt.Chart(label_counts).mark_bar().encode(
                x=alt.X("Count:Q"),
                y=alt.Y("Label:N", sort="-x"),
                color="Label:N"
            ).properties(height=400)

            st.altair_chart(chart, use_container_width=True)

            st.subheader("🧠 Filter & Explore Logs")

            # Filters
            label_filter = st.multiselect("Select target labels to filter", options=df['target_label'].unique())
            source_filter = st.multiselect("Select source(s) to filter", options=df['source'].unique())
            search_term = st.text_input("Search log messages")

            filtered_df = df.copy()
            if label_filter:
                filtered_df = filtered_df[filtered_df['target_label'].isin(label_filter)]
            if source_filter:
                filtered_df = filtered_df[filtered_df['source'].isin(source_filter)]
            if search_term:
                filtered_df = filtered_df[filtered_df['log_message'].str.contains(search_term, case=False, na=False)]

            st.write(f"Displaying {len(filtered_df)} of {len(df)} log entries.")
            st.dataframe(filtered_df, use_container_width=True)

            csv = filtered_df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download filtered logs", csv, "filtered_logs.csv", "text/csv")
