import streamlit as st
import pandas as pd
import random

st.title("Metal Reactivity via Displacement Reactions")

st.write(
    """
In these experiments, a piece of a metal is added to a nitrate solution of another metal.  
A **displacement reaction** (shown as “Reaction” in the table) occurs if and only if the **added metal is more reactive** than the metal ion in solution.  
For each pair, if the metal in the **row** is more reactive than the metal in the **column**, a reaction occurs.
"""
)

# -------------------------------------------------------------------
# RANDOMIZE THE UNDERLYING REACTIVITY ORDER
# -------------------------------------------------------------------
metals = ["A", "B", "C", "D"]

# Create a random order. For example, if random_order becomes ["B", "D", "A", "C"],
# then "B" is the most reactive and "C" the least reactive.
random_order = metals.copy()
random.shuffle(random_order)

# Create a dictionary mapping metal -> reactivity rank (1 is most reactive, 4 is least reactive)
reactivity_ranks = {metal: random_order.index(metal) + 1 for metal in metals}

# For testing/debugging purposes (uncomment for debug):
# st.write("DEBUG: Underlying reactivity order (most reactive to least reactive):", sorted(metals, key=lambda x: reactivity_ranks[x]))

# -------------------------------------------------------------------
# BUILD THE DISPLACEMENT REACTION TABLE
# -------------------------------------------------------------------
# For each cell:
# - If row metal equals column metal: display "—"
# - Else, if the reactivity rank of the row metal is lower (i.e. more reactive) than that of the column metal, show "Reaction"
# - Otherwise, show "No Reaction"
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

# Create a DataFrame. The rows indicate the metal added (displacer) and the columns indicate the metal nitrate solution.
df_table = pd.DataFrame(
    table_data, 
    index=[f"Metal {m} NO₃" for m in metals]
)
df_table.index.name = "Added Metal (Displacer)"

st.subheader("Displacement Reaction Table")
st.write(
    "Below is the table showing the outcome when each metal is added to each metal nitrate solution. "
    "A 'Reaction' indicates that the added metal is more reactive than the metal in solution (i.e. it displaces that metal), "
    "and 'No Reaction' indicates that it is less reactive."
)
st.table(df_table)

# -------------------------------------------------------------------
# QUESTION 1: RANK THE METALS
# -------------------------------------------------------------------
st.subheader("Question 1: Rank the Metals by Reactivity")
st.write(
    "Based on the table above, **rank the metals from most reactive to least reactive** (i.e. the metal that displaces all others should be ranked first, and the one that displaces none should be ranked last)."
)

# Create four selectboxes (one for each ranking position)
col1, col2, col3, col4 = st.columns(4)
with col1:
    rank1 = st.selectbox("Most reactive", metals, key="rank1")
with col2:
    rank2 = st.selectbox("2nd most reactive", metals, key="rank2")
with col3:
    rank3 = st.selectbox("3rd most reactive", metals, key="rank3")
with col4:
    rank4 = st.selectbox("Least reactive", metals, key="rank4")

# -------------------------------------------------------------------
# QUESTION 2: IDENTIFY STRONGEST REDUCING OR OXIDISING AGENT (RANDOMIZED)
# -------------------------------------------------------------------
# Randomly decide which question to ask:
# - For displacement reactions, the strongest reducing agent is the most reactive metal.
# - The strongest oxidising agent is the metal ion that is most easily reduced (i.e. from the least reactive metal).
question_type = random.choice(["reducing", "oxidising"])

if question_type == "reducing":
    st.subheader("Question 2: Identify the Strongest Reducing Agent")
    st.write("Select the metal that is the strongest reducing agent.")
    agent_answer = st.radio("Your answer", metals, key="reducing")
else:
    st.subheader("Question 2: Identify the Strongest Oxidising Agent")
    st.write("Select the metal that is the strongest oxidising agent.")
    agent_answer = st.radio("Your answer", metals, key="oxidising")

# -------------------------------------------------------------------
# QUESTION 3: MULTIPLE CHOICE QUESTION (MCQ)
# -------------------------------------------------------------------
st.subheader("Question 3: Multiple Choice Question")
st.write(
    "When a metal is added to a solution of another metal's nitrate, a displacement reaction will occur if and only if:"
)
mcq_answer = st.radio(
    "Select the correct option:",
    options=[
        "The added metal is more reactive than the metal ion in solution.",
        "The added metal is less reactive than the metal ion in solution.",
        "Both metals have the same reactivity.",
        "The nitrate ion acts as a reducing agent."
    ],
    key="mcq"
)

# -------------------------------------------------------------------
# SUBMIT BUTTON AND ANSWER EVALUATION
# -------------------------------------------------------------------
if st.button("Submit Answers"):
    score = 0
    feedback = []
    
    # --- Evaluate Ranking Answer ---
    student_ranking = [rank1, rank2, rank3, rank4]
    if len(set(student_ranking)) < 4:
        feedback.append("**Ranking Answer:** Please ensure you select a unique metal for each ranking position.")
    else:
        # The correct ranking order is obtained by sorting metals by their reactivity rank (lowest rank = most reactive)
        correct_ranking = sorted(metals, key=lambda x: reactivity_ranks[x])
        if student_ranking == correct_ranking:
            feedback.append("**Ranking Answer:** Correct!")
            score += 1
        else:
            correct_str = ", ".join(correct_ranking)
            feedback.append(f"**Ranking Answer:** Incorrect. The correct order (most reactive to least reactive) is: {correct_str}.")
    
    # --- Evaluate Agent Question ---
    if question_type == "reducing":
        # The strongest reducing agent is the most reactive metal.
        correct_agent = min(metals, key=lambda x: reactivity_ranks[x])
        if agent_answer == correct_agent:
            feedback.append("**Question 2 (Reducing Agent):** Correct!")
            score += 1
        else:
            feedback.append(f"**Question 2 (Reducing Agent):** Incorrect. The strongest reducing agent is Metal {correct_agent}.")
    else:
        # The strongest oxidising agent is associated with the least reactive metal.
        correct_agent = max(metals, key=lambda x: reactivity_ranks[x])
        if agent_answer == correct_agent:
            feedback.append("**Question 2 (Oxidising Agent):** Correct!")
            score += 1
        else:
            feedback.append(f"**Question 2 (Oxidising Agent):** Incorrect. The strongest oxidising agent is Metal {correct_agent}.")
    
    # --- Evaluate MCQ ---
    if mcq_answer == "The added metal is more reactive than the metal ion in solution.":
        feedback.append("**MCQ:** Correct!")
        score += 1
    else:
        feedback.append("**MCQ:** Incorrect. The correct answer is: 'The added metal is more reactive than the metal ion in solution.'")
    
    st.subheader("Results")
    for f in feedback:
        st.write(f)
    st.write(f"**Total Score: {score} out of 3**")
