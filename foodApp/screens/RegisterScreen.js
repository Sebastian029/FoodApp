import React, { useState } from "react";
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  Alert,
  KeyboardAvoidingView,
  Platform,
} from "react-native";
import { colors, shadows } from "../styles/theme";
import { tokenManager } from "../utils/tokenManager";
import { authAPI } from "../utils/api";

export default function RegisterScreen({ navigation }) {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [loading, setLoading] = useState(false);

  const handleRegister = async () => {
    if (password !== confirmPassword) {
      Alert.alert("Error", "Passwords do not match");
      return;
    }

    try {
      setLoading(true);
      const response = await authAPI.register({ name, email, password });
      await tokenManager.setToken(response.data.token);
      navigation.reset({
        index: 0,
        routes: [{ name: "Main" }],
      });
    } catch (error) {
      Alert.alert(
        "Error",
        error.response?.data?.message || "Failed to register"
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <KeyboardAvoidingView
      behavior={Platform.OS === "ios" ? "padding" : "height"}
      className="flex-1 bg-white"
    >
      <View className="flex-1 p-6">
        {/* Header */}
        <View className="items-center mt-20 mb-12">
          <Text className="text-2xl font-bold">Register an account</Text>
        </View>

        {/* Form */}
        <View className="space-y-4">
          <TextInput
            className="bg-gray-50 p-4 rounded-lg border border-gray-200 mb-4"
            placeholder="Enter your name"
            value={name}
            onChangeText={setName}
          />

          <TextInput
            className="bg-gray-50 p-4 rounded-lg border border-gray-200 mb-4"
            placeholder="Enter your email"
            value={email}
            onChangeText={setEmail}
            keyboardType="email-address"
            autoCapitalize="none"
          />

          <TextInput
            className="bg-gray-50 p-4 rounded-lg border border-gray-200 mb-4"
            placeholder="Enter your password"
            value={password}
            onChangeText={setPassword}
            secureTextEntry
          />

          <TextInput
            className="bg-gray-50 p-4 rounded-lg border border-gray-200 mb-6" // More margin-bottom for spacing
            placeholder="Re-type your password"
            value={confirmPassword}
            onChangeText={setConfirmPassword}
            secureTextEntry
          />

          <TouchableOpacity
            onPress={handleRegister}
            disabled={loading}
            className="bg-[#F5A623] p-4 rounded-full shadow-lg"
            style={shadows.default}
          >
            <Text className="text-center text-white font-semibold text-lg">
              {loading ? "Registering..." : "Register"}
            </Text>
          </TouchableOpacity>
        </View>

        {/* Sign In Link */}
        <View className="flex-row justify-center mt-6">
          <Text className="text-gray-600">Already have an account? </Text>
          <TouchableOpacity onPress={() => navigation.navigate("Login")}>
            <Text className="text-[#F5A623] font-semibold">Sign in</Text>
          </TouchableOpacity>
        </View>
      </View>
    </KeyboardAvoidingView>
  );
}
