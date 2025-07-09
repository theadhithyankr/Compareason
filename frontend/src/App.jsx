import React, { useState } from 'react';

function App() {
  const [query, setQuery] = useState('Samsung Galaxy M14');
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);

  const handleSearch = async () => {
    if (!query.trim()) {
      setError('Please enter a search query');
      return;
    }

    setLoading(true);
    setError(null);
    setResults(null);

    try {
      const response = await fetch('http://localhost:8000/compare', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query,
          max_results_per_site: 10,
          sites: ['flipkart', 'amazon', 'reliance']
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setResults(data);
    } catch (err) {
      setError(`Error: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{
      minHeight: '100vh',
      backgroundColor: '#f3f4f6',
      padding: '20px',
      fontFamily: 'Arial, sans-serif'
    }}>
      <div style={{
        maxWidth: '800px',
        margin: '0 auto',
        backgroundColor: 'white',
        padding: '30px',
        borderRadius: '10px',
        boxShadow: '0 2px 10px rgba(0,0,0,0.1)'
      }}>
        <h1 style={{
          textAlign: 'center',
          color: '#1f2937',
          marginBottom: '30px',
          fontSize: '2rem'
        }}>
          🛒 Compareason - Price Comparison
        </h1>

        <div style={{marginBottom: '20px'}}>
          <input
            type="text"
            placeholder="Search for products..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            style={{
              width: '100%',
              padding: '15px',
              fontSize: '16px',
              border: '2px solid #3b82f6',
              borderRadius: '8px',
              marginBottom: '15px',
              boxSizing: 'border-box'
            }}
          />

          <button
            onClick={handleSearch}
            disabled={loading}
            style={{
              width: '100%',
              padding: '15px',
              fontSize: '16px',
              backgroundColor: loading ? '#94a3b8' : '#3b82f6',
              color: 'white',
              border: 'none',
              borderRadius: '8px',
              cursor: loading ? 'not-allowed' : 'pointer',
              fontWeight: 'bold'
            }}
          >
            {loading ? 'Searching...' : 'Compare Prices'}
          </button>
        </div>

        {error && (
          <div style={{
            backgroundColor: '#fef2f2',
            color: '#dc2626',
            padding: '15px',
            borderRadius: '8px',
            marginBottom: '20px',
            border: '1px solid #fecaca'
          }}>
            {error}
          </div>
        )}

        {results && (
          <div style={{
            backgroundColor: '#f8fafc',
            padding: '20px',
            borderRadius: '8px',
            border: '1px solid #e2e8f0'
          }}>
            <h2 style={{marginBottom: '15px', color: '#1f2937'}}>Search Results:</h2>
            <pre style={{
              backgroundColor: '#1f2937',
              color: '#e5e7eb',
              padding: '15px',
              borderRadius: '6px',
              overflow: 'auto',
              fontSize: '14px',
              lineHeight: '1.5'
            }}>
              {JSON.stringify(results, null, 2)}
            </pre>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
