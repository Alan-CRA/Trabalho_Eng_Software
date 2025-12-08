from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.db import transaction
from django.db.models import Avg, Count
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.conf import settings
from .models import Filme, Genero, Ator, Streaming, Avaliacao, Favorito
from .forms import AvaliacaoForm
from .tmdb import search_movie, movie_details, movie_credits, watch_providers, discover_movies

def _ensure_genres(genres):
    objs = []
    for g in genres or []:
        obj, _ = Genero.objects.get_or_create(nome=g.get("name","").strip()[:120])
        objs.append(obj)
    return objs

def _ensure_cast(cast):
    objs = []
    for a in (cast or [])[:20]:
        name = a.get("name","").strip()
        if not name: continue
        obj, _ = Ator.objects.get_or_create(nome=name[:200])
        objs.append(obj)
    return objs

def _providers_to_streaming(providers):
    objs = []
    names = set()
    for region, data in (providers or {}).get("results", {}).items():
        flatrate = data.get("flatrate") or []
        for s in flatrate:
            nm = s.get("provider_name")
            if not nm or nm in names: continue
            names.add(nm)
            obj, _ = Streaming.objects.get_or_create(nome=nm[:200])
            objs.append(obj)
    return objs

@transaction.atomic
def _upsert_movie_from_tmdb(tmdb_id:int):
    det = movie_details(tmdb_id)
    credits = movie_credits(tmdb_id)
    providers = watch_providers(tmdb_id)

    filme, _ = Filme.objects.update_or_create(
        tmdb_id=det["id"],
        defaults={
            "nome": det.get("title") or det.get("name") or "",
            "lancamento": det.get("release_date") or "",
            "tempo": det.get("runtime") or None,
            "sinopse": det.get("overview") or "",
            "nota_media": det.get("vote_average") or None,
            "poster_path": det.get("poster_path") or None,
            "backdrop_path": det.get("backdrop_path") or None,
        }
    )

    filme.genero.set(_ensure_genres(det.get("genres", [])))
    filme.atores.set(_ensure_cast((credits or {}).get("cast", [])))
    filme.streaming.set(_providers_to_streaming(providers))
    return filme

class ListaFilmes(View):
    template_name = "filmes/lista_filmes.html"

    def get(self, request):
        q = request.GET.get("q","").strip()
        filmes = []
        if q:
            data = search_movie(q)
            results = data.get("results", [])
            for r in results:
                tmdb_id = r["id"]
                f, _ = Filme.objects.update_or_create(
                    tmdb_id=tmdb_id,
                    defaults={
                        "nome": r.get("title") or "",
                        "lancamento": r.get("release_date") or "",
                        "nota_media": r.get("vote_average") or None,
                        "poster_path": r.get("poster_path") or None,
                    }
                )
                filmes.append(f)
        ctx = {"filmes": filmes, "IMG": settings.TMDB_IMAGE_BASE_URL}
        return render(request, self.template_name, ctx)

class Detalhes(View):
    template_name = "filmes/detalhes.html"

    def get(self, request):
        tmdb_id = request.GET.get("id")
        if not tmdb_id:
            messages.error(request, "ID do filme não informado.")
            return redirect("pages:home")
        try:
            tmdb_id = int(tmdb_id)
        except ValueError:
            messages.error(request, "ID inválido.")
            return redirect("pages:home")

        filme = Filme.objects.filter(tmdb_id=tmdb_id).first()
        if not filme or not (filme.sinopse and filme.tempo):
            filme = _upsert_movie_from_tmdb(tmdb_id)

        # Avaliação do usuário atual
        avaliacao_usuario = None
        is_favorito = False
        if request.user.is_authenticated:
            avaliacao_usuario = Avaliacao.objects.filter(
                user=request.user, filme=filme
            ).first()
            is_favorito = Favorito.objects.filter(
                user=request.user, filme=filme
            ).exists()

        # Todas as avaliações do filme
        avaliacoes = Avaliacao.objects.filter(filme=filme).select_related('user').order_by('-criado_em')
        
        # Média das avaliações dos usuários
        media_avaliacoes = avaliacoes.aggregate(media=Avg('nota'))['media']
        total_avaliacoes = avaliacoes.count()

        # Formulário de avaliação
        form = AvaliacaoForm(instance=avaliacao_usuario) if avaliacao_usuario else AvaliacaoForm()

        ctx = {
            "filme": filme,
            "IMG": settings.TMDB_IMAGE_BASE_URL,
            "form": form,
            "avaliacao_usuario": avaliacao_usuario,
            "avaliacoes": avaliacoes[:10],  # Limita a 10 avaliações
            "media_avaliacoes": media_avaliacoes,
            "total_avaliacoes": total_avaliacoes,
            "is_favorito": is_favorito,
            "estrelas_range": range(1, 11),  # Range 1-10 para as estrelas
        }
        return render(request, self.template_name, ctx)


@login_required(login_url="contas:entrar")
def avaliar_filme(request, filme_id):
    """View para avaliar ou atualizar avaliação de um filme."""
    filme = get_object_or_404(Filme, id=filme_id)
    
    if request.method == "POST":
        # Verifica se já existe avaliação
        avaliacao_existente = Avaliacao.objects.filter(
            user=request.user, filme=filme
        ).first()
        
        form = AvaliacaoForm(request.POST, instance=avaliacao_existente)
        
        if form.is_valid():
            avaliacao = form.save(commit=False)
            avaliacao.user = request.user
            avaliacao.filme = filme
            avaliacao.save()
            
            if avaliacao_existente:
                messages.success(request, f"Sua avaliação de '{filme.nome}' foi atualizada!")
            else:
                messages.success(request, f"Você avaliou '{filme.nome}' com nota {avaliacao.nota}!")
            
            return redirect(f"/filmes/detalhes?id={filme.tmdb_id}")
        else:
            messages.error(request, "Erro ao salvar avaliação. Verifique os dados.")
    
    return redirect(f"/filmes/detalhes?id={filme.tmdb_id}")


