from django.shortcuts import render
from django.http import HttpResponse
from .models import Article, Tag, Link
from .models import Category, Banner
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.


def hello(request):
    return HttpResponse('欢迎使用Django!')


def index(request):
    banner = Banner.objects.filter(is_active=True)[0:4]
    tui = Article.objects.filter(tui_id=1)[:3]
    allarticle = Article.objects.all().order_by('-id')[0:10]
    hot = Article.objects.all().order_by('views')[:10]
    link = Link.objects.all()
    return render(request, 'index.html', locals())   # 把上下文传到index.html页面


def list(request, lid):
    list = Article.objects.filter(category_id=lid)  # 获取通过URL传进来的lid，然后筛选出对应文章
    cname = Category.objects.get(id=lid)  # 获取当前按文章的栏目名
    page = request.GET.get('page')   # 在URL中获取当前页面数
    paginator = Paginator(list, 5)  # 对查询到的数据对象list进行分页，设置超过5条数据就分页
    try:
        list = paginator.page(page)  # 获取当前页码的记录
    except PageNotAnInteger:
        list = paginator.page(1)  # 如果用户输入的页码不是整数时，显示第一页的内容
    except EmptyPage:
        list = paginator.page(paginator.num_pages)  # 如果用户输入的页数不在系统的页码列表中时，显示最后一页的内容
    return render(request, 'list.html', locals())


def show(request, sid):
    show = Article.objects.get(id=sid)  # 查询指定ID的文章
    # hot = Article.objects.all().order_by('?')[:10]   # 内容下面的可能感兴趣的文章，随机推荐
    category_id = show.category_id  # 获取当前文章的分类id
    hot = Article.objects.filter(category_id=category_id,).exclude(id=sid)[:10]  # 根据分类id推荐感兴趣的文章，推荐列表排除当前文章
    previous_blog = Article.objects.filter(created_time__lt=show.created_time, category=show.category.id).last()
    next_blog = Article.objects.filter(created_time__gt=show.created_time, category=show.category.id).first()
    show.views = show.views + 1
    show.save()
    return render(request, 'show.html', locals())


def tag(request, tag):
    list = Article.objects.filter(tags__name=tag)  # 通过文章标签进行查询文章
    tname = Tag.objects.get(name=tag)   # 获取当前搜索的标签名
    page = request.GET.get('page')
    paginator = Paginator(list, 5)
    try:
        list = paginator.page(page)  # 获取当前页码的记录
    except PageNotAnInteger:
        list = paginator.page(1)  # 如果用户输入的页码不是整数时，显示第一页的内容
    except EmptyPage:
        list = paginator.page(paginator.num_pages)  # 如果用户输入的页数不在系统的页码列表时，显示最后一页的内容
    return render(request, 'tags.html', locals())


def search(request):
    ss = request.GET.get('search')   # 获取搜索的关键词
    list = Article.objects.filter(title__icontains=ss)  # 获取到搜索关键词通过标题进行匹配
    page = request.GET.get('page')
    paginator = Paginator(list, 10)
    try:
        list = paginator.page(page)   # 获取当前页码的揭露
    except PageNotAnInteger:
        list = paginator.page(1)  # 如果用户输入的页码不是整数时，显示第一页的内容
    except EmptyPage:
        list = paginator.page(paginator.num_pages)   # 如果用户输入的页数不在系统的页码列表时，显示最后一页的内容
    return render(request, 'search.html', locals())


def about(request):
    return render(request, 'page.html')


def global_variable(request):
    allcategory = Category.objects.all()  # 通过Category表查出所有分类
    remen = Article.objects.filter(tui__id=2)[:6]    # 右侧热门推荐
    tags = Tag.objects.all()  # 右侧所有标签
    return locals()
