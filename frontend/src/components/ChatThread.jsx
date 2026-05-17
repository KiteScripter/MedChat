export default function ChatThread({ messages, loading }) {
  return (
    <div style={styles.thread}>
      {messages.map((msg, i) => (
        <div key={i} style={{ ...styles.row, justifyContent: msg.role === "user" ? "flex-end" : "flex-start" }}>
          {msg.role === "assistant" && (
            <div style={styles.avatar}>✚</div>
          )}
          <div style={{
            ...styles.bubble,
            ...(msg.role === "user" ? styles.userBubble : styles.aiBubble),
            ...(msg.is_error ? styles.errorBubble : {}),
            ...(!msg.is_confident && msg.role === "assistant" ? styles.lowConfBubble : {}),
          }}>
            {!msg.is_confident && msg.role === "assistant" && !msg.is_error && (
              <div style={styles.lowConfBadge}>
                <span>⚠</span> Low confidence — limited information found in trusted sources
              </div>
            )}
            <p style={styles.text}>{msg.content}</p>
            {msg.sources?.length > 0 && (
              <div style={styles.sources}>
                <span style={styles.sourcesLabel}>Sources</span>
                {msg.sources.map((s) => {
                  let hostname = s;
                  try { hostname = new URL(s).hostname.replace("www.", ""); } catch {}
                  return (
                    <a key={s} href={s} target="_blank" rel="noreferrer" style={styles.sourceLink}>
                      {hostname}
                    </a>
                  );
                })}
              </div>
            )}
            {msg.trusted_sources_searched > 0 && (
              <div style={styles.searchedNote}>
                🔍 Searched {msg.trusted_sources_searched} trusted medical source{msg.trusted_sources_searched !== 1 ? "s" : ""}
              </div>
            )}
          </div>
        </div>
      ))}
      {loading && (
        <div style={{ ...styles.row, justifyContent: "flex-start" }}>
          <div style={styles.avatar}>✚</div>
          <div style={{ ...styles.bubble, ...styles.aiBubble }}>
            <div style={styles.typing}>
              <span />
              <span />
              <span />
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

const styles = {
  thread: { display: "flex", flexDirection: "column", gap: 12 },
  row: { display: "flex", gap: 10, alignItems: "flex-end" },
  avatar: {
    width: 32, height: 32,
    borderRadius: "50%",
    background: "var(--accent)",
    color: "#fff",
    display: "flex", alignItems: "center", justifyContent: "center",
    fontSize: 14, fontWeight: 700,
    flexShrink: 0,
  },
  bubble: {
    maxWidth: "80%",
    padding: "12px 16px",
    borderRadius: 14,
    fontSize: 14,
    lineHeight: 1.65,
  },
  userBubble: {
    background: "var(--accent)",
    color: "#fff",
    borderBottomRightRadius: 4,
  },
  aiBubble: {
    background: "var(--bg)",
    border: "1px solid var(--border)",
    borderBottomLeftRadius: 4,
    color: "var(--text)",
  },
  errorBubble: {
    background: "#fff0f0",
    border: "1px solid #ffcccc",
  },
  lowConfBubble: {
    background: "var(--warn-bg)",
    border: "1px solid var(--warn-border)",
  },
  lowConfBadge: {
    display: "flex", alignItems: "center", gap: 6,
    fontSize: 11, fontWeight: 600,
    color: "#7a5a00",
    marginBottom: 8,
    padding: "4px 8px",
    background: "#fff3cd",
    borderRadius: 6,
  },
  text: { whiteSpace: "pre-wrap" },
  sources: { marginTop: 10, display: "flex", flexWrap: "wrap", gap: 6, alignItems: "center" },
  sourcesLabel: { fontSize: 11, color: "var(--muted)", fontWeight: 600, marginRight: 2 },
  sourceLink: {
    fontSize: 11,
    color: "var(--accent)",
    background: "var(--accent-light)",
    padding: "2px 8px",
    borderRadius: 4,
    textDecoration: "none",
    fontFamily: "var(--mono)",
  },
  searchedNote: {
    marginTop: 8,
    fontSize: 11,
    color: "var(--muted)",
  },
  typing: {
    display: "flex", gap: 5, padding: "2px 0",
    "& span": {
      width: 7, height: 7,
      borderRadius: "50%",
      background: "var(--muted)",
      animation: "blink 1.2s infinite",
    },
  },
};
