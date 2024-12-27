import { createBottomTabNavigator } from "@react-navigation/bottom-tabs";
import { createNativeStackNavigator } from "@react-navigation/native-stack";
import { Home, Calendar, ShoppingCart, Heart } from "lucide-react";
import { SettingsScreen } from "../screens/settings";
import { DietRestrictionsScreen } from "../screens/diet-restrictions";

const Tab = createBottomTabNavigator();
const Stack = createNativeStackNavigator();

function SettingsStack() {
  return (
    <Stack.Navigator screenOptions={{ headerShown: false }}>
      <Stack.Screen name="SettingsMain" component={SettingsScreen} />
      <Stack.Screen
        name="DietRestrictions"
        component={DietRestrictionsScreen}
      />
    </Stack.Navigator>
  );
}

export function TabNavigator() {
  return (
    <Tab.Navigator
      screenOptions={{
        headerShown: false,
        tabBarShowLabel: false,
        tabBarStyle: {
          borderTopWidth: 0,
          elevation: 0,
          shadowOpacity: 0,
        },
      }}
    >
      <Tab.Screen
        name="Home"
        component={SettingsStack}
        options={{
          tabBarIcon: ({ focused }) => (
            <Home
              size={24}
              className={focused ? "text-[#FDB347]" : "text-gray-400"}
            />
          ),
        }}
      />
      <Tab.Screen
        name="Calendar"
        component={SettingsStack}
        options={{
          tabBarIcon: ({ focused }) => (
            <Calendar
              size={24}
              className={focused ? "text-[#FDB347]" : "text-gray-400"}
            />
          ),
        }}
      />
      <Tab.Screen
        name="Cart"
        component={SettingsStack}
        options={{
          tabBarIcon: ({ focused }) => (
            <ShoppingCart
              size={24}
              className={focused ? "text-[#FDB347]" : "text-gray-400"}
            />
          ),
        }}
      />
      <Tab.Screen
        name="Favorites"
        component={SettingsStack}
        options={{
          tabBarIcon: ({ focused }) => (
            <Heart
              size={24}
              className={focused ? "text-[#FDB347]" : "text-gray-400"}
            />
          ),
        }}
      />
    </Tab.Navigator>
  );
}
