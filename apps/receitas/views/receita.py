from django.shortcuts import render, get_list_or_404, get_object_or_404, redirect
from ..models import Receita
from django.contrib.auth.models import User
from django.contrib import auth, messages
from usuarios.views import campo_vazio
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.
def index(request):
    """Busca todas as receitas publicadas com paginação"""
    receitas= Receita.objects.order_by('-data_receita').filter(publicada=True)
    paginator = Paginator(receitas, 3)
    page = request.GET.get('page')
    receitas_por_pagina = paginator.get_page(page)

    dados= {
        'receitas': receitas_por_pagina
    }

    return render(request, 'receitas/index.html', dados)

def receita(request, receita_id):
    """Busca uma receita pelo id"""
    receita = get_object_or_404(Receita, pk=receita_id)

    receita_a_exibir = {
        'receita': receita
    }

    return render(request, 'receitas/receita.html', receita_a_exibir)

def cria_receita(request):
    """Cadastra uma receita"""
    if request.method == 'POST':
        nome_receita = request.POST['nome_receita']
        ingredientes = request.POST['ingredientes']
        modo_preparo = request.POST['modo_preparo']
        tempo_preparo = request.POST['tempo_preparo']
        rendimento = request.POST['rendimento']
        categoria = request.POST['categoria']
        foto_receita = request.FILES['foto_receita']

        if campo_vazio(nome_receita):
            messages.error(request, 'O nome da receita não pode ser vazio')
            return redirect('cria_receita')
        if campo_vazio(ingredientes):
            messages.error(request, 'O campo ingredientes não pode ser vazio')
            return redirect('cria_receita')
        if campo_vazio(modo_preparo):
            messages.error(request, 'O campo modo de preparo não pode ser vazio')
            return redirect('cria_receita')
        if campo_vazio(tempo_preparo):
            messages.error(request, 'O campo tempo de preparo não pode ser vazio')
            return redirect('cria_receita')
        if campo_vazio(rendimento):
            messages.error(request, 'O campo rendimento não pode ser vazio')
            return redirect('cria_receita')
        if campo_vazio(categoria):
            messages.error(request, 'O campo categoria não pode ser vazio')
            return redirect('cria_receita')       

        user = get_object_or_404(User, pk=request.user.id)
        receita = Receita(pessoa=user, nome_receita=nome_receita, ingredientes=ingredientes, modo_preparo=modo_preparo, tempo_preparo=tempo_preparo, redimento=rendimento, categoria=categoria, foto_receita=foto_receita)
        receita.save()
        return redirect('dashboard')
    else:       
        return render(request, 'receitas/cria_receita.html')    

def edita_receita(request, receita_id):
    """Edita uma receita"""
    receita = get_object_or_404(Receita, pk=receita_id)    
    receita_a_editar = { 'receita':receita}
    return render(request, 'receitas/edita_receita.html', receita_a_editar)

def atualiza_receita(request):
    """Atualiza as informações da receita no banco de dados"""
    if request.method == 'POST':
        receita_id = request.POST['receita_id']
        r = Receita.objects.get(pk=receita_id)
        r.nome_receita = request.POST['nome_receita']
        r.ingredientes = request.POST['ingredientes']
        r.modo_preparo = request.POST['modo_preparo']
        r.tempo_preparo = request.POST['tempo_preparo']
        r.redimento = request.POST['rendimento']
        r.categoria = request.POST['categoria']
        if 'foto_receita' in request.FILES:
            r.foto_receita = request.FILES['foto_receita']
        r.save()
        return redirect('dashboard')

def deleta_receita(request, receita_id):
    """Exclui uma receita"""
    receita = get_object_or_404(Receita, pk=receita_id)
    receita.delete()
    return redirect('dashboard')