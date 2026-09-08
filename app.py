import io
import zipfile
from html import escape

import streamlit as st


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="CodeForge AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>
    /* ========================================================
       GLOBAL
       ======================================================== */

    .stApp {
        background:
            radial-gradient(
                circle at 10% 10%,
                rgba(91, 59, 255, 0.10),
                transparent 25%
            ),
            radial-gradient(
                circle at 90% 0%,
                rgba(34, 211, 238, 0.08),
                transparent 20%
            ),
            #07111f;
        color: #f8fafc;
    }

    .main .block-container {
        max-width: 1500px;
        padding-top: 1.2rem;
        padding-bottom: 2rem;
    }


    /* ========================================================
       SIDEBAR
       ======================================================== */

    [data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #07101d 0%,
                #0b1527 100%
            );
        border-right: 1px solid rgba(255,255,255,0.08);
    }

    .sidebar-brand {
        padding: 0.5rem 0.2rem 1.2rem 0.2rem;
        border-bottom: 1px solid rgba(255,255,255,0.08);
        margin-bottom: 1rem;
    }

    .sidebar-brand-title {
        font-size: 1.25rem;
        font-weight: 800;
        color: white;
    }

    .sidebar-brand-title span {
        color: #8b5cf6;
    }

    .sidebar-subtitle {
        color: #94a3b8;
        font-size: 0.78rem;
        margin-top: 0.2rem;
    }


    /* ========================================================
       HEADER
       ======================================================== */

    .top-header {
        padding: 0.25rem 0 1rem 0;
    }

    .brand-title {
        font-size: 2.8rem;
        font-weight: 850;
        letter-spacing: -1.5px;
        color: white;
        line-height: 1;
    }

    .brand-title span {
        color: #8b5cf6;
    }

    .brand-subtitle {
        margin-top: 0.35rem;
        font-size: 1rem;
        color: #cbd5e1;
    }

    .header-flow {
        text-align: right;
        color: #dbeafe;
        font-size: 0.95rem;
        font-weight: 600;
        padding-top: 1.2rem;
    }

    .header-flow span {
        color: #8b5cf6;
        padding: 0 0.45rem;
    }


    /* ========================================================
       CARDS
       ======================================================== */

    .card {
        background: rgba(255,255,255,0.96);
        color: #172033;
        border-radius: 14px;
        padding: 1rem 1.1rem;
        border: 1px solid #dbe4f0;
        box-shadow: 0 8px 30px rgba(2, 8, 23, 0.16);
        margin-bottom: 1rem;
    }


    /* ========================================================
       SECTION TITLES
       ======================================================== */

    .section-title {
        font-size: 1.08rem;
        font-weight: 850;
        margin-bottom: 0.65rem;
        color: #111827 !important;
        background: #f8fafc;
        padding: 0.45rem 0.55rem;
        border-radius: 8px;
    }

    .section-title-dark {
        color: #ffffff !important;
        background: transparent !important;
    }

    .section-number {
        color: #4f46e5;
        margin-right: 0.35rem;
    }


    /* ========================================================
       TABS
       ======================================================== */

    button[data-baseweb="tab"] {
        color: #334155 !important;
        font-weight: 700 !important;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        color: #4f46e5 !important;
        font-weight: 800 !important;
    }

    button[data-baseweb="tab"] p {
        color: inherit !important;
    }


    /* ========================================================
       AGENT CARDS
       ======================================================== */

    .agent-card {
        background: rgba(255,255,255,0.97);
        border: 1px solid #dbe4f0;
        border-radius: 12px;
        padding: 0.8rem 0.9rem;
        min-height: 88px;
        box-shadow: 0 6px 20px rgba(2, 8, 23, 0.10);
    }

    .agent-name {
        font-weight: 800;
        font-size: 0.96rem;
        color: #111827;
    }

    .agent-status {
        font-size: 0.78rem;
        margin-top: 0.18rem;
    }


    /* ========================================================
       REQUIREMENTS
       ======================================================== */

    .requirement-item {
        padding: 0.35rem 0;
        border-bottom: 1px solid #eef2f7;
        font-size: 0.92rem;
    }

    .requirement-item:last-child {
        border-bottom: none;
    }


    /* ========================================================
       ARCHITECTURE
       ======================================================== */

    .arch-box {
        border: 1px solid #dbe4f0;
        border-radius: 10px;
        padding: 0.75rem;
        text-align: center;
        background: #f8fafc;
        font-weight: 700;
    }

    .arch-arrow {
        text-align: center;
        font-size: 1.3rem;
        color: #4f46e5;
        padding: 0.25rem 0;
    }


    /* ========================================================
       FILE TREE
       ======================================================== */

    .file-tree {
        background: #0a0f18;
        color: #e5e7eb;
        border-radius: 10px;
        padding: 1rem;
        font-family: Consolas, monospace;
        font-size: 0.82rem;
        line-height: 1.65;
        min-height: 340px;
        overflow-x: auto;
        white-space: pre-wrap;
    }


    /* ========================================================
       READY BOX
       ======================================================== */

    .ready-box {
        background:
            linear-gradient(
                135deg,
                #ecfdf5 0%,
                #f0fdf4 100%
            );
        border: 1px solid #bbf7d0;
        border-radius: 14px;
        padding: 1rem;
        color: #14532d;
        margin-top: 1rem;
    }

    .ready-title {
        font-size: 1.05rem;
        font-weight: 800;
        margin-bottom: 0.35rem;
    }


    /* ========================================================
       DEMO MODE
       ======================================================== */

    .demo-label {
        display: inline-block;
        background: #ede9fe;
        color: #5b21b6;
        border-radius: 999px;
        padding: 0.25rem 0.65rem;
        font-size: 0.72rem;
        font-weight: 800;
        margin-bottom: 0.7rem;
    }


    /* ========================================================
       FOOTER
       ======================================================== */

    .footer-note {
        text-align: center;
        color: #94a3b8;
        font-size: 0.84rem;
        padding: 1rem 0 0.2rem 0;
    }


    /* ========================================================
       STREAMLIT WIDGETS
       ======================================================== */

    div[data-testid="stTextArea"] textarea,
    div[data-testid="stTextInput"] input,
    div[data-testid="stSelectbox"] > div {
        border-radius: 10px;
    }

    button[kind="primary"],
    button[kind="secondary"] {
        border-radius: 10px;
        font-weight: 800;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SESSION STATE
# ============================================================

DEFAULTS = {
    "project_idea": "",
    "workflow_started": False,
    "clarification_needed": False,
    "demo_mode": False,
    "feedback_type": "UI",
    "feedback_message": "",
    "clarification_answers": {},
    "agent_status": {
        "Requirement Agent": "Waiting",
        "Architect Agent": "Waiting",
        "Developer Agent": "Waiting",
        "Testing Agent": "Waiting",
    },
}

for key, value in DEFAULTS.items():
    if key not in st.session_state:
        if isinstance(value, dict):
            st.session_state[key] = value.copy()
        else:
            st.session_state[key] = value


# ============================================================
# REAL-WORKFLOW PLACEHOLDERS
# ============================================================
# These remain empty until the real agents are connected.
# They are intentionally NOT populated with fake hospital data.

PLACEHOLDER_RESULTS = {
    "requirements": {
        "functional": [],
        "non_functional": [],
        "roles": [],
        "srs": "",
    },
    "architecture": {
        "frontend": "",
        "backend": "",
        "database": "",
        "authentication": "",
        "deployment": "",
    },
    "database": [],
    "api_endpoints": [],
    "project_structure": "",
    "code": {
        "backend": "",
        "frontend": "",
        "database_models": "",
    },
    "readme": "",
    "tests": [],
}


# ============================================================
# DEMO DATA
# ============================================================
# This data exists ONLY to demonstrate the UI.
# It is never presented as real AI output.

DEMO_RESULTS = {
    "requirements": {
        "functional": [
            "Patient registration and profile management",
            "Doctor management",
            "Appointment scheduling and cancellation",
            "Medical record management",
            "Prescription management",
            "Billing and payment handling",
            "Admin dashboard",
            "Role-based authentication",
        ],
        "non_functional": [
            "Responsive web interface",
            "Secure authentication",
            "Reliable data storage",
            "Maintainable modular architecture",
            "Fast API response time",
        ],
        "roles": [
            "Administrator",
            "Doctor",
            "Patient",
        ],
        "srs": """Project: Hospital Management System

Purpose:
Manage patients, doctors, appointments and medical records.

Core modules:
- Patient management
- Doctor management
- Appointment scheduling
- Medical records
- Prescriptions
- Billing
- Authentication

Target:
A modular web-based starter application.""",
    },
    "architecture": {
        "frontend": "React + Vite",
        "backend": "FastAPI (Python)",
        "database": "PostgreSQL",
        "authentication": "JWT / Role-based",
        "deployment": "Optional Docker + Render/Railway",
    },
    "database": [
        "users",
        "patients",
        "doctors",
        "appointments",
        "medical_records",
        "prescriptions",
        "billing",
    ],
    "api_endpoints": [
        "POST /api/patients",
        "GET /api/patients",
        "POST /api/doctors",
        "GET /api/doctors",
        "POST /api/appointments",
        "GET /api/appointments",
    ],
    "project_structure": """hospital-management-system/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   └── routes/
│   │       ├── patients.py
│   │       ├── doctors.py
│   │       └── appointments.py
│   └── database.py
├── frontend/
│   └── src/
│       ├── components/
│       └── pages/
├── requirements.txt
└── README.md""",
    "code": {
        "backend": """from fastapi import FastAPI

app = FastAPI(title="Hospital Management System")

@app.get("/")
def read_root():
    return {
        "message": "Welcome to Hospital Management System API"
    }""",
        "frontend": """function Dashboard() {
    return (
        <main>
            <h1>Hospital Dashboard</h1>
            <p>Manage patients and appointments.</p>
        </main>
    );
}""",
        "database_models": """class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    phone = Column(String)
    email = Column(String)""",
    },
    "readme": """# Hospital Management System

Generated by CodeForge AI — Demo Preview.

## Features
- Patient management
- Doctor management
- Appointment scheduling
- Medical records
- Role-based authentication

## Technology Stack
- Frontend: React
- Backend: FastAPI
- Database: PostgreSQL

This is demonstration data for the CodeForge AI UI.""",
    "tests": [
        ("✅", "Patient API", "Passed"),
        ("✅", "Doctor API", "Passed"),
        ("✅", "Appointment API", "Passed"),
        ("❌", "Invalid Input", "Failed"),
    ],
}


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def reset_project() -> None:
    """Reset all CodeForge UI state."""
    st.session_state.project_idea = ""
    st.session_state.workflow_started = False
    st.session_state.clarification_needed = False
    st.session_state.demo_mode = False
    st.session_state.feedback_type = "UI"
    st.session_state.feedback_message = ""
    st.session_state.clarification_answers = {}

    st.session_state.agent_status = {
        "Requirement Agent": "Waiting",
        "Architect Agent": "Waiting",
        "Developer Agent": "Waiting",
        "Testing Agent": "Waiting",
    }

    # Clear clarification widget values from previous runs.
    for key in (
        "q_users",
        "q_features",
        "q_app_type",
        "q_tech",
    ):
        if key in st.session_state:
            del st.session_state[key]


def set_agent_statuses(
    *,
    started: bool = False,
    demo: bool = False,
) -> None:
    """Set UI-only agent status placeholders."""
    if demo:
        st.session_state.agent_status = {
            "Requirement Agent": "Completed",
            "Architect Agent": "Completed",
            "Developer Agent": "Completed",
            "Testing Agent": "Completed",
        }
        return

    if started:
        st.session_state.agent_status = {
            "Requirement Agent": "Ready",
            "Architect Agent": "Waiting",
            "Developer Agent": "Waiting",
            "Testing Agent": "Waiting",
        }
        return

    st.session_state.agent_status = {
        "Requirement Agent": "Waiting",
        "Architect Agent": "Waiting",
        "Developer Agent": "Waiting",
        "Testing Agent": "Waiting",
    }


def get_results():
    """
    Return demo content only in demo mode.
    Real workflow remains empty until the agents are connected.
    """
    if st.session_state.demo_mode:
        return DEMO_RESULTS

    return PLACEHOLDER_RESULTS


def status_icon(status: str) -> str:
    return {
        "Waiting": "⚪",
        "Ready": "🟡",
        "Running": "🔵",
        "Completed": "✅",
        "Failed": "❌",
    }.get(status, "⚪")


def status_color(status: str) -> str:
    return {
        "Waiting": "#64748b",
        "Ready": "#a16207",
        "Running": "#2563eb",
        "Completed": "#059669",
        "Failed": "#dc2626",
    }.get(status, "#64748b")


def build_demo_zip() -> bytes:
    """
    Create a tiny valid ZIP used only for UI demonstration.
    This is NOT the final project-generation mechanism.
    """
    buffer = io.BytesIO()

    with zipfile.ZipFile(
        buffer,
        mode="w",
        compression=zipfile.ZIP_DEFLATED,
    ) as archive:
        archive.writestr(
            "README.txt",
            (
                "CodeForge AI Phase 3 Demo Preview\n\n"
                "This ZIP contains demonstration content only.\n"
                "It is not AI-generated project output.\n"
            ),
        )

    return buffer.getvalue()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.markdown(
        """
        <div class="sidebar-brand">
            <div class="sidebar-brand-title">
                ◈ CodeForge <span>AI</span>
            </div>
            <div class="sidebar-subtitle">
                Software Project Planning Assistant
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### 📁 Navigation")

    st.button(
        "🆕 New Project",
        use_container_width=True,
    )

    st.button(
        "📂 Projects",
        use_container_width=True,
    )

    st.button(
        "🔗 Agent Workflow",
        use_container_width=True,
    )

    st.button(
        "⚙️ Settings",
        use_container_width=True,
    )

    st.markdown("---")

    st.markdown("### 🧪 UI Testing")

    if st.button(
        "Load Demo Project",
        use_container_width=True,
    ):
        st.session_state.demo_mode = True
        st.session_state.workflow_started = True
        st.session_state.clarification_needed = False
        st.session_state.project_idea = (
            "Build a Hospital Management System for managing "
            "patients, doctors, appointments, and medical records."
        )
        set_agent_statuses(demo=True)
        st.rerun()

    if st.button(
        "Load Clarification Demo",
        use_container_width=True,
    ):
        st.session_state.demo_mode = True
        st.session_state.workflow_started = True
        st.session_state.clarification_needed = True
        st.session_state.project_idea = (
            "Build a Hospital Management System."
        )
        set_agent_statuses(started=True)
        st.rerun()

    if st.button(
        "Reset Project",
        use_container_width=True,
    ):
        reset_project()
        st.rerun()


# ============================================================
# HEADER
# ============================================================

header_left, header_right = st.columns([2.2, 1])

with header_left:
    st.markdown(
        """
        <div class="top-header">
            <div class="brand-title">
                CodeForge <span>AI</span>
            </div>
            <div class="brand-subtitle">
                A Multi-Agent Software Project Planning and
                Code Generation Assistant
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with header_right:
    st.markdown(
        """
        <div class="header-flow">
            Your Idea <span>→</span>
            Project Plan <span>→</span>
            Starter Code
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# DEMO MODE INDICATOR
# ============================================================

if st.session_state.demo_mode:
    st.markdown(
        '<span class="demo-label">'
        "DEMO PREVIEW — sample data only"
        "</span>",
        unsafe_allow_html=True,
    )


# ============================================================
# 1. USER INPUT
# ============================================================

st.markdown(
    '<div class="card">',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="section-title">'
    '<span class="section-number">1.</span>'
    "💡 User Input"
    "</div>",
    unsafe_allow_html=True,
)

project_idea = st.text_area(
    "Describe the software you want to build",
    value=st.session_state.project_idea,
    placeholder=(
        "Example: Build a Hospital Management System for "
        "patients, doctors, appointments and medical records."
    ),
    height=90,
    label_visibility="collapsed",
)

generate_col1, generate_col2 = st.columns([3, 1])

with generate_col2:
    generate_clicked = st.button(
        "✨ Generate with AI",
        type="primary",
        use_container_width=True,
    )

if generate_clicked:
    if not project_idea.strip():
        st.error("Please enter a software idea first.")
    else:
        st.session_state.project_idea = project_idea.strip()

        # Normal generation mode.
        st.session_state.demo_mode = False
        st.session_state.workflow_started = True

        # The REAL Requirement Agent will decide whether
        # clarification is needed in a later phase.
        st.session_state.clarification_needed = False

        set_agent_statuses(started=True)

        st.info(
            "Project idea captured successfully. "
            "The Requirement Agent will analyze completeness "
            "once the real AI workflow is connected."
        )

st.markdown(
    "</div>",
    unsafe_allow_html=True,
)


# ============================================================
# REQUIREMENT CLARIFICATION
# ============================================================

if st.session_state.clarification_needed:
    st.markdown(
        '<div class="card">',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-title">'
        "⚠️ More Information Required"
        "</div>",
        unsafe_allow_html=True,
    )

    st.write(
        "The Requirement Agent has identified that additional "
        "information is required before reliable requirements "
        "can be generated."
    )

    q1, q2 = st.columns(2)

    with q1:
        st.text_input(
            "Who are the primary users?",
            placeholder="Example: Admin, doctors, patients",
            key="q_users",
        )

    with q2:
        st.text_input(
            "What major features are required?",
            placeholder=(
                "Example: appointments, medical records, billing"
            ),
            key="q_features",
        )

    q3, q4 = st.columns(2)

    with q3:
        st.selectbox(
            "Application type",
            [
                "Web Application",
                "Mobile Application",
                "Desktop Application",
            ],
            key="q_app_type",
        )

    with q4:
        st.text_input(
            "Technology/database preference",
            placeholder="Optional",
            key="q_tech",
        )

    if st.button(
        "➡️ Submit Answers",
        type="primary",
    ):
        st.session_state.clarification_answers = {
            "users": st.session_state.get("q_users", ""),
            "features": st.session_state.get("q_features", ""),
            "application_type": st.session_state.get(
                "q_app_type",
                "",
            ),
            "technology": st.session_state.get(
                "q_tech",
                "",
            ),
        }

        st.session_state.clarification_needed = False
        st.session_state.workflow_started = True
        st.session_state.demo_mode = False

        set_agent_statuses(started=True)

        st.success(
            "Answers recorded. The real Requirement Agent "
            "will process them after Gemini and CrewAI are connected."
        )

    st.markdown(
        "</div>",
        unsafe_allow_html=True,
    )

    # Prevent result cards from appearing while clarification
    # is still the active interaction.
    st.stop()


# ============================================================
# 2. AGENT WORKFLOW
# ============================================================

st.markdown(
    '<div class="section-title section-title-dark" '
    'style="margin-top:0.4rem;">'
    "🤖 Agent Workflow"
    "</div>",
    unsafe_allow_html=True,
)

agent_columns = st.columns(4)

for column, (name, status) in zip(
    agent_columns,
    st.session_state.agent_status.items(),
):
    with column:
        icon = status_icon(status)
        color = status_color(status)

        st.markdown(
            f"""
            <div class="agent-card">
                <div style="font-size:1.35rem;">{icon}</div>
                <div class="agent-name">{name}</div>
                <div class="agent-status" style="color:{color};">
                    {status}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ============================================================
# OUTPUT AREA
# ============================================================

if not st.session_state.workflow_started:
    st.markdown(
        '<div class="card">',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-title">'
        "🚀 Ready to Build"
        "</div>",
        unsafe_allow_html=True,
    )

    st.write(
        "Enter a software idea above and click "
        "**Generate with AI** to begin."
    )

    st.caption(
        "The result panels are placeholders during Phase 3. "
        "Real agent-generated content will be connected in later phases."
    )

    st.markdown(
        "</div>",
        unsafe_allow_html=True,
    )

else:
    results = get_results()

    # ========================================================
    # 3. REQUIREMENTS
    # ========================================================

    left_col, middle_col, right_col = st.columns(
        [1.15, 1.15, 0.85]
    )

    with left_col:
        st.markdown(
            '<div class="card">',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="section-title">'
            '<span class="section-number">2.</span>'
            "📋 Requirements"
            "</div>",
            unsafe_allow_html=True,
        )

        req_tab1, req_tab2, req_tab3, req_tab4 = st.tabs(
            [
                "Functional",
                "Non-Functional",
                "User Roles",
                "SRS",
            ]
        )

        with req_tab1:
            items = results["requirements"]["functional"]

            if items:
                for item in items:
                    st.markdown(
                        f'<div class="requirement-item">'
                        f"• {item}"
                        f"</div>",
                        unsafe_allow_html=True,
                    )
            else:
                st.info(
                    "Waiting for the Requirement Agent."
                )

        with req_tab2:
            items = results["requirements"]["non_functional"]

            if items:
                for item in items:
                    st.markdown(
                        f'<div class="requirement-item">'
                        f"• {item}"
                        f"</div>",
                        unsafe_allow_html=True,
                    )
            else:
                st.info(
                    "Waiting for non-functional requirements."
                )

        with req_tab3:
            items = results["requirements"]["roles"]

            if items:
                for item in items:
                    st.markdown(
                        f'<div class="requirement-item">'
                        f"• {item}"
                        f"</div>",
                        unsafe_allow_html=True,
                    )
            else:
                st.info(
                    "Waiting for identified user roles."
                )

        with req_tab4:
            srs = results["requirements"]["srs"]

            if srs:
                st.code(
                    srs,
                    language="text",
                )
            else:
                st.info(
                    "The SRS will appear after the "
                    "Requirement Agent completes its task."
                )

        st.markdown(
            "</div>",
            unsafe_allow_html=True,
        )


    # ========================================================
    # 4. ARCHITECTURE
    # ========================================================

    with middle_col:
        st.markdown(
            '<div class="card">',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="section-title">'
            '<span class="section-number">3.</span>'
            "🏗️ System Architecture"
            "</div>",
            unsafe_allow_html=True,
        )

        arch_tab1, arch_tab2, arch_tab3, arch_tab4 = st.tabs(
            [
                "Tech Stack",
                "Architecture",
                "Database",
                "API Endpoints",
            ]
        )

        with arch_tab1:
            architecture = results["architecture"]

            visible_items = {
                key: value
                for key, value in architecture.items()
                if value
            }

            if visible_items:
                for key, value in visible_items.items():
                    st.markdown(
                        f"**{key.title()}** : {value}"
                    )
            else:
                st.info(
                    "Waiting for the Architect Agent."
                )

        with arch_tab2:
            architecture = results["architecture"]

            if (
                architecture.get("frontend")
                and architecture.get("backend")
                and architecture.get("database")
            ):
                st.markdown(
                    """
                    <div class="arch-box">
                        👤 User / Web App
                    </div>
                    <div class="arch-arrow">↓</div>
                    <div class="arch-box">
                        ⚛️ Frontend — React
                    </div>
                    <div class="arch-arrow">↓</div>
                    <div class="arch-box">
                        ⚡ Backend — FastAPI
                    </div>
                    <div class="arch-arrow">↓</div>
                    <div class="arch-box">
                        🗄️ Database
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                st.info(
                    "Architecture diagram will appear after "
                    "design generation."
                )

        with arch_tab3:
            tables = results["database"]

            if tables:
                st.markdown("**Tables**")

                for table in tables:
                    st.markdown(
                        f"- {table}"
                    )
            else:
                st.info(
                    "Database schema will appear here."
                )

        with arch_tab4:
            endpoints = results["api_endpoints"]

            if endpoints:
                for endpoint in endpoints:
                    st.markdown(
                        f"`{endpoint}`"
                    )
            else:
                st.info(
                    "API endpoints will appear here."
                )

        st.markdown(
            "</div>",
            unsafe_allow_html=True,
        )


    # ========================================================
    # 5. PROJECT STRUCTURE
    # ========================================================

    with right_col:
        st.markdown(
            '<div class="card">',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="section-title">'
            '<span class="section-number">4.</span>'
            "📁 Project Structure"
            "</div>",
            unsafe_allow_html=True,
        )

        project_structure = results["project_structure"]

        if project_structure:
            safe_structure = escape(
                project_structure
            )

            st.markdown(
                f'<div class="file-tree">'
                f"{safe_structure}"
                f"</div>",
                unsafe_allow_html=True,
            )
        else:
            st.info(
                "The Architect Agent will generate the "
                "project structure here."
            )

        if st.session_state.demo_mode:
            st.download_button(
                "⬇️ Download Demo ZIP",
                data=build_demo_zip(),
                file_name="codeforge-ai-demo-preview.zip",
                mime="application/zip",
                use_container_width=True,
            )
        else:
            st.button(
                "⬇️ Download Project",
                disabled=True,
                use_container_width=True,
                help=(
                    "Enabled after the real project-generation "
                    "tool is implemented."
                ),
            )

        st.markdown(
            "</div>",
            unsafe_allow_html=True,
        )


    # ========================================================
    # 6. GENERATED CODE
    # ========================================================

    code_col, readme_col = st.columns(
        [1.15, 1]
    )

    with code_col:
        st.markdown(
            '<div class="card">',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="section-title">'
            '<span class="section-number">5.</span>'
            "💻 Generated Code"
            "</div>",
            unsafe_allow_html=True,
        )

        code_tab1, code_tab2, code_tab3 = st.tabs(
            [
                "Backend (FastAPI)",
                "Frontend (React)",
                "Database Models",
            ]
        )

        with code_tab1:
            backend_code = results["code"]["backend"]

            if backend_code:
                st.code(
                    backend_code,
                    language="python",
                )
            else:
                st.info(
                    "Developer Agent backend code "
                    "will appear here."
                )

        with code_tab2:
            frontend_code = results["code"]["frontend"]

            if frontend_code:
                st.code(
                    frontend_code,
                    language="javascript",
                )
            else:
                st.info(
                    "Developer Agent frontend code "
                    "will appear here."
                )

        with code_tab3:
            database_code = (
                results["code"]["database_models"]
            )

            if database_code:
                st.code(
                    database_code,
                    language="python",
                )
            else:
                st.info(
                    "Database model code will appear here."
                )

        st.markdown(
            "</div>",
            unsafe_allow_html=True,
        )


    # ========================================================
    # 7. README & SETUP
    # ========================================================

    with readme_col:
        st.markdown(
            '<div class="card">',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="section-title">'
            '<span class="section-number">6.</span>'
            "📄 README & Setup"
            "</div>",
            unsafe_allow_html=True,
        )

        readme_tab1, readme_tab2, readme_tab3 = st.tabs(
            [
                "README",
                "Setup Steps",
                "Run Commands",
            ]
        )

        with readme_tab1:
            readme = results["readme"]

            if readme:
                st.code(
                    readme,
                    language="markdown",
                )
            else:
                st.info(
                    "README will be generated with "
                    "the final project."
                )

        with readme_tab2:
            st.markdown(
                """
                **1. Create the generated project folder**

                **2. Install the selected dependencies**

                **3. Configure environment variables**

                **4. Start the generated application**

                **5. Run the generated test suite**
                """
            )

        with readme_tab3:
            st.info(
                "Run commands will be generated by the "
                "Developer Agent based on the selected stack."
            )

        st.markdown(
            "</div>",
            unsafe_allow_html=True,
        )


    # ========================================================
    # 8. TEST RESULTS
    # ========================================================

    st.markdown(
        '<div class="card">',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-title">'
        '<span class="section-number">7.</span>'
        "🧪 Test Results"
        "</div>",
        unsafe_allow_html=True,
    )

    tests = results["tests"]

    if tests:
        test_columns = st.columns(
            len(tests)
        )

        for column, (icon, name, status) in zip(
            test_columns,
            tests,
        ):
            with column:
                color = (
                    "#059669"
                    if status == "Passed"
                    else "#dc2626"
                )

                st.markdown(
                    f"""
                    <div class="agent-card">
                        <div style="font-size:1.2rem;">
                            {icon}
                        </div>
                        <div class="agent-name">
                            {name}
                        </div>
                        <div class="agent-status"
                             style="color:{color};">
                            {status}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        passed = sum(
            status == "Passed"
            for _, _, status in tests
        )

        st.markdown(
            f"<p><strong>Demo summary:</strong> "
            f"{passed} passed / "
            f"{len(tests) - passed} failed</p>",
            unsafe_allow_html=True,
        )

        st.warning(
            "These are demo-only results. Actual test "
            "execution will be implemented by the "
            "Testing Agent later."
        )
    else:
        st.info(
            "No tests have been executed yet. "
            "The Testing Agent will populate this section."
        )

    st.markdown(
        "</div>",
        unsafe_allow_html=True,
    )


    # ========================================================
    # 9. USER FEEDBACK / REFINEMENT
    # ========================================================

    st.markdown(
        '<div class="card">',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-title">'
        "🔄 Refine Output"
        "</div>",
        unsafe_allow_html=True,
    )

    ref_col1, ref_col2 = st.columns(
        [1, 2]
    )

    with ref_col1:
        feedback_type = st.selectbox(
            "What do you want to change?",
            [
                "Requirements",
                "Architecture",
                "Database",
                "APIs",
                "UI",
                "Code",
                "Documentation",
                "Custom Feedback",
            ],
            index=4,
        )

    with ref_col2:
        feedback = st.text_input(
            "Describe your changes",
            value=st.session_state.feedback_message,
            placeholder=(
                "Example: Make the hospital dashboard "
                "simpler with sidebar navigation."
            ),
        )

    if st.button(
        "🔄 Regenerate",
        type="primary",
    ):
        if not feedback.strip():
            st.error(
                "Please enter feedback before regenerating."
            )
        else:
            st.session_state.feedback_type = feedback_type
            st.session_state.feedback_message = (
                feedback.strip()
            )

            st.info(
                f"Feedback captured for **{feedback_type}**. "
                "The relevant agent will process it once "
                "the refinement workflow is connected."
            )

    st.markdown(
        "</div>",
        unsafe_allow_html=True,
    )


    # ========================================================
    # 10. FINAL PROJECT
    # ========================================================

    st.markdown(
        """
        <div class="ready-box">
            <div class="ready-title">
                📦 Final Project
            </div>
            <div>
                This area will contain the final validated
                project package after the complete
                Requirement → Architecture → Development
                → Testing workflow is connected.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.button(
        "⬇️ Download Final Project Package",
        disabled=True,
        use_container_width=True,
        help=(
            "Enabled after actual project generation "
            "and packaging are implemented."
        ),
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer-note">
        “Turning ideas into reality, one agent at a time.” —
        <strong>CodeForge AI</strong>
    </div>
    """,
    unsafe_allow_html=True,
)