/**
 * MINICT Smart Support Intake, Directed Concept & Automated Advisory Portal
 * Frontend Application Logic: app.js
 * Republic of Rwanda - Ministry of ICT and Innovation (MINICT)
 */

let allApplications = [];
let sectorChartInstance = null;
let gapsChartInstance = null;
let currentViewingAppId = null;

document.addEventListener('DOMContentLoaded', () => {
  loadDashboardData();
});

// Tab Navigation
function switchTab(tabId) {
  document.querySelectorAll('.portal-view').forEach(view => view.classList.remove('active'));
  document.querySelectorAll('.nav-btn').forEach(btn => btn.classList.remove('active'));

  if (tabId === 'applicant') {
    document.getElementById('view-applicant').classList.add('active');
    document.getElementById('tab-applicant').classList.add('active');
  } else if (tabId === 'dashboard') {
    document.getElementById('view-dashboard').classList.add('active');
    document.getElementById('tab-dashboard').classList.add('active');
    loadDashboardData();
  }
}

// SOP Modal
function openSopModal() {
  document.getElementById('sop-modal').style.display = 'flex';
}
function closeSopModal() {
  document.getElementById('sop-modal').style.display = 'none';
}

// Form Helpers
function toggleTinField() {
  const reg = document.getElementById('has_business_registration').value;
  const tinGroup = document.getElementById('tin-group');
  tinGroup.style.display = (reg === 'Yes') ? 'flex' : 'none';
}

function updateSectorGuidance() {
  const sector = document.getElementById('sector').value;
  const lmInput = document.getElementById('line_ministry_name');
  if (!lmInput.value) {
    if (sector === 'HealthTech') lmInput.placeholder = 'e.g. Ministry of Health (MoH) / RBC';
    else if (sector === 'EdTech') lmInput.placeholder = 'e.g. Rwanda Basic Education Board (REB) / MINEDUC';
    else if (sector === 'FinTech') lmInput.placeholder = 'e.g. National Bank of Rwanda (BNR) / RSwitch';
    else if (sector === 'AgriTech') lmInput.placeholder = 'e.g. MINAGRI / RAB';
    else if (sector === 'CleanTech, IoT & Smart Cities') lmInput.placeholder = 'e.g. RURA / City of Kigali';
    else if (sector === 'GovTech & Public Services') lmInput.placeholder = 'e.g. RISA / MINALOC / Irembo';
  }
}

