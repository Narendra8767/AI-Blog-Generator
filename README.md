# AI-Blog-Generator<br>
AI Blog Generator that creates full-length, high-quality blogs from just a topic — powered by the incredible combo of LangGraph, LangChain, and OpenAI!<br>

What I Built<br>
Given a topic like "How AI is Transforming Healthcare", the app:<br>

🟦 Generates a clean outline<br>
🟦 Produces a detailed blog post based on the outline<br>
🟦 Assigns a quality score (0–10) using LLM-based evaluation<br>



Tech Stack: LangGraph + LangChain + Flask + OpenAI + Python<br>

💡 How It Works:<br>
Using LangGraph, I designed a clear and controlled stateful workflow:<br>
🔹 create_outline → generates a structured outline<br>
🔹 create_blog → writes detailed content based on the outline<br>
🔹 evaluate_blog → scores the quality of the blog (0–10)<br>

LangGraph handles these stages using nodes (functions) and edges (execution order) to form a Directed Acyclic Graph (DAG). This makes the entire flow modular, explainable, and maintainable.<br>

📚 Learning Outcomes:<br>
✅ Understood how LangGraph simplifies complex multi-step LLM tasks using a graph-based paradigm.<br>
✅ Learned to build and connect nodes, and direct the flow using edges (START → Outline → Blog → Evaluation → END).<br>
✅ Gained clarity on understanding and designing sequential workflows, which is key when orchestrating step-by-step AI pipelines.<br>
✅ Learned how to separate logic into clean, traceable units — essential for building scalable and maintainable agentic AI workflows.<br>


🧠 Why LangGraph?<br>
LangGraph offers a powerful way to design AI workflows as graph-based systems, where each step (node) performs a specific task and flows are explicitly defined.<br>

It helped me:<br>

✅ Model multi-step logic clearly with nodes like outline → blog → evaluation<br>
✅ Maintain shared state across steps, ensuring data consistency<br>
✅ Build modular, reusable components for each phase of the blog generation process<br>
✅ Visualize and control flow, making it easy to extend or debug<br>
✅ Scale the system easily by adding new logic nodes (like SEO scoring or language translation)<br>

LangGraph allowed me to build an AI application that’s not only smart — but structured, traceable, and production-ready.<br>
