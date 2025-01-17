import React, { useState } from "react";
import {
  View,
  Text,
  ScrollView,
  TouchableOpacity,
  Alert,
  ActivityIndicator,
  TextInput,
  Modal,
  SafeAreaView,
} from "react-native";
import { Trash2, PlusCircle } from "react-native-feather";
import { useFocusEffect } from "@react-navigation/native";
import api from "../utils/api";
import { SelectList } from "react-native-dropdown-select-list";

export default function CartScreen() {
  const [cartItems, setCartItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedItem, setSelectedItem] = useState(null);
  const [quantityModalVisible, setQuantityModalVisible] = useState(false);
  const [newQuantity, setNewQuantity] = useState("");
  const [ingredientName, setIngredientName] = useState(""); 
  const [ingredientQuantity, setIngredientQuantity] = useState(""); 
  const [ingredientUnit, setIngredientUnit] = useState("pieces"); 
  const [addIngredientModalVisible, setAddIngredientModalVisible] =
    useState(false);
  const [selectedUnit, setSelectedUnit] = useState("");

  const fetchCart = async () => {
    try {
      setLoading(true);
      const response = await api.get("/cart/");
      setCartItems(response.data.cart_ingredients);
    } catch (error) {
      Alert.alert("Error", "Failed to fetch cart items");
    } finally {
      setLoading(false);
    }
  };

  useFocusEffect(
    React.useCallback(() => {
      fetchCart();
    }, [])
  );

  const handleRemoveAll = async () => {
    Alert.alert(
      "Remove All Items",
      "Are you sure you want to remove all items from your cart?",
      [
        { text: "Cancel", style: "cancel" },
        {
          text: "Remove All",
          style: "destructive",
          onPress: async () => {
            try {
              await api.delete("/cart/");
              setCartItems([]);
            } catch (error) {
              Alert.alert("Error", "Failed to remove items");
            }
          },
        },
      ]
    );
  };

  const handleRemoveItem = async (id) => {
    try {
      await api.delete(`/cart/${id}/`);
      setCartItems(cartItems.filter((item) => item.id !== id));
    } catch (error) {
      Alert.alert("Error", "Failed to remove item");
    }
  };

  const handleUpdateQuantity = async () => {
    if (!selectedItem || !newQuantity) return;

    try {
      await api.patch(`/cart/${selectedItem.id}/`, {
        quantity: parseFloat(newQuantity),
      });
      setCartItems(
        cartItems.map((item) =>
          item.id === selectedItem.id
            ? { ...item, quantity: parseFloat(newQuantity) }
            : item
        )
      );
      setQuantityModalVisible(false);
      setNewQuantity("");
      setSelectedItem(null);
    } catch (error) {
      Alert.alert("Error", "Failed to update quantity");
    }
  };

  const handleToggleBought = async (item) => {
    try {
      await api.patch(`/cart/${item.id}/`, {
        bought: !item.bought,
      });
      setCartItems(
        cartItems.map((cartItem) =>
          cartItem.id === item.id
            ? { ...cartItem, bought: !cartItem.bought }
            : cartItem
        )
      );
    } catch (error) {
      Alert.alert("Error", "Failed to update item status");
    }
  };

  const handleAddToCart = async () => {
    if (!ingredientName || !ingredientQuantity || !ingredientUnit) {
      Alert.alert("Error", "Please fill in all fields");
      return;
    }

    const newIngredient = {
      ingredient_name: ingredientName.toLowerCase(),
      quantity: parseFloat(ingredientQuantity),
      unit: selectedUnit,
    };

    try {
      setLoading(true);
      const response = await api.post("/cart/", {
        ingredients: [newIngredient],
      });
      fetchCart(); 
      setIngredientName(""); 
      setIngredientQuantity("");
      setIngredientUnit("pieces"); 
      setAddIngredientModalVisible(false); 
      Alert.alert("Success", "Ingredient added to cart");
    } catch (error) {
      Alert.alert("Error", "Failed to add ingredient to cart");
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <View className="flex-1 justify-center items-center bg-white">
        <ActivityIndicator size="large" color="#F5A623" />
      </View>
    );
  }

  return (
    <SafeAreaView className="flex-1 bg-white">
      {/* Header */}
      <View className="flex-row justify-between items-center px-4 py-3 border-b border-gray-100">
        <Text className="text-xl font-bold text-[#2D3748]">Your cart</Text>
        <TouchableOpacity
          onPress={handleRemoveAll}
          className="flex-row items-center"
        >
          <Text className="mr-2 text-gray-600">Remove all items</Text>
          <Trash2 size={20} stroke="#666" />
        </TouchableOpacity>
      </View>

      {/* Add Ingredient Button (Plus Icon) */}

      <TouchableOpacity
        onPress={() => {
          setAddIngredientModalVisible(true);
        }}
        style={{
          position: "absolute",
          bottom: 30,
          right: 30,
          backgroundColor: "#F5A623",
          padding: 15,
          borderRadius: 50,
          zIndex: 1000, // Ensure it stays on top
          elevation: 10, // For Android to raise above other components
        }}
      >
        <PlusCircle size={30} color="white" />
      </TouchableOpacity>

      {/* Cart Items */}
      <ScrollView className="flex-1 px-4">
        {cartItems.map((item) => (
          <View
            key={item.id}
            className="flex-row items-center py-4 border-b border-gray-100"
          >
            <TouchableOpacity
              onPress={() => handleToggleBought(item)}
              className={`w-6 h-6 rounded-full border-2 mr-3 items-center justify-center ${
                item.bought
                  ? "bg-[#F5A623] border-[#F5A623]"
                  : "border-gray-300"
              }`}
            >
              {item.bought && (
                <View className="w-3 h-3 bg-white rounded-full" />
              )}
            </TouchableOpacity>

            <TouchableOpacity
              onPress={() => {
                setSelectedItem(item);
                setNewQuantity(item.quantity.toString());
                setQuantityModalVisible(true);
              }}
              className="flex-1"
            >
              <Text className="text-lg text-[#2D3748]">
                {item.quantity} {item.unit}
              </Text>
              <Text className="text-gray-600">{item.ingredient_name}</Text>
            </TouchableOpacity>

            <TouchableOpacity
              onPress={() => handleRemoveItem(item.id)}
              className="p-2"
            >
              <Trash2 size={20} stroke="#666" />
            </TouchableOpacity>
          </View>
        ))}
      </ScrollView>

      {/* Add Ingredient Modal (Popup) */}
      <Modal
        animationType="slide"
        transparent={true}
        visible={addIngredientModalVisible}
        onRequestClose={() => {
          setAddIngredientModalVisible(false);
        }}
      >
        <View className="flex-1 justify-center items-center bg-black/50">
          <View className="bg-white w-[90%] rounded-2xl p-5 shadow-lg">
            <Text className="text-lg font-bold text-gray-800 mb-4 text-center">
              Add Ingredient
            </Text>

            <TextInput
              className="border border-gray-200 rounded-lg px-4 py-2 text-gray-800 mb-4"
              placeholder="Enter ingredient name"
              value={ingredientName}
              onChangeText={setIngredientName}
              placeholderTextColor="#A0AEC0"
            />

            <TextInput
              className="border border-gray-200 rounded-lg px-4 py-2 text-gray-800 mb-4"
              placeholder="Enter quantity"
              keyboardType="numeric"
              value={ingredientQuantity}
              onChangeText={setIngredientQuantity}
              placeholderTextColor="#A0AEC0"
            />

            <SelectList
              setSelected={setSelectedUnit}
              data={[
                { key: "1", value: "pieces" },
                { key: "2", value: "tablespoons" },
                { key: "3", value: "grams" },
                { key: "4", value: "cups" },
                { key: "5", value: "teaspoons" },
              ]}
              save="value"
              placeholder="Select unit"
              dropdownStyles={{ borderRadius: 8, borderColor: "#E2E8F0" }}
              boxStyles={{
                borderWidth: 1,
                borderColor: "#E2E8F0",
                borderRadius: 8,
                paddingVertical: 12,
                paddingHorizontal: 10,
              }}
            />

            <View className="flex-row justify-end mt-4">
              <TouchableOpacity
                onPress={() => setAddIngredientModalVisible(false)}
                className="px-4 py-2"
              >
                <Text className="text-gray-600">Cancel</Text>
              </TouchableOpacity>

              <TouchableOpacity
                onPress={handleAddToCart}
                className="bg-[#F5A623] px-4 py-2 rounded-lg ml-2"
              >
                <Text className="text-white font-medium">Add Ingredient</Text>
              </TouchableOpacity>
            </View>
          </View>
        </View>
      </Modal>

      {/* Quantity Update Modal */}
      <Modal
        animationType="slide"
        transparent={true}
        visible={quantityModalVisible}
        onRequestClose={() => setQuantityModalVisible(false)}
      >
        <View className="flex-1 justify-center items-center bg-black/50">
          <View className="bg-white w-80 rounded-xl p-4">
            <Text className="text-lg font-semibold mb-4">Update Quantity</Text>
            <TextInput
              className="border border-gray-200 rounded-lg px-4 py-2 mb-4"
              keyboardType="numeric"
              value={newQuantity}
              onChangeText={setNewQuantity}
              placeholder="Enter new quantity"
            />
            <View className="flex-row justify-end">
              <TouchableOpacity
                onPress={() => setQuantityModalVisible(false)}
                className="px-4 py-2"
              >
                <Text className="text-gray-600">Cancel</Text>
              </TouchableOpacity>
              <TouchableOpacity
                onPress={handleUpdateQuantity}
                className="bg-[#F5A623] px-4 py-2 rounded-lg ml-2"
              >
                <Text className="text-white font-medium">Update</Text>
              </TouchableOpacity>
            </View>
          </View>
        </View>
      </Modal>
    </SafeAreaView>
  );
}
