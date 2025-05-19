# Import required libraries
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Create a DataFrame with Phase 4 marketing outcomes and their impact scores
data = pd.DataFrame({
    'Outcome': ["Precision Targeting", "Increased ROI", "Faster Execution", "Stronger Trust"],
    'Impact Score': [85, 90, 88, 82]  # Scores out of 100 representing performance impact
})

# Set figure size for better readability
plt.figure(figsize=(10, 6))

# Create a barplot using seaborn to visualize impact scores for each outcome
sns.barplot(
    data=data,
    x='Outcome',
    y='Impact Score',
    hue='Outcome',        # Add color differentiation for each outcome
    palette='Blues_d',    # Use a blue color palette
    legend=False          # Hide legend (not needed due to distinct x-axis labels)
)

# Add plot title and axis labels
plt.title("Phase 4 Outcomes: Performance Metrics", fontsize=16)
plt.ylabel("Impact Score (out of 100)")
plt.xlabel("Outcome Category")
plt.ylim(0, 100)  # Set y-axis limit for better scaling

# Annotate each bar with its impact score
for index, row in data.iterrows():
    plt.text(index, row['Impact Score'] + 1, str(row['Impact Score']),
             ha='center', va='bottom', fontweight='bold')

# Optimize layout and show the plot
plt.tight_layout()
plt.show()
