import React from 'react';

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  children: React.ReactNode;
}

export const Button: React.FC<ButtonProps> = ({
  variant = 'primary',
  size = 'md',
  className = '',
  children,
  ...props
}) => {
  const baseStyles = "inline-flex items-center justify-center font-bold rounded-xl transition-all duration-150 focus:outline-none disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer";
  
  const variantStyles = {
    primary: "bg-accent text-primary hover:bg-[#e28e4d] shadow-sm shadow-accent/20 border border-accent/40 font-black tracking-tight",
    secondary: "bg-secondary text-surface hover:bg-secondary/90 shadow-sm border border-transparent font-bold",
    ghost: "bg-surface text-primary hover:bg-bg border border-[#E5DDD0] font-semibold"
  };

  const sizeStyles = {
    sm: "px-3.5 py-1.5 text-xs font-semibold",
    md: "px-4.5 py-2.5 text-sm",
    lg: "px-6 py-3.5 text-base font-bold"
  };

  return (
    <button
      className={`${baseStyles} ${variantStyles[variant]} ${sizeStyles[size]} ${className}`}
      {...props}
    >
      {children}
    </button>
  );
};
