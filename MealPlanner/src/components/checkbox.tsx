import { Pressable } from 'react-native'
import { Check } from 'lucide-react'

interface CheckboxProps {
  checked: boolean
  onPress: () => void
}

export function Checkbox({ checked, onPress }: CheckboxProps) {
  return (
    <Pressable
      onPress={onPress}
      className={`w-5 h-5 rounded border items-center justify-center ${
        checked ? 'bg-[#22C55E] border-[#22C55E]' : 'border-gray-300'
      }`}
    >
      {checked && <Check size={14} color="white" />}
    </Pressable>
  )
}

