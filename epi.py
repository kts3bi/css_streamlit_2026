# -*- coding: utf-8 -*-
"""
Created on Sun Feb  1 18:38:15 2026

@author: Donald.Tshabalala
"""

import streamlit as st
import pandas as pd
import numpy as np

# Page config
st.set_page_config(page_title="Epidemiologist Profile | Donald Tshabalala", layout="wide")

# -----------------------------
# Profile info (edit here)
# -----------------------------
name = "Mr. Donald Tshabalala"
title = "Epidemiologist & Biostatistics Researcher"
institution = "Sefako Makgatho Health Sciences University (SMU)"
location = "South Africa"
email = "donald.tshabalala@icloud.com"

areas = [
    "HIV epidemiology (AGYW treatment uptake, viral suppression, ART interruption)",
    "Infectious disease surveillance and program evaluation",
    "Applied biostatistics (regression modelling, longitudinal analysis)",
    "Health systems & workforce research (e.g., nurse attrition and service delivery)",
    "Antimicrobial stewardship knowledge and practice research",
    "Data science for public health (R, Stata, Python, Streamlit dashboards)"
]

# Optional links (leave blank if not used)
orcid = ""
google_scholar = ""
linkedin = ""
github = ""

# -----------------------------
# Header
# -----------------------------
st.title("Epidemiologist Research Profile")
st.caption(f"{title} • {institution} • {location}")

col1, col2 = st.columns([1, 2], vertical_alignment="center")

with col1:
    st.image(
        "https://images.pexels.com/photos/3786157/pexels-photo-3786157.jpeg",
        caption="Public health & data science (royalty-free image)",
        use_container_width=True
    )

with col2:
    st.subheader("About")
    st.write(
        "I work at the intersection of epidemiology, biostatistics, and health systems strengthening. "
        "My research focuses on generating actionable evidence for policy and practice—particularly in HIV "
        "program outcomes, antimicrobial stewardship, and workforce dynamics within the South African health system."
    )

    st.subheader("Core research areas")
    for a in areas:
        st.write(f"• {a}")

# -----------------------------
# Quick stats (demo)
# -----------------------------
st.divider()
st.subheader("At-a-glance (demo metrics)")

m1, m2, m3, m4 = st.columns(4)
m1.metric("Active projects", "6")
m2.metric("Primary tools", "R • Stata • Python")
m3.metric("Focus population", "AGYW")
m4.metric("Preferred outputs", "Policy-ready evidence")

# -----------------------------
# Publications upload + filter
# -----------------------------
st.divider()
st.header("Publications")

st.write(
    "Upload a CSV of your publications (e.g., columns like: `Title`, `Authors`, `Journal`, `Year`, `Keywords`). "
    "If you include a `Year` column, the app will automatically plot trends."
)

uploaded_file = st.file_uploader("Upload a CSV of Publications", type="csv")

publications = None
if uploaded_file:
    publications = pd.read_csv(uploaded_file)
    st.dataframe(publications, use_container_width=True)

    # Filter by keyword across all columns
    keyword = st.text_input("Filter by keyword (searches across all columns)", "")
    if keyword.strip():
        filtered = publications[
            publications.apply(
                lambda row: keyword.lower() in row.astype(str).str.lower().values, axis=1
            )
        ]
        st.write(f"Filtered Results for '{keyword}':")
        st.dataframe(filtered, use_container_width=True)
    else:
        st.info("Tip: Type a keyword above to filter your publications.")

# -----------------------------
# Publication trends
# -----------------------------
st.divider()
st.header("Publication trends")

if publications is not None:
    if "Year" in publications.columns:
        # Clean year values safely
        pubs_year = publications.copy()
        pubs_year["Year"] = pd.to_numeric(pubs_year["Year"], errors="coerce")
        year_counts = pubs_year["Year"].dropna().astype(int).value_counts().sort_index()
        if len(year_counts) > 0:
            st.bar_chart(year_counts)
        else:
            st.warning("No valid numeric years found in the `Year` column.")
    else:
        st.warning("Your CSV does not include a `Year` column. Add one to enable trend plots.")
else:
    st.caption("Upload a publications CSV above to enable trends.")

