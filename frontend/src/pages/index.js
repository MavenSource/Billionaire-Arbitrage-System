import React, { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  Box,
  Grid,
  Paper,
  Button,
  Card,
  CardContent,
  Chip,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  CircularProgress
} from '@mui/material';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import AccountBalanceWalletIcon from '@mui/icons-material/AccountBalanceWallet';
import SpeedIcon from '@mui/icons-material/Speed';
import axios from 'axios';

export default function Dashboard() {
  const [health, setHealth] = useState(null);
  const [pools, setPools] = useState([]);
  const [opportunities, setOpportunities] = useState([]);
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState(null);

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 5000); // Refresh every 5 seconds
    return () => clearInterval(interval);
  }, []);

  const fetchData = async () => {
    try {
      const [healthRes, poolsRes, statsRes] = await Promise.all([
        axios.get('http://localhost:8000/api/health'),
        axios.get('http://localhost:8000/api/pools'),
        axios.get('http://localhost:8000/api/stats')
      ]);
      
      setHealth(healthRes.data);
      setPools(poolsRes.data);
      setStats(statsRes.data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching data:', error);
      setLoading(false);
    }
  };

  const findOpportunities = async () => {
    try {
      const res = await axios.get('http://localhost:8000/api/opportunities');
      setOpportunities(res.data);
    } catch (error) {
      console.error('Error finding opportunities:', error);
    }
  };

  if (loading) {
    return (
      <Container maxWidth="lg" sx={{ mt: 4, display: 'flex', justifyContent: 'center' }}>
        <CircularProgress />
      </Container>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      {/* Header */}
      <Box sx={{ mb: 4 }}>
        <Typography variant="h3" component="h1" gutterBottom>
          💰 Billionaire Arbitrage System
        </Typography>
        <Typography variant="subtitle1" color="text.secondary">
          Institutional-Grade DeFi Arbitrage & MEV Platform
        </Typography>
      </Box>

      {/* Status Cards */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={4}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                <TrendingUpIcon color="primary" sx={{ mr: 1 }} />
                <Typography variant="h6">System Status</Typography>
              </Box>
              <Typography variant="h4">
                {health?.status === 'healthy' ? '✅ Healthy' : '⚠️ Degraded'}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Web3: {health?.web3_connected ? 'Connected' : 'Disconnected'}
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={4}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                <AccountBalanceWalletIcon color="success" sx={{ mr: 1 }} />
                <Typography variant="h6">Total Profit</Typography>
              </Box>
              <Typography variant="h4" color="success.main">
                ${health?.total_profit || '0.00'}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Trades: {health?.trades_executed || 0}
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={4}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                <SpeedIcon color="info" sx={{ mr: 1 }} />
                <Typography variant="h6">Opportunities</Typography>
              </Box>
              <Typography variant="h4" color="info.main">
                {health?.opportunities_found || 0}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Found Today
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Actions */}
      <Box sx={{ mb: 4 }}>
        <Button
          variant="contained"
          size="large"
          onClick={findOpportunities}
          sx={{ mr: 2 }}
        >
          🔍 Scan for Opportunities
        </Button>
        <Button variant="outlined" size="large">
          ⚙️ Configure Settings
        </Button>
      </Box>

      {/* Opportunities Table */}
      {opportunities.length > 0 && (
        <Box sx={{ mb: 4 }}>
          <Typography variant="h5" gutterBottom>
            📊 Active Opportunities
          </Typography>
          <TableContainer component={Paper}>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>DEX 1</TableCell>
                  <TableCell>DEX 2</TableCell>
                  <TableCell>Token Pair</TableCell>
                  <TableCell align="right">Profit</TableCell>
                  <TableCell align="right">Profit %</TableCell>
                  <TableCell>Risk</TableCell>
                  <TableCell>Action</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {opportunities.map((opp, index) => (
                  <TableRow key={index}>
                    <TableCell>{opp.pool1.dex}</TableCell>
                    <TableCell>{opp.pool2.dex}</TableCell>
                    <TableCell>
                      {opp.pool1.token0}/{opp.pool1.token1}
                    </TableCell>
                    <TableCell align="right">${opp.profit}</TableCell>
                    <TableCell align="right">{opp.profit_percentage}%</TableCell>
                    <TableCell>
                      <Chip
                        label={opp.risk}
                        color={
                          opp.risk === 'low'
                            ? 'success'
                            : opp.risk === 'medium'
                            ? 'warning'
                            : 'error'
                        }
                        size="small"
                      />
                    </TableCell>
                    <TableCell>
                      <Button variant="contained" size="small" color="success">
                        Execute
                      </Button>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </Box>
      )}

      {/* Pools Table */}
      <Box>
        <Typography variant="h5" gutterBottom>
          💧 Active Liquidity Pools
        </Typography>
        <TableContainer component={Paper}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>DEX</TableCell>
                <TableCell>Token Pair</TableCell>
                <TableCell align="right">Reserve 0</TableCell>
                <TableCell align="right">Reserve 1</TableCell>
                <TableCell align="right">Liquidity</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {pools.map((pool, index) => (
                <TableRow key={index}>
                  <TableCell>
                    <Chip label={pool.dex} color="primary" size="small" />
                  </TableCell>
                  <TableCell>
                    {pool.token0}/{pool.token1}
                  </TableCell>
                  <TableCell align="right">
                    {parseFloat(pool.reserve0).toLocaleString()}
                  </TableCell>
                  <TableCell align="right">
                    {parseFloat(pool.reserve1).toLocaleString()}
                  </TableCell>
                  <TableCell align="right">
                    ${parseFloat(pool.liquidity).toLocaleString()}
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </Box>
    </Container>
  );
}
