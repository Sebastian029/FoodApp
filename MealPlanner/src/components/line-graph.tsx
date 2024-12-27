import { View, Dimensions } from 'react-native'
import { LineChart } from 'react-native-chart-kit'

interface LineGraphProps {
  data: {
    labels: string[]
    datasets: Array<{
      data: number[]
      color?: (opacity: number) => string
    }>
  }
}

export function LineGraph({ data }: LineGraphProps) {
  const screenWidth = Dimensions.get('window').width - 32 // Accounting for padding

  return (
    <View className="bg-white rounded-lg p-4 mb-4">
      <LineChart
        data={data}
        width={screenWidth}
        height={180}
        chartConfig={{
          backgroundColor: '#ffffff',
          backgroundGradientFrom: '#ffffff',
          backgroundGradientTo: '#ffffff',
          decimalPlaces: 1,
          color: (opacity = 1) => `rgba(27, 51, 88, ${opacity})`,
          style: {
            borderRadius: 16,
          },
        }}
        bezier
        style={{
          marginVertical: 8,
          borderRadius: 16,
        }}
      />
    </View>
  )
}

