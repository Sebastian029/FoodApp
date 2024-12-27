import { View, Text, Pressable } from 'react-native'
import { Trash2 } from 'lucide-react'
import { Checkbox } from './checkbox'

interface CartItemProps {
  amount: string
  unit: string
  name: string
  checked: boolean
  onToggle: () => void
  onRemove: () => void
}

export function CartItem({ amount, unit, name, checked, onToggle, onRemove }: CartItemProps) {
  return (
    <View className="flex-row items-center py-3">
      <Checkbox checked={checked} onPress={onToggle} />
      <View className="flex-1 flex-row ml-3">
        <Text className="text-gray-900 font-medium">{amount}</Text>
        <Text className="text-gray-500 ml-1">{unit}</Text>
      </View>
      <Text className="flex-1 text-gray-900">{name}</Text>
      <Pressable onPress={onRemove} className="p-2">
        <Trash2 size={18} className="text-gray-400" />
      </Pressable>
    </View>
  )
}

