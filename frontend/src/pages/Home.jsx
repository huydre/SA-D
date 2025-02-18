// src/pages/Home.jsx
import { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { Link } from 'react-router-dom';
import { fetchBooks, selectAllBooks } from '../features/books/booksSlice';
import { FaBook, FaShoppingCart, FaStar, FaArrowRight, FaTruck, FaHeadset } from 'react-icons/fa';

// Import images
import heroImage from '../assets/hero-books.jpg';
import bookBg from '../assets/book-bg.jpg';

const Home = () => {
  const dispatch = useDispatch();
  const books = useSelector(selectAllBooks);

  useEffect(() => {
    dispatch(fetchBooks({ page: 1 }));
  }, [dispatch]);

  return (
    <div className="min-h-screen">
      {/* Hero Section with Background Image */}
      <section 
        className="relative min-h-[600px] flex items-center"
        style={{
          backgroundImage: `linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)), url(${heroImage})`,
          backgroundSize: 'cover',
          backgroundPosition: 'center',
        }}
      >
        <div className="container mx-auto px-4">
          <div className="max-w-2xl text-white">
            <h1 className="text-5xl font-bold mb-6 leading-tight animate-fade-in">
              Discover Your Next
              <span className="text-yellow-400"> Favorite Book</span>
            </h1>
            <p className="text-xl mb-8 text-gray-300">
              Explore our vast collection of books across all genres.
              From bestsellers to rare finds, we have something for everyone.
            </p>
            <div className="flex gap-4">
              <Link 
                to="/books" 
                className="bg-yellow-400 text-gray-900 px-8 py-4 rounded-full font-semibold hover:bg-yellow-300 transition duration-300 transform hover:scale-105"
              >
                Explore Books
              </Link>
              <Link 
                to="/register" 
                className="border-2 border-white text-white px-8 py-4 rounded-full font-semibold hover:bg-white hover:text-gray-900 transition duration-300 transform hover:scale-105"
              >
                Join Now
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 bg-white">
        <div className="container mx-auto px-4">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-12">
            <div className="text-center group">
              <div className="w-20 h-20 mx-auto mb-6 bg-purple-100 rounded-full flex items-center justify-center group-hover:bg-purple-200 transition duration-300">
                <FaBook className="text-3xl text-purple-600" />
              </div>
              <h3 className="text-xl font-semibold mb-4">Vast Collection</h3>
              <p className="text-gray-600">
                Access thousands of books across multiple genres and categories
              </p>
            </div>
            <div className="text-center group">
              <div className="w-20 h-20 mx-auto mb-6 bg-blue-100 rounded-full flex items-center justify-center group-hover:bg-blue-200 transition duration-300">
                <FaTruck className="text-3xl text-blue-600" />
              </div>
              <h3 className="text-xl font-semibold mb-4">Fast Delivery</h3>
              <p className="text-gray-600">
                Get your books delivered right to your doorstep
              </p>
            </div>
            <div className="text-center group">
              <div className="w-20 h-20 mx-auto mb-6 bg-green-100 rounded-full flex items-center justify-center group-hover:bg-green-200 transition duration-300">
                <FaHeadset className="text-3xl text-green-600" />
              </div>
              <h3 className="text-xl font-semibold mb-4">24/7 Support</h3>
              <p className="text-gray-600">
                Our customer service team is always here to help
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Featured Books Section */}
      <section className="py-20 bg-gray-50">
        <div className="container mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold mb-4">Featured Books</h2>
            <p className="text-gray-600 max-w-2xl mx-auto">
              Discover our hand-picked selection of must-read books
            </p>
          </div>
          
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8">
            {books.slice(0, 4).map((book) => (
              <div key={book.id} className="bg-white rounded-xl shadow-lg overflow-hidden transform hover:-translate-y-2 transition duration-300">
                <div className="relative">
                  <img 
                    src={book.cover_image || bookBg} 
                    alt={book.title}
                    className="w-full h-64 object-cover"
                  />
                  <div className="absolute top-0 right-0 bg-yellow-400 text-gray-900 px-4 py-2 rounded-bl-xl font-semibold">
                    ${book.price}
                  </div>
                </div>
                <div className="p-6">
                  <h3 className="font-semibold text-xl mb-2">{book.title}</h3>
                  <p className="text-gray-600 mb-4">{book.author}</p>
                  <div className="flex items-center justify-between">
                    <div className="flex text-yellow-400">
                      {[...Array(5)].map((_, i) => (
                        <FaStar key={i} />
                      ))}
                    </div>
                    <button className="bg-purple-600 text-white px-6 py-2 rounded-full hover:bg-purple-700 transition duration-300">
                      Add to Cart
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Newsletter Section */}
      <section 
        className="py-20 bg-purple-700 text-white"
        style={{
          backgroundImage: 'linear-gradient(rgba(91, 33, 182, 0.9), rgba(91, 33, 182, 0.9)), url(/newsletter-bg.jpg)',
          backgroundSize: 'cover',
          backgroundPosition: 'center',
        }}
      >
        <div className="container mx-auto px-4">
          <div className="max-w-2xl mx-auto text-center">
            <h2 className="text-4xl font-bold mb-4">
              Stay Updated
            </h2>
            <p className="text-xl mb-8 text-purple-200">
              Subscribe to our newsletter for the latest releases and exclusive offers
            </p>
            <form className="flex gap-4 max-w-md mx-auto">
              <input
                type="email"
                placeholder="Enter your email"
                className="flex-1 px-6 py-4 rounded-full focus:outline-none focus:ring-2 focus:ring-yellow-400 text-gray-900"
              />
              <button 
                type="submit"
                className="bg-yellow-400 text-gray-900 px-8 py-4 rounded-full font-semibold hover:bg-yellow-300 transition duration-300"
              >
                Subscribe
              </button>
            </form>
          </div>
        </div>
      </section>

      {/* Testimonials */}
      <section className="py-20 bg-white">
        <div className="container mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold mb-4">What Readers Say</h2>
            <p className="text-gray-600 max-w-2xl mx-auto">
              Don't just take our word for it
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {testimonials.map((testimonial, index) => (
              <div key={index} className="bg-gray-50 p-8 rounded-xl">
                <div className="flex items-center mb-6">
                  <img
                    src={testimonial.avatar}
                    alt={testimonial.name}
                    className="w-16 h-16 rounded-full object-cover mr-4"
                  />
                  <div>
                    <h4 className="font-semibold text-lg">{testimonial.name}</h4>
                    <div className="flex text-yellow-400">
                      {[...Array(5)].map((_, i) => (
                        <FaStar key={i} className="text-sm" />
                      ))}
                    </div>
                  </div>
                </div>
                <p className="text-gray-600 italic">"{testimonial.comment}"</p>
              </div>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
};

const testimonials = [
  {
    name: "Sarah Johnson",
    avatar: "https://randomuser.me/api/portraits/women/1.jpg",
    comment: "Amazing selection of books! The delivery was quick and the prices are very competitive."
  },
  {
    name: "Michael Chen",
    avatar: "https://randomuser.me/api/portraits/men/2.jpg",
    comment: "I love how easy it is to find and purchase books. The recommendations are always spot on!"
  },
  {
    name: "Emily Davis",
    avatar: "https://randomuser.me/api/portraits/women/3.jpg",
    comment: "The best online bookstore I've used. Great customer service and a wonderful collection."
  }
];

export default Home;