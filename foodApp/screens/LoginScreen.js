import React, { useState } from "react";
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  Image,
  Alert,
  KeyboardAvoidingView,
  Platform,
} from "react-native";
import { shadows } from "../styles/theme";
import { authAPI } from "../utils/api";
import { useAuth } from "../contexts/AuthContext";

export default function LoginScreen({ navigation }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();

  const handleLogin = async () => {
    try {
      setLoading(true);
      const response = await authAPI.login({ email, password });
      await login(response.data);
    } catch (error) {
      Alert.alert("Error", error.response?.data?.message || "Failed to login");
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
        <View className="items-center mt-20 mb-12">
          <Image
            source={require("../assets/logo.png")}
            className="w-40 h-40 mb-6"
          />
          <Text className="text-2xl font-bold">Welcome</Text>
        </View>

        <View className="space-y-4">
          <TextInput
            className="bg-gray-50 p-4 rounded-lg border border-gray-200 mb-4"
            placeholder="Email"
            value={email}
            onChangeText={setEmail}
            keyboardType="email-address"
            autoCapitalize="none"
          />

          <TextInput
            className="bg-gray-50 p-4 rounded-lg border border-gray-200 mb-6"
            placeholder="Password"
            value={password}
            onChangeText={setPassword}
            secureTextEntry
          />

          <TouchableOpacity onPress={() => Alert.alert("Coming soon!")}>
            <Text className="text-right text-gray-600">
              Forget your password?
            </Text>
          </TouchableOpacity>

          <TouchableOpacity
            onPress={handleLogin}
            disabled={loading}
            className="bg-[#F5A623] p-4 rounded-full shadow-lg mt-6"
            style={shadows.default}
          >
            <Text className="text-center text-white font-semibold text-lg">
              {loading ? "Logging in..." : "Login"}
            </Text>
          </TouchableOpacity>
        </View>

        <View className="flex-row justify-center mt-6">
          <Text className="text-gray-600">Don't have an account? </Text>
          <TouchableOpacity onPress={() => navigation.navigate("Register")}>
            <Text className="text-[#F5A623] font-semibold">Sign up</Text>
          </TouchableOpacity>
        </View>
      </View>
    </KeyboardAvoidingView>
  );
}
