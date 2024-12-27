import { StyleSheet } from "react-native";
import { spacing, radius } from "../spacing";
import { typography } from "../typography";
import { ColorScheme } from "../../utils/theme";

export const createAuthStyles = (colors: ColorScheme) =>
  StyleSheet.create({
    container: {
      flex: 1,
      backgroundColor: colors.background.primary,
    },
    content: {
      flex: 1,
      paddingHorizontal: spacing.xl,
      paddingTop: spacing.xxl,
    },
    header: {
      alignItems: "center",
      marginBottom: spacing.xl,
    },
    logo: {
      width: 96,
      height: 96,
      resizeMode: "contain",
    },
    title: {
      fontSize: typography.sizes.xxl,
      fontWeight: typography.weights.medium,
      color: colors.text.primary,
      marginTop: spacing.md,
    },
    inputContainer: {
      flexDirection: "row",
      alignItems: "center",
      backgroundColor: colors.background.card,
      borderRadius: radius.lg,
      paddingHorizontal: spacing.md,
      paddingVertical: spacing.md,
      marginBottom: spacing.md,
    },
    input: {
      flex: 1,
      marginLeft: spacing.sm,
      color: colors.text.primary,
      fontSize: typography.sizes.md,
    },
    forgotPassword: {
      textAlign: "right",
      marginBottom: spacing.xl,
      color: colors.text.secondary,
    },
    button: {
      backgroundColor: colors.primary,
      paddingVertical: spacing.md,
      borderRadius: radius.lg,
      alignItems: "center",
    },
    buttonText: {
      color: "#FFFFFF",
      fontWeight: typography.weights.medium,
    },
    footer: {
      flexDirection: "row",
      justifyContent: "center",
      marginTop: spacing.xl,
    },
  });
