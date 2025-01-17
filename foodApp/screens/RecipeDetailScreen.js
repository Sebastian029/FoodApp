import React, { useState, useEffect } from "react";
import {
  View,
  Text,
  ScrollView,
  TouchableOpacity,
  ActivityIndicator,
  SafeAreaView,
  Modal,
  Share,
} from "react-native";
import { ArrowLeft, Share2, Plus, Check } from "react-native-feather";
import api from "../utils/api";

const formatTime = (minutes) => {
  const hours = Math.floor(minutes / 60);
  const remainingMinutes = minutes % 60;
  return hours > 0
    ? `${hours}h ${remainingMinutes}min`
    : `${remainingMinutes}min`;
};

const handleShare = async (recipe) => {
  try {
    if (!recipe) {
      console.error("Recipe data is not available.");
      return;
    }

    const ingredientsList = recipe.ingredients
      ? recipe.ingredients
          .map(
            (ingredient) =>
              `  • ${ingredient.quantity} ${ingredient.unit} of ${ingredient.ingredient_name}`
          )
          .join("\n")
      : "  No ingredients listed.";

    const message = `
Recipe: ${recipe.title}
Description: ${recipe.description}

Total Calories: ${recipe.total_calories}
Sugars: ${recipe.sugars}g
Protein: ${recipe.protein}g
Fat: ${recipe.fat}g
Carbohydrates: ${recipe.carbohydrates}g
Fiber: ${recipe.fiber}g
Iron: ${recipe.iron}mg
Potassium: ${recipe.potassium}mg
Preparation Time: ${formatTime(recipe.preparation_time)} 

Preparation Guide:
  ${recipe.preparation_guide.replace(/\n/g, "\n  ")}

Ingredients:
${ingredientsList}
`;

    const result = await Share.share({
      message,
    });
  } catch (error) {
    console.error("Error sharing recipe:", error);
  }
};

const NutritionFact = ({ label, value }) => (
  <View className="items-center mx-3">
    <Text className="text-2xl font-bold text-[#2D3748]">{value}</Text>
    <Text className="text-sm text-gray-500">{label}</Text>
  </View>
);

const IngredientItem = ({ amount, unit, name, onAdd, isAdded }) => (
  <View className="flex-row items-center mb-0.5">
    <Text className="text-xl font-semibold text-[#2D3748]">{name}</Text>
    <Text className="text-gray-600 ml-1">
      {amount} {unit}
    </Text>
    <TouchableOpacity
      className="p-1 ml-1"
      onPress={() => !isAdded && onAdd(name, amount, unit)}
      disabled={isAdded}
    >
      <Text
        className={`text-2xl ${isAdded ? "text-gray-400" : "text-[#F5A623]"}`}
      >
        {isAdded ? (
          <Check stroke="#B0BEC5" size={24} />
        ) : (
          <Plus stroke="#F5A623" size={24} />
        )}
      </Text>
    </TouchableOpacity>
  </View>
);

