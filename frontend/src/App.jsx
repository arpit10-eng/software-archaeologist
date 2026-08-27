import { useState } from "react";
import "./App.css";

function App() {
  const [githubUrl, setGithubUrl] = useState("");
  const [branch, setBranch] = useState("main");

  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const analyzeRepository = async () => {
    if (!githubUrl.trim()) {
      setError("Please enter a GitHub repository URL.");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/repository/analyze",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            github_url: githubUrl,
            branch: branch,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Repository analysis failed."
        );
      }

      setResult(data);

    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">

      <header className="header">
        <h1>Software Archaeologist</h1>
        <p>
          Analyze and understand any GitHub repository
        </p>
      </header>

      <main className="main">

        <section className="hero">

          <h2>Repository Analysis</h2>

          <p>
            Enter a GitHub repository URL to discover its
            architecture, dependencies, code quality, security,
            and overall health.
          </p>

          <div className="repository-form">

            <input
              type="text"
              placeholder="https://github.com/username/repository"
              value={githubUrl}
              onChange={(e) => setGithubUrl(e.target.value)}
            />

            <select
              value={branch}
              onChange={(e) => setBranch(e.target.value)}
            >
              <option value="main">main</option>
              <option value="master">master</option>
            </select>

            <button
              onClick={analyzeRepository}
              disabled={loading}
            >
              {loading ? "Analyzing..." : "Analyze Repository"}
            </button>

          </div>

          {error && (
            <div className="error">
              {error}
            </div>
          )}

        </section>

        {result && (
          <>
            <section className="dashboard">

              <div className="score-card">
                <h3>Health Score</h3>

                <div className="score">
                  {result.health_score?.overall_score ?? "--"}
                </div>

                <p>
                  {result.health_score?.health_level ?? ""}
                </p>
              </div>

              <div className="info-card">
                <h3>Repository</h3>
                <p>{result.repository}</p>
              </div>

              <div className="info-card">
                <h3>Language</h3>
                <p>{result.primary_language}</p>
              </div>

              <div className="info-card">
                <h3>Framework</h3>
                <p>{result.framework}</p>
              </div>

            </section>

            <section className="results">

              <h2>Analysis Results</h2>

              <div className="result-card">
                <h3>Architecture</h3>

                <pre>
                  {JSON.stringify(
                    result.architecture,
                    null,
                    2
                  )}
                </pre>
              </div>

              <div className="result-card">
                <h3>Security Summary</h3>

                <pre>
                  {JSON.stringify(
                    result.security_summary,
                    null,
                    2
                  )}
                </pre>
              </div>

              <div className="result-card">
                <h3>AI Recommendations</h3>

                <pre>
                  {JSON.stringify(
                    result.ai_recommendations,
                    null,
                    2
                  )}
                </pre>
              </div>

            </section>
          </>
        )}

        {!result && (
          <section className="features">

            <h2>
              What Software Archaeologist Analyzes
            </h2>

            <div className="feature-grid">

              <div className="feature-card">
                <h3>🏗 Architecture</h3>
                <p>
                  Detects the structure and architecture
                  of the repository.
                </p>
              </div>

              <div className="feature-card">
                <h3>🔐 Security</h3>
                <p>
                  Identifies potential security issues
                  and exposed secrets.
                </p>
              </div>

              <div className="feature-card">
                <h3>📊 Code Quality</h3>
                <p>
                  Analyzes complexity, code smells
                  and maintainability.
                </p>
              </div>

              <div className="feature-card">
                <h3>🧪 Testing</h3>
                <p>
                  Examines the repository's testing
                  structure and quality.
                </p>
              </div>

              <div className="feature-card">
                <h3>📦 Dependencies</h3>
                <p>
                  Detects dependencies and builds
                  a dependency graph.
                </p>
              </div>

              <div className="feature-card">
                <h3>🤖 AI Recommendations</h3>
                <p>
                  Generates recommendations for
                  improving the repository.
                </p>
              </div>

            </div>

          </section>
        )}

      </main>

      <footer>
        <p>
          Software Archaeologist • Repository Intelligence Platform
        </p>
      </footer>

    </div>
  );
}

export default App;