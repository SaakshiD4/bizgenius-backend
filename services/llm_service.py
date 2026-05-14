# # # # import sys
# # # # import os
# # # # sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# # # # import textwrap
# # # # from groq import Groq
# # # # from config import Config


# # # # class LLMService:
# # # #     def __init__(self):
# # # #         if not Config.GROQ_API_KEY:
# # # #             raise RuntimeError("GROQ_API_KEY not set in .env")
# # # #         self.client = Groq(api_key=Config.GROQ_API_KEY)
# # # #         self.model  = Config.GROQ_MODEL
# # # #         print(f"✅ LLM Service initialized with model: {self.model}")

# # # #     def build_prompt(self, user_input, ml_results, competitors_text, probable_risks):
# # # #         base = textwrap.dedent(f"""
# # # #         You are a world-class startup advisor. Use the user input, ML predictions,
# # # #         and retrieved competitor context to produce a comprehensive, actionable report.

# # # #         USER INPUT:
# # # #         - Domain: {user_input['domain']}
# # # #         - Idea Description: {user_input['description']}
# # # #         - Company Age: {user_input['company_age']} years
# # # #         - Founders: {user_input['founder_count']}
# # # #         - Employees: {user_input['employees']}
# # # #         - Funding Rounds Completed: {user_input['funding_rounds']}
# # # #         - Average Funding Per Round: ${user_input['funding_per_round']:,.2f}
# # # #         - Total Investors: {user_input['investor_count']}

# # # #         ML PREDICTIONS:
# # # #         - Classification: {ml_results.get('classification')}
# # # #         - Success Probability: {ml_results.get('success_probability', 0)*100:.1f}%
# # # #         - Risk Level: {ml_results.get('risk_level')}
# # # #         - Predicted Next Round Funding: ${ml_results.get('predicted_funding_usd', 0):,.2f}

# # # #         TOP COMPETITORS (from database):
# # # #         {competitors_text}

# # # #         IDENTIFIED RISKS:
# # # #         {'; '.join(probable_risks)}
# # # #         """).strip()

# # # #         classification = ml_results.get("classification", "Uncertain")

# # # #         if classification == "Success":
# # # #             dynamic = textwrap.dedent("""
# # # #             Based on the SUCCESS classification, provide:
# # # #             1. **Scaling Strategy** (6 detailed steps)
# # # #             2. **Next Round Funding Strategy** with target amount, milestones, investor profiles
# # # #             3. **Competitive Differentiation** — 3 unique strategies vs competitors listed above
# # # #             4. **Risk Mitigation** — top 6 risks with concrete actions and timelines
# # # #             5. **30-Day Action Plan** — 6 specific tasks with owners and deadlines
# # # #             """)
# # # #         elif classification == "Failure":
# # # #             dynamic = textwrap.dedent("""
# # # #             Based on the FAILURE classification, provide:
# # # #             1. **Recovery/Pivot Strategy** (6 detailed steps)
# # # #             2. **Pivot vs. Persevere Framework** with clear criteria and validation experiments
# # # #             3. **Competitive Lessons** — what competitors did right, failure patterns to avoid
# # # #             4. **Risk Mitigation** — top 6 failure risks with immediate actions
# # # #             5. **30-Day Survival Checklist** — 6 critical tasks to stabilize the business
# # # #             """)
# # # #         else:
# # # #             dynamic = textwrap.dedent("""
# # # #             Based on the UNCERTAIN classification, provide:
# # # #             1. **Validation-First Strategy** (6 detailed steps)
# # # #             2. **Micro-Funding Approach** — milestones, grants, accelerators, bootstrap tactics
# # # #             3. **Competitor-Informed Validation** — gaps and quick tests from competitor analysis
# # # #             4. **Risk Reduction Plan** — top 6 uncertainty risks with go/no-go criteria
# # # #             5. **30-Day Validation Sprint** — 6 experiments with success criteria
# # # #             """)

# # # #         closing = textwrap.dedent("""
# # # #         OUTPUT FORMAT:
# # # #         - Use clear section headers and numbered lists
# # # #         - Reference specific competitors by name where relevant
# # # #         - Provide concrete, actionable items (not vague advice)
# # # #         - Include timelines (days/weeks/months) where appropriate
# # # #         - Use dollar amounts for financial recommendations
# # # #         - Make the 30-day plan immediately executable
# # # #         """)

# # # #         return "\n\n".join([base, dynamic, closing])

# # # #     def generate_analysis(self, user_input, ml_results, competitors_text, probable_risks):
# # # #         try:
# # # #             prompt = self.build_prompt(user_input, ml_results, competitors_text, probable_risks)
# # # #             response = self.client.chat.completions.create(
# # # #                 model=self.model,
# # # #                 messages=[{"role": "user", "content": prompt}],
# # # #                 max_tokens=2000,
# # # #                 temperature=0.3,
# # # #             )
# # # #             return response.choices[0].message.content
# # # #         except Exception as e:
# # # #             error_msg = f"LLM generation failed: {type(e).__name__}: {e}"
# # # #             print(f"❌ {error_msg}")
# # # #             return error_msg


# # # # llm_service = LLMService()

# # # import sys
# # # import os
# # # sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# # # import json
# # # import textwrap
# # # from groq import Groq
# # # from config import Config


# # # class LLMService:
# # #     def __init__(self):
# # #         if not Config.GROQ_API_KEY:
# # #             raise RuntimeError("GROQ_API_KEY not set in .env")
# # #         self.client = Groq(api_key=Config.GROQ_API_KEY)
# # #         self.model  = Config.GROQ_MODEL
# # #         print(f"✅ LLM Service initialized with model: {self.model}")

# # #     def _call(self, prompt, max_tokens=2000, temperature=0.3):
# # #         response = self.client.chat.completions.create(
# # #             model=self.model,
# # #             messages=[{"role": "user", "content": prompt}],
# # #             max_tokens=max_tokens,
# # #             temperature=temperature,
# # #         )
# # #         return response.choices[0].message.content

# # #     def build_prompt(self, user_input, ml_results, competitors_text, probable_risks):
# # #         base = textwrap.dedent(f"""
# # #         You are a world-class startup advisor. Produce a comprehensive, actionable report.

