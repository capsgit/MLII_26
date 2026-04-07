"""
app.py

Streamlit UI for Sentiment Analysis App.

Features:
- Text input + language selection
- Sentence-level breakdown
- Global sentiment metrics
- Volatility indicator
- Visual dashboard components
"""

import pandas as pd
import streamlit as st

from sentiment_service import analyze_sentiment


# =========================================================
# UI HELPERS
# =========================================================

def get_sentiment_style(label: str) -> tuple[str, str, str]:
    if label == "positive":
        return "🟢", "#d1fae5", "#166534"
    elif label == "negative":
        return "🔴", "#fee2e2", "#991b1b"
    return "🟡", "#fef3c7", "#92400e"


def render_stat_card(title: str, value: str) -> str:
    return f"""
    <div style="
        background-color: #f0f9ff;
        padding: 16px;
        border-radius: 12px;
        border: 1px solid #e5e7eb;
        text-align: center;
    ">
        <div style="font-size: 13px; color: #6b7280;">{title}</div>
        <div style="font-size: 28px; font-weight: 700;">{value}</div>
    </div>
    """


def render_circle_stat(label: str, value: str, bg: str, emoji: str) -> str:
    return f"""
    <div style="display:flex; flex-direction:column; align-items:center;">
        <div style="
            width:90px;
            height:90px;
            border-radius:50%;
            background:{bg};
            display:flex;
            align-items:center;
            justify-content:center;
            font-size:26px;
            font-weight:700;
        ">
            {value}
        </div>
        <div style="margin-top:6px; font-size:13px;">
            {emoji} {label}
        </div>
    </div>
    """


# =========================================================
# STREAMLIT CONFIG
# =========================================================

st.set_page_config(
    page_title="Sentiment Analysis App",
    page_icon="😐",
    layout="wide",
)

outer_left, main_col, outer_right = st.columns([1, 5, 1])

with main_col:

    st.title("😐 Sentiment Analysis")
    st.write("Write/copy text to be analysed.")

    input_col, side_col = st.columns([4, 1])

    with input_col:
        text_submitted = st.text_area("Enter text 👇", height=220)

    with side_col:
        language = st.selectbox(
            "Language",
            ["EN", "DE", "ES", "FR", "IT"]
        )

        st.caption("Non-English text is translated to English before analysis.")
        analyze_clicked = st.button("🔍 Analyze", use_container_width=True)

    if analyze_clicked:

        result = analyze_sentiment(text_submitted, language)

        if result["ok"]:

            st.success("Analysis completed.")

            # =========================================================
            # HEADER CARD
            # =========================================================

            emoji, bg_color, text_color = get_sentiment_style(result["global_label"])

            st.subheader("Overall result")

            st.markdown(
                f"""
                <div style="
                    background:{bg_color};
                    color:{text_color};
                    padding:14px;
                    border-radius:12px;
                ">
                    <b>{emoji} Overall sentiment: {result['global_label'].capitalize()}</b><br>
                    {result['summary']}
                </div>
                """,
                unsafe_allow_html=True
            )

            # =========================================================
            # TOP METRICS
            # =========================================================

            s1, s2, s3, s4 = st.columns(4)

            s1.markdown(render_stat_card("Language", result["language"]), unsafe_allow_html=True)
            s2.markdown(render_stat_card("Sentences", len(result["sentence_results"])), unsafe_allow_html=True)
            s3.markdown(render_stat_card("Polarity", result["global_polarity"]), unsafe_allow_html=True)
            s4.markdown(render_stat_card("Volatility", result["volatility"]), unsafe_allow_html=True)

            st.divider()

            # =========================================================
            # DISTRIBUTION
            # =========================================================

            st.subheader("Sentiment distribution")

            c1, c2, c3 = st.columns(3)

            c1.markdown(render_circle_stat("Positive", result["counts"]["positive"], "#dcfce7", "🟢"), unsafe_allow_html=True)
            c2.markdown(render_circle_stat("Neutral", result["counts"]["neutral"], "#fef9c3", "🟡"), unsafe_allow_html=True)
            c3.markdown(render_circle_stat("Negative", result["counts"]["negative"], "#fee2e2", "🔴"), unsafe_allow_html=True)

            # =========================================================
            # TABLE
            # =========================================================

            st.subheader("Sentence by sentence")

            df = pd.DataFrame(result["sentence_results"])
            df = df.rename(columns={
                "index": "#",
                "sentence": "Sentence",
                "polarity": "Polarity",
                "label": "Sentiment",
            })

            st.dataframe(df, use_container_width=True, hide_index=True)

        else:
            st.error(result["error"])