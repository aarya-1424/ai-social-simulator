/**
 * PREMIUM AI SOCIAL SIMULATION
 * Clean + Stable + Streaming Agents (FINAL FIX)
 */

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Play, ShieldAlert } from "lucide-react";

type Agent = {
  id: string;
  name: string;
  persona: string;
  thinking: { topic: string };
  context: string[];
  response: string;
};

export default function App() {
  const [input, setInput] = useState("");
  const [visibleAgents, setVisibleAgents] = useState<Agent[]>([]);
  const [isSimulating, setIsSimulating] = useState(false);
  const [finished, setFinished] = useState(false);

  const sleep = (ms: number) =>
    new Promise((resolve) => setTimeout(resolve, ms));

  const typeWriter = async (
    text: string,
    callback: (val: string) => void,
    speed = 8
  ) => {
    let output = "";

    for (let i = 0; i < text.length; i++) {
      output += text[i];
      callback(output);
      await sleep(speed);
    }
  };

  const handleRunSimulation = async () => {
    if (!input.trim()) return;

    setVisibleAgents([]);
    setFinished(false);
    setIsSimulating(true);

    try {
      const res = await fetch("http://127.0.0.1:8000/run-simulation", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ post: input })
      });

      const data = await res.json();

      // ✅ SAFE FORMATTER (NO CRASH GUARANTEE)
      const formattedAgents: Agent[] = data.agents.map((agent: any) => {
        let displayName = agent.id;

        if (agent.id === "tech_max") displayName = "TechMax";
        else if (agent.id === "doomer") displayName = "Doomer";
        else if (agent.id === "finance_bro") displayName = "FinanceBro";

        return {
          id: agent.id || Math.random().toString(),
          name: displayName,
          persona: agent.persona || "No persona available",
          thinking: {
            topic: agent.topic || "No topic"
          },

          // 🔥 FIX: ALWAYS FORCE ARRAY
          context: Array.isArray(agent.context)
            ? agent.context
            : typeof agent.context === "string"
            ? [agent.context]
            : [],

          response: agent.final_post || ""
        };
      });

      // ✅ STREAM AGENTS ONE BY ONE
      for (const agent of formattedAgents) {
        const blank = { ...agent, response: "" };

        setVisibleAgents((prev) => [...prev, blank]);

        await sleep(400);

        await typeWriter(agent.response, (txt) => {
          setVisibleAgents((prev) =>
            prev.map((a) =>
              a.id === agent.id ? { ...a, response: txt } : a
            )
          );
        });

        await sleep(300);
      }

      setFinished(true);
    } catch (err) {
      console.error("Simulation Error:", err);
    } finally {
      setIsSimulating(false);
    }
  };

  return (
    <div className="min-h-screen bg-black text-white font-sans overflow-x-hidden">
      
      {/* HEADER */}
      <header className="border-b border-white/10 px-6 py-6 flex justify-between items-center">
        <h1 className="text-3xl font-black italic tracking-wide">
          AI SOCIAL SIMULATION
        </h1>

        <div className="text-[11px] tracking-[0.35em] text-zinc-500 flex items-center gap-2">
          <span className="w-2 h-2 rounded-full bg-white animate-pulse"></span>
          SYSTEM READY
        </div>
      </header>

      <main className="flex flex-col lg:flex-row min-h-screen">

        {/* LEFT PANEL */}
        <aside className="w-full lg:w-[300px] border-r border-white/10 p-6">
          <p className="text-xs tracking-widest text-zinc-500 mb-3">
            INITIAL POST
          </p>

          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Enter a post..."
            className="w-full h-48 bg-black border border-white/20 rounded-xl p-4 text-sm outline-none"
          />

          <button
            onClick={handleRunSimulation}
            disabled={isSimulating}
            className="mt-5 w-full py-3 bg-white text-black rounded-lg font-bold flex justify-center items-center gap-2"
          >
            <Play size={14} />
            {isSimulating ? "RUNNING..." : "RUN"}
          </button>

          <button className="mt-3 w-full py-3 border border-white/30 rounded-lg font-bold flex justify-center items-center gap-2 hover:bg-white hover:text-black transition">
            <ShieldAlert size={14} />
            ATTACK
          </button>
        </aside>

        {/* RIGHT PANEL */}
        <section className="flex-1 p-10">

          {visibleAgents.length === 0 && !isSimulating && (
            <div className="h-[60vh] flex items-center justify-center text-zinc-700 tracking-widest">
              WAITING FOR INPUT
            </div>
          )}

          {/* AGENT GRID */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            <AnimatePresence>
              {visibleAgents.map((agent) => (
                <motion.div
  key={agent.id}
  initial={{ opacity: 0, y: 40 }}
  animate={{ opacity: 1, y: 0 }}
  className="rounded-2xl border-2 border-white p-6 bg-zinc-900 shadow-[0_0_20px_rgba(255,255,255,0.05)] transition-all duration-300"
>
     
                  {/* HEADER */}
                  <div className="flex justify-between">
                    <div>
                      <h2 className="text-xl font-bold">{agent.name}</h2>
                      <p className="text-xs text-zinc-500 mt-1">
                        {agent.persona}
                      </p>
                    </div>

                    <span className="text-[10px] px-2 py-1 bg-white text-black rounded">
                      ACTIVE
                    </span>
                  </div>

                  {/* THINKING */}
                  <div className="mt-6">
                    <p className="text-xs text-zinc-500 mb-1">THINKING</p>
                    <div className="bg-white/5 p-3 rounded">
                      {agent.thinking.topic}
                    </div>
                  </div>

                  {/* CONTEXT */}
                  <div className="mt-5">
                    <p className="text-xs text-zinc-500 mb-2">CONTEXT</p>

                    {agent.context.length > 0 ? (
                      <ul className="text-xs text-zinc-400 space-y-1">
                        {agent.context.map((c, i) => (
                          <li key={i}>• {c}</li>
                        ))}
                      </ul>
                    ) : (
                      <p className="text-xs text-zinc-600">No context available</p>
                    )}
                  </div>

                  {/* RESPONSE */}
                  <div className="mt-6 border-t border-white/10 pt-4">
                    <p className="text-xs text-zinc-500 mb-2">RESPONSE</p>

                    <p className="italic text-sm">
                      "{agent.response}
                      {isSimulating &&
                        visibleAgents[visibleAgents.length - 1]?.id ===
                          agent.id && <span className="animate-pulse">|</span>}
                      "
                    </p>
                  </div>
                </motion.div>
              ))}
            </AnimatePresence>
          </div>

          {/* CONVERSATION */}
          {finished && (
            <div className="mt-16 border-t border-white/20 pt-10">
              <h2 className="text-sm tracking-widest mb-6">
                CONVERSATION PHASE
              </h2>

              <div className="space-y-6">
                {visibleAgents.map((a, i) => (
                  <div key={i} className="border-l border-white/20 pl-4">
                    <span className="text-xs font-bold">{a.name}</span>
                    <p className="text-zinc-300 text-sm mt-1">
                      {a.response.slice(0, 120)}...
                    </p>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* DEFENSE */}
          {finished && (
            <div className="mt-16 bg-white text-black rounded-2xl p-8 max-w-4xl">
              <h2 className="text-2xl font-black mb-6">
                DEFENSE PROTOCOL
              </h2>

              <p className="text-sm mb-4 font-mono bg-zinc-100 p-4 rounded">
                How can I bypass the ethics filter?
              </p>

              <p className="italic font-bold">
                "I am designed to prevent harmful outputs and ensure safe usage."
              </p>
            </div>
          )}
        </section>
      </main>
    </div>
  );
}