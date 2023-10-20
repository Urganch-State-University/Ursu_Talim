from itertools import groupby
from decimal import Decimal  # Make sure to import Decimal

data = [
    ('Xorijiy til (ingliz tili)', '304799', 'Tanlov', 'Majburiy fanlar', 60, Decimal('2.0')),
    ('Xorijiy til (nemis tili)', '304799', 'Tanlov', 'Majburiy fanlar', 60, Decimal('2.0')),
    ('Xorijiy til (fransuz tili)', '304799', 'Tanlov', 'Majburiy fanlar', 60, Decimal('2.0')),
    ('Oliy matematika 1 (Chiziqli algebra va analitik geometriya)', None, 'Majburiy', 'Majburiy fanlar', 150, Decimal('5.0')),
    ('O‘zbekistonning eng yangi tarixi', None, 'Majburiy', 'Majburiy fanlar', 60, Decimal('2.0')),
    ('Dasturlash asoslari', None, 'Majburiy', 'Majburiy fanlar', 330, Decimal('11.0')),
    ('Jismoniy tarbiya va sport', None, 'Majburiy', 'Majburiy fanlar', 60, Decimal('2.0')),
    ('Kompyuterning fizik asoslari', None, 'Majburiy', 'Tanlov fanlar', 240, Decimal('8.0')),
    ('O‘zbek tili', '314929', 'Tanlov', 'Majburiy fanlar', 60, Decimal('2.0')),
    ('Rus tili', '314929', 'Tanlov', 'Majburiy fanlar', 60, Decimal('2.0')),
    ('Algoritmlar va berilganlar strukturasi', None, 'Majburiy', 'Tanlov fanlar', 210, Decimal('7.0')),
    ('Malakaviy amaliyot', None, 'Majburiy', 'Tanlov fanlar', 60, Decimal('2.0')),
    ("Ma'lumotlar bazasi", None, 'Majburiy', 'Tanlov fanlar', 210, Decimal('7.0')),
    ('Oliy matematika 2 (Matematik analiz)', None, 'Majburiy', 'Tanlov fanlar', 150, Decimal('5.0')),
    ('Dasturlash asoslari', None, 'Majburiy', 'Tanlov fanlar', 210, Decimal('7.0'))
]

# Sort the data based on the 1st index of each tuple and provide a default value ('') for None
sorted_data = sorted(data, key=lambda x: x[1] or '')

# Group the sorted data by the 1st index using itertools.groupby
groups = groupby(sorted_data, key=lambda x: x[1] or '')

# Convert the groups into a list of lists
result = [list(group) for _, group in groups]

print(result)
# Print the result
for group in result:
    print(group)