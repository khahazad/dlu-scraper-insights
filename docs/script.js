let rows = [];
let columns = [
  "pid", "name", "level", "Role", "Joined",
  "gold", "gems", "last_donation", "Rank"
];

let sortState = {
  column: null,
  direction: 1   // 1 = asc, -1 = desc
};

async function loadData() {
  const url = "delulu_data.json";
  const response = await fetch(url);
  const data = await response.json();

  rows = Object.entries(data).map(([pid, fields]) => ({
    pid,
    Role: fields.Role ?? "Former",   // normalize missing role
    ...fields
  }));

  buildTable();
  renderRows(rows);

  // Attach filter events
  document.getElementById("searchInput").oninput = applyFilters;

  // Attach checkbox events for multi-select dropdown
  document.querySelectorAll(".dropdown-content input")
    .forEach(cb => cb.onchange = applyFilters);
  
  // Apply filter immediately on page load 
  applyFilters();
}


// Toggle dropdown
document.addEventListener("click", function (e) {
  const dropdown = document.querySelector(".dropdown");
  if (dropdown.contains(e.target)) {
    dropdown.classList.toggle("show");
  } else {
    dropdown.classList.remove("show");
  }
});

function buildTable() {
  const table = document.getElementById("guildTable");

  // Header
  const thead = document.createElement("thead");
  const headerRow = document.createElement("tr");

  columns.forEach(col => {
    const th = document.createElement("th");
    th.textContent = col;
    th.style.cursor = "pointer";
    th.onclick = () => sortTable(col);
    headerRow.appendChild(th);
  });

  thead.appendChild(headerRow);
  table.appendChild(thead);

  // Body
  const tbody = document.createElement("tbody");
  tbody.id = "guildBody";
  table.appendChild(tbody);
}

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

    // Date sort (ISO)
    if (col === "last_donation" || col === "Joined") {
      return (new Date(x) - new Date(y)) * sortState.direction;
    }

    // String sort
    return x.toString().localeCompare(y.toString()) * sortState.direction;
  });

  applyFilters(); // reapply filters after sorting
}

function applyFilters() {
  const search = document.getElementById("searchInput").value.toLowerCase();

  // Read selected roles from checkboxes
  const selectedRoles = Array.from(
    document.querySelectorAll(".dropdown-content input:checked")
  ).map(cb => cb.value);

  const filtered = rows.filter(row => {
    // Role filter
    if (!selectedRoles.includes(row.Role)) return false;

    // Search filter
    const text = Object.values(row).join(" ").toLowerCase();
    if (search && !text.includes(search)) return false;

    return true;
  });

  renderRows(filtered);
}



loadData();
