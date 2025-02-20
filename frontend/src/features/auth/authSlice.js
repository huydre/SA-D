// src/features/auth/authSlice.js
import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import axios from '../../services/api';

const initialState = {
  user: null,
  isLoading: false,
  error: null,
};

export const login = createAsyncThunk(
  'auth/login',
  async (credentials) => {
    const response = await axios.post('/auth/login/', credentials);
    console.log(response.data);
    localStorage.setItem('token', response.data.tokens.access);
    return response.data.user;
  }
);

export const register = createAsyncThunk(
  'auth/register',
  async (userData) => {
    const response = await axios.post('/auth/register/', userData);
    console.log(response.data);
    localStorage.setItem('token', response.data.tokens.access);
    return response.data.user;
  }
);

const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    logout: (state) => {
      state.user = null;
      localStorage.removeItem('token');
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(login.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(login.fulfilled, (state, action) => {
        state.isLoading = false;
        state.user = action.payload;
      })
      .addCase(login.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.error.message;
      });
  },
});

export const { logout } = authSlice.actions;
export default authSlice.reducer;