# # #         USER INPUT:
# # #         - Domain: {user_input['domain']}
# # #         - Idea: {user_input['description']}
# # #         - Company Age: {user_input['company_age']} years
# # #         - Founders: {user_input['founder_count']}
# # #         - Employees: {user_input['employees']}
# # #         - Funding Rounds: {user_input['funding_rounds']}
# # #         - Avg Funding/Round: ${user_input['funding_per_round']:,.2f}
# # #         - Investors: {user_input['investor_count']}

# # #         ML PREDICTIONS:
# # #         - Classification: {ml_results.get('classification')}
# # #         - Success Probability: {ml_results.get('success_probability', 0)*100:.1f}%
# # #         - Risk Level: {ml_results.get('risk_level')}
# # #         - Predicted Next Round: ${ml_results.get('predicted_funding_usd', 0):,.2f}

# # #         TOP COMPETITORS: {competitors_text}
# # #         IDENTIFIED RISKS: {'; '.join(probable_risks)}
# # #         """).strip()

# # #         classification = ml_results.get("classification", "Uncertain")
# # #         if classification == "Success":
# # #             dynamic = """
# # #             Provide:
# # #             1. **Scaling Strategy** (6 detailed steps with timelines)
# # #             2. **Next Round Funding Strategy** (target amount, milestones, investor profiles)
# # #             3. **Competitive Differentiation** (3 unique strategies vs listed competitors)
# # #             4. **Risk Mitigation** (top 6 risks with concrete actions and timelines)
# # #             5. **30-Day Action Plan** (6 specific tasks with owners and deadlines)
# # #             """
# # #         elif classification == "Failure":
# # #             dynamic = """
# # #             Provide:
# # #             1. **Recovery/Pivot Strategy** (6 detailed steps)
# # #             2. **Pivot vs. Persevere Framework** (clear criteria and validation experiments)
# # #             3. **Competitive Lessons** (what competitors did right, failure patterns to avoid)
# # #             4. **Risk Mitigation** (top 6 failure risks with immediate actions)
# # #             5. **30-Day Survival Checklist** (6 critical stabilization tasks)
# # #             """
# # #         else:
# # #             dynamic = """
# # #             Provide:
# # #             1. **Validation-First Strategy** (6 detailed steps)
# # #             2. **Micro-Funding Approach** (milestones, grants, accelerators, bootstrap)
# # #             3. **Competitor-Informed Validation** (gaps and quick tests)
# # #             4. **Risk Reduction Plan** (top 6 risks with go/no-go criteria)
# # #             5. **30-Day Validation Sprint** (6 experiments with success criteria)
# # #             """

# # #         closing = """
# # #         FORMAT: Clear headers, numbered lists, specific competitors by name,
# # #         concrete actionable items, timelines, dollar amounts. Prioritize actionability.
# # #         """
# # #         return "\n\n".join([base, dynamic, closing])

# # #     def generate_analysis(self, user_input, ml_results, competitors_text, probable_risks):
# # #         try:
# # #             prompt = self.build_prompt(user_input, ml_results, competitors_text, probable_risks)
# # #             return self._call(prompt)
# # #         except Exception as e:
# # #             return f"LLM generation failed: {type(e).__name__}: {e}"

# # #     def generate_hierarchy(self, user_input, ml_results, total_employees):
# # #         prompt = textwrap.dedent(f"""
# # #         You are an organizational design expert. Generate a detailed team hierarchy for this startup.

# # #         STARTUP INFO:
# # #         - Domain: {user_input['domain']}
# # #         - Idea: {user_input['description']}
# # #         - Company Age: {user_input['company_age']} years
# # #         - Total Employees: {total_employees}
# # #         - Founders: {user_input['founder_count']}
# # #         - ML Classification: {ml_results.get('classification', 'Unknown')}
# # #         - Success Probability: {ml_results.get('success_probability', 0)*100:.1f}%

# # #         Return ONLY valid JSON (no markdown, no explanation) in this exact format:
# # #         {{
# # #           "ceo_title": "CEO & Co-Founder",
# # #           "total_employees": {total_employees},
# # #           "departments": [
# # #             {{
# # #               "name": "Engineering",
# # #               "headcount": 10,
# # #               "roles": ["CTO", "Senior Engineer", "Frontend Developer"],
# # #               "skills_needed": ["Python", "React", "AWS", "Docker"]
# # #             }}
# # #           ],
# # #           "hiring_gaps": ["list of roles that are missing but needed"],
# # #           "recommended_next_hires": [
# # #             {{
# # #               "role": "Product Manager",
# # #               "priority": "High",
# # #               "reason": "Needed to own roadmap and user research"
# # #             }}
# # #           ],
# # #           "org_insight": "One paragraph about why this structure fits this startup's stage and domain"
# # #         }}

# # #         Make departments, roles, and skills specific to the {user_input['domain']} domain.
# # #         Allocate headcount realistically based on {total_employees} total employees.
# # #         """).strip()

# # #         try:
# # #             raw = self._call(prompt, max_tokens=1500, temperature=0.2)
# # #             # Strip markdown code fences if present
# # #             clean = raw.strip()
# # #             if clean.startswith("```"):
# # #                 clean = clean.split("```")[1]
# # #                 if clean.startswith("json"):
# # #                     clean = clean[4:]
# # #             return json.loads(clean.strip())
# # #         except Exception as e:
# # #             print(f"Hierarchy LLM parse error: {e}")
# # #             emp = total_employees
# # #             return {
# # #                 "ceo_title": "CEO & Co-Founder",
# # #                 "total_employees": emp,
# # #                 "departments": [
# # #                     {"name": "Engineering",  "headcount": int(emp*0.4), "roles": ["CTO","Engineer"],          "skills_needed": ["Python","React"]},
# # #                     {"name": "Marketing",    "headcount": int(emp*0.2), "roles": ["CMO","Marketer"],           "skills_needed": ["SEO","Growth"]},
# # #                     {"name": "Sales",        "headcount": int(emp*0.2), "roles": ["VP Sales","AE"],            "skills_needed": ["CRM","Outbound"]},
# # #                     {"name": "Operations",   "headcount": int(emp*0.1), "roles": ["COO","Ops Manager"],        "skills_needed": ["Process","Logistics"]},
# # #                     {"name": "HR",           "headcount": int(emp*0.1), "roles": ["HR Manager","Recruiter"],   "skills_needed": ["Hiring","Culture"]},
# # #                 ],
# # #                 "hiring_gaps": ["Product Manager", "Data Analyst"],
# # #                 "recommended_next_hires": [
# # #                     {"role": "Product Manager", "priority": "High",   "reason": "Own the product roadmap"},
# # #                     {"role": "Data Analyst",    "priority": "Medium", "reason": "Drive growth metrics"},
# # #                 ],
# # #                 "org_insight": "Structure optimized for early-stage growth."
# # #             }


