import React from 'react'
import { useDispatch } from 'react-redux';
import { register } from '../features/auth/authSlice';

function Register() {
    const [formData, setFormData] = React.useState({
      full_name: '',
      email: '',
      password: '',
      confirmPassword: '',
      address: '',
      contact: '',
      username: '',
    });
    const [errors, setErrors] = React.useState({});
    const dispatch = useDispatch();
    const [loading, setLoading] = React.useState(false);
    const navigate = { push: () => console.log('Navigation would happen here') }; // Simulated for playground
  
    const validateForm = () => {
      const newErrors = {};
  
      if (!formData.fullName.trim()) {
        newErrors.fullName = 'Full name is required';
      }
  
      if (!formData.email) {
        newErrors.email = 'Email is required';
      } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
        newErrors.email = 'Email is invalid';
      }
  
      if (!formData.password) {
        newErrors.password = 'Password is required';
      } else if (formData.password.length < 6) {
        newErrors.password = 'Password must be at least 6 characters';
      }
  
      if (!formData.confirmPassword) {
        newErrors.confirmPassword = 'Please confirm your password';
      } else if (formData.password !== formData.confirmPassword) {
        newErrors.confirmPassword = 'Passwords do not match';
      }
  
      return newErrors;
    };
  
    const handleChange = (e) => {
      const { name, value } = e.target;
      setFormData(prev => ({
        ...prev,
        [name]: value
      }));
      // Clear error when user starts typing
      if (errors[name]) {
        setErrors(prev => ({
          ...prev,
          [name]: ''
        }));
      }
    };
  
    const handleSubmit = async (e) => {
      e.preventDefault();
      const newErrors = validateForm();
  
      if (Object.keys(newErrors).length === 0) {
        setLoading(true);
        try {
          // Simulated API call
          await dispatch(register(formData)).unwrap();
          await new Promise(resolve => setTimeout(resolve, 1000));
          console.log('Registration successful', formData);
          navigate.push('/login');
        } catch (error) {
          setErrors({ submit: 'Registration failed. Please try again.' });
        } finally {
          setLoading(false);
        }
      } else {
        setErrors(newErrors);
      }
    };
  
    return (
      <div className="min-h-screen bg-gray-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
        <div className="sm:mx-auto sm:w-full sm:max-w-md">
          <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
            Create your account
          </h2>
        </div>
  
        <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
          <div className="bg-white py-8 px-4 shadow sm:rounded-lg sm:px-10">
            <form className="space-y-6" onSubmit={handleSubmit}>
              {/* Full Name Field */}
              <div>
                <label htmlFor="fullName" className="block text-sm font-medium text-gray-700">
                  Full Name
                </label>
                <div className="mt-1">
                  <input
                    id="fullName"
                    name="fullName"
                    type="text"
                    value={formData.fullName}
                    onChange={handleChange}
                    className={`appearance-none block w-full px-3 py-2 border ${
                      errors.fullName ? 'border-red-500' : 'border-gray-300'
                    } rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm`}
                  />
                  {errors.fullName && (
                    <p className="mt-2 text-sm text-red-600">{errors.fullName}</p>
                  )}
                </div>
              </div>
  
              {/* Email Field */}
              <div>
                <label htmlFor="email" className="block text-sm font-medium text-gray-700">
                  Email address
                </label>
                <div className="mt-1">
                  <input
                    id="email"
                    name="email"
                    type="email"
                    value={formData.email}
                    onChange={handleChange}
                    className={`appearance-none block w-full px-3 py-2 border ${
                      errors.email ? 'border-red-500' : 'border-gray-300'
                    } rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm`}
                  />
                  {errors.email && (
                    <p className="mt-2 text-sm text-red-600">{errors.email}</p>
                  )}
                </div>
              </div>
  
              {/* Password Field */}
              <div>
                <label htmlFor="password" className="block text-sm font-medium text-gray-700">
                  Password
                </label>
                <div className="mt-1">
                  <input
                    id="password"
                    name="password"
                    type="password"
                    value={formData.password}
                    onChange={handleChange}
                    className={`appearance-none block w-full px-3 py-2 border ${
                      errors.password ? 'border-red-500' : 'border-gray-300'
                    } rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm`}
                  />
                  {errors.password && (
                    <p className="mt-2 text-sm text-red-600">{errors.password}</p>
                  )}
                </div>
              </div>
  
              {/* Confirm Password Field */}
              <div>
                <label htmlFor="confirmPassword" className="block text-sm font-medium text-gray-700">
                  Confirm Password
                </label>
                <div className="mt-1">
                  <input
                    id="confirmPassword"
                    name="confirmPassword"
                    type="password"
                    value={formData.confirmPassword}
                    onChange={handleChange}
                    className={`appearance-none block w-full px-3 py-2 border ${
                      errors.confirmPassword ? 'border-red-500' : 'border-gray-300'
                    } rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm`}
                  />
                  {errors.confirmPassword && (
                    <p className="mt-2 text-sm text-red-600">{errors.confirmPassword}</p>
                  )}
                </div>
              </div>
  
              {/* Submit Button */}
              <div>
                <button
                  type="submit"
                  disabled={loading}
                  className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {loading ? (
                    <div className="flex items-center">
                      <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                      </svg>
                      Creating account...
                    </div>
                  ) : 'Create Account'}
                </button>
              </div>
  
              {/* Error Message */}
              {errors.submit && (
                <div className="mt-4">
                  <p className="text-sm text-red-600">{errors.submit}</p>
                </div>
              )}
            </form>
  
            {/* Sign in link */}
            <div className="mt-6">
              <div className="relative">
                <div className="absolute inset-0 flex items-center">
                  <div className="w-full border-t border-gray-300" />
                </div>
                <div className="relative flex justify-center text-sm">
                  <span className="px-2 bg-white text-gray-500">
                    Already have an account?
                  </span>
                </div>
              </div>
  
              <div className="mt-6">
                <button
                  onClick={() => navigate.push('/login')}
                  className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-gray-700 bg-gray-50 hover:bg-gray-100"
                >
                  Sign in
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

export default Register