// Live Concept Diagnostic Engine
function evaluateConcept(formData) {
  let score = 20; // baseline
  const gaps = [];
  const advisories = [];
  let routing = 'MINICT Technical Advisory Unit';

  // 1. IP Assessment
  if (formData.has_ip_patent === 'Yes') {
    score += 20;
  } else {
    gaps.push('Missing Intellectual Property / Patent Protection (RDB IP Office)');
    advisories.push('File for software copyright, trademark, or patent at RDB (org.rdb.rw). Having official IP clearance protects your proprietary technology before formal government MoUs.');
  }

  // 2. Data Protection Law No 058/2021
  if (formData.has_data_protection === 'Yes') {
    score += 20;
  } else if (formData.has_data_protection === 'In Progress') {
    score += 10;
    advisories.push('Expedite your Data Controller registration certificate from the NCSA Data Protection & Privacy Office (dppo@ncsa.gov.rw).');
  } else if (formData.has_data_protection === 'No') {
    gaps.push('Non-compliant with Data Protection & Privacy Law N° 058/2021');
    advisories.push('Under Rwandan law, any system processing citizens personal, health, or financial data must register with NCSA before production rollout (https://dppo.ncsa.gov.rw).');
  }

  // 3. Line Ministry Clearance
  const sector = formData.sector;
  if (sector === 'HealthTech') {
    routing = 'Ministry of Health (MoH) & Rwanda Biomedical Centre (RBC)';
    if (formData.has_line_ministry_clearance !== 'Yes') {
      gaps.push('Lacks prior technical clearance from Ministry of Health (MoH) / Rwanda FDA');
      advisories.push('Health technologies must be clinically validated and approved by the MoH Digital Health Working Group before MINICT can execute an MoU.');
    } else {
      score += 20;
    }
  } else if (sector === 'EdTech') {
    routing = 'Rwanda Basic Education Board (REB) & MINEDUC';
    if (formData.has_line_ministry_clearance !== 'Yes') {
      gaps.push('Lacks curriculum alignment approval from REB / MINEDUC');
      advisories.push('EdTech tools intended for Rwandan schools must undergo pedagogical vetting by REB before MINICT can endorse for institutional rollout.');
    } else {
      score += 20;
    }
  } else if (sector === 'FinTech') {
    routing = 'National Bank of Rwanda (BNR) & RSwitch';
    if (formData.has_line_ministry_clearance !== 'Yes') {
      gaps.push('Requires engagement with BNR Regulatory Sandbox or Payment License');
      advisories.push('Solutions facilitating financial transfers or credit scoring must engage the BNR Fintech Regulatory Sandbox before MINICT technical integration.');
    } else {
      score += 20;
    }
  } else if (sector === 'AgriTech') {
    routing = 'Ministry of Agriculture and Animal Resources (MINAGRI) & RAB';
    if (formData.has_line_ministry_clearance === 'Yes') score += 20;
  } else {
    if (formData.has_line_ministry_clearance === 'Yes') score += 20;
  }

  // 4. Business Registration
  if (formData.has_business_registration === 'Yes') {
    score += 10;
  } else {
    gaps.push('Unregistered Entity (No RDB Business Registration / TIN)');
    advisories.push('MINICT cannot execute legally binding MoUs with informal or unregistered entities. Register your business or cooperative via business.rdb.rw.');
  }

  // 5. Stage Mismatch
  if (formData.project_stage === 'Pilot Testing' || formData.project_stage === 'Live in Market') {
    score += 10;
  } else if (formData.project_stage === 'Concept/Idea' && formData.support_type === 'Memorandum of Understanding (MoU)') {
    gaps.push('Stage Mismatch: Requesting formal MoU at Idea/Concept stage without MVP');
    advisories.push('MINICT MoUs are reserved for tested solutions. We recommend joining incubation hubs (e.g. kLab, Norrsken Kigali, 250STARTUPS) to build a functioning MVP first.');
  }

  score = Math.min(100, Math.max(15, score));

  let statusText = 'Ready for Technical Review';
  let explanation = 'Your concept satisfies baseline structural requirements for formal engagement with MINICT.';
  if (score < 50) {
    statusText = 'Early Concept &bull; Prerequisites Needed';
    explanation = 'Foundational gaps identified. We strongly advise addressing IP registration and line ministry validation before scheduling in-person meetings.';
  } else if (score < 75) {
    statusText = 'Moderate Readiness &bull; Action Items Pending';
    explanation = 'Good technological foundation. Complete the pending compliance items to expedite final review.';
  }

  return {
    score,
    statusText,
    explanation,
    gaps,
    advisories,
    routing
  };
}

// Run Interactive Diagnostic Preview
function runLiveDiagnostic() {
  const form = document.getElementById('intake-form');
  const projectTitle = document.getElementById('project_title').value || 'Proposed Innovation';
  const sector = document.getElementById('sector').value;

  if (!sector) {
    alert('Please select a Sector Vertical in Step 3 to run the diagnostic.');
    document.getElementById('sector').focus();
    return;
  }

  const formData = extractFormData();
  const diag = evaluateConcept(formData);

  // Populate Diagnostic Modal
  document.getElementById('diag-app-title').innerHTML = `Automated Structural Evaluation for: <strong>${escapeHtml(projectTitle)}</strong> (${escapeHtml(sector)})`;
  document.getElementById('score-val').textContent = `${diag.score}%`;
  document.getElementById('score-bar').style.width = `${diag.score}%`;
  document.getElementById('score-status-text').innerHTML = diag.statusText;
  document.getElementById('score-explanation').textContent = diag.explanation;

  const gapsListEl = document.getElementById('diag-gaps-list');
  gapsListEl.innerHTML = '';
  if (diag.gaps.length === 0) {
    gapsListEl.innerHTML = '<li style="background:#F0FDF4; border-color:#20744A; color:#166534;">&#10003; No critical structural gaps detected! Ready for technical review.</li>';
  } else {
    diag.gaps.forEach(g => {
      const li = document.createElement('li');
      li.textContent = g;
      gapsListEl.appendChild(li);
    });
  }

  const advListEl = document.getElementById('diag-advisories-list');
  advListEl.innerHTML = '';
  if (diag.advisories.length === 0) {
    advListEl.innerHTML = '<li style="background:#F0FDF4; border-color:#20744A; color:#166534;">&#10003; All governance tracks aligned. Eligible for direct technical scheduling.</li>';
  } else {
    diag.advisories.forEach(a => {
      const li = document.createElement('li');
      li.textContent = a;
      advListEl.appendChild(li);
    });
  }

  document.getElementById('diag-routing').textContent = diag.routing;
  document.getElementById('diagnostic-panel').style.display = 'flex';
}

