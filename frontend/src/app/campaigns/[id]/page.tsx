'use client';

import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import { useParams } from 'next/navigation';
import { Card } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { Button } from '@/components/ui/Button';
import { Sidebar } from '@/components/ui/Sidebar';
import { ChatPanel } from '@/components/dashboard/ChatPanel';

interface CampaignDetail {
  id: string;
  title: string;
  strategy: string;
  target_audience: string;
  expected: {
    customers_reached: number;
    orders: number;
    revenue_inr: number;
    roi_multiple: number;
  };
  actual: {
    customers_reached: number;
    orders: number;
    revenue_inr: number;
    roi_multiple: number;
  };
}

const DEFAULT_DETAILS: Record<string, CampaignDetail> = {
  CAMP_OPP_EARBUD_CROSSSELL: {
    id: "CAMP_OPP_EARBUD_CROSSSELL",
    title: "Nova Pods Companion Case Discount",
    strategy: "cross-sell",
    target_audience: "Earbud buyers within 7 days of purchase",
    expected: {
      customers_reached: 312,
      orders: 45,
      revenue_inr: 14200,
      roi_multiple: 5.7
    },
    actual: {
      customers_reached: 312,
      orders: 51,
      revenue_inr: 16430,
      roi_multiple: 6.2
    }
  },
  CAMP_OPP_WINBACK_COHORT: {
    id: "CAMP_OPP_WINBACK_COHORT",
    title: "Welcome Back to Nova: Exclusive Voucher",
    strategy: "win-back campaign",
    target_audience: "Lapsed active customers inactive for >60 days",
    expected: {
      customers_reached: 180,
      orders: 28,
      revenue_inr: 45000,
      roi_multiple: 2.0
    },
    actual: {
      customers_reached: 180,
      orders: 26,
      revenue_inr: 42000,
      roi_multiple: 1.8
    }
  },
  CAMP_OPP_CASE_SCREEN_BUNDLE: {
    id: "CAMP_OPP_CASE_SCREEN_BUNDLE",
    title: "Essential Protection Kit Bundle (Case + Screen Glass)",
    strategy: "bundle",
    target_audience: "Multi-item shoppers interested in phone protection",
    expected: {
      customers_reached: 2463,
      orders: 75,
      revenue_inr: 95000,
      roi_multiple: 2.8
    },
    actual: {
      customers_reached: 2463,
      orders: 82,
      revenue_inr: 105000,
      roi_multiple: 3.2
    }
  }
};

export default function CampaignDetailPage() {
  const params = useParams();
  const rawId = params?.id as string || 'CAMP_OPP_EARBUD_CROSSSELL';
  
  const detail = DEFAULT_DETAILS[rawId] || DEFAULT_DETAILS['CAMP_OPP_EARBUD_CROSSSELL'];

  const { expected, actual } = detail;
  const isBetterThanExpected = actual.roi_multiple >= expected.roi_multiple;
  const summarySentence = isBetterThanExpected
    ? "This campaign performed better than expected."
    : "This campaign performed below expectations.";

  return (
    <div className="flex h-screen overflow-hidden bg-bg text-primary font-sans">
      <Sidebar activePath="/campaigns" />

      <main className="flex-1 h-screen overflow-y-auto p-6 md:p-10 space-y-8 max-w-4xl">
        
        {/* Navigation Breadcrumb */}
        <div className="flex items-center justify-between">
          <Link href="/campaigns" className="text-xs font-mono font-bold text-accent hover:underline flex items-center space-x-1">
            <span>← Back to Campaigns</span>
          </Link>
          <Badge variant="secondary">Campaign Results</Badge>
        </div>

        {/* Header Bar */}
        <header className="bg-surface p-6 rounded-2xl border border-[#E5DDD0] shadow-sm shadow-primary/5 space-y-2">
          <Badge variant="accent">{detail.strategy.toUpperCase()}</Badge>
          <h1 className="font-display font-black text-2xl md:text-3xl tracking-tight text-primary">
            {detail.title}
          </h1>
          <p className="text-xs text-muted font-medium">
            Target Audience: {detail.target_audience}
          </p>
        </header>

        {/* Offer is Ready for Checkout Banner */}
        <div className="bg-surface p-6 rounded-2xl border-2 border-accent/40 shadow-sm flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
          <div className="space-y-1">
            <div className="flex items-center space-x-2">
              <span className="w-2.5 h-2.5 rounded-full bg-success animate-pulse" />
              <h2 className="font-display font-black text-lg text-primary">Offer is ready for checkout</h2>
            </div>
            <p className="text-xs text-muted font-medium">
              This campaign is active and customer checkout via Razorpay is enabled.
            </p>
          </div>

          <Link href={`/checkout?campaign_id=${detail.id}`}>
            <Button variant="primary" size="md" className="font-bold">
              🛒 Preview Customer Checkout →
            </Button>
          </Link>
        </div>

        {/* Campaign Results Table */}
        <div className="bg-surface p-6 rounded-2xl border border-[#E5DDD0] shadow-sm space-y-6">
          <div className="flex items-center justify-between border-b border-[#E5DDD0] pb-4">
            <h2 className="font-display font-black text-xl text-primary">
              Campaign Results
            </h2>
            <span className="text-xs font-mono font-bold text-muted uppercase">Expected vs Actual</span>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse text-sm">
              <thead>
                <tr className="bg-secondary text-surface font-mono text-xs uppercase tracking-wider">
                  <th className="p-4 font-bold">Metric</th>
                  <th className="p-4 font-bold text-right">Expected</th>
                  <th className="p-4 font-bold text-right">Actual</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[#E5DDD0] font-sans">
                <tr className="hover:bg-bg/50">
                  <td className="p-4 font-bold text-primary">Customers reached</td>
                  <td className="p-4 font-mono text-right text-muted">{expected.customers_reached.toLocaleString('en-IN')}</td>
                  <td className="p-4 font-mono text-right font-bold text-primary">{actual.customers_reached.toLocaleString('en-IN')}</td>
                </tr>

                <tr className="hover:bg-bg/50">
                  <td className="p-4 font-bold text-primary">Orders</td>
                  <td className="p-4 font-mono text-right text-muted">{expected.orders}</td>
                  <td className="p-4 font-mono text-right font-bold text-primary">{actual.orders}</td>
                </tr>

                <tr className="hover:bg-bg/50">
                  <td className="p-4 font-bold text-primary">Revenue</td>
                  <td className="p-4 font-mono text-right text-muted">₹{expected.revenue_inr.toLocaleString('en-IN')}</td>
                  <td className="p-4 font-mono text-right font-bold text-success">₹{actual.revenue_inr.toLocaleString('en-IN')}</td>
                </tr>

                <tr className="hover:bg-bg/50">
                  <td className="p-4 font-bold text-primary">ROI</td>
                  <td className="p-4 font-mono text-right text-muted">{expected.roi_multiple.toFixed(1)}×</td>
                  <td className="p-4 font-mono text-right font-bold text-accent">{actual.roi_multiple.toFixed(1)}×</td>
                </tr>
              </tbody>
            </table>
          </div>

          {/* Plain Summary Sentence Banner */}
          <div className={`p-4 rounded-xl border text-sm font-bold flex items-center space-x-3 ${
            isBetterThanExpected ? 'bg-success/15 border-success/40 text-success' : 'bg-warning/15 border-warning/40 text-warning'
          }`}>
            <span className="text-xl">{isBetterThanExpected ? '📈' : '📉'}</span>
            <span>{summarySentence}</span>
          </div>
        </div>

      </main>
      <ChatPanel />
    </div>
  );
}
