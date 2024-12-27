import { View, Text } from 'react-native'
import Svg, { Circle } from 'react-native-svg'

interface ProgressCircleProps {
  progress: number
  size: number
  strokeWidth: number
  value: string
  label: string
}

export function ProgressCircle({ progress, size, strokeWidth, value, label }: ProgressCircleProps) {
  const radius = (size - strokeWidth) / 2
  const circumference = radius * 2 * Math.PI
  const strokeDashoffset = circumference - (progress / 100) * circumference

  return (
    <View className="items-center">
      <View style={{ width: size, height: size }}>
        <Svg width={size} height={size}>
          <Circle
            stroke="#E5E7EB"
            fill="none"
            cx={size / 2}
            cy={size / 2}
            r={radius}
            strokeWidth={strokeWidth}
          />
          <Circle
            stroke="#3B82F6"
            fill="none"
            cx={size / 2}
            cy={size / 2}
            r={radius}
            strokeWidth={strokeWidth}
            strokeDasharray={`${circumference} ${circumference}`}
            strokeDashoffset={strokeDashoffset}
            strokeLinecap="round"
            transform={`rotate(-90 ${size / 2} ${size / 2})`}
          />
        </Svg>
        <View className="absolute inset-0 items-center justify-center">
          <Text className="text-xs font-medium">{value}</Text>
          <Text className="text-xs text-gray-500">{label}</Text>
        </View>
      </View>
    </View>
  )
}

