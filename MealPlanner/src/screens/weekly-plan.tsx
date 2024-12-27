import { View, Text, ScrollView, ActivityIndicator } from 'react-native'
import { useState } from 'react'
import { ProgressCircle } from '../components/progress-circle'
import { DateSelector } from '../components/date-selector'
import { MealItem } from '../components/meal-item'
import { useMealPlan } from '../hooks/use-meals-cached'
import { format } from 'date-fns'

export function WeeklyPlanScreen() {
  const [selectedDate, setSelectedDate] = useState(new Date())
  const { data: mealPlan, isLoading, error } = useMealPlan(
    format(selectedDate, 'yyyy-MM-dd')
  )

  if (isLoading) {
    return (
      <View className="flex-1 items-center justify-center">
        <ActivityIndicator size="large" color="#FDB347" />
      </View>
    )
  }

  if (error) {
    return (
      <View className="flex-1 items-center justify-center p-4">
        <Text className="text-red-500 text-center">
          Failed to load meal plan. Please try again.
        </Text>
      </View>
    )
  }

  const dailyNutrition = mealPlan?.meals.reduce(
    (acc, meal) => ({
      calories: acc.calories + meal.calories,
      proteins: acc.proteins + meal.protein,
      carbs: acc.carbs + meal.carbs,
      fat: acc.fat + meal.fat,
    }),
    { calories: 0, proteins: 0, carbs: 0, fat: 0 }
  )

  return (
    <View className="flex-1 bg-gray-50">
      <View className="bg-[#FDB347] h-32 rounded-b-3xl">
        <View className="mt-12 px-4">
          <Text className="text-white text-lg font-semibold">Week Total</Text>
        </View>
      </View>

      <View className="px-4 -mt-6">
        <View className="flex-row justify-between mb-6">
          <ProgressCircle
            progress={(dailyNutrition?.calories / 2000) * 100}
            size={60}
            strokeWidth={6}
            value={dailyNutrition?.calories.toString() ?? '0'}
            label="kcal"
          />
          <ProgressCircle
            progress={(dailyNutrition?.proteins / 50) * 100}
            size={60}
            strokeWidth={6}
            value={dailyNutrition?.proteins.toString() ?? '0'}
            label="protein"
          />
          <ProgressCircle
            progress={(dailyNutrition?.carbs / 300) * 100}
            size={60}
            strokeWidth={6}
            value={dailyNutrition?.carbs.toString() ?? '0'}
            label="carbs"
          />
          <ProgressCircle
            progress={(dailyNutrition?.fat / 65) * 100}
            size={60}
            strokeWidth={6}
            value={dailyNutrition?.fat.toString() ?? '0'}
            label="fat"
          />
        </View>

        <DateSelector
          selectedDate={selectedDate}
          onSelectDate={setSelectedDate}
        />

        <ScrollView className="mt-4">
          {mealPlan?.meals.map((meal, index) => (
            <View key={meal.id} className="mb-4">
              <Text className="text-lg font-semibold mb-2">
                {index === 0 ? 'Breakfast' : index === 1 ? 'Lunch' : 'Dinner'}
              </Text>
              <MealItem
                title={meal.name}
                description={meal.description}
                rating={meal.rating}
              />
            </View>
          ))}
        </ScrollView>
      </View>
    </View>
  )
}

