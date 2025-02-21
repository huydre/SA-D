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
  async ({ book, quantity }, { rejectWithValue }) => {
    try {
      const response = await endpoints.cart.addItem({ 
        book_id: book._id, 
        quantity: quantity
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
  totalItems: 0,
  loading: false,
  error: null
};

const cartSlice = createSlice({
  name: 'cart',
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      // Fetch cart
      .addCase(fetchCart.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchCart.fulfilled, (state, action) => {
        state.loading = false;
        // Ensure we don't have duplicates when setting items
  const uniqueItems = [];
  const seenIds = new Set();
  
  action.payload.items.forEach(item => {
    if (!seenIds.has(item.book._id)) {
      uniqueItems.push(item);
      seenIds.add(item.book._id);
    }
  });
  
  state.items = uniqueItems;
  state.totalItems = uniqueItems.length;
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
        // Instead of pushing, we should update existing item or add new one
        const existingItemIndex = state.items.findIndex(
          item => item.book._id === action.payload.book._id
        );
        
        if (existingItemIndex !== -1) {
          // Update existing item
          state.items[existingItemIndex] = action.payload;
        } else {
          // Add new item
          state.items.push(action.payload);
        }
        
        // Update total items count
        state.totalItems = state.items.length;
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
export const selectCartTotal = state => {
  const uniqueItems = new Map();
  
  // Use only the latest entry for each book
  state.cart?.items.forEach(item => {
    uniqueItems.set(item.book._id, item);
  });
  
  return Array.from(uniqueItems.values())
    .reduce((total, item) => total + (parseFloat(item.book.price) * item.quantity), 0);
};
export const selectCartItemsCount = (state) => state.cart.totalItems;

export default cartSlice.reducer;