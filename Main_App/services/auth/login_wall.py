import streamlit as st
from services.persistence.exercise_repository import get_or_create_user


def render_login_wall():
    if st.session_state.get("user_id") is not None:
        return True

    st.markdown(
        """
        <div class="login-hero">
            <div class="login-badge">💪 AI-POWERED FITNESS COACH</div>
            <h1 class="login-title">AI Real-time <span>GYM Trainer</span></h1>
            <p class="login-sub">
                Real-time pose detection, instant voice coaching, and rep tracking —
                powered entirely by computer vision. No wearables. Just your camera.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            """<div class="login-feature">
                <span class="login-feature-icon">🎯</span>
                <strong>Live Form Correction</strong>
                <p>AI watches every rep and flags bad form instantly.</p>
            </div>""",
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            """<div class="login-feature">
                <span class="login-feature-icon">🔊</span>
                <strong>Voice Coaching</strong>
                <p>Spoken cues the moment your posture breaks down.</p>
            </div>""",
            unsafe_allow_html=True,
        )
    with col3:
        st.markdown(
            """<div class="login-feature">
                <span class="login-feature-icon">📊</span>
                <strong>Progress Tracking</strong>
                <p>Automatic rep counts and full session history.</p>
            </div>""",
            unsafe_allow_html=True,
        )

    st.markdown("<div class='login-form-spacer'></div>", unsafe_allow_html=True)

    _, form_col, _ = st.columns([1, 1.1, 1])
    with form_col:
        st.markdown("<p class='login-form-label'>Enter a username to begin</p>", unsafe_allow_html=True)
        with st.form("login_form", clear_on_submit=False):
            username = st.text_input(
                "Name (unique)",
                placeholder="e.g. anjali_fit",
                label_visibility="collapsed",
            )
            submit_button = st.form_submit_button("Start Session", width="stretch")

    if submit_button:
        if not username:
            st.error("Name cannot be empty.")
            return False

        user = get_or_create_user(username)

        st.session_state["user_id"] = user["id"]
        st.session_state["username"] = user["username"]

        st.rerun()

    return False