import streamlit as st

st.set_page_config(page_title="Responsible AI Use Checkpoint", layout="wide")

# -----------------------------
# Styling (bigger type + clearer hierarchy)
# -----------------------------
CSS = """
<style>
  /* Page width + base typography */
  .block-container { max-width: 1200px; padding-top: 1.4rem; }
  html, body, [class*="css"]  { font-size: 18px; }

  h1 { font-weight: 780; letter-spacing: -0.03em; margin-bottom: 0.25rem; }
  .subtle { color: rgba(49,51,63,0.68); font-size: 1.02rem; line-height: 1.35; }

  /* Make radio text larger */
  div[role="radiogroup"] label { font-size: 1.02rem !important; }
  div[role="radiogroup"] p { font-size: 1.05rem !important; }

  /* Cards */
  .card {
    border: 1px solid rgba(49,51,63,0.10);
    border-radius: 18px;
    padding: 18px 18px 14px 18px;
    background: white;
    box-shadow: 0 10px 34px rgba(0,0,0,0.05);
    margin-bottom: 14px;
  }

  .banner {
    border-radius: 18px;
    padding: 16px 16px 14px 16px;
    border: 1px solid rgba(49,51,63,0.10);
    box-shadow: 0 10px 34px rgba(0,0,0,0.05);
    margin-bottom: 14px;
  }
  .bg-green  { background: rgba(26,127,55,0.07); }
  .bg-yellow { background: rgba(183,129,3,0.09); }
  .bg-red    { background: rgba(180,35,24,0.09); }

  .tier-green  { color: #1a7f37; font-weight: 780; }
  .tier-yellow { color: #b78103; font-weight: 780; }
  .tier-red    { color: #b42318; font-weight: 780; }

  .tier-title { font-size: 1.18rem; margin: 0; }
  .tier-desc { margin-top: 8px; color: rgba(49,51,63,0.72); font-size: 1.00rem; line-height: 1.35; }

  .section-title { font-size: 1.08rem; font-weight: 780; margin-bottom: 0.55rem; }

  /* Tags (bigger + more readable) */
  .tag {
    display:inline-block;
    padding: 7px 12px;
    border-radius: 999px;
    border: 1px solid rgba(49,51,63,0.16);
    background: rgba(49,51,63,0.03);
    margin-right: 10px;
    margin-bottom: 10px;
    font-size: 0.98rem;
    line-height: 1.15;
  }

  .item { margin: 0.30rem 0 0.70rem 0; }
  .item small { color: rgba(49,51,63,0.68); display:block; margin-top: 4px; font-size: 0.98rem; line-height: 1.25; }

  .note {
    margin-top: 10px;
    padding: 10px 12px;
    border-radius: 14px;
    border: 1px dashed rgba(49,51,63,0.18);
    background: rgba(49,51,63,0.02);
    color: rgba(49,51,63,0.78);
    font-size: 0.98rem;
    line-height: 1.30;
  }
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# -----------------------------
# Title
# -----------------------------
st.title("Responsible AI Use Checkpoint")
st.markdown(
    '<div class="subtle">A lightweight <b>decision-support</b> interface that translates responsible AI principles into context-sensitive governance actions. (No numeric score is shown.)</div>',
    unsafe_allow_html=True,
)
st.divider()

# -----------------------------
# Helpers
# -----------------------------
def sev(choice_key: str) -> int:
    # A/B/C -> 0/1/2
    return {"A": 0, "B": 1, "C": 2}[choice_key]

def review_strength(choice_key: str) -> int:
    # A thorough -> 2, B basic -> 1, C minimal -> 0
    return {"A": 2, "B": 1, "C": 0}[choice_key]

def radio_abc(question: str, A: str, B: str, C: str, key: str) -> str:
    return st.radio(
        question,
        options=["A", "B", "C"],
        format_func=lambda k: {"A": f"A — {A}", "B": f"B — {B}", "C": f"C — {C}"}[k],
        key=key,
    )

def tier_from_internal(R: int) -> str:
    # Internal thresholds for 0–2 coding (typical R range ~0–14)
    if R <= 4:
        return "green"
    if R <= 8:
        return "yellow"
    return "red"

def tier_label(tier: str, override: bool) -> str:
    if tier == "green":
        return "🟢 Tier 1 — Standard governance sufficient"
    if tier == "yellow":
        return "🟡 Tier 2 — Enhanced governance recommended"
    return "🔴 Tier 3 — Formal governance required (override)" if override else "🔴 Tier 3 — Formal governance required"

def banner_html(tier: str, override: bool) -> str:
    if tier == "green":
        bg = "bg-green"
        cls = "tier-green"
    elif tier == "yellow":
        bg = "bg-yellow"
        cls = "tier-yellow"
    else:
        bg = "bg-red"
        cls = "tier-red"

    text = tier_label(tier, override)
    return f"""
