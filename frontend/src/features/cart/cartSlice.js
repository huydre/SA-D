import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { endpoints } from '../../services/api';

// Fetch cart for current user
export const fetchCart = createAsyncThunk(
  'cart/fetchCart',
  async (_, { rejectWithValue }) => {
    try {
      const response = await endpoints.cart.get();
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response.data);
    }
  }
);

// Add item to cart
export const addItemToCart = createAsyncThunk(
  'cart/addItem',
  async ({ book }, { rejectWithValue }) => {
    try {
      const response = await endpoints.cart.addItem({ 
        book_id: book._id, 
        quantity: 1 
      });
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response.data);
    }
  }
);

// Update cart item
export const updateCartItem = createAsyncThunk(
  'cart/updateItem',
  async ({ itemId, quantity }, { rejectWithValue }) => {
    try {
      const response = await endpoints.cartItems.update(itemId, { quantity });
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response.data);
    }
  }
);

// Remove cart item
export const removeCartItem = createAsyncThunk(
  'cart/removeItem',
  async (itemId, { rejectWithValue }) => {
    try {
      await endpoints.cartItems.delete(itemId);
      return itemId;
    } catch (error) {
      return rejectWithValue(error.response.data);
    }
  }
);

const initialState = {
  items: [],
  loading: false,
  error: null,
};

const cartSlice = createSlice({
  name: 'cart',
  initialState,
  reducers: {
    resetCart: (state) => {
      state.items = [];
      state.loading = false;
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    builder
      // Fetch cart
      .addCase(fetchCart.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchCart.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.items || [];
      })
      .addCase(fetchCart.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      // Add item
      .addCase(addItemToCart.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(addItemToCart.fulfilled, (state, action) => {
        state.loading = false;
        state.items.push(action.payload);
      })
      .addCase(addItemToCart.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      // Update item
      .addCase(updateCartItem.fulfilled, (state, action) => {
        const updatedItem = action.payload;
        const index = state.items.findIndex(item => item.id === updatedItem.id);
        if (index !== -1) {
          state.items[index] = updatedItem;
        }
      })
      // Remove item
      .addCase(removeCartItem.fulfilled, (state, action) => {
        state.items = state.items.filter(item => item.id !== action.payload);
      });
  },
});

export const { resetCart } = cartSlice.actions;

export const selectCartItems = state => state.cart?.items || [];
export const selectCartTotal = state => 
  (state.cart?.items || []).reduce((total, item) => total + (item.book.price * item.quantity), 0);
export const selectCartItemsCount = state =>
  (state.cart?.items || []).reduce((count, item) => count + item.quantity, 0);

export default cartSlice.reducer;