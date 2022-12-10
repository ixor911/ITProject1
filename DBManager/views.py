import csv
import json
from io import StringIO, BytesIO

from django.shortcuts import render, get_object_or_404, redirect
from .serializers import *
from .models import *
from .forms import *
import re
from rest_framework import viewsets

from django.http import HttpResponse
from rest_framework.generics import GenericAPIView


def index(request):
    return render(request, "home.html", {})


# ================ Table ===================
def tables_home(request):
    tables = Table.objects.all()

    context = {
        'tables': tables
    }

    return render(request, "table/table_home.html", context)


def tables_get_table(request, id):
    table = get_object_or_404(Table, id=id)
    table_data = list(table.data.values())

    table_values = []
    for data in table_data:
        table_values.append(data.get('data'))

    first_col = []
    if len(table_values) > 0:
        first_col = table_values[0]

    context = {
        'table': table,
        'table_values': table_values,
        'first_col': first_col,
    }

    return render(request, "table/table_detail.html", context)


def tables_create_table(request):
    form = TableForm()

    if request.method == "POST":
        form = TableForm(request.POST)
        if form.is_valid():
            form.cleaned_data['database'] = Database.objects.first()
            Table.objects.create(**form.cleaned_data)
            return redirect('../')

    context = {
        "form": form,
    }

    return render(request, "table/table_create.html", context)


def tables_delete_table(request, id):
    table = get_object_or_404(Table, id=id)

    if request.method == "POST":
        table.delete()
        return redirect('../')

    context = {
        "table": table,
    }

    return render(request, "table/table_delete.html", context)


# ================ Table Column ===================
def tables_add_col(request, id):
    table = get_object_or_404(Table, id=id)

    if request.method == "POST":
        validation = [False, False]

        if request.POST['name'].replace(" ", "") != "":
            if request.POST['name'] not in table.data.keys():
                validation[0] = True

        if request.POST['type'] is not None:
            validation[1] = True

        if False not in validation:
            table.data[request.POST['name']] = {
                "type": request.POST['type'],
                "data": []
            }

            none_value = None
            if request.POST['type'] == 'int':
                none_value = 0
            elif request.POST['type'] == 'float':
                none_value = 0.0
            elif request.POST['type'] == 'char':
                none_value = ''
            elif request.POST['type'] == 'string':
                none_value = ""
            elif request.POST['type'] == 'money':
                none_value = "$0"
            elif request.POST['type'] == 'money_intv':
                none_value = "$0-0"

            for elem in list(table.data.values())[0].get('data'):
                table.data.get(request.POST['name'])["data"].append(none_value)

            table.save()

            return redirect("./")

    return render(request, "table/table_add_col.html", {})


def tables_edit_col(request, id, col_name):
    table = get_object_or_404(Table, id=id)

    if col_name not in table.data:
        return redirect("../")

    if request.method == 'POST':
        if request.POST['name'].replace(" ", "") != "":
            table.data[request.POST['name']] = table.data.pop(col_name)
            table.save()
            return redirect('../')

    context = {
        "col_name": col_name
    }

    return render(request, "table/table_edit_col.html", context)


def tables_delete_col(request, id, col_name):
    table = get_object_or_404(Table, id=id)

    if col_name not in table.data:
        return redirect("../")

    if request.method == 'POST':
        table.data.pop(col_name)
        table.save()
        return redirect('../')

    context = {
        "col_name": col_name,
        "col_data": table.data.get(col_name).get('data')
    }

    return render(request, "table/table_delete_col.html", context)


# ================ Table Row ===================
def tables_add_row(request, id):
    table = get_object_or_404(Table, id=id)
    cols = table.data.keys()

    context = {
        "cols": cols,
        "data": [],
        "types": []
    }

    if request.method == 'POST':
        validation = True

        for key in cols:
            col = table.data.get(key)
            inp = request.POST[key]

            context.get('data').append(inp)
            context.get('types').append(table.data.get(key).get('type'))

            if col.get('type') == "int":
                try:
                    table.data[key].get('data').append(int(inp))
                except:
                    validation = False

            elif col.get('type') == "float":
                try:
                    table.data[key].get('data').append(float(inp))
                except:
                    validation = False

            elif col.get('type') == "char":
                if len(inp) < 2:
                    table.data[key].get('data').append(inp)
                else:
                    validation = False

            elif col.get('type') == "string":
                table.data[key].get('data').append(inp)

            elif col.get('type') == "money":
                if bool(re.fullmatch("^\D{1}\s?[0-9]+[.]?[0-9]*", inp)): # r 1000.45, $123
                    table.data[key].get('data').append(inp)
                else:
                    validation = False

            elif col.get('type') == "money_intv":
                if bool(re.fullmatch("^\D{1}\s?[0-9]+.?[0-9]*\s?[-]{1}\s?[0-9]+.?[0-9]*", inp)): # $ 56723 - 34289
                    strs = re.findall("[0-9]+[.]?[0-9]*", inp)

                    if float(strs[0]) <= float(strs[1]):
                        table.data[key].get('data').append(inp)
                    else:
                        validation = False
                else:
                    validation = False

        if validation:
            table.save()
            return redirect('./')

    else:
        for key in cols:
            context.get('data').append("")
            context.get('types').append(table.data.get(key).get('type'))

    return render(request, "table/table_add_row.html", context)


def tables_del_row(request, id, row_num):
    table = get_object_or_404(Table, id=id)
    keys = list(table.data.keys())
    values = []

    for diction in table.data.values():
        values.append(diction.get('data'))

    if row_num not in range(0, len(values[0])):
        return redirect("../")

    if request.method == 'POST':
        for key in keys:
            table.data.get(key).get('data').pop(row_num)

        table.save()
        return redirect("../")

    context = {
        "keys": keys,
        "values": values,
        "row_num": row_num
    }

    return render(request, "table/table_delete_row.html", context)


# ================ Database ===================
def export_to_csv(request):
    database = Database.objects.first()
    tables = Table.objects.all()
    response = HttpResponse('text/csv')
    response['Content-Disposition'] = f'attachment; filename={database.name}.csv'
    writer = csv.writer(response)
    writer.writerow(['name', 'data', 'database'])
    table_list = tables.values_list('name', 'data', 'database')

    for table in table_list:
        writer.writerow(table)

    return response


def database_set(request):
    databases = Database.objects.all()
    tables = Table.objects.all()

    if request.method == "POST":
        init_file = request.FILES['database_file']
        dec_file = init_file.read().decode('utf-8')
        reader = csv.DictReader(StringIO(dec_file))
        try:
            data = [line for line in reader]
        except:
            return redirect("/")

        for database in databases:
            database.delete()

        for table in tables:
            table.delete()

        database = Database()
        database.name = init_file.name.split('.')[0]
        database.save()

        for row in data:
            table = Table()

            table.name = row.get('text/csvname')
            table.database = database
            table.data = json.loads(row.get('data').replace("'", '"'))

            table.save()

        return redirect("/table")

    return render(request, "database_set.html", {})


def database_clear(request):
    databases = Database.objects.all()
    tables = Table.objects.all()

    for database in databases:
        database.delete()

    for table in tables:
        table.delete()

    return redirect("/table")


# ================ REST api ===================
class TableViewSet(viewsets.ModelViewSet):
    print(Table.objects.all().first)
    queryset = Table.objects.all().order_by('name')
    serializer_class = TableSerializer


class API(GenericAPIView):
    serializer_class = TableSerializer

