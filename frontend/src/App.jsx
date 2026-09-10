import { useEffect, useMemo, useState } from "react";
import "./App.css";

const API_BASE =
  import.meta.env.VITE_API_BASE_URL ||
  (import.meta.env.DEV
    ? "http://127.0.0.1:8000"
    : "https://software-archaeologist-api.onrender.com");

function getCategoryScores(analysis) {
  if (!analysis) {
    return {};
  }

  if (
    analysis.category_percentages &&
    typeof analysis.category_percentages === "object"
  ) {
    return analysis.category_percentages;
  }

  if (
    analysis.health_score?.category_percentages &&
    typeof analysis.health_score.category_percentages === "object"
  ) {
    return analysis.health_score.category_percentages;
  }

  if (
    analysis.health?.category_percentages &&
    typeof analysis.health.category_percentages === "object"
  ) {
    return analysis.health.category_percentages;
  }

  return {};
}

function getLanguageData(analysis) {
  if (!analysis) {
    return {};
  }

  if (
    analysis.languages &&
    typeof analysis.languages === "object"
  ) {
    return analysis.languages;
  }

  if (
    analysis.language_distribution &&
    typeof analysis.language_distribution === "object"
  ) {
    return analysis.language_distribution;
  }

  return {};
}

/*
 * =========================================================
 * CODE STRUCTURE
 * =========================================================
 *
 * Supports:
 *
 * analysis.total_functions
 * analysis.total_classes
 *
 * OR:
 *
 * analysis.code_structure.total_functions
 * analysis.code_structure.total_classes
 *
 * OR, as a fallback:
 *
 * analysis.code_structure.functions.length
 * analysis.code_structure.classes.length
 */
function getCodeStructure(analysis) {
  if (!analysis) {
    return {
      totalFunctions: null,
      totalClasses: null,
    };
  }

  const codeStructure =
    analysis.code_structure ||
    analysis.codeStructure ||
    {};

  let totalFunctions =
    analysis.total_functions ??
    analysis.totalFunctions ??
    codeStructure.total_functions ??
    codeStructure.totalFunctions ??
    null;

  let totalClasses =
    analysis.total_classes ??
    analysis.totalClasses ??
    codeStructure.total_classes ??
    codeStructure.totalClasses ??
    null;

  /*
   * Final fallback:
   * If only the arrays are available, calculate their lengths.
   */
  if (
    totalFunctions === null &&
    Array.isArray(codeStructure.functions)
  ) {
    totalFunctions = codeStructure.functions.length;
  }

  if (
    totalClasses === null &&
    Array.isArray(codeStructure.classes)
  ) {
    totalClasses = codeStructure.classes.length;
  }

  return {
    totalFunctions,
    totalClasses,
  };
}

function getDependencyGraph(analysis) {
  if (!analysis) {
    return null;
  }

  return (
    analysis.dependency_graph ??
    analysis.dependencyGraph ??
    analysis.dependencies_graph ??
    null
  );
}

