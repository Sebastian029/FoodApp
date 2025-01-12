import React, { useState, useEffect } from "react";
import { useFocusEffect } from "@react-navigation/native";
import {
  View,
  Text,
  ScrollView,
  TouchableOpacity,
  ActivityIndicator,
  SafeAreaView,
  Dimensions,
  Pressable,
  Animated,
  TextInput,
  Modal,
  Alert,
} from "react-native";
import { format, parseISO } from "date-fns";
import {
  ChevronRight,
  RotateCcw,
  Share,
  ChevronDown,
  ChevronUp,
  X,
  Plus,
  Trash2,
  Edit2,
} from "react-native-feather";
import api from "../utils/api";

const { width: SCREEN_WIDTH, height: SCREEN_HEIGHT } = Dimensions.get("window");

const MEAL_TYPES = ["breakfast", "lunch", "dinner", "snack"];

// Weekly Plan Components
const NutrientItem = ({ label, data, unit }) => {
  const range = data.max_7_days - data.min_7_days;
  const percentage = Math.min(
    Math.max(((data.total - data.min_7_days) / range) * 100, 0),
    100
  );
  const isGray = data.min_7_days === 0 && data.max_7_days === 0;

  return (
    <View className="mb-6">
      {/* Label and Total */}
      <View className="flex-row justify-between mb-2">
        <Text
          className={`text-base font-medium ${
            isGray ? "text-gray-400" : "text-gray-600"
          }`}
        >
          {label}
        </Text>
        <Text
          className={`text-base ${isGray ? "text-gray-400" : "text-gray-600"}`}
        >
          {data.total.toLocaleString()} {unit}
        </Text>
      </View>

      {/* Progress Bar */}
      <View className="h-3 bg-gray-100 rounded-full overflow-hidden">
        <View
          className={`h-full ${isGray ? "bg-gray-300" : "bg-[#F5A623]"}`}
          style={{ width: isGray ? "100%" : `${percentage}%` }}
        />
      </View>

      {/* Min and Max */}
      <View className="flex-row justify-between mt-2">
        <Text
          className={`text-sm ${isGray ? "text-gray-400" : "text-gray-500"}`}
        >
          Min: {data.min_7_days.toLocaleString()} {unit}
        </Text>
        <Text
          className={`text-sm ${isGray ? "text-gray-400" : "text-gray-500"}`}
        >
          Max: {data.max_7_days.toLocaleString()} {unit}
        </Text>
      </View>
    </View>
  );
};

const MealItem = ({ recipe, onPress }) => (
  <TouchableOpacity
    onPress={onPress}
    className="flex-row items-center justify-between bg-white rounded-lg p-4 mb-3"
  >
    <View className="flex-1">
      <Text className="text-lg font-semibold text-[#2D3748]">
        {recipe.title}
      </Text>
      <Text className="text-gray-600 text-sm">
        {recipe.description || "Juicy grilled chicken breast with seasoning."}
      </Text>
    </View>
    <View className="flex-row items-center">
      <ChevronRight size={20} stroke="#666" />
    </View>
  </TouchableOpacity>
);

// Daily Plan Components
const NutrientRow = ({ label, value, unit }) => (
  <View className="flex-row justify-between py-1">
    <Text className="text-gray-600">{label}</Text>
    <Text className="font-medium">
      {value} {unit}
    </Text>
  </View>
);

