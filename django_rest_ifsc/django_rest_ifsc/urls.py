
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from api.views import ImportCsv
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^import/', ImportCsv.as_view(), name='import'),
    url(r'^api/', include('api.urls'))

]
