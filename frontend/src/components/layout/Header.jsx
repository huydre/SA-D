import { Link } from 'react-router-dom';
import { useSelector, useDispatch } from 'react-redux';
import { logout } from '../../features/auth/authSlice';
import { FaShoppingCart, FaUser, FaSearch } from 'react-icons/fa';
import { useState } from 'react';

const Header = () => {
  const dispatch = useDispatch();
  const { user } = useSelector((state) => state.auth);
  const cartItems = useSelector((state) => state.cart.items);
  const [showCart, setShowCart] = useState(false);

  // Calculate total items and total price
  const totalItems = cartItems.reduce((total, item) => total + item.quantity, 0);
  const totalPrice = cartItems.reduce((total, item) => total + (item.price * item.quantity), 0);

  return (
    <header className="bg-white shadow-md fixed w-full top-0 z-50">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link to="/" className="text-2xl font-bold text-blue-600 hover:text-blue-700 transition-colors">
            BookStore
          </Link>

          {/* Navigation */}
          <nav className="hidden md:flex items-center space-x-6">
            <Link to="/books" className="text-gray-600 hover:text-blue-600 transition-colors">
              Books
            </Link>
          </nav>

          {/* Auth & Cart */}
          <div className="flex items-center gap-4">
            {user ? (
              <>
                {/* Cart Dropdown */}
                <div className="relative group">
                  <button
                    className="relative p-2 text-gray-600 hover:text-blue-600 transition-colors"
                    onClick={() => setShowCart(!showCart)}
                  >
                    <FaShoppingCart className="text-xl" />
                    {totalItems > 0 && (
                      <span className="absolute -top-1 -right-1 bg-blue-600 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center">
                        {totalItems}
                      </span>
                    )}
                  </button>

                  {/* Cart Dropdown Content */}
                  {showCart && (
                    <div className="absolute right-0 top-full mt-2 w-80 bg-white rounded-lg shadow-lg py-4 z-50">
                      <div className="px-4 py-2 border-b border-gray-200">
                        <h3 className="font-semibold text-gray-700">Shopping Cart ({totalItems} items)</h3>
                      </div>
                      
                      <div className="max-h-96 overflow-y-auto">
                        {cartItems.length > 0 ? (
                          cartItems.map((item) => (
                            <div key={item.id} className="flex items-center px-4 py-3 hover:bg-gray-50">
                              <img
                                src={item.cover_image || '/default-book.jpg'}
                                alt={item.title}
                                className="w-12 h-16 object-cover rounded"
                              />
                              <div className="ml-3 flex-1">
                                <h4 className="text-sm font-medium text-gray-700 truncate">{item.title}</h4>
                                <p className="text-sm text-gray-500">Qty: {item.quantity}</p>
                                <p className="text-sm font-medium text-blue-600">${(item.price * item.quantity).toFixed(2)}</p>
                              </div>
                            </div>
                          ))
                        ) : (
                          <div className="px-4 py-6 text-center text-gray-500">
                            Your cart is empty
                          </div>
                        )}
                      </div>

                      {cartItems.length > 0 && (
                        <div className="px-4 py-3 border-t border-gray-200">
                          <div className="flex justify-between items-center mb-4">
                            <span className="font-medium text-gray-700">Total:</span>
                            <span className="font-bold text-blue-600">${totalPrice.toFixed(2)}</span>
                          </div>
                          <Link
                            to="/cart"
                            className="block w-full px-4 py-2 text-center bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                            onClick={() => setShowCart(false)}
                          >
                            View Cart
                          </Link>
                          <Link
                            to="/checkout"
                            className="block w-full px-4 py-2 mt-2 text-center bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
                            onClick={() => setShowCart(false)}
                          >
                            Checkout
                          </Link>
                        </div>
                      )}
                    </div>
                  )}
                </div>

                {/* User Dropdown */}
                <div className="relative group">
                  <button className="flex items-center gap-2 text-gray-600 hover:text-blue-600 transition-colors">
                    <FaUser className="text-xl" />
                    <span className="hidden md:inline">{user.name}</span>
                  </button>
                  <div className="absolute right-0 top-full mt-2 w-48 bg-white rounded-lg shadow-lg py-2 hidden group-hover:block">
                    <Link
                      to="/profile"
                      className="block px-4 py-2 text-gray-600 hover:bg-blue-50 hover:text-blue-600"
                    >
                      Profile
                    </Link>
                    <Link
                      to="/orders"
                      className="block px-4 py-2 text-gray-600 hover:bg-blue-50 hover:text-blue-600"
                    >
                      Orders
                    </Link>
                    <button
                      onClick={() => dispatch(logout())}
                      className="w-full text-left px-4 py-2 text-gray-600 hover:bg-blue-50 hover:text-blue-600"
                    >
                      Logout
                    </button>
                  </div>
                </div>
              </>
            ) : (
              <>
                <Link
                  to="/login"
                  className="px-4 py-2 text-gray-600 hover:text-blue-600 transition-colors"
                >
                  Login
                </Link>
                <Link
                  to="/register"
                  className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                >
                  Register
                </Link>
              </>
            )}
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;  
