import { View, Text } from 'react-native'
import Svg, { Path } from 'react-native-svg'

export function WaveHeader() {
  return (
    <View className="h-32">
      <View className="absolute top-0 w-full">
        <Svg height={120} width="100%" viewBox="0 0 375 120" preserveAspectRatio="none">
          <Path
            d="M0,0 L375,0 L375,80 C275,120 175,100 0,80 L0,0 Z"
            fill="#FDB347"
          />
        </Svg>
      </View>
      <Text className="text-center mt-12 text-gray-600">
        Monday 1 January 2024
      </Text>
    </View>
  )
}

