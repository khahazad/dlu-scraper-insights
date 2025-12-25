let rows = [];
let columns = [
  "pid", "name", "level", "Role", "Joined",
  "gold", "gems", "last_donation", "Rank"
];

let sortState = {
  column: null,
  direction: 1
};

// -----------------------------
// Load JSON + initialize page
// -----------------------------
async function loadData() {
  const url = "delulu_data.json";
  const response = await fetch(url);
  const data = await response.json();

  // Normalize rows
  rows = Object.entries(data).map(([pid, fields]) => ({
    pid,
    Role: fields.Role ?? "Former",
    ...fields
  }));

  buildTable();
  renderRows(rows);

  // Search filter
  document.getElementById("searchInput").oninput = applyFilters;

  // Role filter
  document.querySelectorAll(".dropdown-content input")
    .forEach(cb => cb.onchange = applyFilters);

  // Apply filter immediately
  applyFilters();
}

// -----------------------------
// Dropdown toggle
// -----------------------------
document.addEventListener("click", function (e) {
  const dropdown = document.querySelector(".dropdown");
  if (dropdown.contains(e.target)) {
    dropdown.classList.toggle("show");
  } else {
    dropdown.classList.remove("show");
  }
});

// -----------------------------
// Format table headers
// -----------------------------
function formatHeader(col) {
  return col
    .replace(/_/g, " ")        // replace underscores with spaces
    .replace(/\b\w/g, c => c.toUpperCase()); // capitalize first letter of each word
}

// -----------------------------
// Build table structure
// -----------------------------
function buildTable() {
  const table = document.getElementById("guildTable");

  const thead = document.createElement("thead");
  const headerRow = document.createElement("tr");

  columns.forEach(col => {
    const th = document.createElement("th");
    th.style.cursor = "pointer";

    const label = document.createElement("span");
    label.textContent = formatHeader(col);

    const icon = document.createElement("span");
    icon.className = "sort-icon";
    icon.textContent = "";

    th.appendChild(label);
    th.appendChild(icon);

    th.onclick = () => sortTable(col);

    headerRow.appendChild(th);
  });

  thead.appendChild(headerRow);
  table.appendChild(thead);

  const tbody = document.createElement("tbody");
  tbody.id = "guildBody";
  table.appendChild(tbody);
}

// -----------------------------
// Render rows
// -----------------------------
function renderRows(data) {
  const tbody = document.getElementById("guildBody");
  tbody.innerHTML = "";

  data.forEach(row => {
    const tr = document.createElement("tr");
    columns.forEach(col => {
      const td = document.createElement("td");
      td.textContent = row[col] ?? "";
      tr.appendChild(td);
    });
    tbody.appendChild(tr);
  });
}

// -----------------------------
// Date parsing (YYYY-MM-DD HH:MM:SS)
// -----------------------------
function parseDate(dateStr) {
  if (!dateStr) return 0;

  const [datePart, timePart] = dateStr.split(" ");
  if (!datePart || !timePart) return 0;

  const [year, month, day] = datePart.split("-").map(Number);
  const [hour, minute, second] = timePart.split(":").map(Number);

  return new Date(year, month - 1, day, hour, minute, second).getTime();
}

// -----------------------------
// Sorting
// -----------------------------
function sortTable(col) {
  // Toggle direction
  if (sortState.column === col) {
    sortState.direction *= -1;
  } else {
    sortState.column = col;
    sortState.direction = 1;
  }

  rows.sort((a, b) => {
    const x = a[col] ?? "";
    const y = b[col] ?? "";

    // Numeric sort
    if (!isNaN(x) && !isNaN(y)) {
      return (Number(x) - Number(y)) * sortState.direction;
    }

    // Date sort
    if (col === "last_donation" || col === "Joined") {
      return (parseDate(x) - parseDate(y)) * sortState.direction;
    }

    // String sort
    return x.toString().localeCompare(y.toString()) * sortState.direction;
  });

  // Reset icons
  document.querySelectorAll("th .sort-icon").forEach(icon => {
    icon.textContent = "";
  });

  // Set icon for sorted column
  const index = columns.indexOf(col);
  const th = document.querySelectorAll("th")[index];
  const icon = th.querySelector(".sort-icon");
  icon.textContent = sortState.direction === 1 ? " ▲" : " ▼";

  applyFilters();
}

// -----------------------------
// Filtering
// -----------------------------
function applyFilters() {
  const search = document.getElementById("searchInput").value.toLowerCase();

  const selectedRoles = Array.from(
    document.querySelectorAll(".dropdown-content input:checked")
  ).map(cb => cb.value);

  const filtered = rows.filter(row => {
    if (!selectedRoles.includes(row.Role)) return false;

    const text = Object.values(row).join(" ").toLowerCase();
    if (search && !text.includes(search)) return false;

    return true;
  });

  renderRows(filtered);
}

// -----------------------------
loadData();
