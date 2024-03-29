from urllib.parse import quote as url_encode


class GetAllSkills:
    QUERY_PATH = "/skills/"  # no input required
    EXPECTED_RESULT = {
        "items": [
            {
                "name": "21 CFR Part 11 (ERES)",
                "category": "Regulation",
                "type": "Skill",
            },
            {"name": "21 CFR Part 58 (GLP)", "category": "Regulation", "type": "Skill"},
            {
                "name": "21 CFR Part 820 (QSR)",
                "category": "Regulation",
                "type": "Skill",
            },
            {"name": "ADaM/TLFs Programming", "category": "Service", "type": "Skill"},
            {
                "name": "ANSI/ISA-95 - Enterprise-Control Systems",
                "category": "Regulation",
                "type": "Skill",
            },
            {
                "name": "AWS Cloud",
                "category": "Infrastructure_Technologies",
                "type": "Skill",
            },
            {
                "name": "Adverse Event Monitoring",
                "category": "Service",
                "type": "Skill",
            },
            {
                "name": "Aliquot handling",
                "category": "R_And_D_Processes",
                "type": "Skill",
            },
            {"name": "Application Migration", "category": "Service", "type": "Skill"},
            {"name": "Arabic", "category": "Languages", "type": "Skill"},
            {"name": "Asp .NET", "category": "Programming_languages", "type": "Skill"},
            {"name": "Assembler", "category": "Programming_languages", "type": "Skill"},
            {
                "name": "Atlassian Confluence",
                "category": "Products_And_Applications",
                "type": "Skill",
            },
            {
                "name": "Atlassian JIRA",
                "category": "Products_And_Applications",
                "type": "Skill",
            },
            {"name": "Automation Testing", "category": "Service", "type": "Skill"},
            {
                "name": "Azure Cloud",
                "category": "Infrastructure_Technologies",
                "type": "Skill",
            },
            {
                "name": "Azure-DevOps",
                "category": "Products_And_Applications",
                "type": "Skill",
            },
            {
                "name": "BIOVIA Notebook (ELN)",
                "category": "Scientific_Products_And_Applications",
                "type": "Skill",
            },
            {
                "name": "BIOVIA Pipeline Pilot",
                "category": "Scientific_Products_And_Applications",
                "type": "Skill",
            },
            {
                "name": "BPMN - Business Process Modelling Notation",
                "category": "Methodology",
                "type": "Skill",
            },
            {
                "name": "Benchling ELN",
                "category": "Scientific_Products_And_Applications",
                "type": "Skill",
            },
            {"name": "BioInformatics", "category": "Service", "type": "Skill"},
            {"name": "Bioanalysis", "category": "R_And_D_Processes", "type": "Skill"},
            {
                "name": "Biovia CISPRO",
                "category": "Scientific_Products_And_Applications",
                "type": "Skill",
            },
            {
                "name": "Biovia ChemDraw",
                "category": "Scientific_Products_And_Applications",
                "type": "Skill",
            },
            {"name": "Bootstrap", "category": "Miscellaneous", "type": "Skill"},
            {"name": "Business Analysis", "category": "Methodology", "type": "Skill"},
            {
                "name": "Business Intelligence Reporting",
                "category": "Data_Management",
                "type": "Skill",
            },
            {
                "name": "Business Process Modelling",
                "category": "Methodology",
                "type": "Skill",
            },
            {"name": "C", "category": "Programming_languages", "type": "Skill"},
            {"name": "C#", "category": "Programming_languages", "type": "Skill"},
            {"name": "C++", "category": "Programming_languages", "type": "Skill"},
            {
                "name": "CDISC Study Data Tabulation Model",
                "category": "Data_Management",
                "type": "Skill",
            },
            {
                "name": "Certara WinNonlin",
                "category": "Scientific_Products_And_Applications",
                "type": "Skill",
            },
            {"name": "Change Management", "category": "Methodology", "type": "Skill"},
            {
                "name": "ChemAxon",
                "category": "Scientific_Products_And_Applications",
                "type": "Skill",
            },
            {
                "name": "Chemaxon Marvin",
                "category": "Scientific_Products_And_Applications",
                "type": "Skill",
            },
            {"name": "Cheminformatics", "category": "Service", "type": "Skill"},
            {"name": "Chinese", "category": "Languages", "type": "Skill"},
            {
                "name": "Chromatography Techniques",
                "category": "R_And_D_Processes",
                "type": "Skill",
            },
            {
                "name": "Chromeleon",
                "category": "Scientific_Products_And_Applications",
                "type": "Skill",
            },
            {
                "name": "Cloud Archecture,Migration & Integration",
                "category": "Service",
                "type": "Skill",
            },
            {
                "name": "Columbus",
                "category": "Scientific_Products_And_Applications",
                "type": "Skill",
            },
            {
                "name": "Compound Management",
                "category": "R_And_D_Processes",
                "type": "Skill",
            },
            {
                "name": "Computational Design & Modelling",
                "category": "Service",
                "type": "Skill",
            },
            {
                "name": "Computer Systems Validation (CSV)",
                "category": "Methodology",
                "type": "Skill",
            },
            {
                "name": "Configuration Management",
                "category": "Infrastructure_Technologies",
                "type": "Skill",
            },
            {
                "name": "Core LIMS",
                "category": "Scientific_Products_And_Applications",
                "type": "Skill",
            },
            {
                "name": "Customer Relationship Management",
                "category": "Methodology",
                "type": "Skill",
            },
            {
                "name": "D360",
                "category": "Scientific_Products_And_Applications",
                "type": "Skill",
            },
            {"name": "DB2", "category": "Infrastructure_Technologies", "type": "Skill"},
            {"name": "DMPK assays", "category": "R_And_D_Processes", "type": "Skill"},
            {
                "name": "Daisy",
                "category": "Scientific_Products_And_Applications",
                "type": "Skill",
            },
            {"name": "Danish", "category": "Languages", "type": "Skill"},
            {
                "name": "Data Analysis/Modelling",
                "category": "Data_Management",
                "type": "Skill",
            },
            {
                "name": "Data Extraction & Wrangling",
                "category": "Data_Management",
                "type": "Skill",
            },
            {"name": "Data Governance", "category": "Data_Management", "type": "Skill"},
            {
                "name": "Data Integration",
                "category": "Data_Management",
                "type": "Skill",
            },
            {"name": "Data Migration", "category": "Data_Management", "type": "Skill"},
            {"name": "Data Pipelines", "category": "Data_Management", "type": "Skill"},
            {
                "name": "Data Visualisation",
                "category": "Data_Management",
                "type": "Skill",
            },
            {
                "name": "Data Warehousing",
                "category": "Infrastructure_Technologies",
                "type": "Skill",
            },
            {"name": "DataOps", "category": "Service", "type": "Skill"},
            {"name": "Design Patterns", "category": "Data_Management", "type": "Skill"},
            {"name": "DevOps & TechOps", "category": "Service", "type": "Skill"},
            {"name": "Digital Coaching", "category": "Service", "type": "Skill"},
            {
                "name": "Disciplined Agile (DA)",
                "category": "Methodology",
                "type": "Skill",
            },
            {"name": "Django", "category": "Miscellaneous", "type": "Skill"},
            {
                "name": "Docollab LIMs/ELN",
                "category": "Scientific_Products_And_Applications",
                "type": "Skill",
            },
            {
                "name": "Dotmatics ELN",
                "category": "Scientific_Products_And_Applications",
                "type": "Skill",
            },
            {"name": "Drug Toxicity", "category": "R_And_D_Processes", "type": "Skill"},
            {"name": "Dutch", "category": "Languages", "type": "Skill"},
            {
                "name": "ELOG",
                "category": "Scientific_Products_And_Applications",
                "type": "Skill",
            },
            {
                "name": "ETL & ELT Processing",
                "category": "Data_Management",
                "type": "Skill",
            },
            {"name": "EU Annex 11", "category": "Regulation", "type": "Skill"},
            {
                "name": "Edison",
                "category": "Scientific_Products_And_Applications",
                "type": "Skill",
            },
            {"name": "English", "category": "Languages", "type": "Skill"},
            {
                "name": "Enterprise Architecture",
                "category": "Methodology",
                "type": "Skill",
            },
            {"name": "Epigenetics", "category": "R_And_D_Processes", "type": "Skill"},
            {
                "name": "Exemplar LIMS",
                "category": "Scientific_Products_And_Applications",
                "type": "Skill",
            },
            {"name": "F#", "category": "Programming_languages", "type": "Skill"},
            {
                "name": "FAIR Data Principles",
                "category": "Data_Management",
                "type": "Skill",
            },
            {
                "name": "Findings ELN",
                "category": "Scientific_Products_And_Applications",
                "type": "Skill",
            },
            {"name": "Formulation", "category": "R_And_D_Processes", "type": "Skill"},
            {"name": "Fortran", "category": "Programming_languages", "type": "Skill"},
            {"name": "French", "category": "Languages", "type": "Skill"},
            {"name": "GAMP", "category": "Regulation", "type": "Skill"},
            {
                "name": "GCP Cloud",
                "category": "Infrastructure_Technologies",
                "type": "Skill",
            },
            {"name": "GDPR", "category": "Regulation", "type": "Skill"},
            {
                "name": "Genedata Screener",
                "category": "Scientific_Products_And_Applications",
                "type": "Skill",
            },
            {
                "name": "Genetic Engineering",
                "category": "R_And_D_Processes",
                "type": "Skill",
            },
            {"name": "Genotyping", "category": "R_And_D_Processes", "type": "Skill"},
            {"name": "German", "category": "Languages", "type": "Skill"},
            {
                "name": "GitHub",
                "category": "Infrastructure_Technologies",
                "type": "Skill",
            },
            {"name": "Go", "category": "Programming_languages", "type": "Skill"},
            {"name": "Graph Data Support", "category": "Service", "type": "Skill"},
            {
                "name": "GraphDB",
                "category": "Products_And_Applications",
                "type": "Skill",
            },
            {
                "name": "Graphpad",
                "category": "Scientific_Products_And_Applications",
                "type": "Skill",
            },
            {"name": "Groovy", "category": "Programming_languages", "type": "Skill"},
            {"name": "HIPAA", "category": "Regulation", "type": "Skill"},
            {
                "name": "HP ALM",
                "category": "Products_And_Applications",
                "type": "Skill",
            },
            {"name": "HTE, HTS & HCS", "category": "Service", "type": "Skill"},
            {"name": "HTML", "category": "Programming_languages", "type": "Skill"},
            {
                "name": "Hamilton",
                "category": "Scientific_Products_And_Applications",
                "type": "Skill",
            },
            {"name": "Hindi", "category": "Languages", "type": "Skill"},
            {
                "name": "IDBS ActivityBase",
                "category": "Scientific_Products_And_Applications",
                "type": "Skill",
            },
            {
                "name": "IDBS Inventory",
                "category": "Scientific_Products_And_Applications",
                "type": "Skill",
            },
            {
                "name": "IDBS Polar",
                "category": "Scientific_Products_And_Applications",
                "type": "Skill",
            },
            {
                "name": "IDBS Request",
                "category": "Scientific_Products_And_Applications",
                "type": "Skill",
            },
            {
                "name": "ISO 13485 - Medical Devices",
                "category": "Regulation",
                "type": "Skill",
            },
            {
                "name": "ISO 14001 - Environmental management",
                "category": "Regulation",
                "type": "Skill",
            },
            {
                "name": "ISO 27001 - Security Management",
                "category": "Regulation",
                "type": "Skill",
            },
            {
                "name": "ISO 9001 - Quality Management",
                "category": "Regulation",
                "type": "Skill",
            },
            {"name": "ITIL Methodology", "category": "Methodology", "type": "Skill"},
            {"name": "In vitro & In vivo", "category": "Service", "type": "Skill"},
            {"name": "Italian", "category": "Languages", "type": "Skill"},
            {"name": "JQuery", "category": "Miscellaneous", "type": "Skill"},
            {"name": "JSP", "category": "Programming_languages", "type": "Skill"},
            {"name": "Japanese", "category": "Languages", "type": "Skill"},
            {"name": "Jasper", "category": "Programming_languages", "type": "Skill"},
            {"name": "Java", "category": "Programming_languages", "type": "Skill"},
            {
                "name": "JavaScript",
                "category": "Programming_languages",
                "type": "Skill",
            },
            {"name": "Julia", "category": "Programming_languages", "type": "Skill"},
            {
                "name": "KNEAT validation",
                "category": "Scientific_Products_And_Applications",
                "type": "Skill",
            },
            {
                "name": "KNIME",
                "category": "Scientific_Products_And_Applications",
                "type": "Skill",
            },
            {"name": "Kanban Methodology", "category": "Methodology", "type": "Skill"},
            {
                "name": "Knowledge Graphs",
                "category": "Data_Management",
                "type": "Skill",
            },
            {
                "name": "L7 Informatics",
                "category": "Scientific_Products_And_Applications",
                "type": "Skill",
            },
            {
                "name": "Lab Instrument Validation",
                "category": "Methodology",
                "type": "Skill",
            },
            {
                "name": "LabGuru LIMS",
                "category": "Scientific_Products_And_Applications",
                "type": "Skill",
            },
            {
                "name": "LabVantage LIMS",
                "category": "Scientific_Products_And_Applications",
                "type": "Skill",
            },
            {
                "name": "Labware LIMS",
                "category": "Scientific_Products_And_Applications",
                "type": "Skill",
            },
            {
                "name": "Large Scale Scrum (LeSS)",
                "category": "Methodology",
                "type": "Skill",
            },
            {
                "name": "Large molecule registration",
                "category": "R_And_D_Processes",
                "type": "Skill",
            },
            {"name": "Lean Methodology", "category": "Methodology", "type": "Skill"},
            {
                "name": "Linux",
                "category": "Infrastructure_Technologies",
                "type": "Skill",
            },
            {"name": "ML Ops", "category": "Data_Management", "type": "Skill"},
            {"name": "Machine Learning & AI", "category": "Service", "type": "Skill"},
            {"name": "Managed Services", "category": "Service", "type": "Skill"},
            {
                "name": "Manufacturing Execution System (MES)",
                "category": "Service",
                "type": "Skill",
            },
            {"name": "Manufacturing QC", "category": "Service", "type": "Skill"},
            {
                "name": "Master Services Agreement Authoring",
                "category": "Methodology",
                "type": "Skill",
            },
            {
                "name": "Mbook ELN",
                "category": "Scientific_Products_And_Applications",
                "type": "Skill",
            },
            {"name": "Medical Writing", "category": "Service", "type": "Skill"},
            {
                "name": "Medidata RAVE - Data Management",
                "category": "Scientific_Products_And_Applications",
                "type": "Skill",
            },
            {
                "name": "Method Development",
                "category": "R_And_D_Processes",
                "type": "Skill",
            },
            {"name": "Method Validation", "category": "Service", "type": "Skill"},
            {"name": "Microbiome", "category": "R_And_D_Processes", "type": "Skill"},
            {"name": "Microservices", "category": "R_And_D_Processes", "type": "Skill"},
            {
                "name": "Microsoft SQL Server",
                "category": "Infrastructure_Technologies",
                "type": "Skill",
            },
            {
                "name": "MoSaIC",
                "category": "Scientific_Products_And_Applications",
                "type": "Skill",
            },
            {
                "name": "Molecular Biology",
                "category": "R_And_D_Processes",
                "type": "Skill",
            },
            {
                "name": "MySQL",
                "category": "Infrastructure_Technologies",
                "type": "Skill",
            },
            {
                "name": "Nagios",
                "category": "Products_And_Applications",
                "type": "Skill",
            },
            {
                "name": "Nautilus",
                "category": "Scientific_Products_And_Applications",
                "type": "Skill",
            },
            {
                "name": "Next Generation Sequencing (NGS)",
                "category": "R_And_D_Processes",
                "type": "Skill",
            },
            {"name": "Nexus", "category": "Methodology", "type": "Skill"},
            {
                "name": "Nugenesis",
                "category": "Scientific_Products_And_Applications",
                "type": "Skill",
            },
            {
                "name": "Ontology Development & Management",
                "category": "Data_Management",
                "type": "Skill",
            },
            {
                "name": "OpenAnalytics PHAEDRA",
                "category": "Scientific_Products_And_Applications",
                "type": "Skill",
            },
            {
                "name": "Oracle BI",
                "category": "Products_And_Applications",
                "type": "Skill",
            },
            {
                "name": "Oracle Database",
                "category": "Infrastructure_Technologies",
                "type": "Skill",
            },
            {"name": "PHP", "category": "Programming_languages", "type": "Skill"},
            {"name": "PLSQL", "category": "Programming_languages", "type": "Skill"},
            {"name": "PMI / PMP (PMBOK)", "category": "Methodology", "type": "Skill"},
            {"name": "PRINCE2", "category": "Methodology", "type": "Skill"},
            {"name": "PROCI - ADKAR", "category": "Methodology", "type": "Skill"},
            {
                "name": "Packaging & Shipping",
                "category": "R_And_D_Processes",
                "type": "Skill",
            },
            {
                "name": "Palantir Foundry",
                "category": "Scientific_Products_And_Applications",
                "type": "Skill",
            },
            {"name": "Perl", "category": "Programming_languages", "type": "Skill"},
            {
                "name": "PharmacoKinetics",
                "category": "R_And_D_Processes",
                "type": "Skill",
            },
            {"name": "Pharmacology & DMPK", "category": "Service", "type": "Skill"},
            {
                "name": "Pillar Science",
                "category": "Scientific_Products_And_Applications",
                "type": "Skill",
            },
            {"name": "Polish", "category": "Languages", "type": "Skill"},
            {"name": "Portuguese", "category": "Languages", "type": "Skill"},
            {
                "name": "PostgresSQL",
                "category": "Programming_languages",
                "type": "Skill",
            },
            {
                "name": "PowerBI",
                "category": "Products_And_Applications",
                "type": "Skill",
            },
            {
                "name": "PowerShell",
                "category": "Programming_languages",
                "type": "Skill",
            },
            {"name": "Process Automation", "category": "Service", "type": "Skill"},
            {
                "name": "Process Development",
                "category": "R_And_D_Processes",
                "type": "Skill",
            },
            {
                "name": "Product Lifecycle Management",
                "category": "Service",
                "type": "Skill",
            },
            {"name": "Proteomics", "category": "R_And_D_Processes", "type": "Skill"},
            {"name": "Protocol design", "category": "Service", "type": "Skill"},
            {"name": "Python", "category": "Programming_languages", "type": "Skill"},
            {"name": "QSAR", "category": "R_And_D_Processes", "type": "Skill"},
            {
                "name": "Qlik",
                "category": "Scientific_Products_And_Applications",
                "type": "Skill",
            },
            {"name": "Quality Reporting", "category": "Service", "type": "Skill"},
            {"name": "R Studio", "category": "Miscellaneous", "type": "Skill"},
            {
                "name": "RDKIT",
                "category": "Scientific_Products_And_Applications",
                "type": "Skill",
            },
            {"name": "REACT", "category": "Miscellaneous", "type": "Skill"},
            {"name": "REDUX", "category": "Miscellaneous", "type": "Skill"},
            {
                "name": "REST API's",
                "category": "Infrastructure_Technologies",
                "type": "Skill",
            },
            {
                "name": "Rational Unified Process (RUP)",
                "category": "Methodology",
                "type": "Skill",
            },
            {"name": "Regulatory Submission", "category": "Service", "type": "Skill"},
            {
                "name": "Regulatory Submission Packages - ADaM/TLFs",
                "category": "Service",
                "type": "Skill",
            },
            {
                "name": "Regulatory Submission Packages - SDTM",
                "category": "Service",
                "type": "Skill",
            },
            {"name": "Regulatory affairs", "category": "Service", "type": "Skill"},
            {
                "name": "Release Management",
                "category": "Infrastructure_Technologies",
                "type": "Skill",
            },
            {
                "name": "Remedy",
                "category": "Products_And_Applications",
                "type": "Skill",
            },
            {
                "name": "Robotic Process Automation & Workflow Orchastration",
                "category": "Service",
                "type": "Skill",
            },
            {
                "name": "Rshiny",
                "category": "Products_And_Applications",
                "type": "Skill",
            },
            {
                "name": "Rspace ELN",
                "category": "Scientific_Products_And_Applications",
                "type": "Skill",
            },
            {"name": "Russian", "category": "Languages", "type": "Skill"},
            {"name": "Rust", "category": "Programming_languages", "type": "Skill"},
            {
                "name": "SAS Business Intelligence",
                "category": "Products_And_Applications",
                "type": "Skill",
            },
            {"name": "SCADA", "category": "Data_Management", "type": "Skill"},
            {
                "name": "SEND - CDISC Non-Clinical",
                "category": "Regulation",
                "type": "Skill",
            },
            {"name": "SQL", "category": "Programming_languages", "type": "Skill"},
            {
                "name": "SSO & Identity Management",
                "category": "Infrastructure_Technologies",
                "type": "Skill",
            },
            {
                "name": "STARLIMS",
                "category": "Scientific_Products_And_Applications",
                "type": "Skill",
            },
            {
                "name": "Sample Management",
                "category": "R_And_D_Processes",
                "type": "Skill",
            },
            {
                "name": "Sapio LIMS",
                "category": "Scientific_Products_And_Applications",
                "type": "Skill",
            },
            {
                "name": "Scaled Agile Framework (Safe)",
                "category": "Methodology",
                "type": "Skill",
            },
            {"name": "Scaler", "category": "Programming_languages", "type": "Skill"},
            {"name": "Schema Design", "category": "Data_Management", "type": "Skill"},
            {
                "name": "SciNote ELN",
                "category": "Scientific_Products_And_Applications",
                "type": "Skill",
            },
            {
                "name": "Scilligence - ELN",
                "category": "Scientific_Products_And_Applications",
                "type": "Skill",
            },
            {"name": "Screening", "category": "R_And_D_Processes", "type": "Skill"},
            {"name": "Scrum Methodology", "category": "Methodology", "type": "Skill"},
            {"name": "Scrum@Scale (SaS)", "category": "Methodology", "type": "Skill"},
            {
                "name": "Semantic Models & Enrichment",
                "category": "Data_Management",
                "type": "Skill",
            },
            {"name": "Sequencing", "category": "R_And_D_Processes", "type": "Skill"},
            {
                "name": "Service Now",
                "category": "Products_And_Applications",
                "type": "Skill",
            },
            {
                "name": "Sharepoint",
                "category": "Products_And_Applications",
                "type": "Skill",
            },
            {
                "name": "Shell Scripting",
                "category": "Programming_languages",
                "type": "Skill",
            },
            {"name": "Slack", "category": "Products_And_Applications", "type": "Skill"},
            {
                "name": "Small molecule registration",
                "category": "R_And_D_Processes",
                "type": "Skill",
            },
            {
                "name": "Snowflake",
                "category": "Infrastructure_Technologies",
                "type": "Skill",
            },
            {
                "name": "Software Design & Architecture",
                "category": "Service",
                "type": "Skill",
            },
            {
                "name": "Software as a Medical Device (SaMD)",
                "category": "Service",
                "type": "Skill",
            },
            {"name": "Spanish", "category": "Languages", "type": "Skill"},
            {"name": "Spectroscopy", "category": "R_And_D_Processes", "type": "Skill"},
            {
                "name": "Spotfire",
                "category": "Scientific_Products_And_Applications",
                "type": "Skill",
            },
            {"name": "Stability", "category": "R_And_D_Processes", "type": "Skill"},
            {"name": "Stability Studies", "category": "Service", "type": "Skill"},
            {
                "name": "StarDrop",
                "category": "Scientific_Products_And_Applications",
                "type": "Skill",
            },
            {
                "name": "Statement of Work Authoring",
                "category": "Methodology",
                "type": "Skill",
            },
            {
                "name": "Statistics - Randomization",
                "category": "Service",
                "type": "Skill",
            },
            {"name": "Statistics Review", "category": "Service", "type": "Skill"},
            {"name": "Strategic Consulting", "category": "Service", "type": "Skill"},
            {"name": "Swift", "category": "Programming_languages", "type": "Skill"},
            {"name": "TOGAF", "category": "Methodology", "type": "Skill"},
            {
                "name": "Tableau",
                "category": "Scientific_Products_And_Applications",
                "type": "Skill",
            },
            {"name": "Tamil", "category": "Languages", "type": "Skill"},
            {
                "name": "Taxonomy Development & Management",
                "category": "Data_Management",
                "type": "Skill",
            },
            {"name": "Template Development", "category": "Service", "type": "Skill"},
            {"name": "Test Script writing", "category": "Service", "type": "Skill"},
            {"name": "Testing and QC", "category": "Service", "type": "Skill"},
            {
                "name": "Titian",
                "category": "Scientific_Products_And_Applications",
                "type": "Skill",
            },
            {"name": "Training", "category": "Service", "type": "Skill"},
            {"name": "Translational Science", "category": "Service", "type": "Skill"},
            {
                "name": "Trello",
                "category": "Products_And_Applications",
                "type": "Skill",
            },
            {
                "name": "Unix",
                "category": "Infrastructure_Technologies",
                "type": "Skill",
            },
            {"name": "VB Script", "category": "Programming_languages", "type": "Skill"},
            {"name": "VBA", "category": "Programming_languages", "type": "Skill"},
            {
                "name": "Value-Flow-Quality (VFQ)",
                "category": "Methodology",
                "type": "Skill",
            },
            {
                "name": "Viedoc - EDC Design",
                "category": "Scientific_Products_And_Applications",
                "type": "Skill",
            },
            {"name": "XML", "category": "Programming_languages", "type": "Skill"},
            {
                "name": "Xbiom",
                "category": "Scientific_Products_And_Applications",
                "type": "Skill",
            },
            {
                "name": "Zoho Analytics",
                "category": "Products_And_Applications",
                "type": "Skill",
            },
            {
                "name": "ecLabNote ELN",
                "category": "Scientific_Products_And_Applications",
                "type": "Skill",
            },
        ]
    }


