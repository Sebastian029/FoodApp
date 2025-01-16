from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from datetime import timedelta

# recipes
class Ingredient(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Recipe(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    total_calories = models.CharField(max_length=255) 
    carbohydrates = models.CharField(max_length=255) 
    fat = models.CharField(max_length=255) 
    fiber = models.CharField(max_length=255) 
    sugars = models.CharField(max_length=255)
    protein = models.CharField(max_length=255)
    iron = models.CharField(max_length=255)
    potassium = models.CharField(max_length=255)
    preparation_time = models.IntegerField()
    preparation_guide = models.TextField()
    meal_type = models.CharField(max_length=255)
    ingredients = models.ManyToManyField(Ingredient, through='RecipeIngredients')

    
    def __str__(self):
        return self.title

class RecipeIngredients(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.FloatField(default=0.0)
    unit = models.CharField(default="", max_length=50)

    class Meta:
        unique_together = ('recipe', 'ingredient')

    def __str__(self):
        return f"{self.quantity} {self.unit} of {self.ingredient.name} in {self.recipe.title}"


# user
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    disliked_ingredients = models.ManyToManyField(
        Ingredient, through='DislikedIngredients', related_name='disliked_by'
    )
    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "surname"]

    def __str__(self):
        return f"{self.name} {self.surname}"


# cart
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  
    ingredients = models.ManyToManyField(Ingredient, through='CartIngredient')

    def __str__(self):
        return f"Cart of {self.user}"

class CartIngredient(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.FloatField()
    unit = models.CharField(max_length=50)
    bought = models.BooleanField(default=False)  

    def __str__(self):
        return f"{self.quantity} {self.unit} of {self.ingredient.name}"
    


# user_preferences 
class UserNutrientPreferences(models.Model):
    DIET_CHOICES = [
        ('low_calories', 'Low Calories'),
        ('high_calories', 'High Calories'),
        ('high_protein', 'High Protein'),
        ('low_fat', 'Low Fat'),
        ('high_fat', 'High Fat'),
        ('low_carbohydrates', 'Low Carbohydrates'),
        ('high_carbohydrates', 'High Carbohydrates'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    diet_type = models.CharField(max_length=20, choices=DIET_CHOICES, default='high_protein')
    min_calories = models.IntegerField(default=1500)
    max_calories = models.IntegerField(default=2500)
    min_sugars = models.IntegerField(default=0)
    max_sugars = models.IntegerField(default=0)
    min_protein = models.IntegerField(default=0)
    max_protein = models.IntegerField(default=0)
    min_fat = models.IntegerField(default=0)
    max_fat = models.IntegerField(default=0)
    min_carbohydrates = models.IntegerField(default=0)
    max_carbohydrates = models.IntegerField(default=0)
    min_fiber = models.IntegerField(default=0)
    max_fiber = models.IntegerField(default=0)
    min_iron = models.IntegerField(default=0)
    max_iron = models.IntegerField(default=0)
    min_potassium = models.IntegerField(default=0)
    max_potassium = models.IntegerField(default=0)

    def __str__(self):
        return f"Nutrients for {self.user} ({self.get_diet_type_display()})"

class DislikedIngredients(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)

# planner_screen
class DayPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'date') 

class DayPlanRecipes(models.Model):
    day_plan = models.ForeignKey(DayPlan, on_delete=models.CASCADE, related_name='recipes')
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('day_plan', 'recipe') 

class UserRecipeUsage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE)
    last_used = models.DateField(auto_now=True) 
    
    class Meta:
        unique_together = ('user', 'recipe') 

# user_screen
class UserWeight(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    weight = models.CharField(max_length=10)
    date = models.DateField()

# macros calculation      
class WeeklySummary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    week_start = models.DateField()  
    week_end = models.DateField()  
    total_calories = models.FloatField(default=0.0)
    total_carbohydrates = models.FloatField(default=0.0)
    total_fat = models.FloatField(default=0.0)
    total_protein = models.FloatField(default=0.0)
    total_fiber = models.FloatField(default=0.0)
    total_sugars = models.FloatField(default=0.0)
    total_iron = models.FloatField(default=0.0)
    total_potassium = models.FloatField(default=0.0)

    class Meta:
        unique_together = ('user', 'week_start')

    def save(self, *args, **kwargs):
        self.week_end = self.week_start + timedelta(days=6)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Weekly Summary ({self.week_start} - {self.week_end}) for {self.user}"
    
class DayPlanItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=255)
    total_calories = models.FloatField()
    total_protein = models.FloatField(default=0)
    total_fats = models.FloatField(default=0)
    total_carbs = models.FloatField(default=0)
    total_fiber = models.FloatField(default=0)
    total_sugars = models.FloatField(default=0)
    total_iron = models.FloatField(default=0)
    total_potassium = models.FloatField(default=0)
    quantity = models.PositiveIntegerField(default=1)
    date = models.DateField(default=timezone.now)  

    def __str__(self):
        return f"{self.item_name} - {self.total_calories} kcal"
    
    
