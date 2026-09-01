'use client';

import React, { useState } from 'react';

const initialAlerts = [
  { id: 1, title: 'Suspicious PowerShell Script Execution', host: 'host_admin (192.168.1.45)', severity: 'High-Risk', time: '18:42:10 IST' },
  { id: 2, title: 'Anomalous Outbound Data Spike', host: 'user_finance (10.0.0.12)', severity: 'Medium-Risk', time: '18:38:05 IST' },
];

export default function LiveAlertStream() {
  const [alerts, setAlerts] = useState(initialAlerts);

  // Function to simulate a new incoming attack alert
  const simulateNewAlert = () => {
    const newAlertsList = [
      {
        id: Date.now(),
        title: 'Unauthorized SSH Brute-Force Attempt',
        host: 'server-db-01 (192.168.1.99)',
        severity: 'High-Risk',
        time: new Date().toLocaleTimeString()
      },
      ...alerts
    ];
    setAlerts(newAlertsList);
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
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
        <div>
          <h3 style={{ margin: '0 0 4px 0', fontSize: '18px', fontWeight: 'bold' }}>
            📡 Live Telemetry & Threat Stream
          </h3>
          <p style={{ margin: 0, fontSize: '13px', color: '#94a3b8' }}>
            Real-time incoming security events monitored by Sentinel-X AI.
          </p>
        </div>
        <button
          onClick={simulateNewAlert}
          style={{
            backgroundColor: '#0284c7',
            color: '#fff',
            border: 'none',
            padding: '10px 16px',
            borderRadius: '8px',
            cursor: 'pointer',
            fontWeight: 'bold',
            fontSize: '13px'
          }}
        >
          ⚡ Simulate Incoming Alert
        </button>
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
        {alerts.map(alert => (
          <div key={alert.id} style={{
            backgroundColor: '#090d16',
            border: '1px solid #1e293b',
            borderRadius: '8px',
            padding: '14px 18px',
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center'
          }}>
            <div>
              <div style={{ display: 'flex', gap: '8px', alignItems: 'center', marginBottom: '4px' }}>
                <span style={{ fontSize: '11px', background: 'rgba(248, 113, 113, 0.1)', color: '#f87171', padding: '2px 6px', borderRadius: '4px', fontWeight: 'bold' }}>
                  {alert.severity}
                </span>
                <span style={{ fontSize: '11px', color: '#94a3b8' }}>{alert.time}</span>
              </div>
              <h4 style={{ margin: 0, fontSize: '14px', fontWeight: '600' }}>{alert.title}</h4>
              <p style={{ margin: '2px 0 0 0', fontSize: '12px', color: '#64748b' }}>Target: {alert.host}</p>
            </div>
            <span style={{ fontSize: '12px', color: '#34d399', background: 'rgba(52, 211, 153, 0.1)', padding: '4px 10px', borderRadius: '6px', fontWeight: 'bold' }}>
              Monitoring Active
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}