class GetSkillPerCategory:
    INPUT = "Data_Management"  # input: single skills category (existing), update EXPECTED_RESULT when this is changed!
    QUERY_PATH = f"/skills/?category={url_encode(INPUT)}"
    EXPECTED_RESULT = {
        "items": [
            {
                "name": "Business Intelligence Reporting",
                "category": "Data_Management",
                "type": "Skill",
            },
            {
                "name": "CDISC Study Data Tabulation Model",
                "category": "Data_Management",
                "type": "Skill",
            },
            {
                "name": "Data Analysis/Modelling",
                "category": "Data_Management",
                "type": "Skill",
            },
            {
                "name": "Data Extraction & Wrangling",
                "category": "Data_Management",
                "type": "Skill",
            },
            {"name": "Data Governance", "category": "Data_Management", "type": "Skill"},
            {
                "name": "Data Integration",
                "category": "Data_Management",
                "type": "Skill",
            },
            {"name": "Data Migration", "category": "Data_Management", "type": "Skill"},
            {"name": "Data Pipelines", "category": "Data_Management", "type": "Skill"},
            {
                "name": "Data Visualisation",
                "category": "Data_Management",
                "type": "Skill",
            },
            {"name": "Design Patterns", "category": "Data_Management", "type": "Skill"},
            {
                "name": "ETL & ELT Processing",
                "category": "Data_Management",
                "type": "Skill",
            },
            {
                "name": "FAIR Data Principles",
                "category": "Data_Management",
                "type": "Skill",
            },
            {
                "name": "Knowledge Graphs",
                "category": "Data_Management",
                "type": "Skill",
            },
            {"name": "ML Ops", "category": "Data_Management", "type": "Skill"},
            {
                "name": "Ontology Development & Management",
                "category": "Data_Management",
                "type": "Skill",
            },
            {"name": "SCADA", "category": "Data_Management", "type": "Skill"},
            {"name": "Schema Design", "category": "Data_Management", "type": "Skill"},
            {
                "name": "Semantic Models & Enrichment",
                "category": "Data_Management",
                "type": "Skill",
            },
            {
                "name": "Taxonomy Development & Management",
                "category": "Data_Management",
                "type": "Skill",
            },
        ]
    }


