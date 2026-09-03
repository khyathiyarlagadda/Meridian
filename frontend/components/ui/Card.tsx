import React from 'react';

export interface CardProps {
  title?: string;
  subtitle?: string;
  headerAction?: React.ReactNode;
  children: React.ReactNode;
  className?: string;
  isHighlighted?: boolean;
}

export const Card: React.FC<CardProps> = ({
  title,
  subtitle,
  headerAction,
  children,
  className = '',
  isHighlighted = false,
}) => {
  return (
    <div
      className={`bg-surface border rounded-2xl p-5 transition-all duration-200 ${
        isHighlighted
          ? 'border-2 border-accent shadow-md shadow-accent/15 ring-2 ring-accent/20'
          : 'border-[#E5DDD0] shadow-sm shadow-primary/5 hover:shadow-md hover:shadow-primary/10 hover:border-accent/40'
      } ${className}`}
    >
      {(title || headerAction) && (
        <div className="flex items-start justify-between border-b border-[#E5DDD0] pb-3 mb-4">
          <div className="pr-2">
            {title && (
              <h3 className="font-display font-black text-xl text-primary tracking-tight leading-snug">
                {title}
              </h3>
            )}
            {subtitle && (
              <p className="text-xs text-muted font-medium mt-0.5 leading-relaxed">{subtitle}</p>
            )}
          </div>
          {headerAction && <div className="shrink-0">{headerAction}</div>}
        </div>
      )}
      {children}
    </div>
  );
};
