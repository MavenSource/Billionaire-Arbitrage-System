import React from 'react'
import { ThemeProvider, CssBaseline } from '@mui/material'
import theme from '../theme'
export default function MyApp({ Component, pageProps }) {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Component {...pageProps} />
    </ThemeProvider>
  )
}
