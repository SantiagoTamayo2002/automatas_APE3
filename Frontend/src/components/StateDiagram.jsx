import React, { useMemo } from 'react'

// Layout positions for each automaton's states
const LAYOUTS = {
  iot: {
    q0: { x: 80, y: 150 },
    q1: { x: 240, y: 150 },
    q2: { x: 400, y: 150 },
    q3: { x: 560, y: 150 },
  },
  genetica: {
    q0: { x: 70, y: 150 },
    q1: { x: 200, y: 150 },
    q2: { x: 330, y: 150 },
    q3: { x: 460, y: 220 },
    q4: { x: 560, y: 150 },
  },
  ecommerce: {
    q0: { x: 80, y: 150 },
    q1: { x: 240, y: 150 },
    q2: { x: 400, y: 150 },
    q3: { x: 560, y: 150 },
  }
}

const R = 36

function arc(x1, y1, x2, y2) {
  const dx = x2 - x1, dy = y2 - y1
  const dist = Math.sqrt(dx * dx + dy * dy)
  const ux = dx / dist, uy = dy / dist
  const nx = -uy, ny = ux
  const cx = (x1 + x2) / 2 + nx * 40
  const cy = (y1 + y2) / 2 + ny * 40
  return `M ${x1 + ux * R} ${y1 + uy * R} Q ${cx} ${cy} ${x2 - ux * R} ${y2 - uy * R}`
}

function straight(x1, y1, x2, y2) {
  const dx = x2 - x1, dy = y2 - y1
  const dist = Math.sqrt(dx * dx + dy * dy)
  const ux = dx / dist, uy = dy / dist
  return `M ${x1 + ux * R} ${y1 + uy * R} L ${x2 - ux * R} ${y2 - uy * R}`
}

function selfLoop(x, y) {
  return `M ${x - 10} ${y - R} C ${x - 50} ${y - 90} ${x + 50} ${y - 90} ${x + 10} ${y - R}`
}

export default function StateDiagram({ definition, activeStates = [], automataKey }) {
  const layout = LAYOUTS[automataKey] || {}
  const { states = [], transitions = {}, initial_state, accept_states = [], state_labels = {} } = definition

  const edges = useMemo(() => {
    const result = []
    const edgeMap = {}

    for (const [from, trans] of Object.entries(transitions)) {
      for (const [token, targets] of Object.entries(trans)) {
        for (const to of targets) {
          const key = `${from}→${to}`
          if (!edgeMap[key]) edgeMap[key] = { from, to, tokens: [] }
          edgeMap[key].tokens.push(token)
        }
      }
    }

    for (const edge of Object.values(edgeMap)) result.push(edge)
    return result
  }, [transitions])

  const isActive = (s) => activeStates.includes(s)
  const isAccept = (s) => accept_states.includes(s)

  return (
    <div style={{ background: 'var(--bg-deep)', border: '1px solid var(--border)', borderRadius: 'var(--radius)', padding: '8px', overflow: 'auto' }}>
      <svg viewBox="0 0 650 300" width="100%" style={{ minWidth: 500 }}>
        <defs>
          <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5"
            markerWidth="6" markerHeight="6" orient="auto-start-reverse">
            <path d="M 0 0 L 10 5 L 0 10 z" fill="#2a4070" />
          </marker>
          <marker id="arrow-active" viewBox="0 0 10 10" refX="9" refY="5"
            markerWidth="6" markerHeight="6" orient="auto-start-reverse">
            <path d="M 0 0 L 10 5 L 0 10 z" fill="#00d4ff" />
          </marker>
          <filter id="glow">
            <feGaussianBlur stdDeviation="3" result="coloredBlur" />
            <feMerge><feMergeNode in="coloredBlur" /><feMergeNode in="SourceGraphic" /></feMerge>
          </filter>
        </defs>

        {/* Edges */}
        {edges.map(({ from, to, tokens }) => {
          const p1 = layout[from], p2 = layout[to]
          if (!p1 || !p2) return null
          const isSelf = from === to
          const active = isActive(from) && isActive(to)
          const color = active ? '#00d4ff' : '#2a4070'
          const label = tokens.join(', ')
          const d = isSelf ? selfLoop(p1.x, p1.y) : arc(p1.x, p1.y, p2.x, p2.y)

          // Label midpoint
          let lx = (p1.x + p2.x) / 2
          let ly = isSelf ? p1.y - 72 : (p1.y + p2.y) / 2 - 28

          return (
            <g key={`${from}-${to}`}>
              <path d={d} fill="none" stroke={color}
                strokeWidth={active ? 2 : 1.5}
                markerEnd={`url(#${active ? 'arrow-active' : 'arrow'})`}
                filter={active ? 'url(#glow)' : undefined}
                style={{ transition: 'stroke 0.3s, stroke-width 0.3s' }}
              />
              <text x={lx} y={ly} textAnchor="middle"
                fill={active ? '#00d4ff' : '#7a9cc0'}
                fontSize="10" fontFamily="JetBrains Mono"
                style={{ transition: 'fill 0.3s' }}>
                {label}
              </text>
            </g>
          )
        })}

        {/* States */}
        {states.map((s) => {
          const pos = layout[s]
          if (!pos) return null
          const active = isActive(s)
          const accept = isAccept(s)
          const isInit = s === initial_state
          const color = active ? (accept ? '#00ff88' : '#00d4ff') : (accept ? '#00ff8844' : 'transparent')
          const stroke = active ? (accept ? '#00ff88' : '#00d4ff') : '#2a4070'

          return (
            <g key={s} transform={`translate(${pos.x}, ${pos.y})`}>
              {/* Initial arrow */}
              {isInit && (
                <g>
                  <line x1={-R - 28} y1={0} x2={-R - 4} y2={0}
                    stroke="#2a4070" strokeWidth={1.5}
                    markerEnd="url(#arrow)" />
                </g>
              )}
              {/* Accept double circle */}
              {accept && (
                <circle r={R + 6} fill="none"
                  stroke={active ? '#00ff88' : '#1e3a2a'}
                  strokeWidth={1.5}
                  style={{ transition: 'stroke 0.3s' }}
                />
              )}
              <circle r={R} fill={color} fillOpacity={active ? 0.15 : 0.05}
                stroke={stroke} strokeWidth={active ? 2 : 1.5}
                filter={active ? 'url(#glow)' : undefined}
                style={{ transition: 'all 0.3s' }}
              />
              {/* State ID */}
              <text textAnchor="middle" dominantBaseline="middle" y={-6}
                fill={active ? (accept ? '#00ff88' : '#00d4ff') : '#7a9cc0'}
                fontSize="13" fontWeight="600" fontFamily="JetBrains Mono"
                style={{ transition: 'fill 0.3s' }}>
                {s}
              </text>
              {/* State label */}
              <text textAnchor="middle" dominantBaseline="middle" y={9}
                fill={active ? '#ffffff88' : '#3d5470'}
                fontSize="8" fontFamily="Syne"
                style={{ transition: 'fill 0.3s' }}>
                {state_labels[s] || ''}
              </text>
            </g>
          )
        })}
      </svg>
    </div>
  )
}