function closeDiagnostic() {
  document.getElementById('diagnostic-panel').style.display = 'none';
}

function extractFormData() {
  return {
    applicant_name: document.getElementById('applicant_name').value.trim(),
    organization_name: document.getElementById('organization_name').value.trim(),
    entity_type: document.getElementById('entity_type').value,
    email: document.getElementById('email').value.trim(),
    phone: document.getElementById('phone').value.trim(),
    district: document.getElementById('district').value,
    has_business_registration: document.getElementById('has_business_registration').value,
    tin_number: document.getElementById('tin_number').value.trim(),
    support_type: document.getElementById('support_type').value,
    project_title: document.getElementById('project_title').value.trim(),
    sector: document.getElementById('sector').value,
    project_stage: document.getElementById('project_stage').value,
    target_beneficiary: document.getElementById('target_beneficiary').value.trim(),
    problem_statement: document.getElementById('problem_statement').value.trim(),
    proposed_solution: document.getElementById('proposed_solution').value.trim(),
    tech_stack: document.getElementById('tech_stack').value.trim(),
    has_ip_patent: document.getElementById('has_ip_patent').value,
    ip_details: document.getElementById('ip_details').value.trim(),
    has_data_protection: document.getElementById('has_data_protection').value,
    dp_details: document.getElementById('dp_details').value.trim(),
    has_line_ministry_clearance: document.getElementById('has_line_ministry_clearance').value,
    line_ministry_name: document.getElementById('line_ministry_name').value.trim()
  };
}

// Form Submission
async function handleFormSubmit(event) {
  if (event) event.preventDefault();

  const formData = extractFormData();

  try {
    const response = await fetch('/api/applications', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(formData)
    });

    if (response.ok) {
      const res = await response.json();
      closeDiagnostic();
      alert(`Application Successfully Recorded!

Reference Number: ${res.reference_no}
Structural Readiness Score: ${res.readiness_score}%
Initial Status: ${res.initial_status}

Your application is now officially logged in the MINICT system.`);
      document.getElementById('intake-form').reset();
      toggleTinField();
      switchTab('dashboard');
    } else {
      alert('Error recording application. Please check backend connection.');
    }
  } catch (err) {
    console.error('Submission error:', err);
    alert('Failed to connect to the portal backend server.');
  }
}

function submitDirectlyFromDiag() {
  const form = document.getElementById('intake-form');
  if (form.checkValidity()) {
    handleFormSubmit();
  } else {
    alert('Please fill out all required fields marked with * before submitting.');
    closeDiagnostic();
  }
}

// ==================== DASHBOARD & ANALYTICS ====================

async function loadDashboardData() {
  try {
    const [analyticsRes, appsRes] = await Promise.all([
      fetch('/api/analytics'),
      fetch('/api/applications')
    ]);

    if (analyticsRes.ok && appsRes.ok) {
      const analytics = await analyticsRes.json();
      allApplications = await appsRes.json();

      updateKpis(analytics);
      renderCharts(analytics);
      renderTable(allApplications);
    }
  } catch (err) {
    console.error('Error fetching dashboard data:', err);
  }
}

function updateKpis(analytics) {
  document.getElementById('kpi-total').textContent = analytics.total_applications || 0;
  document.getElementById('kpi-ready').textContent = analytics.high_readiness_count || 0;
  document.getElementById('kpi-advised').textContent = analytics.medium_readiness_count + analytics.low_readiness_count || 0;

  const referredCount = (analytics.statuses && analytics.statuses['Referred to Line Ministry']) || 0;
  document.getElementById('kpi-referred').textContent = referredCount;
}

