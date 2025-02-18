const BookCard = ({ book }) => {
    const dispatch = useDispatch();
  
    const handleAddToCart = () => {
      console.log('Adding to cart:', book);
      dispatch(addToCart({ book }));
      toast.success('Book added to cart!');
    };
  
    return (
      <div className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow duration-300">
        <img
          src={book.cover_image || '/default-book.jpg'}
          alt={book.title}
          className="w-full h-48 object-cover"
        />
        <div className="p-4">
          <h3 className="text-lg font-semibold truncate">{book.title}</h3>
          <p className="text-gray-600 mb-2">{book.author}</p>
          <div className="mt-4 flex items-center justify-between">
            <span className="text-blue-600 font-bold text-lg">${book.price}</span>
            <button
              onClick={handleAddToCart}
              className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors duration-300 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
            >
              <svg
                className="w-5 h-5"
                fill="none"
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
              </svg>
              Add to Cart
            </button>
          </div>
        </div>
      </div>
    );
  };