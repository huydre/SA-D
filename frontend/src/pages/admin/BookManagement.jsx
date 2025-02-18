import React, { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { fetchBooks, deleteBook } from '../../features/books/booksSlice';
import { useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify';

// Import your book actions here

const BookManagement = () => {
    const navigate = useNavigate();
  const dispatch = useDispatch();
  const { books, loading, error } = useSelector((state) => state.books);

  useEffect(() => {
    // Fetch books when component mounts
    dispatch(fetchBooks());
  }, [dispatch]);

  const handleDeleteBook = async (bookId) => {
    // Call your deleteBook action here
    try {
        console.log('bookId', bookId);
      const deleted = await dispatch(deleteBook(bookId)).unwrap();
      if (deleted) {
        toast.success('Book deleted successfully');
      } else {
        toast.error('Failed to delete book');
      }
    } catch (err) {
      console.error('Failed to delete book:', err);
    }
}

  return (
    <div className="space-y-4">
      <div className="flex justify-between items-center">
        <h2 className="text-xl font-bold">Book Management</h2>
        <button 
        onClick={() => navigate('/admin/books/add')} 
        className="bg-blue-500 text-white px-4 py-2 rounded"
        >
        Add New Book
        </button>
      </div>

      {loading && <div>Loading...</div>}
      {error && <div className="text-red-500">{error}</div>}

      {books.map((book) => (
  <tr key={book.id} className="border-b">
    <td className="px-6 py-4">{book.title}</td>
    <td className="px-6 py-4">{book.author}</td>
    <td className="px-6 py-4">${book.price}</td>
    <td className="px-6 py-4">{book.stock}</td>
    <td className="px-6 py-4 space-x-2">
      <button className="text-blue-500">Edit</button>
      <button 
        onClick={() => {
          if (window.confirm(`Are you sure you want to delete "${book.title}"?`)) {
            handleDeleteBook(book.id);
          }
        }} 
        className="text-red-500 hover:text-red-700"
      >
        Delete
      </button>
    </td>
  </tr>
))}
    </div>
  );
};

export default BookManagement;