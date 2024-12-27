import { NavigationContainer } from "@react-navigation/native";
import { AuthProvider } from "../src/contexts/auth-context";
import { CacheProvider } from "../src/providers/cache-provider";
import { AuthNavigator } from "../src/navigation/auth-navigator";
import { TabNavigator } from "../src/navigation/tab-navigator";
import { ThemeProvider } from "components/theme-provider";

export default function App() {
  const isAuthenticated = false;
  return (
    <CacheProvider>
      <ThemeProvider>
        <AuthProvider>
          <AuthNavigator />
        </AuthProvider>
      </ThemeProvider>
    </CacheProvider>
  );
}
