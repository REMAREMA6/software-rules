import React, { useState } from "react";
import { createRoot } from "react-dom/client";
import "./styles.css";

function TaskBoard() {
  const [tasks, setTasks] = useState([]);
  const [filter, setFilter] = useState("all");
  const [title, setTitle] = useState("");

  async function request(method, path, body) {
    const response = await fetch(path, {
      method,
      headers: { "content-type": "application/json" },
      body: body === undefined ? undefined : JSON.stringify(body)
    });
    if (!response.ok) throw new Error("API request failed");
    return response.json();
  }

  async function createTask(event) {
    event.preventDefault();
    const normalized = title.trim();
    if (!normalized) return;
    const created = await request("POST", "/api/tasks", { title: normalized });
    setTasks(current => [...current, created]);
    setTitle("");
  }

  async function toggleTask(task, completed) {
    const updated = await request("PATCH", "/api/tasks/" + task.id, { completed });
    setTasks(current => current.map(item => item.id === task.id ? updated : item));
  }

  async function deleteTask(task) {
    await request("DELETE", "/api/tasks/" + task.id);
    setTasks(current => current.filter(item => item.id !== task.id));
  }

  const visible = tasks.filter(task =>
    filter === "all" || (filter === "active" ? !task.completed : task.completed)
  );
  const active = import.meta.env.VITE_MUTATION_ACTIVE_COUNT === "1" ? tasks.length : tasks.filter(task => !task.completed).length;

  return <main className="app" id="app">
    <h1>Task Board</h1>
    <p className="hint">A small place to track what needs doing.</p>
    <form className="composer" id="task-form" onSubmit={createTask}>
      <input id="task-input" aria-label="Task name" placeholder="Add a task" required value={title} onChange={event => setTitle(event.target.value)} />
      <button type="submit">Add task</button>
    </form>
    <nav className="filters" aria-label="Task filters">
      {["all", "active", "completed"].map(value =>
        <button key={value} type="button" data-filter={value} aria-pressed={String(filter === value)} onClick={() => setFilter(value)}>
          {value[0].toUpperCase() + value.slice(1)}
        </button>
      )}
    </nav>
    <ul className="tasks" id="task-list">
      {visible.map(task => <li key={task.id} className={"task" + (task.completed ? " done" : "")}>
        <input type="checkbox" checked={task.completed} aria-label={"Complete " + task.title} onChange={event => toggleTask(task, event.target.checked)} />
        <span>{task.title}</span>
        <button type="button" aria-label={"Delete " + task.title} onClick={() => deleteTask(task)}>Delete</button>
      </li>)}
    </ul>
    <p className="summary" id="summary" aria-live="polite">{`${tasks.length}${tasks.length === 1 ? " task" : " tasks"} · ${active} active`}</p>
  </main>;
}

createRoot(document.getElementById("root")).render(<TaskBoard />);
