const API_URL = "http://127.0.0.1:5000/analyze";
const RUN_API_URL = "http://127.0.0.1:5000/run";

/*
 * DOM elements
 */

const codeInput = document.getElementById("codeInput");

const resultBox = document.getElementById("result");

const loading = document.getElementById("loading");
const analyzeButton = document.getElementById("analyzeButton");

const runButton = document.getElementById("runButton");

const summary = document.getElementById("summary");

const issuesBox = document.getElementById("issues");

const positiveBox = document.getElementById("positivePoints");

const concept = document.getElementById("concept");

const explanation = document.getElementById("explanation");

const hints = document.getElementById("hints");

const nextStep = document.getElementById("nextStep");

const fixSection = document.getElementById("fixSection");

const verificationSection = document.getElementById("verificationSection");

const lineCount = document.getElementById("lineCount");

let activeIssueLine = null;

function focusEditorLine(line) {
  const targetLine = Number(line);

  if (!Number.isInteger(targetLine) || targetLine < 1) {
    return;
  }

  const lines = codeInput.value.split("\n");

  if (targetLine > lines.length) {
    return;
  }

  const start = lines
    .slice(0, targetLine - 1)
    .reduce(
      (position, currentLine) => position + currentLine.length + 1,
      0,
    );

  const end = start + lines[targetLine - 1].length;

  codeInput.focus();
  codeInput.setSelectionRange(start, end);

  const lineHeight = parseFloat(
    window.getComputedStyle(codeInput).lineHeight,
  );

  if (Number.isFinite(lineHeight)) {
    codeInput.scrollTop = Math.max(
      0,
      (targetLine - 1) * lineHeight - 90,
    );
  }

  activeIssueLine = targetLine;
  updateLineNumbers();
}


/*
 * Update line counter
 */

function updateLineCount() {
  const code = codeInput.value;

  const lines = code.length === 0 ? 0 : code.split("\n").length;

  lineCount.textContent = `Lines: ${lines}`;
}

/*
 * Clear editor
 */

function clearCode() {
  codeInput.value = "";

  resultBox.classList.remove("visible");

  updateLineCount();

  codeInput.focus();
}

/*
 * Render review issues
 */

function renderIssues(issues) {
  issuesBox.innerHTML = "";

  if (!issues || issues.length === 0) {
    issuesBox.innerHTML = `
            <div class="positive">
                ✅ No issues were detected
                by the current checks.
            </div>
        `;

    return;
  }

  issues.forEach((issue) => {
    const div = document.createElement("div");

    const severity = (issue.severity || "warning").toLowerCase();

    div.className = `issue ${severity}`;

    const issueLine = Number(issue.line);

    if (Number.isInteger(issueLine) && issueLine > 0) {
      div.classList.add("issue-clickable");
      div.tabIndex = 0;
      div.setAttribute(
        "aria-label",
        `Go to line ${issueLine}: ${issue.message || "Issue"}`,
      );

      const goToIssueLine = () => focusEditorLine(issueLine);

      div.addEventListener("click", goToIssueLine);

      div.addEventListener("keydown", (event) => {
        if (event.key === "Enter" || event.key === " ") {
          event.preventDefault();
          goToIssueLine();
        }
      });
    }


    div.innerHTML = `

            <div class="issue-header">

                <span class="issue-category">
                    ❌
                    ${escapeHtml(issue.category || "Issue")}
                </span>

                <span class="severity-badge">
                    ${escapeHtml(issue.severity || "warning")}
                </span>

            </div>

            <p>
                ${escapeHtml(issue.message || "No message available.")}
            </p>

            <p class="issue-line">

                <strong>
                    Line:
                </strong>

                ${issue.line ?? "Unknown"}

            </p>

            <p>

                <strong>
                    💡 Suggestion:
                </strong>

                ${escapeHtml(issue.suggestion || "Review this issue.")}

            </p>
        `;

    issuesBox.appendChild(div);
  });
}

/*
 * Render positive points
 */

function renderPositivePoints(points) {
  positiveBox.innerHTML = "";

  if (!points || points.length === 0) {
    positiveBox.innerHTML = `
            <div class="empty">
                No positive observations
                were returned.
            </div>
        `;

    return;
  }

  points.forEach((point) => {
    const div = document.createElement("div");

    div.className = "positive";

    div.textContent = `✓ ${point}`;

    positiveBox.appendChild(div);
  });
}

/*
 * Render tutor result
 */

