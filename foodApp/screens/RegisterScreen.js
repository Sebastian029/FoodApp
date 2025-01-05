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
import { shadows } from "../styles/theme";
import { authAPI } from "../utils/api";
import { useAuth } from "../contexts/AuthContext";

export default function RegisterScreen({ navigation }) {
  const [name, setName] = useState("");
  const [surname, setSurname] = useState(""); // Added state for surname
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirm_password, setConfirm_password] = useState("");
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();

  const handleRegister = async () => {
    if (password !== confirm_password) {
      Alert.alert("Error", "Passwords do not match");
      return;
    }

    try {
      setLoading(true);
      const response = await authAPI.register({
        name,
        surname,
        email,
        password,
        confirm_password,
      });
      await login(response.data);
    } catch (error) {
      console.error("Registration Error:", error.response || error);
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
        <View className="items-center mt-20 mb-10">
          <Text className="text-2xl font-bold">Register an account</Text>
        </View>

        {/* Form */}
        <View className="space-y-4">
          <TextInput
            className="bg-gray-50 p-4 rounded-lg border border-gray-200"
            placeholder="Enter your name"
            value={name}
            onChangeText={setName}
            style={{ marginVertical: 5 }} // Added margin
          />

          <TextInput
            className="bg-gray-50 p-4 rounded-lg border border-gray-200"
            placeholder="Enter your surname"
            value={surname}
            onChangeText={setSurname}
            style={{ marginVertical: 5 }} // Added margin
          />

          <TextInput
            className="bg-gray-50 p-4 rounded-lg border border-gray-200"
            placeholder="Enter your email"
            value={email}
            onChangeText={setEmail}
            keyboardType="email-address"
            autoCapitalize="none"
            style={{ marginVertical: 5 }} // Added margin
          />

          <TextInput
            className="bg-gray-50 p-4 rounded-lg border border-gray-200"
            placeholder="Enter your password"
            value={password}
            onChangeText={setPassword}
            secureTextEntry
            style={{ marginVertical: 5 }} // Added margin
          />

          <TextInput
            className="bg-gray-50 p-4 rounded-lg border border-gray-200"
            placeholder="Re-type your password"
            value={confirm_password}
            onChangeText={setConfirm_password}
            secureTextEntry
            style={{ marginVertical: 5 }} // Added margin
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
