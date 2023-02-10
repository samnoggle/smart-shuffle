# I just need a pie chart showing the importance of all the feature groups

import matplotlib.pyplot as plt

# Data to plot
labels = 'Track Features', 'Metadata', 'Metrics', 'Contextual Data'
sizes = [215, 130, 245, 210] # not correct yet

# Plot
plt.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=True, startangle=140)

plt.axis('equal')
plt.show()
plt.savefig('FeatureGroupProportionsPie.pdf')