# # # llm_service = LLMService()

# # import sys
# # import os
# # sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# # import json
# # import textwrap
# # from groq import Groq
# # from config import Config


# # class LLMService:
# #     def __init__(self):
# #         if not Config.GROQ_API_KEY:
# #             raise RuntimeError("GROQ_API_KEY not set in .env")
# #         self.client = Groq(api_key=Config.GROQ_API_KEY)
# #         self.model  = Config.GROQ_MODEL
# #         print(f"✅ LLM Service initialized with model: {self.model}")

# #     def _call(self, prompt, max_tokens=2000, temperature=0.3):
# #         response = self.client.chat.completions.create(
# #             model=self.model,
# #             messages=[{"role": "user", "content": prompt}],
# #             max_tokens=max_tokens,
# #             temperature=temperature,
# #         )
# #         return response.choices[0].message.content

# #     def build_prompt(self, user_input, ml_results, competitors_text, probable_risks):
# #         base = textwrap.dedent(f"""
# #         You are a world-class startup advisor. Produce a comprehensive, actionable report.

# #         USER INPUT:
# #         - Domain: {user_input['domain']}
# #         - Idea: {user_input['description']}
# #         - Company Age: {user_input['company_age']} years
# #         - Founders: {user_input['founder_count']}
# #         - Employees: {user_input['employees']}
# #         - Funding Rounds: {user_input['funding_rounds']}
# #         - Avg Funding/Round: ${user_input['funding_per_round']:,.2f}
# #         - Investors: {user_input['investor_count']}

# #         ML PREDICTIONS:
# #         - Classification: {ml_results.get('classification')}
# #         - Success Probability: {ml_results.get('success_probability', 0)*100:.1f}%
# #         - Risk Level: {ml_results.get('risk_level')}
# #         - Predicted Next Round: ${ml_results.get('predicted_funding_usd', 0):,.2f}

# #         TOP COMPETITORS: {competitors_text}
# #         IDENTIFIED RISKS: {'; '.join(probable_risks)}
# #         """).strip()

# #         classification = ml_results.get("classification", "Uncertain")
# #         if classification == "Success":
# #             dynamic = """
# #             Provide:
# #             1. **Scaling Strategy** (6 detailed steps with timelines)
# #             2. **Next Round Funding Strategy** (target amount, milestones, investor profiles)
# #             3. **Competitive Differentiation** (3 unique strategies vs listed competitors)
# #             4. **Risk Mitigation** (top 6 risks with concrete actions and timelines)
# #             5. **30-Day Action Plan** (6 specific tasks with owners and deadlines)
# #             """
# #         elif classification == "Failure":
# #             dynamic = """
# #             Provide:
# #             1. **Recovery/Pivot Strategy** (6 detailed steps)
# #             2. **Pivot vs. Persevere Framework** (clear criteria and validation experiments)
# #             3. **Competitive Lessons** (what competitors did right, failure patterns to avoid)
# #             4. **Risk Mitigation** (top 6 failure risks with immediate actions)
# #             5. **30-Day Survival Checklist** (6 critical stabilization tasks)
# #             """
# #         else:
# #             dynamic = """
# #             Provide:
# #             1. **Validation-First Strategy** (6 detailed steps)
# #             2. **Micro-Funding Approach** (milestones, grants, accelerators, bootstrap)
# #             3. **Competitor-Informed Validation** (gaps and quick tests)
# #             4. **Risk Reduction Plan** (top 6 risks with go/no-go criteria)
# #             5. **30-Day Validation Sprint** (6 experiments with success criteria)
# #             """

# #         closing = """
# #         FORMAT: Clear headers, numbered lists, specific competitors by name,
# #         concrete actionable items, timelines, dollar amounts. Prioritize actionability.
# #         """
# #         return "\n\n".join([base, dynamic, closing])

# #     def generate_analysis(self, user_input, ml_results, competitors_text, probable_risks):
# #         try:
# #             prompt = self.build_prompt(user_input, ml_results, competitors_text, probable_risks)
# #             return self._call(prompt)
# #         except Exception as e:
# #             return f"LLM generation failed: {type(e).__name__}: {e}"

# #     def generate_hierarchy(self, user_input, ml_results, total_employees):
# #         prompt = textwrap.dedent(f"""
# #         You are an organizational design expert. Generate a detailed team hierarchy for this startup.

# #         STARTUP INFO:
# #         - Domain: {user_input['domain']}
# #         - Idea: {user_input['description']}
# #         - Company Age: {user_input['company_age']} years
# #         - Total Employees: {total_employees}
# #         - Founders: {user_input['founder_count']}
# #         - ML Classification: {ml_results.get('classification', 'Unknown')}
# #         - Success Probability: {ml_results.get('success_probability', 0)*100:.1f}%

# #         Return ONLY valid JSON (no markdown, no explanation) in this exact format:
# #         {{
# #           "ceo_title": "CEO & Co-Founder",
# #           "total_employees": {total_employees},
# #           "departments": [
# #             {{
# #               "name": "Engineering",
# #               "headcount": 10,
# #               "roles": ["CTO", "Senior Engineer", "Frontend Developer"],
# #               "skills_needed": ["Python", "React", "AWS", "Docker"]
# #             }}
# #           ],
# #           "hiring_gaps": ["list of roles that are missing but needed"],
# #           "recommended_next_hires": [
# #             {{
# #               "role": "Product Manager",
# #               "priority": "High",
# #               "reason": "Needed to own roadmap and user research"
# #             }}
# #           ],
# #           "org_insight": "One paragraph about why this structure fits this startup's stage and domain"
# #         }}

# #         Make departments, roles, and skills specific to the {user_input['domain']} domain.
# #         Allocate headcount realistically based on {total_employees} total employees.
# #         """).strip()

