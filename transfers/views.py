import datetime
import json
from io import BytesIO

from django.http import JsonResponse
from django.shortcuts import render
from django.db import connection
from itertools import groupby
from django.views import View
from xhtml2pdf import pisa
from django.http import HttpResponse
from django.template.loader import get_template

def showgpaview(request):
    if request.method == "POST":
        try:

            kredit_list = request.POST.getlist('credit[]')
            baho_list: list = request.POST.getlist('grade[]')
            name_list: list = request.POST.getlist('subject_name[]')


            semestr_list: list = request.POST.getlist('semestr[]')
            block_list: list = request.POST.getlist('block[]')



            kredit_list = list(map(float, kredit_list))
            baho_list = [float('2') if item in ['', '0', '1'] else float(item) for item in baho_list]

            kredit_summa = sum(kredit_list)
            result = 0
            for i in range(len(kredit_list)):
                result += kredit_list[i] * baho_list[i]

            gpa = result / kredit_summa
            gpa = "%.2f" % gpa

            # print(kredit_list)
            # print(baho_list)

            subject_list = []
            kredit_summa_r = 0
            for i in range(len(baho_list)):
                if baho_list[i] == 2:
                    subject_list.append(name_list[i])
                    kredit_summa_r += kredit_list[i]
            # print(subject_list, kredit_summa_r)
            context = {
                'gpa': gpa,
                "gpa_subjects_list": subject_list,
                "kredit_sum": kredit_summa_r,
            }

            return JsonResponse(context)


        except json.JSONDecodeError as e:
            print(f"JSON xato: {e}")
    return JsonResponse({})


def showmainformview(request):
    if request.method == 'POST':
        try:
            fakultet = request.POST.get('fakultet')
            talim_shakli = request.POST.get('talim_shakli', None)
            qabul_yili = request.POST.get('qabul_yili', None)
            yonalish = request.POST.get('yonalish', None)
            semester = request.POST.get('semester', None)

            print(fakultet, talim_shakli, qabul_yili, yonalish, semester)
            if fakultet and talim_shakli and qabul_yili and yonalish and semester:
                with connection.cursor() as cursor:
                    cursor.execute(
                        f""" select es._translations->>'name_uz' as fannomi, ecs.in_group, hs.name as fanturi, hsb.name as fanbloki,  ecs.total_acload, ecs.credit, cast (ecs._semester as int)-10 as semester from e_curriculum_subject as ecs 
                inner join h_subject_type as hs on hs.code = ecs._subject_type
                inner join h_subject_block as hsb on ecs._curriculum_subject_block=hsb.code
                inner join e_subject as es on es.id = ecs._subject
                where ecs._curriculum={yonalish} and ecs._semester < '{semester}'
                order by ecs._semester, ecs.in_group""")
                    data = cursor.fetchall()
                    groups = groupby(data, key=lambda x: x[1])

                    # Convert the groups into a list of tuples
                    result = [(key, list(group)) for key, group in groups]

                    # Print the result
                    subjects_list = []
                    for key, group in result:
                        if key != None:
                            subjects_list.append(group)
                        else:
                            for i in group:
                                subjects_list.append(i)

                context = {
                    "subjects_list": subjects_list,
                }

                return JsonResponse(context)


        except json.JSONDecodeError as e:
            print(f"JSON xato: {e}")

    return JsonResponse({})


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


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("utf-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


class DownloadPDF(View):
    def post(self, request, *args, **kwargs):

        kredit_list = request.POST.getlist('credit[]')
        baho_list: list = request.POST.getlist('grade[]')
        name_list: list = request.POST.getlist('subject_name[]')

        semestr_list: list = request.POST.getlist('semestr[]')
        block_list: list = request.POST.getlist('block[]')

        print(semestr_list)
        print(block_list)

        kredit_list = list(map(float, kredit_list))
        baho_list = [float('2') if item in ['', '0', '1'] else float(item) for item in baho_list]

        kredit_summa = sum(kredit_list)
        result = 0
        for i in range(len(kredit_list)):
            result += kredit_list[i] * baho_list[i]

        gpa = result / kredit_summa
        gpa = "%.2f" % gpa

        subject_list = []
        kredit_summa_r = 0
        for i in range(len(baho_list)):
            if baho_list[i] == 2:
                subject_list.append((name_list[i],block_list[i],baho_list[i], kredit_list[i]))
                kredit_summa_r += kredit_list[i]

        # subjects_info = [(name_list[i], kredit_list[i], baho_list[i]) for i in range(len(baho_list))]

        current_date = datetime.datetime.now()
        context = {
            "given_date": current_date.strftime('%d.%m.%Y'),
            "subjects_info": subject_list,
            "semestr_list":semestr_list,
            "block_list":block_list,
            "fakultet": request.POST.get('fakultet'),
            "talim_shakli": request.POST.get('talim_shakli'),
            "qabul_yili": request.POST.get('qabul_yili'),
            "yonalish": request.POST.get('yonalish'),
            "gpa": gpa,
        }
        pdf = render_to_pdf('pages/pdf_generate/GPA.html', context)
        response = HttpResponse(pdf, content_type='application/pdf')
        file_id = current_date.strftime('%Y_%m_%d_%H_%M_S')
        filename = f"Invoice_{file_id}.pdf"
        content = f"attachment; filename={filename}"
        response['Content-Disposition'] = content
        return response


class ViewPDF(View):
    def get(self, request, *args, **kwargs):
        pdf = render_to_pdf('pages/pdf_generate/GPA.html', {})
        return HttpResponse(pdf, content_type='application/pdf')