function renderCharts(analytics) {
  const sectorCtx = document.getElementById('sectorChart').getContext('2d');
  const gapsCtx = document.getElementById('gapsChart').getContext('2d');

  // Destroy previous charts if existing
  if (sectorChartInstance) sectorChartInstance.destroy();
  if (gapsChartInstance) gapsChartInstance.destroy();

  // Sector Chart
  const sectorLabels = Object.keys(analytics.sectors || {});
  const sectorCounts = Object.values(analytics.sectors || {});

  sectorChartInstance = new Chart(sectorCtx, {
    type: 'bar',
    data: {
      labels: sectorLabels.length ? sectorLabels : ['HealthTech', 'EdTech', 'FinTech', 'AgriTech', 'AI & NLP'],
      datasets: [{
        label: 'Number of Applications',
        data: sectorCounts.length ? sectorCounts : [3, 2, 2, 1, 1],
        backgroundColor: ['#003366', '#00A3E0', '#20744A', '#E6A117', '#6B21A8', '#0A2540'],
        borderRadius: 6
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false }
      },
      scales: {
        y: {
          beginAtZero: true,
          ticks: { stepSize: 1 }
        }
      }
    }
  });

  // Gaps Diagnostic Chart
  const gapsData = analytics.gaps_percentage || {
    missing_ip_patent: 65,
    missing_data_protection: 50,
    missing_line_ministry_clearance: 60,
    unregistered_business: 40,
    idea_stage_only: 30
  };

  gapsChartInstance = new Chart(gapsCtx, {
    type: 'bar',
    data: {
      labels: [
        'Missing RDB IP/Patent',
        'Missing NCSA Privacy Registration',
        'Lacking Line Ministry Clearance',
        'Unregistered Business Entity',
        'Idea Stage (No MVP)'
      ],
      datasets: [{
        label: '% of Applicants Falling Short',
        data: [
          gapsData.missing_ip_patent,
          gapsData.missing_data_protection,
          gapsData.missing_line_ministry_clearance,
          gapsData.unregistered_business,
          gapsData.idea_stage_only
        ],
        backgroundColor: '#DC2626',
        borderRadius: 6
      }]
    },
    options: {
      indexAxis: 'y',
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false }
      },
      scales: {
        x: {
          beginAtZero: true,
          max: 100,
          ticks: {
            callback: value => value + '%'
          }
        }
      }
    }
  });
}

function renderTable(apps) {
  const tbody = document.getElementById('applications-tbody');
  tbody.innerHTML = '';

  if (apps.length === 0) {
    tbody.innerHTML = '<tr><td colspan="9" style="text-align:center; padding:20px; color:#64748B;">No applications logged yet.</td></tr>';
    return;
  }

  apps.forEach(app => {
    const tr = document.createElement('tr');

    let statusClass = 'status-advised';
    if (app.status === 'Ready for Technical Review') statusClass = 'status-ready';
    else if (app.status === 'Referred to Line Ministry') statusClass = 'status-referred';
    else if (app.status === 'Escalated to Permanent Secretary') statusClass = 'status-escalated';

    let scoreClass = 'score-low';
    if (app.readiness_score >= 70) scoreClass = 'score-high';
    else if (app.readiness_score >= 45) scoreClass = 'score-med';

    tr.innerHTML = `
      <td><span class="ref-code">${escapeHtml(app.reference_no)}</span></td>
      <td style="color:#64748B; font-size:0.8rem;">${escapeHtml(app.created_at ? app.created_at.split(' ')[0] : '')}</td>
      <td>
        <strong>${escapeHtml(app.organization_name || app.applicant_name)}</strong>
        <div style="font-size:0.78rem; color:#64748B;">${escapeHtml(app.applicant_name)}</div>
      </td>
      <td><span class="badge-tag" style="background:#F1F5F9; color:#334155; border:none; padding:2px 6px;">${escapeHtml(app.sector)}</span></td>
      <td style="font-size:0.82rem;">${escapeHtml(app.support_type)}</td>
      <td><span class="score-badge ${scoreClass}">${app.readiness_score}%</span></td>
      <td><span class="status-badge ${statusClass}">${escapeHtml(app.status)}</span></td>
      <td style="font-size:0.82rem; color:#475569;">${escapeHtml(app.assigned_officer || 'Unassigned')}</td>
      <td>
        <button class="btn-view-app" onclick="openDetailModal(${app.id})">Inspect</button>
      </td>
    `;
    tbody.appendChild(tr);
  });
}

function filterTable() {
  const searchVal = document.getElementById('table-search').value.toLowerCase();
  const sectorVal = document.getElementById('filter-sector').value;
  const statusVal = document.getElementById('filter-status').value;

  const filtered = allApplications.filter(app => {
    const matchSearch = !searchVal || 
      (app.reference_no && app.reference_no.toLowerCase().includes(searchVal)) ||
      (app.organization_name && app.organization_name.toLowerCase().includes(searchVal)) ||
      (app.applicant_name && app.applicant_name.toLowerCase().includes(searchVal)) ||
      (app.project_title && app.project_title.toLowerCase().includes(searchVal));

    const matchSector = !sectorVal || (app.sector === sectorVal);
    const matchStatus = !statusVal || (app.status === statusVal);

    return matchSearch && matchSector && matchStatus;
  });

  renderTable(filtered);
}