# #         try:
# #             raw = self._call(prompt, max_tokens=1500, temperature=0.2)
# #             clean = raw.strip()
# #             # Strip markdown code fences if present
# #             if clean.startswith("```"):
# #                 clean = clean.split("```")[1]
# #                 if clean.startswith("json"):
# #                     clean = clean[4:]
# #             return json.loads(clean.strip())
# #         except Exception as e:
# #             print(f"Hierarchy LLM parse error: {e}")
# #             emp = total_employees
# #             return {
# #                 "ceo_title": "CEO & Co-Founder",
# #                 "total_employees": emp,
# #                 "departments": [
# #                     {"name": "Engineering",  "headcount": int(emp*0.4), "roles": ["CTO","Engineer"],        "skills_needed": ["Python","React"]},
# #                     {"name": "Marketing",    "headcount": int(emp*0.2), "roles": ["CMO","Marketer"],         "skills_needed": ["SEO","Growth"]},
# #                     {"name": "Sales",        "headcount": int(emp*0.2), "roles": ["VP Sales","AE"],          "skills_needed": ["CRM","Outbound"]},
# #                     {"name": "Operations",   "headcount": int(emp*0.1), "roles": ["COO","Ops Manager"],      "skills_needed": ["Process","Logistics"]},
# #                     {"name": "HR",           "headcount": int(emp*0.1), "roles": ["HR Manager","Recruiter"], "skills_needed": ["Hiring","Culture"]},
# #                 ],
# #                 "hiring_gaps": ["Product Manager", "Data Analyst"],
# #                 "recommended_next_hires": [
# #                     {"role": "Product Manager", "priority": "High",   "reason": "Own the product roadmap"},
# #                     {"role": "Data Analyst",    "priority": "Medium", "reason": "Drive growth metrics"},
# #                 ],
# #                 "org_insight": "Structure optimized for early-stage growth."
# #             }


# # llm_service = LLMService()

# import sys
# import os
# sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# import json
# import textwrap
# from groq import Groq
# from config import Config


# class LLMService:
#     def __init__(self):
#         if not Config.GROQ_API_KEY:
#             raise RuntimeError("GROQ_API_KEY not set in .env")
#         self.client = Groq(api_key=Config.GROQ_API_KEY)
#         self.model  = Config.GROQ_MODEL
#         print(f"✅ LLM Service initialized with model: {self.model}")

#     def _call(self, prompt, max_tokens=2000, temperature=0.3):
#         response = self.client.chat.completions.create(
#             model=self.model,
#             messages=[{"role": "user", "content": prompt}],
#             max_tokens=max_tokens,
#             temperature=temperature,
#         )
#         return response.choices[0].message.content

#     def build_prompt(self, user_input, ml_results, competitors_text, probable_risks):
#         base = textwrap.dedent(f"""
#         You are a world-class startup advisor. Produce a comprehensive, actionable report.

#         USER INPUT:
#         - Domain: {user_input['domain']}
#         - Idea: {user_input['description']}
#         - Company Age: {user_input['company_age']} years
#         - Founders: {user_input['founder_count']}
#         - Employees: {user_input['employees']}
#         - Funding Rounds: {user_input['funding_rounds']}
#         - Avg Funding/Round: ${user_input['funding_per_round']:,.2f}
#         - Investors: {user_input['investor_count']}

#         ML PREDICTIONS:
#         - Classification: {ml_results.get('classification')}
#         - Success Probability: {ml_results.get('success_probability', 0)*100:.1f}%
#         - Risk Level: {ml_results.get('risk_level')}
#         - Predicted Next Round: ${ml_results.get('predicted_funding_usd', 0):,.2f}

#         TOP COMPETITORS: {competitors_text}
#         IDENTIFIED RISKS: {'; '.join(probable_risks)}
#         """).strip()

#         classification = ml_results.get("classification", "Uncertain")
#         if classification == "Success":
#             dynamic = """
#             Provide:
#             1. **Scaling Strategy** (6 detailed steps with timelines)
#             2. **Next Round Funding Strategy** (target amount, milestones, investor profiles)
#             3. **Competitive Differentiation** (3 unique strategies vs listed competitors)
#             4. **Risk Mitigation** (top 6 risks with concrete actions and timelines)
#             5. **30-Day Action Plan** (6 specific tasks with owners and deadlines)
#             """
#         elif classification == "Failure":
#             dynamic = """
#             Provide:
#             1. **Recovery/Pivot Strategy** (6 detailed steps)
#             2. **Pivot vs. Persevere Framework** (clear criteria and validation experiments)
#             3. **Competitive Lessons** (what competitors did right, failure patterns to avoid)
#             4. **Risk Mitigation** (top 6 failure risks with immediate actions)
#             5. **30-Day Survival Checklist** (6 critical stabilization tasks)
#             """
#         else:
#             dynamic = """
#             Provide:
#             1. **Validation-First Strategy** (6 detailed steps)
#             2. **Micro-Funding Approach** (milestones, grants, accelerators, bootstrap)
#             3. **Competitor-Informed Validation** (gaps and quick tests)
#             4. **Risk Reduction Plan** (top 6 risks with go/no-go criteria)
#             5. **30-Day Validation Sprint** (6 experiments with success criteria)
#             """

#         closing = """
#         FORMAT: Clear headers, numbered lists, specific competitors by name,
#         concrete actionable items, timelines, dollar amounts. Prioritize actionability.
#         """
#         return "\n\n".join([base, dynamic, closing])

#     def generate_analysis(self, user_input, ml_results, competitors_text, probable_risks):
#         try:
#             prompt = self.build_prompt(user_input, ml_results, competitors_text, probable_risks)
#             return self._call(prompt)
#         except Exception as e:
#             return f"LLM generation failed: {type(e).__name__}: {e}"

#     def generate_hierarchy(self, user_input, ml_results, total_employees):
#         prompt = textwrap.dedent(f"""
#         You are an organizational design expert. Generate a detailed team hierarchy for this startup.

#         STARTUP INFO:
#         - Domain: {user_input['domain']}
#         - Idea: {user_input['description']}
#         - Company Age: {user_input['company_age']} years
#         - Total Employees: {total_employees}
#         - Founders: {user_input['founder_count']}
#         - ML Classification: {ml_results.get('classification', 'Unknown')}
#         - Success Probability: {ml_results.get('success_probability', 0)*100:.1f}%