function renderTutor(tutor) {
  if (!tutor) {
    concept.textContent = "Not available";

    explanation.textContent = "Tutor information was not returned.";

    hints.innerHTML = "";

    nextStep.textContent = "Continue testing your code.";

    return;
  }

  concept.textContent = tutor.concept || "Code Reasoning";

  explanation.textContent = tutor.explanation || "No explanation available.";

  nextStep.textContent = tutor.next_step || "Continue testing your code.";

  hints.innerHTML = "";

  if (tutor.hints && tutor.hints.length > 0) {
    tutor.hints.forEach((hint, index) => {
      const div = document.createElement("div");

      div.className = "hint";

      const number = document.createElement("span");

      number.className = "hint-number";

      number.textContent = index + 1;

      const text = document.createElement("span");

      text.textContent = hint;

      div.appendChild(number);

      div.appendChild(text);

      hints.appendChild(div);
    });
  } else {
    hints.innerHTML = `
            <div class="empty">
                No hints are available
                for this code.
            </div>
        `;
  }
}

/*
 * Render fixer result
 */

function renderFix(fix) {
  fixSection.innerHTML = "";

  if (!fix || !fix.success || !fix.fixed_code) {
    fixSection.innerHTML = `
            <div class="fix-unavailable">
                🔧 No automatic fix is
                currently available for
                this problem.
            </div>
        `;

    return;
  }

  const wrapper = document.createElement("div");

  wrapper.className = "fix-success";

  wrapper.innerHTML = `
        <strong>
            ✅ A local automatic fix
            is available.
        </strong>

        <p>
            ${escapeHtml(
              fix.explanation || "The system generated a possible fix.",
            )}
        </p>
    `;

  fixSection.appendChild(wrapper);

  const codeBlock = document.createElement("pre");

  codeBlock.className = "code-output";

  codeBlock.textContent = fix.fixed_code;

  fixSection.appendChild(codeBlock);

  if (fix.changes && fix.changes.length > 0) {
    const title = document.createElement("p");

    title.innerHTML = "<strong>Changes made:</strong>";

    fixSection.appendChild(title);

    fix.changes.forEach((change) => {
      const item = document.createElement("div");

      item.className = "change-item";

      item.textContent = `✓ ${change}`;

      fixSection.appendChild(item);
    });
  }
}

/*
 * Render verification result
 */

function renderVerification(verification) {
  verificationSection.innerHTML = "";

  if (!verification) {
    verificationSection.innerHTML = `
            <div class="empty">
                ℹ️ No automatic fix was
                generated, so fix
                verification was not required.
            </div>
        `;

    return;
  }

  const box = document.createElement("div");

  box.className = verification.success
    ? "verification success"
    : "verification failed";

  const status = document.createElement("div");

  status.className = "verification-status";

  status.textContent = verification.success
    ? "✅ Fixed code passed verification."
    : "❌ Fixed code failed verification.";

  box.appendChild(status);

  if (verification.details && verification.details.length > 0) {
    verification.details.forEach((detail) => {
      const item = document.createElement("div");

      item.className = "verification-detail";

      item.textContent = `• ${detail}`;

      box.appendChild(item);
    });
  }

  if (verification.errors && verification.errors.length > 0) {
    verification.errors.forEach((error) => {
      const item = document.createElement("div");

      item.className = "verification-error";

      item.textContent = error;

      box.appendChild(item);
    });
  }

  verificationSection.appendChild(box);
}

/*
 * Main analysis function
 */

async function analyzeCode() {
  const code = codeInput.value;

  if (!code.trim()) {
    alert("Please enter Python code.");

    return;
  }

  /*
   * Loading state
   */

  loading.classList.add("active");

  analyzeButton.disabled = true;

  analyzeButton.textContent = "⏳ Analyzing...";

  resultBox.classList.remove("visible");

  try {
    /*
     * API request
     */

    const response = await fetch(API_URL, {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify({
        code: code,
      }),
    });

    const data = await response.json();

    /*
     * API error
     */

    if (!response.ok || !data.success) {
      throw new Error(data.error || "Analysis failed.");
    }

    /*
     * Render all results
     */

    summary.textContent = data.review.summary;

    renderIssues(data.review.issues);

    renderPositivePoints(data.review.positive_points);

    renderTutor(data.tutor);

    renderFix(data.fix);

    renderVerification(data.verification);

    /*
     * Show results
     */

    resultBox.classList.add("visible");

    /*
     * Scroll to result
     */

    resultBox.scrollIntoView({
      behavior: "smooth",
      block: "start",
    });
  } catch (error) {
    console.error("Analysis error:", error);

    alert(error.message || "Could not connect to the AI Coding Assistant API.");
  } finally {
    loading.classList.remove("active");

    analyzeButton.disabled = false;

    analyzeButton.textContent = "🔍 Analyze Code";
  }
}

/*
 * Run Python code
 */

