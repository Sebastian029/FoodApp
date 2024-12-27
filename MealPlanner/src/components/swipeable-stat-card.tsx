import { View, Text, Pressable } from 'react-native'
import { PanGestureHandler } from 'react-native-gesture-handler'
import Animated, {
  useAnimatedGestureHandler,
  useAnimatedStyle,
  useSharedValue,
  withSpring,
} from 'react-native-reanimated'
import { ArrowRight } from 'lucide-react'

interface StatCardProps {
  title: string
  value: string | number
  subtitle?: string
}

export function SwipeableStatCard({ title, value, subtitle }: StatCardProps) {
  const translateX = useSharedValue(0)

  const panGesture = useAnimatedGestureHandler({
    onActive: (event) => {
      translateX.value = event.translationX
    },
    onEnd: () => {
      translateX.value = withSpring(0)
    },
  })

  const rStyle = useAnimatedStyle(() => ({
    transform: [{ translateX: translateX.value }],
  }))

  return (
    <PanGestureHandler onGestureEvent={panGesture}>
      <Animated.View style={rStyle}>
        <Pressable className="bg-white rounded-xl p-4 flex-row items-center justify-between shadow-sm mb-2">
          <View>
            <Text className="text-gray-600 mb-1">{title}</Text>
            <View className="flex-row items-baseline">
              <Text className="text-2xl font-semibold">{value}</Text>
              {subtitle && (
                <Text className="text-gray-500 ml-1">{subtitle}</Text>
              )}
            </View>
          </View>
          <ArrowRight size={20} color="#666" />
        </Pressable>
      </Animated.View>
    </PanGestureHandler>
  )
}