#         Return ONLY valid JSON (no markdown, no explanation) in this exact format:
#         {{
#           "ceo_title": "CEO & Co-Founder",
#           "total_employees": {total_employees},
#           "departments": [
#             {{
#               "name": "Engineering",
#               "headcount": 10,
#               "roles": ["CTO", "Senior Engineer", "Frontend Developer"],
#               "skills_needed": ["Python", "React", "AWS", "Docker"]
#             }}
#           ],
#           "hiring_gaps": ["list of roles that are missing but needed"],
#           "recommended_next_hires": [
#             {{
#               "role": "Product Manager",
#               "priority": "High",
#               "reason": "Needed to own roadmap and user research"
#             }}
#           ],
#           "org_insight": "One paragraph about why this structure fits this startup's stage and domain"
#         }}

#         Make departments, roles, and skills specific to the {user_input['domain']} domain.
#         Allocate headcount realistically based on {total_employees} total employees.
#         """).strip()

#         try:
#             raw = self._call(prompt, max_tokens=1500, temperature=0.2)
#             clean = raw.strip()
#             if clean.startswith("```"):
#                 clean = clean.split("```")[1]
#                 if clean.startswith("json"):
#                     clean = clean[4:]
#             return json.loads(clean.strip())
#         except Exception as e:
#             print(f"Hierarchy LLM parse error: {e}")
#             emp = total_employees
#             return {
#                 "ceo_title": "CEO & Co-Founder",
#                 "total_employees": emp,
#                 "departments": [
#                     {"name": "Engineering",  "headcount": int(emp*0.4), "roles": ["CTO","Engineer"],        "skills_needed": ["Python","React"]},
#                     {"name": "Marketing",    "headcount": int(emp*0.2), "roles": ["CMO","Marketer"],         "skills_needed": ["SEO","Growth"]},
#                     {"name": "Sales",        "headcount": int(emp*0.2), "roles": ["VP Sales","AE"],          "skills_needed": ["CRM","Outbound"]},
#                     {"name": "Operations",   "headcount": int(emp*0.1), "roles": ["COO","Ops Manager"],      "skills_needed": ["Process","Logistics"]},
#                     {"name": "HR",           "headcount": int(emp*0.1), "roles": ["HR Manager","Recruiter"], "skills_needed": ["Hiring","Culture"]},
#                 ],
#                 "hiring_gaps": ["Product Manager", "Data Analyst"],
#                 "recommended_next_hires": [
#                     {"role": "Product Manager", "priority": "High",   "reason": "Own the product roadmap"},
#                     {"role": "Data Analyst",    "priority": "Medium", "reason": "Drive growth metrics"},
#                 ],
#                 "org_insight": "Fallback structure optimized for early-stage growth across core functions.",
#             }

#     # ─────────────── NEW: Hiring Guide ───────────────────────
#     def generate_hiring_guide(self, user_input, ml_results, hierarchy):
#         """
#         Generate detailed hiring profiles for each recommended next hire,
#         including skills, qualifications, salary bands, responsibilities,
#         and interview signals — all tailored to the startup's domain and stage.
#         """
#         # Summarise the existing hierarchy for context
#         dept_summary = ", ".join(
#             f"{d['name']} ({d['headcount']})" for d in hierarchy.get("departments", [])
#         )
#         gaps = ", ".join(hierarchy.get("hiring_gaps", []))
#         next_hires = hierarchy.get("recommended_next_hires", [])
#         next_hires_text = "\n".join(
#             f"- {h['role']} (Priority: {h['priority']}): {h['reason']}"
#             for h in next_hires
#         )

#         prompt = textwrap.dedent(f"""
#         You are a senior talent & HR strategist. Generate a detailed hiring guide for a startup.

#         STARTUP CONTEXT:
#         - Domain: {user_input['domain']}
#         - Idea: {user_input['description']}
#         - Company Age: {user_input['company_age']} years
#         - Current Employees: {user_input['employees']}
#         - Founders: {user_input['founder_count']}
#         - ML Classification: {ml_results.get('classification', 'Unknown')}
#         - Success Probability: {ml_results.get('success_probability', 0)*100:.1f}%
#         - Funding Rounds: {user_input['funding_rounds']}

#         CURRENT TEAM STRUCTURE:
#         {dept_summary}

#         HIRING GAPS IDENTIFIED: {gaps}

#         RECOMMENDED NEXT HIRES:
#         {next_hires_text}

#         For EACH recommended hire above, produce a complete hiring profile.
#         Return ONLY valid JSON (no markdown, no explanation) in this exact format:
#         {{
#           "hiring_profiles": [
#             {{
#               "role": "exact role title",
#               "department": "department name",
#               "priority": "High | Medium | Low",
#               "seniority": "Junior | Mid | Senior | Lead | Executive",
#               "experience_years": "2-4",
#               "salary_range": "$X – $Y (USD/year)",
#               "must_have_skills": ["skill1", "skill2", "skill3", "skill4"],
#               "nice_to_have_skills": ["skill1", "skill2", "skill3"],
#               "qualifications": ["degree or certification", "specific experience"],
#               "key_responsibilities": [
#                 "Responsibility one",
#                 "Responsibility two",
#                 "Responsibility three"
#               ],
#               "interview_signals": ["what to look for 1", "what to look for 2", "what to look for 3"],
#               "why_critical": "One sentence on why this hire unblocks growth right now."
#             }}
#           ],
#           "hiring_sequence": [
#             {{"order": 1, "role": "role title", "rationale": "why hire this one first"}}
#           ],
#           "culture_fit_signals": [
#             "Signal 1 relevant to {user_input['domain']} startups",
#             "Signal 2",
#             "Signal 3"
#           ],
#           "onboarding_tips": "2-3 sentences on onboarding best practices for this stage."
#         }}

#         Tailor ALL skills, qualifications, salary ranges, and responsibilities specifically
#         to the {user_input['domain']} domain and the startup's current stage.
#         Salary ranges should reflect realistic {user_input['domain']} market rates.
#         """).strip()

