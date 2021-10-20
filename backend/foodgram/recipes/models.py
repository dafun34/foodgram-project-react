from django.db import models
from users.models import User


class Tag(models.Model):
    name = models.CharField(max_length=200, blank=False)
    color = models.CharField(max_length=7, blank=True, null=True)
    slug = models.SlugField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name[:15]


class Ingredients(models.Model):
    name = models.CharField(max_length=200,
                            verbose_name='Название ингридиента',
                            )
    measurement_unit = models.CharField(max_length=200,
                                        verbose_name='Еденица измерения')

    def __str__(self):
        return self.name[:15]


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='recipe',
                               verbose_name='Автор рецепта')

    name = models.CharField(max_length=200,
                            blank=False,
                            verbose_name='Название'
                            )

    tags = models.ManyToManyField(Tag, related_name='recipe')

    image = models.ImageField(upload_to='recipes/',
                              blank=False
                              )

    text = models.TextField(blank=False,
                            verbose_name='Описание',
                            )

    ingredients = models.ManyToManyField('Components')

    cooking_time = models.PositiveSmallIntegerField(
                                       verbose_name='Время приготовления',
                                       blank=False,
                                       help_text=(
                                           'Время приготовления в минутах')
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-id']


class Components(models.Model):
    amount = models.PositiveSmallIntegerField()
    name = models.ForeignKey(Ingredients,
                             on_delete=models.CASCADE,
                             related_name='ingredient')
    component_in_recipe = models.ForeignKey(Recipe,
                                            on_delete=models.CASCADE,
                                            blank=True,
                                            null=True,
                                            related_name='component')

    def __str__(self):
        ingredient = self.name.name
        measurement_unit = self.name.measurement_unit
        amount = self.amount
        return f'{ingredient}: {amount} {measurement_unit}'


class Favorite(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='favorite')
    recipe = models.ManyToManyField(Recipe, related_name='favorite')


class ShoppingCard(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='card_user')
    recipe = models.ManyToManyField(Recipe, related_name='card_recipe')
