// src/components/books/BookList.jsx
import { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import {
  fetchBooks,
  selectAllBooks,
  selectBooksLoading,
  selectBooksError,
  selectBooksFilters,
  selectCurrentPage,
  selectTotalPages,
  setFilters,
  setPage,
} from '../../features/books/booksSlice';
import BookCard from './BookCard';

const BookList = () => {
  const dispatch = useDispatch();
  const books = useSelector(selectAllBooks);
  const isLoading = useSelector(selectBooksLoading);
  const error = useSelector(selectBooksError);
  const filters = useSelector(selectBooksFilters);
  const currentPage = useSelector(selectCurrentPage);
  const totalPages = useSelector(selectTotalPages);

  useEffect(() => {
    dispatch(fetchBooks({ page: currentPage, filters }));
  }, [dispatch, currentPage, filters]);

  const handleSearch = (searchTerm) => {
    dispatch(setFilters({ search: searchTerm }));
  };

  const handlePageChange = (newPage) => {
    dispatch(setPage(newPage));
  };

  if (isLoading) {
    return <div className="flex justify-center">Loading...</div>;
  }

  if (error) {
    return <div className="text-red-500 text-center">{error}</div>;
  }

  return (
    <div className="space-y-6">
      {/* Search and Filters */}
      <div className="flex gap-4 mb-6">
        <input
          type="text"
          placeholder="Search books..."
          className="input"
          value={filters.search}
          onChange={(e) => handleSearch(e.target.value)}
        />
        {/* Add more filters here */}
      </div>

      {/* Book Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {books.map((book) => (
          <BookCard key={book.id} book={book} />
        ))}
      </div>

      {/* Pagination */}
      <div className="flex justify-center gap-2 mt-6">
        {Array.from({ length: totalPages }, (_, i) => i + 1).map((page) => (
          <button
            key={page}
            onClick={() => handlePageChange(page)}
            className={`px-4 py-2 rounded ${
              currentPage === page
                ? 'bg-primary text-white'
                : 'bg-gray-200 hover:bg-gray-300'
            }`}
          >
            {page}
          </button>
        ))}
      </div>
    </div>
  );
};

export default BookList;