function App() {
  const [repositoryUrl, setRepositoryUrl] = useState("");
  const [analysis, setAnalysis] = useState(null);

  const [history, setHistory] = useState([]);
  const [historyLoading, setHistoryLoading] = useState(false);

  const [loading, setLoading] = useState(false);

  const [apiStatus, setApiStatus] = useState("checking");

  const [historyError, setHistoryError] = useState("");
  const [analysisError, setAnalysisError] = useState("");

  const [selectedAnalysisId, setSelectedAnalysisId] =
    useState(null);

  /*
   * =========================================================
   * HEALTH SCORE
   * =========================================================
   */

  const healthScore = useMemo(() => {
    if (!analysis) {
      return null;
    }

    const score =
      typeof analysis.health_score === "number"
        ? analysis.health_score
        : analysis.health_score?.overall_score ??
          analysis.overall_score ??
          analysis.health?.overall_score;

    return typeof score === "number"
      ? score.toFixed(2)
      : "N/A";
  }, [analysis]);

  const healthLevel = useMemo(() => {
    if (!analysis) {
      return "Unknown";
    }

    return (
      analysis.health_score?.health_level ??
      analysis.health_level ??
      analysis.health?.health_level ??
      "Unknown"
    );
  }, [analysis]);

  const repositoryName = useMemo(() => {
    if (!analysis?.repository) {
      return "Unknown Repository";
    }

    const parts = analysis.repository
      .replace(/\/$/, "")
      .split("/");

    return parts[parts.length - 1] || "Repository";
  }, [analysis]);

  const categoryScores = useMemo(
    () => getCategoryScores(analysis),
    [analysis]
  );

  const languageData = useMemo(
    () => getLanguageData(analysis),
    [analysis]
  );

  const dependencyGraph = useMemo(
    () => getDependencyGraph(analysis),
    [analysis]
  );

  const codeStructure = useMemo(
    () => getCodeStructure(analysis),
    [analysis]
  );

  const sortedCategories = useMemo(() => {
    return Object.entries(categoryScores)
      .map(([name, value]) => [
        name,
        Number(value) || 0,
      ])
      .sort((a, b) => b[1] - a[1]);
  }, [categoryScores]);

  const sortedLanguages = useMemo(() => {
    return Object.entries(languageData)
      .map(([name, value]) => [
        name,
        Number(value) || 0,
      ])
      .sort((a, b) => b[1] - a[1]);
  }, [languageData]);

  const totalLanguageFiles = useMemo(() => {
    return sortedLanguages.reduce(
      (sum, [, value]) => sum + value,
      0
    );
  }, [sortedLanguages]);

  /*
   * =========================================================
   * API STATUS
   * =========================================================
   */

  async function checkApiStatus() {
    if (!API_BASE) {
      setApiStatus("offline");
      return;
    }

    setApiStatus("checking");

    try {
      const response = await fetch(`${API_BASE}/`, {
        method: "GET",
      });

      if (!response.ok) {
        throw new Error(
          `Backend returned ${response.status}`
        );
      }

      setApiStatus("online");
    } catch (error) {
      console.error("Backend health check failed:", error);
      setApiStatus("offline");
    }
  }

  /*
   * =========================================================
   * LOAD HISTORY
   * =========================================================
   */

  async function loadHistory() {
    setHistoryLoading(true);
    setHistoryError("");

    try {
      const response = await fetch(
        `${API_BASE}/repository/history?limit=20`
      );

      if (!response.ok) {
        throw new Error(
          `Failed to load history (${response.status})`
        );
      }

      const data = await response.json();

      setHistory(data.results || []);
    } catch (error) {
      console.error(error);

      setHistoryError(
        "Unable to load analysis history."
      );
    } finally {
      setHistoryLoading(false);
    }
  }

  /*
   * =========================================================
   * LOAD SAVED ANALYSIS
   * =========================================================
   */

  async function loadAnalysis(analysisId) {
    setLoading(true);
    setAnalysisError("");
    setSelectedAnalysisId(analysisId);

    try {
      const response = await fetch(
        `${API_BASE}/repository/history/${analysisId}`
      );

      if (!response.ok) {
        throw new Error(
          `Failed to load analysis (${response.status})`
        );
      }

      const data = await response.json();

      setAnalysis(data);
      setRepositoryUrl(data.repository || "");
    } catch (error) {
      console.error(error);

      setAnalysisError(
        "Unable to load this analysis."
      );
    } finally {
      setLoading(false);
    }
  }

  /*
   * =========================================================
   * ANALYZE REPOSITORY
   * =========================================================
   */

  async function analyzeRepository() {
    if (!repositoryUrl.trim()) {
      setAnalysisError(
        "Please enter a GitHub repository URL."
      );
      return;
    }

    setLoading(true);
    setAnalysisError("");
    setSelectedAnalysisId(null);

    try {
      const response = await fetch(
        `${API_BASE}/repository/analyze?repository_url=${encodeURIComponent(
          repositoryUrl.trim()
        )}`,
        {
          method: "POST",
        }
      );

      if (!response.ok) {
        const errorData =
          await response.json().catch(
            () => null
          );

        throw new Error(
          errorData?.detail ||
            `Analysis failed (${response.status})`
        );
      }

      const data = await response.json();

      setAnalysis(data);
      setApiStatus("online");

      await loadHistory();
    } catch (error) {
      console.error(error);

      setApiStatus("offline");

      setAnalysisError(
        error.message ||
          "Unable to analyze repository."
      );
    } finally {
      setLoading(false);
    }
  }

  /*
   * =========================================================
   * SHOW LATEST ANALYSIS
   * =========================================================
   */

  function showLatestAnalysis() {
    if (history.length === 0) {
      setSelectedAnalysisId(null);
      return;
    }

    loadAnalysis(history[0].analysis_id);
  }

  /*
   * =========================================================
   * INITIAL LOAD
   * =========================================================
   */

  useEffect(() => {
  const timer = setTimeout(() => {
    loadHistory();
    checkApiStatus();
  }, 0);

  return () => clearTimeout(timer);
}, []);

  /*
   * =========================================================
   * API STATUS DISPLAY
   * =========================================================
   */

  const apiStatusLabel =
    apiStatus === "online"
      ? "Backend: Online"
      : apiStatus === "offline"
        ? "Backend: Offline"
        : "Backend: Checking...";

  const apiStatusStyle = {
    display: "inline-flex",
    alignItems: "center",
    gap: "7px",
    padding: "6px 10px",
    borderRadius: "999px",
    fontSize: "12px",
    fontWeight: "600",
    border: "1px solid",
    background:
      apiStatus === "online"
        ? "rgba(34, 197, 94, 0.10)"
        : apiStatus === "offline"
          ? "rgba(239, 68, 68, 0.10)"
          : "rgba(234, 179, 8, 0.10)",
    borderColor:
      apiStatus === "online"
        ? "rgba(34, 197, 94, 0.30)"
        : apiStatus === "offline"
          ? "rgba(239, 68, 68, 0.30)"
          : "rgba(234, 179, 8, 0.30)",
    color:
      apiStatus === "online"
        ? "#16a34a"
        : apiStatus === "offline"
          ? "#dc2626"
          : "#ca8a04",
  };

  const apiStatusDotStyle = {
    width: "7px",
    height: "7px",
    borderRadius: "50%",
    background:
      apiStatus === "online"
        ? "#16a34a"
        : apiStatus === "offline"
          ? "#dc2626"
          : "#ca8a04",
  };

  return (
    <div className="app">

      {/* Header */}

      <header className="topbar">
        <div>
          <h1>Software Archaeologist</h1>

          <p>
            Repository intelligence and code health analysis
          </p>
        </div>

        <div
          style={apiStatusStyle}
          title={
            apiStatus === "online"
              ? "The FastAPI backend is reachable."
              : apiStatus === "offline"
                ? "The FastAPI backend is unavailable."
                : "Checking backend availability."
          }
        >
          <span style={apiStatusDotStyle} />

          {apiStatusLabel}
        </div>
      </header>

      <main className="container">

        {/* Analyze Repository */}

        <section className="analysis-section">
          <div className="section-heading">
            <div>
              <h2>Analyze Repository</h2>

              <p>
                Enter a public GitHub repository to inspect
                its architecture, code health, dependencies,
                security, and maintainability.
              </p>
            </div>
          </div>

          <div className="analysis-form">
            <input
              type="text"
              value={repositoryUrl}
              onChange={(event) =>
                setRepositoryUrl(event.target.value)
              }
              placeholder="https://github.com/username/repository"
              disabled={loading}
            />

            <button
              onClick={analyzeRepository}
              disabled={loading}
            >
              {loading
                ? "Analyzing..."
                : "Analyze Repository"}
            </button>
          </div>

          {analysisError && (
            <div className="error-message">
              {analysisError}
            </div>
          )}
        </section>

        {/* Repository Dashboard */}

        {analysis && (
          <>
            {/* Repository Header */}

            <section className="repository-header">
              <div>
                <p className="eyebrow">
                  Repository Analysis
                </p>

                <h2>{repositoryName}</h2>

                <p className="repository-url">
                  {analysis.repository}
                </p>
              </div>

              <div className="repository-meta">

                <span>
                  Branch:{" "}
                  <strong>
                    {analysis.branch || "Unknown"}
                  </strong>
                </span>

                <span>
                  Language:{" "}
                  <strong>
                    {analysis.primary_language ||
                      "Unknown"}
                  </strong>
                </span>

                {analysis.created_at && (
                  <span>
                    Analyzed:{" "}
                    <strong>
                      {new Date(
                        analysis.created_at
                      ).toLocaleString()}
                    </strong>
                  </span>
                )}

              </div>
            </section>

            {/* Health Score */}

            <section className="score-section">

              <div className="score-card">

                <p>
                  Overall Health Score
                </p>

                <div className="score-value">
                  {healthScore}
                </div>

                <span className="health-level">
                  {healthLevel}
                </span>

              </div>

              <div className="score-info">

                <h3>
                  Repository Health
                </h3>

                <p>
                  This score summarizes the repository's
                  overall engineering health across security,
                  testing, documentation, maintainability,
                  architecture, and other analysis categories.
                </p>

              </div>

            </section>

            {/* Basic Metrics */}

            <section className="metrics-grid">

              <MetricCard
                title="Python Files"
                value={
                  analysis.total_python_files ??
                  "N/A"
                }
              />

              <MetricCard
                title="Total Lines"
                value={
                  analysis.total_lines ??
                  "N/A"
                }
              />

              <MetricCard
                title="Functions"
                value={
                  codeStructure.totalFunctions ??
                  "N/A"
                }
              />

              <MetricCard
                title="Classes"
                value={
                  codeStructure.totalClasses ??
                  "N/A"
                }
              />

            </section>

            {/* Analytics */}

            <section className="analytics-section">

              <div className="section-heading">
                <div>

                  <h2>
                    Repository Analytics
                  </h2>

                  <p>
                    Visual breakdown of repository
                    health, languages, complexity,
                    and repository size.
                  </p>

                </div>
              </div>

              <div className="analytics-grid">

                {/* Health Categories */}

                <div className="analytics-card">

                  <div className="analytics-card-header">

                    <h3>
                      Health Categories
                    </h3>

                    <span>
                      Score
                    </span>

                  </div>

                  {sortedCategories.length === 0 ? (

                    <div className="chart-empty">
                      No category data available.
                    </div>

                  ) : (

                    <div className="bar-chart">

                      {sortedCategories.map(
                        ([category, score]) => (

                          <div
                            className="bar-row"
                            key={category}
                          >

                            <div className="bar-label">

                              <span>
                                {formatCategoryName(
                                  category
                                )}
                              </span>

                              <strong>
                                {score.toFixed(1)}
                              </strong>

                            </div>

                            <div className="bar-track">

                              <div
                                className="bar-fill"
                                style={{
                                  width: `${Math.min(
                                    Math.max(
                                      score,
                                      0
                                    ),
                                    100
                                  )}%`,
                                }}
                              />

                            </div>

                          </div>

                        )
                      )}

                    </div>

                  )}

                </div>

                {/* Languages */}

                <div className="analytics-card">

                  <div className="analytics-card-header">

                    <h3>
                      Language Distribution
                    </h3>

                    <span>
                      Files
                    </span>

                  </div>

                  {sortedLanguages.length === 0 ? (

                    <div className="chart-empty">
                      No language data available.
                    </div>

                  ) : (

                    <div className="language-chart">

                      {sortedLanguages.map(
                        ([language, count]) => {

                          const percentage =
                            totalLanguageFiles > 0
                              ? (count /
                                  totalLanguageFiles) *
                                100
                              : 0;

                          return (

                            <div
                              className="language-row"
                              key={language}
                            >

                              <div className="language-info">

                                <span>
                                  {language}
                                </span>

                                <strong>
                                  {count}
                                </strong>

                              </div>

                              <div className="language-track">

                                <div
                                  className="language-fill"
                                  style={{
                                    width: `${percentage}%`,
                                  }}
                                />

                              </div>

                              <span className="language-percentage">

                                {percentage.toFixed(
                                  1
                                )}

                                %

                              </span>

                            </div>

                          );
                        }
                      )}

                    </div>

                  )}

                </div>

              </div>

              {/* Complexity */}

              <div className="analytics-grid metrics-analytics">

                <AnalyticsMetric
                  title="Cyclomatic Complexity"
                  value={
                    analysis.total_cyclomatic_complexity ??
                    analysis.complexity
                      ?.total_cyclomatic_complexity ??
                    "N/A"
                  }
                />

                <AnalyticsMetric
                  title="Average Complexity"
                  value={
                    analysis.average_cyclomatic_complexity ??
                    analysis.complexity
                      ?.average_cyclomatic_complexity ??
                    "N/A"
                  }
                />

                <AnalyticsMetric
                  title="Largest File"
                  value={
                    analysis.largest_file_lines
                      ? `${analysis.largest_file_lines} lines`
                      : "N/A"
                  }
                />

                <AnalyticsMetric
                  title="Repository Size"
                  value={formatBytes(
                    analysis.total_size_bytes
                  )}
                />

              </div>

            </section>

            {/* Dependency Graph */}

            <DependencyGraph
              graph={dependencyGraph}
            />

            {/* Code Explorer */}

            <CodeExplorer
              analysis={analysis}
            />

            <FindingsSection
              findings={analysis.findings || []}
            />

            <RecommendationsSection
              recommendations={analysis.ai_recommendations || []}
            />

          </>
        )}

        {/* History */}

        <section className="history-section">

          <div className="section-heading">

            <div>

              <h2>
                Analysis History
              </h2>

              <p>
                Previous repository analyses saved
                in the database.
              </p>

            </div>

            <button
              className="secondary-button"
              onClick={loadHistory}
              disabled={historyLoading}
            >
              {historyLoading
                ? "Refreshing..."
                : "Refresh"}
            </button>

          </div>

          {historyError && (
            <div className="error-message">
              {historyError}
            </div>
          )}

          {historyLoading &&
          history.length === 0 ? (

            <div className="empty-state">
              Loading analysis history...
            </div>

          ) : history.length === 0 ? (

            <div className="empty-state">
              No previous analyses found.
            </div>

          ) : (

            <div className="history-list">

              {history.map((item) => (

                <button
                  key={item.analysis_id}
                  className={`history-item ${
                    selectedAnalysisId ===
                    item.analysis_id
                      ? "selected"
                      : ""
                  }`}
                  onClick={() =>
                    loadAnalysis(
                      item.analysis_id
                    )
                  }
                >

                  <div className="history-main">

                    <strong>
                      {getRepositoryName(
                        item.repository
                      )}
                    </strong>

                    <span>
                      {item.repository}
                    </span>

                  </div>

                  <div className="history-details">

                    <span>
                      {item.branch ||
                        "Unknown branch"}
                    </span>

                    <span>
                      {item.primary_language ||
                        "Unknown language"}
                    </span>

                    <span>
                      {formatDate(
                        item.created_at
                      )}
                    </span>

                  </div>

                  <div className="history-id">
                    #{item.analysis_id}
                  </div>

                </button>

              ))}

            </div>

          )}

          {selectedAnalysisId !== null && (

            <button
              className="latest-button"
              onClick={
                showLatestAnalysis
              }
            >
              View Latest Analysis
            </button>

          )}

        </section>

      </main>

    </div>
  );
}

