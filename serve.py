#!/usr/bin/env python3
"""
MINICT Smart Intake, Directed Concept and Automated Advisory Portal
Server Backend (serve.py)
Developed for: Ministry of ICT and Innovation (MINICT), Republic of Rwanda
Permanent Secretary Technical Assignment
"""

import os
import sys
import json
import sqlite3
import webbrowser
import threading
import urllib.parse
from http.server import HTTPServer, SimpleHTTPRequestHandler
from datetime import datetime

PORT = int(os.environ.get("PORT", 8080))
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'data', 'applications.db')

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            reference_no TEXT UNIQUE,
            created_at TEXT,
            applicant_name TEXT,
            organization_name TEXT,
            entity_type TEXT,
            email TEXT,
            phone TEXT,
            district TEXT,
            support_type TEXT,
            project_title TEXT,
            sector TEXT,
            target_beneficiary TEXT,
            problem_statement TEXT,
            proposed_solution TEXT,
            tech_stack TEXT,
            project_stage TEXT,
            has_ip_patent TEXT,
            ip_details TEXT,
            has_data_protection TEXT,
            dp_details TEXT,
            has_line_ministry_clearance TEXT,
            line_ministry_name TEXT,
            has_business_registration TEXT,
            tin_number TEXT,
            readiness_score INTEGER,
            critical_gaps TEXT,
            advisory_recommendations TEXT,
            line_ministry_routing TEXT,
            status TEXT,
            assigned_officer TEXT,
            technical_notes TEXT
        )
    """)
    conn.commit()

    # Seed realistic Rwandan tech ecosystem applications if empty
    cursor.execute("SELECT COUNT(*) FROM applications")
    if cursor.fetchone()[0] == 0:
        sample_apps = [
            (
                "MINICT-2026-001", "2026-09-08 10:14:00", "Jean de Dieu Habimana", "AfyaLink Telehealth Ltd",
                "Registered Tech Startup", "j.habimana@afyalink.rw", "+250 788 123 456", "Gasabo (Kigali)",
                "Memorandum of Understanding (MoU)", "AI Triage and Tele-consultation for Rural Health Posts",
                "HealthTech", "Rural health center nurses and district hospital doctors",
                "Delayed clinical referral in rural clinics due to lack of specialist doctors.",
                "WhatsApp-integrated and mobile AI triage app running on local language NLP models.",
                "Python, FastAPI, Meta Llama 3 Fine-tune, Flutter, PostgreSQL", "Prototype/MVP",
                "No", "Has not filed for copyright or patent with RDB IP division.",
                "In Progress", "Drafted data protection policy; not yet certified by NCSA DPPO.",
                "No", "Ministry of Health (MoH) / Rwanda Biomedical Centre (RBC)",
                "Yes", "109283746", 55,
                json.dumps(["Missing RDB IP protection", "Missing NCSA Data Protection registration under Law No 058/2021", "Must obtain MoH / Rwanda FDA clinical protocol clearance before MINICT MoU"]),
                json.dumps(["Apply for software copyright with RDB IP Office.", "Register data controller status with NCSA DPPO.", "Engage MoH Digital Health Sandbox before approaching MINICT for nationwide MoU."]),
                "Ministry of Health (MoH) & Rwanda Biomedical Centre (RBC)",
                "Referred to Line Ministry", "V. Muvunyi", "Advised to route to MoH e-Health working group before MINICT formal MoU."
            ),
            (
                "MINICT-2026-002", "2026-09-11 14:30:00", "Aline Uwamahoro", "Somakwacu EdTech",
                "Registered Tech Startup", "aline@somakwacu.rw", "+250 785 654 321", "Kicukiro (Kigali)",
                "Letter of Endorsement / Support", "Interactive Kinyarwanda STEM Content for Basic Education",
                "EdTech", "Primary and secondary school pupils and teachers in Rwanda",
                "High student-to-textbook ratios and lack of interactive digital science curricula in Kinyarwanda.",
                "Offline-first tablet app with gamified interactive simulations mapped to REB curriculum.",
                "React Native, SQLite, Node.js, WebAssembly simulations", "Pilot Testing",
                "Yes", "Registered copyright with RDB IP division in March 2026.",
                "Yes", "Registered as data controller with NCSA Data Protection Office.",
                "Yes", "Rwanda Basic Education Board (REB)",
                "Yes", "104829104", 85,
                json.dumps(["Formal curriculum alignment sign-off from REB pending validation session."]),
                json.dumps(["Submit pilot evaluation metrics to MINICT and REB joint innovation taskforce.", "Eligible for MINICT Endorsement Letter for global grant competition."]),
                "Rwanda Basic Education Board (REB) & MINEDUC",
                "Ready for Technical Review", "V. Muvunyi", "Strong concept with active REB engagement. High candidate for grant endorsement."
            ),
            (
                "MINICT-2026-003", "2026-09-14 09:22:00", "Patrick Mugisha", "AgriSmart Sensors Rwanda",
                "Individual Innovator", "patrick.mugisha@gmail.com", "+250 783 999 111", "Musanze (Northern)",
                "Memorandum of Understanding (MoU)", "Low-Cost IoT Soil Moisture and Nutrient Sensors for Cooperatives",
                "AgriTech", "Smallholder potato and maize farmer cooperatives",
                "Over-fertilization and inefficient irrigation causing degraded yields across volcanic soils.",
                "Solar-powered LoRaWAN soil telemetry nodes connecting to an automated advisory dashboard.",
                "ESP32, LoRaWAN, Python backend, Grafana, SMS Gateway", "Prototype/MVP",
                "No", "Has built custom hardware prototype; no utility model or patent filed.",
                "Not Applicable", "Does not collect personal identifiable data; only soil telemetry.",
                "No", "Ministry of Agriculture and Animal Resources (MINAGRI)",
                "No", "Not registered yet (operating as university spin-off project)", 45,
                json.dumps(["Unregistered entity (Needs RDB business registration)", "Unprotected hardware design (Needs RDB Utility Model/Patent)", "Needs MINAGRI / RAB cooperative alignment"]),
                json.dumps(["Register business entity with RDB.", "Consult RDB IP office on utility model protection for hardware nodes.", "Pilot with RAB (Rwanda Agriculture Board) research station before MINICT MoU."]),
                "MINAGRI & Rwanda Agriculture and Animal Resources Development Board (RAB)",
                "Advised - Pending Prerequisites", "Unassigned", "Sent automated advisory to register with RDB and apply for RDB Patent/Utility Model."
            ),
            (
                "MINICT-2026-004", "2026-09-16 11:45:00", "Claudine Mukamana", "Ishema Micro-Credit Platform",
                "Registered Tech Startup", "c.mukamana@ishema.rw", "+250 788 777 888", "Nyarugenge (Kigali)",
                "Sandbox Testing / Regulatory Navigation", "AI Credit Scoring for Informal Market Vendors (Chamas)",
                "FinTech", "Informal market traders, youth, and women cooperatives without formal collateral",
                "Exclusion of informal traders from formal bank financing due to lack of traditional credit history.",
                "Alternative credit scoring algorithm using mobile money transaction velocity and utility payment consistency.",
                "Python, Scikit-learn, AWS Rwanda local zone, eKash API, USSD & Android", "Prototype/MVP",
                "Yes", "Software copyright filed at RDB.",
                "In Progress", "NCSA compliance audit underway; preliminary registration approved.",
                "In Progress", "National Bank of Rwanda (BNR) Regulatory Sandbox",
                "Yes", "103948215", 75,
                json.dumps(["Pending formal admission into BNR Fintech Regulatory Sandbox."]),
                json.dumps(["Continue BNR Sandbox application.", "MINICT can facilitate technical review and eKash switch testing with RSwitch."]),
                "National Bank of Rwanda (BNR) & RSwitch",
                "Ready for Technical Review", "V. Muvunyi", "Very relevant for financial inclusion and eKash adoption. Recommend technical meeting."
            ),
            (
                "MINICT-2026-005", "2026-09-18 16:10:00", "Eric Ndahiro", "SmartCitizen Public Service Bot",
                "Individual Innovator", "eric.ndahiro@gmail.com", "+250 782 334 455", "Huye (Southern)",
                "Memorandum of Understanding (MoU)", "Voice-Enabled Kinyarwanda Assistant for Local Government Services",
                "AI & Language Tech", "Citizens seeking administrative forms, Irembo guidance, and sector office appointments",
                "Citizens with limited digital literacy struggle to navigate multi-step online public service portals.",
                "Speech-to-text and NLP voice assistant capable of handling conversational Kinyarwanda over phone calls.",
                "Whisper fine-tune, Gemini API, Asterisk PBX, Python, FastSpeech2", "Concept/Idea",
                "No", "No IP protection filed.",
                "No", "Has not addressed citizen audio privacy and consent protocols.",
                "No", "RISA (Rwanda Information Society Authority) & MINALOC",
                "No", "Individual student project", 35,
                json.dumps(["Idea stage only (MINICT requires functioning MVP for MoU)", "Missing IP protection with RDB", "Citizen biometric/voice privacy risk (NCSA clearance required)", "Needs alignment with RISA/Irembo"]),
                json.dumps(["Build interactive prototype and join a university incubation hub (e.g. UR Innovation Pod or kLab).", "Address voice data privacy with NCSA guidelines.", "Engage RISA software engineering division for Irembo integration specs."]),
                "Rwanda Information Society Authority (RISA) & MINALOC",
                "Advised - Pending Prerequisites", "Unassigned", "Referred to local incubator (kLab/UR Hub). Early stage idea."
            )
        ]
        cursor.executemany("""
            INSERT INTO applications (
                reference_no, created_at, applicant_name, organization_name,
                entity_type, email, phone, district, support_type,
                project_title, sector, target_beneficiary, problem_statement,
                proposed_solution, tech_stack, project_stage,
                has_ip_patent, ip_details, has_data_protection, dp_details,
                has_line_ministry_clearance, line_ministry_name,
                has_business_registration, tin_number, readiness_score,
                critical_gaps, advisory_recommendations, line_ministry_routing,
                status, assigned_officer, technical_notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, sample_apps)
        conn.commit()
    conn.close()

class MinictPortalHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=BASE_DIR, **kwargs)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == '/api/applications':
            self.handle_get_applications()
        elif parsed.path == '/api/analytics':
            self.handle_get_analytics()
        elif parsed.path == '/api/export':
            self.handle_export_csv()
        else:
            super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == '/api/applications':
            self.handle_create_application()
        elif parsed.path == '/api/applications/update':
            self.handle_update_application()
        else:
            self.send_error(404, 'Endpoint Not Found')

    def handle_get_applications(self):
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM applications ORDER BY id DESC")
        rows = cursor.fetchall()
        data = [dict(row) for row in rows]
        for item in data:
            try:
                item['critical_gaps'] = json.loads(item['critical_gaps']) if item['critical_gaps'] else []
                item['advisory_recommendations'] = json.loads(item['advisory_recommendations']) if item['advisory_recommendations'] else []
            except:
                pass
        conn.close()

        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

    def handle_get_analytics(self):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM applications")
        total = cursor.fetchone()[0]

        cursor.execute("SELECT sector, COUNT(*) FROM applications GROUP BY sector")
        sectors = dict(cursor.fetchall())

        cursor.execute("SELECT status, COUNT(*) FROM applications GROUP BY status")
        statuses = dict(cursor.fetchall())

        # Gaps analysis
        cursor.execute("SELECT COUNT(*) FROM applications WHERE has_ip_patent = 'No'")
        missing_ip = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM applications WHERE has_data_protection = 'No'")
        missing_dp = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM applications WHERE has_line_ministry_clearance = 'No'")
        missing_lm = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM applications WHERE has_business_registration = 'No'")
        unregistered = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM applications WHERE project_stage = 'Concept/Idea'")
        idea_stage = cursor.fetchone()[0]

        # Readiness distribution
        cursor.execute("SELECT readiness_score FROM applications")
        scores = [r[0] for r in cursor.fetchall()]
        avg_score = round(sum(scores) / len(scores), 1) if scores else 0
        high_readiness = sum(1 for s in scores if s >= 70)
        medium_readiness = sum(1 for s in scores if 40 <= s < 70)
        low_readiness = sum(1 for s in scores if s < 40)

        conn.close()

        result = {
            'total_applications': total,
            'average_readiness_score': avg_score,
            'high_readiness_count': high_readiness,
            'medium_readiness_count': medium_readiness,
            'low_readiness_count': low_readiness,
            'sectors': sectors,
            'statuses': statuses,
            'gaps_percentage': {
                'missing_ip_patent': round((missing_ip / total * 100) if total else 0, 1),
                'missing_data_protection': round((missing_dp / total * 100) if total else 0, 1),
                'missing_line_ministry_clearance': round((missing_lm / total * 100) if total else 0, 1),
                'unregistered_business': round((unregistered / total * 100) if total else 0, 1),
                'idea_stage_only': round((idea_stage / total * 100) if total else 0, 1)
            }
        }

        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(result).encode('utf-8'))

    def handle_create_application(self):
        content_len = int(self.headers.get('Content-Length', 0))
        post_body = self.rfile.read(content_len).decode('utf-8')
        data = json.loads(post_body)

        # Calculate Diagnostic Score and Gaps
        score = 20  # Baseline
        gaps = []
        advisories = []
        routing = "MINICT Technical Advisory Unit"

        # IP Assessment
        if data.get('has_ip_patent') == 'Yes':
            score += 20
        else:
            gaps.append("Missing Intellectual Property / Patent Registration with RDB IP Office")
            advisories.append("File for software copyright, trademark, or patent at RDB (org.rdb.rw) before signing formal MoUs to prevent IP infringement or ownership disputes.")

        # Data Protection
        if data.get('has_data_protection') == 'Yes':
            score += 20
        elif data.get('has_data_protection') == 'In Progress':
            score += 10
            advisories.append("Expedite your Data Controller registration certificate from the NCSA Data Protection & Privacy Office (dppo@ncsa.gov.rw).")
        elif data.get('has_data_protection') == 'No':
            gaps.append("Non-compliant with Data Protection & Privacy Law N° 058/2021")
            advisories.append("Under Rwandan law, systems handling citizen personal/health data must register with NCSA before production rollout. Visit https://dppo.ncsa.gov.rw.")

        # Sectoral Alignment and Line Ministry
        sector = data.get('sector', '')
        if sector == 'HealthTech':
            routing = "Ministry of Health (MoH) & Rwanda Biomedical Centre (RBC)"
            if data.get('has_line_ministry_clearance') != 'Yes':
                gaps.append("Lacks prior technical clearance from Ministry of Health (MoH) / Rwanda FDA")
                advisories.append("Digital health solutions require validation by the MoH Digital Health Technical Working Group and clinical approval before MINICT can execute an MoU.")
            else:
                score += 20
        elif sector == 'EdTech':
            routing = "Rwanda Basic Education Board (REB) & MINEDUC"
            if data.get('has_line_ministry_clearance') != 'Yes':
                gaps.append("Lacks curriculum alignment approval from REB / MINEDUC")
                advisories.append("EdTech platforms targeted at schools must undergo pedagogical vetting by REB before MINICT can endorse for institutional rollout.")
            else:
                score += 20
        elif sector == 'FinTech':
            routing = "National Bank of Rwanda (BNR) & RSwitch"
            if data.get('has_line_ministry_clearance') != 'Yes':
                gaps.append("Requires engagement with BNR Regulatory Sandbox or Payment Services License")
                advisories.append("Financial technologies moving funds or offering credit must enter the BNR Regulatory Sandbox before MINICT technical integration.")
            else:
                score += 20
        elif sector == 'AgriTech':
            routing = "Ministry of Agriculture and Animal Resources (MINAGRI) & RAB"
            if data.get('has_line_ministry_clearance') == 'Yes':
                score += 20
        else:
            if data.get('has_line_ministry_clearance') == 'Yes':
                score += 20

        # Business Registration
        if data.get('has_business_registration') == 'Yes':
            score += 10
        else:
            gaps.append("Unregistered Entity (No RDB Business Registration / TIN)")
            advisories.append("MINICT cannot execute legally binding MoUs with unregistered individuals. Register your business or cooperative online via business.rdb.rw.")

        # Stage Check
        stage = data.get('project_stage', '')
        if stage in ['Pilot Testing', 'Live in Market']:
            score += 10
        elif stage == 'Concept/Idea' and data.get('support_type') == 'Memorandum of Understanding (MoU)':
            gaps.append("Stage Mismatch: Requesting formal MoU at Idea/Concept stage without MVP")
            advisories.append("MINICT MoUs are reserved for tested solutions. We recommend joining incubation programs at kLab, Norrsken Kigali, or 250STARTUPS to build a working MVP first.")

        score = min(100, max(15, score))

        # Determine Initial Status
        if score >= 75:
            initial_status = "Ready for Technical Review"
        elif "Lacks prior technical clearance" in str(gaps) or "Lacks curriculum alignment" in str(gaps):
            initial_status = "Referred to Line Ministry"
        else:
            initial_status = "Advised - Pending Prerequisites"

        # Reference Number
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM applications")
        seq = cursor.fetchone()[0] + 1
        ref_no = f"MINICT-2026-{seq:03d}"
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute("""
            INSERT INTO applications (
                reference_no, created_at, applicant_name, organization_name,
                entity_type, email, phone, district, support_type,
                project_title, sector, target_beneficiary, problem_statement,
                proposed_solution, tech_stack, project_stage,
                has_ip_patent, ip_details, has_data_protection, dp_details,
                has_line_ministry_clearance, line_ministry_name,
                has_business_registration, tin_number, readiness_score,
                critical_gaps, advisory_recommendations, line_ministry_routing,
                status, assigned_officer, technical_notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            ref_no, created_at, data.get('applicant_name'), data.get('organization_name'),
            data.get('entity_type'), data.get('email'), data.get('phone'), data.get('district'),
            data.get('support_type'), data.get('project_title'), data.get('sector'),
            data.get('target_beneficiary'), data.get('problem_statement'), data.get('proposed_solution'),
            data.get('tech_stack'), data.get('project_stage'), data.get('has_ip_patent'),
            data.get('ip_details'), data.get('has_data_protection'), data.get('dp_details'),
            data.get('has_line_ministry_clearance'), data.get('line_ministry_name'),
            data.get('has_business_registration'), data.get('tin_number'), score,
            json.dumps(gaps), json.dumps(advisories), routing,
            initial_status, 'Unassigned', ''
        ))
        conn.commit()
        new_id = cursor.lastrowid
        conn.close()

        response = {
            'success': True,
            'id': new_id,
            'reference_no': ref_no,
            'readiness_score': score,
            'critical_gaps': gaps,
            'advisory_recommendations': advisories,
            'line_ministry_routing': routing,
            'initial_status': initial_status
        }

        self.send_response(201)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode('utf-8'))

    def handle_update_application(self):
        content_len = int(self.headers.get('Content-Length', 0))
        post_body = self.rfile.read(content_len).decode('utf-8')
        data = json.loads(post_body)
        app_id = data.get('id')
        status = data.get('status')
        officer = data.get('assigned_officer')
        notes = data.get('technical_notes')

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE applications
            SET status = COALESCE(?, status),
                assigned_officer = COALESCE(?, assigned_officer),
                technical_notes = COALESCE(?, technical_notes)
            WHERE id = ?
        """, (status, officer, notes, app_id))
        conn.commit()
        conn.close()

        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps({'success': True}).encode('utf-8'))

    def handle_export_csv(self):
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM applications ORDER BY id DESC")
        rows = cursor.fetchall()
        conn.close()

        import csv
        import io
        output = io.StringIO()
        if rows:
            writer = csv.writer(output)
            writer.writerow(rows[0].keys())
            for r in rows:
                writer.writerow(list(r))

        csv_data = output.getvalue()
        self.send_response(200)
        self.send_header('Content-Type', 'text/csv')
        self.send_header('Content-Disposition', 'attachment; filename="minict_applications_export.csv"')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(csv_data.encode('utf-8'))

def open_browser():
    try:
        webbrowser.open(f'http://localhost:{PORT}')
    except Exception as e:
        print('Could not open browser automatically:', e)

if __name__ == '__main__':
    init_db()
    server = HTTPServer(('0.0.0.0', PORT), MinictPortalHandler)
    print(f'==============================================================')
    print(f' MINICT Smart Intake & Directed Advisory Portal Prototype')
    print(f' Ministry of ICT and Innovation - Republic of Rwanda')
    print(f' Server Running at: http://localhost:{PORT}')
    print(f' Press Ctrl+C to stop the server')
    print(f'==============================================================')
    threading.Timer(1.2, open_browser).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped gracefully.")
        server.server_close()
