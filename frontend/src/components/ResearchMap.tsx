import { useState, useEffect } from 'react';

interface Node {
  id: string;
  label: string;
  type: string;
  year?: number;
}

interface Edge {
  source: string;
  target: string;
  relation: string;
}

export default function ResearchMap() {
  const [selectedType, setSelectedType] = useState<string>('ALL');
  const [activeNode, setActiveNode] = useState<Node | null>(null);

  const [nodes, setNodes] = useState<Node[]>([
    { id: 'paper-1', label: 'Vision Transformers for Retinal Analysis', type: 'Paper', year: 2024 },
    { id: 'paper-2', label: 'Multimodal Deep Learning in Brain MRI', type: 'Paper', year: 2025 },
    { id: 'paper-3', label: 'Contrastive Learning on Dermoscopy', type: 'Paper', year: 2023 },
    { id: 'paper-4', label: 'EEG Pupillometry Integration for Migraine', type: 'Paper', year: 2025 },
    { id: 'Vision Transformer', label: 'Vision Transformer', type: 'Method' },
    { id: 'U-Net Segmentation Network', label: 'U-Net Segmentation Network', type: 'Method' },
    { id: 'ResNet Architecture', label: 'ResNet Architecture', type: 'Method' },
    { id: 'EyePACS', label: 'EyePACS Fundus Dataset', type: 'Dataset' },
    { id: 'BraTS', label: 'BraTS MRI Dataset', type: 'Dataset' },
    { id: 'MIMIC Clinical Database', label: 'MIMIC Clinical Database', type: 'Dataset' },
    { id: 'ISIC', label: 'ISIC Dermoscopy Dataset', type: 'Dataset' },
    { id: 'Diabetic Retinopathy Grading', label: 'Diabetic Retinopathy Grading', type: 'Task' },
    { id: 'Brain Tumor Segmentation', label: 'Brain Tumor Segmentation', type: 'Task' },
    { id: 'Migraine Detection & Biomarker Analysis', label: 'Migraine Detection', type: 'Task' },
    { id: 'M. Chetri', label: 'M. Chetri', type: 'Author' },
    { id: 'A. Sharma', label: 'A. Sharma', type: 'Author' },
  ]);

  const [edges, setEdges] = useState<Edge[]>([
    { source: 'paper-1', target: 'Vision Transformer', relation: 'USES_METHOD' },
    { source: 'paper-1', target: 'EyePACS', relation: 'TESTED_ON' },
    { source: 'paper-1', target: 'Diabetic Retinopathy Grading', relation: 'SOLVES_TASK' },
    { source: 'paper-2', target: 'U-Net Segmentation Network', relation: 'USES_METHOD' },
    { source: 'paper-2', target: 'BraTS', relation: 'TESTED_ON' },
    { source: 'paper-2', target: 'Brain Tumor Segmentation', relation: 'SOLVES_TASK' },
    { source: 'paper-4', target: 'ResNet Architecture', relation: 'USES_METHOD' },
    { source: 'paper-4', target: 'MIMIC Clinical Database', relation: 'TESTED_ON' },
    { source: 'paper-4', target: 'Migraine Detection & Biomarker Analysis', relation: 'SOLVES_TASK' },
    { source: 'M. Chetri', target: 'paper-1', relation: 'AUTHORED' },
    { source: 'M. Chetri', target: 'paper-4', relation: 'AUTHORED' },
    { source: 'paper-1', target: 'paper-3', relation: 'CITES' },
  ]);

  useEffect(() => {
    fetch('/api/v1/research/graph')
      .then((res) => res.json())
      .then((data) => {
        if (data.nodes && data.edges) {
          setNodes(data.nodes);
          setEdges(data.edges);
        }
      })
      .catch(() => {});
  }, []);

  const getTypeColor = (type: string) => {
    switch (type) {
      case 'Paper': return '#6366f1';
      case 'Method': return '#06b6d4';
      case 'Dataset': return '#a855f7';
      case 'Task': return '#10b981';
      case 'Author': return '#f59e0b';
      default: return '#9ca3af';
    }
  };

  const filteredNodes = selectedType === 'ALL' ? nodes : nodes.filter((n) => n.type === selectedType);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
      <div className="glass-panel" style={{ padding: '1.5rem' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1rem' }}>
          <div>
            <h2 className="section-title" style={{ marginBottom: '0.3rem' }}>
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="var(--accent-purple)" strokeWidth="2">
                <circle cx="12" cy="12" r="3"></circle>
                <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path>
              </svg>
              Research Knowledge Graph Map
            </h2>
            <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>
              Interactive entity network mapping connections between Papers, Methods, Datasets, Tasks, and Authors.
            </p>
          </div>

          <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
            {['ALL', 'Paper', 'Method', 'Dataset', 'Task', 'Author'].map((type) => (
              <button
                key={type}
                onClick={() => setSelectedType(type)}
                style={{
                  background: selectedType === type ? getTypeColor(type) : 'rgba(15, 23, 42, 0.6)',
                  color: selectedType === type ? '#ffffff' : 'var(--text-muted)',
                  border: '1px solid var(--border-color)',
                  borderRadius: '8px',
                  padding: '0.4rem 0.8rem',
                  fontSize: '0.8rem',
                  cursor: 'pointer',
                  fontWeight: 600,
                  transition: 'all 0.2s ease',
                }}
              >
                {type}
              </button>
            ))}
          </div>
        </div>
      </div>

      <div className="dashboard-grid">
        <section className="glass-panel" style={{ padding: '1.5rem', minHeight: '420px', position: 'relative' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '1rem' }}>
            <span style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>Showing {filteredNodes.length} Entities & {edges.length} Relationships</span>
            <div style={{ display: 'flex', gap: '1rem', fontSize: '0.75rem' }}>
              <span style={{ color: '#6366f1' }}>● Paper</span>
              <span style={{ color: '#06b6d4' }}>● Method</span>
              <span style={{ color: '#a855f7' }}>● Dataset</span>
              <span style={{ color: '#10b981' }}>● Task</span>
              <span style={{ color: '#f59e0b' }}>● Author</span>
            </div>
          </div>

          {/* Interactive Network Graph Grid Visualizer */}
          <div
            style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fill, minmax(180px, 1fr))',
              gap: '1rem',
              marginTop: '1rem',
            }}
          >
            {filteredNodes.map((n) => (
              <div
                key={n.id}
                onClick={() => setActiveNode(n)}
                style={{
                  background: activeNode?.id === n.id ? 'rgba(99, 102, 241, 0.25)' : 'rgba(15, 23, 42, 0.7)',
                  border: `1px solid ${getTypeColor(n.type)}`,
                  borderRadius: '12px',
                  padding: '1rem',
                  cursor: 'pointer',
                  transition: 'all 0.2s ease',
                  boxShadow: activeNode?.id === n.id ? `0 0 15px ${getTypeColor(n.type)}40` : 'none',
                }}
              >
                <span
                  style={{
                    background: `${getTypeColor(n.type)}20`,
                    color: getTypeColor(n.type),
                    fontSize: '0.7rem',
                    fontWeight: 700,
                    padding: '0.2rem 0.5rem',
                    borderRadius: '4px',
                    textTransform: 'uppercase',
                  }}
                >
                  {n.type}
                </span>
                <h4 style={{ fontSize: '0.9rem', color: 'var(--text-main)', marginTop: '0.5rem', lineHeight: '1.4' }}>
                  {n.label}
                </h4>
                {n.year && <span style={{ fontSize: '0.75rem', color: 'var(--text-dim)' }}>Published: {n.year}</span>}
              </div>
            ))}
          </div>
        </section>

        <aside className="glass-panel" style={{ padding: '1.5rem' }}>
          <h3 style={{ fontSize: '1rem', color: 'var(--accent-cyan)', marginBottom: '1rem' }}>Entity Relationship Details</h3>
          {activeNode ? (
            <div>
              <div style={{ padding: '1rem', background: 'rgba(15, 23, 42, 0.6)', borderRadius: '10px', marginBottom: '1rem' }}>
                <span style={{ color: getTypeColor(activeNode.type), fontWeight: 700, fontSize: '0.8rem' }}>
                  {activeNode.type.toUpperCase()}
                </span>
                <h4 style={{ fontSize: '1.05rem', marginTop: '0.25rem', color: '#fff' }}>{activeNode.label}</h4>
                {activeNode.year && <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Year: {activeNode.year}</p>}
              </div>

              <h4 style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginBottom: '0.5rem' }}>Connected Graph Edges:</h4>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                {edges
                  .filter((e) => e.source === activeNode.id || e.target === activeNode.id)
                  .map((e, idx) => (
                    <div
                      key={idx}
                      style={{
                        padding: '0.6rem 0.8rem',
                        background: 'rgba(15, 23, 42, 0.5)',
                        border: '1px solid var(--border-color)',
                        borderRadius: '8px',
                        fontSize: '0.8rem',
                      }}
                    >
                      <span style={{ color: 'var(--accent-purple)', fontWeight: 600 }}>{e.relation}</span>:{' '}
                      {e.source === activeNode.id ? e.target : e.source}
                    </div>
                  ))}
              </div>
            </div>
          ) : (
            <p style={{ fontSize: '0.85rem', color: 'var(--text-dim)', fontStyle: 'italic' }}>
              Click on any node in the graph grid to inspect its relations, connected papers, and dataset entities.
            </p>
          )}
        </aside>
      </div>
    </div>
  );
}