async function runCode() {
  const code = codeInput.value;

  const consoleOutput = document.getElementById("consoleOutput");
  const consoleStatus = document.getElementById("consoleStatus");

  if (!code.trim()) {
    consoleStatus.textContent = "Error";
    consoleOutput.innerHTML =
      '<div class="console-error">Please enter Python code.</div>';
    return;
  }

  runButton.disabled = true;
  runButton.textContent = "⏳ Running...";

  consoleStatus.textContent = "Running";
  consoleOutput.innerHTML =
    '<div class="console-info">Executing Python code...</div>';

  try {
    const response = await fetch(RUN_API_URL, {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify({
        code: code,
      }),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || "Code execution failed.");
    }

    if (data.success) {
      consoleStatus.textContent = "Success";

      const output = data.stdout || "Code executed successfully.";

      consoleOutput.innerHTML = `<div class="console-success">${escapeHtml(output)}</div>`;
    } else if (data.timed_out) {
      consoleStatus.textContent = "Timed out";

      consoleOutput.innerHTML =
        '<div class="console-error">Execution timed out.</div>';
    } else {
      consoleStatus.textContent = "Error";

      const errorOutput = data.stderr || "Code execution failed.";

      consoleOutput.innerHTML = `<div class="console-error">${escapeHtml(errorOutput)}</div>`;
    }
  } catch (error) {
    console.error("Run error:", error);

    consoleStatus.textContent = "Error";

    consoleOutput.innerHTML = `<div class="console-error">${escapeHtml(
      error.message || "Could not connect to the AI Coding Assistant API.",
    )}</div>`;
  } finally {
    runButton.disabled = false;
    runButton.textContent = "▶ Run Code";
  }
}

/*
 * Basic HTML escaping
 *
 * This is important because API/AI
 * generated text should not be inserted
 * directly as executable HTML.
 */

function escapeHtml(value) {
  const div = document.createElement("div");

  div.textContent = String(value);

  return div.innerHTML;
}

/*
 * Editor events
 */

codeInput.addEventListener("input", updateLineCount);

/*
 * Initial state
 */

updateLineCount();

// Python-style editor indentation
codeInput.addEventListener("keydown", function (event) {
  if (event.key !== "Enter") {
    return;
  }

  const start = this.selectionStart;
  const end = this.selectionEnd;

  const beforeCursor = this.value.slice(0, start);
  const currentLine = beforeCursor.split("\n").pop();

  const indentationMatch = currentLine.match(/^\s*/);
  let indentation = indentationMatch ? indentationMatch[0] : "";

  const trimmedLine = currentLine.trimEnd();

  // Continue indentation after a Python block statement.
  if (trimmedLine.endsWith(":")) {
    indentation += "    ";
  }

  event.preventDefault();

  const insertion = "\n" + indentation;

  this.value = this.value.slice(0, start) + insertion + this.value.slice(end);

  const newCursorPosition = start + insertion.length;

  this.selectionStart = newCursorPosition;
  this.selectionEnd = newCursorPosition;

  updateLineCount();
});

/* F1 - Python editor line numbers */

const lineNumbers = document.getElementById("lineNumbers");

function updateLineNumbers() {
  const lines = codeInput.value.split("\n").length;

  lineNumbers.innerHTML = Array.from(
    { length: lines },

    (_, index) => {
      const lineNumber = index + 1;

      const activeClass =
        lineNumber === activeIssueLine ? " active-issue-line" : "";

      return `<div class="${activeClass.trim()}">${lineNumber}</div>`;
    },

  ).join("");

  lineNumbers.scrollTop = codeInput.scrollTop;
}

codeInput.addEventListener("input", updateLineNumbers);

codeInput.addEventListener("scroll", function () {
  lineNumbers.scrollTop = codeInput.scrollTop;
});

updateLineNumbers();

/* F1 - Python indentation controls */

codeInput.addEventListener("keydown", function (event) {
  if (event.key !== "Tab") {
    return;
  }

  event.preventDefault();

  const start = this.selectionStart;
  const end = this.selectionEnd;
  const value = this.value;

  if (event.shiftKey) {
    const lineStart = value.lastIndexOf("\n", start - 1) + 1;
    const lineText = value.slice(lineStart, start);

    if (lineText.startsWith("    ")) {
      this.value = value.slice(0, lineStart) + value.slice(lineStart + 4);

      this.selectionStart = Math.max(start - 4, lineStart);
      this.selectionEnd = Math.max(end - 4, lineStart);
    } else if (lineText.startsWith(" ")) {
      const removeCount = Math.min(4, lineText.match(/^ */)[0].length);

      this.value =
        value.slice(0, lineStart) + value.slice(lineStart + removeCount);

      this.selectionStart = Math.max(start - removeCount, lineStart);
      this.selectionEnd = Math.max(end - removeCount, lineStart);
    }

    updateLineCount();
    updateLineNumbers();
    return;
  }

  this.value = value.slice(0, start) + "    " + value.slice(end);

  this.selectionStart = start + 4;
  this.selectionEnd = start + 4;

  updateLineCount();
  updateLineNumbers();
});

/* F1 - Refresh line numbers after Python Enter handling */

codeInput.addEventListener("keyup", function (event) {
  if (event.key === "Enter") {
    updateLineNumbers();
  }
});
