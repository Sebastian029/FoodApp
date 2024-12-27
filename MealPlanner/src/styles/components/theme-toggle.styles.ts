import { StyleSheet } from 'react-native'
import { spacing, radius } from '../spacing'

export const createThemeToggleStyles = (colors: ColorScheme) =>
  StyleSheet.create({
    toggle: {
      padding: spacing.sm,
      borderRadius: radius.full,
      backgroundColor: colors.background.secondary,
    },
  })

