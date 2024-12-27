import { Pressable } from "react-native";
import { useTheme } from "./theme-provider";
import { Sun, Moon } from "react-native-feather";

export function ThemeToggle() {
  const { isDark, toggleTheme, colors } = useTheme();

  return (
    <Pressable
      onPress={toggleTheme}
      className="p-2 rounded-full"
      style={{ backgroundColor: colors.background.secondary }}
    >
      {isDark ? (
        <Sun color={colors.text.primary} />
      ) : (
        <Moon color={colors.text.primary} />
      )}
    </Pressable>
  );
}
