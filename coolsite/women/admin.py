from django.contrib import admin, messages
from django.utils.safestring import mark_safe

from .models import *


class MarriedFilter(admin.SimpleListFilter):
    title = "Статус женщин"
    parameter_name = "status"

    def lookups(self, request, model_admin):
        return [
            ('married', 'Замужем'),
            ('single', 'Не замужем'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'married':
            return queryset.filter(husband__isnull=False)
        elif self.value() == 'single':
            return queryset.filter(husband__isnull=True)



@admin.register(Women)
class WomenAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'cat', 'time_create', 'get_html_photo', 'is_published', 'brief_info')
    list_display_links = ('title',)
    search_fields = ('title', 'content', 'cat__name')
    list_editable = ('is_published',)
    list_filter = ('is_published', 'time_create', 'cat__name', MarriedFilter)
    prepopulated_fields = {'slug': ('title',)}
    fields = ('title', 'slug', 'cat', 'content', 'photo',
              'is_published', 'husband', 'tags', 'time_create', 'time_update', 'get_html_photo')
    # filter_vertical = ('tags')
    filter_horizontal = ('tags', )
    readonly_fields = ('time_create', 'time_update', 'get_html_photo')
    save_on_top = True
    list_per_page = 5
    actions = ['set_published', 'set_draft']

    @admin.display(description='Краткое описание', ordering='content')
    def brief_info(self, women: Women):
        return f"Описание {len(women.content)} символов"

    @admin.action(description='Опубликавать выбранные записи')
    def set_published(self, request, queryset):
        count = queryset.update(is_published=Women.Status.PUBLISHED)
        self.message_user(request, f'Изменено {count} записей.')

    @admin.action(description='Перевести в черновик выбранные записи')
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=Women.Status.DRAFT)
        self.message_user(request, f'Изменено {count} записей.', messages.WARNING)

    def get_html_photo(self, object):
        if object.photo:
            return mark_safe(f'<img src="{object.photo.url}" width=100>')

    get_html_photo.short_description = 'Миниатюра'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


admin.site.site_title = 'Админ-панель сайта о женщинах'
admin.site.site_header = 'Админ-панель сайта о женщинах'
