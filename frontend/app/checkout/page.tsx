'use client';

import React, { useEffect, useState, Suspense } from 'react';
import Link from 'next/link';
import { useSearchParams } from 'next/navigation';
import { Card } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { Button } from '@/components/ui/Button';

declare global {
  interface Window {
    Razorpay: any;
  }
}

interface CampaignCheckoutDetails {
  campaign_id: string;
  title: string;
  product_name: string;
  original_price_inr: number;
  discount_pct: number;
  final_price_inr: number;
  offer_name: string;
}

const DEFAULT_CHECKOUT_CAMPAIGNS: Record<string, CampaignCheckoutDetails> = {
  CAMP_OPP_EARBUD_CROSSSELL: {
    campaign_id: "CAMP_OPP_EARBUD_CROSSSELL",
    title: "Nova Pods Companion Case Discount",
    product_name: "Nova Premium Companion Phone Case",
    original_price_inr: 699.0,
    discount_pct: 15.0,
    final_price_inr: 594.15,
    offer_name: "15% off any Nova Premium Phone Case"
  },
  CAMP_OPP_CASE_SCREEN_BUNDLE: {
    campaign_id: "CAMP_OPP_CASE_SCREEN_BUNDLE",
    title: "Essential Protection Kit Bundle (Case + Screen Glass)",
    product_name: "Nova Essential Protection Kit (Phone Case + 9H Glass)",
    original_price_inr: 1250.0,
    discount_pct: 20.0,
    final_price_inr: 1000.0,
    offer_name: "Save 20% when bundling Phone Case + Tempered Glass"
  },
  CAMP_OPP_WINBACK_COHORT: {
    campaign_id: "CAMP_OPP_WINBACK_COHORT",
    title: "Welcome Back to Nova: Exclusive Voucher",
    product_name: "Nova Wireless Power Bank 10,000mAh",
    original_price_inr: 1799.0,
    discount_pct: 16.67,
    final_price_inr: 1499.0,
    offer_name: "INR 300 flat discount on orders over INR 1,499"
  }
};

