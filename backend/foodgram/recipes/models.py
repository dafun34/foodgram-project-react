from django.db import models
from users.models import User

class Tag(models.Model):
    name = models.CharField(max_length=200, blank=False)
    color = models.CharField(max_length=7, blank=True)
    slug = models.SlugField(max_length=200, unique=True)

    def __str__(self):
        return self.name[:15]



class Ingredients(models.Model):
    name = models.CharField(max_length=200,
                            verbose_name='Название ингридиента'
                            )
    measurement_unit = models.CharField(max_length=200,
                                        verbose_name='Еденица измерения')


    def __str__(self):
        return self.name[:15]


class Components(models.Model):
    ingredients = models.ForeignKey(Ingredients, on_delete=models.CASCADE)
    amount = models.SmallIntegerField()

    def __str__(self):
        return (f'{self.ingredients.name},'
                f' {self.amount} '
                f'{self.ingredients.measurement_unit}')


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='recipe',
                               verbose_name='Автор рецепта')

    name = models.CharField(max_length=200,
                            blank=False,
                            verbose_name='Название',
                            )

    image = models.ImageField(upload_to='recipes/',
                              blank=False
                              )

    text = models.TextField(blank=False,
                            verbose_name='Описание',
                            )

    ingredients = models.ManyToManyField(Components)

    tag = models.ManyToManyField(Tag, blank=False)



    cooking_time = models.PositiveSmallIntegerField(
                                       verbose_name='Время приготовления',
                                       blank=False,
                                       help_text='Время приготовления в минутах'
    )
    def __str__(self):
        return self.name


class Favorite(models.Model):
    user = models.ForeignKey(User,
                             related_name='favorite',
                             on_delete=models.CASCADE)

    recipe = models.ForeignKey(Recipe,
                               related_name='favorite',
                               on_delete=models.CASCADE)

    class Meta:
        constraints =[
        models.UniqueConstraint(fields=['user', 'recipe'],
                                name='user_recipe')
        ]


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='follower')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='following')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'author'],
                                    name='user_follow')
        ]


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='cart')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='cart')

    def __str__(self):
        return self.recipe.name

