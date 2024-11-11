from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # This will hash the password
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

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "surname"]

    def __str__(self):
        return f"{self.name} {self.surname}"

class UserNutrientPreferences(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    min_calories = models.IntegerField(null=True, blank=True)
    max_calories = models.IntegerField(null=True, blank=True)
    min_sugars = models.IntegerField(null=True, blank=True)
    max_sugars = models.IntegerField(null=True, blank=True)
    min_protein = models.IntegerField(null=True, blank=True)
    max_protein = models.IntegerField(null=True, blank=True)
    min_iron = models.IntegerField(null=True, blank=True)
    max_iron = models.IntegerField(null=True, blank=True)
    min_potassium = models.IntegerField(null=True, blank=True)
    max_potassium = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"Nutrients for {self.user}"





class Recipe(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    total_calories = models.CharField(max_length=255) 
    sugars = models.CharField(max_length=255)
    protein = models.CharField(max_length=255)
    iron = models.CharField(max_length=255)
    potassium = models.CharField(max_length=255)
    preparation_time = models.IntegerField()
    preparation_guide = models.TextField()
    meal_type = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Ingredient(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class RecipeIngredients(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)


class DayPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()


class DayPlanRecipes(models.Model):
    day_plan = models.ForeignKey(DayPlan, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

class RatedRecipes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    rating = models.IntegerField()


class UserWeight(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    weight = models.CharField(max_length=10)
    date = models.DateField()


class DislikedIngredients(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)


class UserIngredients(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.IntegerField()
