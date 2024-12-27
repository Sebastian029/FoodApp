import { useState } from 'react'
import { View, Text, Pressable } from 'react-native'
import { ChevronDown, ChevronUp } from 'lucide-react'

interface ExpandableSectionProps {
  title: string
  children: React.ReactNode
}

export function ExpandableSection({ title, children }: ExpandableSectionProps) {
  const [isExpanded, setIsExpanded] = useState(false)

  return (
    <View className="mb-4">
      <Pressable
        onPress={() => setIsExpanded(!isExpanded)}
        className="flex-row justify-between items-center py-2"
      >
        <Text className="text-gray-900 font-medium">{title}</Text>
        {isExpanded ? (
          <ChevronUp size={20} className="text-gray-400" />
        ) : (
          <ChevronDown size={20} className="text-gray-400" />
        )}
      </Pressable>
      {isExpanded && children}
    </View>
  )
}

