from django.shortcuts import render
from django.db.models import Q
from django.views.generic.list import ListView
from django.views.generic import CreateView
from django.views.generic.detail import DetailView
from .models import Padron_electoral, Distelec

# Create your views here.

class listViewData(ListView):
    """
    This listView is implemented in order to show the complete padron electoral.
    """

    template_name = 'test.html'
    model = Padron_electoral
    paginate_by = 15  # if pagination is desired
    queryset = Padron_electoral.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class distelecListView(ListView):
    """
    This listView is implemented to show the complete distelec
    """

    template_name = 'distelec.html'
    model = Distelec
    paginate_by = 15
    queryset = Distelec.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class searchListView(ListView):
    """
    This listView is implemented to search some data in padron electoral.
    You can search a person by cedula, codelec and name.
    """

    model = Padron_electoral
    template_name = 'filterData.html'
    paginate_by = 15

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self):
        searchData = self.request.GET.get('search')
        print(len(searchData))
        if len(searchData) == 9:
            queryset = Padron_electoral.objects.filter(cedula__icontains=searchData)
            return queryset
        if len(searchData) == 6:
            queryset = Padron_electoral.objects.filter(codelec__icontains=searchData)
            return queryset
        if type(searchData) == str:
            queryset = Padron_electoral.objects.filter(nombre__icontains=searchData)
            return queryset

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

""" 
def getInfoDistelec(request):
    info = request.GET.get('codele')
    query = Distelec.objects.filter(codele=info)
    return render(request, 'distelec.html', context={"query": query})
"""


def get_voters_by_person(codelec):
    """
    This method is used in the class called info_by_person, this class is a detailView.
    With the parameter codelec you can know the total voters with the same codelec, also number de women and men.
    """

    total_voters = Padron_electoral.objects.filter(Q(codelec=codelec)).count()
    total_voters_female = Padron_electoral.objects.filter(Q(codelec=codelec)&Q(sexo=2)).count()
    total_voters_male = Padron_electoral.objects.filter(Q(codelec=codelec) & Q(sexo=1)).count()
    return {'total': total_voters, 'female':total_voters_female, 'male':total_voters_male}

class info_by_person(DetailView):
    """
    This detailView provider information about each person that has been searched.
    In this case you will see the codelec of the selected person, and with the method get_voters_by_person you will see
    total voters, also number de women and men
    """

    model = Padron_electoral
    template_name = 'infoByPerson.html'
    context_object_name = 'info_person'


    def get_context_data(self, **kwargs):
        context = super(info_by_person,self).get_context_data(**kwargs)
        if kwargs['object'] != None:
            info_distelec = Distelec.objects.get(codele=kwargs['object'].codelec)
            context['infor_distelec'] = info_distelec
            context['voters'] = get_voters_by_person(kwargs['object'].codelec)
            print(context)
            return context

    def get_object(self):
        idPerson = self.kwargs.get('cedula')
        data = Padron_electoral.objects.get(cedula=idPerson)
        return data

def get_distelec_count(codele):
    """
    This method is used in the class called info_by_distelec, this class is a detailView.
    With the parameter codelec you can know the total voters with the same codelec, also number de women and men.
    """

    total_person = Padron_electoral.objects.filter(Q(codelec=codele)).count()
    total_female = Padron_electoral.objects.filter(Q(codelec=codele) & Q(sexo=2)).count()
    total_male = Padron_electoral.objects.filter(Q(codelec=codele) & Q(sexo=1)).count()
    return {"total_female":total_female, 'total_male':total_male, 'total_person':total_person}


class info_by_distelec(DetailView):
    """
    The detailView provider information about each row of the distelec.
    You will see the codelec and the result of the method used called get_distelec_count
    """

    model = Distelec
    template_name = 'infoByDistelec.html'
    context_object_name = 'info_distelec'

    def get_context_data(self, **kwargs):
        context = super(info_by_distelec,self).get_context_data(**kwargs)
        if kwargs['object']!=None:
            context['info']=get_distelec_count(kwargs['object'].codele)
            context['cod']= kwargs['object'].codele
            print(context)
            return context

    def get_object(self):
        codelect = self.kwargs.get('codele')
        cod = Distelec.objects.get(codele=codelect)
        return cod

