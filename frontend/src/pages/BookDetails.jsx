import React from "react";
import { useParams } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import { fetchCart } from "../features/cart/cartSlice";
import { useState, useEffect } from "react";
import { fetchBookById } from "../features/books/booksSlice";
import { addItemToCart } from "../features/cart/cartSlice";

export const BookDetails = () => {
  const { id } = useParams();
  const dispatch = useDispatch();
  const { user } = useSelector((state) => state.auth);
  const [book, setBook] = useState(null);
  const [loading, setLoading] = useState(true);
  const [quantity, setQuantity] = useState(1);
  const [error, setError] = useState(null);
  const [addedToCart, setAddedToCart] = useState(false);

  useEffect(() => {
    const fetchBook = async () => {
      try {
        const book = await dispatch(fetchBookById(id)).unwrap();
        setBook(book);
      } catch (error) {
        console.error("Failed to fetch book", error);
      } finally {
        setLoading(false);
      }
    };

    fetchBook();
  }, [id]);

  const handleAddToCart = async () => {
    if (!user) {
      // Redirect to login or show login modal
      return;
    }

    try {
      await dispatch(addItemToCart({ book, quantity: quantity }));
      await dispatch(fetchCart());
    } catch (error) {
      setError("Failed to add item to cart");
    }
  };

  if (loading) return <div>Loading...</div>;
  if (!book) return <div>Book not found</div>;
  console.log(book);
  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-50 to-gray-100">
      <div className="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
        {/* Breadcrumb */}
        <nav className="flex mb-8" aria-label="Breadcrumb">
          <ol className="flex items-center space-x-2">
            <li>
              <a href="/" className="text-gray-500 hover:text-gray-700">
                Home
              </a>
            </li>
            <li className="flex items-center">
              <svg
                className="w-5 h-5 text-gray-400"
                fill="currentColor"
                viewBox="0 0 20 20"
              >
                <path
                  fillRule="evenodd"
                  d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z"
                  clipRule="evenodd"
                />
              </svg>
              <a
                href="/books"
                className="ml-2 text-gray-500 hover:text-gray-700"
              >
                Books
              </a>
            </li>
            <li className="flex items-center">
              <svg
                className="w-5 h-5 text-gray-400"
                fill="currentColor"
                viewBox="0 0 20 20"
              >
                <path
                  fillRule="evenodd"
                  d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z"
                  clipRule="evenodd"
                />
              </svg>
              <span className="ml-2 text-gray-900 font-medium">
                {book.title}
              </span>
            </li>
          </ol>
        </nav>

        <div className="bg-white rounded-2xl shadow-xl overflow-hidden">
          <div className="md:flex">
            {/* Book Image */}
            <div className="md:w-1/2 relative">
              <div className="sticky top-0">
                <img
                  src={book.image}
                  alt={book.title}
                  className="w-full h-[600px] object-cover"
                />
                {book.stock <= 5 && book.stock > 0 && (
                  <div className="absolute top-4 right-4 bg-red-500 text-white px-3 py-1 rounded-full text-sm font-semibold">
                    Only {book.stock} left!
                  </div>
                )}
              </div>
            </div>

            {/* Book Details */}
            <div className="md:w-1/2 p-8 lg:p-12">
              <div className="mb-8">
                <h1 className="text-4xl font-bold text-gray-900 mb-4">
                  {book.title}
                </h1>
                <p className="text-xl text-gray-600 mb-4">by {book.author}</p>
                <div className="flex items-center mb-6">
                  <span className="text-3xl font-bold text-blue-600">
                    ${book.price}
                  </span>
                  <span
                    className={`ml-4 px-3 py-1 rounded-full text-sm font-semibold ${
                      book.stock > 0
                        ? "bg-green-100 text-green-800"
                        : "bg-red-100 text-red-800"
                    }`}
                  >
                    {book.stock > 0 ? `${book.stock} in stock` : "Out of stock"}
                  </span>
                </div>
              </div>

              <div className="mb-8">
                <h2 className="text-2xl font-semibold mb-4">Description</h2>
                <p className="text-gray-600 leading-relaxed">
                  {book.description}
                </p>
              </div>

              <div className="mb-8">
                <h2 className="text-2xl font-semibold mb-4">Details</h2>
                <div className="grid grid-cols-2 gap-6">
                  <div>
                    <p className="text-gray-600 mb-2">
                      <span className="font-semibold text-gray-900">ISBN:</span>{" "}
                      {book.isbn}
                    </p>
                    <p className="text-gray-600">
                      <span className="font-semibold text-gray-900">
                        Publisher:
                      </span>{" "}
                      {book.publisher}
                    </p>
                  </div>
                  <div>
                    <p className="text-gray-600">
                      <span className="font-semibold text-gray-900">
                        Publication Date:
                      </span>{" "}
                      {new Date(book.publication_date).toLocaleDateString()}
                    </p>
                  </div>
                </div>
              </div>

              {book.stock > 0 && (
                <div className="space-y-4">
                  <div className="flex items-center space-x-4">
                    <div className="w-32">
                      <label
                        htmlFor="quantity"
                        className="block text-sm font-medium text-gray-700 mb-1"
                      >
                        Quantity
                      </label>
                      <input
                        type="number"
                        id="quantity"
                        min="1"
                        max={book.stock}
                        value={quantity}
                        onChange={(e) =>
                          setQuantity(
                            Math.min(
                              Math.max(1, parseInt(e.target.value) || 1),
                              book.stock
                            )
                          )
                        }
                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                      />
                    </div>
                    <button
                      onClick={handleAddToCart}
                      disabled={loading}
                      className={`flex-1 px-8 py-3 text-white rounded-lg text-lg font-semibold transition-all transform hover:scale-105 ${
                        loading
                          ? "bg-gray-400 cursor-not-allowed"
                          : "bg-blue-600 hover:bg-blue-700 active:bg-blue-800"
                      }`}
                    >
                      {loading ? (
                        <span className="flex items-center justify-center">
                          <svg
                            className="animate-spin -ml-1 mr-3 h-5 w-5 text-white"
                            xmlns="http://www.w3.org/2000/svg"
                            fill="none"
                            viewBox="0 0 24 24"
                          >
                            <circle
                              className="opacity-25"
                              cx="12"
                              cy="12"
                              r="10"
                              stroke="currentColor"
                              strokeWidth="4"
                            ></circle>
                            <path
                              className="opacity-75"
                              fill="currentColor"
                              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                            ></path>
                          </svg>
                          Adding to Cart...
                        </span>
                      ) : (
                        "Add to Cart"
                      )}
                    </button>
                  </div>

                  {addedToCart && (
                    <div className="animate-fade-in-down p-4 bg-green-100 border border-green-400 text-green-700 rounded-lg flex items-center">
                      <svg
                        className="w-5 h-5 mr-2"
                        fill="currentColor"
                        viewBox="0 0 20 20"
                      >
                        <path
                          fillRule="evenodd"
                          d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                          clipRule="evenodd"
                        />
                      </svg>
                      Added to cart successfully!
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
