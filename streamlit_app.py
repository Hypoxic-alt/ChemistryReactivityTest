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
            "A more reactive metal will replace a less reactive metal ion in solution.",
            "A less reactive metal will replace a more reactive metal ion in solution.",
            "Both metals form a precipitate.",
            "No reaction occurs because the nitrate ion is inert."
        ],
        "correct": "A more reactive metal will replace a less reactive metal ion in solution."
    },
    {
        "question": "What does it mean when you observe a 'Reaction' in the displacement table for a given pair of metals?",
        "options": [
            "The added metal is more reactive than the metal in the nitrate solution.",
            "The added metal is less reactive than the metal in the nitrate solution.",
            "The nitrate ion is reacting with both metals.",
            "The metal in the nitrate solution is more reactive than the added metal."
        ],
        "correct": "The added metal is more reactive than the metal in the nitrate solution."
    }
]

if "selected_mcq" not in st.session_state:
    st.session_state.selected_mcq = random.choice(mcq_bank)

# Randomize the order of MCQ options and store it in session state.
if "mcq_options" not in st.session_state:
    mcq_options = st.session_state.selected_mcq["options"].copy()
    random.shuffle(mcq_options)
    st.session_state.mcq_options = mcq_options

# Retrieve stored values
reactivity_ranks = st.session_state.reactivity_ranks
question_type = st.session_state.question_type
selected_mcq = st.session_state.selected_mcq
mcq_options = st.session_state.mcq_options

# ---------------------------
# Build the Displacement Reaction Table
# ---------------------------
# For each cell: if the row metal is more reactive than the column metal, show "Reaction"; otherwise, "No Reaction".
table_data = {}
for row in metals:
    row_vals = []
    for col in metals:
        if row == col:
            row_vals.append("—")
        else:
            if reactivity_ranks[row] < reactivity_ranks[col]:
                row_vals.append("Reaction")
            else:
                row_vals.append("No Reaction")
    table_data[row] = row_vals

# Create a DataFrame:
# - The first column lists the metal labels.
# - The subsequent columns are titled "ANO₃", "BNO₃", etc.
df_table = pd.DataFrame(table_data, index=metals)
df_table.reset_index(inplace=True)
df_table.rename(columns={"index": "Metal"}, inplace=True)
for m in metals:
    df_table.rename(columns={m: f"{m}NO₃"}, inplace=True)

st.table(df_table)

# ---------------------------
# Question 1: Rank the Metals
# ---------------------------
st.subheader("Question 1: Rank the Metals by Reactivity")
col1, col2, col3, col4 = st.columns(4)
with col1:
    rank1 = st.selectbox("Most reactive", metals, key="rank1")
with col2:
    rank2 = st.selectbox("2nd most reactive", metals, key="rank2")
with col3:
    rank3 = st.selectbox("3rd most reactive", metals, key="rank3")
with col4:
    rank4 = st.selectbox("Least reactive", metals, key="rank4")

# ---------------------------
# Question 2: Strongest Reducing or Oxidising Agent
# ---------------------------
if question_type == "reducing":
    st.subheader("Question 2: Identify the Strongest Reducing Agent")
    agent_answer = st.radio("Your answer", metals, key="reducing")
else:
    st.subheader("Question 2: Identify the Strongest Oxidising Agent")
    agent_answer = st.radio("Your answer", metals, key="oxidising")

# ---------------------------
# Question 3: Multiple Choice Question (MCQ)
# ---------------------------
st.subheader("Question 3: Multiple Choice")
mcq_answer = st.radio(
    selected_mcq["question"],
    options=mcq_options,
    key="mcq"
)

# ---------------------------
# Submission and Evaluation
# ---------------------------
if st.button("Submit Answers"):
    score = 0
    feedback = []
    
    # Evaluate Ranking
    student_ranking = [rank1, rank2, rank3, rank4]
    if len(set(student_ranking)) < 4:
        feedback.append("Ranking: Please ensure you select a unique metal for each position.")
    else:
        correct_ranking = sorted(metals, key=lambda x: reactivity_ranks[x])
        if student_ranking == correct_ranking:
            feedback.append("Ranking: Correct!")
            score += 1
        else:
            correct_str = ", ".join(correct_ranking)
            feedback.append(f"Ranking: Incorrect. Correct order is: {correct_str}.")
    
    # Evaluate Reducing / Oxidising Agent Question
    if question_type == "reducing":
        correct_agent = min(metals, key=lambda x: reactivity_ranks[x])
        if agent_answer == correct_agent:
            feedback.append("Reducing Agent: Correct!")
            score += 1
        else:
            feedback.append(f"Reducing Agent: Incorrect. The strongest reducing agent is Metal {correct_agent}.")
    else:
        correct_agent = max(metals, key=lambda x: reactivity_ranks[x])
        if agent_answer == correct_agent:
            feedback.append("Oxidising Agent: Correct!")
            score += 1
        else:
            feedback.append(f"Oxidising Agent: Incorrect. The strongest oxidising agent is Metal {correct_agent}.")
    
    # Evaluate MCQ
    if mcq_answer == selected_mcq["correct"]:
        feedback.append("MCQ: Correct!")
        score += 1
    else:
        feedback.append(f"MCQ: Incorrect. The correct answer is: '{selected_mcq['correct']}'")
    
    st.subheader("Results")
    for msg in feedback:
        st.write(msg)
    st.write(f"Total Score: {score} out of 3")
