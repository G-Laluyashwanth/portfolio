from django.contrib import admin
from .models import SkillCategory, Skill


class SkillInline(admin.TabularInline):
    model = Skill
    extra = 2
    fields = ('name', 'proficiency', 'years_experience', 'is_featured', 'order')


@admin.register(SkillCategory)
class SkillCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'order', 'description')
    list_editable = ('order',)
    inlines = [SkillInline]


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'proficiency', 'years_experience', 'is_featured', 'order')
    list_editable = ('proficiency', 'is_featured', 'order')
    list_filter = ('category', 'proficiency', 'is_featured')
    search_fields = ('name',)
