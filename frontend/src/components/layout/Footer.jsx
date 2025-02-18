import React from 'react'

function Footer() {
    return (
      <footer className="bg-gray-900 text-gray-300">
        {/* Main Footer */}
        <div className="container mx-auto px-4 py-16">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            {/* About Section */}
            <div className="space-y-4">
              <h3 className="text-xl font-bold text-white">BookStore</h3>
              <p className="text-sm">
                Your one-stop destination for all your literary needs. Discover millions of eBooks, audiobooks, and more.
              </p>
              <div className="flex space-x-4">
                <a href="#" className="hover:text-white transition-colors">
                  <i className="fab fa-facebook-f"></i>
                </a>
                <a href="#" className="hover:text-white transition-colors">
                  <i className="fab fa-twitter"></i>
                </a>
                <a href="#" className="hover:text-white transition-colors">
                  <i className="fab fa-instagram"></i>
                </a>
                <a href="#" className="hover:text-white transition-colors">
                  <i className="fab fa-linkedin-in"></i>
                </a>
              </div>
            </div>
  
            {/* Quick Links */}
            <div>
              <h3 className="text-lg font-semibold text-white mb-4">Quick Links</h3>
              <ul className="space-y-2">
                {['Home', 'About Us', 'Books', 'Categories', 'Contact'].map((link) => (
                  <li key={link}>
                    <a
                      href="#"
                      className="text-sm hover:text-white hover:underline transition-colors"
                    >
                      {link}
                    </a>
                  </li>
                ))}
              </ul>
            </div>
  
            {/* Customer Service */}
            <div>
              <h3 className="text-lg font-semibold text-white mb-4">Customer Service</h3>
              <ul className="space-y-2">
                {[
                  'My Account',
                  'Order History',
                  'Shipping Policy',
                  'Returns & Refunds',
                  'FAQ'
                ].map((item) => (
                  <li key={item}>
                    <a
                      href="#"
                      className="text-sm hover:text-white hover:underline transition-colors"
                    >
                      {item}
                    </a>
                  </li>
                ))}
              </ul>
            </div>
  
            {/* Newsletter */}
            <div>
              <h3 className="text-lg font-semibold text-white mb-4">Newsletter</h3>
              <p className="text-sm mb-4">
                Subscribe to our newsletter and get 10% off your first purchase
              </p>
              <form className="space-y-2">
                <input
                  type="email"
                  placeholder="Your email address"
                  className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg focus:outline-none focus:border-gray-500 text-sm"
                />
                <button
                  type="submit"
                  className="w-full px-4 py-2 bg-yellow-500 text-gray-900 rounded-lg font-semibold hover:bg-yellow-400 transition-colors text-sm"
                >
                  Subscribe
                </button>
              </form>
            </div>
          </div>
        </div>
  
        {/* Bottom Footer */}
        <div className="border-t border-gray-800">
          <div className="container mx-auto px-4 py-6">
            <div className="flex flex-col md:flex-row justify-between items-center space-y-4 md:space-y-0">
              <p className="text-sm">
                © 2025 BookStore. All rights reserved.
              </p>
              <div className="flex space-x-6">
                <a href="#" className="text-sm hover:text-white hover:underline transition-colors">
                  Privacy Policy
                </a>
                <a href="#" className="text-sm hover:text-white hover:underline transition-colors">
                  Terms of Service
                </a>
                <a href="#" className="text-sm hover:text-white hover:underline transition-colors">
                  Cookie Policy
                </a>
              </div>
            </div>
          </div>
        </div>
      </footer>
    );
  }

export default Footer