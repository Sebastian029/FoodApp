import { useState } from 'react'
import { View, Text, Pressable, ScrollView } from 'react-native'
import { Plus, Trash } from 'lucide-react'
import { CartItem } from '../components/cart-item'

interface CartItemType {
  id: string
  amount: string
  unit: string
  name: string
  checked: boolean
}

export function CartScreen() {
  const [items, setItems] = useState<CartItemType[]>([
    { id: '1', amount: '200g', unit: '', name: 'Chicken', checked: true },
    { id: '2', amount: '2', unit: 'p.', name: 'Garlic', checked: true },
    { id: '3', amount: '10', unit: 'ml', name: 'Olive oil', checked: true },
  ])

  const toggleItem = (id: string) => {
    setItems(items.map(item => 
      item.id === id ? { ...item, checked: !item.checked } : item
    ))
  }

  const removeItem = (id: string) => {
    setItems(items.filter(item => item.id !== id))
  }

  const removeAllItems = () => {
    setItems([])
  }

  return (
    <View className="flex-1 bg-white">
      <View className="bg-[#FDB347] h-32 rounded-b-3xl">
        <View className="flex-row justify-between items-center mt-12 px-4">
          <Text className="text-xl font-semibold text-white">Your cart</Text>
          <Pressable
            onPress={removeAllItems}
            className="flex-row items-center"
          >
            <Text className="text-white mr-2">Remove all items</Text>
            <Trash size={20} color="white" />
          </Pressable>
        </View>
      </View>

      <ScrollView className="flex-1 px-4 -mt-6">
        <View className="bg-white rounded-xl p-4 shadow-sm">
          {items.map(item => (
            <CartItem
              key={item.id}
              amount={item.amount}
              unit={item.unit}
              name={item.name}
              checked={item.checked}
              onToggle={() => toggleItem(item.id)}
              onRemove={() => removeItem(item.id)}
            />
          ))}
          <Pressable className="mt-2">
            <Plus size={24} className="text-[#22C55E]" />
          </Pressable>
        </View>
      </ScrollView>
    </View>
  )
}

