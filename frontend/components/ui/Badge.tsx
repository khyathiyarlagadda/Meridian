import React from 'react';

export interface BadgeProps {
  variant?: 'primary' | 'accent' | 'secondary' | 'success' | 'warning' | 'muted';
  children: React.ReactNode;
  className?: string;
}

export const Badge: React.FC<BadgeProps> = ({
  variant = 'primary',
  children,
  className = ''
}) => {
  const variantStyles = {
    primary: "bg-primary text-surface border-transparent",
    accent: "bg-accent/20 text-primary border-accent/40 font-semibold",
    secondary: "bg-secondary text-surface border-transparent",
    success: "bg-success/15 text-success border-success/30 font-semibold",
    warning: "bg-warning/15 text-warning border-warning/30 font-semibold",
    muted: "bg-bg text-muted border-border"
  };

  return (
    <span
      className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-mono tracking-wide border ${variantStyles[variant]} ${className}`}
    >
      {children}
    </span>
  );
};
