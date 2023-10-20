import datetime

from django.http import JsonResponse
from django.shortcuts import render
from django.db import connection
from decouple import config
from home.forms import MyForm
import requests
from itertools import groupby


# Create your views here.


def homeview(request):
    return render(request, 'dashboard.html')


def transfersview(request):
    with connection.cursor() as cursor:
        cursor.execute(""" SELECT * FROM e_department WHERE "_structure_type"='11' AND "id" NOT IN (77, 8, 7, 6);""")
        faculties_list = cursor.fetchall()
        cursor.execute(""" SELECT * FROM h_education_form WHERE code in ('11','13','15','16','17') ORDER BY code ;""")
        education_form_list = cursor.fetchall()

    bugungi_yil = datetime.datetime.now().year
    entered_year = [{"year": i, "name": f"{i}-{i + 1}"} for i in range(bugungi_yil - 5, bugungi_yil + 1)]

    context = {
        "faculties_list": faculties_list,
        "education_form_list": education_form_list,
        "entered_year": entered_year,

    }

    if request.method == 'POST':
        fakultet = request.POST.get('fakultet')
        talim_shakli = request.POST.get('talim_shakli', None)
        qabul_yili = request.POST.get('qabul_yili', None)
        yonalish = request.POST.get('yonalish', None)
        semester = request.POST.get('semester', None)

        print(fakultet, talim_shakli, qabul_yili, yonalish, semester)
        if fakultet and talim_shakli and qabul_yili and yonalish and semester:
            with connection.cursor() as cursor:
                cursor.execute(
                    f""" select es._translations->>'name_uz' as fannomi, ecs.in_group, hs.name as fanturi, hsb.name as fanbloki,  ecs.total_acload, ecs.credit  from e_curriculum_subject as ecs 
inner join h_subject_type as hs on hs.code = ecs._subject_type
inner join h_subject_block as hsb on ecs._curriculum_subject_block=hsb.code
inner join e_subject as es on es.id = ecs._subject
where ecs._curriculum={yonalish} and ecs._semester < '{semester}'
order by ecs._semester, ecs.in_group""")
                data = cursor.fetchall()
                subjects_list=[]
                sorted_data = sorted(data, key=lambda x: x[1] or '')
                groups = groupby(sorted_data, key=lambda x: x[1] or '')
                for i in groups:
                    subjects_list.append([f"{i[0]}",list(i[1])])
                print(subjects_list)


            context = {
                "faculties_list": faculties_list,
                "education_form_list": education_form_list,
                "entered_year": entered_year,
                "subjects_list": subjects_list,

            }

            return render(request, 'pages/tables/transfers.html', context)
    return render(request, 'pages/tables/transfers.html', context)


def ajax_get_options(request):
    print(request)
    fakultet = request.GET.get('fakultet', None)
    talim_shakli = request.GET.get('talim_shakli', None)
    qabul_yili = request.GET.get('qabul_yili', None)

    curriculum_list = {}
    semester_list = {}
    with connection.cursor() as cursor:
        cursor.execute(
            f""" SELECT * FROM e_curriculum WHERE "_department"='{fakultet}' AND "_education_form"='{talim_shakli}' AND "_education_year"='{qabul_yili}';""")
        data = cursor.fetchall()
        for i in data:
            curriculum_list.update({f"{i[0]}": f"{i[1]}"})
    current_year = datetime.datetime.now().year
    current_month = datetime.datetime.now().month
    if current_month >= 7 and current_month <= 12:
        for j in range(1, 2 * (current_year - int(qabul_yili)) + 2):
            semester_list.update({f"{10 + j}": f"{j}-Semester"})
    else:
        for j in range(1, 2 * (current_year - int(qabul_yili)) + 3):
            semester_list.update({f"{10 + j}": f"{j}-Semester"})
    return JsonResponse({'curriculum_list': curriculum_list, 'semester_list': semester_list})
