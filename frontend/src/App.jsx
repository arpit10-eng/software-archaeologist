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

      {/* HEADER */}

      <header className="header">
        <h1>Software Archaeologist</h1>

        <p>
          Analyze and understand any GitHub repository
        </p>
      </header>


      <main className="main">

        {/* REPOSITORY INPUT */}

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

              {loading
                ? "Analyzing..."
                : "Analyze Repository"}

            </button>

          </div>


          {error && (
            <div className="error">
              {error}
            </div>
          )}

        </section>


        {/* ========================= */}
        {/* ANALYSIS DASHBOARD */}
        {/* ========================= */}

        {result && (

          <section className="analysis-dashboard">

            <h2>Repository Analysis Dashboard</h2>


            {/* SUMMARY CARDS */}

            <div className="dashboard">

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

                <p>
                  {result.repository}
                </p>

              </div>


              <div className="info-card">

                <h3>Language</h3>

                <p>
                  {result.primary_language}
                </p>

              </div>


              <div className="info-card">

                <h3>Framework</h3>

                <p>
                  {result.framework || "Not detected"}
                </p>

              </div>

            </div>


            {/* SUMMARY */}

            <div className="result-card">

              <h3>Repository Summary</h3>

              <p>
                {result.summary}
              </p>

            </div>


            {/* BASIC INFORMATION */}

            <div className="result-grid">

              <div className="result-card">

                <h3>Entry Point</h3>

                <pre>
                  {JSON.stringify(
                    result.entry_point,
                    null,
                    2
                  )}
                </pre>

              </div>


              <div className="result-card">

                <h3>Dependencies</h3>

                <pre>
                  {JSON.stringify(
                    result.dependencies,
                    null,
                    2
                  )}
                </pre>

              </div>

            </div>


            {/* ARCHITECTURE */}

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


            {/* CODE QUALITY */}

            <div className="result-grid">

              <div className="result-card">

                <h3>Code Quality</h3>

                <pre>
                  {JSON.stringify(
                    result.quality_report,
                    null,
                    2
                  )}
                </pre>

              </div>


              <div className="result-card">

                <h3>Code Smells</h3>

                <pre>
                  {JSON.stringify(
                    result.code_smells,
                    null,
                    2
                  )}
                </pre>

              </div>

            </div>


            {/* COMPLEXITY */}

            <div className="result-grid">

              <div className="result-card">

                <h3>Complexity</h3>

                <pre>
                  {JSON.stringify(
                    result.complexity,
                    null,
                    2
                  )}
                </pre>

              </div>


              <div className="result-card">

                <h3>Maintainability</h3>

                <pre>
                  {JSON.stringify(
                    result.maintainability,
                    null,
                    2
                  )}
                </pre>

              </div>

            </div>


            {/* SECURITY */}

            <div className="result-grid">

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

                <h3>Secret Exposure</h3>

                <pre>
                  {JSON.stringify(
                    result.secret_exposure,
                    null,
                    2
                  )}
                </pre>

              </div>

            </div>


            {/* TESTING */}

            <div className="result-grid">

              <div className="result-card">

                <h3>Tests</h3>

                <pre>
                  {JSON.stringify(
                    result.tests,
                    null,
                    2
                  )}
                </pre>

              </div>


              <div className="result-card">

                <h3>Documentation</h3>

                <pre>
                  {JSON.stringify(
                    result.documentation,
                    null,
                    2
                  )}
                </pre>

              </div>

            </div>


            {/* REPOSITORY METRICS */}

            <div className="result-grid">

              <div className="result-card">

                <h3>Repository Metrics</h3>

                <pre>
                  {JSON.stringify(
                    result.repository_metrics,
                    null,
                    2
                  )}
                </pre>

              </div>


              <div className="result-card">

                <h3>Repository Size</h3>

                <pre>
                  {JSON.stringify(
                    result.repository_size,
                    null,
                    2
                  )}
                </pre>

              </div>

            </div>


            {/* CI/CD */}

            <div className="result-grid">

              <div className="result-card">

                <h3>CI/CD</h3>

                <pre>
                  {JSON.stringify(
                    result.ci_cd,
                    null,
                    2
                  )}
                </pre>

              </div>


              <div className="result-card">

                <h3>Configuration</h3>

                <pre>
                  {JSON.stringify(
                    result.configuration,
                    null,
                    2
                  )}
                </pre>

              </div>

            </div>


            {/* COMMUNITY */}

            <div className="result-card">

              <h3>Community Analysis</h3>

              <pre>
                {JSON.stringify(
                  result.community,
                  null,
                  2
                )}
              </pre>

            </div>


            {/* AI RECOMMENDATIONS */}

            <div className="result-card ai-card">

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
        )}


        {/* FEATURES */}

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