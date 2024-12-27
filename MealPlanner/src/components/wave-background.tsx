import { View } from "react-native";
import Svg, { Path } from "react-native-svg";

export function WaveBackground() {
  return (
    <>
      <View className="absolute top-0 left-0 w-full z-10">
        <Svg
          height={120}
          width="100%"
          viewBox="0 0 375 120"
          preserveAspectRatio="none"
        >
          <Path
            d="M0,0 L375,0 L375,80 C275,120 175,100 0,80 L0,0 Z"
            fill="#FDB347"
          />
        </Svg>
      </View>

      <View className="absolute bottom-0 left-0 w-full z-10">
        <Svg
          height={120}
          width="100%"
          viewBox="0 0 375 120"
          preserveAspectRatio="none"
        >
          <Path
            d="M0,120 L0,40 C100,20 275,0 375,40 L375,120 L0,120 Z"
            fill="#FDB347"
          />
        </Svg>
      </View>
    </>
  );
}
