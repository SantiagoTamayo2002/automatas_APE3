import React from 'react'

const S = {
  wrap: { overflowX: 'auto' },
  table: {
    width: '100%', borderCollapse: 'collapse',
    fontFamily: 'var(--font-mono)', fontSize: 13,
  },
  th: {
    padding: '8px 16px', textAlign: 'center',
    background: 'var(--bg-deep)', color: 'var(--accent-cyan)',
    borderBottom: '1px solid var(--border-bright)',
    fontSize: 11, letterSpacing: 2, textTransform: 'uppercase',
  },
  thState: {
    padding: '8px 16px', textAlign: 'left',
    background: 'var(--bg-deep)', color: 'var(--text-secondary)',
    borderBottom: '1px solid var(--border-bright)',
    fontSize: 11, letterSpacing: 2, textTransform: 'uppercase',
  },
  td: (active) => ({
    padding: '10px 16px', textAlign: 'center',
    borderBottom: '1px solid var(--border)',
    color: active ? 'var(--accent-green)' : 'var(--text-secondary)',
    fontWeight: active ? 700 : 400,
    transition: 'all 0.3s',
    background: active ? 'rgba(0,255,136,0.04)' : 'transparent',
  }),
  tdState: (active, isAccept) => ({
    padding: '10px 16px', textAlign: 'left',
    borderBottom: '1px solid var(--border)',
    color: active ? 'var(--accent-cyan)' : isAccept ? 'var(--accent-green)' : 'var(--text-primary)',
    fontWeight: active ? 700 : 600,
    background: active ? 'rgba(0,212,255,0.06)' : 'transparent',
    transition: 'all 0.3s',
  }),
}

export default function TransitionTable({ definition, activeStates = [] }) {
  const { states = [], alphabet = [], transitions = {}, accept_states = [], initial_state } = definition

  const getCell = (state, token) => {
    const targets = transitions[state]?.[token]
    if (!targets || targets.length === 0) return '∅'
    return `{${targets.join(', ')}}`
  }

  return (
    <div style={S.wrap}>
      <table style={S.table}>
        <thead>
          <tr>
            <th style={S.thState}>Estado</th>
            {alphabet.map(t => <th key={t} style={S.th}>{t}</th>)}
          </tr>
        </thead>
        <tbody>
          {states.map(s => {
            const active = activeStates.includes(s)
            const isAccept = accept_states.includes(s)
            const isInit = s === initial_state
            return (
              <tr key={s}>
                <td style={S.tdState(active, isAccept)}>
                  {isInit ? '→ ' : '   '}
                  {isAccept ? '* ' : '  '}
                  {s}
                </td>
                {alphabet.map(t => (
                  <td key={t} style={S.td(active)}>
                    {getCell(s, t)}
                  </td>
                ))}
              </tr>
            )
          })}
        </tbody>
      </table>
    </div>
  )
}
