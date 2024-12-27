import { View, Text, Pressable, ScrollView, ActivityIndicator } from 'react-native'
import { ArrowRight } from 'lucide-react'
import { useNavigation } from '@react-navigation/native'
import { LineGraph } from '../components/line-graph'
import { useWeightHistory } from '../hooks/use-diet-restrictions-cached'

export function SettingsScreen() {
  const navigation = useNavigation()
  const { data: weightHistory, isLoading, error } = useWeightHistory()
  
  const weightData = {
    labels: weightHistory?.map(entry => entry.date) ?? [],
    datasets: [
      {
        data: weightHistory?.map(entry => entry.weight) ?? [],
        color: (opacity = 1) => `rgba(59, 130, 246, ${opacity})`,
      }
    ],
  }

  return (
    <ScrollView className="flex-1 bg-white">
      <View className="bg-[#FDB347] h-32 rounded-b-3xl" />
      
      <View className="px-4 -mt-6">
        <View className="bg-white rounded-xl shadow-sm">
          <Pressable
            onPress={() => navigation.navigate('DietRestrictions')}
            className="flex-row justify-between items-center p-4 border-b border-gray-100"
          >
            <Text className="text-gray-900">Update diet restrictions</Text>
            <ArrowRight size={20} className="text-gray-400" />
          </Pressable>

          <Pressable
            className="flex-row justify-between items-center p-4"
          >
            <Text className="text-gray-900">Rate recent recipes</Text>
            <ArrowRight size={20} className="text-gray-400" />
          </Pressable>
        </View>

        <View className="mt-6">
          <Text className="text-xl font-semibold mb-4">Update weekly weight</Text>
          {isLoading ? (
            <ActivityIndicator size="large" color="#FDB347" />
          ) : error ? (
            <Text className="text-red-500">Failed to load weight history</Text>
          ) : (
            <LineGraph data={weightData} />
          )}
        </View>
      </View>
    </ScrollView>
  )
}

