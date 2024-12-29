import React from "react";
import {
  View,
  Text,
  TouchableOpacity,
  Image,
  ScrollView,
  SafeAreaView,
} from "react-native";
import { format } from "date-fns";

const MEAL_TYPES = [
  {
    id: "breakfast",
    title: "Breakfast",
    image: require("../assets/breakfast.png"),
    description: "Start your day right",
  },
  {
    id: "lunch",
    title: "Lunch",
    image: require("../assets/lunch.png"),
    description: "Midday fuel",
  },
  {
    id: "dinner",
    title: "Dinner",
    image: require("../assets/dinner.png"),
    description: "Evening delight",
  },
  {
    id: "snack",
    title: "Snack",
    image: require("../assets/snack.png"),
    description: "Quick bites",
  },
];

export default function HomeScreen({ navigation }) {
  return (
    <SafeAreaView className="flex-1 bg-white">
      {/* Header with Date on top right */}
      <View className="relative">
        <View className="absolute top-0 right-4 mt-6">
          {/* Increased margin-top */}
          <Text className="text-gray-600">
            {format(new Date(), "EEEE d MMMM yyyy")}
          </Text>
        </View>
      </View>

      {/* Meal Type Cards */}
      <ScrollView
        className="flex-1 px-4 pt-4 mt-12" // Added margin-top here
        showsVerticalScrollIndicator={false}
      >
        {MEAL_TYPES.map((mealType) => (
          <TouchableOpacity
            key={mealType.id}
            onPress={() =>
              navigation.navigate("RecipeList", { type: mealType.id })
            }
            className="bg-white rounded-xl shadow-sm mb-4 overflow-hidden"
            style={{
              shadowColor: "#000",
              shadowOffset: { width: 0, height: 2 },
              shadowOpacity: 0.1,
              shadowRadius: 4,
              elevation: 3,
            }}
          >
            <Image
              source={mealType.image}
              className="w-full h-48"
              resizeMode="cover"
            />
            <View className="p-4">
              <Text className="text-xl font-bold text-[#2D3748] mb-1">
                {mealType.title}
              </Text>
              <Text className="text-gray-600">{mealType.description}</Text>
            </View>
          </TouchableOpacity>
        ))}
      </ScrollView>
    </SafeAreaView>
  );
}
