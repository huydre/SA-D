import { Link } from 'react-router-dom';
import { useSelector, useDispatch } from 'react-redux';
import { logout } from '../../features/auth/authSlice';
import { FaShoppingCart, FaUser, FaSearch } from 'react-icons/fa';
import { useState, React, useEffect } from 'react';
import { checkAuth } from '../../features/auth/authSlice';
import { selectIsAuthenticated, selectCurrentUser } from '../../features/auth/authSlice'
import { selectCartItemsCount } from '../../features/cart/cartSlice';
import { fetchCart } from '../../features/cart/cartSlice';

const Header = () => {
  const isAuthenticated = useSelector(selectIsAuthenticated);
  const [showUserDropdown, setShowUserDropdown] = useState(false);
  const user = useSelector(selectCurrentUser);
  const dispatch = useDispatch();
  const cartItems = useSelector((state) => state.cart.items);
  const [showCart, setShowCart] = useState(false);
  const [isLogin, setIsLogin] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      dispatch(checkAuth()).unwrap()
        .then(() => {
          setIsLogin(true);
        })
        .catch(() => {
          setIsLogin(false);
          localStorage.removeItem('token');
        });
    }
  }, [dispatch]);

  useEffect(() => {
    if (isAuthenticated) {
      dispatch(fetchCart());
    }
  }, [isAuthenticated, dispatch]);

  // Calculate total items and total price
  const totalItems = cartItems.reduce((total, item) => total + item.quantity, 0);
  const totalPrice = cartItems.reduce((total, item) => total + (parseFloat(item.subtotal)), 0);

  const handleLogout = () => {
    dispatch(logout());
  };

  console.log('cartItems:', cartItems);

  return (
    <header className="bg-white shadow-lg fixed w-full top-0 z-50">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-20">
          {/* Logo */}
          <a href="/" className="text-3xl font-bold bg-gradient-to-r from-blue-600 to-blue-800 bg-clip-text text-transparent hover:opacity-80 transition-opacity">
            BookStore
          </a>

          {/* Navigation */}
          <nav className="hidden md:flex items-center space-x-8">
            <a href="/books" className="text-gray-700 hover:text-blue-600 font-medium transition-colors">
              Books
            </a>
            <a href="/categories" className="text-gray-700 hover:text-blue-600 font-medium transition-colors">
              Categories
            </a>
            <a href="/about" className="text-gray-700 hover:text-blue-600 font-medium transition-colors">
              About
            </a>
          </nav>

          {/* Auth & Cart */}
          <div className="flex items-center gap-6">
            {isAuthenticated ? (
              <>
                {/* Cart Button */}
                <div className="relative">
                  <button
                    className="relative p-2 text-gray-600 hover:text-blue-600 transition-colors"
                    onClick={() => setShowCart(!showCart)}
                  >
                    <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
                    </svg>
                    {totalItems > 0 && (
                      <span className="absolute -top-1 -right-1 bg-blue-600 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center">
                        {totalItems}
                      </span>
                    )}
                  </button>

                  {/* Cart Dropdown */}
                  {showCart && (
                    <div className="absolute right-0 top-full mt-3 w-96 bg-white rounded-xl shadow-2xl py-4 border border-gray-100">
                      <div className="px-6 py-2 border-b border-gray-100">
                        <h3 className="font-semibold text-gray-800 text-lg">Shopping Cart ({totalItems})</h3>
                      </div>

                      <div className="max-h-96 overflow-y-auto px-2">
                        {cartItems.map((item) => (
                          <div key={item._id} className="flex items-center p-4 hover:bg-gray-50 rounded-lg transition-colors">
                            <img
                              src={"http://localhost:8000/media/" + item.book.image}
                              alt={item.book.title}
                              className="w-16 h-20 object-cover rounded-md shadow-sm"
                            />
                            <div className="ml-4 flex-1">
                              <h4 className="text-gray-800 font-medium">{item.book.title}</h4>
                              <p className="text-gray-500 text-sm mt-1">Qty: {item.quantity}</p>
                              <p className="text-blue-600 font-medium mt-1">${(item.subtotal)}</p>
                            </div>
                          </div>
                        ))}
                      </div>

                      <div className="px-6 py-4 border-t border-gray-100 mt-2">
                        <div className="flex justify-between items-center mb-4">
                          <span className="text-gray-600">Total:</span>
                          <span className="text-xl font-bold text-blue-600">${totalPrice}</span>
                        </div>
                        <div className="space-y-2">
                          <a
                            href="/cart"
                            className="block w-full px-4 py-2.5 text-center bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium"
                          >
                            View Cart
                          </a>
                          <a
                            href="/checkout"
                            className="block w-full px-4 py-2.5 text-center bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors font-medium"
                          >
                            Checkout
                          </a>
                        </div>
                      </div>
                    </div>
                  )}
                </div>

                {/* User Menu */}
                <div className="relative">
                  <button
                    className="flex items-center gap-3 text-gray-700 hover:text-blue-600 transition-colors"
                    onClick={() => setShowUserDropdown(!showUserDropdown)}
                  >
                    <div className="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center">
                      <svg className="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                      </svg>
                    </div>
                    <span className="hidden md:inline font-medium">{user.name}</span>
                  </button>

                  {/* User Dropdown */}
                  {showUserDropdown && (
                    <div className="absolute right-0 top-full mt-3 w-56 bg-white rounded-xl shadow-2xl py-2 border border-gray-100">
                      <a
                        href="/profile"
                        className="flex items-center px-6 py-3 text-gray-700 hover:bg-blue-50 hover:text-blue-600 transition-colors"
                      >
                        <svg className="w-5 h-5 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                        </svg>
                        Profile
                      </a>
                      <a
                        href="/orders"
                        className="flex items-center px-6 py-3 text-gray-700 hover:bg-blue-50 hover:text-blue-600 transition-colors"
                      >
                        <svg className="w-5 h-5 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" />
                        </svg>
                        Orders
                      </a>
                      <div className="border-t border-gray-100 my-2"></div>
                      <button
                        onClick={() => handleLogout()}
                        className="flex items-center w-full px-6 py-3 text-gray-700 hover:bg-blue-50 hover:text-blue-600 transition-colors"
                      >
                        <svg className="w-5 h-5 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                        </svg>
                        Logout
                      </button>
                    </div>
                  )}
                </div>
              </>
            ) : (
              <>
                <a
                  href="/login"
                  className="px-6 py-2.5 text-gray-700 hover:text-blue-600 font-medium transition-colors"
                >
                  Login
                </a>
                <a
                  href="/register"
                  className="px-6 py-2.5 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium"
                >
                  Register
                </a>
              </>
            )}
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;  
