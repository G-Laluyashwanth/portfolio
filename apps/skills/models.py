from django.db import models


class SkillCategory(models.Model):
    """A grouping like Backend, Frontend, ML/Data, Tools."""
    name = models.CharField(max_length=120, unique=True)
    icon = models.CharField(
        max_length=40,
        blank=True,
        help_text='Optional icon name (used in template if you wire one in).'
    )
    description = models.CharField(max_length=240, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'Skill Category'
        verbose_name_plural = 'Skill Categories'

    def __str__(self):
        return self.name


class Skill(models.Model):
    """An individual skill within a category."""

    PROFICIENCY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('expert', 'Expert'),
    ]

    category = models.ForeignKey(SkillCategory, on_delete=models.CASCADE, related_name='skills')
    name = models.CharField(max_length=80)
    proficiency = models.CharField(max_length=20, choices=PROFICIENCY_CHOICES, default='advanced')
    years_experience = models.DecimalField(
        max_digits=4, decimal_places=1, default=1.0,
        help_text='e.g. 3.5'
    )
    is_featured = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['category__order', 'order', 'name']
        constraints = [
            models.UniqueConstraint(
                fields=['category', 'name'],
                name='unique_skill_per_category',
            ),
        ]

    def __str__(self):
        return f'{self.name} ({self.get_proficiency_display()})'
