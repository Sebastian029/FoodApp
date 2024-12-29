import { createBottomTabNavigator } from "@react-navigation/bottom-tabs";
import { Home, Calendar, User, ShoppingCart } from "react-native-feather";
import HomeScreen from "../screens/HomeScreen";
import PlannerScreen from "../screens/PlannerScreen";
import ProfileScreen from "../screens/ProfileScreen";
import CartScreen from "../screens/CartScreen";
import { colors } from "../styles/theme";

const Tab = createBottomTabNavigator();

export default function TabNavigator() {
  return (
    <Tab.Navigator
      screenOptions={{
        tabBarActiveTintColor: colors.primary,
        tabBarInactiveTintColor: "gray",
        tabBarStyle: {
          paddingBottom: 5,
          paddingTop: 5,
        },
        headerShown: false,
      }}
    >
      <Tab.Screen
        name="Home"
        component={HomeScreen}
        options={{
          tabBarIcon: ({ color, size }) => (
            <Home stroke={color} width={size} height={size} />
          ),
        }}
      />
      <Tab.Screen
        name="Planner"
        component={PlannerScreen}
        options={{
          tabBarIcon: ({ color, size }) => (
            <Calendar stroke={color} width={size} height={size} />
          ),
        }}
      />
      <Tab.Screen
        name="Cart"
        component={CartScreen}
        options={{
          tabBarIcon: ({ color, size }) => (
            <ShoppingCart stroke={color} width={size} height={size} />
          ),
        }}
      />
      <Tab.Screen
        name="Profile"
        component={ProfileScreen}
        options={{
          tabBarIcon: ({ color, size }) => (
            <User stroke={color} width={size} height={size} />
          ),
        }}
      />
    </Tab.Navigator>
  );
}