# -----------------------------
# Epidemiology demo data explorer
# -----------------------------
st.divider()
st.header("Explore epidemiology demo data")
st.write(
    "These small demo datasets are included to showcase how an epidemiologist might explore "
    "surveillance, program performance, or field data in a simple dashboard."
)

# Demo datasets (synthetic)
surveillance = pd.DataFrame({
    "Week": np.arange(1, 13),
    "Suspected_cases": [12, 18, 15, 22, 19, 25, 27, 31, 24, 20, 18, 16],
    "Confirmed_cases": [4, 7, 6, 9, 8, 11, 13, 14, 10, 9, 7, 6],
    "District": ["A", "A", "B", "B", "A", "C", "C", "C", "B", "A", "B", "A"]
})

hiv_program = pd.DataFrame({
    "Facility": ["Clinic 1", "Clinic 2", "Clinic 3", "Clinic 4", "Clinic 5"],
    "AGYW_initiated_ART": [85, 64, 92, 58, 77],
    "Viral_suppression_%": [78, 71, 82, 69, 75],
    "Interruptions_%": [9, 12, 7, 14, 10]
})

ams_knowledge = pd.DataFrame({
    "Programme": ["Nursing", "Pharmacy", "Medical"],
    "Mean_score_%": [61, 68, 64],
    "Sample_size": [120, 85, 95]
})

dataset = st.selectbox(
    "Choose a dataset",
    ["Weekly surveillance (synthetic)", "HIV programme indicators (synthetic)", "Antimicrobial stewardship knowledge (synthetic)"]
)

if dataset == "Weekly surveillance (synthetic)":
    st.write("### Weekly surveillance line list summary")
    st.dataframe(surveillance, use_container_width=True)

    week_range = st.slider("Select epidemiological week range", 1, int(surveillance["Week"].max()), (1, 12))
    d_filter = st.multiselect("Filter by district", sorted(surveillance["District"].unique()), default=sorted(surveillance["District"].unique()))

    df = surveillance[
        surveillance["Week"].between(week_range[0], week_range[1]) &
        surveillance["District"].isin(d_filter)
    ]

    st.write("Filtered results:")
    st.dataframe(df, use_container_width=True)

    st.write("Cases over time (confirmed)")
    st.line_chart(df.set_index("Week")["Confirmed_cases"])

elif dataset == "HIV programme indicators (synthetic)":
    st.write("### HIV programme indicators (AGYW-focused)")
    st.dataframe(hiv_program, use_container_width=True)

    vs_min = st.slider("Minimum viral suppression (%)", 0, 100, 70)
    df = hiv_program[hiv_program["Viral_suppression_%"] >= vs_min]

    st.write(f"Facilities with viral suppression ≥ {vs_min}%:")
    st.dataframe(df, use_container_width=True)

    st.write("Viral suppression by facility")
    chart_df = df.set_index("Facility")["Viral_suppression_%"]
    st.bar_chart(chart_df)

elif dataset == "Antimicrobial stewardship knowledge (synthetic)":
    st.write("### Antimicrobial stewardship knowledge scores")
    st.dataframe(ams_knowledge, use_container_width=True)

    min_score = st.slider("Minimum mean score (%)", 0, 100, 60)
    df = ams_knowledge[ams_knowledge["Mean_score_%"] >= min_score]

    st.write("Filtered programmes:")
    st.dataframe(df, use_container_width=True)

    st.write("Mean score by programme")
    st.bar_chart(df.set_index("Programme")["Mean_score_%"])

# -----------------------------
# Contact + links
# -----------------------------
st.divider()
st.header("Contact")

st.write(f"**Email:** {email}")
st.write(f"**Institution:** {institution}")

# Optional links section
links = []
if orcid.strip():
    links.append(("ORCID", orcid))
if google_scholar.strip():
    links.append(("Google Scholar", google_scholar))
if linkedin.strip():
    links.append(("LinkedIn", linkedin))
if github.strip():
    links.append(("GitHub", github))

if links:
    st.subheader("Links")
    for label, url in links:
        st.write(f"- {label}: {url}")
else:
    st.caption("Add your ORCID / Google Scholar / LinkedIn / GitHub links in the variables at the top if you want them displayed.")

st.divider()
st.caption("Built with Streamlit • Profile template for CSS2026")

