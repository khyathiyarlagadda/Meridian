import React from 'react';
import Link from 'next/link';

export interface NavItem {
  label: string;
  href: string;
  icon?: string;
}

export interface SidebarProps {
  activePath?: string;
}

const PRIMARY_NAV_ITEMS: NavItem[] = [
  { label: 'Overview', href: '/', icon: '📊' },
  { label: 'Opportunities', href: '/opportunities', icon: '💡' },
  { label: 'Customers', href: '/customers', icon: '👥' },
  { label: 'Products', href: '/products', icon: '📦' },
  { label: 'Campaigns', href: '/campaigns', icon: '🎯' },
  { label: 'Experiments', href: '/experiments', icon: '🧪' },
  { label: 'Activity', href: '/ai-activity', icon: '⚡' },
];

const UTILITY_NAV_ITEMS: NavItem[] = [
  { label: 'Settings', href: '/settings', icon: '⚙️' },
];

export const Sidebar: React.FC<SidebarProps> = ({ activePath = '/' }) => {
  return (
    <aside className="w-64 bg-primary text-bg h-screen sticky top-0 p-6 flex flex-col justify-between hidden md:flex border-r border-[#4A3228] shadow-lg shrink-0 overflow-y-auto">
      <div className="space-y-6">
        {/* Brand Header */}
        <div className="flex items-center space-x-3 pb-2 border-b border-[#4A3228]">
          <div className="w-10 h-10 rounded-xl bg-[#FDFBF7] p-1 border border-[#E5DDD0] flex items-center justify-center shadow-md overflow-hidden shrink-0">
            <img src="/meridian-logo.svg" alt="Meridian Logo" className="w-full h-full object-contain" />
          </div>
          <div>
            <div className="font-display font-extrabold text-xl text-bg tracking-tight leading-tight">
              Meridian
            </div>
            <div className="text-[10px] text-accent font-mono uppercase tracking-widest font-bold">
              Find your next move.
            </div>
          </div>
        </div>

        {/* Commercial Operations Section */}
        <nav className="space-y-1">
          <div className="text-[10px] font-bold text-bg/50 uppercase tracking-widest px-3 mb-2 font-mono">
            Commercial Operations
          </div>
          {PRIMARY_NAV_ITEMS.map((item) => {
            const isActive = activePath === item.href;
            return (
              <Link
                key={item.label}
                href={item.href}
                className={`flex items-center justify-between px-3.5 py-2.5 rounded-xl text-sm font-semibold transition-all duration-150 ${
                  isActive
                    ? 'bg-accent text-primary font-bold shadow-md shadow-accent/20 scale-[1.02]'
                    : 'text-bg/75 hover:text-bg hover:bg-bg/10'
                }`}
              >
                <span className="flex items-center space-x-2.5">
                  <span className="text-base">{item.icon}</span>
                  <span>{item.label}</span>
                </span>
              </Link>
            );
          })}
        </nav>

        {/* System Settings Divider & Utility Section */}
        <div className="pt-4 border-t border-[#4A3228] space-y-1">
          <div className="text-[10px] font-bold text-bg/50 uppercase tracking-widest px-3 mb-2 font-mono">
            System & Governance
          </div>
          {UTILITY_NAV_ITEMS.map((item) => {
            const isActive = activePath === item.href;
            return (
              <Link
                key={item.label}
                href={item.href}
                className={`flex items-center justify-between px-3.5 py-2.5 rounded-xl text-sm font-semibold transition-all duration-150 ${
                  isActive
                    ? 'bg-accent text-primary font-bold shadow-md shadow-accent/20 scale-[1.02]'
                    : 'text-bg/75 hover:text-bg hover:bg-bg/10'
                }`}
              >
                <span className="flex items-center space-x-2.5">
                  <span className="text-base">{item.icon}</span>
                  <span>{item.label}</span>
                </span>
              </Link>
            );
          })}
        </div>
      </div>

      {/* Footer Merchant Info */}
      <div className="pt-6 border-t border-[#4A3228] space-y-2">
        <div className="flex items-center space-x-2">
          <div className="w-2.5 h-2.5 rounded-full bg-success ring-2 ring-success/30 animate-pulse" />
          <span className="text-xs font-bold text-bg tracking-wide">NOVA Merchant Active</span>
        </div>
        <div className="text-[10px] text-bg/50 font-mono">
          Environment: Windows Sandbox
        </div>
      </div>
    </aside>
  );
};
