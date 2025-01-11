import React, { useState, useEffect } from "react";
import {
  View,
  Text,
  ScrollView,
  TouchableOpacity,
  ActivityIndicator,
  SafeAreaView,
} from "react-native";
import { format, parseISO } from "date-fns";
import { ArrowLeft, ArrowRight } from "react-native-feather";
import api from "../utils/api";

const NUTRIENTS = [
  { key: "calories", label: "Calories", unit: "kcal" },
  { key: "carbohydrates", label: "Carbs", unit: "g" },
  { key: "fat", label: "Fat", unit: "g" },
  { key: "protein", label: "Protein", unit: "g" },
  { key: "fiber", label: "Fiber", unit: "g" },
  { key: "sugars", label: "Sugars", unit: "g" },
  { key: "iron", label: "Iron", unit: "mg" },
  { key: "potassium", label: "Potassium", unit: "mg" },
];

const NutrientRow = ({ label, value, unit, isTotal = false }) => (
  <View className="flex-row justify-between items-center py-2">
    <Text className={`${isTotal ? "font-semibold" : ""} text-gray-700`}>
      {label}
    </Text>
    <Text className={`${isTotal ? "font-semibold" : ""} text-gray-900`}>
      {parseFloat(value).toLocaleString()} {unit}
    </Text>
  </View>
);

const DayCard = ({ dayData }) => {
  const [expanded, setExpanded] = useState(false);

  return (
    <TouchableOpacity
      onPress={() => setExpanded(!expanded)}
      className="bg-white rounded-xl shadow-sm p-4 mb-4"
    >
      <View className="flex-row justify-between items-center mb-2">
        <View>
          <Text className="text-lg font-semibold text-[#2D3748]">
            {dayData.day_of_week}
          </Text>
          <Text className="text-sm text-gray-500">
            {format(parseISO(dayData.date), "MMM d, yyyy")}
          </Text>
        </View>
        <View className="items-end">
          <Text className="text-base font-medium text-[#2D3748]">
            {parseFloat(dayData.daily_totals.calories).toLocaleString()} kcal
          </Text>
        </View>
      </View>

      {expanded && (
        <View className="mt-4 pt-4 border-t border-gray-100">
          <Text className="text-base font-semibold text-[#2D3748] mb-2">
            Daily Totals
          </Text>
          {NUTRIENTS.map((nutrient) => (
            <NutrientRow
              key={nutrient.key}
              label={nutrient.label}
              value={dayData.daily_totals[nutrient.key]}
              unit={nutrient.unit}
            />
          ))}
        </View>
      )}
    </TouchableOpacity>
  );
};

const WeekSummary = ({ weekData, weekRange }) => {
  if (!weekData || !weekData.days) return null;

  const currentDate = new Date();
  const weekStart = new Date(weekRange.week_start);
  const weekEnd = new Date(weekRange.week_end);

  const isCurrentWeek = currentDate >= weekStart && currentDate <= weekEnd;

  let targetDayData;
  if (isCurrentWeek) {
    targetDayData = weekData.days.find((day) => {
      const dayDate = new Date(day.date);
      return dayDate.toDateString() === currentDate.toDateString();
    });
  } else {
    targetDayData = weekData.days[weekData.days.length - 1];
  }

  if (!targetDayData) return null;

  return (
    <View className="bg-[#F5A623] rounded-xl p-4 mb-6">
      <View className="flex-row justify-between items-center mb-4">
        <Text className="text-white text-lg font-semibold">Week Summary</Text>
        <Text className="text-white text-sm">
          {format(parseISO(weekRange.week_start), "MMM d")} -{" "}
          {format(parseISO(weekRange.week_end), "MMM d, yyyy")}
        </Text>
      </View>
      <View className="space-y-2">
        {NUTRIENTS.map((nutrient) => (
          <View key={nutrient.key} className="flex-row justify-between">
            <Text className="text-white">{nutrient.label}</Text>
            <Text className="text-white font-medium">
              {parseFloat(
                targetDayData.cumulative_totals[nutrient.key]
              ).toLocaleString()}{" "}
              {nutrient.unit}
            </Text>
          </View>
        ))}
      </View>
    </View>
  );
};

