'use client';

import React, { useEffect, useState } from 'react';
import { Card } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { Button } from '@/components/ui/Button';
import { Sidebar } from '@/components/ui/Sidebar';
import { ChatPanel } from '@/components/dashboard/ChatPanel';

interface GuardrailSettings {
  max_discount_percent: number;
  max_campaign_budget: number;
  max_campaigns_per_day: number;
  auto_approve_analysis: boolean;
  auto_approve_draft_campaigns: boolean;
  require_approval_to_launch: boolean;
}

const DEFAULT_SETTINGS: GuardrailSettings = {
  max_discount_percent: 25.0,
  max_campaign_budget: 50000.0,
  max_campaigns_per_day: 10,
  auto_approve_analysis: false,
  auto_approve_draft_campaigns: false,
  require_approval_to_launch: true
};

export default function SettingsPage() {
  const [settings, setSettings] = useState<GuardrailSettings>(DEFAULT_SETTINGS);
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [saveSuccess, setSaveSuccess] = useState<string | null>(null);

  useEffect(() => {
    fetchSettings();
  }, []);

  const fetchSettings = async () => {
    setLoading(true);
    try {
      const res = await fetch('http://127.0.0.1:8000/api/settings/guardrails');
      if (res.ok) {
        const data = await res.json();
        setSettings(data);
      }
    } catch (err) {
      console.log('Using default guardrail settings state');
    } finally {
      setLoading(false);
    }
  };

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    setSaveSuccess(null);

    const payload = {
      ...settings,
      require_approval_to_launch: true // Enforce human-in-the-loop requirement
    };

    try {
      const res = await fetch('http://127.0.0.1:8000/api/settings/guardrails', {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });

      if (res.ok) {
        const updated = await res.json();
        setSettings(updated);
        setSaveSuccess(`Merchant settings saved successfully! Max Budget: ₹${updated.max_campaign_budget.toLocaleString('en-IN')}, Max Discount: ${updated.max_discount_percent}%`);
      } else {
        setSaveSuccess('Error saving merchant settings.');
      }
    } catch (err) {
      setSaveSuccess('Backend unreachable; settings saved locally.');
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="flex h-screen overflow-hidden bg-bg text-primary font-sans">
      <Sidebar activePath="/settings" />

      <main className="flex-1 h-screen overflow-y-auto p-6 md:p-10 pb-36 space-y-8 max-w-7xl">
        
        {/* Header Bar */}
        <header className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 bg-surface p-6 rounded-2xl border border-[#E5DDD0] shadow-sm shadow-primary/5">
          <div>
            <div className="flex items-center space-x-2">
              <Badge variant="secondary">Limits & Approval</Badge>
              <span className="text-xs text-muted font-mono">Store Limits & Approval</span>
            </div>
            <h1 className="font-display font-black text-2xl md:text-3xl tracking-tight text-primary mt-1">
              Store Limits & Approval Settings
            </h1>
            <p className="text-xs text-muted font-medium mt-0.5">
              Configure your store details, payment test mode, and spending guardrails to keep your AI marketing assistant safe and under your control.
            </p>
          </div>

          <div className="flex items-center space-x-3">
            <Button variant="ghost" size="sm" onClick={fetchSettings} disabled={loading}>
              {loading ? 'Refreshing...' : '🔄 Refresh Saved Settings'}
            </Button>
          </div>
        </header>

        {saveSuccess && (
          <div className="p-4 rounded-xl bg-success/15 border border-success text-success font-mono text-xs font-bold flex items-center justify-between shadow-sm">
            <span>✓ {saveSuccess}</span>
            <button onClick={() => setSaveSuccess(null)} className="text-xs text-muted hover:text-primary font-bold">✕</button>
          </div>
        )}

        <form onSubmit={handleSave} className="space-y-8">
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            
            {/* Payment Setup & Merchant Profile */}
            <Card title="Payment Setup & Merchant Account" subtitle="Payment Setup — Manage your merchant account details and payment test mode status.">
              <div className="space-y-4 font-sans text-xs">
                <div className="bg-bg p-4 rounded-xl border border-[#E5DDD0] space-y-3 font-sans">
                  <div className="flex justify-between items-center">
                    <div>
                      <div className="font-bold text-primary">Merchant Business Name</div>
                      <div className="text-[11px] text-muted">Your registered merchant business entity</div>
                    </div>
                    <strong className="text-primary font-mono font-bold">NOVA Electronics & Lifestyle</strong>
                  </div>

                  <div className="flex justify-between items-center pt-2 border-t border-[#E5DDD0]">
                    <div>
                      <div className="font-bold text-primary">Store Account ID</div>
                      <div className="text-[11px] text-muted">Unique merchant account identifier</div>
                    </div>
                    <strong className="text-primary font-mono text-xs font-bold">NOVA_ELECTRONICS_INDIA</strong>
                  </div>
                </div>

                <div className="bg-secondary/10 p-4 rounded-xl border border-secondary/20 space-y-2 font-sans">
                  <div className="flex items-center justify-between">
                    <div>
                      <div className="font-bold text-secondary">Payment Gateway Status</div>
                      <div className="text-[11px] text-muted">Connected Razorpay Sandbox Integration</div>
                    </div>
                    <Badge variant="success">Test Sandbox Active</Badge>
                  </div>
                  <div className="text-xs text-primary font-medium mt-1 leading-relaxed bg-surface/80 p-3 rounded-lg border border-secondary/15">
                    <strong>Payment Mode: Test Mode (no real money is charged).</strong>
                    <p className="text-[11px] text-muted mt-1">
                      This is intentionally configured for testing campaign orders safely in the sandbox environment before connecting live customer payments.
                    </p>
                  </div>
                </div>
              </div>
            </Card>

            {/* Spending & Margin Guardrails */}
            <Card title="Spending & Margin Guardrails" subtitle="Spending & Margin Limits — Control how much your AI agent can spend and discount without asking you first.">
              <div className="space-y-5 text-xs font-sans">
                
                <div>
                  <label className="block text-primary font-bold mb-1">
                    Max Campaign Budget (INR):
                  </label>
                  <input
                    type="number"
                    value={settings.max_campaign_budget}
                    onChange={(e) => setSettings({ ...settings, max_campaign_budget: Number(e.target.value) })}
                    className="w-full bg-bg border border-[#E5DDD0] rounded-xl p-3 font-mono text-sm font-bold text-primary focus:outline-none focus:border-accent"
                    step="1000"
                    min="1000"
                    required
                  />
                  <p className="text-[11px] text-muted mt-1 leading-normal">
                    Campaigns won't be allowed to spend more than this total amount. Any proposed campaign exceeding this budget will be automatically rejected to protect your marketing funds.
                  </p>
                </div>

                <div>
                  <label className="block text-primary font-bold mb-1">
                    Max Discount Percent (%):
                  </label>
                  <input
                    type="number"
                    value={settings.max_discount_percent}
                    onChange={(e) => setSettings({ ...settings, max_discount_percent: Number(e.target.value) })}
                    className="w-full bg-bg border border-[#E5DDD0] rounded-xl p-3 font-mono text-sm font-bold text-primary focus:outline-none focus:border-accent"
                    step="1"
                    min="1"
                    max="100"
                    required
                  />
                  <p className="text-[11px] text-muted mt-1 leading-normal">
                    Campaigns won't be allowed to offer more than this discount rate, protecting your profit margins.
                  </p>
                </div>

                <div>
                  <label className="block text-primary font-bold mb-1">
                    Max Campaigns Executed Per Day:
                  </label>
                  <input
                    type="number"
                    value={settings.max_campaigns_per_day}
                    onChange={(e) => setSettings({ ...settings, max_campaigns_per_day: Number(e.target.value) })}
                    className="w-full bg-bg border border-[#E5DDD0] rounded-xl p-3 font-mono text-sm font-bold text-primary focus:outline-none focus:border-accent"
                    step="1"
                    min="1"
                    required
                  />
                  <p className="text-[11px] text-muted mt-1 leading-normal">
                    Prevents over-messaging your customers by capping the maximum number of campaign dispatches per day.
                  </p>
                </div>

              </div>
            </Card>

          </div>

          {/* Automation & Safety Rules */}
          <Card title="Automation & Safety Rules" subtitle="Automation & Safety Rules — Choose which analysis tasks run automatically and enforce merchant approval safety locks.">
            <div className="space-y-4 font-sans text-xs">
              
              <div className="flex items-center justify-between pb-3 border-b border-[#E5DDD0]">
                <div className="pr-4">
                  <div className="font-bold text-primary">Auto-Approve Commercial Opportunity Analysis</div>
                  <div className="text-[11px] text-muted mt-0.5">
                    Automatically log and analyze newly discovered revenue opportunities as soon as customer behavior patterns emerge.
                  </div>
                </div>
                <input
                  type="checkbox"
                  checked={settings.auto_approve_analysis}
                  onChange={(e) => setSettings({ ...settings, auto_approve_analysis: e.target.checked })}
                  className="w-5 h-5 accent-accent rounded cursor-pointer shrink-0"
                />
              </div>

              <div className="flex items-center justify-between pb-3 border-b border-[#E5DDD0]">
                <div className="pr-4">
                  <div className="font-bold text-primary">Auto-Approve Low-Risk Draft Campaigns</div>
                  <div className="text-[11px] text-muted mt-0.5">
                    Allow low-cost, small-discount campaign drafts (Budget ≤ ₹10,000 and Discount ≤ 10%) to execute automatically.
                  </div>
                </div>
                <input
                  type="checkbox"
                  checked={settings.auto_approve_draft_campaigns}
                  onChange={(e) => setSettings({ ...settings, auto_approve_draft_campaigns: e.target.checked })}
                  className="w-5 h-5 accent-accent rounded cursor-pointer shrink-0"
                />
              </div>

              {/* Disabled Safety Lock Toggle */}
              <div className="flex items-center justify-between p-4 bg-secondary/10 border border-secondary/20 rounded-xl">
                <div className="pr-4">
                  <div className="font-bold text-secondary flex items-center space-x-2">
                    <span>🛡️ Always ask before launching a campaign</span>
                    <Badge variant="secondary">Safety Feature Active</Badge>
                  </div>
                  <div className="text-[11px] text-muted mt-1 leading-relaxed">
                    Safety Feature: Keeps you in full control — no marketing campaign can be published to real customers without your explicit manual review and approval.
                  </div>
                </div>
                <input
                  type="checkbox"
                  checked={true}
                  disabled
                  className="w-5 h-5 accent-secondary rounded cursor-not-allowed opacity-60 shrink-0"
                />
              </div>

              <div className="pt-4 flex justify-start">
                <Button variant="primary" size="lg" type="submit" disabled={saving}>
                  {saving ? 'Saving Settings...' : '💾 Save Merchant Settings'}
                </Button>
              </div>

            </div>
          </Card>

        </form>

      </main>
      <ChatPanel />
    </div>
  );
}
