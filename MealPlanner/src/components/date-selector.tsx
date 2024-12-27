import { View, Text, ScrollView, Pressable } from 'react-native'

interface DateSelectorProps {
  selectedDate: number
  onSelectDate: (date: number) => void
}

export function DateSelector({ selectedDate, onSelectDate }: DateSelectorProps) {
  const days = ['Monday 21', 'Tuesday 22', 'Wednesday 23']

  return (
    <View className="flex-row bg-gray-100 rounded-lg p-1">
      {days.map((day, index) => (
        <Pressable
          key={index}
          onPress={() => onSelectDate(index)}
          className={`flex-1 p-2 rounded-md ${
            selectedDate === index ? 'bg-white shadow' : ''
          }`}
        >
          <Text
            className={`text-center text-sm ${
              selectedDate === index ? 'text-gray-900' : 'text-gray-500'
            }`}
          >
            {day}
          </Text>
        </Pressable>
      ))}
    </View>
  )
}

