import React, { useState } from "react";
import { View, Text, TouchableOpacity } from "react-native";
import { useAuth } from "../contexts/AuthContext";

export default function ProfileScreen() {
  const [loading, setLoading] = useState(false);
  const { logout } = useAuth();

  const handleLogout = async () => {
    try {
      setLoading(true);
      await logout();
    } catch (error) {
      Alert.alert("Error", "Failed to logout");
    } finally {
      setLoading(false);
    }
  };

  return (
    <View className="flex-1 justify-center items-center bg-white p-6">
      <Text className="text-2xl font-bold text-gray-800 mb-8">Profile</Text>
      <TouchableOpacity
        onPress={handleLogout}
        disabled={loading}
        className="bg-[#F5A623] px-6 py-3 rounded-full"
      >
        <Text className="text-white font-semibold">
          {loading ? "Logging out..." : "Logout"}
        </Text>
      </TouchableOpacity>
    </View>
  );
}
