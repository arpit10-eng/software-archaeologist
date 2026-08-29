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

  // Helper function for displaying JSON data
  const displayData = (data) => {
    if (data === undefined || data === null) {
      return "No data available";
    }

    if (
      typeof data === "string" ||
      typeof data === "number" ||
      typeof data === "boolean"
    ) {
      return String(data);
    }

    return JSON.stringify(data, null, 2);
  };

  return (
    <div className="app">

      {/* ================= HEADER ================= */}

      <header className="header">
        <h1>Software Archaeologist</h1>

        <p>
          Analyze and understand any GitHub repository
        </p>
      </header>


      {/* ================= MAIN ================= */}

      <main className="main">

        {/* ================= REPOSITORY INPUT ================= */}

        <section className="hero">

          <h2>Repository Analysis</h2>

          <p>
            Enter a GitHub repository URL to discover its
            architecture, dependencies, code quality, security,
            testing, and overall health.
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


        {/* =====================================================
            ANALYSIS DASHBOARD
        ===================================================== */}

        {result && (

          <section className="analysis-dashboard">

            <h2>Analysis Dashboard</h2>


            {/* ================= OVERVIEW ================= */}

            <h3 className="section-title">
              📊 Overview
            </h3>

            <div className="dashboard">

              {/* Health Score */}

              <div className="score-card">

                <h3>Health Score</h3>

                <div className="score">
                  {result.health_score?.overall_score ?? "--"}
                </div>

                <p>
                  {result.health_score?.health_level ?? ""}
                </p>

              </div>


              {/* Repository */}

              <div className="info-card">

                <h3>Repository</h3>

                <p>
                  {result.repository}
                </p>

              </div>


              {/* Language */}

              <div className="info-card">

                <h3>Primary Language</h3>

                <p>
                  {result.primary_language || "Unknown"}
                </p>

              </div>


              {/* Framework */}

              <div className="info-card">

                <h3>Framework</h3>

                <p>
                  {result.framework || "None detected"}
                </p>

              </div>


              {/* Branch */}

              <div className="info-card">

                <h3>Branch</h3>

                <p>
                  {result.branch || "main"}
                </p>

              </div>


              {/* Entry Point */}

              <div className="info-card">

                <h3>Entry Point</h3>

                <p>
                  {displayData(result.entry_point)}
                </p>

              </div>

            </div>


            {/* ================= SUMMARY ================= */}

            <div className="result-card full-width">

              <h3>📝 Repository Summary</h3>

              <pre>
                {displayData(result.summary)}
              </pre>

            </div>


            {/* =================================================
                CODE ANALYSIS
            ================================================= */}

            <h3 className="section-title">
              💻 Code Analysis
            </h3>

            <div className="result-grid">


              {/* Architecture */}

              <div className="result-card">

                <h3>🏗 Architecture</h3>

                <pre>
                  {displayData(result.architecture)}
                </pre>

              </div>


              {/* Code Structure */}

              <div className="result-card">

                <h3>📁 Code Structure</h3>

                <pre>
                  {displayData(result.code_structure)}
                </pre>

              </div>


              {/* Complexity */}

              <div className="result-card">

                <h3>📈 Complexity</h3>

                <pre>
                  {displayData(result.complexity)}
                </pre>

              </div>


              {/* Code Smells */}

              <div className="result-card">

                <h3>⚠️ Code Smells</h3>

                <pre>
                  {displayData(result.code_smells)}
                </pre>

              </div>


              {/* Dead Code */}

              <div className="result-card">

                <h3>🗑 Dead Code</h3>

                <pre>
                  {displayData(result.dead_code)}
                </pre>

              </div>


              {/* Maintainability */}

              <div className="result-card">

                <h3>🔧 Maintainability</h3>

                <pre>
                  {displayData(result.maintainability)}
                </pre>

              </div>

            </div>


            {/* =================================================
                DEPENDENCIES
            ================================================= */}

            <h3 className="section-title">
              📦 Dependencies
            </h3>

            <div className="result-grid">


              {/* Dependencies */}

              <div className="result-card">

                <h3>📦 Dependencies</h3>

                <pre>
                  {displayData(result.dependencies)}
                </pre>

              </div>


              {/* Dependency Graph */}

              <div className="result-card">

                <h3>🔗 Dependency Graph</h3>

                <pre>
                  {displayData(result.dependency_graph)}
                </pre>

              </div>


              {/* Circular Dependencies */}

              <div className="result-card">

                <h3>🔄 Circular Dependencies</h3>

                <pre>
                  {displayData(
                    result.circular_dependencies
                  )}
                </pre>

              </div>

            </div>


            {/* =================================================
                API
            ================================================= */}

            <h3 className="section-title">
              🌐 API Analysis
            </h3>

            <div className="result-card">

              <h3>🚀 API Endpoints</h3>

              <pre>
                {displayData(result.api_endpoints)}
              </pre>

            </div>


            {/* =================================================
                QUALITY
            ================================================= */}

            <h3 className="section-title">
              ⭐ Code Quality
            </h3>

            <div className="result-grid">


              {/* Quality Report */}

              <div className="result-card">

                <h3>📊 Quality Report</h3>

                <pre>
                  {displayData(result.quality_report)}
                </pre>

              </div>


              {/* Repository Metrics */}

              <div className="result-card">

                <h3>📐 Repository Metrics</h3>

                <pre>
                  {displayData(
                    result.repository_metrics
                  )}
                </pre>

              </div>

            </div>


            {/* =================================================
                SECURITY
            ================================================= */}

            <h3 className="section-title">
              🔐 Security
            </h3>

            <div className="result-grid">


              {/* Security Issues */}

              <div className="result-card">

                <h3>🚨 Security Issues</h3>

                <pre>
                  {displayData(
                    result.security_issues
                  )}
                </pre>

              </div>


              {/* Security Summary */}

              <div className="result-card">

                <h3>🛡 Security Summary</h3>

                <pre>
                  {displayData(
                    result.security_summary
                  )}
                </pre>

              </div>


              {/* Secret Exposure */}

              <div className="result-card">

                <h3>🔑 Secret Exposure</h3>

                <pre>
                  {displayData(
                    result.secret_exposure
                  )}
                </pre>

              </div>

            </div>


            {/* =================================================
                DOCUMENTATION & TESTING
            ================================================= */}

            <h3 className="section-title">
              🧪 Documentation & Testing
            </h3>

            <div className="result-grid">


              {/* Documentation */}

              <div className="result-card">

                <h3>📚 Documentation</h3>

                <pre>
                  {displayData(
                    result.documentation
                  )}
                </pre>

              </div>


              {/* Tests */}

              <div className="result-card">

                <h3>🧪 Tests</h3>

                <pre>
                  {displayData(result.tests)}
                </pre>

              </div>


              {/* CI/CD */}

              <div className="result-card">

                <h3>⚙️ CI/CD</h3>

                <pre>
                  {displayData(result.ci_cd)}
                </pre>

              </div>


              {/* Configuration */}

              <div className="result-card">

                <h3>⚙️ Configuration</h3>

                <pre>
                  {displayData(
                    result.configuration
                  )}
                </pre>

              </div>

            </div>


            {/* =================================================
                REPOSITORY INFORMATION
            ================================================= */}

            <h3 className="section-title">
              📂 Repository Information
            </h3>

            <div className="result-grid">


              {/* Repository Size */}

              <div className="result-card">

                <h3>📏 Repository Size</h3>

                <pre>
                  {displayData(
                    result.repository_size
                  )}
                </pre>

              </div>


              {/* License */}

              <div className="result-card">

                <h3>📜 License</h3>

                <pre>
                  {displayData(result.license)}
                </pre>

              </div>


              {/* Community */}

              <div className="result-card">

                <h3>👥 Community</h3>

                <pre>
                  {displayData(result.community)}
                </pre>

              </div>

            </div>


            {/* =================================================
                AI RECOMMENDATIONS
            ================================================= */}

            <h3 className="section-title">
              🤖 AI Recommendations
            </h3>

            <div className="result-card ai-card">

              <h3>
                Recommended Improvements
              </h3>

              <pre>
                {displayData(
                  result.ai_recommendations
                )}
              </pre>

            </div>


            {/* =================================================
                ANALYZER VERSION
            ================================================= */}

            <div className="analyzer-version">

              Analyzer Version:{" "}
              {result.analyzer_version || "2.0.0"}

            </div>

          </section>
        )}


        {/* =====================================================
            FEATURES - BEFORE ANALYSIS
        ===================================================== */}

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


      {/* ================= FOOTER ================= */}

      <footer>

        <p>
          Software Archaeologist • Repository
          Intelligence Platform
        </p>

      </footer>

    </div>
  );
}

export default App;