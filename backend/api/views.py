from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.utils.timezone import now
from django.db.models import Case, When, Value, IntegerField, Sum, F
from decimal import Decimal
from django.db.models.functions import Cast
from django.db.models.fields import IntegerField
from datetime import timedelta, datetime

from .models import (Recipe, Ingredient,
                     DayPlan, DayPlanRecipes,
                     UserWeight,DislikedIngredients,
                     UserNutrientPreferences,Cart,
                     Ingredient, CartIngredient,
                     DayPlanItem
)

from .serializers import (
    RecipeSerializer, UserWeightSerializer,
    DislikedIngredientsSerializer, UserNutrientPreferencesSerializer,
    DietTypeSerializer,RegisterSerializer,
    AllIngredientSerializer
)
from .utils import  upload_recipes_from_csv, plan_meals_for_week

# user auth
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = [AllowAny]
    
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data.get("refresh")
            
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
                
                return Response({"detail": "Successfully logged out."}, status=status.HTTP_205_RESET_CONTENT)
            else:
                return Response({"detail": "Refresh token missing."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"detail": "Invalid token or token already blacklisted."},
                status=status.HTTP_400_BAD_REQUEST,
            )

class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        return Response({"message": "You have access to this view."})
    
    
    
# user preferences  
class UserNutrientPreferencesView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            preferences = UserNutrientPreferences.objects.get(user=request.user)
            serializer = UserNutrientPreferencesSerializer(preferences, data=request.data, partial=True)
        except UserNutrientPreferences.DoesNotExist:
            serializer = UserNutrientPreferencesSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    
    
    def get(self, request):
        try:
            preferences = UserNutrientPreferences.objects.get(user=request.user)
            serializer = UserNutrientPreferencesSerializer(preferences)
            return Response(serializer.data)
        except UserNutrientPreferences.DoesNotExist:
            return Response({"detail": "Preferences not set."}, status=status.HTTP_404_NOT_FOUND)