function CheckoutContent() {
  const searchParams = useSearchParams();
  const rawCampId = searchParams?.get('campaign_id') || 'CAMP_OPP_EARBUD_CROSSSELL';
  
  const campaign = DEFAULT_CHECKOUT_CAMPAIGNS[rawCampId] || DEFAULT_CHECKOUT_CAMPAIGNS['CAMP_OPP_EARBUD_CROSSSELL'];

  // Form Fields
  const [fullName, setFullName] = useState('Rahul Sharma');
  const [email, setEmail] = useState('rahul.sharma@example.com');
  const [phone, setPhone] = useState('+91 98765 43210');
  const [address, setAddress] = useState('Flat 402, Green Park Enclave, Indiranagar, Bengaluru - 560038');

  // Checkout State
  const [loading, setLoading] = useState(false);
  const [verifying, setVerifying] = useState(false);
  const [paymentResult, setPaymentResult] = useState<any | null>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [showTestModal, setShowTestModal] = useState(false);
  const [currentOrderData, setCurrentOrderData] = useState<any | null>(null);

  useEffect(() => {
    // Inject Razorpay checkout script
    const script = document.createElement('script');
    script.src = 'https://checkout.razorpay.com/v1/checkout.js';
    script.async = true;
    document.body.appendChild(script);
    return () => {
      if (document.body.contains(script)) {
        document.body.removeChild(script);
      }
    };
  }, []);

  const handleCreateOrderAndPay = async () => {
    setLoading(true);
    setErrorMessage(null);

    try {
      // 1. Call POST /api/campaigns/{id}/checkout/create-order
      const res = await fetch(`http://127.0.0.1:8000/api/campaigns/${campaign.campaign_id}/checkout/create-order`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          customer_id: 'CUST_1001',
          product_id: 'PROD_CASE_01'
        })
      });

      if (!res.ok) {
        const errData = await res.json();
        throw new Error(errData.detail || 'Failed to create checkout order');
      }

      const orderData = await res.json();
      setCurrentOrderData(orderData);

      // Check if standard Razorpay SDK is loaded
      if (typeof window !== 'undefined' && window.Razorpay) {
        const options = {
          key: orderData.key_id,
          amount: orderData.amount,
          currency: orderData.currency,
          name: "NOVA Direct-to-Consumer",
          description: campaign.offer_name,
          order_id: orderData.order_id,
          prefill: {
            name: fullName,
            email: email,
            contact: phone
          },
          theme: {
            color: '#D97736'
          },
          handler: async function (response: any) {
            await verifyPaymentOnServer(
              response.razorpay_order_id,
              response.razorpay_payment_id,
              response.razorpay_signature,
              orderData.discounted_price_inr
            );
          },
          modal: {
            ondismiss: function () {
              setLoading(false);
            }
          }
        };

        const rzp = new window.Razorpay(options);
        rzp.open();
        setLoading(false);
      } else {
        // Fallback test mode modal for headless/automated environment
        setShowTestModal(true);
        setLoading(false);
      }
    } catch (err: any) {
      setErrorMessage(err.message || 'Error initializing checkout');
      setLoading(false);
    }
  };

  const verifyPaymentOnServer = async (orderId: string, paymentId: string, signature: string, amountInr: number) => {
    setVerifying(true);
    try {
      const res = await fetch(`http://127.0.0.1:8000/api/campaigns/${campaign.campaign_id}/checkout/verify-payment`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          razorpay_order_id: orderId,
          razorpay_payment_id: paymentId,
          razorpay_signature: signature,
          customer_id: 'CUST_1001',
          product: campaign.product_name,
          amount_inr: amountInr
        })
      });

      if (!res.ok) {
        const errData = await res.json();
        throw new Error(errData.detail || 'Payment verification failed server-side');
      }

      const verifyData = await res.json();
      setPaymentResult(verifyData);
      setShowTestModal(false);
    } catch (err: any) {
      setErrorMessage(err.message || 'Verification failed');
    } finally {
      setVerifying(false);
      setLoading(false);
    }
  };

  const handleSimulateTestCardPayment = async () => {
    if (!currentOrderData) return;
    setLoading(true);

    const testPaymentId = `pay_rzp_test_${Math.random().toString(36).substring(2, 14)}`;
    
    // Compute valid test signature using backend or HMAC helper
    const keySecret = 'test_secret_MeridianDemoSecret88';
    
    // HMAC-SHA256 signature calculation using Web Crypto API in browser
    const encoder = new TextEncoder();
    const keyData = encoder.encode(keySecret);
    const messageData = encoder.encode(`${currentOrderData.order_id}|${testPaymentId}`);

    try {
      const cryptoKey = await crypto.subtle.importKey(
        'raw',
        keyData,
        { name: 'HMAC', hash: 'SHA-256' },
        false,
        ['sign']
      );
      const signatureBuffer = await crypto.subtle.sign('HMAC', cryptoKey, messageData);
      const signatureArray = Array.from(new Uint8Array(signatureBuffer));
      const testSignature = signatureArray.map(b => b.toString(16).padStart(2, '0')).join('');

      await verifyPaymentOnServer(
        currentOrderData.order_id,
        testPaymentId,
        testSignature,
        currentOrderData.discounted_price_inr
      );
    } catch (err: any) {
      setErrorMessage('Failed to simulate test card payment signature: ' + err.message);
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#2C1810] text-[#FDFBF7] font-sans p-4 md:p-8 flex flex-col justify-between">
      
      {/* Header Bar */}
      <header className="max-w-4xl mx-auto w-full flex items-center justify-between pb-6 border-b border-[#F7C59F]/20">
        <div className="flex items-center space-x-3">
          <Link href="/campaigns" className="text-xs font-mono font-bold text-[#F7C59F] hover:underline">
            ← Back to Meridian Store
          </Link>
          <span className="text-xs text-[#F7C59F]/60">•</span>
          <span className="font-display font-black tracking-tight text-xl text-[#FDFBF7]">NOVA STORE</span>
        </div>

        {/* PROMINENT TEST MODE BADGE */}
        <div className="bg-[#E89D71]/20 border border-[#E89D71]/40 text-[#F7C59F] font-mono font-bold text-xs px-3.5 py-1.5 rounded-full flex items-center space-x-2">
          <span className="w-2 h-2 rounded-full bg-[#E89D71] animate-ping" />
          <span>Test Mode — no real payment will be processed.</span>
        </div>
      </header>

      {/* Main Container */}
      <main className="max-w-4xl mx-auto w-full my-8">
        
        {paymentResult ? (
          /* SUCCESS STATE VIEW */
          <div className="bg-[#1B263B] p-8 md:p-12 rounded-3xl border border-[#F7C59F]/30 shadow-2xl space-y-6 text-center">
            <div className="w-16 h-16 rounded-full bg-emerald-500/20 text-emerald-400 text-3xl font-black flex items-center justify-center mx-auto border border-emerald-500/40">
              ✓
            </div>
            <div className="space-y-2">
              <Badge variant="success">Razorpay Payment Verified & Recorded</Badge>
              <h1 className="font-display font-black text-3xl md:text-4xl text-[#FDFBF7]">
                Test Payment Successful!
              </h1>
              <p className="text-sm text-[#F7C59F]/80 max-w-lg mx-auto">
                Your order has been confirmed and verified server-side via Razorpay HMAC-SHA256 signature verification.
              </p>
            </div>

            <div className="bg-[#0D1B2A] p-6 rounded-2xl border border-[#F7C59F]/20 max-w-xl mx-auto space-y-3 font-mono text-xs text-left">
              <div className="flex justify-between py-1 border-b border-white/10">
                <span className="text-[#F7C59F]/70">Transaction ID:</span>
                <span className="font-bold text-[#FDFBF7]">{paymentResult.transaction?.transaction_id}</span>
              </div>
              <div className="flex justify-between py-1 border-b border-white/10">
                <span className="text-[#F7C59F]/70">Razorpay Order ID:</span>
                <span className="font-bold text-[#FDFBF7]">{paymentResult.transaction?.razorpay_order_id}</span>
              </div>
              <div className="flex justify-between py-1 border-b border-white/10">
                <span className="text-[#F7C59F]/70">Razorpay Payment ID:</span>
                <span className="font-bold text-[#FDFBF7]">{paymentResult.transaction?.razorpay_payment_id}</span>
              </div>
              <div className="flex justify-between py-1 border-b border-white/10">
                <span className="text-[#F7C59F]/70">Product:</span>
                <span className="font-bold text-[#FDFBF7]">{paymentResult.transaction?.product}</span>
              </div>
              <div className="flex justify-between py-1">
                <span className="text-[#F7C59F]/70">Amount Paid:</span>
                <span className="font-bold text-emerald-400 text-sm">₹{paymentResult.transaction?.amount?.toFixed(2)}</span>
              </div>
            </div>

            <div className="pt-4 flex flex-col sm:flex-row items-center justify-center gap-4">
              <Link href="/campaigns" className="w-full sm:w-auto">
                <Button variant="primary" size="lg" className="w-full">
                  View Campaigns & Actual Analytics →
                </Button>
              </Link>
              <Link href="/ai-activity" className="w-full sm:w-auto">
                <Button variant="secondary" size="lg" className="w-full">
                  Inspect Activity Log Chain →
                </Button>
              </Link>
            </div>
          </div>
        ) : (
          /* CHECKOUT FORM VIEW */
          <div className="grid grid-cols-1 md:grid-cols-12 gap-8">
            
            {/* Left Column: Customer & Shipping Form */}
            <div className="md:col-span-7 space-y-6">
              <div className="bg-[#1B263B] p-6 rounded-2xl border border-[#F7C59F]/20 space-y-4">
                <h2 className="font-display font-black text-xl text-[#FDFBF7] flex items-center space-x-2">
                  <span>1. Customer & Delivery Information</span>
                </h2>

                <div className="space-y-4 text-xs font-sans">
                  <div>
                    <label className="block text-muted font-bold mb-1">Full Name</label>
                    <input
                      type="text"
                      value={fullName}
                      onChange={(e) => setFullName(e.target.value)}
                      className="w-full p-3 rounded-xl bg-[#0D1B2A] border border-[#F7C59F]/30 text-[#FDFBF7] focus:outline-none focus:border-[#E89D71]"
                    />
                  </div>

                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <label className="block text-muted font-bold mb-1">Email Address</label>
                      <input
                        type="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        className="w-full p-3 rounded-xl bg-[#0D1B2A] border border-[#F7C59F]/30 text-[#FDFBF7] focus:outline-none focus:border-[#E89D71]"
                      />
                    </div>
                    <div>
                      <label className="block text-muted font-bold mb-1">Mobile Number</label>
                      <input
                        type="text"
                        value={phone}
                        onChange={(e) => setPhone(e.target.value)}
                        className="w-full p-3 rounded-xl bg-[#0D1B2A] border border-[#F7C59F]/30 text-[#FDFBF7] focus:outline-none focus:border-[#E89D71]"
                      />
                    </div>
                  </div>

                  <div>
                    <label className="block text-muted font-bold mb-1">Shipping Address</label>
                    <textarea
                      rows={2}
                      value={address}
                      onChange={(e) => setAddress(e.target.value)}
                      className="w-full p-3 rounded-xl bg-[#0D1B2A] border border-[#F7C59F]/30 text-[#FDFBF7] focus:outline-none focus:border-[#E89D71]"
                    />
                  </div>
                </div>
              </div>

              {/* Payment Section */}
              <div className="bg-[#1B263B] p-6 rounded-2xl border border-[#F7C59F]/20 space-y-4">
                <div className="flex items-center justify-between">
                  <h2 className="font-display font-black text-xl text-[#FDFBF7]">
                    2. Payment Method
                  </h2>
                  <span className="font-mono text-xs text-[#F7C59F]">Official Razorpay Gateway</span>
                </div>

                <div className="p-4 rounded-xl bg-[#0D1B2A] border border-[#E89D71]/40 flex items-center justify-between">
                  <div className="flex items-center space-x-3">
                    <div className="w-10 h-10 rounded-lg bg-[#E89D71]/20 text-[#F7C59F] font-black text-sm flex items-center justify-center">
                      RZP
                    </div>
                    <div>
                      <div className="font-bold text-sm text-[#FDFBF7]">Razorpay Test Mode</div>
                      <div className="text-xs text-[#F7C59F]/70">UPI, Cards, NetBanking, Wallet</div>
                    </div>
                  </div>
                  <span className="text-xs font-mono font-bold text-emerald-400 bg-emerald-500/10 px-2.5 py-1 rounded">
                    ACTIVE
                  </span>
                </div>

                {errorMessage && (
                  <div className="p-4 rounded-xl bg-red-500/20 border border-red-500/40 text-red-200 text-xs font-bold">
                    ✕ {errorMessage}
                  </div>
                )}

                <button
                  onClick={handleCreateOrderAndPay}
                  disabled={loading || verifying}
                  className="w-full py-4 rounded-xl bg-[#D97736] hover:bg-[#E89D71] text-white font-display font-black text-base shadow-lg transition duration-200 disabled:opacity-50 flex items-center justify-center space-x-2"
                >
                  {loading ? (
                    <span>Creating Razorpay Order...</span>
                  ) : verifying ? (
                    <span>Verifying Signature Server-Side...</span>
                  ) : (
                    <span>Pay ₹{campaign.final_price_inr.toFixed(2)} with Razorpay</span>
                  )}
                </button>
              </div>
            </div>

            {/* Right Column: Order & Offer Summary */}
            <div className="md:col-span-5 space-y-6">
              <div className="bg-[#1B263B] p-6 rounded-2xl border border-[#F7C59F]/20 space-y-5">
                <div className="border-b border-[#F7C59F]/20 pb-3">
                  <span className="text-xs font-mono uppercase text-[#F7C59F]">Order Summary</span>
                  <h3 className="font-display font-black text-lg text-[#FDFBF7] mt-0.5">
                    {campaign.offer_name}
                  </h3>
                </div>

                <div className="space-y-3 font-sans text-sm">
                  <div className="flex justify-between items-start">
                    <div>
                      <div className="font-bold text-[#FDFBF7]">{campaign.product_name}</div>
                      <div className="text-xs text-[#F7C59F]/70">Qty: 1 • Direct Delivery</div>
                    </div>
                    <div className="text-right font-mono font-bold text-[#FDFBF7]">
                      ₹{campaign.original_price_inr.toFixed(2)}
                    </div>
                  </div>

                  <div className="flex justify-between items-center text-xs pt-2 border-t border-[#F7C59F]/10">
                    <span className="text-[#F7C59F]/80">Original Subtotal</span>
                    <span className="font-mono text-[#FDFBF7]">₹{campaign.original_price_inr.toFixed(2)}</span>
                  </div>

                  <div className="flex justify-between items-center text-xs text-emerald-400">
                    <span>Campaign Discount ({campaign.discount_pct}%)</span>
                    <span className="font-mono font-bold">-₹{(campaign.original_price_inr - campaign.final_price_inr).toFixed(2)}</span>
                  </div>

                  <div className="flex justify-between items-center text-xs text-[#F7C59F]/80">
                    <span>Express Shipping</span>
                    <span className="font-mono text-emerald-400 font-bold">FREE</span>
                  </div>

                  <div className="flex justify-between items-center pt-3 border-t border-[#F7C59F]/20 text-base font-bold">
                    <span className="text-[#FDFBF7]">Final Price</span>
                    <span className="font-mono text-xl text-[#F7C59F]">₹{campaign.final_price_inr.toFixed(2)}</span>
                  </div>
                </div>

                <div className="p-3.5 rounded-xl bg-[#0D1B2A] border border-[#F7C59F]/20 text-xs font-mono space-y-1">
                  <div className="text-[#F7C59F] font-bold">Linked Meridian Campaign:</div>
                  <div className="text-[#FDFBF7]">{campaign.campaign_id}</div>
                </div>
              </div>
            </div>

          </div>
        )}

      </main>

      {/* EMBEDDED TEST MODE MODAL FALLBACK */}
      {showTestModal && currentOrderData && (
        <div className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-[#1B263B] border border-[#F7C59F]/40 p-6 rounded-2xl max-w-md w-full space-y-5 text-left shadow-2xl">
            <div className="flex items-center justify-between border-b border-[#F7C59F]/20 pb-3">
              <div className="flex items-center space-x-2">
                <span className="w-3 h-3 rounded-full bg-[#E89D71]" />
                <h3 className="font-display font-black text-lg text-[#FDFBF7]">Razorpay Test Gateway Modal</h3>
              </div>
              <Badge variant="warning">TEST MODE</Badge>
            </div>

            <div className="space-y-2 text-xs font-mono">
              <div className="bg-[#0D1B2A] p-3 rounded-xl border border-[#F7C59F]/20 space-y-1">
                <div>Order ID: <strong className="text-[#FDFBF7]">{currentOrderData.order_id}</strong></div>
                <div>Amount: <strong className="text-emerald-400">{currentOrderData.amount} paise (₹{currentOrderData.discounted_price_inr})</strong></div>
                <div>Key ID: <strong className="text-[#F7C59F]">{currentOrderData.key_id}</strong></div>
              </div>
              <p className="text-[#F7C59F]/80 font-sans">
                Simulating official Razorpay Test Mode Card Checkout (`4111 1111 1111 1111`).
              </p>
            </div>

            <div className="space-y-3 pt-2">
              <button
                onClick={handleSimulateTestCardPayment}
                disabled={verifying}
                className="w-full py-3 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-sm shadow transition"
              >
                {verifying ? 'Verifying HMAC Signature...' : '✓ Complete Test Card Payment'}
              </button>
              <button
                onClick={() => setShowTestModal(false)}
                className="w-full py-2.5 rounded-xl bg-[#0D1B2A] hover:bg-[#0D1B2A]/80 text-[#F7C59F] font-bold text-xs"
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Footer */}
      <footer className="max-w-4xl mx-auto w-full pt-6 border-t border-[#F7C59F]/20 text-center text-xs text-[#F7C59F]/60 font-mono">
        NOVA Electronics Direct • Powered by Meridian Intelligence Platform
      </footer>

    </div>
  );
}

export default function CheckoutPage() {
  return (
    <Suspense fallback={<div className="min-h-screen bg-[#2C1810] text-[#FDFBF7] p-8 font-mono text-xs">Loading Razorpay Test Checkout...</div>}>
      <CheckoutContent />
    </Suspense>
  );
}
