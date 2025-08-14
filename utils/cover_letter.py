from datetime import date

TEMPLATE = """{today}

Hiring Manager
{company}
{company_location}

Subject: Application for {role}

Dear Hiring Manager,

I’m excited to apply for the {role} role at {company}. With {years_exp}+ years across {domains}, I’ve delivered impact such as:
{bullets}

In this role, I would:
- Apply my strengths in {strengths} to drive outcomes
- Quickly close gaps in {gaps_to_close}
- Collaborate closely with {teams} to execute roadmap

Attached are my resume and portfolio. I’d welcome the chance to discuss how I can help {company_short} reach its goals.

Sincerely,
{candidate}
{contact}
"""

def render_cover_letter_fallback(**kwargs) -> str:
    data = {
        "today": date.today().strftime("%B %d, %Y"),
        "company": "Company",
        "company_location": "City, Country",
        "role": "Role Title",
        "years_exp": "X",
        "domains": "software/data/products",
        "bullets": "- Impact 1\n- Impact 2\n- Impact 3",
        "strengths": "Python, data pipelines, stakeholder comms",
        "gaps_to_close": "domain specifics identified in the JD",
        "teams": "Product, Design, and Engineering",
        "company_short": "the team",
        "candidate": "Your Name",
        "contact": "email • phone • LinkedIn",
        **kwargs,
    }
    return TEMPLATE.format(**data)
