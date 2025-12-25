async function loadData() {
  const url = "delulu_data.json";  // served from same folder
  const response = await fetch(url);
  const data = await response.json();

  // Convert dictionary → array
  const rows = Object.entries(data).map(([pid, fields]) => ({
    pid,
    ...fields
  }));

  // Define column order
  const columns = [
    "pid", "name", "level", "Role", "Joined",
    "gold", "gems", "last_donation", "Rank"
  ];

  const table = document.getElementById("guildTable");

  // Build header
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

  // Build body
  const tbody = document.createElement("tbody");
  table.appendChild(tbody);

  function renderRows() {
    tbody.innerHTML = "";
    rows.forEach(row => {
      const tr = document.createElement("tr");
      columns.forEach(col => {
        const td = document.createElement("td");
        td.textContent = row[col] ?? "";
        tr.appendChild(td);
      });
      tbody.appendChild(tr);
    });
  }

  renderRows();

  // Sorting function
  function sortTable(col) {
    rows.sort((a, b) => {
      const x = a[col] ?? "";
      const y = b[col] ?? "";

      // Numeric sort if both values are numbers
      if (!isNaN(x) && !isNaN(y)) {
        return Number(x) - Number(y);
      }

      return x > y ? 1 : x < y ? -1 : 0;
    });

    renderRows();
  }
}

loadData();
