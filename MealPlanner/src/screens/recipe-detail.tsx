import { View, Text, ScrollView, Pressable, ActivityIndicator } from 'react-native'
import { ArrowLeft, Maximize2, Plus } from 'lucide-react'
import { useNavigation, useRoute } from '@react-navigation/native'
import { useMeal } from '../hooks/use-meals-cached'

export function RecipeDetailScreen() {
  const navigation = useNavigation()
  const route = useRoute()
  const { mealId } = route.params as { mealId: string }
  
  const { data: meal, isLoading, error } = useMeal(mealId)

  if (isLoading) {
    return (
      <View className="flex-1 items-center justify-center">
        <ActivityIndicator size="large" color="#FDB347" />
      </View>
    )
  }

  if (error || !meal) {
    return (
      <View className="flex-1 items-center justify-center p-4">
        <Text className="text-red-500 text-center">
          Failed to load recipe details. Please try again.
        </Text>
      </View>
    )
  }

  return (
    <View className="flex-1 bg-gray-50">
      <View className="bg-[#FDB347] h-32 rounded-b-3xl">
        <View className="flex-row justify-between items-center mt-12 px-4">
          <Pressable onPress={() => navigation.goBack()}>
            <ArrowLeft size={24} color="white" />
          </Pressable>
          <Pressable>
            <Maximize2 size={24} color="white" />
          </Pressable>
        </View>
      </View>

      <ScrollView className="flex-1 px-4 -mt-6">
        <View className="bg-white rounded-xl p-6 shadow-sm">
          <Text className="text-2xl font-bold mb-2">{meal.name}</Text>
          <Text className="text-gray-600 leading-relaxed">
            {meal.description}
          </Text>

          <View className="mt-6">
            <Text className="text-xl font-semibold mb-4">Nutritions</Text>
            <View className="flex-row justify-between">
              <View className="items-center">
                <Text className="text-lg font-semibold">{meal.calories}</Text>
                <Text className="text-gray-500">kcal</Text>
              </View>
              <View className="items-center">
                <Text className="text-lg font-semibold">{meal.protein}g</Text>
                <Text className="text-gray-500">protein</Text>
              </View>
              <View className="items-center">
                <Text className="text-lg font-semibold">{meal.carbs}g</Text>
                <Text className="text-gray-500">carbs</Text>
              </View>
              <View className="items-center">
                <Text className="text-lg font-semibold">{meal.fat}g</Text>
                <Text className="text-gray-500">fat</Text>
              </View>
            </View>
          </View>

          <View className="mt-6">
            <Text className="text-xl font-semibold mb-4">Ingredients</Text>
            <View className="space-y-3">
              {meal.ingredients.map((ingredient, index) => (
                <View key={index} className="flex-row justify-between items-center">
                  <Text className="text-gray-600">{ingredient.name}</Text>
                  <View className="flex-row items-center">
                    <Text className="text-gray-600">
                      {ingredient.amount}{ingredient.unit}
                    </Text>
                    <Plus size={16} className="ml-2 text-blue-500" />
                  </View>
                </View>
              ))}
            </View>
          </View>

          <View className="mt-6">
            <Text className="text-xl font-semibold mb-4">Preparation</Text>
            <View className="space-y-2">
              {meal.preparation.map((step, index) => (
                <Text key={index} className="text-gray-600">
                  {index + 1}. {step}
                </Text>
              ))}
            </View>
          </View>
        </View>
      </ScrollView>
    </View>
  )
}

