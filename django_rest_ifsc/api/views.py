from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import HttpResponseRedirect, render
from django.urls import reverse
from django.views import View
from .models import Bank, Branch
from .serializers import BSerializer
import csv

class ImportCsv(View):
    def get(self, request):
        return render(request, 'main.html')

    def post(self, request):
        csv_file = request.FILES.get('csv_file')
        decoded_file = csv_file.read().decode('utf-8').splitlines()
        reader = csv.DictReader(decoded_file)
        count = 0

        for row in reader:
            bank_name = row.get('bank_name')
            ifsc = row.get('ifsc')
            branch = row.get('branch')
            address = row.get('address')
            city = row.get('city')
            district = row.get('district')
            state = row.get('state')
            print("IFSC-- {}".format(ifsc))
            if not ifsc:
                break
            bank_object, created = Bank.objects.get_or_create(
                name=bank_name
            )
            branch_defaults = {
                'name': branch,
                'bank': bank_object,
                'address': address,
                'city': city,
                'district': district,
                'state': state
            }

            branch_object, created = Branch.objects.update_or_create(
                ifsc=ifsc, defaults=branch_defaults
            )
            if created:
                print("row created{}".format(branch_defaults))



            count += 1
        messages.success(request, "{} rows imported.".format(count))

        return render(request, 'main.html')


class DetailView(View):
    def get(self, request, ifsc):
        branch = Branch.objects.filter(ifsc__iexact=ifsc).first()
        serializer = BSerializer(branch)
        return JsonResponse(serializer.data, safe=False)


class ListView(View):
    def get(self, request, city, bank):
        branch_qset = Branch.objects.filter(
            city__iexact=city, bank__name__icontains=bank)
        serializer = BSerializer(branch_qset, many=True)
        return JsonResponse(serializer.data, safe=False)

#
