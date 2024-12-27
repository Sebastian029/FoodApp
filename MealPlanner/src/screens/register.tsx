import { useState } from "react";
import { View, Text, Pressable, ActivityIndicator } from "react-native";
import { useNavigation } from "@react-navigation/native";
import { AuthInput } from "../components/auth-input";
import { useTheme } from "../components/theme-provider";
import { createAuthStyles } from "../styles/components/auth.styles";

export function RegisterScreen() {
  const navigation = useNavigation();
  const { colors } = useTheme();
  const styles = createAuthStyles(colors);

  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [retypePassword, setRetypePassword] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  async function handleRegister() {
    try {
      setIsLoading(true);
      // Your registration logic here
    } catch (error) {
      console.error("Registration failed:", error);
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <View style={styles.container}>
      <View style={styles.content}>
        <Text style={styles.title}>Register an account</Text>

        <AuthInput
          type="name"
          placeholder="Enter your name"
          value={name}
          onChangeText={setName}
        />

        <AuthInput
          type="email"
          placeholder="Enter your email"
          value={email}
          onChangeText={setEmail}
          autoCapitalize="none"
          keyboardType="email-address"
        />

        <AuthInput
          type="password"
          placeholder="Enter your password"
          value={password}
          onChangeText={setPassword}
          secureTextEntry
        />

        <AuthInput
          type="password"
          placeholder="Re-type your password"
          value={retypePassword}
          onChangeText={setRetypePassword}
          secureTextEntry
        />

        <Pressable
          style={[styles.button, isLoading && styles.buttonDisabled]}
          onPress={handleRegister}
          disabled={isLoading}
        >
          {isLoading ? (
            <ActivityIndicator color="#FFFFFF" />
          ) : (
            <Text style={styles.buttonText}>Register</Text>
          )}
        </Pressable>

        <View style={styles.footer}>
          <Text style={{ color: colors.text.secondary }}>
            Already have an account?{" "}
          </Text>
          <Pressable onPress={() => navigation.navigate("Login")}>
            <Text style={{ color: colors.primary, fontWeight: "500" }}>
              Sign in
            </Text>
          </Pressable>
        </View>
      </View>
    </View>
  );
}
