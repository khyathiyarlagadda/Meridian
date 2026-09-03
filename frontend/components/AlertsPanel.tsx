'use client';

import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import { Badge } from '@/components/ui/Badge';
import { Button } from '@/components/ui/Button';

export interface OpportunityAlert {
  id: string;
  timestamp: string;
  type: string;
  severity: 'HIGH' | 'MEDIUM' | 'LOW';
  title: string;
  description: string;
  target_url: string;
  opportunity_id?: string;
}

export const AlertsPanel: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [alerts, setAlerts] = useState<OpportunityAlert[]>([]);
  const [loading, setLoading] = useState(false);
  const [refreshing, setRefreshing] = useState(false);

  useEffect(() => {
    fetchAlerts();
  }, []);

  const fetchAlerts = async () => {
    setLoading(true);
    try {
      const res = await fetch('http://127.0.0.1:8000/api/alerts');
      if (res.ok) {
        const data = await res.json();
        if (data.alerts) setAlerts(data.alerts);
      }
    } catch (err) {
      console.log('Using default fallback alerts state');
    } finally {
      setLoading(false);
    }
  };

  const handleRunPipelineRefresh = async () => {
    setRefreshing(true);
    try {
      const res = await fetch('http://127.0.0.1:8000/api/alerts/refresh', {
        method: 'POST',
      });
      if (res.ok) {
        const data = await res.json();
        if (data.alerts) {
          setAlerts(data.alerts);
        }
      }
    } catch (err) {
      console.error('Error refreshing alerts pipeline:', err);
    } finally {
      setRefreshing(false);
    }
  };

  return (
    <>
      {/* Header Bell Trigger Button */}
      <button
        onClick={() => setIsOpen(true)}
        className="relative flex items-center space-x-2 bg-surface hover:bg-bg border border-[#E5DDD0] px-3.5 py-2 rounded-xl text-xs font-bold text-primary shadow-sm transition cursor-pointer"
        title="Opportunity Alerts & Notifications"
      >
        <span className="text-base">🔔</span>
        <span className="font-display">Alerts</span>
        {alerts.length > 0 && (
          <span className="bg-accent text-primary font-mono text-[10px] font-black px-1.5 py-0.5 rounded-full shadow-sm">
            {alerts.length}
          </span>
        )}
      </button>

      {/* Slide-Over Drawer Overlay */}
      {isOpen && (
        <div className="fixed inset-0 z-50 flex justify-end bg-primary/40 backdrop-blur-xs transition-opacity">
          <div className="bg-surface border-l border-[#E5DDD0] w-full max-w-md h-full shadow-2xl flex flex-col justify-between font-sans">
            
            {/* Drawer Header */}
            <div className="p-5 border-b border-[#E5DDD0] bg-bg flex items-center justify-between">
              <div>
                <div className="flex items-center space-x-2">
                  <Badge variant="accent">Opportunity Alerts</Badge>
                  <span className="text-[10px] font-mono text-muted">Real-Time Signal Pipeline</span>
                </div>
                <h2 className="font-display font-black text-xl text-primary mt-1">
                  Alert Notifications ({alerts.length})
                </h2>
              </div>
              <button
                onClick={() => setIsOpen(false)}
                className="text-muted hover:text-primary font-bold text-xl p-1 cursor-pointer"
              >
                ✕
              </button>
            </div>

            {/* Controls Bar */}
            <div className="p-4 bg-surface border-b border-[#E5DDD0] flex items-center justify-between">
              <span className="text-xs text-muted font-mono font-bold">Detection Pipeline Status</span>
              <Button
                variant="primary"
                size="sm"
                onClick={handleRunPipelineRefresh}
                disabled={refreshing}
              >
                {refreshing ? '⚡ Re-Running Pipeline...' : '⚡ Re-Run Detection Pipeline'}
              </Button>
            </div>

            {/* Alert Cards Feed */}
            <div className="flex-1 p-5 overflow-y-auto space-y-4">
              {loading && alerts.length === 0 && (
                <div className="text-xs text-muted font-mono animate-pulse">
                  Fetching opportunity alerts...
                </div>
              )}

              {alerts.map((alert) => (
                <div
                  key={alert.id}
                  className="bg-bg p-4 rounded-2xl border border-[#E5DDD0] space-y-2.5 shadow-sm hover:border-accent/40 transition"
                >
                  <div className="flex items-center justify-between">
                    <Badge variant={alert.severity === 'HIGH' ? 'accent' : 'secondary'}>
                      {alert.severity} • {alert.type.replace(/_/g, ' ')}
                    </Badge>
                    <span className="text-[10px] font-mono text-muted">{alert.timestamp}</span>
                  </div>

                  <h3 className="font-display font-bold text-sm text-primary leading-snug">
                    {alert.title}
                  </h3>

                  <p className="text-xs text-muted leading-relaxed">
                    {alert.description}
                  </p>

                  <div className="pt-1 flex justify-end">
                    <Link
                      href={alert.target_url}
                      onClick={() => setIsOpen(false)}
                      className="text-xs font-mono font-bold text-accent hover:underline flex items-center space-x-1"
                    >
                      <span>Review Opportunity & Campaign →</span>
                    </Link>
                  </div>
                </div>
              ))}
            </div>

            {/* Drawer Footer */}
            <div className="p-4 border-t border-[#E5DDD0] bg-bg flex items-center justify-between text-xs text-muted font-mono">
              <span>NOVA Signal Pipeline: Active</span>
              <button
                onClick={fetchAlerts}
                className="text-accent hover:underline font-bold"
              >
                🔄 Refresh Feed
              </button>
            </div>

          </div>
        </div>
      )}
    </>
  );
};
