import { View, Text, Pressable } from 'react-native'
import { ArrowRight, Star } from 'lucide-react'
import { useNavigation } from '@react-navigation/native'

interface MealItemProps {
  title: string
  description: string
  rating?: number
  tags?: string[]
}

export function MealItem({ title, description, rating, tags }: MealItemProps) {
  const navigation = useNavigation()

  return (
    <Pressable
      className="bg-white rounded-lg p-4 mb-3 shadow-sm"
      onPress={() => navigation.navigate('RecipeDetail', { title })}
    >
      <View className="flex-row justify-between items-center">
        <View className="flex-1">
          <Text className="text-lg font-semibold">{title}</Text>
          <Text className="text-gray-500 text-sm mt-1">{description}</Text>
          
          {tags && (
            <View className="flex-row mt-2 gap-2">
              {tags.map((tag, index) => (
                <View
                  key={index}
                  className="px-2 py-1 rounded bg-gray-100"
                >
                  <Text className="text-xs text-gray-600">{tag}</Text>
                </View>
              ))}
            </View>
          )}
          
          {rating && (
            <View className="flex-row mt-2">
              {[...Array(5)].map((_, index) => (
                <Star
                  key={index}
                  size={16}
                  className={index < rating ? 'text-yellow-400' : 'text-gray-300'}
                  fill={index < rating ? '#FBBF24' : 'none'}
                />
              ))}
            </View>
          )}
        </View>
        <ArrowRight size={20} className="text-gray-400" />
      </View>
    </Pressable>
  )
}

