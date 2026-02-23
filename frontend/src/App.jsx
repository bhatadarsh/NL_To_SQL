import { useState, useRef, useEffect } from "react";
import {
  BarChart, Bar, LineChart, Line, PieChart, Pie, Cell,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer
} from "recharts";

const API_BASE = "http://localhost:8000";

const COLORS = ["#6EE7B7", "#34D399", "#10B981", "#059669", "#047857",
                "#A7F3D0", "#D1FAE5", "#6EE7F7", "#38BDF8", "#0EA5E9"];

// ── helpers ──────────────────────────────────────────────────────────────────

function guessChartType(columns, rows) {
  if (!columns || columns.length < 2 || !rows || rows.length === 0) return "table";
  const hasNumber = columns.some(c => typeof rows[0][c] === "number");
  if (!hasNumber) return "table";
  if (rows.length === 1) return "table";
  if (columns.length === 2) return rows.length <= 6 ? "pie" : "bar";
  return "bar";
}

function getChartAxes(columns, rows) {
  if (!columns || !rows || rows.length === 0) return {};
  const labelCol = columns.find(c => typeof rows[0][c] === "string") || columns[0];
  const valueCol = columns.find(c => typeof rows[0][c] === "number") || columns[1];
  return { labelCol, valueCol };
}

// ── sub-components ────────────────────────────────────────────────────────────

