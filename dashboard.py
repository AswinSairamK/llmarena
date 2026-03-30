import streamlit as st
import json
import glob
from pathlib import Path

st.set_page_config(
    page_title="LLMArena",
    page_icon="",
    layout="wide"
)

# ============================================================
# LOAD LATEST BENCHMARK REPORT
# ============================================================

report_files = glob.glob("reports/llmarena_full_report_*.json")
# glob finds all files matching the pattern
# * is a wildcard — matches any characters

if not report_files:
    st.error("No benchmark reports found. Run the notebook first!")
    st.stop()
    # st.stop() halts the app — nothing below runs

# get the most recent report
latest_report = sorted(report_files)[-1]
# sorted() sorts alphabetically — timestamps sort chronologically
# [-1] gets the last item — most recent

with open(latest_report, "r", encoding="utf-8") as f:
    report = json.load(f)
# load the JSON report into a Python dictionary

# extract results
llama  = report["extraction_results"]["llama_3_groq"]
gemini = report["extraction_results"]["gemini_2_5_flash"]
rag    = report["rag_results"]

# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("LLMArena")
st.sidebar.caption("Multi-LLM Research Paper Benchmarker")
st.sidebar.divider()

page = st.sidebar.radio(
    "Navigation",
    ["Leaderboard", "Extraction Results", "RAG Q&A", "Full Report"]
)

st.sidebar.divider()
st.sidebar.caption(f"Report: {Path(latest_report).name}")
st.sidebar.caption(f"Tested at: {report['tested_at'][:19]}")
st.sidebar.caption(f"Paper: {report['paper_tested'][:40]}...")


# ============================================================
# PAGE 1 — LEADERBOARD
# ============================================================

if page == "Leaderboard":

    st.title("LLMArena Leaderboard")
    st.caption("Multi-LLM benchmark results for research paper extraction")
    st.divider()

    # top metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Llama 3 accuracy",  f"{llama['accuracy']}%")
    col2.metric("Gemini accuracy",   f"{gemini['accuracy']}%")
    col3.metric(
        "Speed advantage",
        f"{round(gemini['latency_s'] / llama['latency_s'], 1)}x",
        delta="Llama 3 faster"
    )
    # delta shows a green arrow with label underneath the metric
    col4.metric(
        "Cost advantage",
        "Free vs $" + str(gemini['cost_usd']),
        delta="Llama 3 cheaper"
    )

    st.divider()

    # leaderboard table
    st.subheader("Model Comparison")

    leaderboard_data = [
        {
            "Rank"          : "1",
            "Model"         : "Llama 3 (Groq)",
            "Accuracy"      : f"{llama['accuracy']}%",
            "Latency"       : f"{llama['latency_s']}s",
            "Total tokens"  : f"{llama['total_tokens']:,}",
            "Cost per paper": f"${llama['cost_usd']}",
            "Winner"        : "Speed + Cost"
        },
        {
            "Rank"          : "2",
            "Model"         : "Gemini 2.5 Flash",
            "Accuracy"      : f"{gemini['accuracy']}%",
            "Latency"       : f"{gemini['latency_s']}s",
            "Total tokens"  : f"{gemini['total_tokens']:,}",
            "Cost per paper": f"${gemini['cost_usd']}",
            "Winner"        : "Detail"
        },
    ]
    st.dataframe(leaderboard_data, use_container_width=True)

    st.divider()

    # bar charts
    st.subheader("Visual Comparison")

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.markdown("**Latency (seconds) — lower is better**")
        st.bar_chart({
            "Llama 3 (Groq)"   : llama["latency_s"],
            "Gemini 2.5 Flash" : gemini["latency_s"]
        })
        # st.bar_chart() creates a simple bar chart
        # dictionary keys = x axis labels
        # dictionary values = bar heights

    with chart_col2:
        st.markdown("**Cost per paper ($) — lower is better**")
        st.bar_chart({
            "Llama 3 (Groq)"   : llama["cost_usd"],
            "Gemini 2.5 Flash" : gemini["cost_usd"]
        })

    st.divider()
    st.subheader("Recommendation")
    st.success(report["recommendation"])
    # st.success() shows a green box with a checkmark


# ============================================================
# PAGE 2 — EXTRACTION RESULTS
# ============================================================

