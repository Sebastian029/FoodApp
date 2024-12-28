import React from 'react'
import { View, Text, TouchableOpacity, Alert } from 'react-native'
import { tokenManager } from '../utils/tokenManager'
import { authAPI } from '../utils/api'
import { useNavigation } from '@react-navigation/native'

export default function ProfileScreen() {
  const navigation = useNavigation()

  const handleLogout = async () => {
    try {
      await authAPI.logout()
      await tokenManager.removeToken()
      navigation.reset({
        index: 0,
        routes: [{ name: 'Auth' }]
      })
    } catch (error) {
      Alert.alert('Error', 'Failed to logout')
    }
  }

  return (
    <View className="flex-1 justify-center items-center bg-white p-6">
      <Text className="text-2xl font-bold text-gray-800 mb-8">Profile</Text>
      <TouchableOpacity 
        onPress={handleLogout}
        className="bg-[#F5A623] px-6 py-3 rounded-full"
      >
        <Text className="text-white font-semibold">Logout</Text>
      </TouchableOpacity>
    </View>
  )
}

