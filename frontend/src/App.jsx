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
        throw new Error(data.detail || "Repository analysis failed.");
      }

      setResult(data);
    } catch (err) {
      setError(err.message || "Something went wrong.");
    } finally {
      setLoading(false);
    }
  };

  const getScoreClass = (score) => {
    if (score >= 80) return "score-good";
    if (score >= 60) return "score-average";
    return "score-poor";
  };

  const getSeverityClass = (severity) => {
    if (!severity) return "";

    return severity.toLowerCase().replace(/\s+/g, "-");
  };

  const formatName = (value) => {
    if (!value) return "";

    return value
      .replace(/_/g, " ")
      .replace(/-/g, " ")
      .replace(/\b\w/g, (char) => char.toUpperCase());
  };

  const renderList = (items, emptyMessage = "None detected.") => {
    if (!items || items.length === 0) {
      return <p className="empty">{emptyMessage}</p>;
    }

    return (
      <ul className="simple-list">
        {items.map((item, index) => (
          <li key={index}>{typeof item === "string" ? item : JSON.stringify(item)}</li>
        ))}
      </ul>
    );
  };

  const renderArchitecture = () => {
    const architecture = result?.architecture;

    if (!architecture) {
      return <p className="empty">No architecture information available.</p>;
    }

    return (
      <div className="architecture-grid">
        {Object.entries(architecture).map(([key, values]) => (
          <div className="architecture-item" key={key}>
            <h4>{formatName(key)}</h4>

            {Array.isArray(values) ? (
              values.length > 0 ? (
                <ul>
                  {values.map((value, index) => (
                    <li key={index}>{value}</li>
                  ))}
                </ul>
              ) : (
                <p className="empty">None</p>
              )
            ) : (
              <p>{String(values)}</p>
            )}
          </div>
        ))}
      </div>
    );
  };

  const renderDependencyGraph = () => {
    const graph = result?.dependency_graph;

    if (!graph || Object.keys(graph).length === 0) {
      return <p className="empty">No dependency graph available.</p>;
    }

    return (
      <div className="dependency-graph">
        {Object.entries(graph).map(([file, dependencies]) => (
          <div className="dependency-node" key={file}>
            <div className="node-file">{file}</div>

            <div className="node-arrow">↓</div>

            {dependencies && dependencies.length > 0 ? (
              <div className="node-dependencies">
                {dependencies.map((dependency, index) => (
                  <span className="dependency-tag" key={index}>
                    {dependency}
                  </span>
                ))}
              </div>
            ) : (
              <span className="no-dependency">No dependencies</span>
            )}
          </div>
        ))}
      </div>
    );
  };

  const renderComplexity = () => {
    const complexity = result?.complexity;

    if (!complexity) {
      return <p className="empty">No complexity information available.</p>;
    }

    return (
      <>
        <div className="metric-grid">
          <div className="metric-card">
            <span>Total Lines</span>
            <strong>{complexity.total_lines ?? 0}</strong>
          </div>

          <div className="metric-card">
            <span>Python Files</span>
            <strong>{complexity.total_python_files ?? 0}</strong>
          </div>

          <div className="metric-card">
            <span>Total Functions</span>
            <strong>{complexity.total_functions ?? 0}</strong>
          </div>

          <div className="metric-card">
            <span>Total Classes</span>
            <strong>{complexity.total_classes ?? 0}</strong>
          </div>

          <div className="metric-card">
            <span>Total Cyclomatic Complexity</span>
            <strong>{complexity.total_cyclomatic_complexity ?? 0}</strong>
          </div>

          <div className="metric-card">
            <span>Average Complexity</span>
            <strong>
              {complexity.average_cyclomatic_complexity ?? 0}
            </strong>
          </div>

          <div className="metric-card">
            <span>Complexity Level</span>
            <strong>{complexity.complexity_level || "Unknown"}</strong>
          </div>

          <div className="metric-card">
            <span>Largest File</span>
            <strong>{complexity.largest_file || "Unknown"}</strong>
          </div>
        </div>

        {complexity.longest_function && (
          <div className="highlight-box">
            <h4>Longest Function</h4>
            <p>
              <strong>{complexity.longest_function.name}</strong>
              {" "}in{" "}
              <strong>{complexity.longest_function.file}</strong>
            </p>
            <p>
              Lines: {complexity.longest_function.lines}
            </p>
          </div>
        )}

        {complexity.most_complex_functions?.length > 0 && (
          <div className="table-container">
            <h4>Most Complex Functions</h4>

            <table>
              <thead>
                <tr>
                  <th>Function</th>
                  <th>File</th>
                  <th>Lines</th>
                  <th>Complexity</th>
                  <th>Severity</th>
                </tr>
              </thead>

              <tbody>
                {complexity.most_complex_functions.map((item, index) => (
                  <tr key={index}>
                    <td>{item.name}</td>
                    <td>{item.file}</td>
                    <td>{item.lines}</td>
                    <td>{item.complexity}</td>
                    <td>
                      <span
                        className={`severity ${getSeverityClass(
                          item.severity
                        )}`}
                      >
                        {item.severity || "N/A"}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {complexity.complexity_warnings?.length > 0 && (
          <div className="warning-list">
            <h4>Complexity Warnings</h4>

            {complexity.complexity_warnings.map((warning, index) => (
              <div className="warning-item" key={index}>
                <div className="warning-header">
                  <strong>{warning.function}</strong>

                  <span
                    className={`severity ${getSeverityClass(
                      warning.severity
                    )}`}
                  >
                    {warning.severity}
                  </span>
                </div>

                <p>
                  <strong>File:</strong> {warning.file}
                </p>

                <p>
                  <strong>Complexity:</strong> {warning.complexity}
                </p>

                <p>{warning.recommendation}</p>
              </div>
            ))}
          </div>
        )}
      </>
    );
  };

  const renderSecurity = () => {
    const summary = result?.security_summary;
    const issues = result?.security_issues || [];

    return (
      <>
        {summary && (
          <div className="security-summary">
            <div>
              <span>Total</span>
              <strong>{summary.total_issues ?? 0}</strong>
            </div>

            <div>
              <span>Critical</span>
              <strong>{summary.critical ?? 0}</strong>
            </div>

            <div>
              <span>High</span>
              <strong>{summary.high ?? 0}</strong>
            </div>

            <div>
              <span>Medium</span>
              <strong>{summary.medium ?? 0}</strong>
            </div>

            <div>
              <span>Low</span>
              <strong>{summary.low ?? 0}</strong>
            </div>
          </div>
        )}

        <div className="issue-list">
          {issues.length === 0 ? (
            <p className="empty">No security issues detected.</p>
          ) : (
            issues.map((issue, index) => (
              <div className="issue-card" key={index}>
                <div className="issue-header">
                  <strong>{issue.issue}</strong>

                  <span
                    className={`severity ${getSeverityClass(
                      issue.severity
                    )}`}
                  >
                    {issue.severity}
                  </span>
                </div>

                <p>
                  <strong>File:</strong> {issue.file}
                </p>

                <p>
                  <strong>Line:</strong> {issue.line}
                </p>

                <p>
                  <strong>Recommendation:</strong>{" "}
                  {issue.recommendation}
                </p>
              </div>
            ))
          )}
        </div>
      </>
    );
  };

  const renderCodeSmells = () => {
    const smells = result?.code_smells || [];

    if (smells.length === 0) {
      return <p className="empty">No code smells detected.</p>;
    }

    return (
      <div className="smell-list">
        {smells.map((smell, index) => (
          <div className="smell-card" key={index}>
            <div className="issue-header">
              <strong>{smell.issue}</strong>

              <span
                className={`severity ${getSeverityClass(
                  smell.severity
                )}`}
              >
                {smell.severity}
              </span>
            </div>

            <p>
              <strong>File:</strong> {smell.file}
            </p>

            <p>
              <strong>Recommendation:</strong>{" "}
              {smell.recommendation}
            </p>
          </div>
        ))}
      </div>
    );
  };

  const renderRecommendations = () => {
    const recommendations = result?.ai_recommendations || [];

    if (recommendations.length === 0) {
      return <p className="empty">No recommendations available.</p>;
    }

    return (
      <div className="recommendation-list">
        {recommendations.map((item, index) => (
          <div className="recommendation-card" key={index}>
            <div className="recommendation-top">
              <span className="recommendation-category">
                {item.category}
              </span>

              <span
                className={`severity ${getSeverityClass(
                  item.priority
                )}`}
              >
                {item.priority}
              </span>
            </div>

            <p>{item.recommendation}</p>
          </div>
        ))}
      </div>
    );
  };

  const renderDependencyList = () => {
    const dependencies = result?.dependencies || [];

    if (dependencies.length === 0) {
      return <p className="empty">No dependencies detected.</p>;
    }

    return (
      <div className="tag-container">
        {dependencies.map((dependency, index) => (
          <span className="tag" key={index}>
            {dependency}
          </span>
        ))}
      </div>
    );
  };

  const renderApiEndpoints = () => {
    const endpoints = result?.api_endpoints || [];

    if (endpoints.length === 0) {
      return <p className="empty">No API endpoints detected.</p>;
    }

    return (
      <div className="endpoint-list">
        {endpoints.map((endpoint, index) => (
          <div className="endpoint" key={index}>
            <span className={`method ${endpoint.method?.toLowerCase()}`}>
              {endpoint.method}
            </span>

            <code>{endpoint.path}</code>
          </div>
        ))}
      </div>
    );
  };

  const renderHealthBreakdown = () => {
    const breakdown = result?.health_score?.breakdown;

    if (!breakdown) {
      return <p className="empty">No score breakdown available.</p>;
    }

    return (
      <div className="health-breakdown">
        {Object.entries(breakdown).map(([key, value]) => (
          <div className="health-row" key={key}>
            <div className="health-label">
              <span>{formatName(key)}</span>
              <strong>{value}</strong>
            </div>

            <div className="progress">
              <div
                className="progress-fill"
                style={{
                  width: `${Math.min(Math.max(value * 10, 0), 100)}%`,
                }}
              />
            </div>
          </div>
        ))}
      </div>
    );
  };

  const renderTests = () => {
    const tests = result?.tests;

    if (!tests) {
      return <p className="empty">No test information available.</p>;
    }

    return (
      <>
        <div className="metric-grid">
          <div className="metric-card">
            <span>Test Files</span>
            <strong>{tests.test_file_count ?? 0}</strong>
          </div>

          <div className="metric-card">
            <span>Test Functions</span>
            <strong>{tests.test_function_count ?? 0}</strong>
          </div>

          <div className="metric-card">
            <span>Test Score</span>
            <strong>{tests.test_quality?.score ?? 0}</strong>
          </div>

          <div className="metric-card">
            <span>Test Quality</span>
            <strong>{tests.test_quality?.level || "Unknown"}</strong>
          </div>
        </div>

        <h4>Test Files</h4>
        {renderList(tests.test_files)}

        <h4>Test Functions</h4>
        {renderList(tests.test_functions)}
      </>
    );
  };

  const renderDocumentation = () => {
    const documentation = result?.documentation;

    if (!documentation) {
      return <p className="empty">No documentation information available.</p>;
    }

    return (
      <>
        <div className="metric-grid">
          <div className="metric-card">
            <span>Documentation Files</span>
            <strong>
              {documentation.documentation_file_count ?? 0}
            </strong>
          </div>

          <div className="metric-card">
            <span>Comments</span>
            <strong>{documentation.comments ?? 0}</strong>
          </div>

          <div className="metric-card">
            <span>Docstrings</span>
            <strong>{documentation.docstrings ?? 0}</strong>
          </div>

          <div className="metric-card">
            <span>Quality Score</span>
            <strong>
              {documentation.documentation_quality?.score ?? 0}
            </strong>
          </div>
        </div>

        <div className="highlight-box">
          <h4>
            {documentation.documentation_quality?.level || "Unknown"}
          </h4>

          <p>
            {documentation.documentation_quality?.reason ||
              "No documentation assessment available."}
          </p>
        </div>

        <h4>Documentation Files</h4>
        {renderList(documentation.documentation_files)}
      </>
    );
  };

  const renderMaintainability = () => {
    const maintainability = result?.maintainability;

    if (!maintainability) {
      return <p className="empty">No maintainability data available.</p>;
    }

    return (
      <div className="metric-grid">
        <div className="metric-card">
          <span>Excellent Files</span>
          <strong>{maintainability.excellent ?? 0}</strong>
        </div>

        <div className="metric-card">
          <span>Good Files</span>
          <strong>{maintainability.good ?? 0}</strong>
        </div>

        <div className="metric-card">
          <span>Poor Files</span>
          <strong>{maintainability.poor ?? 0}</strong>
        </div>

        <div className="metric-card">
          <span>Worst File</span>
          <strong>{maintainability.worst_file || "None"}</strong>
        </div>
      </div>
    );
  };

  const renderCommunity = () => {
    const community = result?.community;

    if (!community) {
      return <p className="empty">No community information available.</p>;
    }

    return (
      <div className="boolean-grid">
        <div className={community.contributing ? "bool yes" : "bool no"}>
          <strong>CONTRIBUTING.md</strong>
          <span>{community.contributing ? "Present" : "Missing"}</span>
        </div>

        <div className={community.code_of_conduct ? "bool yes" : "bool no"}>
          <strong>Code of Conduct</strong>
          <span>
            {community.code_of_conduct ? "Present" : "Missing"}
          </span>
        </div>

        <div
          className={
            community.pull_request_template ? "bool yes" : "bool no"
          }
        >
          <strong>Pull Request Template</strong>
          <span>
            {community.pull_request_template ? "Present" : "Missing"}
          </span>
        </div>

        <div
          className={
            community.issue_template_count > 0 ? "bool yes" : "bool no"
          }
        >
          <strong>Issue Templates</strong>
          <span>{community.issue_template_count ?? 0}</span>
        </div>
      </div>
    );
  };

  const renderConfiguration = () => {
    const configuration = result?.configuration;

    if (!configuration) {
      return <p className="empty">No configuration information available.</p>;
    }

    return (
      <div className="boolean-grid">
        <div
          className={
            configuration.env_example_found ? "bool yes" : "bool no"
          }
        >
          <strong>.env.example</strong>
          <span>
            {configuration.env_example_found ? "Found" : "Missing"}
          </span>
        </div>

        <div
          className={
            configuration.environment_file_count > 0
              ? "bool yes"
              : "bool no"
          }
        >
          <strong>Environment Files</strong>
          <span>{configuration.environment_file_count ?? 0}</span>
        </div>

        <div
          className={
            configuration.config_file_count > 0 ? "bool yes" : "bool no"
          }
        >
          <strong>Config Files</strong>
          <span>{configuration.config_file_count ?? 0}</span>
        </div>
      </div>
    );
  };

  const renderLicense = () => {
    const license = result?.license;

    if (!license) {
      return <p className="empty">No license information available.</p>;
    }

    return (
      <div className="license-box">
        <div>
          <span>License</span>
          <strong>{license.license}</strong>
        </div>

        <div>
          <span>Status</span>
          <strong>{license.status}</strong>
        </div>

        <p>{license.reason}</p>

        <h4>License Files</h4>
        {renderList(license.license_files, "No license files found.")}
      </div>
    );
  };

  const renderCiCd = () => {
    const ci = result?.ci_cd;

    if (!ci) {
      return <p className="empty">No CI/CD information available.</p>;
    }

    return (
      <div className="boolean-grid">
        <div className={ci.github_actions ? "bool yes" : "bool no"}>
          <strong>GitHub Actions</strong>
          <span>{ci.github_actions ? "Configured" : "Not Configured"}</span>
        </div>

        <div className={ci.workflow_count > 0 ? "bool yes" : "bool no"}>
          <strong>Workflow Files</strong>
          <span>{ci.workflow_count ?? 0}</span>
        </div>
      </div>
    );
  };

  const renderSecretExposure = () => {
    const secrets = result?.secret_exposure;

    if (!secrets) {
      return <p className="empty">No secret exposure information available.</p>;
    }

    return (
      <>
        <div className="boolean-grid">
          <div className={secrets.gitignore_found ? "bool yes" : "bool no"}>
            <strong>.gitignore</strong>
            <span>{secrets.gitignore_found ? "Found" : "Missing"}</span>
          </div>

          <div
            className={
              secrets.sensitive_file_count === 0 ? "bool yes" : "bool no"
            }
          >
            <strong>Sensitive Files</strong>
            <span>{secrets.sensitive_file_count ?? 0}</span>
          </div>
        </div>

        <h4>Sensitive Files</h4>
        {renderList(secrets.sensitive_files, "No sensitive files detected.")}
      </>
    );
  };

  const renderRepositorySize = () => {
    const size = result?.repository_size;

    if (!size) {
      return <p className="empty">No repository size information available.</p>;
    }

    return (
      <div className="metric-grid">
        <div className="metric-card">
          <span>Total Size</span>
          <strong>
            {(size.total_size_bytes / 1024).toFixed(2)} KB
          </strong>
        </div>

        <div className="metric-card">
          <span>Largest File</span>
          <strong>{size.largest_file}</strong>
        </div>

        <div className="metric-card">
          <span>Largest File Size</span>
          <strong>
            {(size.largest_file_size_bytes / 1024).toFixed(2)} KB
          </strong>
        </div>
      </div>
    );
  };

  const renderFiles = () => {
    const files = result?.files || [];

    if (files.length === 0) {
      return <p className="empty">No files detected.</p>;
    }

    return (
      <div className="file-list">
        {files.map((file, index) => (
          <div className="file-item" key={index}>
            <span>{file}</span>
          </div>
        ))}
      </div>
    );
  };

  return (
    <div className="app">
      <header className="header">
        <div>
          <h1>Software Archaeologist</h1>
          <p>Repository Intelligence Platform</p>
        </div>
      </header>

      <main className="main">
        <section className="hero">
          <div className="hero-content">
            <span className="eyebrow">REPOSITORY ANALYSIS</span>

            <h2>Understand Any GitHub Repository</h2>

            <p>
              Analyze architecture, dependencies, complexity, security,
              maintainability, testing, documentation and overall repository
              health.
            </p>
          </div>

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

          {error && <div className="error">{error}</div>}
        </section>

        {!result && (
          <section className="features">
            <div className="section-heading">
              <span className="eyebrow">CAPABILITIES</span>
              <h2>What Software Archaeologist Analyzes</h2>
            </div>

            <div className="feature-grid">
              <div className="feature-card">
                <div className="feature-icon">🏗️</div>
                <h3>Architecture</h3>
                <p>
                  Detect project structure, layers, services, models,
                  utilities and application organization.
                </p>
              </div>

              <div className="feature-card">
                <div className="feature-icon">📦</div>
                <h3>Dependencies</h3>
                <p>
                  Identify dependencies and visualize relationships between
                  repository files.
                </p>
              </div>

              <div className="feature-card">
                <div className="feature-icon">📊</div>
                <h3>Complexity</h3>
                <p>
                  Measure functions, classes, lines and cyclomatic
                  complexity.
                </p>
              </div>

              <div className="feature-card">
                <div className="feature-icon">🔐</div>
                <h3>Security</h3>
                <p>
                  Detect potential security problems and exposed sensitive
                  information.
                </p>
              </div>

              <div className="feature-card">
                <div className="feature-icon">🧪</div>
                <h3>Testing</h3>
                <p>
                  Analyze test files, test functions and overall test
                  quality.
                </p>
              </div>

              <div className="feature-card">
                <div className="feature-icon">🤖</div>
                <h3>AI Recommendations</h3>
                <p>
                  Generate actionable recommendations for improving the
                  repository.
                </p>
              </div>
            </div>
          </section>
        )}

        {result && (
          <div className="dashboard">
            <section className="overview-section">
              <div className="section-heading">
                <span className="eyebrow">ANALYSIS COMPLETE</span>
                <h2>Repository Overview</h2>
              </div>

              <div className="overview-grid">
                <div className="overview-card">
                  <span>Repository</span>
                  <strong>{result.repository}</strong>
                </div>

                <div className="overview-card">
                  <span>Branch</span>
                  <strong>{result.branch}</strong>
                </div>

                <div className="overview-card">
                  <span>Primary Language</span>
                  <strong>{result.primary_language}</strong>
                </div>

                <div className="overview-card">
                  <span>Framework</span>
                  <strong>{result.framework}</strong>
                </div>

                <div className="overview-card">
                  <span>Entry Point</span>
                  <strong>{result.entry_point}</strong>
                </div>

                <div className="overview-card">
                  <span>Analyzer Version</span>
                  <strong>{result.analyzer_version}</strong>
                </div>
              </div>
            </section>

            <section className="dashboard-section health-section">
              <div className="section-heading">
                <span className="eyebrow">REPOSITORY HEALTH</span>
                <h2>Health Score</h2>
              </div>

              <div className="health-layout">
                <div
                  className={`health-score ${getScoreClass(
                    result.health_score?.overall_score
                  )}`}
                >
                  <span>Overall Score</span>
                  <strong>
                    {result.health_score?.overall_score ?? "--"}
                  </strong>
                  <p>{result.health_score?.health_level}</p>
                </div>

                <div className="health-content">
                  {renderHealthBreakdown()}
                </div>
              </div>
            </section>

            <section className="dashboard-section">
              <div className="section-heading">
                <span className="eyebrow">REPOSITORY</span>
                <h2>Repository Metrics</h2>
              </div>

              <div className="metric-grid">
                <div className="metric-card">
                  <span>Total Files</span>
                  <strong>{result.total_files ?? 0}</strong>
                </div>

                <div className="metric-card">
                  <span>Python Files</span>
                  <strong>{result.python_files ?? 0}</strong>
                </div>

                <div className="metric-card">
                  <span>Directories</span>
                  <strong>
                    {result.repository_metrics?.directories ?? 0}
                  </strong>
                </div>

                <div className="metric-card">
                  <span>Average File Size</span>
                  <strong>
                    {result.repository_metrics?.average_file_size ?? 0} B
                  </strong>
                </div>

                <div className="metric-card">
                  <span>Largest Directory</span>
                  <strong>
                    {result.repository_metrics?.largest_directory ||
                      "Unknown"}
                  </strong>
                </div>

                <div className="metric-card">
                  <span>Markdown Files</span>
                  <strong>{result.markdown_files ?? 0}</strong>
                </div>
              </div>
            </section>

            <section className="dashboard-section">
              <div className="section-heading">
                <span className="eyebrow">SYSTEM DESIGN</span>
                <h2>Architecture</h2>
              </div>

              <div className="result-card">{renderArchitecture()}</div>
            </section>

            <section className="dashboard-section">
              <div className="section-heading">
                <span className="eyebrow">PACKAGE ANALYSIS</span>
                <h2>Dependencies</h2>
              </div>

              <div className="result-card">
                <h3>Detected Dependencies</h3>
                {renderDependencyList()}
              </div>
            </section>

            <section className="dashboard-section">
              <div className="section-heading">
                <span className="eyebrow">RELATIONSHIPS</span>
                <h2>Dependency Graph</h2>
              </div>

              <div className="result-card">
                {renderDependencyGraph()}
              </div>
            </section>

            <section className="dashboard-section">
              <div className="section-heading">
                <span className="eyebrow">CODE ANALYSIS</span>
                <h2>Complexity Analysis</h2>
              </div>

              <div className="result-card">{renderComplexity()}</div>
            </section>

            <section className="dashboard-section">
              <div className="section-heading">
                <span className="eyebrow">CODE STRUCTURE</span>
                <h2>Classes & Functions</h2>
              </div>

              <div className="result-card">
                <div className="structure-columns">
                  <div>
                    <h3>Classes</h3>
                    {renderList(result.code_structure?.classes)}
                  </div>

                  <div>
                    <h3>Functions</h3>
                    {renderList(result.code_structure?.functions)}
                  </div>
                </div>
              </div>
            </section>

            <section className="dashboard-section">
              <div className="section-heading">
                <span className="eyebrow">SECURITY</span>
                <h2>Security Analysis</h2>
              </div>

              <div className="result-card">{renderSecurity()}</div>
            </section>

            <section className="dashboard-section">
              <div className="section-heading">
                <span className="eyebrow">CODE QUALITY</span>
                <h2>Code Smells</h2>
              </div>

              <div className="result-card">{renderCodeSmells()}</div>
            </section>

            <section className="dashboard-section">
              <div className="section-heading">
                <span className="eyebrow">DEPENDENCY HEALTH</span>
                <h2>Circular Dependencies</h2>
              </div>

              <div className="result-card">
                <div
                  className={
                    result.circular_dependencies?.found
                      ? "status-box danger"
                      : "status-box success"
                  }
                >
                  <strong>
                    {result.circular_dependencies?.found
                      ? "Circular Dependencies Found"
                      : "No Circular Dependencies"}
                  </strong>

                  <span>
                    {result.circular_dependencies?.message}
                  </span>

                  <span>
                    Cycle Count:{" "}
                    {result.circular_dependencies?.cycle_count ?? 0}
                  </span>
                </div>

                {result.circular_dependencies?.cycles?.length > 0 && (
                  <div className="cycle-list">
                    {result.circular_dependencies.cycles.map(
                      (cycle, index) => (
                        <div className="cycle-item" key={index}>
                          {Array.isArray(cycle)
                            ? cycle.join(" → ")
                            : cycle}
                        </div>
                      )
                    )}
                  </div>
                )}
              </div>
            </section>

            <section className="dashboard-section">
              <div className="section-heading">
                <span className="eyebrow">MAINTAINABILITY</span>
                <h2>Maintainability</h2>
              </div>

              <div className="result-card">
                {renderMaintainability()}
              </div>
            </section>

            <section className="dashboard-section">
              <div className="section-heading">
                <span className="eyebrow">DOCUMENTATION</span>
                <h2>Documentation</h2>
              </div>

              <div className="result-card">
                {renderDocumentation()}
              </div>
            </section>

            <section className="dashboard-section">
              <div className="section-heading">
                <span className="eyebrow">QUALITY ASSURANCE</span>
                <h2>Testing</h2>
              </div>

              <div className="result-card">{renderTests()}</div>
            </section>

            <section className="dashboard-section">
              <div className="section-heading">
                <span className="eyebrow">REPOSITORY POLICY</span>
                <h2>License</h2>
              </div>

              <div className="result-card">{renderLicense()}</div>
            </section>

            <section className="dashboard-section">
              <div className="section-heading">
                <span className="eyebrow">DEVOPS</span>
                <h2>CI/CD</h2>
              </div>

              <div className="result-card">{renderCiCd()}</div>
            </section>

            <section className="dashboard-section">
              <div className="section-heading">
                <span className="eyebrow">OPEN SOURCE</span>
                <h2>Community</h2>
              </div>

              <div className="result-card">{renderCommunity()}</div>
            </section>

            <section className="dashboard-section">
              <div className="section-heading">
                <span className="eyebrow">CONFIGURATION</span>
                <h2>Configuration</h2>
              </div>

              <div className="result-card">{renderConfiguration()}</div>
            </section>

            <section className="dashboard-section">
              <div className="section-heading">
                <span className="eyebrow">SECRETS</span>
                <h2>Secret Exposure</h2>
              </div>

              <div className="result-card">{renderSecretExposure()}</div>
            </section>

            <section className="dashboard-section">
              <div className="section-heading">
                <span className="eyebrow">SIZE ANALYSIS</span>
                <h2>Repository Size</h2>
              </div>

              <div className="result-card">{renderRepositorySize()}</div>
            </section>

            <section className="dashboard-section">
              <div className="section-heading">
                <span className="eyebrow">API ANALYSIS</span>
                <h2>API Endpoints</h2>
              </div>

              <div className="result-card">{renderApiEndpoints()}</div>
            </section>

            <section className="dashboard-section">
              <div className="section-heading">
                <span className="eyebrow">QUALITY REPORT</span>
                <h2>Repository Quality Report</h2>
              </div>

              <div className="result-card">
                <div className="quality-columns">
                  <div>
                    <h3>Strengths</h3>
                    {renderList(
                      result.quality_report?.strengths,
                      "No strengths detected."
                    )}
                  </div>

                  <div>
                    <h3>Warnings</h3>
                    {renderList(
                      result.quality_report?.warnings,
                      "No warnings detected."
                    )}
                  </div>
                </div>
              </div>
            </section>

            <section className="dashboard-section ai-section">
              <div className="section-heading">
                <span className="eyebrow">INTELLIGENCE</span>
                <h2>AI Recommendations</h2>
              </div>

              <div className="result-card">
                {renderRecommendations()}
              </div>
            </section>

            <section className="dashboard-section">
              <div className="section-heading">
                <span className="eyebrow">SUMMARY</span>
                <h2>Repository Summary</h2>
              </div>

              <div className="summary-card">
                <p>{result.summary}</p>
              </div>
            </section>

            <section className="dashboard-section">
              <div className="section-heading">
                <span className="eyebrow">SOURCE TREE</span>
                <h2>Repository Files</h2>
              </div>

              <div className="result-card">{renderFiles()}</div>
            </section>
          </div>
        )}
      </main>

      <footer>
        <p>Software Archaeologist • Repository Intelligence Platform</p>
      </footer>
    </div>
  );
}

export default App;