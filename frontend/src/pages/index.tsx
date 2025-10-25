import { useState, useEffect } from 'react'
import Head from 'next/head'
import {
  Container,
  Typography,
  Box,
  Paper,
  Grid,
  Card,
  CardContent,
  Button,
  Chip,
  Alert,
  CircularProgress,
} from '@mui/material'
import { createTheme, ThemeProvider } from '@mui/material/styles'
import axios from 'axios'

const darkTheme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#00ff88',
    },
    secondary: {
      main: '#ff00ff',
    },
  },
})

interface HealthData {
  status: string
  message: string
  rpc_configured: boolean
}

interface PoolData {
  pool_id: string
  dex: string
  token_a: string
  token_b: string
  liquidity: number
}

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export default function Home() {
  const [health, setHealth] = useState<HealthData | null>(null)
  const [pools, setPools] = useState<PoolData[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetchData()
  }, [])

  const fetchData = async () => {
    try {
      setLoading(true)
      setError(null)

      // Fetch health status
      const healthResponse = await axios.get<HealthData>(`${API_BASE_URL}/api/health`)
      setHealth(healthResponse.data)

      // Fetch pools
      const poolsResponse = await axios.get<PoolData[]>(`${API_BASE_URL}/api/pools`)
      setPools(poolsResponse.data)
    } catch (err) {
      setError('Failed to connect to backend API. Make sure the backend is running.')
      console.error('API Error:', err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <ThemeProvider theme={darkTheme}>
      <Head>
        <title>Billionaire Arbitrage System</title>
        <meta name="description" content="DeFi Arbitrage and MEV Platform" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <Box sx={{ bgcolor: '#0a0e27', minHeight: '100vh', py: 4 }}>
        <Container maxWidth="xl">
          {/* Header */}
          <Box sx={{ mb: 4, textAlign: 'center' }}>
            <Typography variant="h2" component="h1" sx={{ 
              fontWeight: 'bold', 
              color: '#00ff88',
              mb: 1 
            }}>
              💎 Billionaire Arbitrage System
            </Typography>
            <Typography variant="h6" sx={{ color: '#888' }}>
              DeFi Arbitrage & MEV Extraction Platform
            </Typography>
          </Box>

          {/* Error Alert */}
          {error && (
            <Alert severity="error" sx={{ mb: 3 }}>
              {error}
            </Alert>
          )}

          {/* System Status */}
          {loading && (
            <Box sx={{ display: 'flex', justifyContent: 'center', my: 4 }}>
              <CircularProgress />
            </Box>
          )}

          {!loading && health && (
            <Grid container spacing={3} sx={{ mb: 4 }}>
              <Grid item xs={12} md={4}>
                <Card sx={{ bgcolor: '#1a1f3a' }}>
                  <CardContent>
                    <Typography variant="h6" gutterBottom>
                      System Status
                    </Typography>
                    <Chip 
                      label={health.status.toUpperCase()} 
                      color="success" 
                      sx={{ mt: 1 }}
                    />
                  </CardContent>
                </Card>
              </Grid>

              <Grid item xs={12} md={4}>
                <Card sx={{ bgcolor: '#1a1f3a' }}>
                  <CardContent>
                    <Typography variant="h6" gutterBottom>
                      RPC Configuration
                    </Typography>
                    <Chip 
                      label={health.rpc_configured ? 'CONFIGURED' : 'NOT CONFIGURED'} 
                      color={health.rpc_configured ? 'success' : 'warning'}
                      sx={{ mt: 1 }}
                    />
                  </CardContent>
                </Card>
              </Grid>

              <Grid item xs={12} md={4}>
                <Card sx={{ bgcolor: '#1a1f3a' }}>
                  <CardContent>
                    <Typography variant="h6" gutterBottom>
                      Active Pools
                    </Typography>
                    <Typography variant="h4" sx={{ color: '#00ff88', mt: 1 }}>
                      {pools.length}
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
            </Grid>
          )}

          {/* Pools Table */}
          {!loading && pools.length > 0 && (
            <Paper sx={{ p: 3, bgcolor: '#1a1f3a' }}>
              <Typography variant="h5" gutterBottom sx={{ mb: 3 }}>
                DeFi Pools
              </Typography>
              <Grid container spacing={2}>
                {pools.map((pool) => (
                  <Grid item xs={12} md={6} key={pool.pool_id}>
                    <Card sx={{ bgcolor: '#0f1428' }}>
                      <CardContent>
                        <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
                          <Typography variant="h6">
                            {pool.token_a} / {pool.token_b}
                          </Typography>
                          <Chip label={pool.dex} size="small" color="primary" />
                        </Box>
                        <Typography variant="body2" color="textSecondary">
                          Pool ID: {pool.pool_id}
                        </Typography>
                        <Typography variant="body1" sx={{ mt: 1, color: '#00ff88' }}>
                          Liquidity: ${pool.liquidity.toLocaleString()}
                        </Typography>
                      </CardContent>
                    </Card>
                  </Grid>
                ))}
              </Grid>
            </Paper>
          )}

          {/* Setup Instructions */}
          {!loading && !health?.rpc_configured && (
            <Alert severity="info" sx={{ mt: 3 }}>
              <Typography variant="h6" gutterBottom>
                Setup Required
              </Typography>
              <Typography variant="body2">
                1. Copy backend/.env.example to backend/.env<br/>
                2. Add your RPC_URL and PRIVATE_KEY<br/>
                3. Restart the backend server
              </Typography>
            </Alert>
          )}

          {/* Action Buttons */}
          <Box sx={{ mt: 4, textAlign: 'center' }}>
            <Button 
              variant="contained" 
              onClick={fetchData}
              sx={{ mr: 2 }}
            >
              Refresh Data
            </Button>
            <Button 
              variant="outlined"
              href="http://localhost:8000/docs"
              target="_blank"
            >
              API Documentation
            </Button>
          </Box>
        </Container>
      </Box>
    </ThemeProvider>
  )
}