// Application Detail Modal
function openDetailModal(id) {
  const app = allApplications.find(a => a.id === id);
  if (!app) return;

  currentViewingAppId = id;
  document.getElementById('modal-ref-title').textContent = `${app.reference_no} &bull; ${app.project_title}`;
  document.getElementById('modal-org-subtitle').textContent = `${app.organization_name} (${app.applicant_name}) &bull; ${app.sector} &bull; Stage: ${app.project_stage}`;
  document.getElementById('modal-status-select').value = app.status;

  const gaps = Array.isArray(app.critical_gaps) ? app.critical_gaps : [];
  const advs = Array.isArray(app.advisory_recommendations) ? app.advisory_recommendations : [];

  const html = `
    <div style="display:grid; grid-template-columns: 2fr 1fr; gap:20px;">
      <div>
        <h4 style="color:#003366; margin-bottom:8px;">Directed Concept Note</h4>
        <p><strong>Problem Statement:</strong> ${escapeHtml(app.problem_statement || 'N/A')}</p>
        <p style="margin-top:8px;"><strong>Proposed Solution:</strong> ${escapeHtml(app.proposed_solution || 'N/A')}</p>
        <p style="margin-top:8px;"><strong>Technical Architecture:</strong> <code>${escapeHtml(app.tech_stack || 'N/A')}</code></p>
        <p style="margin-top:8px;"><strong>Target Beneficiaries:</strong> ${escapeHtml(app.target_beneficiary || 'N/A')}</p>
        
        <h4 style="color:#003366; margin-top:16px; margin-bottom:8px;">Structural Assessment Dimensions</h4>
        <ul style="font-size:0.88rem; padding-left:18px;">
          <li><strong>IP / Patent:</strong> ${escapeHtml(app.has_ip_patent)} (${escapeHtml(app.ip_details || 'No filing')})</li>
          <li><strong>Data Protection (Law 058/2021):</strong> ${escapeHtml(app.has_data_protection)} (${escapeHtml(app.dp_details || 'No cert')})</li>
          <li><strong>Line Ministry Clearance:</strong> ${escapeHtml(app.has_line_ministry_clearance)} (${escapeHtml(app.line_ministry_name || 'None')})</li>
          <li><strong>Business Entity (RDB TIN):</strong> ${escapeHtml(app.has_business_registration)} (${escapeHtml(app.tin_number || 'Unregistered')})</li>
        </ul>
      </div>

      <div style="background:#F8FAFC; padding:16px; border-radius:8px; border:1px solid #E2E8F0;">
        <h4 style="color:#003366; margin-bottom:8px;">Automated Diagnostic</h4>
        <div style="font-size:1.6rem; font-weight:800; color:#003366;">${app.readiness_score}%</div>
        <div style="font-size:0.8rem; color:#64748B; margin-bottom:12px;">Structural Readiness Score</div>
        
        <strong>Recommended Routing:</strong>
        <p style="font-size:0.85rem; color:#166534; font-weight:600; margin-bottom:10px;">${escapeHtml(app.line_ministry_routing || 'MINICT Advisory')}</p>

        <strong>Identified Gaps:</strong>
        <ul style="font-size:0.78rem; color:#DC2626; padding-left:16px; margin-bottom:10px;">
          ${gaps.map(g => `<li>${escapeHtml(g)}</li>`).join('') || '<li>None</li>'}
        </ul>

        <strong>Assigned Technical Officer:</strong>
        <p style="font-size:0.85rem; color:#1E293B;">${escapeHtml(app.assigned_officer || 'Unassigned')}</p>
      </div>
    </div>
  `;

  document.getElementById('modal-content').innerHTML = html;
  document.getElementById('detail-modal').style.display = 'flex';
}

function closeDetailModal() {
  document.getElementById('detail-modal').style.display = 'none';
  currentViewingAppId = null;
}

async function saveStatusUpdate() {
  if (!currentViewingAppId) return;

  const newStatus = document.getElementById('modal-status-select').value;
  try {
    const res = await fetch('/api/applications/update', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        id: currentViewingAppId,
        status: newStatus
      })
    });

    if (res.ok) {
      alert('Application status updated successfully!');
      closeDetailModal();
      loadDashboardData();
    }
  } catch (err) {
    console.error('Update error:', err);
    alert('Failed to update status.');
  }
}

function exportDataCsv() {
  window.location.href = '/api/export';
}

function escapeHtml(str) {
  if (!str) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}