export default function WeeklyNutritionScreen({ navigation }) {
  const [allWeeks, setAllWeeks] = useState([]);
  const [currentWeekIndex, setCurrentWeekIndex] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchWeeklyNutrition = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await api.get("/weekly-nutrition/");

      if (response.data && Array.isArray(response.data)) {
        const weeksData = response.data.map((week) => ({
          ...week,
          days: week.days.sort((a, b) => new Date(b.date) - new Date(a.date)),
        }));
        setAllWeeks(weeksData);
      } else {
        setError("Invalid data structure received");
      }
    } catch (err) {
      setError("Failed to load nutrition data");
    } finally {
      setLoading(false);
    }
  };

  const handlePrevWeek = () => {
    if (currentWeekIndex < allWeeks.length - 1) {
      setCurrentWeekIndex(currentWeekIndex + 1);
    }
  };

  const handleNextWeek = () => {
    if (currentWeekIndex > 0) {
      setCurrentWeekIndex(currentWeekIndex - 1);
    }
  };

  useEffect(() => {
    fetchWeeklyNutrition();
  }, []);

  useEffect(() => {
    if (allWeeks.length) {
      const currentDate = new Date();
      // Find the current week
      const currentWeekIndex = allWeeks.findIndex((week) => {
        const weekStart = new Date(week.week_start);
        const weekEnd = new Date(week.week_end);
        return currentDate >= weekStart && currentDate <= weekEnd;
      });

      // If a week is found, set it as the current week
      if (currentWeekIndex !== -1) {
        setCurrentWeekIndex(currentWeekIndex);
      }
    }
  }, [allWeeks]);

  if (loading) {
    return (
      <View className="flex-1 justify-center items-center bg-white">
        <ActivityIndicator size="large" color="#F5A623" />
      </View>
    );
  }

  if (error) {
    return (
      <View className="flex-1 justify-center items-center bg-white p-4">
        <Text className="text-red-600 text-center mb-4">{error}</Text>
        <TouchableOpacity
          onPress={fetchWeeklyNutrition}
          className="bg-[#F5A623] px-6 py-3 rounded-lg"
        >
          <Text className="text-white font-medium">Try Again</Text>
        </TouchableOpacity>
      </View>
    );
  }

  if (!allWeeks.length) return null;

  const currentWeek = allWeeks[currentWeekIndex];

  return (
    <SafeAreaView className="flex-1 bg-white">
      <View className="flex-row justify-between items-center p-4 border-b border-gray-100">
        <Text className="text-xl font-semibold text-[#2D3748]">
          Weekly Nutrition
        </Text>
        <View className="flex-row items-center space-x-4">
          <TouchableOpacity
            className="p-2"
            onPress={handleNextWeek}
            disabled={currentWeekIndex <= 0}
          >
            <ArrowLeft
              stroke={currentWeekIndex <= 0 ? "#999" : "#666"}
              size={20}
            />
          </TouchableOpacity>
          <TouchableOpacity
            className="p-2"
            onPress={handlePrevWeek}
            disabled={currentWeekIndex >= allWeeks.length - 1}
          >
            <ArrowRight
              stroke={currentWeekIndex >= allWeeks.length - 1 ? "#999" : "#666"}
              size={20}
            />
          </TouchableOpacity>
        </View>
      </View>

      <ScrollView className="flex-1 p-4">
        <WeekSummary weekData={currentWeek} weekRange={currentWeek} />
        {currentWeek.days.map((dayData) => (
          <DayCard key={dayData.date} dayData={dayData} />
        ))}
      </ScrollView>
    </SafeAreaView>
  );
}
