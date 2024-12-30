import React, { useState } from "react";
import {
  View,
  Text,
  TouchableOpacity,
  TextInput,
  ScrollView,
  SafeAreaView,
} from "react-native";
import { ArrowLeft, HelpCircle, ChevronRight } from "react-native-feather";

export default function DietRestrictionsScreen({ navigation }) {
  const [restrictions, setRestrictions] = useState({
    calories: { min: "", max: "" },
    proteins: { min: "", max: "" },
    fiber: { min: "", max: "" },
    sugar: { min: "", max: "" },
  });

  const handleSave = () => {
    // TODO: Implement save functionality
    navigation.goBack();
  };

  const renderInput = (label, field) => (
    <View className="mb-6">
      <View className="flex-row justify-between items-center mb-2">
        <Text className="text-[#2D3748]">{label}</Text>
        <TouchableOpacity>
          <HelpCircle size={20} stroke="#666" />
        </TouchableOpacity>
      </View>
      <View className="flex-row space-x-4">
        <View className="flex-1">
          <TextInput
            className="bg-gray-50 p-4 rounded-lg border border-gray-200"
            placeholder="Min"
            value={restrictions[field].min}
            onChangeText={(text) =>
              setRestrictions((prev) => ({
                ...prev,
                [field]: { ...prev[field], min: text },
              }))
            }
            keyboardType="numeric"
          />
        </View>
        <View className="flex-1">
          <TextInput
            className="bg-gray-50 p-4 rounded-lg border border-gray-200"
            placeholder="Max"
            value={restrictions[field].max}
            onChangeText={(text) =>
              setRestrictions((prev) => ({
                ...prev,
                [field]: { ...prev[field], max: text },
              }))
            }
            keyboardType="numeric"
          />
        </View>
      </View>
    </View>
  );

  return (
    <SafeAreaView className="flex-1 bg-white">
      {/* Header */}
      <View className="flex-row items-center p-4 border-b border-gray-100">
        <TouchableOpacity
          onPress={() => navigation.goBack()}
          className="p-2 -ml-2"
        >
          <ArrowLeft stroke="#2D3748" size={24} />
        </TouchableOpacity>
        <Text className="flex-1 text-xl font-semibold text-[#2D3748] text-center mr-10">
          Diet restrictions
        </Text>
      </View>

      <ScrollView className="flex-1 p-4">
        {renderInput("Calories", "calories")}
        {renderInput("Proteins", "proteins")}
        {renderInput("Fiber", "fiber")}
        {renderInput("Sugar", "sugar")}

        {/* Diet Type Section */}
        <TouchableOpacity className="flex-row justify-between items-center p-4 bg-gray-50 rounded-lg mb-4">
          <Text className="text-[#2D3748]">Your diet type</Text>
          <ChevronRight stroke="#666" size={20} />
        </TouchableOpacity>

        {/* Blocked Ingredients Section */}
        <TouchableOpacity className="flex-row justify-between items-center p-4 bg-gray-50 rounded-lg mb-6">
          <Text className="text-[#2D3748]">Blocked ingredients</Text>
          <ChevronRight stroke="#666" size={20} />
        </TouchableOpacity>

        {/* Save Button */}
        <TouchableOpacity
          onPress={handleSave}
          className="bg-[#2D3748] p-4 rounded-lg"
        >
          <Text className="text-white text-center font-semibold">Save</Text>
        </TouchableOpacity>
      </ScrollView>
    </SafeAreaView>
  );
}
