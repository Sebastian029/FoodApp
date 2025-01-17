import React, { useState, useEffect } from "react";
import {
  View,
  Text,
  TouchableOpacity,
  ScrollView,
  ActivityIndicator,
  SafeAreaView,
  TextInput,
  Alert,
} from "react-native";
import { ArrowLeft, Check, Search } from "react-native-feather";
import api from "../utils/api";

export default function BlockedIngredientsScreen({ navigation }) {
  const [ingredients, setIngredients] = useState([]);
  const [selectedIngredients, setSelectedIngredients] = useState(new Set());
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);
      const [ingredientsResponse, blockedResponse] = await Promise.all([
        api.get("/ingredients/"),
        api.get("/disliked-ingredients/"),
      ]);

      const blockedIds = new Set(blockedResponse.data.map((item) => item.id));

      setIngredients(ingredientsResponse.data);
      setSelectedIngredients(blockedIds);
    } catch (error) {
      Alert.alert("Error", "Failed to fetch ingredients");
    } finally {
      setLoading(false);
    }
  };

  const handleSave = async () => {
    try {
      setSaving(true);
      await api.post("/disliked-ingredients/", {
        ingredient_ids: Array.from(selectedIngredients),
      });
      navigation.goBack();
    } catch (error) {
      Alert.alert("Error", "Failed to save blocked ingredients");
    } finally {
      setSaving(false);
    }
  };

  const toggleIngredient = (id) => {
    setSelectedIngredients((prev) => {
      const newSet = new Set(prev);
      if (newSet.has(id)) {
        newSet.delete(id);
      } else {
        newSet.add(id);
      }
      return newSet;
    });
  };

  const filteredIngredients = ingredients.filter((ingredient) =>
    ingredient.name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  if (loading) {
    return (
      <View className="flex-1 justify-center items-center bg-white">
        <ActivityIndicator size="large" color="#F5A623" />
      </View>
    );
  }

  return (
    <SafeAreaView className="flex-1 bg-white">
      <View className="flex-row items-center justify-between p-4 border-b border-gray-100">
        <View className="flex-row items-center">
          <TouchableOpacity
            onPress={() => navigation.goBack()}
            className="p-2 -ml-2"
          >
            <ArrowLeft stroke="#2D3748" size={24} />
          </TouchableOpacity>
          <Text className="text-xl font-semibold text-[#2D3748] ml-2">
            Blocked Ingredients
          </Text>
        </View>
        <TouchableOpacity
          onPress={handleSave}
          disabled={saving}
          className="bg-[#2D3748] px-4 py-2 rounded-lg"
        >
          <Text className="text-white font-medium">
            {saving ? "Saving..." : "Save"}
          </Text>
        </TouchableOpacity>
      </View>

      <View className="p-4">
        <View className="flex-row items-center bg-gray-50 rounded-lg px-4 py-2 border border-gray-200">
          <Search stroke="#666" size={20} />
          <TextInput
            className="flex-1 ml-2 text-base text-gray-800"
            placeholder="Search ingredients..."
            value={searchQuery}
            onChangeText={setSearchQuery}
          />
        </View>
      </View>

      <ScrollView className="flex-1 px-4">
        {filteredIngredients.map((ingredient) => (
          <TouchableOpacity
            key={ingredient.id}
            onPress={() => toggleIngredient(ingredient.id)}
            className="flex-row items-center justify-between py-4 border-b border-gray-100"
          >
            <Text className="text-[#2D3748] text-lg">{ingredient.name}</Text>
            <View
              className={`w-6 h-6 rounded-full border-2 items-center justify-center
                ${
                  selectedIngredients.has(ingredient.id)
                    ? "bg-[#F5A623] border-[#F5A623]"
                    : "border-gray-300"
                }`}
            >
              {selectedIngredients.has(ingredient.id) && (
                <Check size={16} stroke="#fff" />
              )}
            </View>
          </TouchableOpacity>
        ))}
      </ScrollView>
    </SafeAreaView>
  );
}
