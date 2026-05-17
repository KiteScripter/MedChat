import { useState, useRef, useEffect } from "react";
import ChatThread from "./components/ChatThread.jsx";
import ChatInput from "./components/ChatInput.jsx";

const API = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

export default function App() {
  const [messages, setMessages] = useState([
    {
      role: "assistant",
      content: "Hello! I'm MedChat, a medical information assistant powered by trusted clinical sources — NIH, CDC, WHO, Mayo Clinic, peer-reviewed journals, and more.\n\nI can help answer questions about symptoms, conditions, medications, and treatments. Please note that I provide **educational information only** and am not a substitute for professional medical advice.\n\nWhat would you like to know?",
      is_confident: true,
      sources: [],
    },
  ]);
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  async function handleSend(question) {
    const userMsg = { role: "user", content: question };
    setMessages((prev) => [...prev, userMsg]);
    setLoading(true);

    try {
      const res = await fetch(`${API}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          question,
          messages: messages.map((m) => ({ role: m.role, content: m.content })),
        }),
      });

      if (!res.ok) throw new Error(`Server error: ${res.status}`);
      const data = await res.json();

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: data.answer,
          is_confident: data.is_confident,
          sources: data.sources ?? [],
          trusted_sources_searched: data.trusted_sources_searched,
        },
      ]);
    } catch (e) {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: "I encountered a technical error and couldn't retrieve information. Please try again, or consult a medical professional directly.",
          is_confident: false,
          sources: [],
          is_error: true,
        },
      ]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div style={styles.shell}>
      {/* Header */}
      <header style={styles.header}>
        <div style={styles.logo}>
          <span style={styles.cross}>✚</span>
          <span style={styles.appName}>MedChat</span>
        </div>
        <p style={styles.tagline}>Medical information from trusted clinical sources only</p>
        <div style={styles.sourceBadges}>
          {["NIH", "CDC", "WHO", "Mayo Clinic", "PubMed", "NHS"].map((s) => (
            <span key={s} style={styles.badge}>{s}</span>
          ))}
        </div>
      </header>

      {/* Disclaimer */}
      <div style={styles.disclaimer}>
        ⚕ <strong>Educational purposes only.</strong> Always consult a qualified healthcare professional for personal medical advice.
      </div>

      {/* Chat */}
      <div style={styles.chatArea}>
        <ChatThread messages={messages} loading={loading} />
        <div ref={bottomRef} />
      </div>

      {/* Input */}
      <div style={styles.inputBar}>
        <ChatInput onSend={handleSend} disabled={loading} />
      </div>
    </div>
  );
}

const styles = {
  shell: {
    display: "flex",
    flexDirection: "column",
    height: "100vh",
    maxWidth: 780,
    margin: "0 auto",
    background: "var(--surface)",
    boxShadow: "0 0 40px rgba(0,0,0,0.08)",
  },
  header: {
    padding: "20px 24px 16px",
    borderBottom: "1px solid var(--border)",
    background: "var(--surface)",
  },
  logo: { display: "flex", alignItems: "center", gap: 10, marginBottom: 4 },
  cross: { fontSize: 22, color: "var(--accent)", fontWeight: 700 },
  appName: { fontFamily: "var(--sans)", fontWeight: 800, fontSize: 22, color: "var(--accent)", letterSpacing: "-0.02em" },
  tagline: { fontSize: 12, color: "var(--muted)", marginBottom: 10 },
  sourceBadges: { display: "flex", flexWrap: "wrap", gap: 6 },
  badge: {
    fontSize: 11,
    fontWeight: 600,
    background: "var(--accent-light)",
    color: "var(--accent)",
    padding: "2px 8px",
    borderRadius: 100,
    fontFamily: "var(--mono)",
  },
  disclaimer: {
    background: "var(--warn-bg)",
    borderBottom: "1px solid var(--warn-border)",
    padding: "8px 24px",
    fontSize: 12,
    color: "#7a5a00",
  },
  chatArea: {
    flex: 1,
    overflowY: "auto",
    padding: "20px 24px",
    display: "flex",
    flexDirection: "column",
    gap: 16,
  },
  inputBar: {
    borderTop: "1px solid var(--border)",
    padding: "16px 24px",
    background: "var(--surface)",
  },
};
