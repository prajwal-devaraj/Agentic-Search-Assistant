"use client";

import { FormEvent, useMemo, useState } from "react";

type Mode = "quick" | "deep" | "compare" | "code" | "news";
type Result = {
  session_id: string;
  answer: string;
  sources: { id: string; title: string; url: string; snippet: string; domain: string; score: number }[];
  trust: { score: number; band: string; domain_diversity: number; notes: string[] };
  trace: { name: string; status: string; detail: string }[];
};

const API = process.env.NEXT_PUBLIC_PRAJNA_API_URL ?? "http://localhost:8000";
const modes: { key: Mode; label: string; hint: string }[] = [
  { key: "quick", label: "Quick", hint: "Fast answer" },
  { key: "deep", label: "Deep", hint: "More evidence" },
  { key: "compare", label: "Compare", hint: "Trade-offs" },
  { key: "code", label: "Code", hint: "Docs-first" },
  { key: "news", label: "News", hint: "Freshness" },
];

export default function Home() {
  const [query, setQuery] = useState("");
  const [mode, setMode] = useState<Mode>("quick");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<Result | null>(null);
  const [error, setError] = useState("");

  const canSearch = useMemo(() => query.trim().length > 1 && !loading, [query, loading]);

  async function submit(e: FormEvent) {
    e.preventDefault();
    if (!canSearch) return;
    setLoading(true);
    setError("");
    try {
      const res = await fetch(`${API}/v1/search`, {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ query, mode, max_sources: mode === "deep" ? 10 : 6 }),
      });
      if (!res.ok) throw new Error(`Search failed (${res.status})`);
      setResult(await res.json());
    } catch (err) {
      setError(err instanceof Error ? err.message : "Search failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="shell">
      <aside className="sidebar">
        <div className="brand">
          <div className="mark">P</div>
          <div><strong>PRAJNA</strong><span>universal search</span></div>
        </div>
        <button className="newSearch" onClick={() => { setQuery(""); setResult(null); }}>＋ New search</button>
        <nav>
          <p className="navTitle">Lenses</p>
          {modes.map((item) => (
            <button key={item.key} className={mode === item.key ? "navItem active" : "navItem"} onClick={() => setMode(item.key)}>
              <span>{item.label}</span><small>{item.hint}</small>
            </button>
          ))}
        </nav>
        <div className="sideFoot"><span className="pulse" /> PRAJNA framework online</div>
      </aside>

      <section className="workspace">
        <header className="topbar">
          <div><span className="eyebrow">PRAJNA / {mode.toUpperCase()}</span></div>
          <a className="github" href="https://github.com/prajwal-devaraj/Agentic-Search-Assistant" target="_blank">GitHub ↗</a>
        </header>

        {!result && !loading ? (
          <section className="hero">
            <div className="orb" aria-hidden="true"><div className="orbCore" /></div>
            <p className="eyebrow">PLAN · RETRIEVE · ASSESS · JOIN · NAVIGATE · ANSWER</p>
            <h1>Ask the web.<br /><em>Inspect the evidence.</em></h1>
            <p className="sub">A search workspace that shows where an answer came from, how much evidence survived ranking, and what the system actually did.</p>
            <form className="searchBox" onSubmit={submit}>
              <textarea value={query} onChange={(e) => setQuery(e.target.value)} placeholder="Ask anything — research, compare, code, investigate…" rows={3} />
              <div className="searchBottom">
                <div className="modePill">{mode}</div>
                <button disabled={!canSearch}>Search <span>↗</span></button>
              </div>
            </form>
            <div className="examples">
              {[
                "Compare vector databases for RAG",
                "Explain an unfamiliar research paper",
                "Find evidence for and against a claim",
              ].map((q) => <button key={q} onClick={() => setQuery(q)}>{q}</button>)}
            </div>
          </section>
        ) : (
          <section className="results">
            <form className="compactSearch" onSubmit={submit}>
              <input value={query} onChange={(e) => setQuery(e.target.value)} />
              <button disabled={!canSearch}>{loading ? "Working…" : "Search"}</button>
            </form>

            {loading && <div className="loadingCard"><span className="spinner" /> PRAJNA is collecting and ranking evidence…</div>}
            {error && <div className="errorCard">{error}</div>}

            {result && !loading && <>
              <div className="resultGrid">
                <article className="answerCard">
                  <div className="cardLabel">SYNTHESIS</div>
                  <div className="answerText">{result.answer}</div>
                </article>
                <aside className="trustCard">
                  <div className="cardLabel">TRUST PANEL</div>
                  <div className="score">{result.trust.score}<span>/100</span></div>
                  <div className={`band ${result.trust.band}`}>{result.trust.band} evidence</div>
                  <div className="trustMeta"><span>{result.sources.length} sources</span><span>{result.trust.domain_diversity} domains</span></div>
                </aside>
              </div>

              <section className="flowCard">
                <div className="cardLabel">PRAJNA TRACE</div>
                <div className="flow">
                  {result.trace.map((step, i) => <div className="step" key={step.name}><b>{i + 1}</b><span>{step.name}<small>{step.detail}</small></span></div>)}
                </div>
              </section>

              <section>
                <div className="sectionTitle"><div><span className="cardLabel">EVIDENCE</span><h2>Sources</h2></div><span>{result.sources.length} ranked</span></div>
                <div className="sources">
                  {result.sources.map((source, i) => (
                    <a className="sourceCard" href={source.url} target="_blank" rel="noreferrer" key={source.id}>
                      <div className="sourceTop"><span className="sourceIndex">{String(i + 1).padStart(2, "0")}</span><span className="domain">{source.domain}</span><span className="relevance">{Math.round(source.score * 100)}%</span></div>
                      <h3>{source.title}</h3><p>{source.snippet}</p>
                    </a>
                  ))}
                </div>
              </section>
            </>}
          </section>
        )}
      </section>
    </main>
  );
}
