from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import Livreto
from .controller import PDFController
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.contrib import messages

def livreto_index(request):
    filter = request.GET.get('filter')
    search = request.GET.get('search')
    if filter:
        livretos = Livreto.objects.filter(system=filter)
    elif search:
        livretos = Livreto.objects.filter(
            Q(name__icontains=search)|
            Q(description__icontains=search)|
            Q(system__icontains=search)
        )
    else:
        livretos = Livreto.objects.all()
    context = {
        'livretos': livretos,
        'filter': filter,
        'search': search,
        'systems': Livreto._meta.get_field('system').choices
    }
    return render(request, 'livreto.html', context=context)

def livreto_infos(request, system):
    livretos = [livreto.json() for livreto in Livreto.objects.filter(system=system, active=True)]
    return JsonResponse(livretos, safe=False)

def livreto_register(request):
    if request.method != "POST":
        raise
    # form html
    form_name = request.POST.get('name')
    form_description = request.POST.get('description')
    form_system = request.POST.get('system')
    form_pdf = request.FILES['pdf']
    # create livreto
    Livreto.objects.create(
        name = form_name,
        description = form_description,
        system = form_system,
        pdf=form_pdf
    )
    messages.success(request, "Livreto criado com sucesso!")
    return redirect('livreto_index')

def livreto_update(request, pk):
    if request.method != "POST":
        raise
    # get livreto
    livreto = get_object_or_404(Livreto, pk=pk)
    # form html
    form_name = request.POST.get('name')
    form_description = request.POST.get('description')
    form_system = request.POST.get('system')
    if 'pdf' in request.FILES:
        form_pdf = request.FILES['pdf']
    else:
        form_pdf = None
    # change livreto
    livreto.name = form_name
    livreto.description = form_description
    livreto.system = form_system
    if form_pdf:
        livreto.pdf = form_pdf
    livreto.save()
    messages.success(request, "Livreto editado com sucesso!")
    return redirect('livreto_index')

def livreto_delete(request, pk):
    livreto = get_object_or_404(Livreto, pk=pk)
    livreto.delete()
    messages.success(request, "Livreto deletado com sucesso!")
    return redirect('livreto_index')

def livreto_render(request, slug):
    livreto = get_object_or_404(Livreto, slug=slug)
    controller = PDFController(livreto.pdf)
    return render(
        request,
        'livreto_render.html',
        context={'livreto': livreto, 'pages': range(controller.pages)}
    )

def livreto_render_pdf(request, slug):
    livreto = get_object_or_404(Livreto, slug=slug)
    response = HttpResponse(open(livreto.pdf.path, 'rb'), content_type='application/pdf')
    response['Content-Disposition'] = f'inline;filename={livreto.slug}.pdf'
    return response

@csrf_exempt
def livreto_render_page_as_image(request, slug, num, dpi=100):
    livreto = get_object_or_404(Livreto, slug=slug)
    controller = PDFController(livreto.pdf)
    image_bytes = controller.get_page_as_image(num, dpi=dpi)
    response = HttpResponse(image_bytes, content_type='image/png')
    response['Content-Disposition'] = f'inline; filename="{livreto.slug}-page-{num}.png"'
    return response