@login_required(login_url="contas:entrar")
def excluir_avaliacao(request, filme_id):
    """View para excluir avaliação de um filme."""
    filme = get_object_or_404(Filme, id=filme_id)
    
    avaliacao = Avaliacao.objects.filter(user=request.user, filme=filme).first()
    if avaliacao:
        avaliacao.delete()
        messages.success(request, f"Sua avaliação de '{filme.nome}' foi removida.")
    
    return redirect(f"/filmes/detalhes?id={filme.tmdb_id}")


@login_required(login_url="contas:entrar")
def favoritar_filme(request, filme_id):
    """View para adicionar ou remover filme dos favoritos."""
    filme = get_object_or_404(Filme, id=filme_id)
    
    favorito_existente = Favorito.objects.filter(user=request.user, filme=filme).first()
    
    if favorito_existente:
        # Remove dos favoritos
        favorito_existente.delete()
        messages.success(request, f"'{filme.nome}' foi removido dos seus favoritos.")
    else:
        # Adiciona aos favoritos
        Favorito.objects.create(user=request.user, filme=filme)
        messages.success(request, f"'{filme.nome}' foi adicionado aos seus favoritos!")
    
    return redirect(f"/filmes/detalhes?id={filme.tmdb_id}")


@login_required(login_url="contas:entrar")
def recomendacoes(request):
    """
    View para exibir recomendações personalizadas baseadas nas avaliações do usuário.
    Algoritmo:
    1. Pega filmes que o usuário avaliou bem (nota >= 7)
    2. Identifica os gêneros mais frequentes desses filmes
    3. Busca filmes populares desses gêneros na API TMDB
    4. Filtra filmes que o usuário já avaliou ou favoritou
    """
    # Buscar avaliações positivas do usuário (nota >= 7)
    avaliacoes_positivas = Avaliacao.objects.filter(
        user=request.user,
        nota__gte=7
    ).select_related('filme').prefetch_related('filme__genero')
    
    # Coletar IDs de filmes já vistos/avaliados
    filmes_vistos_ids = set(
        Avaliacao.objects.filter(user=request.user).values_list('filme__tmdb_id', flat=True)
    )
    filmes_favoritos_ids = set(
        Favorito.objects.filter(user=request.user).values_list('filme__tmdb_id', flat=True)
    )
    filmes_excluir = filmes_vistos_ids | filmes_favoritos_ids
    
    # Contar frequência de gêneros nas avaliações positivas
    generos_contagem = {}
    for av in avaliacoes_positivas:
        for genero in av.filme.genero.all():
            generos_contagem[genero.nome] = generos_contagem.get(genero.nome, 0) + 1
    
    # Mapear nomes de gêneros para IDs do TMDB
    GENERO_TMDB_IDS = {
        "Ação": 28, "Aventura": 12, "Animação": 16, "Comédia": 35,
        "Crime": 80, "Documentário": 99, "Drama": 18, "Família": 10751,
        "Fantasia": 14, "História": 36, "Terror": 27, "Música": 10402,
        "Mistério": 9648, "Romance": 10749, "Ficção Científica": 878,
        "Cinema TV": 10770, "Thriller": 53, "Guerra": 10752, "Faroeste": 37,
    }
    
    # Pegar os 3 gêneros mais frequentes
    generos_ordenados = sorted(generos_contagem.items(), key=lambda x: x[1], reverse=True)[:3]
    generos_preferidos = [g[0] for g in generos_ordenados]
    generos_ids = [GENERO_TMDB_IDS.get(g) for g in generos_preferidos if g in GENERO_TMDB_IDS]
    
    recomendados = []
    mensagem_status = ""
    
    if generos_ids:
        # Buscar filmes recomendados via API TMDB
        try:
            payload = discover_movies(genre_ids=generos_ids, min_vote=6.5, page=1)
            results = payload.get("results", [])
            
            # Filtrar filmes já vistos e mapear para formato padrão
            for movie in results:
                if movie.get("id") not in filmes_excluir:
                    recomendados.append({
                        "id": movie.get("id"),
                        "title": movie.get("title", ""),
                        "poster_path": movie.get("poster_path"),
                        "vote_average": movie.get("vote_average"),
                        "release_date": movie.get("release_date", ""),
                        "overview": movie.get("overview", "")[:150] + "..." if movie.get("overview") else "",
                    })
                if len(recomendados) >= 12:
                    break
                    
            mensagem_status = f"Baseado nos seus gêneros favoritos: {', '.join(generos_preferidos)}"
        except Exception as e:
            mensagem_status = "Não foi possível carregar recomendações no momento."
    else:
        mensagem_status = "Avalie mais filmes com nota 7 ou superior para receber recomendações personalizadas!"
    
    context = {
        "recomendados": recomendados,
        "generos_preferidos": generos_preferidos,
        "mensagem_status": mensagem_status,
        "total_avaliacoes": Avaliacao.objects.filter(user=request.user).count(),
        "IMG": settings.TMDB_IMAGE_BASE_URL,
    }
    return render(request, "filmes/recomendacoes.html", context)
