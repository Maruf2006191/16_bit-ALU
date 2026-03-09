#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd

# --- 1. Extracted Data from Genus Reports ---
# Total Power values (in Watts)
P_baseline = 74.159e-6      # From ngated_power.rpt
P_gated = 39.992e-6         # From gated_power.rpt

# Timing (in Seconds)
T_delay = 17.724e-9         # From ngated_timing.rpt (Critical path)

# System Parameters
VDD = 1.0                   # Nominal Voltage (Volts)
F_target = 50e6             # Target Frequency (50 MHz)
T_target = 1 / F_target     # Target Period (20 ns)
Vth = 0.8                   # Threshold Voltage (Volts)

print("Calculating DVFS Parameters...")

# --- 2. DVFS Calculations ---
# Switched Capacitance: C = P / (V^2 * f)
C_baseline = P_baseline / ((VDD ** 2) * F_target)
C_gated = P_gated / ((VDD ** 2) * F_target)

# Peak Timing
f_max = 1 / T_delay
T_max = T_delay 

# Proportionality Constant (K): K = T_max * (VDD - Vth) / VDD
K = T_max * ((VDD - Vth) / VDD)

# Optimized Voltage (VDD_opt): VDD_opt = (K / T_target) + Vth
VDD_opt = (K / T_target) + Vth

# New Power calculations at VDD_opt
# P = C * (V^2) * f
P_mode1 = C_baseline * (VDD_opt ** 2) * F_target
P_mode2 = C_gated * (VDD_opt ** 2) * F_target

# Print intermediate results
print(f"Total Switched Capacitance (Baseline): {C_baseline * 1e12:.4f} pF")
print(f"Max Frequency (f_max): {f_max / 1e6:.2f} MHz")
print(f"Proportionality Constant (K): {K * 1e9:.4f} ns")
print(f"Optimized Voltage (VDD_opt): {VDD_opt:.4f} V\n")

# --- 3. Create Mode Table and Export to Excel ---
# Prepare the data dictionary
data = {
    "Operating Mode": [
        "Mode 0 (Baseline)", 
        "Mode 1 (DVFS Only)", 
        "Mode 2 (Hybrid Gated)"
    ],
    "Voltage (V)": [
        round(VDD, 3), 
        round(VDD_opt, 3), 
        round(VDD_opt, 3)
    ],
    "Frequency (MHz)": [
        F_target / 1e6, 
        F_target / 1e6, 
        F_target / 1e6
    ],
    "Total Power (\u03bcW)": [
        round(P_baseline * 1e6, 2), 
        round(P_mode1 * 1e6, 2), 
        round(P_mode2 * 1e6, 2)
    ]
}

# Convert to a Pandas DataFrame
df = pd.DataFrame(data)

# Print the table to the console
print("=== DVFS Mode Table ===")
print(df.to_string(index=False))

# Export to Excel
excel_filename = "DVFS_Mode_Table.xlsx"
df.to_excel(excel_filename, index=False)
print(f"\nSuccess! Table exported to '{excel_filename}'.")


# In[ ]:




