from django import forms
from django.db import connection

class MyForm(forms.Form):
    FACULTIES=[]
    with connection.cursor() as cursor:
        cursor.execute(""" SELECT * FROM e_department WHERE "_structure_type"='11' AND "id" NOT IN (77, 8, 7, 6);""")
        data = cursor.fetchall()
        FACULTIES = [(i[2],i[2]) for i in data]



    CHOICES = (
        ('value1', 'Option 1'),
        ('value2', 'Option 2'),
        ('value3', 'Option 3'),
        ('value4', 'Option 4'),
        ('value5', 'Option 5'),
    )

    Fakultetlar1 = forms.ChoiceField(choices=FACULTIES, label='Fakultetlar')

    select2 = forms.ChoiceField(choices=CHOICES, label='Select 2')
    select3 = forms.ChoiceField(choices=CHOICES, label='Select 3')
    select4 = forms.ChoiceField(choices=CHOICES, label='Select 4')
    select5 = forms.ChoiceField(choices=CHOICES, label='Select 5')
