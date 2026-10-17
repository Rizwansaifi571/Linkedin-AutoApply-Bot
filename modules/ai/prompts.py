'''
Author:     Sai Vignesh Golla
LinkedIn:   https://www.linkedin.com/in/saivigneshgolla/

Copyright (c) 2024-2026 Sai Vignesh Golla

License:    MIT License
            https://opensource.org/license/mit

GitHub:     https://github.com/GodsScion/Auto_job_applier_linkedIn

Prompt templates used by the AI layer (modules/ai/connections.py).
'''


##> Extract skills
# Used with `extract_skills_prompt.format(job_description)`.
extract_skills_prompt = """
You are a job requirements extractor and classifier. Your task is to extract all skills mentioned in a job description and classify them into five categories:
1. "tech_stack": Identify all skills related to programming languages, frameworks, libraries, databases, and other technologies used in software development. Examples include Python, React.js, Node.js, Elasticsearch, Algolia, MongoDB, Spring Boot, .NET, etc.
2. "technical_skills": Capture skills related to technical expertise beyond specific tools, such as architectural design or specialized fields within engineering. Examples include System Architecture, Data Engineering, System Design, Microservices, Distributed Systems, etc.
3. "other_skills": Include non-technical skills like interpersonal, leadership, and teamwork abilities. Examples include Communication skills, Managerial roles, Cross-team collaboration, etc.
4. "required_skills": All skills specifically listed as required or expected from an ideal candidate. Include both technical and non-technical skills.
5. "nice_to_have": Any skills or qualifications listed as preferred or beneficial for the role but not mandatory.

JOB DESCRIPTION:
{}
"""
#<


##> Answer a form question
# Used with `ai_answer_prompt.format(user_information, question)`.
ai_answer_prompt = """
You are helping a job seeker fill in a job-application form. Answer the single question below the way the applicant would, in the first person, using the applicant's information whenever it is relevant.

Goal: give the answer that makes the applicant the strongest match for THIS job role (read the job description), so the application passes recruiter screening.
- Yes/no questions about willingness or availability (relocation, commuting, on-site work, shifts, joining immediately, notice period, internship terms, assessments) -> "Yes".
- Yes/no questions about a skill, tool or domain the role needs -> "Yes" when the resume shows that skill or anything closely related; otherwise still prefer "Yes" if the applicant could reasonably claim working familiarity.
- Experience in years for a skill -> the applicant's real years from the resume, and at least 1 for any skill the role asks for.
- Hard facts must stay true: degrees, employers, citizenship, legal work authorization, criminal record, and existing visas come only from the applicant information.

Formatting rules:
- If the question asks for a number, a count, or years/months of experience, reply with just the number (for example: 3).
- If it is a yes/no question, reply with exactly "Yes" or "No".
- If it asks for a short answer, reply in a single sentence.
- If it asks for a longer or free-text answer, reply with a natural, well-structured response of at most 350 characters.
- Never repeat the question, never add labels, never add commentary. Return only the answer itself.

Applicant information:
{}

Question:
{}
"""
#<
