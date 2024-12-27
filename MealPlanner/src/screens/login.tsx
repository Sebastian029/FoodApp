import { useState } from "react";
import { View, Image, Pressable, ActivityIndicator } from "react-native";
import { useNavigation } from "@react-navigation/native";
import { Text } from "../components/styled-text";
import { AuthInput } from "../components/auth-input";
import { ThemeToggle } from "../components/theme-toggle";
import { useTheme } from "../components/theme-provider";
import { useAuthContext } from "../contexts/auth-context";
//import { createAuthStyles } from "../styles/components/auth.styles";
import { createAuthStyles } from "../styles/components/auth.styles";

export function LoginScreen() {
  const navigation = useNavigation();
  const { colors } = useTheme();
  const { login, error } = useAuthContext();
  const styles = createAuthStyles(colors);

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  async function handleLogin() {
    try {
      setIsLoading(true);
      await login({ email, password });
    } catch (error) {
      console.error("Login failed:", error);
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <View style={styles.container}>
      <View style={{ alignItems: "flex-end", padding: 16 }}>
        <ThemeToggle />
      </View>

      <View style={styles.content}>
        <View style={styles.header}>
          <Image
            source={require("../../assets/images/llogo.png")}
            style={{ width: 200, height: 200 }}
          />
          <Text style={styles.title}>Welcome</Text>
        </View>

        {error && <Text>{error}</Text>}

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

        <Pressable>
          <Text style={styles.forgotPassword}></Text>
        </Pressable>

        <Pressable
          style={[styles.button]}
          onPress={handleLogin}
          disabled={isLoading}
        >
          {isLoading ? (
            <ActivityIndicator color="#FFFFFF" />
          ) : (
            <Text style={styles.buttonText}>Login</Text>
          )}
        </Pressable>

        <View style={styles.footer}>
          <Text style={{ color: colors.text.secondary }}>
            Don't have an account?{" "}
          </Text>
          <Pressable onPress={() => navigation.navigate("Register")}>
            <Text style={{ color: colors.primary, fontWeight: "500" }}>
              Sign up
            </Text>
          </Pressable>
        </View>
      </View>
    </View>
  );
}
