// src/features/books/booksSlice.js

import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import axios from '../../services/api';

// Initial state
const initialState = {
    books: [],
    status: 'idle',
    error: null,
    currentPage: 1,
    totalPages: 0,
    totalItems: 0,
    filters: {
      minPrice: '',
      maxPrice: '',
      category: '',
      sortBy: 'title'
    }
  };

// Async thunks
export const fetchBooks = createAsyncThunk(
    'books/fetchBooks',
    async ({ page = 1, search = '', filters = {} } = {}, { rejectWithValue }) => {
      try {
        const params = {
          page,
          search,
          ...filters
        };
        const response = await axios.get('/books/', { params });
        return response.data;
      } catch (error) {
        console.error(error);
        return rejectWithValue(error.response?.data || 'Something went wrong');
      }
    }
  );

export const fetchBookById = createAsyncThunk(
  'books/fetchBookById',
  async (id, { rejectWithValue }) => {
    try {
      const response = await axios.get(`/books/${id}/`);
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response?.data || 'Failed to fetch book');
    }
  }
);

export const createBook = createAsyncThunk(
  'books/createBook',
  async (bookData, { rejectWithValue }) => {
    try {
      const response = await axios.post('/books/', bookData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response?.data || 'Failed to create book');
    }
  }
);

export const updateBook = createAsyncThunk(
  'books/updateBook',
  async ({ id, bookData }, { rejectWithValue }) => {
    try {
      const response = await axios.put(`/books/${id}/`, bookData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response?.data || 'Failed to update book');
    }
  }
);

export const deleteBook = createAsyncThunk(
  'books/deleteBook',
  async (bookId, { rejectWithValue }) => {
    try {
      await axios.delete(`/books/${bookId}/`);
      return bookId;
    } catch (error) {
      return rejectWithValue(error.response?.data || 'Failed to delete book');
    }
  }
);

// Slice
const booksSlice = createSlice({
    name: 'books',
    initialState,
    reducers: {
      setFilters: (state, action) => {
        state.filters = { ...state.filters, ...action.payload };
      },
      setCurrentPage: (state, action) => {
        state.currentPage = action.payload;
      },
      resetFilters: (state) => {
        state.filters = initialState.filters;
      }
    },
    extraReducers: (builder) => {
      builder
        .addCase(fetchBooks.pending, (state) => {
          state.status = 'loading';
        })
        .addCase(fetchBooks.fulfilled, (state, action) => {
          state.status = 'succeeded';
          state.books = action.payload.results;
          state.totalPages = Math.ceil(action.payload.count / 12);
          state.totalItems = action.payload.count;
        })
        .addCase(fetchBooks.rejected, (state, action) => {
          state.status = 'failed';
          state.error = action.payload?.message || 'Something went wrong';
        })
        .addCase(deleteBook.fulfilled, (state, action) => {
          state.books = state.books.filter(book => book.id !== action.payload);
        });
    },
  });

  export const { setFilters, setCurrentPage, resetFilters } = booksSlice.actions;

  export const selectAllBooks = (state) => state.books.books;
  export const selectBooksStatus = (state) => state.books.status;
  export const selectBooksError = (state) => state.books.error;
  export const selectCurrentPage = (state) => state.books.currentPage;
  export const selectTotalPages = (state) => state.books.totalPages;
  export const selectFilters = (state) => state.books.filters;

export default booksSlice.reducer;