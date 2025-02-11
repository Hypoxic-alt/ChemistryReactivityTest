import streamlit as st
import pandas as pd
import random

st.title("Metal Reactivity Test")

# List of metals
metals = ["A", "B", "C", "D"]

# Randomize the underlying reactivity order
random_order = metals.copy()
random.shuffle(random_order)
# Lower rank number = more reactive (1 = most reactive, 4 = least reactive)
reactivity_ranks = {metal: random_order.index(metal) + 1 for metal in metals}

# Build the displacement reaction table.
# For each cell: if row metal is more reactive than column metal → "Reaction", else "No Reaction"
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

# Create DataFrame with first column as "Metal"
df_table = pd.DataFrame(table_data, index=metals)
df_table.reset_index(inplace=True)
df_table.rename(columns={"index": "Metal"}, inplace=True)

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

# ---------------------------------------------------------
# Question 2: Strongest Reducing or Oxidising Agent (Random)
# ---------------------------------------------------------
question_type = random.choice(["reducing", "oxidising"])
if question_type == "reducing":
    st.subheader("Question 2: Identify the Strongest Reducing Agent")
    agent_answer = st.radio("Your answer", metals, key="reducing")
else:
    st.subheader("Question 2: Identify the Strongest Oxidising Agent")
    agent_answer = st.radio("Your answer", metals, key="oxidising")

# ------------------------------------
# Question 3: Multiple Choice Question
# ------------------------------------
st.subheader("Question 3: Multiple Choice")
mcq_answer = st.radio(
    "When a metal is added to a solution of another metal's nitrate, a displacement reaction occurs if and only if:",
    options=[
        "The added metal is more reactive than the metal ion in solution.",
        "The added metal is less reactive than the metal ion in solution.",
        "Both metals have the same reactivity.",
        "The nitrate ion acts as a reducing agent."
    ],
    key="mcq"
)

# ---------------
# Submission
# ---------------
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
    if mcq_answer == "The added metal is more reactive than the metal ion in solution.":
        feedback.append("MCQ: Correct!")
        score += 1
    else:
        feedback.append("MCQ: Incorrect. The correct answer is: 'The added metal is more reactive than the metal ion in solution.'")
    
    st.subheader("Results")
    for msg in feedback:
        st.write(msg)
    st.write(f"Total Score: {score} out of 3")
