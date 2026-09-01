'use client';

import React, { useState } from 'react';

const initialPlaybooks = [
  {
    id: 'pb-1',
    title: 'Isolate Compromised Host & Revoke Sessions',
    target: 'host-fin-04 (user_finance)',
    threatLevel: 'High-Risk',
    aiConfidence: '94%',
    mitreRef: 'T1566.001 / T1059.001',
    status: 'Pending Review'
  },
  {
    id: 'pb-2',
    title: 'Block Outbound DNS Tunneling Destination',
    target: 'ip-198.51.100.24',
    threatLevel: 'Medium-Risk',
    aiConfidence: '88%',
    mitreRef: 'T1041',
    status: 'Pending Review'
  }
];

export default function ApprovalWorkflow() {
  const [playbooks, setPlaybooks] = useState(initialPlaybooks);

  const handleAction = (id, newStatus) => {
    setPlaybooks(prev =>
      prev.map(item => (item.id === id ? { ...item, status: newStatus } : item))
    );
  };

  return (
    <div style={{
      backgroundColor: '#0f172a',
      border: '1px solid #1e293b',
      borderRadius: '12px',
      padding: '24px',
      color: '#f8fafc',
      fontFamily: 'sans-serif'
    }}>
      <div style={{ marginBottom: '20px' }}>
        <h3 style={{ margin: '0 0 6px 0', fontSize: '18px', fontWeight: 'bold' }}>
          🛡️ Human-in-the-Loop Playbook Approvals
        </h3>
        <p style={{ margin: 0, fontSize: '13px', color: '#94a3b8' }}>
          Review and authorize high-impact AI-recommended containment actions before execution.
        </p>
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
        {playbooks.map(pb => (
          <div key={pb.id} style={{
            backgroundColor: '#090d16',
            border: '1px solid #1e293b',
            borderRadius: '10px',
            padding: '18px',
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            flexWrap: 'wrap',
            gap: '12px'
          }}>
            <div style={{ maxWidth: '500px' }}>
              <div style={{ display: 'flex', gap: '8px', marginBottom: '6px', alignItems: 'center' }}>
                <span style={{ fontSize: '11px', background: '#1e293b', padding: '2px 6px', borderRadius: '4px', color: '#38bdf8', fontWeight: 'bold' }}>
                  {pb.mitreRef}
                </span>
                <span style={{ fontSize: '11px', background: 'rgba(248, 113, 113, 0.1)', color: '#f87171', padding: '2px 6px', borderRadius: '4px', fontWeight: 'bold' }}>
                  {pb.threatLevel}
                </span>
                <span style={{ fontSize: '11px', color: '#94a3b8' }}>
                  AI Confidence: {pb.aiConfidence}
                </span>
              </div>
              <h4 style={{ margin: '0 0 4px 0', fontSize: '15px', fontWeight: '600' }}>
                {pb.title}
              </h4>
              <p style={{ margin: 0, fontSize: '12px', color: '#64748b' }}>
                Target Resource: <span style={{ color: '#cbd5e1' }}>{pb.target}</span>
              </p>
            </div>

            <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
              <div style={{ fontSize: '13px', fontWeight: 'bold', padding: '6px 12px', borderRadius: '6px', backgroundColor: pb.status === 'Approved' ? 'rgba(52, 211, 153, 0.1)' : pb.status === 'Rejected' ? 'rgba(248, 113, 113, 0.1)' : 'rgba(251, 191, 36, 0.1)', color: pb.status === 'Approved' ? '#34d399' : pb.status === 'Rejected' ? '#f87171' : '#fbbf24' }}>
                {pb.status}
              </div>

              {pb.status === 'Pending Review' && (
                <div style={{ display: 'flex', gap: '8px' }}>
                  <button
                    onClick={() => handleAction(pb.id, 'Approved')}
                    style={{ backgroundColor: '#059669', color: '#fff', border: 'none', padding: '8px 14px', borderRadius: '6px', cursor: 'pointer', fontWeight: 'bold', fontSize: '12px' }}
                  >
                    Approve
                  </button>
                  <button
                    onClick={() => handleAction(pb.id, 'Rejected')}
                    style={{ backgroundColor: '#dc2626', color: '#fff', border: 'none', padding: '8px 14px', borderRadius: '6px', cursor: 'pointer', fontWeight: 'bold', fontSize: '12px' }}
                  >
                    Reject
                  </button>
                </div>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}