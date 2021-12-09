from django.contrib import admin


from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author' , 'status', 'publish')
    search_fields = ('title' , 'body')
    prepopulated_fields = {'slug': ('title',)}
