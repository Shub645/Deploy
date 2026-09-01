'use client';

import React, { useState } from 'react';

const attackChainNodes = [
  {
    id: 'node-1',
    stage: 'Initial Access',
    entity: 'Phishing Email Vector',
    detail: 'Targeted spear-phishing attachment received by user_finance',
    mitre: 'T1566.001',
    status: 'Compromised',
    color: '#f87171'
  },
  {
    id: 'node-2',
    stage: 'Execution',
    entity: 'PowerShell Payload',
    detail: 'Encoded script executed from temp directory',
    mitre: 'T1059.001',
    status: 'Active Threat',
    color: '#fbbf24'
  },
  {
    id: 'node-3',
    stage: 'Credential Access',
    entity: 'LSASS Memory Dump',
    detail: 'Attempted credential harvest via procdump',
    mitre: 'T1003.001',
    status: 'Blocked',
    color: '#34d399'
  },
  {
    id: 'node-4',
    stage: 'Exfiltration',
    entity: 'C2 Beaconing',
    detail: 'Outbound DNS tunneling query detected to external node',
    mitre: 'T1041',
    status: 'Mitigated',
    color: '#38bdf8'
  }
];

export default function AttackChainGraph() {
  const [selectedNode, setSelectedNode] = useState(attackChainNodes[1]);

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
          🛡️ Attack-Chain Correlation Matrix
        </h3>
        <p style={{ margin: 0, fontSize: '13px', color: '#94a3b8' }}>
          Live telemetry mapped across MITRE ATT&CK kill-chain phases. Click any node to inspect telemetry.
        </p>
      </div>

      {/* Graph Node Flow */}
      <div style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        gap: '12px',
        overflowX: 'auto',
        paddingBottom: '16px'
      }}>
        {attackChainNodes.map((node, index) => (
          <React.Fragment key={node.id}>
            <div
              onClick={() => setSelectedNode(node)}
              style={{
                flex: 1,
                minWidth: '200px',
                backgroundColor: selectedNode.id === node.id ? '#1e293b' : '#090d16',
                border: `2px solid ${selectedNode.id === node.id ? node.color : '#334155'}`,
                borderRadius: '10px',
                padding: '16px',
                cursor: 'pointer',
                transition: 'all 0.2s ease'
              }}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
                <span style={{ fontSize: '11px', fontWeight: 'bold', color: node.color, textTransform: 'uppercase' }}>
                  {node.stage}
                </span>
                <span style={{ fontSize: '11px', background: '#1e293b', padding: '2px 6px', borderRadius: '4px', color: '#cbd5e1' }}>
                  {node.mitre}
                </span>
              </div>
              <div style={{ fontSize: '14px', fontWeight: '600', marginBottom: '4px' }}>
                {node.entity}
              </div>
              <div style={{ fontSize: '12px', color: '#64748b' }}>
                Status: <span style={{ color: node.color }}>{node.status}</span>
              </div>
            </div>

            {index < attackChainNodes.length - 1 && (
              <div style={{ color: '#475569', fontWeight: 'bold', fontSize: '18px' }}>
                →
              </div>
            )}
          </React.Fragment>
        ))}
      </div>

      {/* Selected Node Inspection Drawer */}
      <div style={{
        marginTop: '20px',
        backgroundColor: '#090d16',
        border: '1px solid #1e293b',
        borderRadius: '8px',
        padding: '16px'
      }}>
        <h4 style={{ margin: '0 0 8px 0', fontSize: '14px', color: '#38bdf8' }}>
          Node Inspection: {selectedNode.entity} ({selectedNode.mitre})
        </h4>
        <p style={{ margin: '0 0 8px 0', fontSize: '13px', color: '#cbd5e1' }}>
          <strong>Telemetry Detail:</strong> {selectedNode.detail}
        </p>
        <p style={{ margin: 0, fontSize: '12px', color: '#64748b' }}>
          Tactic Stage: {selectedNode.stage} | Current State: {selectedNode.status}
        </p>
      </div>
    </div>
  );
}