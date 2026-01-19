let rows = [];
let columns = [
  "pid", "name", "level", 
  "Class", "PvP", "Rank", "Role", "Joined", "Login",
  "gold", "gems", "last_donation"
];

let visibleColumns = new Set(columns); // all visible by default
let sortState = {
  column: null,
  direction: 1
};


// -----------------------------
// Fetch Json Timestamp
// -----------------------------

/**
 * Affiche la date/heure du dernier commit qui a modifié docs/delulu_data.json
 * - Source primaire: GitHub API (commits?path=...)
 * - Fallback: Last-Modified du fichier brut (raw.githubusercontent.com)
 * - Affichage: anglais, 24h, sans secondes, adapté au fuseau du navigateur
 */
async function fetchJsonTimestamp() {
  const USER = "khahazad";
  const REPO = "dlu-scraper-insights";
  const BRANCH = "main";
  const FILE_PATH = "docs/delulu_data.json";

  const tsEl = document.getElementById("dataTimestamp");
  if (!tsEl) return;

  // Petite fonction de formatage "universel"
  const formatLocal = (date) =>
    date.toLocaleString("en-US", {
      year: "numeric",
      month: "short", // Jan, Feb, ...
      day: "2-digit",
      hour: "2-digit",
      minute: "2-digit",
      hour12: false, // 24h to avoid AM/PM ambiguity
    });

  // 1) Tentative via GitHub API (dernier commit qui a touché le fichier)
  try {
    const apiUrl =
      `https://api.github.com/repos/${USER}/${REPO}/commits` +
      `?path=${encodeURIComponent(FILE_PATH)}` +
      `&sha=${encodeURIComponent(BRANCH)}` +
      `&per_page=1`;

    const resp = await fetch(apiUrl, {
      headers: {
        // Optionnel: indiquer qu'on accepte du JSON; pas besoin de token public
        "Accept": "application/vnd.github+json",
      },
    });

    if (!resp.ok) {
      throw new Error(`GitHub API HTTP ${resp.status}`);
    }

    const commits = await resp.json();
    if (Array.isArray(commits) && commits.length > 0) {
      // La date du commit (UTC, ex: "2026-01-19T13:05:00Z")
      const isoDate = commits[0]?.commit?.committer?.date || commits[0]?.commit?.author?.date;
      if (isoDate) {
        const localDate = new Date(isoDate); // conversion auto vers l'heure locale du navigateur
        tsEl.textContent = `Last data update: ${formatLocal(localDate)}`;
        return; // Succès → on sort
      }
    }

    // Si pas de commit trouvé / pas de date → on tente le fallback
    throw new Error("No commit info for the file.");
  } catch (e) {
    console.warn("Primary (GitHub commits API) failed:", e);
  }

  // 2) Fallback: HEAD sur le fichier brut pour lire Last-Modified
  try {
    const rawUrl = `https://raw.githubusercontent.com/${USER}/${REPO}/${BRANCH}/${FILE_PATH}`;
    const head = await fetch(rawUrl, { method: "HEAD" });

    if (!head.ok) {
      throw new Error(`Raw HEAD HTTP ${head.status}`);
    }

    const lastModified = head.headers.get("Last-Modified"); // ex: "Mon, 19 Jan 2026 13:05:00 GMT"
    if (lastModified) {
      const localDate = new Date(lastModified);
      tsEl.textContent = `Last data update: ${formatLocal(localDate)}`;
      return;
    }

    throw new Error("No Last-Modified header.");
  } catch (e) {
    console.warn("Fallback (HEAD Last-Modified) failed:", e);
  }

  // 3) Si tout échoue, on affiche un message discret
  tsEl.textContent = "Last data update: unavailable";
}

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
  document.querySelectorAll("#roleSelector input")
    .forEach(cb => cb.onchange = applyFilters);
  
  // Column selector
  document.querySelectorAll("#columnSelector input")
    .forEach(cb => cb.onchange = updateVisibleColumns);

  // ExportTable button
  document.getElementById("exportBtn").onclick = exportTable;

  // Apply filter immediately
  applyFilters();
  updateVisibleColumns();
}

// -----------------------------
// Dropdown toggle
// -----------------------------
document.addEventListener("click", function (e) {
  document.querySelectorAll(".dropdown").forEach(drop => {
    if (drop.contains(e.target)) {
      drop.classList.toggle("show");
    } else {
      drop.classList.remove("show");
    }
  });
});

