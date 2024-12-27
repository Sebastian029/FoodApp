import { View, ScrollView } from 'react-native'
import { WaveHeader } from '../components/wave-header'
import { SwipeableStatCard } from '../components/swipeable-stat-card'
import { ProgressCircle } from '../components/progress-circle'

export function HomeScreen() {
  return (
    <View className="flex-1 bg-gray-50">
      <WaveHeader />
      
      <ScrollView className="flex-1 px-4">
        <View className="flex-row justify-between mb-4">
          <View className="items-center">
            <ProgressCircle progress={60} size={80} strokeWidth={8} />
            <View className="items-center mt-2">
              <Text className="text-sm text-gray-600">1000</Text>
              <Text className="text-xs text-gray-500">kcal</Text>
            </View>
          </View>
          <View className="items-center">
            <ProgressCircle progress={40} size={80} strokeWidth={8} />
            <View className="items-center mt-2">
              <Text className="text-sm text-gray-600">1000</Text>
              <Text className="text-xs text-gray-500">steps</Text>
            </View>
          </View>
        </View>

        <SwipeableStatCard
          title="Rate recipes"
          value="4"
        />
        
        <SwipeableStatCard
          title="Update weight"
          value="100"
          subtitle="kg"
        />
      </ScrollView>
    </View>
  )
}

