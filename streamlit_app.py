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

# Define the MCQ question bank (Question 3)
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
# In this table:
# - The rows represent the metals present in the nitrate solution.
# - The columns (after renaming) represent the metals that are added (as their nitrate form).
#
# A displacement reaction occurs if the added metal (from the column) is more reactive
# than the metal in the solution (from the row). Because a lower rank number indicates
# higher reactivity, this condition is met when:
#
#     reactivity_ranks[row] > reactivity_ranks[col]
#
# That is, if the reactivity rank of the metal in the solution (row) is greater than
# that of the added metal (column), then the added metal will displace the metal in solution.
table_data = {}
for row in metals:
    row_vals = []
    for col in metals:
        if row == col:
            row_vals.append("—")
        else:
            if reactivity_ranks[row] > reactivity_ranks[col]:
                row_vals.append("Reaction")
            else:
                row_vals.append("No Reaction")
    table_data[row] = row_vals

# Create a DataFrame:
# - The first column (labeled "Metal") is taken from the index and represents the metals in solution.
# - The other columns are renamed (e.g., "ANO₃", "BNO₃", etc.) to indicate the metal being added.
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
labels = ["Most reactive", "2nd most reactive", "3rd most reactive", "Least reactive"]
cols = st.columns(4)
student_ranking = []

for i, label in enumerate(labels):
    with cols[i]:
        choice = st.selectbox(label, metals, key=f"rank{i+1}")
        student_ranking.append(choice)

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
# Question 4: Displacement Reaction Equation (MCQ)
# ---------------------------
st.subheader("Question 4: Identify the Correct Displacement Reaction Equation")
st.write("""
Consider a displacement reaction where a more reactive metal **A** displaces a less reactive metal **B** from its nitrate solution.
Which of the following is the correctly balanced chemical equation for this reaction?
""")

# Define the correct equation and generate distractors with common mistakes:
correct_eq = "A(s) + BNO₃(aq) → ANO₃(aq) + B(s)"
# Distractor 1: Reaction written in reverse.
distractor1 = "B(s) + ANO₃(aq) → A(s) + BNO₃(aq)"
# Distractor 2: Nitrate group attached to the wrong metal in the products.
distractor2 = "A(s) + BNO₃(aq) → BNO₃(aq) + ANO₃(aq)"
# Distractor 3: Reactants are both metals (ignoring the nitrate component).
distractor3 = "A(s) + B(s) → ANO₃(aq) + BNO₃(aq)"

eq_options = [correct_eq, distractor1, distractor2, distractor3]
random.shuffle(eq_options)
selected_eq = st.radio("Select the correctly balanced equation:", eq_options, key="eq")

# ---------------------------
# Submission and Evaluation
# ---------------------------
if st.button("Submit Answers"):
    score = 0
    feedback = []
    
    # Evaluate Ranking (Question 1)
    if len(set(student_ranking)) < 4:
        feedback.append("Ranking: Please ensure you select a unique metal for each position.")
    else:
        # Correct ranking: metals sorted in ascending order of their reactivity rank 
        # (lowest rank number = most reactive)
        correct_ranking = sorted(metals, key=lambda x: reactivity_ranks[x])
        if student_ranking == correct_ranking:
            feedback.append("Ranking: Correct!")
            score += 1
        else:
            correct_str = ", ".join(correct_ranking)
            feedback.append(f"Ranking: Incorrect. Correct order is: {correct_str}.")
    
    # Evaluate Reducing / Oxidising Agent (Question 2)
    if question_type == "reducing":
        # The strongest reducing agent is the most reactive (lowest rank number)
        correct_agent = min(metals, key=lambda x: reactivity_ranks[x])
        if agent_answer == correct_agent:
            feedback.append("Reducing Agent: Correct!")
            score += 1
        else:
            feedback.append(f"Reducing Agent: Incorrect. The strongest reducing agent is Metal {correct_agent}.")
    else:
        # The strongest oxidising agent is the least reactive (highest rank number)
        correct_agent = max(metals, key=lambda x: reactivity_ranks[x])
        if agent_answer == correct_agent:
            feedback.append("Oxidising Agent: Correct!")
            score += 1
        else:
            feedback.append(f"Oxidising Agent: Incorrect. The strongest oxidising agent is Metal {correct_agent}.")
    
    # Evaluate MCQ (Question 3)
    if mcq_answer == selected_mcq["correct"]:
        feedback.append("MCQ: Correct!")
        score += 1
    else:
        feedback.append(f"MCQ: Incorrect. The correct answer is: '{selected_mcq['correct']}'")
    
    # Evaluate Equation MCQ (Question 4)
    if selected_eq == correct_eq:
        feedback.append("Equation: Correct!")
        score += 1
    else:
        feedback.append(f"Equation: Incorrect. The correct equation is:\n\n**{correct_eq}**")
    
    st.subheader("Results")
    for msg in feedback:
        st.write(msg)
    st.write(f"Total Score: {score} out of 4")
