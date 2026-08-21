import { useState } from 'react';
import ResearchExplorer from './components/ResearchExplorer';
import AIAssistant from './components/AIAssistant';
import ResearchMap from './components/ResearchMap';
import ResearchTrends from './components/ResearchTrends';
import ResearchGaps from './components/ResearchGaps';
import ReviewGenerator from './components/ReviewGenerator';

export default function App() {
  const [activeTab, setActiveTab] = useState<
    'explorer' | 'assistant' | 'map' | 'trends' | 'gaps' | 'generator'
  >('explorer');

  const navItems = [
    { id: 'explorer', label: 'Research Explorer', icon: '🔍' },
    { id: 'assistant', label: 'AI Assistant', icon: '🤖' },
    { id: 'map', label: 'Research Map', icon: '🕸️' },
    { id: 'trends', label: 'Trends & Analytics', icon: '📈' },
    { id: 'gaps', label: 'Research Gaps', icon: '⚡' },
    { id: 'generator', label: 'Report Generator', icon: '📄' },
  ];

  return (
    <div className="app-container">
      {/* Top Header */}
      <header className="header">
        <div className="logo-group">
          <div className="logo-icon">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#fff" strokeWidth="2.5">
              <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5" />
            </svg>
          </div>
          <div>
            <h1 className="logo-title">ResearchPilot</h1>
            <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)', margin: 0 }}>
              AI Research Intelligence & Research-Gap Engine
            </p>
          </div>
        </div>

        <div className="status-badge">
          <span className="status-dot"></span>
          Focus: Computer Vision for Healthcare
        </div>
      </header>

      {/* Navigation Tabs */}
      <nav
        style={{
          display: 'flex',
          gap: '0.5rem',
          marginBottom: '2rem',
          overflowX: 'auto',
          paddingBottom: '0.5rem',
        }}
      >
        {navItems.map((item) => (
          <button
            key={item.id}
            onClick={() => setActiveTab(item.id as any)}
            style={{
              background: activeTab === item.id ? 'linear-gradient(135deg, var(--primary), var(--primary-hover))' : 'rgba(18, 26, 44, 0.65)',
              color: activeTab === item.id ? '#ffffff' : 'var(--text-muted)',
              border: activeTab === item.id ? '1px solid rgba(99, 102, 241, 0.5)' : '1px solid var(--border-color)',
              borderRadius: '12px',
              padding: '0.75rem 1.25rem',
              fontFamily: 'var(--font-body)',
              fontWeight: 600,
              fontSize: '0.88rem',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '0.5rem',
              whiteSpace: 'nowrap',
              transition: 'all 0.2s cubic-bezier(0.4, 0, 0.2, 1)',
              boxShadow: activeTab === item.id ? '0 4px 15px rgba(99, 102, 241, 0.3)' : 'none',
            }}
          >
            <span>{item.icon}</span>
            {item.label}
          </button>
        ))}
      </nav>

      {/* Main View Display */}
      <main>
        {activeTab === 'explorer' && <ResearchExplorer />}
        {activeTab === 'assistant' && <AIAssistant />}
        {activeTab === 'map' && <ResearchMap />}
        {activeTab === 'trends' && <ResearchTrends />}
        {activeTab === 'gaps' && <ResearchGaps />}
        {activeTab === 'generator' && <ReviewGenerator />}
      </main>
    </div>
  );
}
