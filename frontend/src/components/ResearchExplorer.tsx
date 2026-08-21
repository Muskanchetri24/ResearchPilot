import React, { useState } from 'react';

export default function ResearchExplorer() {
  const [query, setQuery] = useState('Vision Transformers for medical imaging');
  const [domain, setDomain] = useState('Computer Vision for Healthcare');
  const [yearFilter, setYearFilter] = useState('2020-2026');
  const [loading, setLoading] = useState(false);
  const [papers] = useState([
    {
      id: 'paper-1',
      title: 'Vision Transformers for Retinal Image Analysis',
      authors: ['A. Sharma', 'M. Chetri'],
      year: 2024,
      venue: 'IEEE Trans. Medical Imaging',
      citations: 42,
      score: 0.94,
      methods: ['Vision Transformer', 'Self-Attention'],
      dataset: 'EyePACS',
      task: 'Diabetic Retinopathy Grading',
      abstract: 'We present a self-attention transformer architecture for grading fundus retinal images, demonstrating a 4.2% sensitivity improvement over traditional CNNs.',
    },
    {
      id: 'paper-2',
      title: 'Multimodal Deep Learning in Brain MRI Segmentation',
      authors: ['R. Chen', 'K. Patel'],
      year: 2025,
      venue: 'MICCAI',
      citations: 89,
      score: 0.91,
      methods: ['U-Net Segmentation Network', 'Multimodal Fusion'],
      dataset: 'BraTS',
      task: 'Brain Tumor Segmentation',
      abstract: 'Integrates T1, T2, and FLAIR MRI modalities using a 3D U-Net variant to accurately segment glioblastoma sub-regions.',
    },
    {
      id: 'paper-4',
      title: 'EEG Pupillometry Integration for Migraine Detection',
      authors: ['M. Chetri', 'E. Davis'],
      year: 2025,
      venue: 'Journal of Neural Engineering',
      citations: 18,
      score: 0.88,
      methods: ['ResNet Architecture', 'Feature Fusion'],
      dataset: 'MIMIC Clinical Database',
      task: 'Migraine Detection & Biomarker Analysis',
      abstract: 'Combines dynamic pupillary reflex signals with continuous EEG telemetry to detect pre-migraine autonomic fluctuations.',
    },
  ]);

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setTimeout(() => {
      setLoading(false);
    }, 600);
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
      <div className="glass-panel" style={{ padding: '1.5rem' }}>
        <h2 className="section-title">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="var(--accent-cyan)" strokeWidth="2">
            <circle cx="11" cy="11" r="8"></circle>
            <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
          </svg>
          Literature & Paper Search Explorer
        </h2>

        <form onSubmit={handleSearch} style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          <div className="query-box" style={{ marginBottom: 0 }}>
            <input
              type="text"
              className="input-field"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Search papers, methods, datasets, or topics..."
            />
            <button type="submit" className="btn-primary" disabled={loading}>
              {loading ? 'Searching...' : 'Explore Corpus'}
            </button>
          </div>

          <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap' }}>
            <select
              className="input-field"
              style={{ width: 'auto', minWidth: '200px' }}
              value={domain}
              onChange={(e) => setDomain(e.target.value)}
            >
              <option value="Computer Vision for Healthcare">Computer Vision for Healthcare</option>
              <option value="Natural Language Processing">Natural Language Processing</option>
              <option value="Generative AI & RAG">Generative AI & RAG</option>
              <option value="Multimodal AI">Multimodal AI</option>
            </select>

            <select
              className="input-field"
              style={{ width: 'auto', minWidth: '150px' }}
              value={yearFilter}
              onChange={(e) => setYearFilter(e.target.value)}
            >
              <option value="2020-2026">2020 – 2026</option>
              <option value="2018-2026">2018 – 2026</option>
              <option value="All Years">All Publication Years</option>
            </select>
          </div>
        </form>
      </div>

      {/* Results */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
        {papers.map((p) => (
          <div key={p.id} className="glass-panel" style={{ padding: '1.5rem' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '0.5rem' }}>
              <div>
                <h3 style={{ fontSize: '1.15rem', color: 'var(--text-main)', marginBottom: '0.3rem' }}>{p.title}</h3>
                <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>
                  Authors: {p.authors.join(', ')} • <strong>{p.venue}</strong> ({p.year})
                </p>
              </div>
              <span
                style={{
                  background: 'rgba(99, 102, 241, 0.15)',
                  color: 'var(--primary)',
                  border: '1px solid rgba(99, 102, 241, 0.3)',
                  borderRadius: '20px',
                  padding: '0.25rem 0.75rem',
                  fontSize: '0.8rem',
                  fontWeight: 600,
                }}
              >
                Match: {(p.score * 100).toFixed(0)}%
              </span>
            </div>

            <p style={{ fontSize: '0.9rem', color: 'var(--text-muted)', marginBottom: '1rem', lineHeight: '1.6' }}>
              {p.abstract}
            </p>

            <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap', alignItems: 'center' }}>
              <span className="badge" style={{ background: 'rgba(6, 182, 212, 0.1)', color: 'var(--accent-cyan)', border: '1px solid rgba(6, 182, 212, 0.3)', padding: '0.2rem 0.6rem', borderRadius: '6px', fontSize: '0.75rem' }}>
                Method: {p.methods.join(', ')}
              </span>
              <span className="badge" style={{ background: 'rgba(168, 85, 247, 0.1)', color: 'var(--accent-purple)', border: '1px solid rgba(168, 85, 247, 0.3)', padding: '0.2rem 0.6rem', borderRadius: '6px', fontSize: '0.75rem' }}>
                Dataset: {p.dataset}
              </span>
              <span className="badge" style={{ background: 'rgba(16, 185, 129, 0.1)', color: '#10b981', border: '1px solid rgba(16, 185, 129, 0.3)', padding: '0.2rem 0.6rem', borderRadius: '6px', fontSize: '0.75rem' }}>
                Task: {p.task}
              </span>
              <span style={{ fontSize: '0.8rem', color: 'var(--text-dim)', marginLeft: 'auto' }}>
                Citations: {p.citations}
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
