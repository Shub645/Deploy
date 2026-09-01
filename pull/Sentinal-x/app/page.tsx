"use client";
import React, { useState } from 'react';
import { 
  Shield, Zap, Lock, UserCheck, Terminal, Share2, Activity, Database, 
  ShieldAlert, Fingerprint, CheckCircle2, Clock, BarChart3, ShieldCheck, 
  MessageSquare, Send, X, ThumbsUp, ThumbsDown, Edit3, Globe, Server, 
  Laptop, RefreshCw, Trash2, History, EyeOff, HardDrive, Mail, Check, ShieldCheck as PrivacyIcon
} from 'lucide-react';

export default function SentinelXMasterFinal() {
  // --- STATE ---
  const [isAuthModalOpen, setIsAuthModalOpen] = useState(false);
  const [isFeedbackModalOpen, setIsFeedbackModalOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [status, setStatus] = useState("INVESTIGATING"); 
  const [mvpScore] = useState(94); 

  const [alerts, setAlerts] = useState([
    { id: 1, source: 'EMAIL', event: 'Phishing [T1566.001]', time: '10:02:01', tier: 'HIGH' },
    { id: 2, source: 'ENDPOINT', event: 'Credential Theft [T1003]', time: '10:02:45', tier: 'CRITICAL' },
    { id: 3, source: 'NETWORK', event: 'Lateral Movement [T1021]', time: '10:03:10', tier: 'CRITICAL' },
  ]);

  const [logs, setLogs] = useState([
    { id: 1, time: '10:00:05', msg: 'Privacy Shield: Local LLM Active.', hash: '8f3a' },
    { id: 2, time: '10:01:40', msg: 'Correlation Engine: Mapping Path...', hash: '2d91' },
    { id: 3, time: '10:04:12', msg: 'Jury Consensus: Attack Verified.', hash: '5e12' },
  ]);

  // --- ACTIONS ---
  const runSystemScan = () => {
    setIsLoading(true);
    setTimeout(() => {
      setIsLoading(false);
      setLogs(prev => [{ id: Date.now(), time: 'NOW', msg: 'System Scan: No tampering found.', hash: 'a1b2' }, ...prev]);
    }, 2000);
  };

  const handleAction = (name: string, isHighRisk: boolean) => {
    if (isHighRisk) { setIsAuthModalOpen(true); } 
    else { 
      setStatus("EXECUTING..."); 
      setTimeout(() => { setStatus("MITIGATED"); alert("Sentinel X: Playbook executed."); }, 1000); 
    }
  };

  const zoomClass = "transition-all duration-300 hover:scale-[1.02] hover:shadow-[0_0_30px_rgba(59,130,246,0.2)] hover:bg-[#0d1e3d]";
  const buttonZoomClass = "transition-all duration-200 active:scale-95 hover:scale-105 cursor-pointer shadow-lg";

  return (
    <div className="min-h-screen bg-[#050b1a] text-slate-200 font-sans selection:bg-blue-500/30 overflow-x-hidden">
      
      {/* --- HEADER (Day 5 + Hackathon Privacy Feature) --- */}
      <nav className="border-b border-white/10 bg-[#0a192f]/90 backdrop-blur-md sticky top-0 z-50">
        <div className="max-w-[1600px] mx-auto px-6 h-20 flex items-center justify-between text-white">
          <div className="flex items-center gap-4">
            <div className="bg-blue-600 p-2 rounded-xl shadow-[0_0_20px_rgba(37,99,235,0.5)]">
              <Shield size={26} className="text-white" />
            </div>
            <div>
              <h1 className="font-black text-2xl tracking-tighter uppercase leading-none">SENTINEL <span className="text-blue-400">X</span></h1>
              <div className="flex items-center gap-3 mt-1">
                <span className="text-[9px] text-blue-300/50 font-bold tracking-[0.3em] uppercase">AI Security Operations</span>
                <span className="bg-green-500/10 text-green-500 text-[8px] px-1.5 py-0.5 rounded border border-green-500/20 font-black uppercase tracking-tighter flex items-center gap-1">
                   <PrivacyIcon size={10}/> PII Redaction: ACTIVE (142 scrubbed)
                </span>
              </div>
            </div>
          </div>

          <div className="flex items-center gap-6">
            <div className="hidden lg:flex flex-col items-end border-r border-white/10 pr-6">
              <span className="text-[9px] font-bold text-blue-300/50 uppercase tracking-widest leading-none mb-1">MVP Readiness</span>
              <span className="text-lg font-black text-blue-400 leading-none">94%</span>
            </div>
            <button onClick={runSystemScan} className={`${buttonZoomClass} flex items-center gap-2 bg-blue-600 px-4 py-2 rounded-xl text-[10px] font-black uppercase tracking-widest`}>
              <RefreshCw size={14} className={isLoading ? 'animate-spin' : ''} /> {isLoading ? 'SCANNING...' : 'SYSTEM SCAN'}
            </button>
            <button onClick={() => setIsFeedbackModalOpen(true)} className={`${buttonZoomClass} flex items-center gap-2 bg-[#112240] border border-blue-500/30 px-4 py-2 rounded-xl text-[10px] font-black uppercase tracking-widest text-white`}>
              <MessageSquare size={14} className="text-blue-400" /> Human Feedback
            </button>
          </div>
        </div>
      </nav>

      <main className="max-w-[1600px] mx-auto p-6 grid grid-cols-12 gap-8">
        
        {/* --- LEFT: ALERT TIMELINE --- */}
        <section className="col-span-12 lg:col-span-3 space-y-4">
          <div className="flex items-center justify-between px-2 text-white">
            <h2 className="text-[10px] font-black text-blue-300/50 uppercase tracking-[0.2em] flex items-center gap-2 italic"><Terminal size={14} /> Alert Timeline</h2>
            <button onClick={() => setAlerts([])} className="text-slate-600 hover:text-red-500 transition-colors"><Trash2 size={14}/></button>
          </div>
          <div className="space-y-3">
            {isLoading ? (
              <div className="p-10 text-center animate-pulse text-blue-500 uppercase text-[10px] font-black tracking-widest">Analyzing Silos...</div>
            ) : alerts.length > 0 ? (
              alerts.map((ev) => (
                <div key={ev.id} className={`${zoomClass} bg-[#0a192f] border border-white/5 p-4 rounded-2xl relative overflow-hidden`}>
                  <div className={`absolute top-0 left-0 w-1 h-full ${ev.tier === 'CRITICAL' ? 'bg-red-500 shadow-[0_0_10px_red]' : 'bg-orange-500'}`}></div>
                  <div className="flex justify-between mb-2">
                    <span className="text-[9px] font-mono text-blue-300/50">{ev.time}</span>
                    <span className={`text-[9px] font-black px-2 py-0.5 rounded border ${ev.tier === 'CRITICAL' ? 'bg-red-500/10 text-red-400 border-red-500/20' : 'bg-orange-500/10 text-orange-400 border-orange-500/20'}`}>{ev.tier}</span>
                  </div>
                  <h3 className="text-sm font-bold text-white tracking-tight">{ev.event}</h3>
                  <p className="text-[10px] text-blue-300/50 font-bold mt-3 uppercase tracking-tighter italic">ENCRYPTED LOG</p>
                </div>
              ))
            ) : (
              <div className="bg-[#0a192f] border border-dashed border-white/10 rounded-2xl p-10 text-center"><CheckCircle2 size={32} className="text-green-500 mx-auto mb-3 opacity-40" /><p className="text-[10px] font-black text-slate-500 uppercase tracking-widest">System Secure</p></div>
            )}
          </div>
        </section>

        {/* --- CENTER: ATTACK CHAIN & 3-NODE TOPOLOGY --- */}
        <section className="col-span-12 lg:col-span-6 space-y-4 text-white">
          <h2 className="text-[10px] font-black text-blue-300/50 uppercase tracking-[0.2em] px-2 italic">MITRE Path & Network Topology</h2>
          <div className={`${zoomClass} bg-[#0a192f] border border-white/5 rounded-3xl p-8 flex flex-col shadow-2xl space-y-8`}>
            
            {/* Attack Chain */}
            <div className="space-y-0 text-white">
              {[
                { title: 'Initial Access', mitre: 'T1566', icon: <Share2 />, active: false },
                { title: 'Exfiltration Attempt', mitre: 'T1041', icon: <ShieldAlert />, active: true }
              ].map((step, idx, arr) => (
                <div key={idx} className="relative">
                  <div className="flex items-center gap-8">
                    <div className={`w-12 h-12 rounded-xl border flex items-center justify-center transition-all ${step.active ? 'bg-red-500/20 border-red-500/50 text-red-500 animate-pulse shadow-[0_0_20px_rgba(239,68,68,0.2)]' : 'bg-[#112240] border-white/5 text-blue-300/50'}`}>{step.icon}</div>
                    <div>
                      <h4 className={`text-sm font-black uppercase tracking-tight ${step.active ? 'text-red-400' : 'text-white'}`}>{step.title}</h4>
                      <p className="text-[10px] text-blue-400 font-mono font-bold tracking-widest uppercase tracking-tighter">MITRE ID: {step.mitre}</p>
                    </div>
                  </div>
                  {idx !== arr.length - 1 && <div className="ml-6 border-l-2 border-dashed border-white/10 h-6 my-1"></div>}
                </div>
              ))}
            </div>

            {/* --- FIXED 3-NODE TOPOLOGY GRAPH --- */}
            <div className="bg-[#050b1a] rounded-2xl p-6 border border-white/5 relative h-64 overflow-hidden shadow-inner">
                <p className="absolute top-4 left-4 text-[9px] font-black text-blue-500 uppercase tracking-[0.3em]">Live Connection Topology</p>
                <svg className="absolute inset-0 w-full h-full" viewBox="0 0 800 300">
                    <defs><filter id="lineGlow"><feGaussianBlur stdDeviation="3" result="blur"/><feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>
                    <path d="M 160 150 L 400 150" fill="none" stroke="#ef4444" strokeWidth="2" filter="url(#lineGlow)" opacity="0.6" />
                    <circle r="4" fill="#ef4444"><animateMotion dur="1.5s" repeatCount="indefinite" path="M 160 150 L 400 150" /></circle>
                    <path d="M 400 150 L 640 150" fill="none" stroke="#3b82f6" strokeWidth="2" filter="url(#lineGlow)" opacity="0.6" />
                    <circle r="4" fill="#3b82f6"><animateMotion dur="2s" repeatCount="indefinite" path="M 400 150 L 640 150" /></circle>
                </svg>
                <div className="relative h-full w-full flex items-center justify-between px-20">
                    <div className="flex flex-col items-center gap-2 group z-10"><div className="w-14 h-14 rounded-full border-2 border-red-500 bg-red-950/20 flex items-center justify-center text-red-500 shadow-[0_0_15px_red] transition-transform group-hover:scale-110"><Globe size={24} /></div><span className="text-[9px] font-black uppercase text-red-500">Attacker IP</span></div>
                    <div className="flex flex-col items-center gap-2 group z-10"><div className="w-20 h-20 rounded-full border-2 border-blue-500 bg-blue-950/40 flex items-center justify-center text-blue-400 shadow-[0_0_20px_blue] animate-pulse transition-transform group-hover:scale-110"><Laptop size={36} /></div><span className="text-[11px] font-black uppercase text-white tracking-widest underline">WKSTN-99</span></div>
                    <div className="flex flex-col items-center gap-2 group z-10"><div className="w-14 h-14 rounded-full border-2 border-white/10 bg-[#112240] flex items-center justify-center text-slate-500 group-hover:border-blue-400 group-hover:text-blue-400 transition-all group-hover:scale-110"><Server size={24} /></div><span className="text-[9px] font-black uppercase text-slate-500">SQL-DB-01</span></div>
                </div>
            </div>

            {/* AI Reasoning (Jury Verdict Restored) */}
            <div className="bg-blue-900/10 border border-blue-500/30 p-5 rounded-2xl backdrop-blur-md">
              <div className="flex items-center justify-between mb-2">
                <div className="flex items-center gap-3 text-blue-400 font-bold"><Zap size={16} fill="currentColor" /><span className="text-[10px] font-black uppercase tracking-[0.2em]">Sentinel X AI Analysis</span></div>
                <div className="bg-green-500/10 text-green-500 text-[8px] px-2 py-1 rounded-full border border-green-500/20 font-black uppercase tracking-widest flex items-center gap-1">
                   <ShieldCheck size={10}/> Jury Verdict: 2/2 Agree (No Poisoning)
                </div>
              </div>
              <p className="text-[11px] leading-relaxed text-blue-100 font-medium italic">"Attack Pattern Confirmed. Cross-correlation suggests data exfiltration targeting SQL-DB-01 via private RAG analysis."</p>
            </div>
          </div>
        </section>

        {/* --- RIGHT: PLAYBOOKS & METRICS & LEDGER --- */}
        <section className="col-span-12 lg:col-span-3 space-y-6">
          <h2 className="text-[10px] font-bold text-blue-300/50 uppercase tracking-[0.2em] px-2 italic text-white">Ranked Playbooks</h2>
          <div className="space-y-4">
            
            {/* Rank #1 Playbook (Day 4 Card Feedback Restored) */}
            <div className={`${zoomClass} bg-[#0a192f] border border-white/5 p-5 rounded-2xl group`}>
              <div className="flex justify-between items-center mb-4">
                <span className="text-[9px] text-blue-400 font-black bg-blue-500/10 px-2 py-1 rounded border border-blue-500/20 uppercase tracking-widest">RANK #1</span>
                <div className="flex items-center gap-2 text-white">
                    <button className="p-1.5 hover:bg-green-500/20 rounded text-slate-500 hover:text-green-500 transition-colors"><ThumbsUp size={14}/></button>
                    <button className="p-1.5 hover:bg-red-500/20 rounded text-slate-500 hover:text-red-500 transition-colors"><ThumbsDown size={14}/></button>
                </div>
              </div>
              <h4 className="text-sm font-black mb-1 uppercase text-white tracking-tight">Isolate Host (WKSTN-99)</h4>
              <p className="text-[9px] text-red-500 font-bold uppercase mb-4 italic tracking-tighter">Critical Impact • Auth Required</p>
              <button onClick={() => handleAction("ISOLATION", true)} className={`${buttonZoomClass} w-full py-3 bg-red-600 hover:bg-red-500 text-white rounded-xl text-[10px] font-black uppercase tracking-widest mb-3 shadow-lg shadow-red-600/20`}>Authorize Action</button>
              <button className="w-full flex items-center justify-center gap-2 text-[9px] font-bold text-blue-400/50 hover:text-blue-400 uppercase tracking-widest"><Edit3 size={12}/> Edit Logic</button>
            </div>

            {/* Rank #2 Playbook Restored */}
            <div className={`${zoomClass} bg-[#0a192f] border border-white/5 p-5 rounded-2xl`}>
              <div className="flex justify-between items-center mb-4 text-white">
                <span className="text-[9px] text-slate-500 font-black bg-white/5 px-2 py-1 rounded border border-white/10 uppercase tracking-widest">RANK #2</span>
                <div className="flex items-center gap-2"><button className="p-1.5 hover:bg-green-500/20 rounded text-slate-500 hover:text-green-500"><ThumbsUp size={14}/></button><button className="p-1.5 hover:bg-red-500/20 rounded text-slate-500 hover:text-red-500"><ThumbsDown size={14}/></button></div>
              </div>
              <h4 className="text-sm font-black mb-1 uppercase text-white tracking-tight">Reset User Password</h4>
              <p className="text-[9px] text-green-500 font-bold uppercase mb-4 italic tracking-tighter">Low Risk • AI Approved</p>
              <button onClick={() => handleAction("RESET", false)} className={`${buttonZoomClass} w-full py-3 bg-blue-600/10 hover:bg-blue-600 border border-blue-500/30 rounded-xl text-[10px] font-black uppercase text-white flex items-center justify-center gap-2 shadow-lg shadow-blue-600/20`}><Zap size={14} className="text-yellow-400"/> Execute</button>
            </div>
          </div>

          {/* Metrics & Ledger (Hashes Restored) */}
          <div className={`${zoomClass} bg-[#0a192f] border border-white/5 p-5 rounded-2xl shadow-xl`}>
             <h3 className="text-[10px] font-black text-blue-300/50 uppercase tracking-widest mb-4 flex items-center gap-2 italic text-white"><BarChart3 size={14}/> Analyst Metrics</h3>
             <div className="grid grid-cols-2 gap-4 mb-6">
                <div className="bg-[#112240] p-3 rounded-xl text-center border border-white/5 font-bold"><p className="text-xl font-black text-white">04</p><p className="text-[8px] text-blue-300/50 uppercase">Mitigated</p></div>
                <div className="bg-[#112240] p-3 rounded-xl text-center border border-white/5 font-bold"><p className="text-xl font-black text-white">12s</p><p className="text-[8px] text-blue-300/50 uppercase">Avg Time</p></div>
             </div>
             <div className="border-t border-white/5 pt-4">
                <h4 className="text-[9px] font-black text-slate-500 uppercase flex items-center gap-2 mb-3 text-white"><History size={12}/> Evidence Ledger</h4>
                <div className="h-32 overflow-y-auto space-y-3 font-mono text-[9px]">
                  {logs.map(log => (
                    <div key={log.id} className="border-l border-blue-500/30 pl-3">
                      <div className="flex justify-between items-center mb-1 text-white font-bold"><span className="text-blue-500/50">[{log.time}]</span><div className="flex items-center gap-1 font-bold text-white uppercase"><span className="text-[8px] text-slate-600 font-bold text-white">HASH: {log.hash}</span><Check size={10} className="text-green-500" /></div></div>
                      <span className="text-slate-400 leading-tight block font-bold">{log.msg}</span>
                    </div>
                  ))}
                </div>
             </div>
          </div>
        </section>
      </main>

      {/* --- MODALS (Day 4 Workflow Modify Restored) --- */}
      {isAuthModalOpen && (
        <div className="fixed inset-0 z-[60] flex items-center justify-center p-6 bg-black/95 backdrop-blur-md">
          <div className="bg-[#0a192f] border border-red-500/30 w-full max-w-xl rounded-3xl p-10 shadow-2xl relative text-white">
            <button onClick={() => setIsAuthModalOpen(false)} className="absolute top-6 right-6 text-slate-500 hover:text-white transition-all"><X size={24}/></button>
            <h2 className="text-2xl font-black tracking-tighter uppercase italic text-red-500 mb-6 border-b border-white/5 pb-4">Authorization Required</h2>
            <div className="bg-white/5 p-4 rounded-xl border border-white/5 mb-6">
               <p className="text-[9px] font-black text-slate-500 uppercase mb-2 tracking-widest">Modify High-Risk Workflow</p>
               <div className="flex gap-2">
                  <span className="bg-red-500/10 text-red-500 px-2 py-1 rounded text-[10px] border border-red-500/20 font-bold">FULL ISOLATION</span>
                  <span className="bg-white/5 text-slate-500 px-2 py-1 rounded text-[10px] border border-white/10 font-bold hover:text-white cursor-pointer transition-colors">VPN-ONLY LIMIT</span>
               </div>
            </div>
            <textarea className="w-full bg-[#050b1a] border border-white/10 rounded-2xl p-5 text-sm focus:border-red-500 outline-none text-red-400 font-mono mb-6" rows={3} placeholder="JUSTIFICATION FOR EVIDENCE LEDGER..."></textarea>
            <div className="flex gap-4"><button onClick={() => setIsAuthModalOpen(false)} className="flex-1 py-4 text-xs font-black text-slate-500 hover:text-white uppercase tracking-widest font-bold">Abort</button><button onClick={() => {setIsAuthModalOpen(false); alert("Auth logged.");}} className="flex-1 py-4 bg-red-600 hover:bg-red-500 text-white rounded-2xl text-[10px] font-black uppercase tracking-widest shadow-xl shadow-red-600/20 font-bold">Confirm Auth</button></div>
          </div>
        </div>
      )}

      {isFeedbackModalOpen && (
        <div className="fixed inset-0 z-[60] flex items-center justify-center p-6 bg-black/95 backdrop-blur-md">
          <div className="bg-[#0a192f] border border-blue-500/30 w-full max-w-xl rounded-3xl p-10 shadow-2xl relative text-white">
            <button onClick={() => setIsFeedbackModalOpen(false)} className="absolute top-6 right-6 text-slate-500 hover:text-white hover:rotate-90 transition-all"><X size={24} /></button>
            <div className="flex items-center gap-4 text-blue-400 mb-8 border-b border-white/5 pb-6 font-bold text-white"><MessageSquare size={32} /><div><h2 className="text-2xl font-black tracking-tighter uppercase italic font-bold text-white">Optimize AI Reasoning</h2><p className="text-[10px] text-blue-300/50 font-bold tracking-[0.3em] uppercase font-bold text-white tracking-widest">Human Feedback Loop</p></div></div>
            <div className="mb-6"><p className="text-[10px] font-black text-slate-500 uppercase mb-3 tracking-widest">Analysis Accuracy Rating</p><div className="flex gap-3">{['Inaccurate', 'Partial', 'Accurate'].map(r => <button key={r} className="flex-1 py-2 bg-white/5 border border-white/10 rounded-lg text-[10px] font-bold uppercase hover:border-blue-500 hover:text-blue-400 transition-all">{r}</button>)}</div></div>
            <textarea className="w-full bg-[#050b1a] border border-white/10 rounded-2xl p-5 text-sm focus:border-blue-500 outline-none text-blue-400 font-mono mb-6" rows={4} placeholder="HOW CAN SENTINEL X IMPROVE?"></textarea>
            <div className="flex gap-4 font-white font-bold"><button onClick={() => setIsFeedbackModalOpen(false)} className="flex-1 py-4 text-xs font-black text-slate-500 hover:text-white uppercase tracking-widest font-bold">Cancel</button><button onClick={() => {setIsFeedbackModalOpen(false); alert("Feedback integrated.");}} className={`${buttonZoomClass} flex-[2] py-4 bg-blue-600 hover:bg-blue-500 text-white rounded-2xl text-[10px] font-black uppercase tracking-widest font-bold shadow-lg shadow-blue-600/20`}><Send size={14} /> Submit Feedback</button></div>
          </div>
        </div>
      )}
    </div>
  );
}