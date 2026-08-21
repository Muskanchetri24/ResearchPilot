import { useState, useEffect } from 'react';

interface Gap {
  opportunity_id: string;
  method: string;
  dataset: string;
  task: string;
  paper_count: number;
  recent_growth: string;
  evidence_strength: string;
  opportunity_score: number;
  description: string;
  supporting_paper_titles: string[];
}

export default function ResearchGaps() {
  const [gaps, setGaps] = useState<Gap[]>([
    {
      opportunity_id: 'gap-1',
      method: 'Multimodal Vision Transformer',
      dataset: 'MIMIC Clinical + Pupillometry',
      task: 'Migraine Detection & Biomarker Analysis',
      paper_count: 3,
      recent_growth: 'High',
      evidence_strength: 'Emerging',
      opportunity_score: 94.5,
      description:
        'Combining ocular pupillometry features with EEG clinical streams using multimodal ViTs shows high potential for objective migraine diagnosis, with only 3 published studies to date.',
      supporting_paper_titles: ['EEG Pupillometry Integration for Migraine Detection'],
    },
    {
      opportunity_id: 'gap-2',
      method: 'Federated Self-Supervised Learning',
      dataset: 'EyePACS Fundus Imaging',
      task: 'Diabetic Retinopathy Grading',
      paper_count: 6,
      recent_growth: 'High',
      evidence_strength: 'Moderate',
      opportunity_score: 88.2,
      description:
        'Privacy-preserving federated SSL across decentralized ophthalmic clinics remains underexplored despite high clinical demand.',
      supporting_paper_titles: ['Vision Transformers for Retinal Image Analysis'],
    },
    {
      opportunity_id: 'gap-3',
      method: 'Diffusion-based Data Augmentation',
      dataset: 'BraTS MRI Cohort',
      task: 'Rare Tumor Subtype Segmentation',
      paper_count: 8,
      recent_growth: 'Medium',
      evidence_strength: 'Moderate',
      opportunity_score: 81.0,
      description:
        'Synthetic MRI sample generation for rare glioblastoma subtypes to alleviate extreme class imbalance.',
      supporting_paper_titles: ['Multimodal Deep Learning in Brain MRI Segmentation'],
    },
  ]);

  useEffect(() => {
    fetch('/api/v1/research/gaps')
      .then((res) => res.json())
      .then((data) => {
        if (Array.isArray(data) && data.length > 0) setGaps(data);
      })
      .catch(() => {});
  }, []);

  const getScoreColor = (score: number) => {
    if (score >= 90) return '#ec4899';
    if (score >= 80) return '#a855f7';
    return '#6366f1';
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
      <div className="glass-panel" style={{ padding: '1.5rem' }}>
        <h2 className="section-title">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#ec4899" strokeWidth="2">
            <path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path>
          </svg>
          Research Gap & Opportunity Discovery Engine
        </h2>
        <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>
          Candidate research opportunities ranked quantitatively using the Opportunity Ranking Matrix (Novelty × Recency × Citation Impact × Underexploration).
        </p>
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
        {gaps.map((gap) => (
          <div key={gap.opportunity_id} className="glass-panel" style={{ padding: '1.5rem', borderLeft: `4px solid ${getScoreColor(gap.opportunity_score)}` }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '1rem' }}>
              <div>
                <div style={{ display: 'flex', gap: '0.5rem', alignItems: 'center', marginBottom: '0.4rem' }}>
                  <span
                    style={{
                      background: 'rgba(236, 72, 153, 0.1)',
                      color: getScoreColor(gap.opportunity_score),
                      border: `1px solid ${getScoreColor(gap.opportunity_score)}40`,
                      borderRadius: '6px',
                      padding: '0.2rem 0.6rem',
                      fontSize: '0.75rem',
                      fontWeight: 700,
                    }}
                  >
                    OPPORTUNITY SCORE: {gap.opportunity_score.toFixed(1)} / 100
                  </span>
                  <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                    Analyzed Papers: {gap.paper_count}
                  </span>
                </div>
                <h3 style={{ fontSize: '1.2rem', color: 'var(--text-main)', marginBottom: '0.5rem' }}>
                  {gap.method} + {gap.dataset}
                </h3>
              </div>

              <div style={{ display: 'flex', gap: '0.5rem' }}>
                <span className="badge" style={{ background: 'rgba(16, 185, 129, 0.1)', color: '#10b981', border: '1px solid rgba(16, 185, 129, 0.3)', padding: '0.25rem 0.6rem', borderRadius: '6px', fontSize: '0.75rem' }}>
                  Growth: {gap.recent_growth}
                </span>
                <span className="badge" style={{ background: 'rgba(6, 182, 212, 0.1)', color: 'var(--accent-cyan)', border: '1px solid rgba(6, 182, 212, 0.3)', padding: '0.25rem 0.6rem', borderRadius: '6px', fontSize: '0.75rem' }}>
                  Evidence: {gap.evidence_strength}
                </span>
              </div>
            </div>

            <p style={{ fontSize: '0.95rem', color: 'var(--text-muted)', margin: '0.75rem 0 1rem', lineHeight: '1.6' }}>
              {gap.description}
            </p>

            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', flexWrap: 'wrap', fontSize: '0.8rem', color: 'var(--text-dim)' }}>
              <span>Supporting Literature:</span>
              {gap.supporting_paper_titles.map((title, idx) => (
                <span
                  key={idx}
                  style={{
                    background: 'rgba(15, 23, 42, 0.6)',
                    border: '1px solid var(--border-color)',
                    padding: '0.2rem 0.6rem',
                    borderRadius: '6px',
                    color: 'var(--text-main)',
                  }}
                >
                  📄 {title}
                </span>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