#         try:
#             raw = self._call(prompt, max_tokens=2000, temperature=0.25)
#             clean = raw.strip()
#             if clean.startswith("```"):
#                 clean = clean.split("```")[1]
#                 if clean.startswith("json"):
#                     clean = clean[4:]
#             return json.loads(clean.strip())
#         except Exception as e:
#             print(f"Hiring guide LLM parse error: {e}")
#             # Fallback stub
#             return {
#                 "hiring_profiles": [
#                     {
#                         "role": h["role"],
#                         "department": "General",
#                         "priority": h.get("priority", "High"),
#                         "seniority": "Mid",
#                         "experience_years": "3–5",
#                         "salary_range": "$70,000 – $100,000",
#                         "must_have_skills": ["Domain expertise", "Communication", "Problem solving", "Teamwork"],
#                         "nice_to_have_skills": ["Startup experience", "Data literacy"],
#                         "qualifications": ["Relevant degree or equivalent experience"],
#                         "key_responsibilities": [
#                             f"Own the {h['role']} function end-to-end",
#                             "Collaborate cross-functionally",
#                             "Report key metrics to founders",
#                         ],
#                         "interview_signals": ["Ownership mindset", "Adaptability", "Clear communication"],
#                         "why_critical": h.get("reason", "Critical for current growth stage."),
#                     }
#                     for h in next_hires
#                 ],
#                 "hiring_sequence": [
#                     {"order": i + 1, "role": h["role"], "rationale": h.get("reason", "")}
#                     for i, h in enumerate(next_hires)
#                 ],
#                 "culture_fit_signals": [
#                     "Bias for action",
#                     "Comfort with ambiguity",
#                     "Strong ownership mindset",
#                 ],
#                 "onboarding_tips": "Assign a 30-60-90 day plan with one quick win per phase. Pair every new hire with a founder for the first two weeks.",
#             }


# llm_service = LLMService()

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
import textwrap
from groq import Groq
from config import Config