class GetSingleSkill:
    INPUT = "CDISC Study Data Tabulation Model"  # input: single skill name (existing),
    # update EXPECTED_RESULT when this is changed!
    QUERY_PATH = f"/skills/{url_encode(INPUT)}"
    EXPECTED_RESULT = {
        "name": "CDISC Study Data Tabulation Model",
        "category": "Data_Management",
        "type": "Skill",
    }


class GetSingleSkillNotFound:
    INPUT = "TEST SKILL"  # input: single skill name (not existing)
    QUERY_PATH = f"/skills/{url_encode(INPUT)}"
    EXPECTED_DETAIL = "Skill not found"


class CreatDuplicateSkill:
    INPUT_SKILL = "CDISC Study Data Tabulation Model"
    INPUT_CATEGORY = "Data_Management"  # inputs: single skill name and corresponding skill category (existing)
    INPUT = {"name": INPUT_SKILL, "category": INPUT_CATEGORY}
    QUERY_PATH = "/skills/"
    EXPECTED_DETAIL = "'CDISC Study Data Tabulation Model' skill already exists"


class DeleteSkillNotFound:
    INPUT = "TEST SKILL"
    QUERY_PATH = f"/skills/{url_encode(INPUT)}"
    EXPECTED_DETAIL = "Skill not found"


class CreateSkill:
    INPUT_SKILL = "TEST SKILL"
    INPUT_CATEGORY = "Data_Management"  # inputs: single skill name and corresponding skill category (existing)
    INPUT = {"name": INPUT_SKILL, "category": INPUT_CATEGORY}
    QUERY_PATH = "/skills/"
    EXPECTED_RESULT = {"name": INPUT_SKILL, "category": INPUT_CATEGORY, "type": "Skill"}

    QUERY_PATH_DOUBLE_CHECK = f"/skills/{url_encode(INPUT_SKILL)}"
    EXPECTED_DOUBLE_CHECK_RESULT = {
        "name": INPUT_SKILL,
        "category": INPUT_CATEGORY,
        "type": "Skill",
    }


class DeleteSkill:
    INPUT = "CDISC Study Data Tabulation Model"
    QUERY_PATH = f"/skills/{url_encode(INPUT)}"
    EXPECTED_MESSAGE = f"Deleted skill {INPUT}"
    EXPECTED_DOUBLE_CHECK_DETAIL = "Skill not found"
