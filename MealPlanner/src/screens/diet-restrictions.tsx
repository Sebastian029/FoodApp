import { View, Text, ScrollView, Pressable, ActivityIndicator } from 'react-native'
import { RangeInput } from '../components/range-input'
import { ExpandableSection } from '../components/expandable-section'
import { useDietRestrictions, useUpdateDietRestrictions } from '../hooks/use-diet-restrictions-cached'

export function DietRestrictionsScreen() {
  const { data: restrictions, isLoading, error } = useDietRestrictions()
  const { mutate: updateRestrictions, isPending: isUpdating } = useUpdateDietRestrictions()

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
          Failed to load diet restrictions. Please try again.
        </Text>
      </View>
    )
  }

  const handleSave = () => {
    if (restrictions) {
      updateRestrictions(restrictions)
    }
  }

  return (
    <ScrollView className="flex-1 bg-white">
      <View className="bg-[#FDB347] h-32 rounded-b-3xl">
        <View className="mt-12 px-4">
          <Text className="text-xl font-semibold text-white">Diet restrictions</Text>
        </View>
      </View>
      
      <View className="px-4 py-6">
        <View className="bg-white rounded-xl p-4 shadow-sm">
          <RangeInput
            label="Calories"
            minValue={restrictions?.calories.min.toString()}
            maxValue={restrictions?.calories.max.toString()}
            onMinChange={(value) => {
              updateRestrictions({
                ...restrictions,
                calories: { ...restrictions.calories, min: parseInt(value) || 0 }
              })
            }}
            onMaxChange={(value) => {
              updateRestrictions({
                ...restrictions,
                calories: { ...restrictions.calories, max: parseInt(value) || 0 }
              })
            }}
          />

          <RangeInput
            label="Proteins"
            minValue={restrictions?.proteins.min.toString()}
            maxValue={restrictions?.proteins.max.toString()}
            onMinChange={(value) => {
              updateRestrictions({
                ...restrictions,
                proteins: { ...restrictions.proteins, min: parseInt(value) || 0 }
              })
            }}
            onMaxChange={(value) => {
              updateRestrictions({
                ...restrictions,
                proteins: { ...restrictions.proteins, max: parseInt(value) || 0 }
              })
            }}
          />

          <RangeInput
            label="Fiber"
            minValue={restrictions?.fiber.min.toString()}
            maxValue={restrictions?.fiber.max.toString()}
            onMinChange={(value) => {
              updateRestrictions({
                ...restrictions,
                fiber: { ...restrictions.fiber, min: parseInt(value) || 0 }
              })
            }}
            onMaxChange={(value) => {
              updateRestrictions({
                ...restrictions,
                fiber: { ...restrictions.fiber, max: parseInt(value) || 0 }
              })
            }}
          />

          <RangeInput
            label="Sugar"
            minValue={restrictions?.sugar.min.toString()}
            maxValue={restrictions?.sugar.max.toString()}
            onMinChange={(value) => {
              updateRestrictions({
                ...restrictions,
                sugar: { ...restrictions.sugar, min: parseInt(value) || 0 }
              })
            }}
            onMaxChange={(value) => {
              updateRestrictions({
                ...restrictions,
                sugar: { ...restrictions.sugar, max: parseInt(value) || 0 }
              })
            }}
          />

          <ExpandableSection title="Your diet type">
            <View className="mt-2">
              <Text className="text-gray-600">
                {restrictions?.dietType || 'No diet type selected'}
              </Text>
            </View>
          </ExpandableSection>

          <ExpandableSection title="Blocked ingredients">
            <View className="mt-2">
              {restrictions?.blockedIngredients.length ? (
                restrictions.blockedIngredients.map((ingredient, index) => (
                  <Text key={index} className="text-gray-600">
                    • {ingredient}
                  </Text>
                ))
              ) : (
                <Text className="text-gray-600">No blocked ingredients</Text>
              )}
            </View>
          </ExpandableSection>

          <Pressable 
            className={`bg-[#1B3358] py-3 rounded-lg mt-4 ${isUpdating ? 'opacity-50' : ''}`}
            onPress={handleSave}
            disabled={isUpdating}
          >
            {isUpdating ? (
              <ActivityIndicator color="white" />
            ) : (
              <Text className="text-white text-center font-medium">Save</Text>
            )}
          </Pressable>
        </View>
      </View>
    </ScrollView>
  )
}

