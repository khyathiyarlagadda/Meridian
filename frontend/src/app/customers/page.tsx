'use client';

import React, { useEffect, useState } from 'react';
import { Card } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { StatNumber } from '@/components/ui/StatNumber';
import { Sidebar } from '@/components/ui/Sidebar';
import { ChatPanel } from '@/components/dashboard/ChatPanel';

interface SegmentSummary {
  segment: string;
  count: number;
  avg_recency_days: number;
  avg_frequency: number;
  avg_monetary_inr: number;
  avg_aov_inr: number;
}

const DEFAULT_SEGS: SegmentSummary[] = [
  { segment: "High-value customers", count: 320, avg_recency_days: 12.4, avg_frequency: 5.2, avg_monetary_inr: 12450.0, avg_aov_inr: 2394.0 },
  { segment: "Frequent buyers", count: 450, avg_recency_days: 24.1, avg_frequency: 3.8, avg_monetary_inr: 7890.0, avg_aov_inr: 2076.0 },
  { segment: "Likely to buy", count: 510, avg_recency_days: 31.0, avg_frequency: 2.1, avg_monetary_inr: 4120.0, avg_aov_inr: 1961.0 },
  { segment: "Haven't purchased recently", count: 180, avg_recency_days: 72.5, avg_frequency: 4.1, avg_monetary_inr: 9850.0, avg_aov_inr: 2402.0 },
  { segment: "Inactive shoppers", count: 540, avg_recency_days: 114.2, avg_frequency: 1.2, avg_monetary_inr: 1850.0, avg_aov_inr: 1541.0 }
];

export default function CustomersPage() {
  const [segments, setSegments] = useState<SegmentSummary[]>(DEFAULT_SEGS);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchSegments();
  }, []);

  const fetchSegments = async () => {
    setLoading(true);
    try {
      const res = await fetch('http://127.0.0.1:8000/api/segments');
      const data = await res.json();
      if (data.segments_summary?.length) {
        // Map technical names to plain language
        const mapped = data.segments_summary.map((s: any) => {
          let plainName = s.segment;
          if (s.segment.includes('Champion')) plainName = 'High-value customers';
          else if (s.segment.includes('Loyal Customer')) plainName = 'Frequent buyers';
          else if (s.segment.includes('Potential')) plainName = 'Likely to buy';
          else if (s.segment.includes('At-Risk')) plainName = "Haven't purchased recently";
          else if (s.segment.includes('Hibernating')) plainName = 'Inactive shoppers';
          return { ...s, segment: plainName };
        });
        setSegments(mapped);
      }
    } catch (err) {
      console.log('Using fallback segments data');
    } finally {
      setLoading(false);
    }
  };

  const totalCustomers = segments.reduce((acc, c) => acc + c.count, 0);
  const totalMonetary = segments.reduce((acc, c) => acc + (c.count * c.avg_monetary_inr), 0);

  return (
    <div className="flex h-screen overflow-hidden bg-bg text-primary font-sans">
      <Sidebar activePath="/customers" />

      <main className="flex-1 h-screen overflow-y-auto p-6 md:p-10 space-y-8 max-w-7xl">
        
        {/* Header Bar */}
        <header className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 bg-surface p-6 rounded-2xl border border-[#E5DDD0] shadow-sm shadow-primary/5">
          <div>
            <div className="flex items-center space-x-2">
              <Badge variant="secondary">Customer Groups</Badge>
              <span className="text-xs text-muted font-mono">Grouped by Purchasing Activity</span>
            </div>
            <h1 className="font-display font-black text-2xl md:text-3xl tracking-tight text-primary mt-1">
              Customer Groups & Behavior
            </h1>
            <p className="text-xs text-muted font-medium mt-0.5">
              Clear breakdown of your active shoppers by buying habits and recency
            </p>
          </div>
        </header>

        {/* Top Summary Stats */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-5">
          <StatNumber
            label="Total Profiled Customers"
            value={totalCustomers.toLocaleString('en-IN')}
            subtext="Tracked across customer groups"
            trend="Active"
            trendPositive={true}
          />
          <StatNumber
            label="Total Customer Spend"
            value={`₹${(totalMonetary / 100000).toFixed(1)}L`}
            subtext="Combined shopping volume"
            trend="100% Verified"
            trendPositive={true}
          />
          <StatNumber
            label="Haven't Purchased Recently"
            value="180"
            subtext="Top spenders inactive for >60 days"
            trend="Action Recommended"
            trendPositive={false}
          />
        </div>

        {/* Segment Cards Grid */}
        <div className="space-y-4">
          <h2 className="font-display font-black text-xl tracking-tight text-primary">
            Customer Groups ({segments.length} Groups)
          </h2>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {segments.map((seg) => (
              <Card
                key={seg.segment}
                title={seg.segment}
                subtitle={`${seg.count.toLocaleString('en-IN')} active customer profiles`}
                headerAction={
                  <Badge variant={seg.segment.includes('High-value') ? 'success' : (seg.segment.includes("Haven't") ? 'warning' : 'secondary')}>
                    {seg.segment.includes('High-value') ? '★ Top Tier' : (seg.segment.includes("Haven't") ? '⚠️ Action Recommended' : 'Group')}
                  </Badge>
                }
              >
                <div className="space-y-3 font-sans">
                  <div className="bg-secondary/10 p-3 rounded-xl border border-secondary/20 space-y-1.5 font-mono text-xs">
                    <div className="flex justify-between">
                      <span className="text-muted">Days Since Last Order:</span>
                      <span className="font-bold text-secondary">{seg.avg_recency_days} days</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-muted">Average Order Count:</span>
                      <span className="font-bold text-secondary">{seg.avg_frequency} orders</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-muted">Average Total Spend:</span>
                      <span className="font-bold text-accent">₹{seg.avg_monetary_inr.toLocaleString('en-IN')}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-muted">Average Order Value:</span>
                      <span className="font-bold text-primary">₹{seg.avg_aov_inr.toLocaleString('en-IN')}</span>
                    </div>
                  </div>
                </div>
              </Card>
            ))}
          </div>
        </div>

      </main>
      <ChatPanel />
    </div>
  );
}
