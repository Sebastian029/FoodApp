export const theme = {
  light: {
    colors: {
      primary: '#1B3358',
      text: {
        primary: '#1A1A1A',
        secondary: '#666666',
        muted: '#999999',
      },
      background: {
        primary: '#FFFFFF',
        secondary: '#F5F5F5',
        card: '#FFFFFF'
      },
      accent: '#FDB347',
      border: '#E5E7EB'
    }
  },
  dark: {
    colors: {
      primary: '#3B82F6',
      text: {
        primary: '#FFFFFF',
        secondary: '#E5E7EB',
        muted: '#9CA3AF',
      },
      background: {
        primary: '#111827',
        secondary: '#1F2937',
        card: '#374151'
      },
      accent: '#FDB347',
      border: '#374151'
    }
  }
}

export type ThemeColors = typeof theme.light.colors
export type Theme = {
  isDark: boolean
  colors: ThemeColors
  toggleTheme: () => void
}

export type ColorScheme = {
  primary: string;
  text: {
    primary: string;
    secondary: string;
    muted: string;
  };
  background: {
    primary: string;
    secondary: string;
    card: string;
  };
  accent: string;
  border: string;
};
