from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.views.decorators.http import require_http_methods, require_safe
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth import logout
from django.core.urlresolvers import reverse
from planet.models import Article, Category

from django.http import HttpResponse
import json
from django.utils import timezone

@ensure_csrf_cookie
@require_safe
def index(request):
    articles = Article.objects.order_by('-pub_time')
    # categories are used for right column render so we need to pass
    # it over to the template
    categories = Category.objects.all()
    context = {
        'articles': articles,
        'categories': categories,
    }
    return render(request, 'index.html', context)

@ensure_csrf_cookie
@require_safe
def detail(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    context = {
        'article': article,
    }
    return render(request, 'article.html', context)

@require_http_methods(["POST"])
def vote(request, article_id):
    data = {}
    if request.user.is_authenticated():
        article = get_object_or_404(Article, pk=article_id)
        v_ids = [str(v['id']) for v in article.voters.all()]
        # ensure we compare the actual strings or it won't work
        if len(v_ids) == 0 or str(request.user.id) not in v_ids:
            article.score += 10
            article.score_update_time = timezone.now()
            article.voters.add(str(request.user.id))
            article.save()
        data['res'] = 'OK'
        data['id'] = article_id
    else:
        data['res'] = 'ERR'
        data['error'] = 'unauthenticated'
    return HttpResponse(json.dumps(data), content_type='application/json')

@require_safe
def logout_view(request):
    logout(request)
    return redirect(reverse('index'))
