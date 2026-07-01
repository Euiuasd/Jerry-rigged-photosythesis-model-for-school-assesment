import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("How to Act Like a Plant - Guide by me")
st.markdown("Coded(jerry rigged code this looks absolutely terrible) and equations calculated by mark ")
st.markdown("This website demonstrates the impact of various variables on plant photosynthesis.")

st.sidebar.header("Adjust Photosynthesis Variables")

num_leaves = st.sidebar.slider(
    "Number of Leaves", 
    min_value=1, max_value=100, value=1, step=1,
    help="The amount of leaves doing photosynthesis. Duh :D"
)

W_c = st.sidebar.slider(
    "Carbon Limit [%]", 
    min_value=0, max_value=100, value=50, step=5,
    help="How fast the rubisco enzyme can absorb the CO2 out of the air."
)

W_j = st.sidebar.slider(
    "Light Energy Processing [%]", 
    min_value=0, max_value=100, value=60, step=5,
    help="How fast the plant can process light energy "
)

O_conc = st.sidebar.slider(
    "Oxygen Concentration  [%]", 
    min_value=0, max_value=30, value=21, step=1,
    help="The oxygen concentration inside the plant."
)

T_tau = st.sidebar.slider(
    "Temperature Factor ", 
    min_value=1000, max_value=5000, value=2500, step=100,
    help="Represents the Tau symbol, has an effect on rubisco efficiency"
)

C_a = st.sidebar.slider(
    "Atmospheric CO2 [ppm]", 
    min_value=100, max_value=1000, value=400, step=10,
    help="Atmospheric CO2 concentration (ppm)."
)

C_i = 0.7 * C_a

if T_tau * C_i == 0:
    rubisco_efficiency = 0
else:
    rubisco_efficiency = 1 - ((0.5 * O_conc) / (T_tau * C_i))

A_gross_single = min(W_c, W_j) * rubisco_efficiency
A_gross_total = A_gross_single * num_leaves

st.subheader("Results")
st.write(f"**Calculated Internal CO2 (C_i):** {int(C_i)} ppm")
st.write(f"**Gross Photosynthesis per Leaf:** {int(A_gross_single)} units")
st.write(f"**Total Gross Photosynthesis ({num_leaves} leaves):** {int(A_gross_total)} units")

st.subheader("Total Gross Photosynthesis vs. Atmospheric CO2")

ca_values = np.linspace(100, 1000, 100)
ci_values = 0.7 * ca_values

a_gross_values = [
    (min(W_c, W_j) * (1 - ((0.5 * O_conc) / (T_tau * ci)))) * num_leaves 
    for ci in ci_values
]

fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(ca_values, a_gross_values, color='green', label='Photosynthesis Response Curve')
ax.scatter([C_a], [A_gross_total], color='red', zorder=5, label='Current State')

ax.set_title("Impact of Atmospheric CO2 on Total Gross Photosynthesis")
ax.set_xlabel("Atmospheric CO2 Concentration [ppm]")
ax.set_ylabel("Total Gross Photosynthesis [units]")
ax.legend()
ax.grid(True, linestyle='--', alpha=0.7)

st.pyplot(fig)