const AddItemModal = ({ visible, onClose, onSubmit }) => {
  const [itemName, setItemName] = useState("");
  const [calories, setCalories] = useState("");
  const [protein, setProtein] = useState("");
  const [fats, setFats] = useState("");
  const [carbs, setCarbs] = useState("");
  const [sugars, setSugars] = useState("");
  const [iron, setIron] = useState("");
  const [potassium, setPotassium] = useState("");

  const handleSubmit = () => {
    if (!itemName || !calories) {
      Alert.alert("Error", "Item name and calories are required");
      return;
    }

    onSubmit({
      item_name: itemName,
      total_calories: parseFloat(calories),
      total_protein: parseFloat(protein) || 0,
      total_fats: parseFloat(fats) || 0,
      total_carbs: parseFloat(carbs) || 0,
      total_sugars: parseFloat(sugars) || 0,
      total_iron: parseFloat(iron) || 0,
      total_potassium: parseFloat(potassium) || 0,
    });

    // Reset form
    setItemName("");
    setCalories("");
    setProtein("");
    setFats("");
    setCarbs("");
    setSugars("");
    setIron("");
    setPotassium("");
  };

  return (
    <Modal
      visible={visible}
      animationType="slide"
      transparent={true}
      onRequestClose={onClose}
    >
      <View className="flex-1 justify-end">
        <View className="bg-white rounded-t-3xl p-6 h-[70%]">
          <View className="flex-row justify-between items-center mb-6">
            <Text className="text-xl font-semibold text-[#2D3748]">
              Add New Item
            </Text>
            <TouchableOpacity onPress={onClose}>
              <X size={24} stroke="#666" />
            </TouchableOpacity>
          </View>

          <ScrollView
            className="flex-1"
            keyboardShouldPersistTaps="handled"
            keyboardDismissMode="on-drag"
          >
            <View className="space-y-4">
              <View>
                <Text className="text-gray-600 mb-1">Item Name *</Text>
                <TextInput
                  className="bg-gray-50 p-4 rounded-lg border border-gray-200"
                  value={itemName}
                  onChangeText={setItemName}
                  placeholder="Enter item name"
                />
              </View>

              <View>
                <Text className="text-gray-600 mb-1">Calories (kcal) *</Text>
                <TextInput
                  className="bg-gray-50 p-4 rounded-lg border border-gray-200"
                  value={calories}
                  onChangeText={setCalories}
                  keyboardType="numeric"
                  placeholder="Enter calories"
                />
              </View>

              <View>
                <Text className="text-gray-600 mb-1">Protein (g)</Text>
                <TextInput
                  className="bg-gray-50 p-4 rounded-lg border border-gray-200"
                  value={protein}
                  onChangeText={setProtein}
                  keyboardType="numeric"
                  placeholder="Enter protein"
                />
              </View>

              <View>
                <Text className="text-gray-600 mb-1">Fats (g)</Text>
                <TextInput
                  className="bg-gray-50 p-4 rounded-lg border border-gray-200"
                  value={fats}
                  onChangeText={setFats}
                  keyboardType="numeric"
                  placeholder="Enter fats"
                />
              </View>

              <View>
                <Text className="text-gray-600 mb-1">Carbs (g)</Text>
                <TextInput
                  className="bg-gray-50 p-4 rounded-lg border border-gray-200"
                  value={carbs}
                  onChangeText={setCarbs}
                  keyboardType="numeric"
                  placeholder="Enter carbs"
                />
              </View>

              <View>
                <Text className="text-gray-600 mb-1">Sugars (g)</Text>
                <TextInput
                  className="bg-gray-50 p-4 rounded-lg border border-gray-200"
                  value={sugars}
                  onChangeText={setSugars}
                  keyboardType="numeric"
                  placeholder="Enter sugars"
                />
              </View>

              <View>
                <Text className="text-gray-600 mb-1">Iron (mg)</Text>
                <TextInput
                  className="bg-gray-50 p-4 rounded-lg border border-gray-200"
                  value={iron}
                  onChangeText={setIron}
                  keyboardType="numeric"
                  placeholder="Enter iron"
                />
              </View>

              <View>
                <Text className="text-gray-600 mb-1">Potassium (mg)</Text>
                <TextInput
                  className="bg-gray-50 p-4 rounded-lg border border-gray-200"
                  value={potassium}
                  onChangeText={setPotassium}
                  keyboardType="numeric"
                  placeholder="Enter potassium"
                />
              </View>
            </View>
          </ScrollView>

          <TouchableOpacity
            onPress={handleSubmit}
            className="bg-[#F5A623] p-4 rounded-lg mt-4"
          >
            <Text className="text-white text-center font-semibold">
              Add Item
            </Text>
          </TouchableOpacity>
        </View>
      </View>
    </Modal>
  );
};

const EditQuantityModal = ({ visible, onClose, onSubmit, currentQuantity }) => {
  const [quantity, setQuantity] = useState(currentQuantity.toString());

  const handleSubmit = () => {
    const newQuantity = parseInt(quantity);
    if (isNaN(newQuantity) || newQuantity < 1) {
      Alert.alert("Error", "Please enter a valid quantity");
      return;
    }
    onSubmit(newQuantity);
    onClose();
  };

  return (
    <Modal
      visible={visible}
      animationType="slide"
      transparent={true}
      onRequestClose={onClose}
    >
      <View className="flex-1 justify-center items-center bg-black/50">
        <View className="bg-white w-80 rounded-xl p-4">
          <Text className="text-lg font-semibold mb-4">Update Quantity</Text>
          <TextInput
            className="bg-gray-50 p-4 rounded-lg border border-gray-200 mb-4"
            value={quantity}
            onChangeText={setQuantity}
            keyboardType="numeric"
            placeholder="Enter quantity"
          />
          <View className="flex-row justify-end gap-4">
            <TouchableOpacity onPress={onClose}>
              <Text className="text-gray-600">Cancel</Text>
            </TouchableOpacity>
            <TouchableOpacity onPress={handleSubmit}>
              <Text className="text-[#F5A623] font-medium">Update</Text>
            </TouchableOpacity>
          </View>
        </View>
      </View>
    </Modal>
  );
};