/* =========================================================
   FINDINGS
========================================================= */

function FindingsSection({ findings }) {
  const severityOrder = {
    Critical: 0,
    High: 1,
    Medium: 2,
    Low: 3,
    Info: 4,
  };

  const sorted = [...findings].sort(
    (a, b) =>
      (severityOrder[a.severity] ?? 9) -
      (severityOrder[b.severity] ?? 9)
  );

  return (
    <section className="findings-section">

      <div className="section-heading">

        <div>
          <h2>Detailed Findings</h2>

          <p>
            Evidence-backed issues detected during
            repository analysis.
          </p>
        </div>

        <span className="finding-count">
          {sorted.length} findings
        </span>

      </div>

      {sorted.length === 0 ? (

        <div className="empty-state">
          No actionable findings were detected.
        </div>

      ) : (

        <div className="findings-list">

          {sorted.map((item, index) => (

            <article
              className="finding-card"
              key={`${item.category}-${item.title}-${index}`}
            >

              <div className="finding-topline">

                <span
                  className={`severity severity-${String(
                    item.severity || "Medium"
                  ).toLowerCase()}`}
                >
                  {item.severity}
                </span>

                <span className="finding-category">
                  {item.category}
                </span>

              </div>

              <h3>
                {item.title}
              </h3>

              <p>
                {item.description}
              </p>

              {item.evidence?.length > 0 && (

                <div className="evidence">

                  <strong>
                    Evidence
                  </strong>

                  {item.evidence.map(
                    (evidence, i) => (
                      <code key={i}>
                        {evidence}
                      </code>
                    )
                  )}

                </div>

              )}

              {item.recommendation && (

                <div className="finding-action">

                  <strong>
                    Recommended action:
                  </strong>{" "}
                  {item.recommendation}

                </div>

              )}

            </article>

          ))}

        </div>

      )}

    </section>
  );
}

