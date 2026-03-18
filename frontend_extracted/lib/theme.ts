'use client';

export type Theme = 'dark' | 'light' | 'auto';

export const THEME_KEY = 'insightpulse-theme';

export function getThemeFromStorage(): Theme {
  if (typeof window === 'undefined') return 'dark';
  
  try {
    const stored = localStorage.getItem(THEME_KEY) as Theme | null;
    return stored || 'dark';
  } catch {
    return 'dark';
  }
}

export function setThemeInStorage(theme: Theme) {
  if (typeof window === 'undefined') return;
  
  try {
    localStorage.setItem(THEME_KEY, theme);
  } catch {
    console.error('Failed to save theme preference');
  }
}

export function applyTheme(theme: Theme) {
  if (typeof document === 'undefined') return;

  const root = document.documentElement;
  
  if (theme === 'auto') {
    const isDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    root.classList.toggle('dark', isDark);
    root.classList.toggle('light', !isDark);
  } else if (theme === 'dark') {
    root.classList.add('dark');
    root.classList.remove('light');
  } else {
    root.classList.remove('dark');
    root.classList.add('light');
  }
}

export function getSystemTheme(): 'dark' | 'light' {
  if (typeof window === 'undefined') return 'dark';
  return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
}

export const themeColors = {
  dark: {
    background: '#080818',
    foreground: '#e0e0ff',
    card: '#0f0f1e',
    primary: '#6366f1',
    secondary: '#8b5cf6',
    accent: '#14b8a6',
    border: '#2d2d4d',
  },
  light: {
    background: '#f8f9fa',
    foreground: '#1a1a2e',
    card: '#ffffff',
    primary: '#4f46e5',
    secondary: '#7c3aed',
    accent: '#0891b2',
    border: '#e0e0ff',
  },
};