elif page == "Extraction Results":

    st.title("Extraction Results")
    st.caption("Field by field extraction comparison")
    st.divider()

    # load extracted data from report file
    report_files = glob.glob("reports/benchmark_*.json")
    if report_files:
        with open(sorted(report_files)[-1], "r", encoding="utf-8") as f:
            bench = json.load(f)

        llama_extracted  = bench["results"]["llama-3-groq"]["extracted"]
        gemini_extracted = bench["results"]["gemini-2.5-flash"]["extracted"]

        fields = [
            "title", "published_year", "journal_or_venue",
            "doi", "research_domain", "proposed_model", "methodology"
        ]

        for field in fields:
            llama_val  = llama_extracted.get(field)
            gemini_val = gemini_extracted.get(field)

            agree = str(llama_val).lower() == str(gemini_val).lower()
            # check if both models agreed on this field

            with st.expander(f"{'AGREE' if agree else 'DIFFER'} — {field}"):
                # st.expander() creates a collapsible section
                col_a, col_b = st.columns(2)
                with col_a:
                    st.markdown("**Llama 3 (Groq)**")
                    st.write(llama_val or "null")
                with col_b:
                    st.markdown("**Gemini 2.5 Flash**")
                    st.write(gemini_val or "null")

        # authors
        with st.expander("Authors"):
            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown("**Llama 3 (Groq)**")
                for a in (llama_extracted.get("authors") or []):
                    st.write(f"- {a}")
            with col_b:
                st.markdown("**Gemini 2.5 Flash**")
                for a in (gemini_extracted.get("authors") or []):
                    st.write(f"- {a}")

        # key findings
        with st.expander("Key findings"):
            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown("**Llama 3 (Groq)**")
                for f in (llama_extracted.get("key_findings") or []):
                    st.write(f"- {f}")
            with col_b:
                st.markdown("**Gemini 2.5 Flash**")
                for f in (gemini_extracted.get("key_findings") or []):
                    st.write(f"- {f}")

        # benchmark scores
        with st.expander("Benchmark scores"):
            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown("**Llama 3 (Groq)**")
                for s in (llama_extracted.get("benchmark_scores") or []):
                    st.write(f"- {s}")
            with col_b:
                st.markdown("**Gemini 2.5 Flash**")
                for s in (gemini_extracted.get("benchmark_scores") or []):
                    st.write(f"- {s}")
    else:
        st.warning("No extraction report found. Run the notebook first.")


# ============================================================
# PAGE 3 — RAG Q&A
# ============================================================

elif page == "RAG Q&A":

    st.title("RAG Question Answering")
    st.caption("Both models answer the same questions using retrieved paper chunks")
    st.divider()

    # RAG summary metrics
    r1, r2, r3 = st.columns(3)
    r1.metric("Questions asked",      rag["questions_asked"])
    r2.metric("Llama avg latency",    f"{rag['llama_avg_latency']}s")
    r3.metric("Gemini avg latency",   f"{rag['gemini_avg_latency']}s")

    st.divider()

    # RAG latency chart
    st.subheader("RAG Latency per Question")
    rag_chart_data = {}
    for i, qa in enumerate(rag["qa_pairs"]):
        short_q = f"Q{i+1}"
        rag_chart_data[short_q] = qa["groq_latency"]
    # we only show Llama latency here — Gemini shown in table below

    st.bar_chart(rag_chart_data)

    st.divider()

    # Q&A pairs
    st.subheader("Question by Question Answers")

    for i, qa in enumerate(rag["qa_pairs"]):
        st.markdown(f"**Q{i+1}: {qa['question']}**")

        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("**Llama 3 (Groq)**")
            st.info(qa["groq_answer"])
            # st.info() shows a blue info box
            st.caption(f"Latency: {qa['groq_latency']}s")

        with col_b:
            st.markdown("**Gemini 2.5 Flash**")
            st.info(qa["gemini_answer"])
            st.caption(f"Latency: {qa['gemini_latency']}s")

        st.divider()


# ============================================================
# PAGE 4 — FULL REPORT
# ============================================================

elif page == "Full Report":

    st.title("Full Benchmark Report")
    st.caption("Raw JSON report from the latest benchmark run")
    st.divider()

    st.json(report)
    # st.json() displays a formatted, collapsible JSON viewer

    # download button
    st.download_button(
        label="Download JSON Report",
        data=json.dumps(report, indent=2, ensure_ascii=False),
        file_name=Path(latest_report).name,
        mime="application/json",
        use_container_width=True
    )