class personCreateView(CreateView):
    template_name = 'create_person.html'
    #form_class = PersonCreateForm

    def get_initial(self, *args, **kwargs):
        initial= super(personCreateView, self).get_initial(**kwargs)
        initial['tittle']='my tittle'
        return initial


#CONSULTAS
#1. cantidad de todos los votantes

def getQuantityVoters(request):
    """
    This method is used for different functions, to know the quantity of people has the same fecha_caducidad cedula
    of the president.
    On the other hand, you will know the total voters, female and male by each province.
    """
    #por Costa Rica
    quantity = Padron_electoral.objects.all().count()
    quantityF = Padron_electoral.objects.filter(sexo=2).count()
    quantityM = Padron_electoral.objects.filter(sexo=1).count()
    #por provincia
    quantitySJ = Padron_electoral.objects.filter(Q(codelec__startswith='1')).count()
    quantityMSJ = Padron_electoral.objects.filter(Q(codelec__startswith="1")& Q(sexo=2)).count()
    quantityHSJ = Padron_electoral.objects.filter(Q(codelec__startswith="1")& Q(sexo=1)).count()
    quantityA = Padron_electoral.objects.filter(Q(codelec__startswith='2')).count()
    quantityMA = Padron_electoral.objects.filter(Q(codelec__startswith='2')& Q(sexo=2)).count()
    quantityHA = Padron_electoral.objects.filter(Q(codelec__startswith='2') & Q(sexo=1)).count()
    quantityC = Padron_electoral.objects.filter(Q(codelec__startswith='3')).count()
    quantityMC = Padron_electoral.objects.filter(Q(codelec__startswith='3')& Q(sexo=2)).count()
    quantityHC = Padron_electoral.objects.filter(Q(codelec__startswith='3')& Q(sexo=1)).count()
    quantityH = Padron_electoral.objects.filter(Q(codelec__startswith='4')).count()
    quantityMH = Padron_electoral.objects.filter(Q(codelec__startswith='4')& Q(sexo=2)).count()
    quantityHH = Padron_electoral.objects.filter(Q(codelec__startswith='4')& Q(sexo=1)).count()
    quantityG = Padron_electoral.objects.filter(Q(codelec__startswith='5')).count()
    quantityMGu = Padron_electoral.objects.filter(Q(codelec__startswith='5')& Q(sexo=2)).count()
    quantityHGu = Padron_electoral.objects.filter(Q(codelec__startswith='5')& Q(sexo=1)).count()
    quantityP = Padron_electoral.objects.filter(Q(codelec__startswith='6')).count()
    quantityMP = Padron_electoral.objects.filter(Q(codelec__startswith='6')& Q(sexo=2)).count()
    quantityHP = Padron_electoral.objects.filter(Q(codelec__startswith='6')& Q(sexo=1)).count()
    quantityL = Padron_electoral.objects.filter(Q(codelec__startswith='7')).count()
    quantityML = Padron_electoral.objects.filter(Q(codelec__startswith='7')& Q(sexo=2)).count()
    quantityHL = Padron_electoral.objects.filter(Q(codelec__startswith='7')& Q(sexo=1)).count()
    #information from president 110600078
    presi_id = '207000998'
    info_presi = Padron_electoral.objects.get(cedula__iexact=presi_id)
    fecha_caduc_presi = Padron_electoral.objects.filter(Q(fecha_caducidad__iexact='20280524')).count()

    print(fecha_caduc_presi, "info presi")

    context ={"quantity": quantity, "quantityFG": quantityF, "quantityMG": quantityM,
              "quantitySJ":quantitySJ, "quantityMSJ": quantityMSJ, "quantityHSJ": quantityHSJ,
              "quantityA": quantityA,"quantityMA": quantityMA,"quantityHA": quantityHA,
              "quantityC": quantityC,"quantityMC": quantityMC,"quantityHC": quantityHC,
              "quantityH": quantityH,"quantityMH": quantityMH,"quantityHH": quantityHH,
              "quantityG": quantityG,"quantityMGu": quantityMGu,"quantityHGu": quantityHGu,
              "quantityP": quantityP,"quantityMP": quantityMP,"quantityHP": quantityHP,
              "quantityL": quantityL,"quantityML": quantityML,"quantityHL": quantityHL,
              "fecha_caduc_presi":fecha_caduc_presi}

    return render(request, 'generic.html', context)

