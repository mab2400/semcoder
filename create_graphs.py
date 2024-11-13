import matplotlib.pyplot as plt
import numpy as np

# Data for the overall percentages (control vs. ablated)
overall_categories = ['Control', 'Ablated']
overall_percentages = [62.80, 57.93]

# Calculate the overall relative drop
relative_drop = (62.80 - 57.93) / 62.80 * 100

# Plot 1: Overall percentages (control vs. ablated)
plt.figure(figsize=(8, 5))
bars = plt.bar(overall_categories, overall_percentages, color=['skyblue', 'salmon'])
plt.title("Overall Performance (Control vs. Ablated)")
plt.ylabel("Pass Rate (%)")
plt.ylim(0, 100)

# Add relative drop label above the "Ablated" bar
plt.text(bars[1].get_x() + bars[1].get_width() / 2, bars[1].get_height() + 1,
         f"{relative_drop:.2f}% relative drop", ha='center', va='bottom', fontsize=8)

plt.show()

# Data for the individual categories (control vs. ablated)
categories = ['ListArray', 'DS', 'Math', 'String']
control_scores = [65.00, 55.00, 66.67, 59.09]
ablated_scores = [62.50, 40.00, 61.67, 56.82]

# Calculate the relative drop for each category
relative_drops = [(control - ablated) / control * 100 for control, ablated in zip(control_scores, ablated_scores)]

# Plot 2: Category-wise performance (control vs. ablated)
x = np.arange(len(categories))  # the label locations
width = 0.35  # the width of the bars

fig, ax = plt.subplots(figsize=(10, 6))
bars1 = ax.bar(x - width/2, control_scores, width, label='Control', color='skyblue')
bars2 = ax.bar(x + width/2, ablated_scores, width, label='Ablated', color='salmon')

# Add some text for labels, title, and custom x-axis tick labels, etc.
ax.set_xlabel("Category")
ax.set_ylabel("Pass Rate (%)")
ax.set_title("Category-wise Performance (Control vs. Ablated)")
ax.set_xticks(x)
ax.set_xticklabels(categories)
ax.legend()

# Annotate the relative drop over the ablated bars
for i, (bar, drop) in enumerate(zip(bars2, relative_drops)):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1, f"{drop:.2f}% \n relative drop", ha='center', va='bottom', fontsize=7)

plt.ylim(0, 100)
plt.show()
