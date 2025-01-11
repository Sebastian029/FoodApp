import React, { useState, useEffect } from "react";
import {
  View,
  Text,
  TouchableOpacity,
  TextInput,
  Alert,
  ScrollView,
  ActivityIndicator,
  SafeAreaView,
  Dimensions,
} from "react-native";
import { ChevronRight, LogOut } from "react-native-feather";
import { format } from "date-fns";
import { LineChart } from "react-native-chart-kit";
import api from "../utils/api";
import { useAuth } from "../contexts/AuthContext";

const screenWidth = Dimensions.get("window").width;

export default function UserPreferencesScreen({ navigation }) {
  const [weight, setWeight] = useState("");
  const [canUpdateWeight, setCanUpdateWeight] = useState(false);
  const [weightHistory, setWeightHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [loggingOut, setLoggingOut] = useState(false);
  const { logout } = useAuth();

  const checkCanUpdateWeight = async () => {
    try {
      const response = await api.get("/can-update-weight/");
      setCanUpdateWeight(response.data.can_update);
    } catch (error) {
      console.error("Error checking weight update status:", error);
    }
  };

  const fetchWeightHistory = async () => {
    try {
      const response = await api.get("/weights/");
      setWeightHistory(response.data);
    } catch (error) {
      console.error("Error fetching weight history:", error);
    }
  };

  useEffect(() => {
    Promise.all([checkCanUpdateWeight(), fetchWeightHistory()]).finally(() =>
      setLoading(false)
    );
  }, []);

  const handleUpdateWeight = async () => {
    if (!weight) {
      Alert.alert("Error", "Please enter your weight");
      return;
    }

    try {
      const today = format(new Date(), "yyyy-MM-dd");
      await api.post("/update-weight/", {
        weight,
        date: today,
      });
      Alert.alert("Success", "Weight updated successfully");
      setWeight("");
      checkCanUpdateWeight();
      fetchWeightHistory();
    } catch (error) {
      Alert.alert("Error", "Failed to update weight");
    }
  };

  const handleLogout = async () => {
    Alert.alert("Logout", "Are you sure you want to logout?", [
      {
        text: "Cancel",
        style: "cancel",
      },
      {
        text: "Logout",
        style: "destructive",
        onPress: async () => {
          try {
            setLoggingOut(true);
            await logout();
          } catch (error) {
            Alert.alert("Error", "Failed to logout");
          } finally {
            setLoggingOut(false);
          }
        },
      },
    ]);
  };

  const chartConfig = {
    backgroundGradientFrom: "#ffffff",
    backgroundGradientTo: "#ffffff",
    color: (opacity = 1) => `rgba(245, 166, 35, ${opacity})`,
    strokeWidth: 2,
    barPercentage: 0.5,
    useShadowColorFromDataset: false,
    propsForDots: {
      r: "6",
      strokeWidth: "2",
      stroke: "#F5A623",
    },
    propsForLabels: {
      fontSize: 12,
    },
  };

  const chartData = {
    labels: weightHistory.map((entry) => format(new Date(entry.date), "MMM d")),
    datasets: [
      {
        data: weightHistory.map((entry) => parseFloat(entry.weight)),
        color: (opacity = 1) => `rgba(245, 166, 35, ${opacity})`,
        strokeWidth: 2,
      },
    ],
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
      <View className="flex-1">
        <ScrollView className="flex-1 px-4">
          {/* Navigation Buttons */}
          <View className="py-4">
            <TouchableOpacity
              onPress={() => navigation.navigate("DietRestrictions")}
              className="flex-row justify-between items-center bg-white p-4 rounded-xl shadow-sm"
            >
              <Text className="text-lg text-[#2D3748]">
                Update diet restrictions
              </Text>
              <ChevronRight stroke="#666" size={20} />
            </TouchableOpacity>
            <View className="h-4" />
            <TouchableOpacity
              className="flex-row justify-between items-center bg-white p-4 rounded-xl shadow-sm"
              onPress={() => navigation.navigate("WeeklyNutrition")}
            >
              <Text className="text-lg text-[#2D3748]">
                Get Weekly Nutrition Information
              </Text>
              <ChevronRight stroke="#666" size={20} />
            </TouchableOpacity>
          </View>

          {/* Weight Update Section */}
          <View className="bg-white p-4 rounded-xl shadow-sm mb-6">
            <Text className="text-xl font-semibold text-[#2D3748] mb-4">
              Update weekly weight
            </Text>
            <View className="space-y-4">
              <View>
                <Text className="text-gray-600 mb-2">Weight</Text>
                <TextInput
                  className={`bg-gray-50 p-4 rounded-lg border ${
                    canUpdateWeight
                      ? "border-gray-200"
                      : "border-gray-100 bg-gray-100"
                  }`}
                  placeholder="Enter weight in kg"
                  value={weight}
                  onChangeText={setWeight}
                  keyboardType="numeric"
                  editable={canUpdateWeight}
                />
              </View>
              <TouchableOpacity
                onPress={handleUpdateWeight}
                disabled={!canUpdateWeight}
                className={`p-4 rounded-lg ${
                  canUpdateWeight ? "bg-[#2D3748]" : "bg-gray-200"
                }`}
              >
                <Text className="text-white text-center font-semibold">
                  Save
                </Text>
              </TouchableOpacity>
            </View>
          </View>

          {/* Weight History Chart */}
          {weightHistory.length > 0 && (
            <View className="bg-white p-4 rounded-xl shadow-sm mb-6">
              <Text className="text-xl font-semibold text-[#2D3748] mb-4">
                Weight History
              </Text>
              <LineChart
                data={chartData}
                width={screenWidth - 32}
                height={220}
                chartConfig={chartConfig}
                bezier
                style={{
                  marginVertical: 8,
                  borderRadius: 16,
                }}
                withDots={true}
                withInnerLines={true}
                withOuterLines={true}
                withVerticalLines={false}
                withHorizontalLines={true}
                withVerticalLabels={true}
                withHorizontalLabels={true}
                fromZero={false}
                yAxisLabel=""
                yAxisSuffix=" kg"
              />
            </View>
          )}
        </ScrollView>

        {/* Logout Button - Fixed at bottom */}
        <View className="px-4 pb-6 pt-2 border-t border-gray-100">
          <TouchableOpacity
            onPress={handleLogout}
            disabled={loggingOut}
            className="flex-row justify-center items-center bg-red-50 p-4 rounded-xl"
          >
            <Text className="text-red-600 text-lg mr-2">Logout</Text>
            <LogOut stroke="#DC2626" size={20} />
          </TouchableOpacity>
        </View>
      </View>
    </SafeAreaView>
  );
}
