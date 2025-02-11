import streamlit as st
import pandas as pd
import random

st.title("Metal Reactivity Test")

# List of metals
metals = ["A", "B", "C", "D"]

# ---------------------------
# Initialize Session State
# ---------------------------
if "reactivity_ranks" not in st.session_state:
    random_order = metals.copy()
    random.shuffle(random_order)
    # Lower rank number means more reactive (1 = most reactive)
    st.session_state.reactivity_ranks = {metal: random_order.index(metal) + 1 for metal in metals}

if "question_type" not in st.session_state:
    st.session_state.question_type = random.choice(["reducing", "oxidising"])

# Define the MCQ question bank
mcq_bank = [
    {
        "question": "When a metal is added to a solution of another metal's nitrate, a displacement reaction occurs if and only if:",
        "options": [
            "The added metal is more reactive than the metal ion in solution.",
            "The added metal is less reactive than the metal ion in solution.",
            "Both metals have the same reactivity.",
            "The nitrate ion acts as a reducing agent."
        ],
        "correct": "The added metal is more reactive than the metal ion in solution."
    },
    {
        "question": "If metal X displaces metal Y from its nitrate solution, which statement is true?",
        "options": [
            "Metal X is more reactive than metal Y.",
            "Metal X is less reactive than metal Y.",
            "Metal X and metal Y have the same reactivity.",
            "Metal Y is a stronger reducing agent than metal X."
        ],
        "correct": "Metal X is more reactive than metal Y."
    },
    {
        "question": "Which statement best describes a displacement reaction between metals in nitrate solutions?",
        "options": [
            "A more reactive metal will replace a less reactive metal ion in solution."
