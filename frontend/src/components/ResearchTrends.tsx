import { useState, useEffect } from 'react';

export default function ResearchTrends() {
  const [data, setData] = useState({
    total_papers_analyzed: 2847,
    publication_velocity: [
      { year: 2019, count: 142 },
      { year: 2020, count: 235 },
      { year: 2021, count: 389 },
      { year: 2022, count: 512 },
      { year: 2023, count: 698 },
      { year: 2024, count: 870 },
      { year: 2025, count: 1120 },
    ],
    method_popularity: [
      { method: 'CNN Architectures', share: 31, trend: 'stable' },
      { method: 'Vision Transformers (ViT)', share: 27, trend: 'rising' },
      { method: 'Transfer Learning', share: 18, trend: 'stable' },
      { method: 'Multimodal / Foundation Models', share: 12, trend: 'sharply_rising' },
      { method: 'Federated Learning', share: 7, trend: 'rising' },
      { method: 'Traditional ML / SVM', share: 5, trend: 'declining' },
    ],
    evolution_timeline: [
      { year: 2018, dominant_architecture: 'CNNs (ResNet, VGG)' },
      { year: 2020, dominant_architecture: 'Transfer Learning & U-Net' },
      { year: 2022, dominant_architecture: 'Vision Transformers (ViT)' },
      { year: 2024, dominant_architecture: 'Multimodal Contrastive Learning' },
      { year: 2026, dominant_architecture: 'Medical Foundation Models & RAG' },
    ],
    topic_clusters: [
      { cluster_id: 1, name: 'Facial Analysis & Pupillometry', size: 420 },
      { cluster_id: 2, name: 'Retinal & Fundus Imaging', size: 380 },
      { cluster_id: 3, name: 'Brain MRI & Neuro-Oncology', size: 510 },
      { cluster_id: 4, name: 'Multimodal Vision + EEG', size: 290 },
      { cluster_id: 5, name: 'Federated Medical AI', size: 180 },
    ],
  });

  useEffect(() => {
    fetch('/api/v1/research/trends')
      .then((res) => res.json())
      .then((resData) => {
        if (resData.publication_velocity) setData(resData);
      })
      .catch(() => {});
  }, []);

  const maxCount = Math.max(...data.publication_velocity.map((v) => v.count));

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
      <div className="glass-panel" style={{ padding: '1.5rem' }}>
        <h2 className="section-title">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#10b981" strokeWidth="2">
            <polyline points="23 6 13.5 15.5 8.5 10.5 1 18"></polyline>
            <polyline points="17 6 23 6 23 12"></polyline>
          </svg>
          Research Trend Analytics & Temporal Evolution
        </h2>
        <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>
          Analyzing publication velocity, methodology shifts, and BERTopic clusters across {data.total_papers_analyzed.toLocaleString()} papers.
        </p>
      </div>

      <div className="dashboard-grid">
        {/* Publication Velocity Bar Chart */}
        <section className="glass-panel" style={{ padding: '1.5rem' }}>
          <h3 style={{ fontSize: '1rem', color: 'var(--accent-cyan)', marginBottom: '1.25rem' }}>
            Publication Volume Velocity (2019 – 2025)
          </h3>
          <div style={{ display: 'flex', alignItems: 'flex-end', gap: '1rem', height: '200px', paddingTop: '1rem' }}>
            {data.publication_velocity.map((v) => (
              <div key={v.year} style={{ flex: 1, display: 'flex', flexDirection: 'column', alignItems: 'center', height: '100%', justifyContent: 'flex-end' }}>
                <span style={{ fontSize: '0.75rem', color: 'var(--accent-cyan)', fontWeight: 600, marginBottom: '0.3rem' }}>
                  {v.count}
                </span>
                <div
                  style={{
                    width: '100%',
                    height: `${(v.count / maxCount) * 100}%`,
                    background: 'linear-gradient(180deg, var(--primary), var(--accent-cyan))',
                    borderRadius: '6px 6px 0 0',
                    transition: 'all 0.4s ease',
                  }}
                ></div>
                <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: '0.5rem' }}>{v.year}</span>
              </div>
            ))}
          </div>
        </section>

        {/* Methodology Share */}
        <aside className="glass-panel" style={{ padding: '1.5rem' }}>
          <h3 style={{ fontSize: '1rem', color: 'var(--accent-purple)', marginBottom: '1.25rem' }}>
            Methodology Market Share
          </h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.85rem' }}>
            {data.method_popularity.map((m) => (
              <div key={m.method}>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.85rem', marginBottom: '0.2rem' }}>
                  <span style={{ color: 'var(--text-main)' }}>{m.method}</span>
                  <span style={{ fontWeight: 600, color: 'var(--accent-cyan)' }}>{m.share}%</span>
                </div>
                <div style={{ background: 'rgba(15, 23, 42, 0.8)', height: '8px', borderRadius: '4px', overflow: 'hidden' }}>
                  <div
                    style={{
                      width: `${m.share}%`,
                      height: '100%',
                      background: m.trend === 'sharply_rising' ? 'linear-gradient(90deg, #a855f7, #ec4899)' : 'var(--primary)',
                      borderRadius: '4px',
                    }}
                  ></div>
                </div>
              </div>
            ))}
          </div>
        </aside>
      </div>

      {/* Evolution Timeline */}
      <div className="glass-panel" style={{ padding: '1.5rem' }}>
        <h3 style={{ fontSize: '1rem', color: 'var(--text-main)', marginBottom: '1.25rem' }}>
          Methodological Paradigm Evolution Timeline
        </h3>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: '1rem' }}>
          {data.evolution_timeline.map((item) => (
            <div
              key={item.year}
              style={{
                background: 'rgba(15, 23, 42, 0.6)',
                border: '1px solid var(--border-color)',
                borderRadius: '12px',
                padding: '1.25rem',
                borderLeft: '4px solid var(--accent-cyan)',
              }}
            >
              <span style={{ fontSize: '0.8rem', color: 'var(--accent-cyan)', fontWeight: 700 }}>{item.year}</span>
              <h4 style={{ fontSize: '0.95rem', color: 'var(--text-main)', marginTop: '0.4rem', lineHeight: '1.4' }}>
                {item.dominant_architecture}
              </h4>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