class IngredientListCreateView(generics.ListCreateAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = AllIngredientSerializer
  
class UserDislikedIngredientsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        disliked_ingredients = DislikedIngredients.objects.filter(user=user)
        ingredients = [item.ingredient for item in disliked_ingredients]
        serializer = AllIngredientSerializer(ingredients, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = DislikedIngredientsSerializer(data=request.data)
        if serializer.is_valid():
            ingredient_ids = serializer.validated_data['ingredient_ids']
            user = request.user

            DislikedIngredients.objects.filter(user=user).delete()

            disliked_ingredients = [
                DislikedIngredients(user=user, ingredient=Ingredient.objects.get(id=ingredient_id))
                for ingredient_id in ingredient_ids
            ]
            DislikedIngredients.objects.bulk_create(disliked_ingredients)

            return Response({"message": "Disliked ingredients saved successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# recipes
class RecipeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

class RecipeListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        recipes = Recipe.objects.all()
        serializer = RecipeSerializer(recipes, many=True)
        return Response(serializer.data)
    
class RecipeTypeView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        meal_type = request.query_params.get('meal_type', None)
        
        if meal_type:
            recipes = Recipe.objects.filter(meal_type=meal_type)
        else:
            recipes = Recipe.objects.all()
        
        serializer = RecipeSerializer(recipes, many=True)
        return Response(serializer.data)
    

# user_screen 
class UpdateWeightView(APIView):
    permission_classes = [IsAuthenticated]  
    def post(self, request):
        user = request.user
        weight = request.data.get('weight')
        date = request.data.get('date', now().date())

        if not user.is_authenticated:
            return Response({"error": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)

        today = now().date()
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)

        weekly_entry_exists = UserWeight.objects.filter(
            user=user,
            date__range=[start_of_week, end_of_week]
        ).exists()

        if weekly_entry_exists:
            return Response({"error": "You can only update weight once per week."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserWeightSerializer(data={'user': user.id, 'weight': weight, 'date': date})
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserWeightListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        user_weights = UserWeight.objects.filter(user=user).order_by('-date')  # Optionally order by date
        serializer = UserWeightSerializer(user_weights, many=True)
        return Response(serializer.data)
    
class CanUpdateWeightView(APIView):
    permission_classes = [IsAuthenticated]  
    def get(self, request):
        user = request.user

        if not user.is_authenticated:
            return Response({"error": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)

        today = now().date()
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)

        weekly_entry_exists = UserWeight.objects.filter(
            user=user,
            date__range=[start_of_week, end_of_week]
        ).exists()

        can_update = not weekly_entry_exists
        return Response({"can_update": can_update}, status=status.HTTP_200_OK)
    
    
class DietTypeView(generics.RetrieveUpdateAPIView):
    serializer_class = DietTypeSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return UserNutrientPreferences.objects.get_or_create(user=self.request.user)[0]
    
class DietChoicesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        diet_choices = dict(UserNutrientPreferences.DIET_CHOICES)
        return Response(diet_choices)
    
    
# cart
class CartAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    @staticmethod
    def is_positive_number(value):
        
        return isinstance(value, (int, float)) and value > 0
    
    def get_cart(self, user):
       
        cart, created = Cart.objects.get_or_create(user=user)
        return cart

    def post(self, request):
       
        user = request.user
        cart = self.get_cart(user)  

        ingredients_data = request.data.get('ingredients')
        recipe_id = request.data.get('recipe_id')

        if ingredients_data:
            for item in ingredients_data:
                quantity = item.get("quantity")
                if not self.is_positive_number(quantity):
                    return Response({"message": "Quantity must be a positive number."}, status=status.HTTP_400_BAD_REQUEST)
                ingredient, created = Ingredient.objects.get_or_create(
                    name=item['ingredient_name']
                )

                existing_cart_ingredient = CartIngredient.objects.filter(cart=cart, ingredient=ingredient).first()

                if existing_cart_ingredient:
                    if existing_cart_ingredient.unit != item['unit']:
                        CartIngredient.objects.create(
                            cart=cart,
                            ingredient=ingredient,
                            quantity=item['quantity'],
                            unit=item['unit']
                        )
                    else:
                        existing_cart_ingredient.quantity += item['quantity']
                        existing_cart_ingredient.save()
                else:
                    CartIngredient.objects.create(
                        cart=cart,
                        ingredient=ingredient,
                        quantity=item['quantity'],
                        unit=item['unit']
                    )

            return Response({"message": "Ingredients added to cart."}, status=status.HTTP_201_CREATED)

        elif recipe_id:
            try:
                recipe = Recipe.objects.get(id=recipe_id)
                serializer = RecipeSerializer(recipe)
                ingredients = serializer.data.get('ingredients')

                if not ingredients:
                    return Response({"message": "No ingredients found in this recipe."}, status=status.HTTP_404_NOT_FOUND)

                for item in ingredients:
                    quantity = item.get("quantity")
                    if not self.is_positive_number(quantity):
                        return Response({"message": "Quantity must be a positive number."}, status=status.HTTP_400_BAD_REQUEST)
                    ingredient, created = Ingredient.objects.get_or_create(
                        name=item['ingredient_name']
                    )

                    existing_cart_ingredient = CartIngredient.objects.filter(cart=cart, ingredient=ingredient).first()

                    if existing_cart_ingredient:
                        if existing_cart_ingredient.unit != item['unit']:
                            CartIngredient.objects.create(
                                cart=cart,
                                ingredient=ingredient,
                                quantity=item['quantity'],
                                unit=item['unit']
                            )
                        else:
                            existing_cart_ingredient.quantity += item['quantity']
                            existing_cart_ingredient.save()
                    else:
                        CartIngredient.objects.create(
                            cart=cart,
                            ingredient=ingredient,
                            quantity=item['quantity'],
                            unit=item['unit']
                        )

                return Response({"message": "Ingredients from recipe added to cart."}, status=status.HTTP_201_CREATED)

            except Recipe.DoesNotExist:
                return Response({"message": "Recipe not found."}, status=status.HTTP_404_NOT_FOUND)

        return Response({"message": "No ingredients or recipe ID provided."}, status=status.HTTP_400_BAD_REQUEST)
    def get(self, request):
        """
        Retrieves the ingredients in the user's cart.
        """
        user = request.user
        cart = self.get_cart(user)

        cart_ingredients = CartIngredient.objects.filter(cart=cart)
        cart_ingredients_data = []

        for item in cart_ingredients:
            cart_ingredients_data.append({
                'id': item.id,
                'ingredient_name': item.ingredient.name,
                'quantity': item.quantity,
                'unit': item.unit,
                'bought': item.bought  
            })

        return Response({'cart_ingredients': cart_ingredients_data}, status=status.HTTP_200_OK)

    def patch(self, request, ingredient_id):
        """
        Update the quantity or 'bought' status of a specific ingredient in the cart.
        """
        user = request.user
        cart = self.get_cart(user)

        try:
            cart_ingredient = CartIngredient.objects.get(cart=cart, id=ingredient_id)
        except CartIngredient.DoesNotExist:
            return Response({"message": "Ingredient not found in cart."}, status=status.HTTP_404_NOT_FOUND)

        quantity = request.data.get('quantity')
        if quantity is not None:
            cart_ingredient.quantity = quantity
            
        bought = request.data.get('bought')
        if bought is not None:
            cart_ingredient.bought = bought

        cart_ingredient.save()
        return Response({"message": "Cart ingredient updated."}, status=status.HTTP_200_OK)

    def delete(self, request, ingredient_id=None):
        user = request.user
        cart = self.get_cart(user)

        if ingredient_id:
            try:
                cart_ingredient = CartIngredient.objects.get(cart=cart, id=ingredient_id)
                cart_ingredient.delete()  
                return Response({"message": "Ingredient removed from cart."}, status=status.HTTP_200_OK)
            except CartIngredient.DoesNotExist:
                return Response({"message": "Ingredient not found in cart."}, status=status.HTTP_404_NOT_FOUND)
        else:
    
            CartIngredient.objects.filter(cart=cart).delete()  
            return Response({"message": "All ingredients removed from cart."}, status=status.HTTP_200_OK)

# planner_screen
class WeeklyMealPlanView(APIView):
    def post(self, request):
        user = request.user  
        plan_meals_for_week(user)
        today = datetime.today().date()

        weekly_plan = []
        
        for i in range(7):
            plan_date = today + timedelta(days=i)

            day_plan, created = DayPlan.objects.get_or_create(user=user, date=plan_date)

            recipes = DayPlanRecipes.objects.filter(day_plan=day_plan).select_related('recipe')
            recipe_data = [
                {
                    'id': recipe.recipe.id,
                    'title': recipe.recipe.title,
                    'meal_type': recipe.recipe.meal_type,
                    'total_calories': recipe.recipe.total_calories,
                    'description':recipe.recipe.description,
                }
                for recipe in recipes
            ]

            weekly_plan.append({
                'date': plan_date.strftime('%Y-%m-%d'),  
                'recipes': recipe_data,
            })

        return Response({"weekly_plan": weekly_plan}, status=status.HTTP_200_OK)

    def get(self, request):
    
        user = request.user  


        today = datetime.today().date()
        end_date = today + timedelta(days=6)

   
        plans = DayPlanRecipes.objects.filter(
            day_plan__user=user,
            day_plan__date__range=(today, end_date)
        ).select_related('day_plan', 'recipe').order_by('day_plan__date', 
            Case(
                When(recipe__meal_type='breakfast', then=Value(1)),
                When(recipe__meal_type='lunch', then=Value(2)),
                When(recipe__meal_type='snack', then=Value(3)),
                When(recipe__meal_type='dinner', then=Value(4)),
                default=Value(5),
                output_field=IntegerField()
            )
        )

        planned_recipes = {}
        for plan in plans:
            plan_date = plan.day_plan.date.strftime('%Y-%m-%d')  # Convert date to string
            if plan_date not in planned_recipes:
                planned_recipes[plan_date] = []
            planned_recipes[plan_date].append(RecipeSerializer(plan.recipe).data)

        return Response({"planned_recipes": planned_recipes}, status=status.HTTP_200_OK)

    
    def patch(self, request):
        user = request.user
        day = request.data.get("day")  
        current_recipe_id = request.data.get("current_recipe_id")
        new_recipe_id = request.data.get("new_recipe_id")

        if not (day and current_recipe_id and new_recipe_id):
            return Response(
                {"error": "Missing required parameters: day, current_recipe_id, or new_recipe_id."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            plan_date = datetime.strptime(day, "%Y-%m-%d").date()

            day_plan = DayPlan.objects.filter(user=user, date=plan_date).first()
            if not day_plan:
                return Response({"error": "No meal plan found for the specified day."}, status=status.HTTP_404_NOT_FOUND)

            day_plan_recipe = DayPlanRecipes.objects.filter(day_plan=day_plan, recipe_id=current_recipe_id).first()
            if not day_plan_recipe:
                return Response({"error": "The specified recipe is not part of the day's meal plan."}, status=status.HTTP_404_NOT_FOUND)

            new_recipe = Recipe.objects.filter(id=new_recipe_id).first()
            if not new_recipe:
                return Response({"error": "The specified new recipe does not exist."}, status=status.HTTP_404_NOT_FOUND)

            if DayPlanRecipes.objects.filter(day_plan=day_plan, recipe_id=new_recipe_id).exists():
                return Response(
                    {"error": "The recipe is already assigned to this day."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            day_plan_recipe.recipe = new_recipe
            day_plan_recipe.save()

            return Response({"message": "Recipe updated successfully."})

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DayPlanItemView(APIView):
    def post(self, request):
        user = request.user
        date = request.data.get('date')
        items = request.data.get('items', [])

        if not date or not items:
            return Response({"detail": "Date and items are required."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            plan_date = datetime.strptime(date, "%Y-%m-%d").date()
        except ValueError:
            return Response({"detail": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)

        for item in items:
            item_name = item.get('item_name')
            total_calories = item.get('total_calories', 0)

            if not item_name:
                return Response(
                    {"detail": "Each item must have 'item_name'."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            DayPlanItem.objects.create(
                user=user,
                date=plan_date,  
                item_name=item_name,
                total_calories=total_calories,
                total_protein=item.get('total_protein', 0),
                total_fats=item.get('total_fats', 0),
                total_carbs=item.get('total_carbs', 0),
                total_sugars=item.get('total_sugars', 0),
                total_iron=item.get('total_iron', 0),
                total_potassium=item.get('total_potassium', 0),
            )

        return Response({"detail": "Items added successfully."}, status=status.HTTP_201_CREATED)

    def get(self, request):
        items = DayPlanItem.objects.filter(user=request.user).order_by('date')

        items_by_date = {}
        for item in items:
            date_str = item.date.strftime('%Y-%m-%d')
            if date_str not in items_by_date:
                items_by_date[date_str] = []

            items_by_date[date_str].append({
                'id': item.id,
                'item_name': item.item_name,
                'total_calories': item.total_calories,
                'total_protein': item.total_protein,
                'total_fats': item.total_fats,
                'total_carbs': item.total_carbs,
                'total_sugars': item.total_sugars,
                'total_iron': item.total_iron,
                'total_potassium': item.total_potassium,
                'quantity': item.quantity,
            })

        return Response({"items_by_date": items_by_date}, status=status.HTTP_200_OK)

    def patch(self, request, item_id):
        try:
            item = DayPlanItem.objects.get(id=item_id, user=request.user)
        except DayPlanItem.DoesNotExist:
            return Response({"detail": "Item not found."}, status=status.HTTP_404_NOT_FOUND)

        data = request.data
        item.item_name = data.get('item_name', item.item_name)
        item.total_calories = data.get('total_calories', item.total_calories)
        item.total_protein = data.get('total_protein', item.total_protein)
        item.total_fats = data.get('total_fats', item.total_fats)
        item.total_carbs = data.get('total_carbs', item.total_carbs)
        item.total_sugars = data.get('total_sugars', item.total_sugars)
        item.total_iron = data.get('total_iron', item.total_iron)
        item.total_potassium = data.get('total_potassium', item.total_potassium)
        item.quantity = data.get('quantity', item.quantity)
        item.date = datetime.strptime(data.get('date', item.date.strftime('%Y-%m-%d')), "%Y-%m-%d").date()
        item.save()

        return Response({"detail": "Item updated successfully."}, status=status.HTTP_200_OK)

    def delete(self, request, item_id):
        try:
            item = DayPlanItem.objects.get(id=item_id, user=request.user)
            item.delete()
            return Response({"detail": "Item deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except DayPlanItem.DoesNotExist:
            return Response({"detail": "Item not found."}, status=status.HTTP_404_NOT_FOUND)

class ResetMealPlansView(APIView):
    permission_classes = [IsAuthenticated]  

    def delete(self, request):
        DayPlanRecipes.objects.filter(day_plan__user=request.user).delete()
        DayPlan.objects.filter(user=request.user).delete()

        return Response({"message": "Your meal plans have been deleted successfully."}, status=status.HTTP_200_OK)
    

class NutrientSummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        recipe_fields = ['total_calories', 'sugars', 'protein', 'iron', 'potassium', 'carbohydrates', 'fat', 'fiber']
        preference_fields = {
            'total_calories': ['min_calories', 'max_calories'],
            'sugars': ['min_sugars', 'max_sugars'],
            'protein': ['min_protein', 'max_protein'],
            'fat': ['min_fat', 'max_fat'],
            'carbohydrates': ['min_carbohydrates', 'max_carbohydrates'],
            'fiber': ['min_fiber', 'max_fiber'],
            'iron': ['min_iron', 'max_iron'],
            'potassium': ['min_potassium', 'max_potassium']
        }

        aggregates = {field: 0 for field in recipe_fields}

        planned_recipes = DayPlanRecipes.objects.filter(day_plan__user=user)

        for plan_recipe in planned_recipes:
            recipe = plan_recipe.recipe
            for field in recipe_fields:
                value = getattr(recipe, field, 0) or 0  
                try:
                    aggregates[field] += float(value)
                except ValueError:
                    aggregates[field] += 0  

        try:
            preferences = UserNutrientPreferences.objects.get(user=user)
        except UserNutrientPreferences.DoesNotExist:
            return Response(
                {"detail": "User nutrient preferences not set."},
                status=status.HTTP_404_NOT_FOUND
            )

        comparisons = {}
        for field in recipe_fields:
            min_field, max_field = preference_fields[field]

            min_value = getattr(preferences, min_field, None) * 7
            max_value = getattr(preferences, max_field, None) * 7

           

            total = aggregates[field]

            comparisons[field] = {
                "total": total,
                "min_7_days": min_value,
                "max_7_days": max_value,
    
            }

        return Response({"comparisons": comparisons})



class WeeklyNutritionView(APIView):
    def get_date_range(self, request):
        try:
            if request.query_params.get('start_date') and request.query_params.get('end_date'):
                start_date = datetime.strptime(
                    request.query_params.get('start_date'), 
                    '%Y-%m-%d'
                ).date()
                end_date = datetime.strptime(
                    request.query_params.get('end_date'), 
                    '%Y-%m-%d'
                ).date()
            else:
                end_date = datetime.now().date()
                end_date = end_date - timedelta(days=end_date.weekday())
                end_date = end_date + timedelta(days=6)
                start_date = end_date - timedelta(weeks=4) - timedelta(days=6)
            
            return start_date, end_date
            
        except (TypeError, ValueError):
            raise ValueError("Invalid date format. Use YYYY-MM-DD")

    def get_cumulative_nutrition(self, user, start_date, current_date):
        day_plans = DayPlan.objects.filter(
            user=user,
            date__range=[start_date, current_date]
        )
        
        recipe_nutrition = DayPlanRecipes.objects.filter(
            day_plan__in=day_plans
        ).aggregate(
            calories=Sum(Cast('recipe__total_calories', output_field=IntegerField())),
            carbohydrates=Sum(Cast('recipe__carbohydrates', output_field=IntegerField())),
            fat=Sum(Cast('recipe__fat', output_field=IntegerField())),
            protein=Sum(Cast('recipe__protein', output_field=IntegerField())),
            fiber=Sum(Cast('recipe__fiber', output_field=IntegerField())),
            sugars=Sum(Cast('recipe__sugars', output_field=IntegerField())),
            iron=Sum(Cast('recipe__iron', output_field=IntegerField())),
            potassium=Sum(Cast('recipe__potassium', output_field=IntegerField()))
        )

        item_nutrition = DayPlanItem.objects.filter(
            user=user,
            date__range=[start_date, current_date]
        ).aggregate(
            calories=Sum(F('total_calories') * F('quantity')),
            carbohydrates=Sum(F('total_carbs') * F('quantity')),
            fat=Sum(F('total_fats') * F('quantity')),
            protein=Sum(F('total_protein') * F('quantity')),
            fiber=Sum(F('total_fiber') * F('quantity')),
            sugars=Sum(F('total_sugars') * F('quantity')),
            iron=Sum(F('total_iron') * F('quantity')),
            potassium=Sum(F('total_potassium') * F('quantity'))
        )

        combined_nutrition = {}
        for key in recipe_nutrition.keys():
            recipe_value = Decimal('0') if recipe_nutrition[key] is None else Decimal(str(recipe_nutrition[key]))
            item_value = Decimal('0') if item_nutrition[key] is None else Decimal(str(item_nutrition[key]))
            combined_nutrition[key] = recipe_value + item_value

        return combined_nutrition

    def get_daily_nutrition(self, user, date):
        nutrition_keys = [
            'calories', 'carbohydrates', 'fat', 'protein',
            'fiber', 'sugars', 'iron', 'potassium'
        ]
        
        day_plan = DayPlan.objects.filter(
            user=user,
            date=date
        ).first()
        
        recipe_nutrition = {key: Decimal('0') for key in nutrition_keys}
        if day_plan:
            recipe_values = DayPlanRecipes.objects.filter(
                day_plan=day_plan
            ).aggregate(
                calories=Sum(Cast('recipe__total_calories', output_field=IntegerField())),
                carbohydrates=Sum(Cast('recipe__carbohydrates', output_field=IntegerField())),
                fat=Sum(Cast('recipe__fat', output_field=IntegerField())),
                protein=Sum(Cast('recipe__protein', output_field=IntegerField())),
                fiber=Sum(Cast('recipe__fiber', output_field=IntegerField())),
                sugars=Sum(Cast('recipe__sugars', output_field=IntegerField())),
                iron=Sum(Cast('recipe__iron', output_field=IntegerField())),
                potassium=Sum(Cast('recipe__potassium', output_field=IntegerField()))
            )
            for key in nutrition_keys:
                if recipe_values.get(key) is not None:
                    recipe_nutrition[key] = Decimal(str(recipe_values[key]))

        item_nutrition = DayPlanItem.objects.filter(
            user=user,
            date=date
        ).aggregate(
            calories=Sum(F('total_calories') * F('quantity')),
            carbohydrates=Sum(F('total_carbs') * F('quantity')),
            fat=Sum(F('total_fats') * F('quantity')),
            protein=Sum(F('total_protein') * F('quantity')),
            fiber=Sum(F('total_fiber') * F('quantity')),
            sugars=Sum(F('total_sugars') * F('quantity')),
            iron=Sum(F('total_iron') * F('quantity')),
            potassium=Sum(F('total_potassium') * F('quantity'))
        )

        combined_nutrition = {}
        for key in nutrition_keys:
            item_value = Decimal('0') if item_nutrition.get(key) is None else Decimal(str(item_nutrition[key]))
            combined_nutrition[key] = recipe_nutrition[key] + item_value

        return combined_nutrition

    def serialize_nutrition_values(self, nutrition_data):
        return {
            key: str(value) if isinstance(value, Decimal) else value
            for key, value in nutrition_data.items()
        }

    def get(self, request):
        try:
            start_date, end_date = self.get_date_range(request)
        except ValueError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = request.user
        response_data = []
        
        current_date = start_date
        while current_date <= end_date:
            week_start = current_date - timedelta(days=current_date.weekday())
            week_end = min(week_start + timedelta(days=6), end_date)
            
            week_data = {
                'week_start': week_start.strftime('%Y-%m-%d'),
                'week_end': week_end.strftime('%Y-%m-%d'),
                'days': []
            }
            
            current_week_date = week_start
            while current_week_date <= week_end:
                daily_nutrition = self.get_daily_nutrition(user, current_week_date)
                cumulative_nutrition = self.get_cumulative_nutrition(
                    user, 
                    week_start, 
                    current_week_date
                )
                
                day_data = {
                    'date': current_week_date.strftime('%Y-%m-%d'),
                    'day_of_week': current_week_date.strftime('%A'),
                    'daily_totals': self.serialize_nutrition_values(daily_nutrition),
                    'cumulative_totals': self.serialize_nutrition_values(cumulative_nutrition)
                }
                week_data['days'].append(day_data)
                current_week_date += timedelta(days=1)
            
            response_data.append(week_data)
            current_date = week_end + timedelta(days=1)
        
        return Response(response_data)
    
    
  
# UPDATE DATA
@api_view(['GET'])
def upload_recipes_csv(request):
    file_path = 'updated_data.csv'  
    success, message = upload_recipes_from_csv(file_path)

    if success:
        return Response({'message': message}, status=status.HTTP_201_CREATED)
    else:
        return Response({'error': message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
