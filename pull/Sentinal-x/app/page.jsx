'use client';

import React, { useState } from 'react';
import AttackChainGraph from './AttackchainGraph';
import ApprovalWorkFlow from './ApprovalWorkFlow';
import LiveAlertStream from './LiveAlertStream';


export default function Home() {
  const [viewTab, setViewTab] = useState('mitre');

  return (
    <main className="p-8 space-y-6">
      <h1 className="text-2xl font-bold">Sentinel-X Dashboard</h1>

      {/* View Tab Toggle Buttons */}
      <div className="flex gap-2">
        <button
          onClick={() => setViewTab('stream')}
          className={`px-4 py-2 rounded font-semibold text-sm transition-colors ${
            viewTab === 'stream' ? 'bg-slate-800 text-white' : 'bg-slate-900 text-slate-400 hover:text-white'
          }`}
        >
          📋 Live Alert Stream
        </button>
        <button
          onClick={() => setViewTab('mitre')}
          className={`px-4 py-2 rounded font-semibold text-sm transition-colors ${
            viewTab === 'mitre' ? 'bg-slate-800 text-white' : 'bg-slate-900 text-slate-400 hover:text-white'
          }`}
        >
          🛡️ MITRE ATT&CK Matrix View
        </button>
        <button
  onClick={() => setViewTab('approval')}
  className={`px-4 py-2 rounded font-semibold text-sm transition-colors ${
    viewTab === 'approval' ? 'bg-slate-800 text-white' : 'bg-slate-900 text-slate-400 hover:text-white'
  }`}
>
  ⚡ Human Approval Workflow
</button>
<button
  onClick={() => setViewTab('stream')}
  className={`px-4 py-2 rounded font-semibold text-sm transition-colors ${
    viewTab === 'stream' ? 'bg-slate-800 text-white' : 'bg-slate-900 text-slate-400 hover:text-white'
  }`}
>
  📡 Live Stream
</button>
      </div>

      {/* Severity Legend */}
      <div className="flex gap-4">
        <span className="px-3 py-1 bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 rounded font-bold text-xs">
          Green / Auto
        </span>
        <span className="px-3 py-1 bg-amber-500/20 text-amber-400 border border-amber-500/30 rounded font-bold text-xs">
          Amber / Pending
        </span>
        <span className="px-3 py-1 bg-rose-500/20 text-rose-400 border border-rose-500/30 rounded font-bold text-xs">
          Red / High-Risk
        </span>
      </div>

      {/* Conditional View Rendering */}
      {viewTab === 'mitre' && <AttackChainGraph />}
{viewTab === 'approval' && <ApprovalWorkflow />}
{viewTab === 'stream' && <LiveAlertStream />}
      {viewTab === 'stream' && (
        <div className="p-6 bg-slate-900 border border-slate-800 rounded-xl text-slate-400">
          Live alert stream telemetry feed...
        </div>
      )}
    </main>
  );
}