function RecommendationsSection({
  recommendations,
}) {
  return (
    <section className="recommendations-section">

      <div className="section-heading">

        <div>
          <h2>AI Recommendations</h2>

          <p>
            Prioritized recommendations generated
            from detected evidence and scores.
          </p>
        </div>

        <span className="finding-count">
          {recommendations.length} recommendations
        </span>

      </div>

      {recommendations.length === 0 ? (

        <div className="empty-state">
          No additional recommendations are required.
        </div>

      ) : (

        <div className="recommendations-list">

          {recommendations.map(
            (item, index) => (

              <article
                className="recommendation-card"
                key={`${item.category}-${item.title}-${index}`}
              >

                <div className="recommendation-header">

                  <div>

                    <span
                      className={`priority priority-${String(
                        item.priority || "Medium"
                      ).toLowerCase()}`}
                    >
                      {item.priority}
                    </span>

                    <span className="finding-category">
                      {item.category}
                    </span>

                  </div>

                  <span>
                    #{index + 1}
                  </span>

                </div>

                <h3>
                  {item.title}
                </h3>

                <p>
                  {item.description}
                </p>

                {item.evidence?.length > 0 && (

                  <div className="recommendation-evidence">

                    {item.evidence.map(
                      (evidence, i) => (
                        <span key={i}>
                          {evidence}
                        </span>
                      )
                    )}

                  </div>

                )}

                {item.action && (

                  <div className="finding-action">

                    <strong>
                      Next step:
                    </strong>{" "}
                    {item.action}

                  </div>

                )}

              </article>

            )
          )}

        </div>

      )}

    </section>
  );
}

