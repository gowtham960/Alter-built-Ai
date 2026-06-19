import React, { useState } from 'react';
import { createRoot } from 'react-dom/client';
import './style.css';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

function App() {
  const [question, setQuestion] = useState('Rain delayed concrete work for 3 days. Can we request a schedule extension?');
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  async function askAgent() {
    setLoading(true);
    setError('');
    setResponse(null);

    try {
      const res = await fetch(`${API_URL}/ask`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question }),
      });

      if (!res.ok) {
        throw new Error('Backend request failed');
      }

      const data = await res.json();
      setResponse(data);
    } catch (err) {
      setError('Could not reach backend. Make sure FastAPI is running on port 8000.');
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="page">
      <section className="hero">
        <p className="eyebrow">Agentic RAG Portfolio Project</p>
        <h1>Alter Built AI</h1>
        <p className="subtitle">
          Analyze construction delays, contract clauses, weather records, site notes, RFIs,
          and change-order history with an evidence-based AI agent.
        </p>
      </section>

      <section className="card">
        <label htmlFor="question">Ask a construction change-order question</label>
        <textarea
          id="question"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          rows="4"
        />
        <button onClick={askAgent} disabled={loading}>
          {loading ? 'Analyzing...' : 'Analyze Claim'}
        </button>
        {error && <p className="error">{error}</p>}
      </section>

      {response && (
        <section className="result">
          <div className="summary">
            <h2>{response.recommendation}</h2>
            <p><strong>Confidence:</strong> {response.confidence}</p>
            <p>{response.answer}</p>
            <p><strong>Next action:</strong> {response.next_action}</p>
          </div>

          <div className="evidenceGrid">
            {response.evidence.map((item, index) => (
              <article className="evidenceCard" key={index}>
                <span>{item.source_type}</span>
                <h3>{item.source_name}</h3>
                <p>{item.detail}</p>
              </article>
            ))}
          </div>
        </section>
      )}
    </main>
  );
}

createRoot(document.getElementById('root')).render(<App />);
