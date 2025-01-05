import React, { useState, useEffect } from "react";
import { useFocusEffect } from "@react-navigation/native";
import {
  View,
  Text,
  ScrollView,
  TouchableOpacity,
  ActivityIndicator,
  SafeAreaView,
  Dimensions,
  Pressable,
  Animated,
} from "react-native";
import { format, parseISO } from "date-fns";
import {
  ChevronRight,
  RotateCcw,
  Share,
  ChevronDown,
  ChevronUp,
  X,
} from "react-native-feather";
import api from "../utils/api";

const { width: SCREEN_WIDTH, height: SCREEN_HEIGHT } = Dimensions.get("window");

const MEAL_TYPES = ["breakfast", "lunch", "dinner", "snack"];

const NutrientItem = ({ label, data, unit }) => {
  const range = data.max_7_days - data.min_7_days;
  const percentage = Math.min(
    Math.max(((data.total - data.min_7_days) / range) * 100, 0),
    100
  );

  return (
    <View className="mb-6">
      <View className="flex-row justify-between mb-2">
        <Text className="text-base font-medium text-gray-600">{label}</Text>
        <Text className="text-base text-gray-600">
          {data.total.toLocaleString()} {unit}
        </Text>
      </View>

      <View className="h-3 bg-gray-100 rounded-full overflow-hidden">
        <View
          className="h-full bg-[#F5A623]"
          style={{ width: `${percentage}%` }}
        />
      </View>

      <View className="flex-row justify-between mt-2">
        <Text className="text-sm text-gray-500">
          Min: {data.min_7_days.toLocaleString()} {unit}
        </Text>
        <Text className="text-sm text-gray-500">
          Max: {data.max_7_days.toLocaleString()} {unit}
        </Text>
      </View>
    </View>
  );
};

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
  const [nutrientData, setNutrientData] = useState(null);
  const [loadingNutrients, setLoadingNutrients] = useState(true);
  const [isNutrientSummaryExpanded, setIsNutrientSummaryExpanded] =
    useState(false);
  const [summaryAnimation] = useState(new Animated.Value(0));

  const fetchNutrientData = async () => {
    try {
      setLoadingNutrients(true);
      const response = await api.get("/nutrient-summary/");
      setNutrientData(response.data);
    } catch (error) {
      console.error("Error fetching nutrient data:", error);
    } finally {
      setLoadingNutrients(false);
    }
  };

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
      fetchNutrientData();
    }, [])
  );

  const toggleNutrientSummary = () => {
    const toValue = isNutrientSummaryExpanded ? 0 : 1;
    setIsNutrientSummaryExpanded(!isNutrientSummaryExpanded);
    Animated.spring(summaryAnimation, {
      toValue,
      useNativeDriver: true,
      tension: 20,
      friction: 7,
    }).start();
  };

  const selectedDayPlan = weeklyPlan.find((day) => day.date === selectedDate);

  const getRecipesByType = (type) => {
    return (
      selectedDayPlan?.recipes.filter((recipe) => recipe.meal_type === type) ||
      []
    );
  };

  if (loading) {
    return (
      <View className="flex-1 justify-center items-center bg-white">
        <ActivityIndicator size="large" color="#F5A623" />
      </View>
    );
  }

  const renderNutrientSummary = (fullScreen = false) => {
    if (loadingNutrients) {
      return (
        <View
          className={`p-4 bg-white rounded-lg ${
            !fullScreen && "shadow-sm mb-4"
          }`}
        >
          <ActivityIndicator size="small" color="#F5A623" />
        </View>
      );
    }

    if (!nutrientData) return null;

    return (
      <View className={`bg-white rounded-lg ${!fullScreen && "shadow-sm"}`}>
        <TouchableOpacity
          onPress={fullScreen ? null : toggleNutrientSummary}
          className="flex-row justify-between items-center p-4"
        >
          <Text className="text-lg font-semibold text-[#2D3748]">
            Weekly Nutrient Summary
          </Text>
          {!fullScreen && (
            <View className="flex-row items-center">
              {isNutrientSummaryExpanded ? (
                <ChevronUp size={20} stroke="#666" />
              ) : (
                <ChevronDown size={20} stroke="#666" />
              )}
            </View>
          )}
        </TouchableOpacity>

        <Animated.View
          style={{
            opacity: fullScreen ? 1 : summaryAnimation,
            transform: [
              {
                translateY: fullScreen
                  ? 0
                  : summaryAnimation.interpolate({
                      inputRange: [0, 1],
                      outputRange: [-20, 0],
                    }),
              },
            ],
          }}
          className={`px-4 ${fullScreen ? "pb-6" : "pb-4"}`}
        >
          {(isNutrientSummaryExpanded || fullScreen) && (
            <>
              <NutrientItem
                label="Calories"
                data={nutrientData.comparisons.total_calories}
                unit="kcal"
              />

              <NutrientItem
                label="Sugars"
                data={nutrientData.comparisons.sugars}
                unit="g"
              />

              <NutrientItem
                label="Protein"
                data={nutrientData.comparisons.protein}
                unit="g"
              />

              <NutrientItem
                label="Iron"
                data={nutrientData.comparisons.iron}
                unit="mg"
              />

              <NutrientItem
                label="Potassium"
                data={nutrientData.comparisons.potassium}
                unit="mg"
              />
            </>
          )}
        </Animated.View>
      </View>
    );
  };

  return (
    <SafeAreaView className="flex-1 bg-white">
      <View className="flex-1">
        <ScrollView className="flex-1">
          {/* Nutrient Summary Section */}
          <View className="px-4 pt-4">{renderNutrientSummary(false)}</View>

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
