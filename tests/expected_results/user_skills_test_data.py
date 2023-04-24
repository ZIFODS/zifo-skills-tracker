from urllib.parse import quote as url_encode


class UserSkillsGetAll:
    QUERY_PATH = "/user/skills/"  # no input required
    EXPECTED_OUTPUT = {
        "items": [
            {"name": "21 CFR Part 58 (GLP)", "category": "Regulation", "type": "Skill"},
            {
                "name": "Azure-DevOps",
                "category": "Products_And_Applications",
                "type": "Skill",
            },
            {
                "name": "BIOVIA Pipeline Pilot",
                "category": "Scientific_Products_And_Applications",
                "type": "Skill",
            },
            {
                "name": "Business Process Modelling",
                "category": "Methodology",
                "type": "Skill",
            },
            {"name": "C++", "category": "Programming_languages", "type": "Skill"},
            {
                "name": "Cloud Archecture,Migration & Integration",
                "category": "Service",
                "type": "Skill",
            },
            {
                "name": "Computational Design & Modelling",
                "category": "Service",
                "type": "Skill",
            },
            {
                "name": "GraphDB",
                "category": "Products_And_Applications",
                "type": "Skill",
            },
            {
                "name": "HP ALM",
                "category": "Products_And_Applications",
                "type": "Skill",
            },
            {
                "name": "Hamilton",
                "category": "Scientific_Products_And_Applications",
                "type": "Skill",
            },
            {
                "name": "Mbook ELN",
                "category": "Scientific_Products_And_Applications",
                "type": "Skill",
            },
            {"name": "Nexus", "category": "Methodology", "type": "Skill"},
            {
                "name": "Remedy",
                "category": "Products_And_Applications",
                "type": "Skill",
            },
            {
                "name": "SciNote ELN",
                "category": "Scientific_Products_And_Applications",
                "type": "Skill",
            },
            {"name": "Slack", "category": "Products_And_Applications", "type": "Skill"},
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
        ]
    }


class UserSkillsGetCategory:
    INPUT = "Programming_languages"  # input: skill category (existing) - update EXPECTED_OUTPUT if this is changed
    QUERY_PATH = f"/user/skills/?category={url_encode(INPUT)}"
    EXPECTED_OUTPUT = {
        "items": [{"name": "C++", "category": "Programming_languages", "type": "Skill"}]
    }


class UserSkillsGetLearnedSkill:
    INPUT = "C++"  # input: skill name (existing) - update EXPECTED_OUTPUT if this is changed
    QUERY_PATH = f"/user/skills/{url_encode(INPUT)}"
    EXPECTED_OUTPUT = {
        "name": "C++",
        "category": "Programming_languages",
        "type": "Skill",
    }


class UserSkillsGetUnlearnedSkill:
    INPUT = "CDISC Study Data Tabulation Model"
    # input: skill name (existing but not linked to test user) - update EXPECTED_OUTPUT if this is changed
    QUERY_PATH = f"/user/skills/{url_encode(INPUT)}"
    EXPECTED_DETAIL = "Skill not found for user"


class UserSkillsTrainTrainedSkill:
    INPUT = [{"name": "C++", "category": "Programming_languages"}]
    # input: POST request body - list with one skill dict linked to test user
    QUERY_PATH = "/user/skills/"  # POST request - no parameters in URL
    EXPECTED_DETAIL = (
        f"The following skills are already linked to the user: {INPUT[0]['name']}"
    )


class UserSkillsForgetUntrainedSkill:
    INPUT = "CDISC Study Data Tabulation Model"  # input: skill name (existing but not linked to test user)
    QUERY_PATH = f"/user/skills/?skill_names={url_encode(INPUT)}"
    EXPECTED_DETAIL = f"The following skills are not linked to the user: {INPUT}"


class UserSkillsTrainUnknownSkill:
    INPUT = [{"name": "knitting", "category": "Programming_languages"}]
    # input: POST request body - list with one skill dict linked to test user
    QUERY_PATH = "/user/skills/"  # POST request - no parameters in URL
    EXPECTED_DETAIL = "Skill not found and could not be linked to user"


class UserSkillsTrainSkills:
    QUERY_PATH = "/user/skills/"  # POST request - no parameters in URL
    INPUT = [
        {"name": "CDISC Study Data Tabulation Model", "category": "Data_Management"},
        {"name": "Dutch", "category": "Languages"},
    ]
    # input: POST request body, list with multiple skill dicts not linked to test user
    EXPECTED_OUTPUT = {
        "items": [
            {
                "name": "CDISC Study Data Tabulation Model",
                "category": "Data_Management",
                "type": "Skill",
            },
            {"name": "Dutch", "category": "Languages", "type": "Skill"},
        ]
    }


class UserSkillsForgetSkills:
    INPUT1 = "C++"
    INPUT2 = "Remedy"  # inputs: 2 skill names in alphabetical order, existing and linked to test user
    QUERY_PATH = f"/user/skills/?skill_names={url_encode(INPUT1)}&skill_names={url_encode(INPUT2)}"
    EXPECTED_MESSAGE = (
        f"Removed {INPUT1}, {INPUT2} " f"for user anthony_hopkins@gmail.com"
    )