export default function RecipeDetailScreen({ navigation, route }) {
  const [recipe, setRecipe] = useState(null);
  const [loading, setLoading] = useState(true);
  const [confirmationMessage, setConfirmationMessage] = useState(null);
  const [addedIngredients, setAddedIngredients] = useState(new Set());
  const [weeklyPlan, setWeeklyPlan] = useState([]);
  const [modalVisible, setModalVisible] = useState(false);
  const [selectedDay, setSelectedDay] = useState(null);
  const [selectedRecipe, setSelectedRecipe] = useState(null);
  const [newRecipeId, setNewRecipeId] = useState(null);
  const [clicked, setClicked] = useState(false);

  const isFromPlanner = route?.params?.fromPlanner;

  useEffect(() => {
    const fetchRecipe = async () => {
      try {
        const response = await api.get(`/recipes/${route.params.recipeId}/`);
        setRecipe(response.data);
      } catch (error) {
        console.error("Error fetching recipe:", error);
      } finally {
        setLoading(false);
      }
    };

    const fetchWeeklyPlan = async () => {
      try {
        const response = await api.post("/weekly-meal-plan/");
        setWeeklyPlan(response.data.weekly_plan);
      } catch (error) {
        console.error("Error fetching weekly meal plan:", error);
      }
    };

    fetchRecipe();
    fetchWeeklyPlan();
  }, [route.params.recipeId]);

  const addIngredientToCart = async (ingredientName, amount, unit) => {
    try {
      const response = await api.post("/cart/", {
        ingredients: [
          {
            ingredient_name: ingredientName,
            quantity: amount,
            unit: unit,
          },
        ],
      });
      setAddedIngredients((prev) => new Set(prev).add(ingredientName)); 
      setConfirmationMessage(`${ingredientName} added to cart!`);
    } catch (error) {
      console.error("Error adding ingredient to cart:", error);
      setConfirmationMessage("Error adding ingredient to cart.");
    }
  };
  const formatDate = (date) => {
    return new Date(date).toISOString().split("T")[0];
  };

  const handleSaveRecipeChange = async () => {
    if (!selectedDay || !selectedRecipe || !newRecipeId) {
      console.error("Please select a day, recipe, and new recipe.");
      return;
    }

 
    const formattedDate = new Date(selectedDay).toISOString().split("T")[0]; 

    console.log(formattedDate);
    console.log(selectedRecipe.id);
    console.log(newRecipeId);

    try {
      const response = await api.patch("/weekly-meal-plan/", {
        day: formattedDate, 
        current_recipe_id: selectedRecipe.id,
        new_recipe_id: newRecipeId,
      });

      console.log("Recipe changed successfully:", response.data);
      setModalVisible(false);
    } catch (error) {
      console.error(
        "Error saving recipe change:",
        error.response ? error.response.data : error
      );
    }
  };

  const preparationSteps = recipe?.preparation_guide
    ? recipe.preparation_guide.split(/\d+\./).filter(Boolean)
    : [];

  if (loading) {
    return (
      <View className="flex-1 justify-center items-center bg-white">
        <ActivityIndicator size="large" color="#F5A623" />
      </View>
    );
  }
  const addAllIngredientsToCart = async () => {
    if (!clicked) {
      setClicked(true);
      try {
        if (!recipe || !recipe.id) {
          console.error("Recipe ID is not available.");
          return;
        }

        const response = await api.post("/cart/", {
          recipe_id: recipe.id,
        });

        setAddedIngredients(
          new Set(
            recipe.ingredients.map((ingredient) => ingredient.ingredient_name)
          )
        );
        setConfirmationMessage("All ingredients added to cart!");
      } catch (error) {
        console.error("Error adding all ingredients to cart:", error);
        setConfirmationMessage("Error adding all ingredients to cart.");
      }
    }
  };
  return (
    <SafeAreaView className="flex-1 bg-white">
      <View className="relative">
        <View
          className="absolute w-full px-4 flex-row justify-between items-center"
          style={{
            top: 0,
            left: 0,
            right: 0,
            zIndex: 10,
          }}
        >
          <TouchableOpacity onPress={() => navigation.goBack()} className="p-2">
            <ArrowLeft stroke="#2D3748" size={24} />
          </TouchableOpacity>
          <TouchableOpacity onPress={() => handleShare(recipe)} className="p-2">
            <Share2 stroke="#2D3748" size={24} />
          </TouchableOpacity>
        </View>
      </View>

      <ScrollView className="flex-1 px-4 mt-12">
        <View className="bg-white rounded-t-3xl pt-6">
          <Text className="text-2xl font-bold text-[#2D3748] mb-3">
            {recipe.title}
          </Text>
          <Text className="text-gray-600 mb-6 leading-6">
            {recipe.description}
          </Text>

          <View className="bg-white rounded-xl p-4 mb-6">
            <Text className="text-2xl font-semibold text-[#2D3748] mb-4">
              Nutritions
            </Text>
            <ScrollView
              horizontal={true}
              showsHorizontalScrollIndicator={false}
            >
              <View className="flex-row justify-between space-x-200">
                <NutritionFact label="kcal" value={recipe.total_calories} />
                <NutritionFact label="sugar" value={`${recipe.sugars}g`} />
                <NutritionFact label="protein" value={`${recipe.protein}g`} />
                <NutritionFact label="fat" value={`${recipe.fat}g`} />
                <NutritionFact
                  label="carbohydrates"
                  value={`${recipe.carbohydrates}g`}
                />
                <NutritionFact label="fiber" value={`${recipe.fiber}g`} />
                <NutritionFact label="iron" value={`${recipe.iron}mg`} />
                <NutritionFact
                  label="potassium"
                  value={`${recipe.potassium}mg`}
                />
              </View>
            </ScrollView>
          </View>

          <View className="bg-white rounded-xl p-4 mb-0">
            <View className="flex-row justify-between items-center mb-4">
              <Text className="text-2xl font-semibold text-[#2D3748]">
                Ingredients
              </Text>
            </View>
            {recipe.ingredients && recipe.ingredients.length > 0 ? (
              recipe.ingredients.map((ingredient, index) => (
                <IngredientItem
                  key={index}
                  name={ingredient.ingredient_name}
                  amount={ingredient.quantity}
                  unit={ingredient.unit}
                  onAdd={addIngredientToCart}
                  isAdded={addedIngredients.has(ingredient.ingredient_name)}
                />
              ))
            ) : (
              <Text className="text-gray-500">No ingredients listed.</Text>
            )}
            <TouchableOpacity
              className="flex-row items-center p-2 rounded-full"
              style={{
                width: "50%",
                backgroundColor: clicked ? "#d3d3d3" : "#F5A623", 
              }}
              onPress={addAllIngredientsToCart}
              disabled={clicked} 
            >
              <Plus stroke="#fff" size={16} />
              <Text className="text-white text-center font-semibold ml-2 text-sm">
                Add All Ingredients
              </Text>
            </TouchableOpacity>
          </View>

          <View className="bg-white rounded-xl p-4 mb-6">
            <Text className="text-2xl font-semibold text-[#2D3748] mb-4">
              Preparation ({formatTime(recipe.preparation_time)})
            </Text>
            {preparationSteps.length > 0 ? (
              preparationSteps.map((step, index) => (
                <View key={index} className="mb-3">
                  <Text className="text-gray-800">
                    <Text className="font-bold text-[#F5A623]">{`${
                      index + 1
                    }.`}</Text>
                    {step.trim()}
                  </Text>
                </View>
              ))
            ) : (
              <Text className="text-gray-500">
                No preparation steps available.
              </Text>
            )}
          </View>

          <TouchableOpacity
            onPress={() => setModalVisible(true)}
            className={`p-3 rounded-full mt-6 ${
              isFromPlanner ? "bg-gray-400" : "bg-[#F5A623]"
            }`}
            disabled={isFromPlanner}
          >
            <Text className="text-white text-center font-semibold">
              Change Recipe
            </Text>
          </TouchableOpacity>
        </View>
      </ScrollView>

      <Modal
        visible={modalVisible}
        animationType="slide"
        onRequestClose={() => setModalVisible(false)}
      >
        <View className="flex-1 justify-center items-center bg-white p-6 rounded-lg shadow-lg pt-12">
          <Text className="text-2xl font-semibold text-[#2D3748]">
            Select a Day and Recipe
          </Text>
          <ScrollView
            contentContainerStyle={{ flexGrow: 1 }}
            className="w-full"
          >
            <View className="mt-6">
              <Text className="text-lg font-medium text-[#2D3748]">
                Choose Day:
              </Text>

              <ScrollView
                horizontal={true}
                showsHorizontalScrollIndicator={false}
                className="mt-4"
              >
                {weeklyPlan.map((plan, index) => (
                  <TouchableOpacity
                    key={index}
                    onPress={() => setSelectedDay(plan.date)}
                    className="py-3 px-4 mx-2 rounded-lg border border-[#E2E8F0] hover:bg-[#F5F5F5]"
                  >
                    <Text
                      className={`${
                        selectedDay === plan.date
                          ? "text-[#F5A623] font-semibold"
                          : "text-[#2D3748]"
                      }`}
                    >
                      {plan.date}
                    </Text>
                  </TouchableOpacity>
                ))}
              </ScrollView>
            </View>

            <View className="mt-6">
              <Text className="text-lg font-medium text-[#2D3748]">
                Choose Recipe to Replace:
              </Text>
              {selectedDay &&
                weeklyPlan
                  .find((plan) => plan.date === selectedDay)
                  ?.recipes.map((recipe) => (
                    <TouchableOpacity
                      key={recipe.id}
                      onPress={() => setSelectedRecipe(recipe)}
                      className="py-3 px-4 my-2 rounded-lg border border-[#E2E8F0] hover:bg-[#F5F5F5]"
                    >
                      <Text
                        className={`${
                          selectedRecipe?.id === recipe.id
                            ? "text-[#F5A623] font-semibold"
                            : "text-[#2D3748]"
                        }`}
                      >
                        {recipe.title}
                      </Text>
                    </TouchableOpacity>
                  ))}
            </View>

            <View className="mt-6">
              <Text className="text-lg font-medium text-[#2D3748]">
                Choose New Recipe:
              </Text>
              {recipe && (
                <TouchableOpacity
                  onPress={() => setNewRecipeId(recipe.id)}
                  className="py-3 px-4 my-2 rounded-lg border border-[#E2E8F0] hover:bg-[#F5F5F5]"
                >
                  <Text
                    className={`${
                      newRecipeId === recipe.id
                        ? "text-[#F5A623] font-semibold"
                        : "text-[#2D3748]"
                    }`}
                  >
                    {recipe.title}
                  </Text>
                </TouchableOpacity>
              )}
            </View>

            <View className="flex-row justify-between mt-8">
              <TouchableOpacity
                onPress={handleSaveRecipeChange}
                className="w-1/2 bg-[#F5A623] rounded-lg py-3 px-6 items-center justify-center"
              >
                <Text className="text-white font-semibold text-lg">Save</Text>
              </TouchableOpacity>

              <TouchableOpacity
                onPress={() => setModalVisible(false)}
                className="w-1/2 bg-white border border-[#CBD5E0] rounded-lg py-3 px-6 items-center justify-center"
              >
                <Text className="text-[#2D3748] font-semibold text-lg">
                  Cancel
                </Text>
              </TouchableOpacity>
            </View>
          </ScrollView>
        </View>
      </Modal>
    </SafeAreaView>
  );
}
