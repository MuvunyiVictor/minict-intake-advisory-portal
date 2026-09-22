# MINICT Smart Support Intake, Directed Concept & Automated Advisory Portal

> **A Strategic Digital Gatekeeper and Ecosystem Intelligence System for the Ministry of ICT and Innovation (MINICT), Republic of Rwanda.**  
> *Prepared for the Permanent Secretary (PS) by Victor Muvunyi (Innovation & Emerging Technologies).*

---

## 1. Executive Summary & Policy Rationale

The Ministry of ICT and Innovation (MINICT) receives hundreds of outreach requests annually from tech founders, researchers, startups, and development partners. These applicants request:
* **Memoranda of Understanding (MoUs)** for nationwide partnerships.
* **Official Letters of Endorsement** for global grant competitions and accelerators.
* **Technical Consultations & GovTech Pilot Integrations**.
* **Regulatory Sandbox Navigation** (e.g., eKash switch integration, healthtech trials).

### The Core Problem:
1. **Inefficient & Unrecorded Intake:** Inquiries arrive through disparate channels (physical letters, ad-hoc emails, executive referrals). Many are assigned directly to technical officers without initial triaging, leaving no institutional audit trail or performance metrics.
2. **Foundational Structural Deficits:** The majority of applicants approach MINICT prematurely. They lack basic structural prerequisites, such as:
   - **Intellectual Property (IP) Protection / Patent Filing** with the Rwanda Development Board (RDB).
   - **Data Protection & Privacy Compliance** under Law N° 058/2021 with the National Cyber Security Authority (NCSA).
   - **Domain Clearance from Line Ministries** (e.g., Health applications approaching MINICT without Ministry of Health / RBC / Rwanda FDA validation; EdTech applications without Rwanda Basic Education Board / MINEDUC clearance).
3. **Absence of Ecosystem Analytics:** Because intake has not been digitally standardized, leadership cannot measure where Rwandan tech interest is concentrated or which systemic gaps exist across startups.

