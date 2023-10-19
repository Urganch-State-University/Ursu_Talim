import datetime

from django.http import JsonResponse
from django.shortcuts import render
from django.db import connection

from home.forms import MyForm


# Create your views here.


def homeview(request):
    return render(request, 'dashboard.html')


def transfersview(request):
    print(request)
    with connection.cursor() as cursor:
        cursor.execute(""" SELECT * FROM e_department WHERE "_structure_type"='11' AND "id" NOT IN (77, 8, 7, 6);""")
        faculties_list = cursor.fetchall()
        cursor.execute(""" SELECT * FROM h_education_form ORDER BY code;""")
        education_form_list = cursor.fetchall()

    bugungi_yil=datetime.datetime.now().year
    entered_year=[{"year":i,"name":f"{i}-{i+1}"} for i in range(bugungi_yil-5,bugungi_yil+1)]


    context={
        "faculties_list":faculties_list,
        "education_form_list":education_form_list,
        "entered_year":entered_year,

    }






    return render(request, 'pages/tables/transfers.html',context)


def ajax_get_options(request):
    print(request)
    fakultet = request.GET.get('fakultet', None)
    talim_shakli = request.GET.get('talim_shakli', None)
    qabul_yili = request.GET.get('qabul_yili', None)
    options={}
    with connection.cursor() as cursor:
        cursor.execute(f""" SELECT * FROM e_curriculum WHERE "_department"='{fakultet}' AND "_education_form"='{talim_shakli}' AND "_education_year"='{qabul_yili}';""")
        data = cursor.fetchall()
        options=[{f"{i[0]}":i[1]} for i in data]



    return JsonResponse({'curriculum_list': options})


