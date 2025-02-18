const Button = ({ children, variant = 'primary', ...props }) => {
    return (
      <button 
        className={`btn ${variant === 'primary' ? 'btn-primary' : 'bg-gray-200 hover:bg-gray-300'}`}
        {...props}
      >
        {children}
      </button>
    );
  };
  
  export default Button;