import React from 'react';

export interface StatNumberProps {
  label: string;
  value: string | number;
  subtext?: string;
  trend?: string;
  trendPositive?: boolean;
}

export const StatNumber: React.FC<StatNumberProps> = ({
  label,
  value,
  subtext,
  trend,
  trendPositive = true
}) => {
  return (
    <div className="bg-surface border border-[#E5DDD0] rounded-2xl p-5 shadow-sm shadow-primary/5 hover:border-accent/40 transition-all duration-200 space-y-2">
      <div className="flex items-center justify-between">
        <span className="text-[11px] font-bold text-muted uppercase tracking-wider font-mono">
          {label}
        </span>
        {trend && (
          <span
            className={`text-xs font-mono font-bold px-2.5 py-0.5 rounded-full flex items-center space-x-1 ${
              trendPositive ? 'bg-success/10 text-success border border-success/20' : 'bg-warning/10 text-warning border border-warning/20'
            }`}
          >
            <span>{trendPositive ? '▲' : '▼'}</span>
            <span>{trend}</span>
          </span>
        )}
      </div>

      <div className="font-display font-extrabold text-3xl text-accent tracking-tight drop-shadow-xs">
        {value}
      </div>

      {subtext && (
        <p className="text-xs text-muted font-medium leading-relaxed">
          {subtext}
        </p>
      )}
    </div>
  );
};
