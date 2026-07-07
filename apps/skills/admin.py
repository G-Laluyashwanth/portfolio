from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline
from unfold.decorators import display

from .models import SkillCategory, Skill


class SkillInline(TabularInline):
    model = Skill
    extra = 2
    fields = ('name', 'proficiency', 'years_experience', 'is_featured', 'order')
    ordering = ('order', 'name')


@admin.register(SkillCategory)
class SkillCategoryAdmin(ModelAdmin):
    list_display = ('name', 'skill_count', 'order', 'description')
    list_editable = ('order',)
    inlines = [SkillInline]
    search_fields = ('name', 'description')
    ordering = ('order', 'name')

    @display(description='Skills')
    def skill_count(self, obj):
        return obj.skills.count()


@admin.register(Skill)
class SkillAdmin(ModelAdmin):
    list_display = ('name', 'category', 'proficiency_badge', 'years_experience', 'featured_badge', 'order')
    list_editable = ('order',)
    list_filter = ('category', 'proficiency', 'is_featured')
    search_fields = ('name',)
    list_filter_submit = True
    ordering = ('category__order', 'order', 'name')

    @display(
        description='Level',
        label={
            'beginner': 'info',
            'intermediate': 'primary',
            'advanced': 'success',
            'expert': 'warning',
        },
    )
    def proficiency_badge(self, obj):
        return obj.proficiency

    @display(description='Featured', label={True: 'success', False: 'default'})
    def featured_badge(self, obj):
        return obj.is_featured
