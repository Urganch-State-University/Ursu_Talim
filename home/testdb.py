
from django.shortcuts import render
from django.db import connection

def get_data(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM your_table_name")
        data = cursor.fetchall()

    return render(request, 'your_template.html', {'data': data})
