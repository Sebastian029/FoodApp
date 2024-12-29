import React, { useState, useEffect } from "react";
import {
  View,
  Text,
  ScrollView,
  TouchableOpacity,
  ActivityIndicator,
  SafeAreaView,
  Share,
} from "react-native";
import { ArrowLeft, Share2, Plus, Check } from "react-native-feather";
import api from "../utils/api";

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
Iron: ${recipe.iron}mg
Potassium: ${recipe.potassium}mg
Preparation Time: ${recipe.preparation_time} minutes

Preparation Guide:
  ${recipe.preparation_guide.replace(/\n/g, "\n  ")}

Ingredients:
${ingredientsList}
`;

    const result = await Share.share({
      message,
    });

    if (result.action === Share.sharedAction) {
      if (result.activityType) {
        console.log("Shared with activity type:", result.activityType);
      } else {
        console.log("Recipe shared successfully!");
      }
    } else if (result.action === Share.dismissedAction) {
      console.log("Share was dismissed");
    }
  } catch (error) {
    console.error("Error sharing recipe:", error);
  }
};

const NutritionFact = ({ label, value }) => (
  <View className="items-center">
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

    fetchRecipe();
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
      setAddedIngredients((prev) => new Set(prev).add(ingredientName)); // Add ingredient to the set
      setConfirmationMessage(`${ingredientName} added to cart!`);
    } catch (error) {
      console.error("Error adding ingredient to cart:", error);
      setConfirmationMessage("Error adding ingredient to cart.");
    }
  };

  if (loading) {
    return (
      <View className="flex-1 justify-center items-center bg-white">
        <ActivityIndicator size="large" color="#F5A623" />
      </View>
    );
  }

  const preparationSteps = recipe.preparation_guide
    ? recipe.preparation_guide.split(/\d+\./).filter(Boolean)
    : [];

  return (
    <SafeAreaView className="flex-1 bg-white">
      {/* Header with wave */}
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

          {/* Nutrition Facts */}
          <View className="bg-white rounded-xl p-4 mb-6">
            <Text className="text-2xl font-semibold text-[#2D3748] mb-4">
              Nutritions
            </Text>
            <View className="flex-row justify-between">
              <NutritionFact label="calories" value={recipe.total_calories} />
              <NutritionFact label="sugar" value={`${recipe.sugars}g`} />
              <NutritionFact label="protein" value={`${recipe.protein}g`} />
              <NutritionFact label="iron" value={`${recipe.iron}mg`} />
              <NutritionFact
                label="potassium"
                value={`${recipe.potassium}mg`}
              />
            </View>
          </View>

          {/* Ingredients */}
          <View className="bg-white rounded-xl p-4 mb-6">
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
          </View>

          {/* Preparation */}
          <View className="bg-white rounded-xl p-4 mb-6">
            <Text className="text-2xl font-semibold text-[#2D3748] mb-4">
              Preparation ({recipe.preparation_time} min)
            </Text>
            {preparationSteps.length > 0 ? (
              preparationSteps.map((step, index) => (
                <View key={index} className="mb-3">
                  <Text className="text-gray-800">
                    <Text className="font-bold text-[#F5A623]">{`${
                      index + 1
                    }.`}</Text>{" "}
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
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}
