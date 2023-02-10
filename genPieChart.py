# I just need a pie chart showing the importance of all the feature groups

import matplotlib.pyplot as plt

# Data to plot
labels = 'Spotify Data', 'Metrics', 'Contextual Data'
sizes = [0.014088, 0.282283, 0.703629] # not correct yet

# Plot
plt.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=False, startangle=140)

plt.axis('equal')
plt.show()
plt.savefig('FeatureGroupProportionsPie.pdf')