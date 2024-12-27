import { createNativeStackNavigator } from "@react-navigation/native-stack";
import { LoginScreen } from "../screens/login"; 
import { RegisterScreen } from "../screens/register"; 

const Stack = createNativeStackNavigator();

export function AuthNavigator() {
  return (
    <Stack.Navigator id={undefined} screenOptions={{ headerShown: false }}>
      <Stack.Screen name="Login" component={LoginScreen} />
      <Stack.Screen name="Register" component={RegisterScreen} />
    </Stack.Navigator>
  );
}
