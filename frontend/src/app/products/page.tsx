'use client';

import React, { useEffect, useState } from 'react';
import { Card } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { StatNumber } from '@/components/ui/StatNumber';
import { Sidebar } from '@/components/ui/Sidebar';
import { ChatPanel } from '@/components/dashboard/ChatPanel';

interface ProductTrend {
  product_id: string;
  product_name: string;
  category: string;
  price_inr: number;
  units_w3: number;
  units_w2: number;
  units_w1: number;
  wow_change_w2: number;
  wow_change_w1: number;
  status: 'emerging' | 'declining' | 'stable';
  cross_sell?: string[];
}

const DEFAULT_TRENDS: ProductTrend[] = [
  { product_id: "PROD_WATCH_01", product_name: "Nova Fit Pulse 2", category: "Smartwatches", price_inr: 4199, units_w3: 40, units_w2: 55, units_w1: 75, wow_change_w2: 37.5, wow_change_w1: 36.4, status: "emerging", cross_sell: ["Nylon Sport Strap", "Magnetic Charging Dock"] },
  { product_id: "PROD_EAR_01", product_name: "Nova Pods Lite", category: "Wireless Earbuds", price_inr: 1499, units_w3: 100, units_w2: 76, units_w1: 62, wow_change_w2: -24.0, wow_change_w1: -18.4, status: "declining", cross_sell: ["Companion Case", "Fast USB-C Charger"] },
  { product_id: "PROD_CASE_01", product_name: "Nova Clear Armor Case", category: "Phone Cases", price_inr: 499, units_w3: 85, units_w2: 88, units_w1: 90, wow_change_w2: 3.5, wow_change_w1: 2.3, status: "stable", cross_sell: ["9H Tempered Glass", "Camera Lens Guard"] }
];

export default function ProductsPage() {
  const [products, setProducts] = useState<ProductTrend[]>(DEFAULT_TRENDS);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchProducts();
  }, []);

  const fetchProducts = async () => {
    setLoading(true);
    try {
      const res = await fetch('http://127.0.0.1:8000/api/products/trends');
      const data = await res.json();
      if (data.products?.length) {
        const enriched = data.products.map((p: any) => {
          let cross = ["Screen Protector", "USB-C Cable"];
          if (p.category.includes('Earbud') || p.product_name.includes('Pod')) cross = ["Companion Case", "Fast Charger"];
          else if (p.category.includes('Case')) cross = ["9H Tempered Glass", "Lens Protector"];
          else if (p.category.includes('Watch')) cross = ["Sport Strap", "Charging Stand"];
          return { ...p, cross_sell: cross };
        });
        setProducts(enriched);
      }
    } catch (err) {
      console.log('Using fallback products data');
    } finally {
      setLoading(false);
    }
  };

  const emergingCount = products.filter(p => p.status === 'emerging').length;
  const decliningCount = products.filter(p => p.status === 'declining').length;
  const stableCount = products.filter(p => p.status === 'stable').length;

  return (
    <div className="flex h-screen overflow-hidden bg-bg text-primary font-sans">
      <Sidebar activePath="/products" />

      <main className="flex-1 h-screen overflow-y-auto p-6 md:p-10 space-y-8 max-w-7xl">
        
        {/* Header Bar */}
        <header className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 bg-surface p-6 rounded-2xl border border-[#E5DDD0] shadow-sm shadow-primary/5">
          <div>
            <div className="flex items-center space-x-2 flex-wrap gap-y-1">
              <Badge variant="secondary">Product Performance</Badge>
              <span className="text-xs text-muted font-mono">Weekly Demand & Pairings</span>
              <Badge variant="accent">Synced from NOVA Store · Last updated 2 hours ago</Badge>
            </div>
            <h1 className="font-display font-black text-2xl md:text-3xl tracking-tight text-primary mt-1">
              Products & Frequently Bought Together
            </h1>
            <p className="text-xs text-muted font-medium mt-0.5">
              Live sales momentum and natural product combinations across your store
            </p>
          </div>
        </header>

        {/* Top Summary Stats */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-5">
          <StatNumber
            label="Trending Up Products"
            value={emergingCount}
            subtext="Weekly sales growing fast"
            trend="High Demand"
            trendPositive={true}
          />
          <StatNumber
            label="Trending Down Products"
            value={decliningCount}
            subtext="Weekly sales slowing"
            trend="Promotion Helpful"
            trendPositive={false}
          />
          <StatNumber
            label="Steady Selling Products"
            value={stableCount}
            subtext="Consistent weekly demand"
            trend="Steady"
            trendPositive={true}
          />
        </div>

        {/* Products Table */}
        <div className="space-y-4">
          <h2 className="font-display font-black text-xl tracking-tight text-primary">
            Store Products & Combinations ({products.length} Products)
          </h2>

          <div className="bg-surface border border-[#E5DDD0] rounded-2xl overflow-hidden shadow-sm shadow-primary/5">
            <div className="overflow-x-auto">
              <table className="w-full text-left border-collapse text-xs">
                <thead>
                  <tr className="bg-secondary text-surface font-mono text-[10px] uppercase tracking-wider">
                    <th className="p-4 font-bold">Product Name</th>
                    <th className="p-4 font-bold">Category</th>
                    <th className="p-4 font-bold text-right">Price (INR)</th>
                    <th className="p-4 font-bold">Often Bought With</th>
                    <th className="p-4 font-bold text-right">Weekly Trend</th>
                    <th className="p-4 font-bold text-center">Status</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-[#E5DDD0] font-sans">
                  {products.map((p) => (
                    <tr key={p.product_id} className="hover:bg-bg/50 transition-colors">
                      <td className="p-4 font-bold text-primary">
                        <div>{p.product_name}</div>
                        <div className="text-[10px] text-muted font-mono">ID: {p.product_id}</div>
                      </td>
                      <td className="p-4 text-muted font-medium">{p.category}</td>
                      <td className="p-4 text-right font-mono font-bold text-primary">₹{p.price_inr.toLocaleString('en-IN')}</td>
                      <td className="p-4">
                        <div className="bg-bg px-3 py-1.5 rounded-lg border border-[#E5DDD0] text-primary font-medium text-xs">
                          <span className="text-accent font-bold">Often bought with → </span>
                          {(p.cross_sell || ["Screen Protector", "Charger"]).join(", ")}
                        </div>
                      </td>
                      <td className="p-4 text-right font-mono font-bold">
                        <span className={p.wow_change_w1 >= 0 ? 'text-success' : 'text-warning'}>
                          {p.wow_change_w1 >= 0 ? `+${p.wow_change_w1}%` : `${p.wow_change_w1}%`}
                        </span>
                      </td>
                      <td className="p-4 text-center">
                        <Badge variant={p.status === 'emerging' ? 'success' : (p.status === 'declining' ? 'warning' : 'secondary')}>
                          {p.status === 'emerging' ? 'TRENDING UP' : (p.status === 'declining' ? 'TRENDING DOWN' : 'STEADY')}
                        </Badge>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>

      </main>
      <ChatPanel />
    </div>
  );
}
