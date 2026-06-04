# app/utils/session.py
"""
Lightweight user-identity helpers for Streamlit.

No real authentication — just a username that the user types into the sidebar.
All DB queries are scoped to this username so teammates don't see each other's
data sources or scan reports.
"""
import streamlit as st

_SESSION_KEY = "current_user"


def get_current_user() -> str | None:
    """
    Return the logged-in username from session state, or None if not set.
    All pages should call this and gate access behind it.
    """
    return st.session_state.get(_SESSION_KEY)


def set_current_user(username: str):
    """Persist username into session state."""
    st.session_state[_SESSION_KEY] = username.strip()


def clear_current_user():
    """Log out — clear username from session state."""
    st.session_state.pop(_SESSION_KEY, None)


def require_login():
    """
    If no user is logged in, show a blocking login prompt and stop execution.
    Call this at the top of every page (after set_page_config).
    Returns the username string when logged in.
    """
    user = get_current_user()
    if not user:
        import textwrap
        st.markdown(textwrap.dedent("""
        <div style="
          max-width:420px; margin:80px auto; padding:40px 32px;
          background:#141414; border:1px solid #2A2A2A; border-radius:6px;
          text-align:center;
        ">
          <div style="font-family:'Space Mono',monospace;font-size:14px;color:#E8A838;
                      letter-spacing:0.2em;text-transform:uppercase;margin-bottom:20px">
            COMPLIANCE SCANNER
          </div>
          <div style="font-family:'Space Mono',monospace;font-size:22px;font-weight:700;
                      color:#F0EDE6;margin-bottom:6px">
            IDENTIFY YOURSELF
          </div>
          <div style="font-family:'DM Sans',sans-serif;font-size:15px;color:#7A7A7A;
                      margin-bottom:28px">
            Enter a username to access your private workspace.<br>
            Data is isolated per user — your teammates won't see yours.
          </div>
        </div>
        """), unsafe_allow_html=True)

        col_l, col_m, col_r = st.columns([1, 2, 1])
        with col_m:
            with st.form("login_form", clear_on_submit=False):
                username_input = st.text_input(
                    "Username",
                    placeholder="e.g. alice, bob, team-alpha",
                    label_visibility="collapsed",
                )
                submitted = st.form_submit_button(
                    "⬡  ENTER WORKSPACE",
                    type="primary",
                    use_container_width=True,
                )

            if submitted:
                if username_input.strip():
                    set_current_user(username_input.strip())
                    st.rerun()
                else:
                    st.error("Username cannot be empty.")

        st.stop()
    return user
