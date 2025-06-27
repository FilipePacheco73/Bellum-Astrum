import React from 'react';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary';
  children: React.ReactNode;
  className?: string;
}

const base =
  'w-full rounded-xl font-bold transition-all duration-200 shadow-lg drop-shadow-md';

const variants = {
  primary:
    'py-2 sm:py-2.5 bg-gradient-to-tr from-blue-700 via-blue-500 to-cyan-400 hover:from-blue-600 hover:to-cyan-300 text-white text-base border-none ring-1 ring-blue-400/40 hover:ring-2 hover:ring-blue-300/60 focus:ring-2 focus:ring-blue-400/80',
  secondary:
    'py-2 text-blue-300 hover:text-blue-100 text-sm underline underline-offset-2 bg-transparent border-none',
};

const Button: React.FC<ButtonProps> = ({ variant = 'primary', children, className = '', ...props }) => (
  <button
    className={`${base} ${variants[variant]} ${className}`.trim()}
    {...props}
  >
    {children}
  </button>
);

export default Button;
