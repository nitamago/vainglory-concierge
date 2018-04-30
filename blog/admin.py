from django.contrib import admin
from django.urls import path
from django.shortcuts import render, redirect
from django.http import HttpResponse

# Register your models here.
from .models import Article

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title',
                    'abstract',
                    'content',
                    'tags',
                    'is_public')
    actions =['edit_article']

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            #path(r'^editor/$', self.admin_site.admin_view(self.hoge), name='hoge')
            path('editor/', self.admin_site.admin_view(self.editor)),
            path('register/', self.admin_site.admin_view(self.register)),
            #path('editor/', include('blog_editor.urls')),
            #url('editor/', include('blog_editor.urls')),
        ]
        return my_urls + urls

    def editor(self, request):
        return render(request, 'blog/editor.html')

    def register(self, request):
        title = request.POST['title']
        abstract = request.POST['abstract']
        content = request.POST['content']
        article_id = request.POST['id']
        obj, created = Article.objects.get_or_create(id=article_id)

        obj.title = title
        obj.abstract = abstract
        obj.content = content

        obj.save()
        return redirect('/admin/blog/article/')

    def edit_article(self, request, queryset):
        first = queryset[0]
        return render(request, 'blog/editor.html', {"data": first})


admin.site.register(Article, ArticleAdmin)
