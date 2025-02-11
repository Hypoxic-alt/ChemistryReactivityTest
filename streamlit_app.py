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

# Randomize the order of MCQ options and store in session state.
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
# - Rows represent metals in the nitrate solution.
# - Columns (after renaming) represent the metals added (as their nitrate form).
#
# A displacement reaction occurs if the metal added is more reactive than the metal in solution.
# (Recall: a lower reactivity rank means more reactive.)
# Thus, a reaction occurs when:
#     reactivity_ranks[metal_in_solution] > reactivity_ranks[metal_added]
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
# - The first column ("Metal") is from the index (metals in solution).
# - The other columns are renamed (e.g., "ANO₃", "BNO₃", etc.) to indicate the metal added.
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
mcq_answer = st.radio(selected_mcq["question"], options=mcq_options, key="mcq")

# ---------------------------
# Question 4: Reaction Equation (MCQ)
# ---------------------------
# This question is generated only once and stored in session state.
# One valid reaction is generated based on the displacement table.
# The distractors include:
# - The reverse of the valid reaction.
# - An equation based on a pair that will not react.
# - An equation with an incorrect nitrate placement.
if "eq_options" not in st.session_state:
    # Choose a valid pair where a reaction occurs:
    valid_pairs = [(sol, add) for sol in metals for add in metals 
                   if sol != add and reactivity_ranks[sol] > reactivity_ranks[add]]
    # valid pair: (solution_metal, added_metal) so that added_metal displaces solution_metal
    solution_metal, added_metal = random.choice(valid_pairs)
    st.session_state.solution_metal = solution_metal
    st.session_state.added_metal = added_metal

    # Correct reaction equation
    correct_eq = f"{added_metal}(s) + {solution_metal}NO₃(aq) → {added_metal}NO₃(aq) + {solution_metal}(s)"
    
    # Distractor 1: The reverse reaction (invalid)
    distractor1 = f"{solution_metal}(s) + {added_metal}NO₃(aq) → {solution_metal}NO₃(aq) + {added_metal}(s)"
    
    # Distractor 2: An equation based on an invalid pair (a pair that will not react)
    invalid_pairs = [(sol, add) for sol in metals for add in metals 
                     if sol != add and not (reactivity_ranks[sol] > reactivity_ranks[add])]
    # Exclude the reversed valid pair if present
    invalid_pairs = [pair for pair in invalid_pairs if pair != (added_metal, solution_metal)]
    if invalid_pairs:
        sol_invalid, add_invalid = random.choice(invalid_pairs)
        distractor2 = f"{add_invalid}(s) + {sol_invalid}NO₃(aq) → {add_invalid}NO₃(aq) + {sol_invalid}(s)"
    else:
        distractor2 = f"{solution_metal}(s) + {added_metal}NO₃(aq) → {solution_metal}(s) + {added_metal}NO₃(aq)"
    
    # Distractor 3: Incorrect nitrate placement for the valid pair
    distractor3 = f"{added_metal}(s) + {solution_metal}NO₃(aq) → {solution_metal}NO₃(aq) + {added_metal}NO₃(aq)"
    
    eq_options = [correct_eq, distractor1, distractor2, distractor3]
    random.shuffle(eq_options)
    st.session_state.eq_options = eq_options
    st.session_state.correct_eq = correct_eq

st.subheader("Question 4: Select the Reaction That Will Occur")
st.write("Select the correctly balanced chemical equation:")
selected_eq = st.radio("Reaction Equation:", st.session_state.eq_options, key="eq")

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
        correct_ranking = sorted(metals, key=lambda x: reactivity_ranks[x])
        if student_ranking == correct_ranking:
            feedback.append("Ranking: Correct!")
            score += 1
        else:
            correct_str = ", ".join(correct_ranking)
            feedback.append(f"Ranking: Incorrect. Correct order is: {correct_str}.")
    
    # Evaluate Reducing / Oxidising Agent (Question 2)
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
    
    # Evaluate MCQ (Question 3)
    if mcq_answer == selected_mcq["correct"]:
        feedback.append("MCQ: Correct!")
        score += 1
    else:
        feedback.append(f"MCQ: Incorrect. The correct answer is: '{selected_mcq['correct']}'")
    
    # Evaluate Reaction Equation (Question 4)
    if selected_eq == st.session_state.correct_eq:
        feedback.append("Reaction Equation: Correct!")
        score += 1
    else:
        feedback.append(f"Reaction Equation: Incorrect. The correct equation is:\n\n**{st.session_state.correct_eq}**")
    
    st.subheader("Results")
    for msg in feedback:
        st.write(msg)
    st.write(f"Total Score: {score} out of 4")
