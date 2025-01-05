import React, { useState, useEffect } from "react";
import { useFocusEffect } from "@react-navigation/native";
import {
  View,
  Text,
  ScrollView,
  TouchableOpacity,
  ActivityIndicator,
  SafeAreaView,
} from "react-native";
import { format, parseISO } from "date-fns";
import { ChevronRight, RotateCcw, Share } from "react-native-feather";
import api from "../utils/api";

const WEEK_TOTALS = [
  { day: "Mon", calories: 1000 },
  { day: "Tue", calories: 1000 },
  { day: "Wed", calories: 1000 },
  { day: "Thu", calories: 1000 },
];

const MEAL_TYPES = ["breakfast", "lunch", "dinner", "snack"];

const CalorieCircle = ({ day, calories, progress = 0.75 }) => (
  <View className="items-center mx-2">
    <View className="w-16 h-16 relative">
      <View className="w-full h-full rounded-full border-4 border-[#3B82F6] opacity-20" />
      <View
        className="absolute top-0 left-0 w-full h-full rounded-full border-4 border-[#3B82F6]"
        style={{
          clip: `rect(0, ${32 * progress}px, 64px, 0)`,
        }}
      />
      <View className="absolute top-0 left-0 w-full h-full items-center justify-center">
        <Text className="text-xs text-gray-600">{calories}</Text>
        <Text className="text-xs text-gray-600">kcal</Text>
      </View>
    </View>
    <Text className="text-xs text-gray-600 mt-1">{day}</Text>
  </View>
);

const MealItem = ({ recipe, onRefresh, onPress }) => (
  <TouchableOpacity
    onPress={onPress}
    className="flex-row items-center justify-between bg-white rounded-lg p-4 mb-3"
  >
    <View className="flex-1">
      <Text className="text-lg font-semibold text-[#2D3748]">
        {recipe.title}
      </Text>
      <Text className="text-gray-600 text-sm">
        {recipe.description || "Juicy grilled chicken breast with seasoning."}
      </Text>
    </View>
    <View className="flex-row items-center">
      <ChevronRight size={20} stroke="#666" />
    </View>
  </TouchableOpacity>
);

export default function PlannerScreen({ navigation }) {
  const [weeklyPlan, setWeeklyPlan] = useState([]);
  const [selectedDate, setSelectedDate] = useState(null);
  const [loading, setLoading] = useState(true);

  const fetchWeeklyPlan = async () => {
    try {
      setLoading(true);
      setWeeklyPlan([]); // Reset state before fetching
      setSelectedDate(null);
      const response = await api.post("/weekly-meal-plan/");
      setWeeklyPlan(response.data.weekly_plan);
      setSelectedDate(response.data.weekly_plan[0]?.date);
    } catch (error) {
      console.error("Error fetching weekly plan:", error);
    } finally {
      setLoading(false);
    }
  };

  useFocusEffect(
    React.useCallback(() => {
      fetchWeeklyPlan();
    }, [])
  );

  const selectedDayPlan = weeklyPlan.find((day) => day.date === selectedDate);

  const getRecipesByType = (type) => {
    return (
      selectedDayPlan?.recipes.filter((recipe) => recipe.meal_type === type) ||
      []
    );
  };

  const handleRefreshMeal = async (mealType) => {
    // TODO: Implement meal refresh logic
    console.log("Refreshing meal:", mealType);
  };

  if (loading) {
    return (
      <View className="flex-1 justify-center items-center bg-white">
        <ActivityIndicator size="large" color="#F5A623" />
      </View>
    );
  }

  return (
    <SafeAreaView className="flex-1 bg-white">
      <View className="flex-1">
        {/* Main Content ScrollView */}
        <ScrollView className="flex-1">
          {/* <View className="pt-6 pb-4">
            <Text className="text-lg font-semibold text-center mb-4">
              Week Total
            </Text>
            <View className="flex-row justify-center px-4">
              {WEEK_TOTALS.map((total, index) => (
                <CalorieCircle
                  key={index}
                  day={total.day}
                  calories={total.calories}
                />
              ))}
            </View>
          </View> */}

          {/* Date Selector - Horizontal ScrollView */}
          <View className="px-4 py-2 border-t border-b border-gray-100">
            <ScrollView horizontal showsHorizontalScrollIndicator={false}>
              {weeklyPlan.map((day) => (
                <TouchableOpacity
                  key={day.date}
                  onPress={() => setSelectedDate(day.date)}
                  className={`w-32 h-10 rounded-lg flex items-center justify-center mr-2 ${
                    selectedDate === day.date ? "bg-[#475569]" : "bg-gray-100"
                  }`}
                >
                  <Text
                    className={`${
                      selectedDate === day.date
                        ? "text-white font-medium"
                        : "text-gray-600"
                    } text-sm`}
                  >
                    {format(parseISO(day.date), "EEEE d")}
                  </Text>
                </TouchableOpacity>
              ))}
            </ScrollView>
          </View>

          {/* Meal List */}
          <View className="flex-1 px-4 pt-4">
            {MEAL_TYPES.map((type) => {
              const recipes = getRecipesByType(type);
              if (recipes.length === 0) return null;

              return (
                <View key={type} className="mb-4">
                  <Text className="text-[#2D3748] font-semibold text-lg capitalize mb-2">
                    {type}
                  </Text>
                  {recipes.map((recipe) => (
                    <MealItem
                      key={recipe.id}
                      recipe={recipe}
                      onRefresh={() => handleRefreshMeal(type)}
                      onPress={() =>
                        navigation.navigate("RecipeDetail", {
                          recipeId: recipe.id,
                          fromPlanner: true,
                        })
                      }
                    />
                  ))}
                </View>
              );
            })}
          </View>
        </ScrollView>
      </View>
    </SafeAreaView>
  );
}
