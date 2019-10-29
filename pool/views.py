from django.shortcuts import render
from .models import Article, Category, Tag, Tui, Link, Banner
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.


def global_var(request):
    category = Category.objects.all()                  #传入base.html页面中的category所有对象
    retui = Article.objects.filter(tui__id=2)[0:4]   #取出热文推荐及tui表中id=2的文章
    tag = Tag.objects.all()  # 取出所有的tag标签
    return locals()

# 首页
def index(request):
    banner = Banner.objects.filter(is_active=True)[0:4]     #在index.html中轮播图位置取banner表中的四张图片
    tui = Article.objects.filter(tui__id=1)[0:3]            #在index.html中推荐阅读中取关联了tui表中id为1的文章的三篇
    new = Article.objects.order_by('-id')[0:8]              #通过order_by反序把最新的八篇文章取出来
    views = Article.objects.all().order_by('-views')[0:5]   #根据阅读量排序取出前五名的文章
    link = Link.objects.all()                               #取Link表中的链接
    return render(request, 'index.html', locals())


# 列表页

def list(request, lid):
    article = Article.objects.filter(category__id=lid).order_by('-id')      #根据传入的分类lid取出对面分类的文章
    name = Category.objects.get(pk=lid)                                     #根据传入的lid获取对应的分类名称
    link = Link.objects.all()
    page = request.GET.get('page')
    paginator = Paginator(article,2)
    try:
        article = paginator.page(page)
    except PageNotAnInteger:
        article = paginator.page(1)
    except EmptyPage:
        article = paginator.page(paginator.num_pages)

    return render(request, 'list.html', locals())


# 内容页
def show(request, sid):
    body = Article.objects.get(id=sid)                      #根据url传入的sid获取对应id的文章
    name = Category.objects.get(name=body.category)
    tags = Tag.objects.filter(article__id=sid)
    link = Link.objects.all()
    next_blog = Article.objects.filter(created_time__gt=body.created_time,category__id=body.category.id).first()
    previous_blog = Article.objects.filter(created_time__lt=body.created_time,category__id=body.category.id).last()
    hobby = Article.objects.filter(category=body.category).exclude(id=sid)[0:4]         #根据文章的分类取出所有的文章
    body.views = body.views + 1
    body.save()

    return render(request, 'show.html', locals())


# 标签页
def tag(request, t):
    article = Article.objects.filter(tags__name=t)
    link = Link.objects.all()
    tagname = Tag.objects.get(name=t)
    page = request.GET.get('page')
    paginator = Paginator(article, 2)
    try:
        article = paginator.page(page)
    except PageNotAnInteger:
        article = paginator.page(1)
    except EmptyPage:
        article = paginator.page(paginator.num_pages)

    return render(request, 'tag.html',locals())


# 搜索页
def search(request):
    word = request.GET.get('search')
    article = Article.objects.filter(title__icontains=word)
    link = Link.objects.all()
    page = request.GET.get('page')
    paginator = Paginator(article, 2)
    try:
        article = paginator.page(page)
    except PageNotAnInteger:
        article = paginator.page(1)
    except EmptyPage:
        article = paginator.page(paginator.num_pages)

    return render(request,'search.html',locals())


# 关于我们
def about(request):
    category = Category.objects.all()
    context = {
        'category':category
    }
    return render(request,'page.html',context)
