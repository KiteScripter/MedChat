import { useState } from "react";

const EXAMPLE_QUESTIONS = [
  "What are the symptoms of type 2 diabetes?",
  "How does ibuprofen work?",
  "What is the recommended dosage of vitamin D?",
  "What are the early signs of hypertension?",
];

export default function ChatInput({ onSend, disabled }) {
  const [value, setValue] = useState("");

  function submit(e) {
    e.preventDefault();
    if (value.trim() && !disabled) {
      onSend(value.trim());
      setValue("");
    }
  }

  function handleKey(e) {
    if (e.key === "Enter" && !e.shiftKey) submit(e);
  }

  return (
    <div>
      <div style={styles.examples}>
        {EXAMPLE_QUESTIONS.map((q) => (
          <button key={q} style={styles.exampleBtn} onClick={() => { setValue(q); }} disabled={disabled}>
            {q}
          </button>
        ))}
      </div>
      <form onSubmit={submit} style={styles.form}>
        <textarea
          style={styles.input}
          value={value}
          onChange={(e) => setValue(e.target.value)}
          onKeyDown={handleKey}
          placeholder="Ask a medical question… (Enter to send, Shift+Enter for new line)"
          disabled={disabled}
          rows={2}
          autoFocus
        />
        <button style={{ ...styles.btn, opacity: disabled || !value.trim() ? 0.5 : 1 }} disabled={disabled || !value.trim()}>
          {disabled ? "…" : "Send"}
        </button>
      </form>
      <p style={styles.note}>
        ⚕ For emergencies, call your local emergency number immediately.
      </p>
    </div>
  );
}

const styles = {
  examples: { display: "flex", flexWrap: "wrap", gap: 6, marginBottom: 10 },
  exampleBtn: {
    background: "var(--accent-light)",
    color: "var(--accent)",
    border: "1px solid var(--border)",
    borderRadius: 6,
    padding: "4px 10px",
    fontSize: 12,
    cursor: "pointer",
    fontFamily: "var(--body)",
    textAlign: "left",
  },
  form: { display: "flex", gap: 10, alignItems: "flex-end" },
  input: {
    flex: 1,
    border: "1px solid var(--border)",
    borderRadius: 10,
    padding: "10px 14px",
    color: "var(--text)",
    fontFamily: "var(--body)",
    fontSize: 14,
    resize: "none",
    outline: "none",
    background: "var(--bg)",
    lineHeight: 1.5,
  },
  btn: {
    background: "var(--accent)",
    color: "#fff",
    border: "none",
    borderRadius: 10,
    padding: "10px 20px",
    fontWeight: 600,
    fontSize: 14,
    cursor: "pointer",
    fontFamily: "var(--body)",
    height: 44,
  },
  note: {
    marginTop: 8,
    fontSize: 11,
    color: "var(--muted)",
    textAlign: "center",
  },
};