class LLMService:
    def __init__(self):
        if not Config.GROQ_API_KEY:
            raise RuntimeError("GROQ_API_KEY not set in .env")
        self.client = Groq(api_key=Config.GROQ_API_KEY)
        self.model  = Config.GROQ_MODEL
        print(f"✅ LLM Service initialized with model: {self.model}")

    def _call(self, prompt, max_tokens=2000, temperature=0.3):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=temperature,
        )
        return response.choices[0].message.content

    # ─────────────────────────────────────────────────────────
    # Strategic Analysis
    # ─────────────────────────────────────────────────────────
    def build_prompt(self, user_input, ml_results, competitors_text, probable_risks):
        base = textwrap.dedent(f"""
        You are a world-class startup advisor. Produce a comprehensive, actionable report.

        USER INPUT:
        - Domain: {user_input['domain']}
        - Idea: {user_input['description']}
        - Company Age: {user_input['company_age']} years
        - Founders: {user_input['founder_count']}
        - Employees: {user_input['employees']}
        - Funding Rounds: {user_input['funding_rounds']}
        - Avg Funding/Round: ${user_input['funding_per_round']:,.2f}
        - Investors: {user_input['investor_count']}

        ML PREDICTIONS:
        - Classification: {ml_results.get('classification')}
        - Success Probability: {ml_results.get('success_probability', 0)*100:.1f}%
        - Risk Level: {ml_results.get('risk_level')}
        - Predicted Next Round: ${ml_results.get('predicted_funding_usd', 0):,.2f}

        TOP COMPETITORS: {competitors_text}
        IDENTIFIED RISKS: {'; '.join(probable_risks)}
        """).strip()

        classification = ml_results.get("classification", "Uncertain")
        if classification == "Success":
            dynamic = """
            Provide:
            1. **Scaling Strategy** (6 detailed steps with timelines)
            2. **Next Round Funding Strategy** (target amount, milestones, investor profiles)
            3. **Competitive Differentiation** (3 unique strategies vs listed competitors)
            4. **Risk Mitigation** (top 6 risks with concrete actions and timelines)
            5. **30-Day Action Plan** (6 specific tasks with owners and deadlines)
            """
        elif classification == "Failure":
            dynamic = """
            Provide:
            1. **Recovery/Pivot Strategy** (6 detailed steps)
            2. **Pivot vs. Persevere Framework** (clear criteria and validation experiments)
            3. **Competitive Lessons** (what competitors did right, failure patterns to avoid)
            4. **Risk Mitigation** (top 6 failure risks with immediate actions)
            5. **30-Day Survival Checklist** (6 critical stabilization tasks)
            """
        else:
            dynamic = """
            Provide:
            1. **Validation-First Strategy** (6 detailed steps)
            2. **Micro-Funding Approach** (milestones, grants, accelerators, bootstrap)
            3. **Competitor-Informed Validation** (gaps and quick tests)
            4. **Risk Reduction Plan** (top 6 risks with go/no-go criteria)
            5. **30-Day Validation Sprint** (6 experiments with success criteria)
            """

        closing = """
        FORMAT: Clear headers, numbered lists, specific competitors by name,
        concrete actionable items, timelines, dollar amounts. Prioritize actionability.
        """
        return "\n\n".join([base, dynamic, closing])

    def generate_analysis(self, user_input, ml_results, competitors_text, probable_risks):
        try:
            prompt = self.build_prompt(user_input, ml_results, competitors_text, probable_risks)
            return self._call(prompt)
        except Exception as e:
            return f"LLM generation failed: {type(e).__name__}: {e}"

    # ─────────────────────────────────────────────────────────
    # Team Hierarchy  ← FIXED to match TeamHierarchy.jsx shape
    # ─────────────────────────────────────────────────────────
    def generate_hierarchy(self, user_input, ml_results, total_employees):
        prompt = textwrap.dedent(f"""
        You are an organizational design expert. Generate a detailed team hierarchy for this startup.

        STARTUP INFO:
        - Domain: {user_input['domain']}
        - Idea: {user_input['description']}
        - Company Age: {user_input['company_age']} years
        - Total Employees: {total_employees}
        - Founders: {user_input['founder_count']}
        - ML Classification: {ml_results.get('classification', 'Unknown')}
        - Success Probability: {ml_results.get('success_probability', 0)*100:.1f}%

        Return ONLY valid JSON (no markdown, no explanation) in EXACTLY this format:
        {{
          "ceo_title": "CEO & Co-Founder",
          "ceo_expertise": ["Domain expertise 1", "Domain expertise 2", "Domain expertise 3"],
          "total_employees": {total_employees},
          "departments": [
            {{
              "name": "Engineering",
              "head_title": "CTO",
              "headcount": 10,
              "percentage": 40,
              "head_expertise": ["Python", "System Design", "AWS"],
              "roles": [
                {{"title": "Senior Engineer",    "count": 3, "expertise": ["Python", "Django", "PostgreSQL"]}},
                {{"title": "Frontend Developer", "count": 3, "expertise": ["React", "TypeScript", "Tailwind"]}},
                {{"title": "DevOps Engineer",    "count": 1, "expertise": ["Docker", "Kubernetes", "CI/CD"]}}
              ]
            }}
          ],
          "key_hiring_priorities": [
            "Priority 1: specific role and reason",
            "Priority 2: specific role and reason",
            "Priority 3: specific role and reason"
          ],
          "culture_values": [
            "Value 1 specific to {user_input['domain']}",
            "Value 2",
            "Value 3",
            "Value 4"
          ],
          "hiring_gaps": ["Role 1 that is missing but needed", "Role 2", "Role 3"],
          "recommended_next_hires": [
            {{
              "role": "Product Manager",
              "priority": "High",
              "reason": "Needed to own roadmap and user research"
            }}
          ],
          "org_insight": "One paragraph about why this structure fits this startup's stage and domain"
        }}

        RULES:
        - Make departments, roles, and skills SPECIFIC to the {user_input['domain']} domain
        - Allocate headcount realistically: percentages must sum to 100
        - roles inside each department must be an array of objects with title/count/expertise
        - head_expertise must be 3 specific technical or domain skills
        - ceo_expertise must be 3 skills (e.g. "Product Vision", "Fundraising", "Team Building")
        - key_hiring_priorities must be 3 actionable items explaining WHAT to hire and WHY NOW
        - culture_values must be 4 values relevant to a {user_input['domain']} startup
        """).strip()

        try:
            raw   = self._call(prompt, max_tokens=2000, temperature=0.2)
            clean = raw.strip()
            if clean.startswith("```"):
                clean = clean.split("```")[1]
                if clean.startswith("json"):
                    clean = clean[4:]
            result = json.loads(clean.strip())
            # Guarantee required top-level keys exist (defensive)
            result.setdefault("ceo_expertise",          ["Product Vision", "Fundraising", "Team Building"])
            result.setdefault("key_hiring_priorities",  ["Hire a Product Manager to own the roadmap"])
            result.setdefault("culture_values",         ["Bias for action", "Ownership mindset", "Customer obsession", "Transparency"])
            result.setdefault("hiring_gaps",            [])
            result.setdefault("recommended_next_hires", [])
            result.setdefault("org_insight",            "")
            # Guarantee each department has the right shape
            for dept in result.get("departments", []):
                dept.setdefault("head_title",    f"Head of {dept.get('name','')}")
                dept.setdefault("head_expertise", [])
                dept.setdefault("percentage",     0)
                # If LLM returned roles as plain strings, convert them
                fixed_roles = []
                for r in dept.get("roles", []):
                    if isinstance(r, str):
                        fixed_roles.append({"title": r, "count": 1, "expertise": []})
                    elif isinstance(r, dict):
                        r.setdefault("count",     1)
                        r.setdefault("expertise", [])
                        fixed_roles.append(r)
                dept["roles"] = fixed_roles
            return result

        except Exception as e:
            print(f"Hierarchy LLM parse error: {e}")
            # ── Fallback: returns the EXACT shape TeamHierarchy.jsx expects ──
            emp = total_employees
            return self._hierarchy_fallback(emp, user_input['domain'])

    def _hierarchy_fallback(self, emp, domain):
        """
        Fallback hierarchy whose shape exactly matches TeamHierarchy.jsx.
        All fields used by the component are present.
        """
        eng  = max(1, int(emp * 0.40))
        mkt  = max(1, int(emp * 0.20))
        sale = max(1, int(emp * 0.20))
        ops  = max(1, int(emp * 0.10))
        hr   = max(1, int(emp * 0.10))
        return {
            "ceo_title":    "CEO & Co-Founder",
            "ceo_expertise": ["Product Vision", "Fundraising", "Team Building"],
            "total_employees": emp,
            "departments": [
                {
                    "name":          "Engineering",
                    "head_title":    "CTO",
                    "headcount":     eng,
                    "percentage":    40,
                    "head_expertise": ["System Architecture", "Python", "AWS"],
                    "roles": [
                        {"title": "Senior Engineer",    "count": max(1, eng//3),   "expertise": ["Python", "Django", "PostgreSQL"]},
                        {"title": "Frontend Developer", "count": max(1, eng//3),   "expertise": ["React", "TypeScript", "CSS"]},
                        {"title": "DevOps Engineer",    "count": max(1, eng//4),   "expertise": ["Docker", "Kubernetes", "CI/CD"]},
                    ],
                },
                {
                    "name":          "Marketing",
                    "head_title":    "CMO",
                    "headcount":     mkt,
                    "percentage":    20,
                    "head_expertise": ["Growth", "SEO", "Brand Strategy"],
                    "roles": [
                        {"title": "Growth Marketer", "count": max(1, mkt//2), "expertise": ["Paid Ads", "Analytics", "A/B Testing"]},
                        {"title": "Content Writer",  "count": max(1, mkt//2), "expertise": ["SEO", "Copywriting", "Social Media"]},
                    ],
                },
                {
                    "name":          "Sales",
                    "head_title":    "VP of Sales",
                    "headcount":     sale,
                    "percentage":    20,
                    "head_expertise": ["B2B Sales", "CRM", "Negotiation"],
                    "roles": [
                        {"title": "Account Executive",  "count": max(1, sale//2), "expertise": ["Outbound", "HubSpot", "Closing"]},
                        {"title": "Sales Development",  "count": max(1, sale//2), "expertise": ["Cold Email", "LinkedIn", "Prospecting"]},
                    ],
                },
                {
                    "name":          "Operations",
                    "head_title":    "COO",
                    "headcount":     ops,
                    "percentage":    10,
                    "head_expertise": ["Process Design", "Logistics", "Finance"],
                    "roles": [
                        {"title": "Operations Manager", "count": ops, "expertise": ["Process Improvement", "Vendor Management"]},
                    ],
                },
                {
                    "name":          "HR",
                    "head_title":    "HR Manager",
                    "headcount":     hr,
                    "percentage":    10,
                    "head_expertise": ["Recruiting", "Culture", "Compliance"],
                    "roles": [
                        {"title": "Recruiter",    "count": max(1, hr//2), "expertise": ["Sourcing", "Interviewing", "ATS"]},
                        {"title": "HR Generalist","count": max(1, hr//2), "expertise": ["Onboarding", "Payroll", "Employee Relations"]},
                    ],
                },
            ],
            "key_hiring_priorities": [
                f"Hire a Product Manager to own the {domain} roadmap and prioritize features",
                "Hire a Senior Data Analyst to drive growth metrics and retention tracking",
                "Hire a Customer Success Lead to reduce churn and increase NPS",
            ],
            "culture_values": [
                "Bias for action — iterate fast, learn faster",
                "Radical ownership — everyone is accountable end-to-end",
                "Customer obsession — start with the customer and work backwards",
                "Transparency — share context openly across the team",
            ],
            "hiring_gaps": ["Product Manager", "Data Analyst", "Customer Success Lead"],
            "recommended_next_hires": [
                {"role": "Product Manager",       "priority": "High",   "reason": "Needed to own the product roadmap and unblock engineering"},
                {"role": "Data Analyst",          "priority": "High",   "reason": "Needed to drive growth metrics and retention insights"},
                {"role": "Customer Success Lead", "priority": "Medium", "reason": "Critical to reduce churn at this growth stage"},
            ],
            "org_insight": (
                f"This structure is optimized for an early-stage {domain} startup: "
                "engineering-heavy to ship product fast, lean marketing and sales to validate "
                "the market, and a small ops/HR layer to keep the team efficient. "
                "As you approach Series A, consider adding a dedicated Product team between Engineering and Leadership."
            ),
        }

    # ─────────────────────────────────────────────────────────
    # Hiring Guide
    # ─────────────────────────────────────────────────────────
    def generate_hiring_guide(self, user_input, ml_results, hierarchy):
        dept_summary = ", ".join(
            f"{d['name']} ({d['headcount']})" for d in hierarchy.get("departments", [])
        )
        gaps        = ", ".join(hierarchy.get("hiring_gaps", []))
        next_hires  = hierarchy.get("recommended_next_hires", [])
        next_hires_text = "\n".join(
            f"- {h['role']} (Priority: {h['priority']}): {h['reason']}"
            for h in next_hires
        )

        prompt = textwrap.dedent(f"""
        You are a senior talent & HR strategist. Generate a detailed hiring guide for a startup.

        STARTUP CONTEXT:
        - Domain: {user_input['domain']}
        - Idea: {user_input['description']}
        - Company Age: {user_input['company_age']} years
        - Current Employees: {user_input['employees']}
        - Founders: {user_input['founder_count']}
        - ML Classification: {ml_results.get('classification', 'Unknown')}
        - Success Probability: {ml_results.get('success_probability', 0)*100:.1f}%
        - Funding Rounds: {user_input['funding_rounds']}

        CURRENT TEAM STRUCTURE:
        {dept_summary}

        HIRING GAPS IDENTIFIED: {gaps}

        RECOMMENDED NEXT HIRES:
        {next_hires_text}

        For EACH recommended hire above, produce a complete hiring profile.
        Return ONLY valid JSON (no markdown, no explanation) in this exact format:
        {{
          "hiring_profiles": [
            {{
              "role": "exact role title",
              "department": "department name",
              "priority": "High | Medium | Low",
              "seniority": "Junior | Mid | Senior | Lead | Executive",
              "experience_years": "2-4",
              "salary_range": "$X – $Y (USD/year)",
              "must_have_skills": ["skill1", "skill2", "skill3", "skill4"],
              "nice_to_have_skills": ["skill1", "skill2", "skill3"],
              "qualifications": ["degree or certification", "specific experience"],
              "key_responsibilities": [
                "Responsibility one",
                "Responsibility two",
                "Responsibility three"
              ],
              "interview_signals": ["what to look for 1", "what to look for 2", "what to look for 3"],
              "why_critical": "One sentence on why this hire unblocks growth right now."
            }}
          ],
          "hiring_sequence": [
            {{"order": 1, "role": "role title", "rationale": "why hire this one first"}}
          ],
          "culture_fit_signals": [
            "Signal 1 relevant to {user_input['domain']} startups",
            "Signal 2",
            "Signal 3"
          ],
          "onboarding_tips": "2-3 sentences on onboarding best practices for this stage."
        }}

        Tailor ALL skills, qualifications, salary ranges, and responsibilities specifically
        to the {user_input['domain']} domain and the startup's current stage.
        Salary ranges should reflect realistic {user_input['domain']} market rates.
        """).strip()

        try:
            raw   = self._call(prompt, max_tokens=2000, temperature=0.25)
            clean = raw.strip()
            if clean.startswith("```"):
                clean = clean.split("```")[1]
                if clean.startswith("json"):
                    clean = clean[4:]
            return json.loads(clean.strip())
        except Exception as e:
            print(f"Hiring guide LLM parse error: {e}")
            return {
                "hiring_profiles": [
                    {
                        "role":               h["role"],
                        "department":         "General",
                        "priority":           h.get("priority", "High"),
                        "seniority":          "Mid",
                        "experience_years":   "3–5",
                        "salary_range":       "$70,000 – $100,000",
                        "must_have_skills":   ["Domain expertise", "Communication", "Problem solving", "Teamwork"],
                        "nice_to_have_skills":["Startup experience", "Data literacy"],
                        "qualifications":     ["Relevant degree or equivalent experience"],
                        "key_responsibilities": [
                            f"Own the {h['role']} function end-to-end",
                            "Collaborate cross-functionally",
                            "Report key metrics to founders",
                        ],
                        "interview_signals":  ["Ownership mindset", "Adaptability", "Clear communication"],
                        "why_critical":       h.get("reason", "Critical for current growth stage."),
                    }
                    for h in next_hires
                ],
                "hiring_sequence": [
                    {"order": i + 1, "role": h["role"], "rationale": h.get("reason", "")}
                    for i, h in enumerate(next_hires)
                ],
                "culture_fit_signals": [
                    "Bias for action",
                    "Comfort with ambiguity",
                    "Strong ownership mindset",
                ],
                "onboarding_tips": (
                    "Assign a 30-60-90 day plan with one quick win per phase. "
                    "Pair every new hire with a founder for the first two weeks."
                ),
            }


llm_service = LLMService()