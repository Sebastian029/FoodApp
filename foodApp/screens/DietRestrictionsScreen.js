import React, { useState, useEffect } from "react";
import {
  View,
  Text,
  TouchableOpacity,
  TextInput,
  ScrollView,
  SafeAreaView,
  Alert,
  Modal,
  Pressable,
} from "react-native";
import { ArrowLeft, HelpCircle, ChevronRight } from "react-native-feather";
import { SelectList } from "react-native-dropdown-select-list";
import api from "../utils/api";

export default function DietRestrictionsScreen({ navigation }) {
  const [tooltipField, setTooltipField] = useState(null);
  const handleHelpPress = (field) => {
    setTooltipField(field);
  };

  const handleHelpRelease = () => {
    setTooltipField(null);
  };
  const [restrictions, setRestrictions] = useState({
    calories: { min: "", max: "" },
    proteins: { min: "", max: "" },
    sugar: { min: "", max: "" },
    iron: { min: "", max: "" },
    potassium: { min: "", max: "" },
    fat: { min: "", max: "" },
    carbohydrates: { min: "", max: "" },
    fiber: { min: "", max: "" },
  });
  const [loading, setLoading] = useState(false);
  const [dietTypes, setDietTypes] = useState([]);
  const [selectedDietType, setSelectedDietType] = useState("");
  const [modalVisible, setModalVisible] = useState(false);

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
        fat: {
          min: data.min_fat.toString(),
          max: data.max_fat.toString(),
        },
        carbohydrates: {
          min: data.min_carbohydrates.toString(),
          max: data.max_carbohydrates.toString(),
        },
        fiber: {
          min: data.min_fiber.toString(),
          max: data.max_fiber.toString(),
        },
      });
    } catch (error) {
      console.error("Error fetching diet restrictions:", error);
      Alert.alert("Error", "Failed to load diet restrictions.");
    } finally {
      setLoading(false);
    }
  };

  const fetchDietTypes = async () => {
    try {
      const response = await api.get("/diet-choices/");
      const dietChoices = response.data;
      setDietTypes(
        Object.entries(dietChoices).map(([key, value]) => ({
          key,
          value,
        }))
      );
    } catch (error) {
      console.error("Error fetching diet types:", error);
      Alert.alert("Error", "Failed to load diet types.");
    }
  };

  const fetchSelectedDietType = async () => {
    try {
      const response = await api.get("/diet-type/");
      setSelectedDietType(response.data.diet_type);
    } catch (error) {
      console.error("Error fetching selected diet type:", error);
      Alert.alert("Error", "Failed to load selected diet type.");
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
        min_fat: restrictions.fat.min,
        max_fat: restrictions.fat.max,
        min_carbohydrates: restrictions.carbohydrates.min,
        max_carbohydrates: restrictions.carbohydrates.max,
        min_fiber: restrictions.fiber.min,
        max_fiber: restrictions.fiber.max,
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

  const handleDietTypeChange = async (selected) => {
    try {
      setLoading(true);

      // Convert selected diet type to lowercase and replace spaces with underscores
      let validDietType = selected.toLowerCase().replace(/\s+/g, "_");

      const response = await api.put("/diet-type/", {
        diet_type: validDietType,
      });
      setSelectedDietType(selected);
      setModalVisible(false);
    } catch (error) {
      console.error(
        "Error saving diet type:",
        error.response?.data || error.message
      );
      Alert.alert(
        "Error",
        `Failed to save diet type: ${
          error.response?.data?.message || error.message
        }`
      );
    } finally {
      setLoading(false);
    }
  };

  const handleResetMealPlans = async () => {
    Alert.alert(
      "Reset Meal Plans",
      "Are you sure you want to reset all your planned meals? This action cannot be undone.",
      [
        {
          text: "Cancel",
          style: "cancel",
        },
        {
          text: "Reset",
          style: "destructive",
          onPress: async () => {
            try {
              setLoading(true);
              await api.delete("/reset-meal-plans/");
              Alert.alert(
                "Success",
                "Meal plans have been reset successfully."
              );
            } catch (error) {
              console.error("Error resetting meal plans:", error);
              Alert.alert("Error", "Failed to reset meal plans.");
            } finally {
              setLoading(false);
            }
          },
        },
      ]
    );
  };

  const renderInput = (label, field) => (
    <View className="mb-4">
      <View className="flex-row justify-between items-center mb-1">
        <Text className="text-[#2D3748]">{label}</Text>
        <TouchableOpacity
          onPressIn={() => handleHelpPress(field)}
          onPressOut={handleHelpRelease}
        >
          <HelpCircle size={20} stroke="#666" />
        </TouchableOpacity>
      </View>

      {tooltipField === field && (
        <View className="mt-2 p-3 bg-gradient-to-r from-blue-500 via-blue-600 to-blue-700 text-white rounded-xl shadow-lg">
          <Text className="text-sm font-semibold text-center">
            Set your {label} value. If set to 0, it will not be included in the
            meal planning calculations.
          </Text>
        </View>
      )}
      <View className="flex-row space-x-4">
        <View className="flex-1">
          <TextInput
            className="bg-gray-50 p-3 rounded-lg border border-gray-200"
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
            className="bg-gray-50 p-3 rounded-lg border border-gray-200"
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
    fetchDietTypes();
    fetchSelectedDietType();
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
        {renderInput("Fat (g)", "fat")}
        {renderInput("Carbohydrates (g)", "carbohydrates")}
        {renderInput("Fiber (g)", "fiber")}
        {renderInput("Sugar (g)", "sugar")}
        {renderInput("Iron (mg)", "iron")}
        {renderInput("Potassium (mg)", "potassium")}

        {/* Diet Type Section */}
        <TouchableOpacity
          onPress={() => setModalVisible(true)}
          className="flex-row justify-between items-center p-4 bg-gray-50 rounded-lg mb-4"
        >
          <Text className="text-[#2D3748]">{`Your diet type: ${selectedDietType}`}</Text>
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

        {/* Reset Meal Plans Button */}
        <TouchableOpacity
          onPress={handleResetMealPlans}
          disabled={loading}
          className="flex-row justify-between items-center p-4 bg-red-50 rounded-lg mb-6"
        >
          <Text className="text-red-600">Reset planned meals</Text>
          <ChevronRight stroke="#DC2626" size={20} />
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

      {/* Modal for selecting diet type */}
      <Modal
        visible={modalVisible}
        animationType="slide"
        transparent={true}
        onRequestClose={() => setModalVisible(false)}
      >
        <View className="flex-1 justify-center items-center bg-black/50">
          <View className="bg-white p-4 rounded-lg w-80">
            <Text className="text-xl mb-4">Select your diet type</Text>
            <SelectList
              setSelected={handleDietTypeChange}
              data={dietTypes}
              save="value"
              search={false}
              placeholder="Select Diet Type"
              defaultOption={selectedDietType}
            />
            <Pressable
              onPress={() => setModalVisible(false)}
              className="mt-4 p-4 bg-gray-300 rounded-lg"
            >
              <Text className="text-center">Close</Text>
            </Pressable>
          </View>
        </View>
      </Modal>
    </SafeAreaView>
  );
}