// -----------------------------
// Update Visible Columns
// -----------------------------
function updateVisibleColumns() {
  visibleColumns = new Set(
    Array.from(document.querySelectorAll("#columnSelector input:checked"))
      .map(cb => cb.value)
  );

  // Rebuild table header + rerender rows
  const table = document.getElementById("guildTable");
  table.innerHTML = ""; // clear old table
  buildTable();
  applyFilters();
}

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

  // --- Colonne # (non triable, fixe en 1ère position) ---
  const thNum = document.createElement("th");
  thNum.textContent = "#";
  thNum.className = "num-col";
  thNum.style.width = "4ch";
  thNum.style.textAlign = "right";
  headerRow.appendChild(thNum);

  // --- Colonnes existantes (triables) ---
  Array.from(visibleColumns).forEach(col => {
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

  data.forEach((row, i) => {
    const tr = document.createElement("tr");

    // --- Cellule numéro (1-based, reflète l'ordre affiché) ---
    const tdNum = document.createElement("td");
    tdNum.textContent = i + 1;
    tdNum.className = "num-col";
    tdNum.style.textAlign = "right";
    tr.appendChild(tdNum);

    // --- Autres colonnes visibles ---
    Array.from(visibleColumns).forEach(col => {
      const td = document.createElement("td");

      if (col === "pid") {
        const a = document.createElement("a");
        a.href = `https://demonicscans.org/player.php?pid=${row.pid}`;
        a.textContent = row.pid;
        a.target = "_blank";
        td.appendChild(a);
      } else {
        td.textContent = row[col] ?? "";
      }

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

    // Detect empty values
    const xEmpty = (x === null || x === undefined || x === "");
    const yEmpty = (y === null || y === undefined || y === "");

    // Empty values always last
    if (xEmpty && !yEmpty) return 1;
    if (!xEmpty && yEmpty) return -1;
    if (xEmpty && yEmpty) return 0;

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

  const visible = Array.from(visibleColumns);
  const index = visible.indexOf(col);
  const th = document.querySelectorAll("th")[index + 1]; // index +1 = saute la colonne "#"
  const icon = th.querySelector(".sort-icon");
  icon.textContent = sortState.direction === 1 ? " ▲" : " ▼";

  applyFilters();
}

// -----------------------------
// Filtering
// -----------------------------
function applyFilters() {
  const search = document.getElementById("searchInput").value.trim().toLowerCase();

  const selectedRoles = Array.from(
    document.querySelectorAll(".dropdown-content input:checked")
  ).map(cb => cb.value);

  // Détermine si l'utilisateur utilise mode OR ("|")
  const useOr = search.includes("|");

  // Prépare termes selon le mode
  let terms = [];
  if (useOr) {
    terms = search.split("|").map(t => t.trim()).filter(t => t.length > 0);
  } else if (search.length > 0) {
    terms = [search]; // un seul bloc de texte si pas de "|"
  }

  const filtered = rows.filter(row => {
    if (!selectedRoles.includes(row.Role)) return false;

    const text = Object.values(row).join(" ").toLowerCase();

    // Si pas de recherche → passe
    if (terms.length === 0) return true;

    // Mode OR → au moins un terme présent
    if (useOr) {
      return terms.some(term => text.includes(term));
    }

    // Mode normal (pas de OR) → recherche "classique"
    return text.includes(search);
  });

  renderRows(filtered);
}

// -----------------------------
// Export Table
// -----------------------------
function exportTable() {
  // Get currently displayed rows
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

  // Build CSV header using displayed column titles
  const cols = Array.from(visibleColumns);
  let csv = cols.map(formatHeader).join(",") + "\n";

  // Build CSV rows
  filtered.forEach(row => {
    const line = cols.map(col => {
      let value = row[col] ?? "";
      // Escape quotes
      value = String(value).replace(/"/g, '""');
      return `"${value}"`;
    }).join(",");
    csv += line + "\n";
  });

  // Trigger download
  const blob = new Blob([csv], { type: "text/csv" });
  const url = URL.createObjectURL(blob);

  const a = document.createElement("a");
  a.href = url;
  a.download = "delulu_export.csv";
  a.click();

  URL.revokeObjectURL(url);
}

// -----------------------------
loadData();
fetchJsonTimestamp();
