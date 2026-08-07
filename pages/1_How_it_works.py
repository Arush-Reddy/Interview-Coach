"""How the interview coach turns context into focused practice."""

import streamlit as st

from utils.styles import (
    inject_global_styles,
    render_accessibility_control,
    render_product_nav,
)


st.set_page_config(
    page_title="How it works · AI Interview Coach",
    page_icon=":material/route:",
    layout="wide",
    initial_sidebar_state="collapsed",
)
inject_global_styles()
render_product_nav("How it works")
render_accessibility_control()

st.markdown(
    """
    <section class="how-hero">
        <div class="how-hero-copy">
            <span class="eyebrow">HOW IT WORKS</span>
            <h1>Your experience in. <span>Better answers out.</span></h1>
            <p>
                Bring the résumé and role. Your coach turns that context into
                questions worth practising—and feedback you can act on.
            </p>
            <div class="how-actions">
                <a class="how-primary-link" href="/" target="_self">
                    Start practising&nbsp; →
                </a>
                <a class="how-secondary-link" href="/About" target="_self">
                    About the project
                </a>
            </div>
        </div>
        <div class="how-map" aria-label="How the interview coach works">
            <span class="map-label">YOUR INTERVIEW CONTEXT</span>
            <div class="context-row">
                <div class="context-chip">Résumé</div>
                <div class="context-chip">Target role</div>
                <div class="context-chip">Job listing</div>
            </div>
            <div class="map-connector"></div>
            <div class="coach-core">
                <div class="coach-symbol">AI</div>
                <div>
                    <strong>Personalized interview coach</strong>
                    <small>Connects your background to the opportunity</small>
                </div>
            </div>
            <div class="map-connector"></div>
            <div class="outcome-row">
                <div class="outcome-chip">Role match</div>
                <div class="outcome-chip">Questions</div>
                <div class="outcome-chip">Feedback</div>
            </div>
        </div>
    </section>

    <section class="how-section">
        <div class="how-section-heading">
            <div>
                <span class="eyebrow">THE PRACTICE LOOP</span>
                <h2>Three steps. One focused session.</h2>
            </div>
            <p>
                Each stage keeps the same interview context, so your questions
                and feedback feel connected—not randomly generated.
            </p>
        </div>
        <div class="step-grid">
            <article class="step-card">
                <div class="step-top">
                    <span class="step-number">01</span>
                    <span class="step-arrow">↘</span>
                </div>
                <h3>Set the interview context</h3>
                <p>
                    Upload your résumé, choose the role, and optionally add the
                    job listing for a sharper match.
                </p>
                <div class="step-tags">
                    <span>PDF · DOCX · Image</span>
                    <span>Role-aware</span>
                </div>
            </article>
            <article class="step-card">
                <div class="step-top">
                    <span class="step-number">02</span>
                    <span class="step-arrow">↘</span>
                </div>
                <h3>Practise questions that fit</h3>
                <p>
                    Get questions grounded in your projects, skills, experience,
                    and the responsibilities of the role.
                </p>
                <div class="step-tags">
                    <span>Voice or text</span>
                    <span>Tailored questions</span>
                </div>
            </article>
            <article class="step-card">
                <div class="step-top">
                    <span class="step-number">03</span>
                    <span class="step-arrow">✓</span>
                </div>
                <h3>Turn feedback into progress</h3>
                <p>
                    Review answer quality and communication habits, then use the
                    next-step guidance to improve your response.
                </p>
                <div class="step-tags">
                    <span>Clear scores</span>
                    <span>Actionable feedback</span>
                </div>
            </article>
        </div>
    </section>

    <section class="personalization">
        <div class="personalization-copy">
            <span class="eyebrow">PERSONAL BY DESIGN</span>
            <h2>Feedback built around your answer.</h2>
            <p>
                The coach looks at both what you said and how you delivered it.
                That makes every review specific enough to use on your next try.
            </p>
            <div class="personal-points">
                <div class="personal-point"><i></i>Content and answer structure</div>
                <div class="personal-point"><i></i>Clarity, pace, and filler words</div>
                <div class="personal-point"><i></i>Strengths and practical next steps</div>
            </div>
        </div>
        <div class="feedback-demo" aria-label="Example interview feedback">
            <div class="feedback-toolbar">
                <span>Interview practice · Question 2</span>
                <span class="live-pill"><i></i> Voice answer</span>
            </div>
            <div class="feedback-question">
                <small>BEHAVIOURAL</small>
                <p>Tell me about a time you handled a difficult project deadline.</p>
            </div>
            <div class="waveform" aria-hidden="true">
                <span style="height:24px"></span><span style="height:42px"></span>
                <span style="height:32px"></span><span style="height:56px"></span>
                <span style="height:38px"></span><span style="height:64px"></span>
                <span style="height:48px"></span><span style="height:28px"></span>
                <span style="height:52px"></span><span style="height:36px"></span>
                <span style="height:60px"></span><span style="height:30px"></span>
                <span style="height:44px"></span><span style="height:22px"></span>
            </div>
            <div class="feedback-results">
                <div class="feedback-result">
                    <small>ANSWER STRUCTURE</small>
                    <strong>Clear STAR flow</strong>
                </div>
                <div class="feedback-result">
                    <small>COMMUNICATION</small>
                    <strong>Confident pace</strong>
                </div>
                <div class="feedback-result">
                    <small>NEXT STEP</small>
                    <strong>Quantify the result</strong>
                </div>
            </div>
        </div>
    </section>

    <section class="how-cta">
        <div>
            <h2>Ready to practise the role you want?</h2>
            <p>Start with your résumé, or use the sample profile to explore.</p>
        </div>
        <a class="how-primary-link" href="/" target="_self">
            Build my interview plan&nbsp; →
        </a>
    </section>
    """,
    unsafe_allow_html=True,
)
