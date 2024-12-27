import { View, TextInput, TextInputProps, StyleSheet } from "react-native";
import { User, Mail, Lock } from "react-native-feather";
import { useTheme } from "./theme-provider";
import { spacing } from "../styles/spacing";
import { ColorScheme } from "../utils/theme";

interface AuthInputProps extends TextInputProps {
  type: "name" | "email" | "password";
}

export function AuthInput({ type, style, ...props }: AuthInputProps) {
  const { colors } = useTheme();
  const styles = createAuthInputStyles(colors);

  const Icon = {
    name: User,
    email: Mail,
    password: Lock,
  }[type];

  return (
    <View style={[styles.container]}>
      <Icon width={20} height={20} color={colors.text.secondary} />{" "}
      {/* Feather icons use width and height */}
      <TextInput
        style={styles.input}
        placeholderTextColor={colors.text.muted}
        secureTextEntry={type === "password"}
        autoCapitalize={type === "name" ? "words" : "none"}
        autoComplete={type === "password" ? "password" : "off"}
        keyboardType={type === "email" ? "email-address" : "default"}
        {...props}
      />
    </View>
  );
}

const createAuthInputStyles = (colors: ColorScheme) =>
  StyleSheet.create({
    container: {
      flexDirection: "row",
      alignItems: "center",
      backgroundColor: colors.background.card,
      borderRadius: 12,
      paddingHorizontal: spacing.md,
      paddingVertical: spacing.md,
      marginBottom: spacing.md,
    },
    input: {
      flex: 1,
      marginLeft: spacing.sm,
      color: colors.text.primary,
    },
  });