function BarViz({ columns, rows }) {
  const { labelCol, valueCol } = getChartAxes(columns, rows);
  return (
    <ResponsiveContainer width="100%" height={280}>
      <BarChart data={rows} margin={{ top: 10, right: 20, left: 0, bottom: 40 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="#1a3a2a" />
        <XAxis dataKey={labelCol} tick={{ fill: "#6EE7B7", fontSize: 11 }}
          angle={-35} textAnchor="end" interval={0} />
        <YAxis tick={{ fill: "#6EE7B7", fontSize: 11 }} />
        <Tooltip contentStyle={{ background: "#0a1f14", border: "1px solid #10B981", color: "#D1FAE5" }} />
        <Legend wrapperStyle={{ color: "#6EE7B7" }} />
        <Bar dataKey={valueCol} fill="#10B981" radius={[4, 4, 0, 0]} />
      </BarChart>
    </ResponsiveContainer>
  );
}

function LineViz({ columns, rows }) {
  const { labelCol, valueCol } = getChartAxes(columns, rows);
  return (
    <ResponsiveContainer width="100%" height={280}>
      <LineChart data={rows} margin={{ top: 10, right: 20, left: 0, bottom: 40 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="#1a3a2a" />
        <XAxis dataKey={labelCol} tick={{ fill: "#6EE7B7", fontSize: 11 }}
          angle={-35} textAnchor="end" interval={0} />
        <YAxis tick={{ fill: "#6EE7B7", fontSize: 11 }} />
        <Tooltip contentStyle={{ background: "#0a1f14", border: "1px solid #10B981", color: "#D1FAE5" }} />
        <Line type="monotone" dataKey={valueCol} stroke="#34D399" strokeWidth={2} dot={{ fill: "#6EE7B7" }} />
      </LineChart>
    </ResponsiveContainer>
  );
}

function PieViz({ columns, rows }) {
  const { labelCol, valueCol } = getChartAxes(columns, rows);
  return (
    <ResponsiveContainer width="100%" height={280}>
      <PieChart>
        <Pie data={rows} dataKey={valueCol} nameKey={labelCol}
          cx="50%" cy="50%" outerRadius={100} label={({ name, percent }) =>
            `${name} ${(percent * 100).toFixed(0)}%`}
          labelLine={{ stroke: "#6EE7B7" }}>
          {rows.map((_, i) => <Cell key={i} fill={COLORS[i % COLORS.length]} />)}
        </Pie>
        <Tooltip contentStyle={{ background: "#0a1f14", border: "1px solid #10B981", color: "#D1FAE5" }} />
      </PieChart>
    </ResponsiveContainer>
  );
}

function DataTable({ columns, rows }) {
  return (
    <div style={{ overflowX: "auto" }}>
      <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 13 }}>
        <thead>
          <tr>
            {columns.map(c => (
              <th key={c} style={{
                padding: "10px 14px", textAlign: "left", color: "#6EE7B7",
                borderBottom: "1px solid #1a3a2a", fontFamily: "'Space Mono', monospace",
                fontSize: 11, letterSpacing: "0.08em", textTransform: "uppercase",
                whiteSpace: "nowrap", background: "#071510"
              }}>{c}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((row, i) => (
            <tr key={i} style={{ background: i % 2 === 0 ? "transparent" : "#071510" }}>
              {columns.map(c => (
                <td key={c} style={{
                  padding: "9px 14px", color: "#D1FAE5",
                  borderBottom: "1px solid #0f2a1a", fontFamily: "'Space Mono', monospace",
                  fontSize: 12
                }}>
                  {row[c] === null ? <span style={{ color: "#374151" }}>null</span> : String(row[c])}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function ResultCard({ result }) {
  const [chartType, setChartType] = useState(null);
  const db = result.db_result;

  useEffect(() => {
    if (db?.columns && db?.rows)
      setChartType(guessChartType(db.columns, db.rows));
  }, [result]);

  const hasData = db?.success && db?.rows?.length > 0;
  const hasNumbers = db?.columns?.some(c => typeof db.rows?.[0]?.[c] === "number");

  return (
    <div style={{
      background: "#0a1f14", border: "1px solid #1a3a2a", borderRadius: 12,
      padding: "24px", marginBottom: 20, animation: "fadeSlide 0.4s ease"
    }}>
      {/* Question */}
      <div style={{ display: "flex", alignItems: "flex-start", gap: 12, marginBottom: 18 }}>
        <div style={{
          background: "#10B981", color: "#000", borderRadius: 6,
          padding: "4px 10px", fontSize: 11, fontWeight: 700,
          fontFamily: "'Space Mono', monospace", whiteSpace: "nowrap"
        }}>YOU</div>
        <p style={{ color: "#D1FAE5", margin: 0, fontSize: 15, lineHeight: 1.5 }}>
          {result.question}
        </p>
      </div>

      {/* SQL */}
      {result.sql && (
        <div style={{ marginBottom: 18 }}>
          <div style={{ color: "#6EE7B7", fontSize: 11, fontFamily: "'Space Mono', monospace",
            marginBottom: 8, letterSpacing: "0.08em" }}>GENERATED SQL</div>
          <pre style={{
            background: "#020c06", border: "1px solid #1a3a2a", borderRadius: 8,
            padding: "14px 16px", color: "#34D399", fontSize: 12,
            fontFamily: "'Space Mono', monospace", overflowX: "auto", margin: 0, lineHeight: 1.6
          }}>{result.sql}</pre>
        </div>
      )}

      {/* Status badges */}
      <div style={{ display: "flex", gap: 8, marginBottom: 18, flexWrap: "wrap" }}>
        <span style={{
          background: result.success ? "#052e16" : "#1f0a0a",
          border: `1px solid ${result.success ? "#10B981" : "#ef4444"}`,
          color: result.success ? "#6EE7B7" : "#fca5a5",
          borderRadius: 20, padding: "3px 12px", fontSize: 11,
          fontFamily: "'Space Mono', monospace"
        }}>
          {result.success ? "✓ SQL Valid" : "✗ SQL Failed"}
        </span>
        {hasData && (
          <span style={{
            background: "#052e16", border: "1px solid #10B981",
            color: "#6EE7B7", borderRadius: 20, padding: "3px 12px",
            fontSize: 11, fontFamily: "'Space Mono', monospace"
          }}>
            {db.row_count} row{db.row_count !== 1 ? "s" : ""}
          </span>
        )}
        {result.attempts > 0 && (
          <span style={{
            background: "#1a1a05", border: "1px solid #ca8a04",
            color: "#fde68a", borderRadius: 20, padding: "3px 12px",
            fontSize: 11, fontFamily: "'Space Mono', monospace"
          }}>
            {result.attempts} attempt{result.attempts !== 1 ? "s" : ""}
          </span>
        )}
      </div>

      {/* DB Error */}
      {db && !db.success && (
        <div style={{
          background: "#1f0a0a", border: "1px solid #ef4444",
          borderRadius: 8, padding: "12px 16px", color: "#fca5a5",
          fontSize: 12, fontFamily: "'Space Mono', monospace", marginBottom: 16
        }}>
          ✗ {db.error}
        </div>
      )}

      {/* Irrelevant message */}
      {!result.success && !result.sql && (
        <div style={{
          background: "#1a1205", border: "1px solid #ca8a04",
          borderRadius: 8, padding: "12px 16px", color: "#fde68a", fontSize: 13
        }}>
          ⚠ {result.message}
        </div>
      )}

      {/* Chart switcher + visualization */}
      {hasData && (
        <>
          {hasNumbers && (
            <div style={{ display: "flex", gap: 6, marginBottom: 14 }}>
              {["table", "bar", "line", "pie"].map(t => (
                <button key={t} onClick={() => setChartType(t)}
                  style={{
                    background: chartType === t ? "#10B981" : "transparent",
                    border: "1px solid #1a3a2a", borderRadius: 6,
                    color: chartType === t ? "#000" : "#6EE7B7",
                    padding: "4px 12px", fontSize: 11, cursor: "pointer",
                    fontFamily: "'Space Mono', monospace", textTransform: "uppercase",
                    letterSpacing: "0.05em", transition: "all 0.2s"
                  }}>
                  {t === "table" ? "⊞" : t === "bar" ? "▐▐" : t === "line" ? "╱╲" : "◉"} {t}
                </button>
              ))}
            </div>
          )}

          <div style={{ marginTop: 8 }}>
            {chartType === "bar"  && <BarViz  columns={db.columns} rows={db.rows} />}
            {chartType === "line" && <LineViz columns={db.columns} rows={db.rows} />}
            {chartType === "pie"  && <PieViz  columns={db.columns} rows={db.rows} />}
            {chartType === "table" && <DataTable columns={db.columns} rows={db.rows} />}
          </div>
        </>
      )}

      {/* No data */}
      {db?.success && db?.rows?.length === 0 && (
        <div style={{ color: "#374151", fontSize: 13, fontFamily: "'Space Mono', monospace",
          textAlign: "center", padding: "20px 0" }}>
          No records found.
        </div>
      )}
    </div>
  );
}

// ── main app ──────────────────────────────────────────────────────────────────

export default function App() {
  const [question, setQuestion] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [dbStatus, setDbStatus] = useState(null);
  const bottomRef = useRef(null);
  const inputRef = useRef(null);

  useEffect(() => {
    fetch(`${API_BASE}/health`)
      .then(r => r.json())
      .then(d => setDbStatus(d.database))
      .catch(() => setDbStatus("not connected"));
  }, []);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [results]);

  async function handleAsk() {
    if (!question.trim() || loading) return;
    const q = question.trim();
    setQuestion("");
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/ask`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: q })
      });
      const data = await res.json();
      setResults(prev => [...prev, data]);
    } catch (e) {
      setResults(prev => [...prev, {
        question: q, sql: null, db_result: null,
        success: false, message: "Could not connect to API. Is the server running?",
        attempts: 0, intent: null, validation: null
      }]);
    }
    setLoading(false);
    setTimeout(() => inputRef.current?.focus(), 100);
  }

  function handleKey(e) {
    if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); handleAsk(); }
  }

  const SUGGESTIONS = [
    "show me all customers from India",
    "which products have rating above 4.5?",
    "top 5 customers by total orders",
    "list all employees in Sales department",
    "how many orders per status?",
    "products with stock less than 50",
  ];

  return (
    <>
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Space+Mono:ital,wght@0,400;0,700;1,400&family=Sora:wght@300;400;500;600&display=swap');
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { background: #020c06; color: #D1FAE5; font-family: 'Sora', sans-serif; }
        ::-webkit-scrollbar { width: 6px; height: 6px; }
        ::-webkit-scrollbar-track { background: #020c06; }
        ::-webkit-scrollbar-thumb { background: #1a3a2a; border-radius: 3px; }
        @keyframes fadeSlide {
          from { opacity: 0; transform: translateY(16px); }
          to   { opacity: 1; transform: translateY(0); }
        }
        @keyframes pulse {
          0%, 100% { opacity: 1; } 50% { opacity: 0.4; }
        }
        @keyframes spin {
          to { transform: rotate(360deg); }
        }
        textarea:focus { outline: none; }
        button:hover { opacity: 0.85; }
      `}</style>

      <div style={{ minHeight: "100vh", display: "flex", flexDirection: "column" }}>

        {/* Header */}
        <header style={{
          borderBottom: "1px solid #1a3a2a", padding: "16px 32px",
          display: "flex", alignItems: "center", justifyContent: "space-between",
          background: "#020c06", position: "sticky", top: 0, zIndex: 100
        }}>
          <div style={{ display: "flex", alignItems: "center", gap: 14 }}>
            <div style={{
              width: 36, height: 36, background: "#10B981",
              borderRadius: 8, display: "flex", alignItems: "center",
              justifyContent: "center", fontSize: 18, fontWeight: 700, color: "#000"
            }}>⌘</div>
            <div>
              <div style={{ fontFamily: "'Space Mono', monospace", fontSize: 14,
                fontWeight: 700, color: "#6EE7B7", letterSpacing: "0.05em" }}>
                NL2SQL
              </div>
              <div style={{ fontSize: 11, color: "#374151" }}>
                natural language → sql → results
              </div>
            </div>
          </div>
          <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
            <div style={{
              width: 8, height: 8, borderRadius: "50%",
              background: dbStatus === "connected" ? "#10B981" : "#ef4444",
              animation: dbStatus === "connected" ? "pulse 2s infinite" : "none"
            }} />
            <span style={{ fontSize: 11, color: "#6b7280",
              fontFamily: "'Space Mono', monospace" }}>
              DB {dbStatus || "checking..."}
            </span>
          </div>
        </header>

        {/* Main content */}
        <main style={{ flex: 1, maxWidth: 860, width: "100%",
          margin: "0 auto", padding: "32px 24px", paddingBottom: 160 }}>

          {/* Empty state */}
          {results.length === 0 && (
            <div style={{ textAlign: "center", paddingTop: 60 }}>
              <div style={{ fontSize: 48, marginBottom: 16 }}>⌗</div>
              <h1 style={{
                fontFamily: "'Space Mono', monospace", fontSize: 28,
                color: "#6EE7B7", marginBottom: 8, letterSpacing: "-0.02em"
              }}>Ask your database anything</h1>
              <p style={{ color: "#374151", fontSize: 14, marginBottom: 40 }}>
                Type in plain English. Get SQL + charts instantly.
              </p>

              {/* Suggestions */}
              <div style={{ display: "flex", flexWrap: "wrap", gap: 8, justifyContent: "center" }}>
                {SUGGESTIONS.map(s => (
                  <button key={s} onClick={() => setQuestion(s)}
                    style={{
                      background: "transparent", border: "1px solid #1a3a2a",
                      borderRadius: 20, padding: "7px 16px", color: "#6EE7B7",
                      fontSize: 12, cursor: "pointer", fontFamily: "'Sora', sans-serif",
                      transition: "all 0.2s"
                    }}
                    onMouseEnter={e => e.target.style.borderColor = "#10B981"}
                    onMouseLeave={e => e.target.style.borderColor = "#1a3a2a"}>
                    {s}
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* Results */}
          {results.map((r, i) => <ResultCard key={i} result={r} />)}

          {/* Loading */}
          {loading && (
            <div style={{
              background: "#0a1f14", border: "1px solid #1a3a2a",
              borderRadius: 12, padding: "24px", marginBottom: 20,
              display: "flex", alignItems: "center", gap: 14
            }}>
              <div style={{
                width: 20, height: 20, border: "2px solid #1a3a2a",
                borderTopColor: "#10B981", borderRadius: "50%",
                animation: "spin 0.8s linear infinite"
              }} />
              <span style={{ color: "#6EE7B7", fontFamily: "'Space Mono', monospace",
                fontSize: 12 }}>Generating SQL...</span>
            </div>
          )}

          <div ref={bottomRef} />
        </main>

        {/* Input bar — fixed at bottom */}
        <div style={{
          position: "fixed", bottom: 0, left: 0, right: 0,
          background: "linear-gradient(to top, #020c06 70%, transparent)",
          padding: "20px 24px 28px"
        }}>
          <div style={{ maxWidth: 860, margin: "0 auto" }}>
            <div style={{
              display: "flex", gap: 10, alignItems: "flex-end",
              background: "#0a1f14", border: "1px solid #1a3a2a",
              borderRadius: 14, padding: "12px 14px",
              boxShadow: "0 0 40px rgba(16,185,129,0.08)"
            }}>
              <textarea
                ref={inputRef}
                value={question}
                onChange={e => setQuestion(e.target.value)}
                onKeyDown={handleKey}
                placeholder="Ask a question about your data..."
                rows={1}
                style={{
                  flex: 1, background: "transparent", border: "none",
                  color: "#D1FAE5", fontSize: 14, fontFamily: "'Sora', sans-serif",
                  resize: "none", lineHeight: 1.5, paddingTop: 2,
                  caretColor: "#10B981"
                }}
              />
              <button onClick={handleAsk} disabled={loading || !question.trim()}
                style={{
                  background: question.trim() && !loading ? "#10B981" : "#1a3a2a",
                  border: "none", borderRadius: 8, width: 38, height: 38,
                  cursor: question.trim() && !loading ? "pointer" : "default",
                  display: "flex", alignItems: "center", justifyContent: "center",
                  fontSize: 16, color: question.trim() && !loading ? "#000" : "#374151",
                  transition: "all 0.2s", flexShrink: 0
                }}>
                {loading ? (
                  <div style={{
                    width: 16, height: 16, border: "2px solid #374151",
                    borderTopColor: "#6EE7B7", borderRadius: "50%",
                    animation: "spin 0.8s linear infinite"
                  }} />
                ) : "↑"}
              </button>
            </div>
            <div style={{ textAlign: "center", marginTop: 8, color: "#1a3a2a",
              fontSize: 11, fontFamily: "'Space Mono', monospace" }}>
              Enter to send · Shift+Enter for new line
            </div>
          </div>
        </div>

      </div>
    </>
  );
}