export default function PlannerScreen({ navigation }) {
  // Weekly Plan State
  const [weeklyPlan, setWeeklyPlan] = useState([]);
  const [selectedDate, setSelectedDate] = useState(null);
  const [loading, setLoading] = useState(true);
  const [nutrientData, setNutrientData] = useState(null);
  const [loadingNutrients, setLoadingNutrients] = useState(true);
  const [isNutrientSummaryExpanded, setIsNutrientSummaryExpanded] =
    useState(false);
  const [summaryAnimation] = useState(new Animated.Value(0));

  // Daily Plan State
  const [dailyItems, setDailyItems] = useState({});
  const [showAddModal, setShowAddModal] = useState(false);
  const [showEditModal, setShowEditModal] = useState(false);
  const [selectedItem, setSelectedItem] = useState(null);
  const [activeTab, setActiveTab] = useState("weekly"); // 'weekly' or 'daily'
  const today = format(new Date(), "yyyy-MM-dd");
  const todayISO = new Date().toISOString().split("T")[0];

  // Fetch Data
  const fetchWeeklyPlan = async () => {
    try {
      setLoading(true);
      setWeeklyPlan([]); // Reset state before fetching
      setSelectedDate(null);
      const response = await api.post("/weekly-meal-plan/");
      setWeeklyPlan(response.data.weekly_plan);
      setSelectedDate(response.data.weekly_plan[0]?.date);
    } catch (error) {
      console.error("Error fetching weekly plan:", error);
    } finally {
      setLoading(false);
    }
  };

  const fetchNutrientData = async () => {
    try {
      setLoadingNutrients(true);
      const response = await api.get("/nutrient-summary/");
      setNutrientData(response.data);
    } catch (error) {
      console.error("Error fetching nutrient data:", error);
    } finally {
      setLoadingNutrients(false);
    }
  };

  const fetchDailyItems = async () => {
    try {
      const response = await api.get("/day-plan-items/");
      setDailyItems(response.data.items_by_date);
    } catch (error) {
      console.error("Error fetching items:", error);
      Alert.alert("Error", "Failed to load items");
    }
  };

  useFocusEffect(
    React.useCallback(() => {
      fetchWeeklyPlan();
      fetchNutrientData();
      fetchDailyItems();
    }, [])
  );

  // Weekly Plan Functions
  const toggleNutrientSummary = () => {
    const toValue = isNutrientSummaryExpanded ? 0 : 1;
    setIsNutrientSummaryExpanded(!isNutrientSummaryExpanded);
    Animated.spring(summaryAnimation, {
      toValue,
      useNativeDriver: true,
      tension: 20,
      friction: 7,
    }).start();
  };

  const selectedDayPlan = weeklyPlan.find((day) => day.date === selectedDate);

  const getRecipesByType = (type) => {
    return (
      selectedDayPlan?.recipes.filter((recipe) => recipe.meal_type === type) ||
      []
    );
  };

  // Daily Plan Functions
  const handleAddItem = async (itemData) => {
    try {
      await api.post("/day-plan-items/", {
        date: todayISO,
        items: [itemData],
      });
      console.log(todayISO);
      setShowAddModal(false);
      fetchDailyItems();
    } catch (error) {
      console.error("Error adding item:", error);
      Alert.alert("Error", "Failed to add item");
    }
  };

  const handleDeleteItem = async (itemId) => {
    Alert.alert("Delete Item", "Are you sure you want to delete this item?", [
      { text: "Cancel", style: "cancel" },
      {
        text: "Delete",
        style: "destructive",
        onPress: async () => {
          try {
            await api.delete(`/day-plan-items/${itemId}/`);
            fetchDailyItems();
          } catch (error) {
            console.error("Error deleting item:", error);
            Alert.alert("Error", "Failed to delete item");
          }
        },
      },
    ]);
  };

  const handleUpdateQuantity = async (quantity) => {
    try {
      await api.patch(`/day-plan-items/${selectedItem.id}/`, {
        quantity,
      });
      fetchDailyItems();
      setShowEditModal(false);
      setSelectedItem(null);
    } catch (error) {
      console.error("Error updating quantity:", error);
      Alert.alert("Error", "Failed to update quantity");
    }
  };

  if (loading) {
    return (
      <View className="flex-1 justify-center items-center bg-white">
        <ActivityIndicator size="large" color="#F5A623" />
      </View>
    );
  }

  const renderWeeklyPlan = () => (
    <>
      <ScrollView className="flex-1">
        {/* Nutrient Summary Section */}
        <View className="px-4 pt-4">
          <View className={`bg-white rounded-lg shadow-sm`}>
            <TouchableOpacity
              onPress={toggleNutrientSummary}
              className="flex-row justify-between items-center p-4"
            >
              <Text className="text-lg font-semibold text-[#2D3748]">
                Weekly Nutrient Summary
              </Text>
              <View className="flex-row items-center">
                {isNutrientSummaryExpanded ? (
                  <ChevronUp size={20} stroke="#666" />
                ) : (
                  <ChevronDown size={20} stroke="#666" />
                )}
              </View>
            </TouchableOpacity>

            <Animated.View
              style={{
                opacity: summaryAnimation,
                transform: [
                  {
                    translateY: summaryAnimation.interpolate({
                      inputRange: [0, 1],
                      outputRange: [-20, 0],
                    }),
                  },
                ],
              }}
              className="px-2 pb-2"
            >
              {isNutrientSummaryExpanded && nutrientData && (
                <>
                  <NutrientItem
                    label="Calories"
                    data={nutrientData.comparisons.total_calories}
                    unit="kcal"
                  />
                  <NutrientItem
                    label="Sugars"
                    data={nutrientData.comparisons.sugars}
                    unit="g"
                  />
                  <NutrientItem
                    label="Protein"
                    data={nutrientData.comparisons.protein}
                    unit="g"
                  />
                  <NutrientItem
                    label="Fat"
                    data={nutrientData.comparisons.fat}
                    unit="g"
                  />
                  <NutrientItem
                    label="Carbohydrates"
                    data={nutrientData.comparisons.carbohydrates}
                    unit="g"
                  />
                  <NutrientItem
                    label="Fiber"
                    data={nutrientData.comparisons.fiber}
                    unit="g"
                  />
                  <NutrientItem
                    label="Iron"
                    data={nutrientData.comparisons.iron}
                    unit="mg"
                  />
                  <NutrientItem
                    label="Potassium"
                    data={nutrientData.comparisons.potassium}
                    unit="mg"
                  />
                </>
              )}
            </Animated.View>
          </View>
        </View>

        <View className="px-4 py-2 border-t border-b border-gray-100 mt-4">
          <ScrollView horizontal showsHorizontalScrollIndicator={false}>
            {weeklyPlan.map((day) => (
              <TouchableOpacity
                key={day.date}
                onPress={() => setSelectedDate(day.date)}
                className={`w-32 h-10 rounded-lg flex items-center justify-center mr-2 ${
                  selectedDate === day.date ? "bg-[#475569]" : "bg-gray-100"
                }`}
              >
                <Text
                  className={`${
                    selectedDate === day.date
                      ? "text-white font-medium"
                      : "text-gray-600"
                  } text-sm`}
                >
                  {format(parseISO(day.date), "EEEE d")}
                </Text>
              </TouchableOpacity>
            ))}
          </ScrollView>
        </View>

        {/* Meal List */}
        <View className="flex-1 px-4 pt-4">
          {MEAL_TYPES.map((type) => {
            const recipes = getRecipesByType(type);
            if (recipes.length === 0) return null;

            return (
              <View key={type} className="mb-4">
                <Text className="text-[#2D3748] font-semibold text-lg capitalize mb-2">
                  {type}
                </Text>
                {recipes.map((recipe) => (
                  <MealItem
                    key={recipe.id}
                    recipe={recipe}
                    onPress={() =>
                      navigation.navigate("RecipeDetail", {
                        recipeId: recipe.id,
                        fromPlanner: true,
                      })
                    }
                  />
                ))}
              </View>
            );
          })}
        </View>
      </ScrollView>
    </>
  );

  const renderDailyPlan = () => (
    <>
      <ScrollView className="flex-1 p-4">
        {Object.entries(dailyItems)
          .filter(([date]) => date === todayISO)
          .map(([date, dayItems]) => (
            <View key={date} className="mb-6">
              <Text className="text-lg font-semibold text-[#2D3748] mb-4">
                Today's Items
              </Text>

              {dayItems.map((item) => (
                <View
                  key={item.id}
                  className="bg-white rounded-xl shadow-sm p-4 mb-4"
                >
                  <View className="flex-row justify-between items-start mb-2">
                    <View className="flex-1">
                      <Text className="text-lg font-medium text-[#2D3748]">
                        {item.item_name}
                      </Text>
                      <Text className="text-sm text-gray-500">
                        Quantity: {item.quantity}
                      </Text>
                    </View>
                    <View className="flex-row gap-2">
                      <TouchableOpacity
                        onPress={() => {
                          setSelectedItem(item);
                          setShowEditModal(true);
                        }}
                        className="p-2"
                      >
                        <Edit2 size={20} stroke="#666" />
                      </TouchableOpacity>
                      <TouchableOpacity
                        onPress={() => handleDeleteItem(item.id)}
                        className="p-2"
                      >
                        <Trash2 size={20} stroke="#666" />
                      </TouchableOpacity>
                    </View>
                  </View>

                  <View className="border-t border-gray-100 pt-2 mt-2">
                    <NutrientRow
                      label="Calories"
                      value={item.total_calories * item.quantity}
                      unit="kcal"
                    />
                    <NutrientRow
                      label="Protein"
                      value={item.total_protein * item.quantity}
                      unit="g"
                    />
                    <NutrientRow
                      label="Fats"
                      value={item.total_fats * item.quantity}
                      unit="g"
                    />
                    <NutrientRow
                      label="Carbs"
                      value={item.total_carbs * item.quantity}
                      unit="g"
                    />
                    <NutrientRow
                      label="Sugars"
                      value={item.total_sugars * item.quantity}
                      unit="g"
                    />
                    <NutrientRow
                      label="Iron"
                      value={item.total_iron * item.quantity}
                      unit="mg"
                    />
                    <NutrientRow
                      label="Potassium"
                      value={item.total_potassium * item.quantity}
                      unit="mg"
                    />
                  </View>
                </View>
              ))}
            </View>
          ))}
      </ScrollView>

      <AddItemModal
        visible={showAddModal}
        onClose={() => setShowAddModal(false)}
        onSubmit={handleAddItem}
      />

      <EditQuantityModal
        visible={showEditModal}
        onClose={() => {
          setShowEditModal(false);
          setSelectedItem(null);
        }}
        onSubmit={handleUpdateQuantity}
        currentQuantity={selectedItem?.quantity || 1}
      />
    </>
  );

  return (
    <SafeAreaView className="flex-1 bg-white">
      <View className="flex-1">
        {/* Header with Tabs */}
        <View className="border-b border-gray-100">
          <View className="flex-row justify-between items-center p-4">
            <Text className="text-xl font-semibold text-[#2D3748]">
              Meal Planner
            </Text>
            {activeTab === "daily" && (
              <TouchableOpacity
                onPress={() => setShowAddModal(true)}
                className="bg-[#F5A623] p-2 rounded-lg"
              >
                <Plus size={24} stroke="#fff" />
              </TouchableOpacity>
            )}
          </View>
          <View className="flex-row px-4 pb-2">
            <TouchableOpacity
              onPress={() => setActiveTab("weekly")}
              className={`mr-4 pb-2 ${
                activeTab === "weekly" ? "border-b-2 border-[#F5A623]" : ""
              }`}
            >
              <Text
                className={`text-base ${
                  activeTab === "weekly"
                    ? "text-[#F5A623] font-medium"
                    : "text-gray-600"
                }`}
              >
                Weekly Plan
              </Text>
            </TouchableOpacity>
            <TouchableOpacity
              onPress={() => setActiveTab("daily")}
              className={`mr-4 pb-2 ${
                activeTab === "daily" ? "border-b-2 border-[#F5A623]" : ""
              }`}
            >
              <Text
                className={`text-base ${
                  activeTab === "daily"
                    ? "text-[#F5A623] font-medium"
                    : "text-gray-600"
                }`}
              >
                Daily Items
              </Text>
            </TouchableOpacity>
          </View>
        </View>

        {/* Content */}
        {activeTab === "weekly" ? renderWeeklyPlan() : renderDailyPlan()}
      </View>
    </SafeAreaView>
  );
}
