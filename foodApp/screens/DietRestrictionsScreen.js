import React, { useState, useEffect } from "react";
import {
  View,
  Text,
  TouchableOpacity,
  TextInput,
  ScrollView,
  SafeAreaView,
  Alert,
} from "react-native";
import { ArrowLeft, HelpCircle, ChevronRight } from "react-native-feather";
import api from "../utils/api";

export default function DietRestrictionsScreen({ navigation }) {
  const [restrictions, setRestrictions] = useState({
    calories: { min: "", max: "" },
    proteins: { min: "", max: "" },
    sugar: { min: "", max: "" },
    iron: { min: "", max: "" },
    potassium: { min: "", max: "" },
  });
  const [loading, setLoading] = useState(false);

  const fetchDietRestrictions = async () => {
    try {
      setLoading(true);
      const response = await api.get("/preferences/");
      const data = response.data;
      setRestrictions({
        calories: {
          min: data.min_calories.toString(),
          max: data.max_calories.toString(),
        },
        proteins: {
          min: data.min_protein.toString(),
          max: data.max_protein.toString(),
        },
        sugar: {
          min: data.min_sugars.toString(),
          max: data.max_sugars.toString(),
        },
        iron: {
          min: data.min_iron.toString(),
          max: data.max_iron.toString(),
        },
        potassium: {
          min: data.min_potassium.toString(),
          max: data.max_potassium.toString(),
        },
      });
    } catch (error) {
      console.error("Error fetching diet restrictions:", error);
      Alert.alert("Error", "Failed to load diet restrictions.");
    } finally {
      setLoading(false);
    }
  };

  const handleSave = async () => {
    try {
      setLoading(true);
      await api.post("/preferences/", {
        min_calories: restrictions.calories.min,
        max_calories: restrictions.calories.max,
        min_protein: restrictions.proteins.min,
        max_protein: restrictions.proteins.max,
        min_sugars: restrictions.sugar.min,
        max_sugars: restrictions.sugar.max,
        min_iron: restrictions.iron.min,
        max_iron: restrictions.iron.max,
        min_potassium: restrictions.potassium.min,
        max_potassium: restrictions.potassium.max,
      });
      Alert.alert("Success", "Diet restrictions saved successfully.");
      navigation.goBack();
    } catch (error) {
      console.error("Error saving diet restrictions:", error);
      Alert.alert("Error", "Failed to save diet restrictions.");
    } finally {
      setLoading(false);
    }
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

  useEffect(() => {
    fetchDietRestrictions();
  }, []);

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
        {renderInput("Calories (kcal)", "calories")}
        {renderInput("Proteins (g)", "proteins")}
        {renderInput("Sugar (g)", "sugar")}
        {renderInput("Iron (mg)", "iron")}
        {renderInput("Potassium (mg)", "potassium")}

        {/* Diet Type Section */}
        <TouchableOpacity className="flex-row justify-between items-center p-4 bg-gray-50 rounded-lg mb-4">
          <Text className="text-[#2D3748]">Your diet type</Text>
          <ChevronRight stroke="#666" size={20} />
        </TouchableOpacity>

        {/* Blocked Ingredients Section */}
        <TouchableOpacity
          onPress={() => navigation.navigate("BlockedIngredients")}
          className="flex-row justify-between items-center p-4 bg-gray-50 rounded-lg mb-6"
        >
          <Text className="text-[#2D3748]">Blocked ingredients</Text>
          <ChevronRight stroke="#666" size={20} />
        </TouchableOpacity>

        {/* Save Button */}
        <TouchableOpacity
          onPress={handleSave}
          disabled={loading}
          className={`${
            loading ? "bg-gray-400" : "bg-[#2D3748]"
          } p-4 rounded-lg`}
        >
          <Text className="text-white text-center font-semibold">
            {loading ? "Saving..." : "Save"}
          </Text>
        </TouchableOpacity>
      </ScrollView>
    </SafeAreaView>
  );
}