/* =========================================================
   DEPENDENCY GRAPH
========================================================= */

function DependencyGraph({ graph }) {

  const [selectedNode, setSelectedNode] =
    useState(null);

  const normalizedGraph = useMemo(
    () => normalizeGraph(graph),
    [graph]
  );

  if (
    normalizedGraph.nodes.length === 0
  ) {

    return (

      <section className="dependency-section">

        <div className="section-heading">

          <div>

            <h2>
              Dependency Graph
            </h2>

            <p>
              Visual representation of
              relationships between repository
              files and modules.
            </p>

          </div>

        </div>

        <div className="graph-empty">
          No dependency relationships were
          detected.
        </div>

      </section>

    );
  }

  const positions = calculateNodePositions(
    normalizedGraph.nodes
  );

  return (

    <section className="dependency-section">

      <div className="section-heading">

        <div>

          <h2>
            Dependency Graph
          </h2>

          <p>
            Click a module to inspect its
            dependency relationships.
          </p>

        </div>

        <div className="graph-stats">

          <span>
            {normalizedGraph.nodes.length} nodes
          </span>

          <span>
            {normalizedGraph.edges.length} edges
          </span>

        </div>

      </div>

      <div className="dependency-graph-container">

        <svg
          className="dependency-graph"
          viewBox="0 0 1000 600"
          preserveAspectRatio="xMidYMid meet"
        >

          <defs>

            <marker
              id="arrow"
              markerWidth="8"
              markerHeight="8"
              refX="7"
              refY="4"
              orient="auto"
              markerUnits="strokeWidth"
            >

              <path
                d="M 0 0 L 8 4 L 0 8 z"
                fill="currentColor"
              />

            </marker>

          </defs>

          <g className="graph-edges">

            {normalizedGraph.edges.map(
              (edge, index) => {

                const source =
                  positions[edge.source];

                const target =
                  positions[edge.target];

                if (
                  !source ||
                  !target
                ) {
                  return null;
                }

                return (

                  <line
                    key={`edge-${index}`}
                    x1={source.x}
                    y1={source.y}
                    x2={target.x}
                    y2={target.y}
                    className={
                      selectedNode ===
                        edge.source ||
                      selectedNode ===
                        edge.target
                        ? "graph-edge highlighted"
                        : "graph-edge"
                    }
                    markerEnd="url(#arrow)"
                  />

                );
              }
            )}

          </g>

          <g className="graph-nodes">

            {normalizedGraph.nodes.map(
              (node) => {

                const position =
                  positions[node.id];

                if (!position) {
                  return null;
                }

                const isSelected =
                  selectedNode ===
                  node.id;

                return (

                  <g
                    key={node.id}
                    className={
                      isSelected
                        ? "graph-node selected"
                        : "graph-node"
                    }
                    transform={`translate(${position.x}, ${position.y})`}
                    onClick={() =>
                      setSelectedNode(
                        node.id
                      )
                    }
                  >

                    <circle
                      r="24"
                    />

                    <text
                      y="42"
                      textAnchor="middle"
                    >
                      {shortenNodeName(
                        node.label
                      )}
                    </text>

                  </g>

                );
              }
            )}

          </g>

        </svg>

      </div>

      {selectedNode && (

        <div className="selected-node">

          <div>

            <span>
              Selected Module
            </span>

            <strong>
              {selectedNode}
            </strong>

          </div>

          <div className="selected-node-connections">

            <div>

              <span>
                Depends on
              </span>

              <strong>
                {
                  normalizedGraph.edges.filter(
                    (edge) =>
                      edge.source ===
                      selectedNode
                  ).length
                }
              </strong>

            </div>

            <div>

              <span>
                Used by
              </span>

              <strong>
                {
                  normalizedGraph.edges.filter(
                    (edge) =>
                      edge.target ===
                      selectedNode
                  ).length
                }
              </strong>

            </div>

          </div>

        </div>

      )}

    </section>
  );
}

