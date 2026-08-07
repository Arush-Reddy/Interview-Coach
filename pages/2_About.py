"""Project background for the AI Interview Coach."""

import streamlit as st

from utils.styles import (
    inject_global_styles,
    render_accessibility_control,
    render_product_nav,
)


st.set_page_config(
    page_title="About · AI Interview Coach",
    page_icon=":material/info:",
    layout="wide",
    initial_sidebar_state="collapsed",
)
inject_global_styles()
render_product_nav("About")
render_accessibility_control()

st.markdown(
    """
    <section class="about-hero-modern">
        <div class="about-hero-copy">
            <span class="eyebrow">ABOUT THE PROJECT</span>
            <h1>Practice built for the <span>interview that matters.</span></h1>
            <p>
                AI Interview Coach helps students and early-career candidates
                turn their real experience into focused, role-specific practice.
            </p>
            <div class="how-actions">
                <a class="how-primary-link" href="/" target="_self">
                    Try the coach&nbsp; →
                </a>
                <a class="how-secondary-link" href="/How_it_works" target="_self">
                    See how it works
                </a>
            </div>
        </div>
        <div class="project-identity" aria-label="Build Beyond hackathon project">
            <div class="project-card-top">
                <span>BUILD BEYOND</span>
                <i></i>
            </div>
            <div class="project-monogram">
                <strong>AI<br>INTERVIEW<br>COACH</strong>
                <span>HACKATHON PROJECT</span>
            </div>
            <div class="project-signals">
                <div class="project-signal">Personalized</div>
                <div class="project-signal">Voice-enabled</div>
                <div class="project-signal">Role-aware</div>
            </div>
        </div>
    </section>
    <section class="about-story-section">
        <div class="about-section-heading">
            <div>
                <span class="eyebrow">THE STORY</span>
                <h2>From generic preparation to useful practice.</h2>
            </div>
            <p>
                The project started with one simple idea: interview guidance is
                more valuable when it understands both the candidate and the role.
            </p>
        </div>
        <div class="story-grid">
            <article class="story-panel problem">
                <span class="story-index">01 · THE PROBLEM</span>
                <h3>Most practice starts without context.</h3>
                <p>
                    Generic question lists cannot see the projects you built,
                    the skills you developed, or the opportunity you are aiming for.
                    That makes preparation feel disconnected from the real interview.
                </p>
            </article>
            <article class="story-panel approach">
                <span class="story-index">02 · THE APPROACH</span>
                <h3>Connect the person to the role.</h3>
                <p>
                    The coach brings together your résumé, target position, and
                    job listing before it creates questions or evaluates an answer.
                </p>
            </article>
            <article class="story-panel outcome">
                <div>
                    <span class="story-index">03 · THE OUTCOME</span>
                    <h3>A complete practice loop.</h3>
                </div>
                <div class="outcome-list">
                    <div class="outcome-line"><span>01</span>Understand your role match</div>
                    <div class="outcome-line"><span>02</span>Practise tailored questions by voice or text</div>
                    <div class="outcome-line"><span>03</span>Turn specific feedback into a stronger next answer</div>
                </div>
            </article>
        </div>
    </section>
    <section class="about-tech">
        <div class="about-tech-header">
            <div>
                <span class="eyebrow">BUILT WITH</span>
                <h2>Technology with a purpose.</h2>
            </div>
            <p>
                Each part of the stack supports a real step in the experience,
                from understanding the résumé to reviewing a spoken answer.
            </p>
        </div>
        <div class="tech-grid">
            <article class="tech-item">
                <div class="tech-mark">G</div>
                <h3>Gemini</h3>
                <p>Résumé analysis, role matching, tailored questions, and answer feedback.</p>
            </article>
            <article class="tech-item">
                <div class="tech-mark">St</div>
                <h3>Streamlit</h3>
                <p>The interactive product experience and interview workspace.</p>
            </article>
            <article class="tech-item">
                <div class="tech-mark">W</div>
                <h3>Whisper</h3>
                <p>Voice transcription for realistic spoken-answer practice.</p>
            </article>
            <article class="tech-item">
                <div class="tech-mark">Py</div>
                <h3>Python</h3>
                <p>Document processing, scoring, communication analysis, and reports.</p>
            </article>
        </div>
    </section>
    <section class="about-principle">
        <span class="eyebrow">THE PRODUCT PRINCIPLE</span>
        <blockquote>
            Every feature should make practice more focused or feedback
            <span>more actionable.</span>
        </blockquote>
    </section>
    <section class="about-final-cta">
        <div>
            <h2>See what your next interview could look like.</h2>
            <p>Upload your résumé, or start instantly with the sample profile.</p>
        </div>
        <a class="how-primary-link" href="/" target="_self">
            Build my interview plan&nbsp; →
        </a>
    </section>
    """,
    unsafe_allow_html=True,
)
