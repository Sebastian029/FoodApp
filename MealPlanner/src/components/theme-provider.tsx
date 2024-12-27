import { createContext, useContext, useState, useEffect } from "react";
import { useColorScheme } from "react-native";
import type { Theme } from "../utils/theme";
import { theme as defaultTheme } from "../utils/theme";

const ThemeContext = createContext<Theme>({
  isDark: false,
  colors: defaultTheme.light.colors,
  toggleTheme: () => {},
});

export function ThemeProvider({ children }: { children: React.ReactNode }) {
  const systemColorScheme = useColorScheme();
  const [isDark, setIsDark] = useState(systemColorScheme === "dark");

  useEffect(() => {
    setIsDark(systemColorScheme === "dark");
  }, [systemColorScheme]);

  const toggleTheme = () => {
    const newIsDark = !isDark; // Toggle the theme
    setIsDark(newIsDark); // Update the state

    // Log the updated state
    console.log("Theme toggled. Is dark mode:", newIsDark ? "dark" : "light");
  };
  const colors = isDark ? defaultTheme.dark.colors : defaultTheme.light.colors;

  return (
    <ThemeContext.Provider value={{ isDark, colors, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}

export function useTheme() {
  return useContext(ThemeContext);
}