/* =========================================================
   CODE EXPLORER
========================================================= */

function CodeExplorer({ analysis }) {

  const [searchTerm, setSearchTerm] =
    useState("");

  const [selectedFile, setSelectedFile] =
    useState(null);

  const [fileContent, setFileContent] =
    useState("");

  const [fileLoading, setFileLoading] =
    useState(false);

  const [fileError, setFileError] =
    useState("");

  const files = useMemo(() => {

    if (
      Array.isArray(
        analysis?.file_metadata
      )
    ) {
      return analysis.file_metadata;
    }

    if (
      Array.isArray(
        analysis?.files
      )
    ) {

      return analysis.files.map(
        (file) => ({
          path: file,
          extension:
            getExtension(file),
          language:
            getLanguageFromExtension(
              getExtension(file)
            ),
          size_bytes: null,
          lines: null,
        })
      );
    }

    return [];

  }, [analysis]);

  const filteredFiles = useMemo(() => {

    const term =
      searchTerm
        .trim()
        .toLowerCase();

    if (!term) {
      return files;
    }

    return files.filter(
      (file) =>
        String(
          file.path || ""
        )
          .toLowerCase()
          .includes(term) ||
        String(
          file.language || ""
        )
          .toLowerCase()
          .includes(term)
    );

  }, [files, searchTerm]);

  async function openFile(file) {

    if (!file?.path) {
      return;
    }

    setSelectedFile(file);
    setFileContent("");
    setFileError("");
    setFileLoading(true);

    try {

      const params = new URLSearchParams({
        repository:
          analysis.repository || "",
        branch:
          analysis.branch || "main",
        path: file.path,
      });

      const response = await fetch(
        `${API_BASE}/repository/file?${params.toString()}`
      );

      if (!response.ok) {

        const errorData =
          await response
            .json()
            .catch(() => null);

        throw new Error(
          errorData?.detail ||
            `Unable to load file (${response.status})`
        );
      }

      const data =
        await response.json();

      setFileContent(
        data.content || ""
      );

    } catch (error) {

      console.error(error);

      setFileError(
        error.message ||
          "Unable to load file."
      );

    } finally {

      setFileLoading(false);

    }
  }

  return (

    <section className="code-explorer-section">

      <div className="section-heading">

        <div>

          <h2>
            Code Explorer
          </h2>

          <p>
            Browse analyzed files and inspect
            their source code directly.
          </p>

        </div>

        <span className="file-count">
          {filteredFiles.length} files
        </span>

      </div>

      <div className="code-explorer">

        {/* File List */}

        <aside className="file-browser">

          <div className="file-search">

            <input
              type="text"
              value={searchTerm}
              onChange={(event) =>
                setSearchTerm(
                  event.target.value
                )
              }
              placeholder="Search files..."
            />

          </div>

          {filteredFiles.length === 0 ? (

            <div className="file-empty">
              No files found.
            </div>

          ) : (

            <div className="file-list">

              {filteredFiles.map(
                (file) => (

                  <button
                    key={file.path}
                    className={`file-item ${
                      selectedFile?.path ===
                      file.path
                        ? "selected"
                        : ""
                    }`}
                    onClick={() =>
                      openFile(file)
                    }
                  >

                    <div className="file-item-name">
                      {getFileName(
                        file.path
                      )}
                    </div>

                    <div className="file-item-path">
                      {file.path}
                    </div>

                    <div className="file-item-meta">

                      <span>
                        {file.language ||
                          "Unknown"}
                      </span>

                      {file.lines !==
                        null &&
                        file.lines !==
                        undefined && (

                          <span>
                            {file.lines} lines
                          </span>

                        )}

                    </div>

                  </button>

                )
              )}

            </div>

          )}

        </aside>

        {/* Source Viewer */}

        <div className="source-viewer">

          {!selectedFile ? (

            <div className="source-empty">

              <div>

                <h3>
                  Select a file
                </h3>

                <p>
                  Choose a file from the
                  explorer to inspect its
                  source code.
                </p>

              </div>

            </div>

          ) : (

            <>

              <div className="source-header">

                <div>

                  <strong>
                    {selectedFile.path}
                  </strong>

                  <div className="source-meta">

                    <span>
                      {selectedFile.language ||
                        "Unknown"}
                    </span>

                    {selectedFile.lines !==
                      null &&
                      selectedFile.lines !==
                      undefined && (

                        <span>
                          {selectedFile.lines} lines
                        </span>

                      )}

                    {selectedFile.size_bytes !==
                      null &&
                      selectedFile.size_bytes !==
                      undefined && (

                        <span>
                          {formatBytes(
                            selectedFile.size_bytes
                          )}
                        </span>

                      )}

                  </div>

                </div>

              </div>

              {fileLoading ? (

                <div className="source-status">
                  Loading source code...
                </div>

              ) : fileError ? (

                <div className="source-error">
                  {fileError}
                </div>

              ) : (

                <div className="source-code-container">

                  <pre className="source-code">

                    {fileContent
                      .split("\n")
                      .map(
                        (
                          line,
                          index
                        ) => (

                          <div
                            className="code-line"
                            key={index}
                          >

                            <span className="line-number">
                              {index + 1}
                            </span>

                            <span className="line-content">
                              {line ||
                                " "}
                            </span>

                          </div>

                        )
                      )}

                  </pre>

                </div>

              )}

            </>

          )}

        </div>

      </div>

    </section>
  );
}

