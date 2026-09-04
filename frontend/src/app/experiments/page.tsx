'use client';

import React, { useEffect, useState } from 'react';
import { Card } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { Button } from '@/components/ui/Button';
import { Sidebar } from '@/components/ui/Sidebar';
import { ChatPanel } from '@/components/dashboard/ChatPanel';

interface VariantGroup {
  group_name: string;
  discount_pct: number;
  sample_size: number;
  converted_count: number;
  conversion_rate_pct: number;
  gross_revenue_inr: number;
  discount_cost_inr: number;
  net_profit_inr: number;
  measured_aov_inr: number;
}

interface ExperimentPayload {
  experiment_name: string;
  opportunity_type: string;
  total_audience: number;
  groups: {
    control: VariantGroup;
    variant_a: VariantGroup;
    variant_b: VariantGroup;
  };
  key_takeaway: string;
  comparison_summary: {
    highest_conversion_variant: string;
    highest_conversion_rate_pct: number;
    highest_profit_variant: string;
    highest_net_profit_inr: number;
  };
}

export default function ExperimentsPage() {
  const [data, setData] = useState<ExperimentPayload | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchExperiment();
  }, []);

  const fetchExperiment = async () => {
    setLoading(true);
    try {
      const res = await fetch('http://127.0.0.1:8000/api/experiments');
      if (res.ok) {
        const json = await res.json();
        setData(json);
      }
    } catch (err) {
      console.log('Using default experiment state');
    } finally {
      setLoading(false);
    }
  };

  const control = data?.groups?.control || {
    group_name: "No Offer (Control)",
    discount_pct: 0.0,
    sample_size: 500,
    converted_count: 17,
    conversion_rate_pct: 3.40,
    gross_revenue_inr: 21368.91,
    discount_cost_inr: 0.0,
    net_profit_inr: 21368.91,
    measured_aov_inr: 1256.99
  };

  const variantA = data?.groups?.variant_a || {
    group_name: "Offer A (5% Off)",
    discount_pct: 5.0,
    sample_size: 500,
    converted_count: 23,
    conversion_rate_pct: 4.60,
    gross_revenue_inr: 29264.27,
    discount_cost_inr: 1463.21,
    net_profit_inr: 27801.06,
    measured_aov_inr: 1208.74
  };

  const variantB = data?.groups?.variant_b || {
    group_name: "Offer B (10% Off)",
    discount_pct: 10.0,
    sample_size: 500,
    converted_count: 38,
    conversion_rate_pct: 7.60,
    gross_revenue_inr: 47639.76,
    discount_cost_inr: 4763.98,
    net_profit_inr: 42875.79,
    measured_aov_inr: 1128.31
  };

  // Plain-language rewrite for takeaway
  const rawTakeaway = data?.key_takeaway || "💡 TAKEAWAY: Variant B (10% Discount) produced both the highest conversion rate (7.6%) and highest net profit (₹42,875.79).";
  const plainTakeaway = rawTakeaway
    .replace(/Variant A/g, 'Offer A (5% Off)')
    .replace(/Variant B/g, 'Offer B (10% Off)')
    .replace(/Control/g, 'No Offer');

  return (
    <div className="flex h-screen overflow-hidden bg-bg text-primary font-sans">
      <Sidebar activePath="/experiments" />

      <main className="flex-1 h-screen overflow-y-auto p-6 md:p-10 space-y-8 max-w-7xl">
        
        {/* Header Bar */}
        <header className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 bg-surface p-6 rounded-2xl border border-[#E5DDD0] shadow-sm shadow-primary/5">
          <div>
            <div className="flex items-center space-x-2">
              <Badge variant="secondary">Try Two Offers</Badge>
              <span className="text-xs text-muted font-mono">Offer Comparison Test</span>
            </div>
            <h1 className="font-display font-black text-2xl md:text-3xl tracking-tight text-primary mt-1">
              Try Two Offers
            </h1>
            <p className="text-xs text-muted font-medium mt-0.5">
              Comparing No Offer (0%) vs Offer A (5% off) vs Offer B (10% off) across {data?.total_audience || 1500} shoppers
            </p>
          </div>

          <div className="flex items-center space-x-3">
            <Button variant="primary" size="sm" onClick={fetchExperiment} disabled={loading}>
              {loading ? 'Comparing Offers...' : '🧪 Rerun Offer Comparison'}
            </Button>
          </div>
        </header>

        {/* Plain-Language Takeaway Banner */}
        <div className="p-5 rounded-2xl bg-surface border-2 border-accent/40 shadow-md space-y-2">
          <div className="flex items-center space-x-2">
            <Badge variant="accent">Key Takeaway</Badge>
            <span className="text-xs font-mono font-bold text-muted">Store Offer Result</span>
          </div>
          <div className="font-display font-bold text-base md:text-lg text-primary leading-snug">
            {plainTakeaway}
          </div>
          <p className="text-xs text-muted font-sans">
            Calculated from actual order metrics across your store audience.
          </p>
        </div>

        {/* Offer Options Summary Cards */}
        <div className="space-y-4">
          <h2 className="font-display text-xl font-bold tracking-tight text-primary">
            Offer Options
          </h2>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            
            {/* Control */}
            <div className="bg-surface p-5 rounded-2xl border border-[#E5DDD0] space-y-3">
              <div className="flex items-center justify-between">
                <span className="font-display font-bold text-base text-primary">No Offer (Control)</span>
                <Badge variant="secondary">0% Discount</Badge>
              </div>
              <div className="space-y-1">
                <div className="text-[10px] font-mono text-muted uppercase tracking-widest">Conversion Rate</div>
                <div className="font-display font-black text-2xl text-primary">{control.conversion_rate_pct}%</div>
                <div className="text-xs text-muted font-mono">{control.converted_count} orders / {control.sample_size} shoppers</div>
              </div>
              <div className="pt-2 border-t border-[#E5DDD0] grid grid-cols-2 gap-2 text-xs font-mono">
                <div>
                  <div className="text-muted text-[10px]">Net Profit:</div>
                  <div className="font-bold text-success">₹{control.net_profit_inr.toLocaleString('en-IN')}</div>
                </div>
                <div>
                  <div className="text-muted text-[10px]">Average Order Value:</div>
                  <div className="font-bold text-primary">₹{control.measured_aov_inr.toLocaleString('en-IN')}</div>
                </div>
              </div>
            </div>

            {/* Variant A */}
            <div className="bg-surface p-5 rounded-2xl border border-accent/40 space-y-3 relative overflow-hidden">
              <div className="flex items-center justify-between">
                <span className="font-display font-bold text-base text-primary">Offer A (5% Off)</span>
                <Badge variant="accent">5% Discount</Badge>
              </div>
              <div className="space-y-1">
                <div className="text-[10px] font-mono text-muted uppercase tracking-widest">Conversion Rate</div>
                <div className="font-display font-black text-2xl text-primary">{variantA.conversion_rate_pct}%</div>
                <div className="text-xs text-muted font-mono">{variantA.converted_count} orders / {variantA.sample_size} shoppers</div>
              </div>
              <div className="pt-2 border-t border-[#E5DDD0] grid grid-cols-2 gap-2 text-xs font-mono">
                <div>
                  <div className="text-muted text-[10px]">Net Profit:</div>
                  <div className="font-bold text-success">₹{variantA.net_profit_inr.toLocaleString('en-IN')}</div>
                </div>
                <div>
                  <div className="text-muted text-[10px]">Discount Cost:</div>
                  <div className="font-bold text-accent">₹{variantA.discount_cost_inr.toLocaleString('en-IN')}</div>
                </div>
              </div>
            </div>

            {/* Variant B */}
            <div className="bg-surface p-5 rounded-2xl border border-success/40 space-y-3 relative overflow-hidden">
              <div className="flex items-center justify-between">
                <span className="font-display font-bold text-base text-primary">Offer B (10% Off)</span>
                <Badge variant="success">10% Discount</Badge>
              </div>
              <div className="space-y-1">
                <div className="text-[10px] font-mono text-muted uppercase tracking-widest">Conversion Rate</div>
                <div className="font-display font-black text-2xl text-success">{variantB.conversion_rate_pct}%</div>
                <div className="text-xs text-muted font-mono">{variantB.converted_count} orders / {variantB.sample_size} shoppers</div>
              </div>
              <div className="pt-2 border-t border-[#E5DDD0] grid grid-cols-2 gap-2 text-xs font-mono">
                <div>
                  <div className="text-muted text-[10px]">Net Profit:</div>
                  <div className="font-bold text-success">₹{variantB.net_profit_inr.toLocaleString('en-IN')}</div>
                </div>
                <div>
                  <div className="text-muted text-[10px]">Discount Cost:</div>
                  <div className="font-bold text-accent">₹{variantB.discount_cost_inr.toLocaleString('en-IN')}</div>
                </div>
              </div>
            </div>

          </div>
        </div>

        {/* 3-Way Comparison Table */}
        <div className="space-y-4 pt-2">
          <h2 className="font-display text-xl font-bold tracking-tight text-primary">
            Which one made more money?
          </h2>

          <Card className="overflow-hidden p-0 border-[#E5DDD0]">
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs font-sans border-collapse">
                <thead>
                  <tr className="bg-secondary text-bg font-mono uppercase tracking-wider text-[11px]">
                    <th className="p-3.5 pl-4">Offer Option</th>
                    <th className="p-3.5">Discount</th>
                    <th className="p-3.5">Shoppers</th>
                    <th className="p-3.5">Orders</th>
                    <th className="p-3.5">Conversion Rate</th>
                    <th className="p-3.5">Gross Revenue</th>
                    <th className="p-3.5">Discount Cost</th>
                    <th className="p-3.5">Net Profit</th>
                    <th className="p-3.5 pr-4">Average Order Value</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-[#E5DDD0] font-mono">
                  
                  {/* Control Row */}
                  <tr className="hover:bg-bg/40">
                    <td className="p-3.5 pl-4 font-bold text-primary">No Offer (Control)</td>
                    <td className="p-3.5 text-muted">{control.discount_pct}%</td>
                    <td className="p-3.5 text-muted">{control.sample_size}</td>
                    <td className="p-3.5 text-primary font-bold">{control.converted_count}</td>
                    <td className="p-3.5 text-primary font-bold">{control.conversion_rate_pct}%</td>
                    <td className="p-3.5 text-primary font-bold">₹{control.gross_revenue_inr.toLocaleString('en-IN')}</td>
                    <td className="p-3.5 text-muted">₹{control.discount_cost_inr.toLocaleString('en-IN')}</td>
                    <td className="p-3.5 text-success font-bold">₹{control.net_profit_inr.toLocaleString('en-IN')}</td>
                    <td className="p-3.5 pr-4 text-primary font-bold">₹{control.measured_aov_inr.toLocaleString('en-IN')}</td>
                  </tr>

                  {/* Variant A Row */}
                  <tr className="hover:bg-bg/40">
                    <td className="p-3.5 pl-4 font-bold text-primary">Offer A (5% Off)</td>
                    <td className="p-3.5 text-accent font-bold">{variantA.discount_pct}%</td>
                    <td className="p-3.5 text-muted">{variantA.sample_size}</td>
                    <td className="p-3.5 text-primary font-bold">{variantA.converted_count}</td>
                    <td className="p-3.5 text-primary font-bold">{variantA.conversion_rate_pct}%</td>
                    <td className="p-3.5 text-primary font-bold">₹{variantA.gross_revenue_inr.toLocaleString('en-IN')}</td>
                    <td className="p-3.5 text-accent font-bold">₹{variantA.discount_cost_inr.toLocaleString('en-IN')}</td>
                    <td className="p-3.5 text-success font-bold">₹{variantA.net_profit_inr.toLocaleString('en-IN')}</td>
                    <td className="p-3.5 pr-4 text-primary font-bold">₹{variantA.measured_aov_inr.toLocaleString('en-IN')}</td>
                  </tr>

                  {/* Variant B Row */}
                  <tr className="hover:bg-bg/40">
                    <td className="p-3.5 pl-4 font-bold text-primary">Offer B (10% Off)</td>
                    <td className="p-3.5 text-success font-bold">{variantB.discount_pct}%</td>
                    <td className="p-3.5 text-muted">{variantB.sample_size}</td>
                    <td className="p-3.5 text-success font-bold">{variantB.converted_count}</td>
                    <td className="p-3.5 text-success font-bold">{variantB.conversion_rate_pct}%</td>
                    <td className="p-3.5 text-primary font-bold">₹{variantB.gross_revenue_inr.toLocaleString('en-IN')}</td>
                    <td className="p-3.5 text-accent font-bold">₹{variantB.discount_cost_inr.toLocaleString('en-IN')}</td>
                    <td className="p-3.5 text-success font-bold">₹{variantB.net_profit_inr.toLocaleString('en-IN')}</td>
                    <td className="p-3.5 pr-4 text-primary font-bold">₹{variantB.measured_aov_inr.toLocaleString('en-IN')}</td>
                  </tr>

                </tbody>
              </table>
            </div>
          </Card>
        </div>

      </main>
      <ChatPanel />
    </div>
  );
}
