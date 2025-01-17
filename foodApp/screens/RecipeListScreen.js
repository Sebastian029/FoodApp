import React, { useState, useEffect } from "react";
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  ScrollView,
  ActivityIndicator,
  SafeAreaView,
} from "react-native";
import { Search, ChevronRight } from "react-native-feather";
import api from "../utils/api";

export default function RecipeListScreen({ navigation, route }) {
  const [recipes, setRecipes] = useState([]); 
  const [filteredRecipes, setFilteredRecipes] = useState([]); 
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedRecipe, setSelectedRecipe] = useState(null);

  const fetchRecipes = async () => {
    try {
      const response = await api.get(
        `/recipes/by-type/?meal_type=${route.params?.type || ""}`
      );
      setRecipes(response.data);
      setFilteredRecipes(response.data); 
    } catch (error) {
      console.error("Error fetching recipes:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchRecipes();
  }, [route.params?.type]);

  const handleSearch = (query) => {
    setSearchQuery(query);
    if (query.trim() === "") {
      setFilteredRecipes(recipes);
    } else {
      const queryIngredients = query
        .toLowerCase()
        .split(" ")
        .map((ingredient) => ingredient.trim());

      setFilteredRecipes(
        recipes.filter((recipe) =>
          queryIngredients.every((ingredient) =>
            recipe.ingredients.some((item) =>
              item.ingredient_name.toLowerCase().includes(ingredient)
            )
          )
        )
      );
    }
  };

  const handleRecipePress = (recipe) => {
    setSelectedRecipe(recipe.id);
    navigation.navigate("RecipeDetail", { recipeId: recipe.id });
  };

  return (
    <SafeAreaView className="flex-1 bg-white">
      <View className="px-4 mt-4 mb-4">
        <View className="flex-row items-center bg-white rounded-lg shadow-sm px-4 py-2 border border-gray-300">
          <Search stroke="#666" size={20} />
          <TextInput
            className="flex-1 ml-2 text-base text-gray-800"
            placeholder="Search recipes..."
            value={searchQuery}
            onChangeText={handleSearch}
          />
        </View>
      </View>

      {loading ? (
        <View className="flex-1 justify-center items-center">
          <ActivityIndicator size="large" color="#F5A623" />
        </View>
      ) : (
        <ScrollView
          className="flex-1 px-4"
          showsVerticalScrollIndicator={false}
        >
          {filteredRecipes.map((recipe) => (
            <TouchableOpacity
              key={recipe.id}
              onPress={() => handleRecipePress(recipe)}
              className={`mb-3 bg-white rounded-xl p-4 flex-row items-center justify-between ${
                selectedRecipe === recipe.id
                  ? "border border-[#3B82F6]"
                  : "border border-transparent"
              }`}
              style={{
                shadowColor: "#000",
                shadowOffset: { width: 0, height: 1 },
                shadowOpacity: 0.05,
                shadowRadius: 2,
                elevation: 2,
              }}
            >
              <View className="flex-1 pr-4">
                <Text className="text-lg font-semibold text-[#2D3748] mb-1">
                  {recipe.title}
                </Text>
                <Text className="text-gray-600 text-sm">
                  {recipe.description ||
                    "Juicy grilled chicken breast with seasoning."}
                </Text>
              </View>
              <ChevronRight
                stroke={selectedRecipe === recipe.id ? "#3B82F6" : "#666"}
                size={20}
              />
            </TouchableOpacity>
          ))}
        </ScrollView>
      )}
    </SafeAreaView>
  );
}
