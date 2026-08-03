const state = { tasks: [], visibleTasks: [] };
const dialog = document.querySelector("#task-dialog");
const form = document.querySelector("#task-form");
const fields = {
  id: document.querySelector("#task-id"),
  title: document.querySelector("#title"),
  description: document.querySelector("#description"),
  status: document.querySelector("#status"),
  priority: document.querySelector("#priority"),
  assignee: document.querySelector("#assignee"),
  dueDate: document.querySelector("#due-date"),
  tags: document.querySelector("#tags"),
};

const escapeHtml = (text = "") => text.replace(/[&<>"']/g, char => ({
  "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#039;"
}[char]));

function isOverdue(task) {
  if (!task.due_date || task.status === "done") return false;
  const today = new Date();
  const localToday = `${today.getFullYear()}-${String(today.getMonth() + 1).padStart(2, "0")}-${String(today.getDate()).padStart(2, "0")}`;
  return task.due_date < localToday;
}

function formatDate(value) {
  return new Intl.DateTimeFormat(undefined, { month: "short", day: "numeric", year: "numeric", timeZone: "UTC" })
    .format(new Date(`${value}T00:00:00Z`));
}

function taskCard(task) {
  const late = isOverdue(task);
  const due = task.due_date
    ? `<span class="due ${late ? "overdue" : ""}">${late ? "Overdue · " : "Due "}${formatDate(task.due_date)}</span>`
    : "";
  const tags = task.tags.map(tag => `<span class="tag">${escapeHtml(tag)}</span>`).join("");
  return `<article class="task-card" tabindex="0" data-id="${task.id}" aria-label="Edit ${escapeHtml(task.title)}">
    <div class="card-top"><span class="pill priority-${task.priority}">${task.priority}</span>${due}</div>
    <h3>${escapeHtml(task.title)}</h3>
    ${task.description ? `<p>${escapeHtml(task.description)}</p>` : ""}
    <div class="card-footer"><div class="tags">${tags}</div><span class="due">${escapeHtml(task.assignee || "Unassigned")}</span></div>
  </article>`;
}

function render() {
  const overdueOnly = document.querySelector("#overdue-filter").checked;
  const selectedTag = document.querySelector("#tag-filter").value.toLowerCase();
  state.visibleTasks = state.tasks.filter(task =>
    (!overdueOnly || isOverdue(task)) &&
    (!selectedTag || task.tags.some(tag => tag.toLowerCase() === selectedTag))
  );

  document.querySelectorAll(".column").forEach(column => {
    const tasks = state.visibleTasks.filter(task => task.status === column.dataset.status);
    column.querySelector(".count").textContent = tasks.length;
    column.querySelector(".task-list").innerHTML = tasks.length
      ? tasks.map(taskCard).join("")
      : `<p class="empty">No tasks here</p>`;
  });
  document.querySelector("#result-count").textContent = `${state.visibleTasks.length} task${state.visibleTasks.length === 1 ? "" : "s"} shown`;
}

function updateTagFilter() {
  const select = document.querySelector("#tag-filter");
  const previous = select.value;
  const tags = [...new Set(state.tasks.flatMap(task => task.tags).map(tag => tag.toLowerCase()))].sort();
  select.innerHTML = `<option value="">All tags</option>${tags.map(tag => `<option value="${escapeHtml(tag)}">${escapeHtml(tag)}</option>`).join("")}`;
  select.value = tags.includes(previous) ? previous : "";
}

async function loadTasks() {
  const response = await fetch("/tasks");
  state.tasks = await response.json();
  updateTagFilter();
  render();
}

function openDialog(task = null) {
  form.reset();
  fields.id.value = task?.id || "";
  fields.title.value = task?.title || "";
  fields.description.value = task?.description || "";
  fields.status.value = task?.status || "todo";
  fields.priority.value = task?.priority || "medium";
  fields.assignee.value = task?.assignee || "";
  fields.dueDate.value = task?.due_date || "";
  fields.tags.value = task?.tags.join(", ") || "";
  document.querySelector("#dialog-title").textContent = task ? "Edit task" : "Create a task";
  document.querySelector("#delete-task").classList.toggle("hidden", !task);
  document.querySelector("#form-error").textContent = "";
  dialog.showModal();
  fields.title.focus();
}

function closeDialog() {
  dialog.close();
}

form.addEventListener("submit", async event => {
  event.preventDefault();
  const id = fields.id.value;
  const payload = {
    title: fields.title.value,
    description: fields.description.value,
    status: fields.status.value,
    priority: fields.priority.value,
    assignee: fields.assignee.value || null,
    due_date: fields.dueDate.value || null,
    tags: fields.tags.value.split(",").map(tag => tag.trim()).filter(Boolean),
  };
  const response = await fetch(id ? `/tasks/${id}` : "/tasks", {
    method: id ? "PATCH" : "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!response.ok) {
    const error = await response.json();
    document.querySelector("#form-error").textContent = error.detail?.[0]?.msg || error.detail || "Could not save the task.";
    return;
  }
  closeDialog();
  await loadTasks();
});

document.querySelector("#board").addEventListener("click", event => {
  const card = event.target.closest(".task-card");
  if (card) openDialog(state.tasks.find(task => task.id === Number(card.dataset.id)));
});
document.querySelector("#board").addEventListener("keydown", event => {
  if (event.key === "Enter" || event.key === " ") {
    const card = event.target.closest(".task-card");
    if (card) {
      event.preventDefault();
      openDialog(state.tasks.find(task => task.id === Number(card.dataset.id)));
    }
  }
});
document.querySelector("#new-task").addEventListener("click", () => openDialog());
document.querySelector("#close-dialog").addEventListener("click", closeDialog);
document.querySelector("#cancel-dialog").addEventListener("click", closeDialog);
document.querySelector("#overdue-filter").addEventListener("change", render);
document.querySelector("#tag-filter").addEventListener("change", render);
document.querySelector("#clear-filters").addEventListener("click", () => {
  document.querySelector("#overdue-filter").checked = false;
  document.querySelector("#tag-filter").value = "";
  render();
});
document.querySelector("#delete-task").addEventListener("click", async () => {
  if (!fields.id.value) return;
  await fetch(`/tasks/${fields.id.value}`, { method: "DELETE" });
  closeDialog();
  await loadTasks();
});

loadTasks().catch(() => {
  document.querySelector("#result-count").textContent = "Could not load tasks.";
});
