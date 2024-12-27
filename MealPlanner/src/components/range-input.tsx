import { View, Text, TextInput } from 'react-native'

interface RangeInputProps {
  label: string
  minValue: string
  maxValue: string
  onMinChange: (value: string) => void
  onMaxChange: (value: string) => void
}

export function RangeInput({ label, minValue, maxValue, onMinChange, onMaxChange }: RangeInputProps) {
  return (
    <View className="mb-4">
      <View className="flex-row justify-between items-center mb-2">
        <Text className="text-gray-900 font-medium">{label}</Text>
        <View className="flex-row items-center">
          <View className="w-16 h-10 bg-gray-100 rounded-lg mr-2">
            <TextInput
              className="flex-1 text-center"
              keyboardType="numeric"
              value={minValue}
              onChangeText={onMinChange}
              placeholder="Min"
            />
          </View>
          <View className="w-16 h-10 bg-gray-100 rounded-lg">
            <TextInput
              className="flex-1 text-center"
              keyboardType="numeric"
              value={maxValue}
              onChangeText={onMaxChange}
              placeholder="Max"
            />
          </View>
        </View>
      </View>
    </View>
  )
}