### The Solution:
An intelligent **Intake & Automated Advisory Portal** embeddable into the official MINICT website ([minict.gov.rw](https://www.minict.gov.rw/)) and the national ecosystem hub ([innovaterwanda.rw](https://innovaterwanda.rw/en)).

The portal forces applicants through a **Directed Concept Note**, performs an **automated real-time gap analysis**, generates an immediate **Smart Advisory Clearance Report**, and logs every submission into a **Leadership Intelligence Dashboard**.

---

## 2. System Architecture & Core Capabilities

```
+-----------------------------------------------------------------------------------+
|                        APPLICANT & INNOVATOR INTERFACE                             |
|  - Step 1: Entity Profile & RDB Registration Verification                         |
|  - Step 2: Specific Support Category Requested (MoU, Endorsement, Sandbox)        |
|  - Step 3: Directed Concept Note (Problem, Solution Architecture, Tech Stack)     |
|  - Step 4: Structural Dimensions (RDB IP/Patent, NCSA Privacy, Line Clearances)   |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
|                     AUTOMATED AI / RULE-BASED ADVISORY ENGINE                     |
|  * Calculates Structural Readiness Score (0 - 100%)                                |
|  * Flags Critical Gaps (Unprotected IP, Missing DPPO cert, Missing Line Approval)|
|  * Emits Tailored Advisory Action Plan & Institutional Routing (MoH, REB, BNR)    |
|  * Generates Downloadable / Printable Concept Diagnostic Clearance Report         |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
|                      CENTRAL REGISTRY & SQLITE DATABASE                           |
|  * Issues Official Tracking Reference (e.g., MINICT-2026-006)                     |
|  * Records Full Concept Note, Entity Details, and Diagnostic Audit Trail           |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
|                   MINICT LEADERSHIP & POLICY INTELLIGENCE DASHBOARD                |
|  * Executive KPIs (Total Inquiries, Ready for MoU, Advised, Referred to Ministries)|
|  * Sectoral Density Analytics (HealthTech, EdTech, FinTech, AgriTech, AI)         |
|  * Ecosystem Gaps Diagnostic Matrix (% Lacking IP, % Lacking Data Protection)     |
|  * Dynamic Policy Recommendations for Ministry Leadership                         |
|  * Application Lifecycle Management (Assign Officer, Escalate to PS, Export CSV)  |
+-----------------------------------------------------------------------------------+
```

---

## 3. The 4 Structural Readiness Pillars (Directed Assessment)

The portal evaluates every concept against four foundational criteria before permitting physical appointments or formal MoUs:

1. **Intellectual Property (IP) & Patent Safeguards:**
   - *Requirement:* Software copyright, trademark, or patent registered with the RDB Intellectual Property Division.
   - *Rationale:* Protects founders from IP theft and shields MINICT from facilitating disputed proprietary assets.
2. **Data Protection & Privacy Compliance (Law N° 058/2021):**
   - *Requirement:* Registration as a Data Controller or Processor with the NCSA Data Protection & Privacy Office (DPPO).
   - *Rationale:* Ensures that any system collecting citizen, health, or financial telemetry adheres strictly to Rwanda's national data privacy framework.
3. **Sectoral Line Ministry Alignment:**
   - *Requirement:* Prior technical clearance from the responsible sector regulator:
     - **HealthTech:** Ministry of Health (MoH) Digital Health Working Group & Rwanda FDA.
     - **EdTech:** Rwanda Basic Education Board (REB) & MINEDUC.
     - **FinTech:** National Bank of Rwanda (BNR) Regulatory Sandbox & RSwitch.
     - **Telecom & IoT:** Rwanda Utilities Regulatory Authority (RURA).
   - *Rationale:* Prevents innovators from bypassing regulatory agencies and ensures MINICT acts as an enabler rather than an ad-hoc vetting body.
4. **Entity Registration & Product Maturity:**
   - *Requirement:* Valid RDB registration (TIN number) and a working prototype/MVP.
   - *Rationale:* Formal government MoUs cannot be entered into with unregistered individuals or raw ideas without proof of technical feasibility. Early-stage ideas are redirected to incubation hubs (kLab, Norrsken Kigali, 250STARTUPS).

---

## 4. How to Run the Prototype Locally

The prototype is designed with zero external Python library dependencies, utilizing Python's built-in `http.server` and `sqlite3` engines.

### Method 1: Double-Click Launcher (Windows)
1. Navigate to:  
   `C:\Users\pc\Desktop\Desktop_files\Victor Laptop\PROJECTS_ASSIGNED\FY_26_27\assignments\PS\SOPs\`
2. Double-click **`run_portal.bat`**.
3. A command console will launch the server and automatically open your default browser to:  
   `http://localhost:8080`

### Method 2: Command Line
```powershell
cd "C:\Users\pc\Desktop\Desktop_files\Victor Laptop\PROJECTS_ASSIGNED\FY_26_27\assignments\PS\SOPs"
py serve.py
```

---

## 5. DevOps & Integration Guide for MINICT IT Team

### A. Embedding into `https://www.minict.gov.rw/`
The portal is responsive and self-contained. The MINICT webmaster can integrate it using any of the following three patterns:

#### 1. Embedded iFrame / Dedicated Subpage
Add a new menu item under **Services > Innovator Support & MoU Portal** on `minict.gov.rw`:
```html
<iframe 
  src="https://support-portal.minict.gov.rw" 
  width="100%" 
  height="900px" 
  frameborder="0" 
  style="border: none; border-radius: 8px;">
</iframe>
```

#### 2. Reverse Proxy Subpath (Nginx Configuration)
If deploying alongside the primary MINICT portal on GovCloud:
```nginx
location /portal/ {
    proxy_pass http://127.0.0.1:8080/;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}
```

#### 3. Containerized Microservice (Docker)
Create a `Dockerfile` in the root directory:
```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY . /app
EXPOSE 8080
CMD ["python", "serve.py"]
```
Deploy to Rwanda GovCloud (AOS Kubernetes / Docker Engine):
```bash
docker build -t minict-intake-portal:v1 .
docker run -d -p 8080:8080 --name minict_portal minict-intake-portal:v1
```

---

## 6. Project Directory Structure

```
SOPs/
|-- run_portal.bat                 # One-click Windows startup script
|-- serve.py                       # Python HTTP server & REST API (SQLite CRUD)
|-- index.html                     # Main portal UI (Applicant + Leadership views)
|-- styles.css                     # Official Rwanda Gov design system
|-- app.js                         # Diagnostic scoring engine & Chart.js logic
|-- README.md                      # Executive guide & DevOps blueprint
|-- SOP_MINICT_INNOVATOR_INTAKE.md # Standard Operating Procedures for PS & Staff
`-- data/
    `-- applications.db            # SQLite database with schema & seeded records
```

---

## 7. Policy Impact for the Permanent Secretary

By implementing this portal, the Permanent Secretary achieves four immediate policy outcomes:
1. **100% Tracking & Transparency:** Eliminates "lost" applications and ensures all support requests receive an audit reference number.
2. **80% Reduction in Administrative Friction:** Eliminates unvetted meetings; technical officers only engage applicants who have met baseline IP, regulatory, and technical requirements.
3. **Data-Driven Ecosystem Interventions:** Real-time visibility into what startups lack (e.g. If 70% lack IP, MINICT organizes an RDB IP masterclass).
4. **Seamless Inter-Ministerial Governance:** Formally routes sector-specific innovations to MoH, MINEDUC, and BNR before committing MINICT resources.
