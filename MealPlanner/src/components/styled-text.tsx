import { Text as RNText, TextProps } from 'react-native'
import { useTheme } from './theme-provider'

interface StyledTextProps extends TextProps {
  variant?: 'primary' | 'secondary' | 'muted'
}

export function Text({ variant = 'primary', style, ...props }: StyledTextProps) {
  const { colors } = useTheme()
  
  const textColor = {
    primary: colors.text.primary,
    secondary: colors.text.secondary,
    muted: colors.text.muted,
  }[variant]

  return (
    <RNText 
      style={[{ color: textColor }, style]} 
      className={props.className}
      {...props} 
    />
  )
}