/* =========================================================
   GRAPH HELPERS
========================================================= */

function normalizeGraph(graph) {

  if (!graph) {

    return {
      nodes: [],
      edges: [],
    };

  }

  if (
    Array.isArray(graph.nodes) &&
    Array.isArray(graph.edges)
  ) {

    return {

      nodes: graph.nodes.map(
        (node, index) => {

          if (
            typeof node === "string"
          ) {

            return {
              id: node,
              label: node,
            };

          }

          const id =
            node.id ??
            node.name ??
            node.path ??
            String(index);

          return {

            id: String(id),

            label: String(
              node.label ??
                node.name ??
                node.path ??
                id
            ),

          };

        }
      ),

      edges: graph.edges
        .map((edge) => {

          if (
            Array.isArray(edge) &&
            edge.length >= 2
          ) {

            return {

              source: String(
                edge[0]
              ),

              target: String(
                edge[1]
              ),

            };

          }

          return {

            source: String(
              edge.source ??
                edge.from ??
                ""
            ),

            target: String(
              edge.target ??
                edge.to ??
                ""
            ),

          };

        })
        .filter(
          (edge) =>
            edge.source &&
            edge.target
        ),

    };

  }

  if (
    typeof graph === "object" &&
    !Array.isArray(graph)
  ) {

    const nodes = Object.keys(graph);

    const edges = [];

    nodes.forEach((source) => {

      const dependencies =
        graph[source];

      if (
        Array.isArray(
          dependencies
        )
      ) {

        dependencies.forEach(
          (target) => {

            edges.push({

              source,

              target: String(
                target
              ),

            });

          }
        );

      }

    });

    return {

      nodes: [
        ...new Set(
          [
            ...nodes,
            ...edges.flatMap(
              (edge) => [
                edge.source,
                edge.target,
              ]
            ),
          ]
        ),
      ].map((name) => ({

        id: String(name),

        label: String(name),

      })),

      edges,

    };

  }

  return {
    nodes: [],
    edges: [],
  };
}

