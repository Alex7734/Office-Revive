import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import random
import numpy as np
from matplotlib import rcParams

#Popularitate in timp


attendanceEvents = pd.DataFrame({
    'Attendance': [6, 10, 8, 2, 9, 1]},
    index=['Football', 'Video games', 'Karting', 'Movies', 'Laser tag', 'Hiking']
)

attendancePeople = pd.DataFrame({
    'Attendance': [7, 5, 8, 2, 1, 6, 3, 8, 2, 10, 1]
}, index=['Mihai', 'George', 'Bella', 'Terry', 'Lola', 'Michelle', 'Sharon', 'Josh', 'Frank', 'Vinnie', 'Ron'])

ratings = pd.DataFrame({
    'OverallInterests': ['Football', 'Video games', 'Karting', 'Movies', 'Laser tag', 'Hiking'],
    'Mihai': [4, 5, 6, 8, 9, 10],
    'George': [2, 5, 1, 3, 8, 9],
    'Bella': [10, 3, 8, 5, 4, 2],
    'Terry': [4, 5, 6, 3, 1, 7],
    'Lola': [6, 10, 3, 7, 1, 2],
    'Michelle': [7, 8, 2, 4, 5, 9],
    'Sharon': [3, 10, 1, 2, 5, 9],
    'Josh': [6, 4, 9, 1, 2, 7],
    'Frank': [6, 10, 3, 7, 1, 2],
    'Vinnie': [4, 1, 3, 8, 9, 7],
    'Ron': [9, 2, 8, 1, 6, 3]
})

print(ratings)

# Prezenta
# Popularitate
# Puncte
# Gender by activity
# Likes by activity


rcParams.update({'figure.autolayout': True})

i = 1
for person in ['Bella', 'Ron']:
    r = random.random()
    g = random.random()
    b = random.random()
    ratings.plot(kind='bar', x='OverallInterests', y=person, color=(r, g, b), width=0.9)
    plt.savefig(f'test{i}.png')
    i += 1

attendanceEvents.plot.pie(y='Attendance')
plt.savefig(f'attendanceEvent.png')
attendancePeople.plot.pie(y='Attendance')
plt.savefig(f'attendancePeople.png')

plt.show()
