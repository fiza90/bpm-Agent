import streamlit as st

from agents.orchestrator import OrchestratorAgent
from agents.mining_agent import MiningAgent



# -----------------------------
# Initialize Agents
# -----------------------------

agent = OrchestratorAgent()

mining_agent = MiningAgent()



# -----------------------------
# Load CSS
# -----------------------------

def load_css():

    with open("styles.css") as f:

        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )



load_css()



# -----------------------------
# Page Header
# -----------------------------

st.markdown(
    """
    <div class="main-title">
    🤖 BPM Agentic AI Assistant
    </div>

    <div class="sub-title">
    Analyze business processes, identify bottlenecks and generate intelligent execution plans.
    </div>
    """,
    unsafe_allow_html=True
)



# =====================================================
# BPM PROCESS ANALYSIS SECTION
# =====================================================


st.markdown(
    '<div class="card">',
    unsafe_allow_html=True
)


query = st.text_area(

    "Describe your process",

    height=150,

    placeholder=
    "Example: Analyze the Source to Pay process and identify bottlenecks..."

)


run = st.button(
    "🚀 Generate Plan"
)


st.markdown(
    "</div>",
    unsafe_allow_html=True
)



if run:


    with st.spinner(
        "🧠 AI Agents are working..."
    ):


        result = agent.execute(query)



    st.success(
        "Plan Generated Successfully"
    )


    st.markdown(
        '<div class="plan-card">',
        unsafe_allow_html=True
    )


    st.subheader(
        "📋 Execution Plan"
    )



    # Response Agent returns text

    if isinstance(result, str):

        st.write(result)



    # Previous dictionary responses

    elif isinstance(result, dict):


        for step, output in result.items():


            st.markdown(
                f"""
                <div class="plan-card">

                <h3>🤖 {step}</h3>

                </div>
                """,
                unsafe_allow_html=True
            )



            if isinstance(output, dict):


                if "bottlenecks" in output:

                    st.markdown(
                        "### ⚠️ Bottlenecks"
                    )

                    for item in output["bottlenecks"]:

                        st.write(
                            "•",
                            item
                        )



                if "recommendations" in output:

                    st.markdown(
                        "### 💡 Recommendations"
                    )

                    for item in output["recommendations"]:

                        st.write(
                            "•",
                            item
                        )


            else:

                st.write(output)



    else:

        st.write(result)



    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )



# =====================================================
# PROCESS MINING SECTION
# =====================================================


st.markdown("---")


st.header(
    "📂 Process Mining Data Analysis"
)



uploaded_file = st.file_uploader(

    "Upload Event Log (CSV/XLSX)",

    type=[
        "csv",
        "xlsx"
    ]

)



if uploaded_file:


    with st.spinner(
        "🔍 Analyzing event log..."
    ):


        mining_result = mining_agent.analyze(

            uploaded_file

        )



    st.success(
        "Event Log Analysis Completed"
    )



    st.subheader(
        "📊 Mining Readiness Report"
    )



    if mining_result["status"] == "completed":


        summary = mining_result["summary"]



        col1, col2, col3, col4 = st.columns(4)



        with col1:

            st.metric(

                "Total Events",

                summary["total_events"]

            )



        with col2:

            st.metric(

                "Total Cases",

                summary["total_cases"]

            )



        with col3:

            st.metric(

                "Activities",

                summary["unique_activities"]

            )



        with col4:

            st.metric(

                "Resources",

                summary["unique_resources"]

            )



        st.markdown(
            "### 📅 Time Range"
        )


        st.write(

            summary["start_date"],

            "to",

            summary["end_date"]

        )



        st.markdown(
            "### ✅ Mining Readiness"
        )


        st.info(

            mining_result["readiness"]

        )



        if mining_result["issues"]:


            st.warning(
                "Issues Found"
            )


            for issue in mining_result["issues"]:

                st.write(
                    "•",
                    issue
                )



        st.markdown(
            "### 🔄 Activity Frequency"
        )


        st.write(

            mining_result["activity_frequency"]

        )



    else:


        st.error(

            mining_result["message"]

        )