function calculateNodePositions(nodes) {

  const positions = {};

  const centerX = 500;
  const centerY = 300;

  const radius = Math.min(
    220,
    80 + nodes.length * 8
  );

  nodes.forEach(
    (node, index) => {

      const angle =
        (2 * Math.PI * index) /
        nodes.length;

      positions[node.id] = {

        x:
          centerX +
          radius *
            Math.cos(angle),

        y:
          centerY +
          radius *
            Math.sin(angle),

      };

    }
  );

  return positions;
}

function shortenNodeName(name) {

  if (!name) {
    return "";
  }

  const value = String(name);

  if (value.length <= 22) {
    return value;
  }

  return `${value.slice(
    0,
    19
  )}...`;
}

/* =========================================================
   GENERAL HELPERS
========================================================= */

function getExtension(path) {

  if (!path) {
    return "";
  }

  const lastDot =
    path.lastIndexOf(".");

  if (
    lastDot === -1
  ) {
    return "";
  }

  return path
    .slice(lastDot)
    .toLowerCase();
}

function getLanguageFromExtension(
  extension
) {

  const languages = {

    ".py": "Python",
    ".js": "JavaScript",
    ".jsx": "JavaScript",
    ".ts": "TypeScript",
    ".tsx": "TypeScript",
    ".java": "Java",
    ".c": "C",
    ".cpp": "C++",
    ".h": "C/C++",
    ".hpp": "C++",
    ".go": "Go",
    ".rs": "Rust",
    ".rb": "Ruby",
    ".php": "PHP",
    ".cs": "C#",
    ".swift": "Swift",
    ".kt": "Kotlin",
    ".html": "HTML",
    ".css": "CSS",
    ".sql": "SQL",

  };

  return (
    languages[extension] ||
    "Unknown"
  );
}

function getFileName(path) {

  if (!path) {
    return "Unknown";
  }

  const normalized =
    path.replace(
      /\\/g,
      "/"
    );

  const parts =
    normalized.split("/");

  return (
    parts[parts.length - 1] ||
    path
  );
}

function MetricCard({
  title,
  value,
}) {

  return (

    <div className="metric-card">

      <span>
        {title}
      </span>

      <strong>
        {value}
      </strong>

    </div>

  );

}

function AnalyticsMetric({
  title,
  value,
}) {

  return (

    <div className="analytics-metric">

      <span>
        {title}
      </span>

      <strong>
        {value}
      </strong>

    </div>

  );

}

function getRepositoryName(repository) {

  if (!repository) {
    return "Unknown Repository";
  }

  const parts = repository
    .replace(/\/$/, "")
    .split("/");

  return (
    parts[parts.length - 1] ||
    "Repository"
  );
}

function formatCategoryName(
  category
) {

  return String(category)
    .replace(/_/g, " ")
    .replace(
      /\b\w/g,
      (letter) =>
        letter.toUpperCase()
    );
}

function formatBytes(bytes) {

  if (
    bytes === null ||
    bytes === undefined ||
    Number.isNaN(
      Number(bytes)
    )
  ) {

    return "N/A";

  }

  const value = Number(bytes);

  if (value < 1024) {

    return `${value} B`;

  }

  if (
    value <
    1024 * 1024
  ) {

    return `${(
      value / 1024
    ).toFixed(1)} KB`;

  }

  if (
    value <
    1024 *
      1024 *
      1024
  ) {

    return `${(
      value /
      (1024 * 1024)
    ).toFixed(1)} MB`;

  }

  return `${(
    value /
    (1024 *
      1024 *
      1024)
  ).toFixed(1)} GB`;
}

function formatDate(date) {

  if (!date) {
    return "Unknown date";
  }

  const parsedDate =
    new Date(date);

  if (
    Number.isNaN(
      parsedDate.getTime()
    )
  ) {

    return date;

  }

  return parsedDate.toLocaleString();
}

export default App;