<div class="banner {bg}">
  <div class="tier-title {cls}">{text}</div>
  <div class="tier-desc">
    Tier is determined from <b>consequence</b>, <b>exposure</b>, and <b>review strength</b>.
    The internal index is used only to select governance actions (not shown as a score).
  </div>
</div>
"""

# -----------------------------
# Layout
# -----------------------------
left, right = st.columns([1.35, 1])

# -----------------------------
# Questions
# -----------------------------
with left:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Assessment</div>', unsafe_allow_html=True)

    q1 = radio_abc(
        "Q1. What is the level of institutional authority or liability exposure associated with this content?",
        "Personal / Low institutional impact",
        "Embedded in institutional role (e.g., teaching communication, internal coordination)",
        "Official institutional representation (policy, compliance, formal decision)",
        "q1",
    )

    q2 = radio_abc(
        "Q2. If factual or regulatory errors occur in this content, how severe would the institutional consequences be?",
        "Low – Errors would have minimal institutional impact",
        "Moderate – Errors may require correction or clarification",
        "High – Errors could lead to formal complaints, appeals, compliance issues, reputational harm, or legal consequences",
        "q2",
    )

    q3 = radio_abc(
        "Q3. Will you input or generate identifiable information about a student, staff member, or other individual?",
        "No – No identifiable information involved",
        "Possibly – Limited or non-sensitive information",
        "Yes – Includes personal, academic, employment, or sensitive data",
        "q3",
    )

    q4 = radio_abc(
        "Q4. Could this content affect someone’s grade, job, evaluation, or formal status?",
        "No – Informational only",
        "Possibly – May influence a decision",
        "Yes – Directly used for grading, evaluation, employment, or formal decisions",
        "q4",
    )

    q5 = radio_abc(
        "Q5. Does this content involve race, gender, disability, religion, nationality, or other identity-related topics?",
        "No – No identity-related topics involved",
        "Possibly – Indirect or contextual reference",
        "Yes – Directly discusses identity-related matters",
        "q5",
    )

    q6 = radio_abc(
        "Q6. Will you input, summarize, or rewrite copyrighted, licensed, or proprietary materials using AI?",
        "No – Only original or public-domain content",
        "Possibly – Short excerpts or limited use",
        "Yes – Substantial copyrighted or restricted materials",
        "q6",
    )

    q7 = radio_abc(
        "Q7. How broadly will this content be distributed or made accessible?",
        "Limited – Small internal group (e.g., draft or internal use)",
        "Moderate – Course, department, or institutional community",
        "Wide – Public-facing or institution-wide distribution",
        "q7",
    )

    q8 = radio_abc(
        "Q8. What level of human review will occur before this content is used?",
        "Thorough review – Careful fact-checking and substantive editing",
        "Basic review – Quick read-through or minor edits",
        "Primarily AI-generated – Minimal changes before use (e.g., quick draft or summary)",
        "q8",
    )

    # Your requested explicit label:
    q9 = radio_abc(
        "Q9. If appropriate in this context, do you plan to disclose or document the use of AI? (Documentation only — does not affect tier)",
        "Yes – Disclosure or documentation planned",
        "Not yet decided",
        "No – No disclosure or documentation planned",
        "q9",
    )

    st.markdown(
        '<div class="note"><b>Note:</b> Q9 does <b>not</b> change the governance tier. It only adjusts documentation / disclosure actions.</div>',
        unsafe_allow_html=True,
    )

    st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# Internal coding + tier (Q9 excluded by design)
# -----------------------------
Q1 = sev(q1)
Q2 = sev(q2)
Q3 = sev(q3)
Q4 = sev(q4)
Q5 = sev(q5)
Q6 = sev(q6)
Q7 = sev(q7)
Q9 = sev(q9)
Q8 = review_strength(q8)

# Internal residual index (hidden) — intentionally excludes Q9
R = max(2 * (Q2 + Q4) + (Q3 + Q5 + Q6) - Q8, 0)

# Override: Q2=C, Q4=C, Q8=C (high consequence + formal decision + minimal review)
override_red = (Q2 == 2 and Q4 == 2 and Q8 == 0)

tier = tier_from_internal(R)
if override_red:
    tier = "red"

# -----------------------------
# Flags (make them feel like “diagnostic labels”)
# -----------------------------
authority_flag = (Q1 == 2)
wide_distribution_flag = (Q7 == 2)
transparency_gap_flag = (Q9 != 0)

high_consequence_flag = (Q2 == 2)
formal_decision_flag = (Q4 == 2)
pii_flag = (Q3 == 2)
identity_flag = (Q5 == 2)
copyright_flag = (Q6 == 2)
weak_review_flag = (Q8 == 0)

flag_labels = []
if authority_flag:
    flag_labels.append("Authority / official representation")
if wide_distribution_flag:
    flag_labels.append("Wide distribution / public-facing")
if pii_flag:
    flag_labels.append("Identifiable personal data")
if formal_decision_flag:
    flag_labels.append("Formal status / evaluation impact")
if high_consequence_flag:
    flag_labels.append("High institutional consequence")
if identity_flag:
    flag_labels.append("Identity-related topic")
if copyright_flag:
    flag_labels.append("Copyright / licensed materials")

# Q9 creates a “documentation attention” label, but not a tier driver
if transparency_gap_flag:
    flag_labels.append("Documentation/disclosure not confirmed (Q9)")

gate_mode = (
    high_consequence_flag
    or formal_decision_flag
    or authority_flag
    or wide_distribution_flag
    or pii_flag
)

# -----------------------------
# Recommendations
# -----------------------------
do_now = []
do_next = []
consider = []

# Always useful
do_next.append(("Keep traceability artifacts", "Save key AI inputs/outputs (prompts, drafts) for later review."))

# Tier-driven
if tier == "red":
    do_now.append(("Human review required", "Mandatory human review with a named reviewer before use."))
elif tier == "yellow":
    do_next.append(("Substantive review", "Do fact-checking and edits before use."))
else:
    consider.append(("Quick sanity check", "Brief read-through for obvious issues before sharing."))

# Gate mode
if gate_mode:
    do_now.append(("Decision record", "Document purpose, audience, what AI did, what was changed, date/version."))

# Transparency / documentation (Q9-only lever)
if (high_consequence_flag or formal_decision_flag or authority_flag or wide_distribution_flag) and transparency_gap_flag:
    do_now.append(("Documentation baseline", "At minimum: document AI use internally; for public-facing/official, add disclosure where appropriate."))
elif transparency_gap_flag:
    do_next.append(("Document AI use", "Consider internal documentation even if you do not publicly disclose."))

# Topic-specific
if pii_flag:
    do_now.append(("Privacy protection", "Minimize/anonymize identifiers; avoid sensitive data; follow institutional privacy policy."))
if identity_flag:
    do_next.append(("Bias check", "Scan for stereotyping; consider equity-focused review for identity-related content."))
if copyright_flag:
    do_now.append(("Copyright check", "Confirm rights; use short excerpts or licensed/public-domain sources."))
if weak_review_flag and tier in ("yellow", "red"):
    do_now.append(("Increase review level", "Current review level is insufficient—upgrade review before deployment."))

def dedupe(items):
    seen = set()
    out = []
    for t, d in items:
        if t not in seen:
            out.append((t, d))
            seen.add(t)
    return out

do_now = dedupe(do_now)
do_next = dedupe(do_next)
consider = dedupe(consider)

# -----------------------------
# Right panel: Results
# -----------------------------
with right:
    st.markdown(banner_html(tier, override_red), unsafe_allow_html=True)

    # Flags (bigger, tag-style, with an explanatory line)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Governance flags (triggered)</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="subtle">These labels indicate <b>what drives governance attention</b> in this context. (They are not a score.)</div>',
        unsafe_allow_html=True,
    )
    if not flag_labels:
        st.markdown('<div class="subtle">No flags triggered.</div>', unsafe_allow_html=True)
    else:
        tags = "".join([f'<span class="tag">{x}</span>' for x in flag_labels])
        st.markdown(tags, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Checklist
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Action checklist</div>', unsafe_allow_html=True)

    if do_now:
        st.markdown("**⚠ Do now**")
        for t, d in do_now:
            st.markdown(f'<div class="item"><b>{t}</b><small>{d}</small></div>', unsafe_allow_html=True)

    if do_next:
        st.markdown("**✔ Do next**")
        for t, d in do_next:
            st.markdown(f'<div class="item"><b>{t}</b><small>{d}</small></div>', unsafe_allow_html=True)

    if consider:
        st.markdown("**○ Consider**")
        for t, d in consider:
            st.markdown(f'<div class="item"><b>{t}</b><small>{d}</small></div>', unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    with st.expander("Show rationale (no score)", expanded=False):
        lines = []
        if override_red:
            lines.append("Override applied: high consequence + formal decision + minimal review.")
        if gate_mode:
            lines.append("Gate mode: decision record required prior to deployment.")
        # Explicitly restate Q9 rule:
        lines.append("Q9 note: documentation/disclosure choices affect actions only, not tier.")
        if flag_labels:
            lines.append("Flags: " + "; ".join(flag_labels) + ".")
        st.write("\n".join(lines))

