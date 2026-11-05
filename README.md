<div align="center">

<!-- HERO BANNER -->
<img src="assets/hero.svg" alt="LinkedIn Auto Apply Bot" width="100%"/>

<a href="https://github.com/Rizwansaifi571/Linkedin-AutoApply-Bot">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=22&pause=1200&color=7C3AED&center=true&vCenter=true&width=720&lines=Automate+LinkedIn+Easy+Apply+%E2%9A%A1;Answers+forms+from+your+own+answer+bank+%F0%9F%A7%A0;Optional+AI+via+Gemini%2C+OpenAI%2C+Ollama+%F0%9F%A4%96;Local-first.+Private.+Reviewable.+%F0%9F%94%92" alt="Typing animation"/>
</a>

<br/>

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Selenium](https://img.shields.io/badge/Selenium-Automation-43B02A?style=for-the-badge&logo=selenium&logoColor=white)](https://www.selenium.dev/)
[![Flask](https://img.shields.io/badge/Flask-Control%20Panel-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![LangChain](https://img.shields.io/badge/LangChain-AI%20Layer-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)](https://www.langchain.com/)
[![License](https://img.shields.io/badge/License-MIT-F59E0B?style=for-the-badge)](LICENSE)

![Stars](https://img.shields.io/github/stars/Rizwansaifi571/Linkedin-AutoApply-Bot?style=for-the-badge&color=EC4899&logo=github)
![Forks](https://img.shields.io/github/forks/Rizwansaifi571/Linkedin-AutoApply-Bot?style=for-the-badge&color=7C3AED&logo=github)
![Issues](https://img.shields.io/github/issues/Rizwansaifi571/Linkedin-AutoApply-Bot?style=for-the-badge&color=0A66C2&logo=github)
![Last commit](https://img.shields.io/github/last-commit/Rizwansaifi571/Linkedin-AutoApply-Bot?style=for-the-badge&color=10B981&logo=git&logoColor=white)

### 🚀 &nbsp;[Quick start](#quick-start) &nbsp;•&nbsp; ✨ [Features](#features) &nbsp;•&nbsp; 🧭 [How it works](#how-it-works) &nbsp;•&nbsp; ⚙️ [Configuration](#configuration) &nbsp;•&nbsp; 🛟 [Troubleshooting](#troubleshooting)

</div>

<br/>

> [!WARNING]
> This tool automates actions in **your** LinkedIn account. Review every setting before you run it, follow LinkedIn's Terms of Service and the law where you live, and remember: you are responsible for your account and every application it sends.

<img src="assets/divider.svg" alt="" width="100%"/>

## <img src="https://fonts.gstatic.com/s/e/notoemoji/latest/2728/512.gif" alt="" width="34" align="center"> Features

<table>
<tr>
<td width="50%" valign="top">

### 🎯 &nbsp;Precision search
Search by title, location, experience level, work setting, salary band, company and posting date. Jobs that don't fit your filters are skipped before they cost you time.

</td>
<td width="50%" valign="top">

### 🧠 &nbsp;Your answer bank
Every Easy Apply question is matched against `question_answers.csv` first. Anything new goes to a **review queue** so you answer it once and never again.

</td>
</tr>
<tr>
<td width="50%" valign="top">

### 🤖 &nbsp;Optional AI help
Plug in **Gemini, OpenAI, DeepSeek, Ollama or LM Studio** for unknown questions, skill extraction and tailored messages. The core flow works with no AI at all.

</td>
<td width="50%" valign="top">

### 🛡️ &nbsp;Smart filters
Skip jobs by bad words, security-clearance wording, experience requirements and visa-sponsorship language. Whole-word matching, so "Java" never skips "JavaScript".

</td>
</tr>
<tr>
<td width="50%" valign="top">

### 🖥️ &nbsp;Local control panel
A Flask panel on `127.0.0.1` for your profile, search, filters, run settings and application history. No cloud, no account.

</td>
<td width="50%" valign="top">

### 📊 &nbsp;Readable history
Applied jobs, failed applications and questions to review land in plain CSV files, with logs and screenshots for every failure.

</td>
</tr>
<tr>
<td width="50%" valign="top">

### ⏱️ &nbsp;Limit-aware
Detects LinkedIn's daily Easy Apply limit and stops cleanly instead of hammering the site.

</td>
<td width="50%" valign="top">

### 🚀 &nbsp;Y Combinator bot
Includes `runYCBot.py` for Y Combinator job applications, with AI-written messages and automatic template fallback.

</td>
</tr>
</table>

<img src="assets/divider.svg" alt="" width="100%"/>

## <img src="https://fonts.gstatic.com/s/e/notoemoji/latest/1f680/512.gif" alt="" width="34" align="center"> Quick start

### 1️⃣ &nbsp;Prerequisites

| | Requirement |
|---|---|
| 🐍 | Python **3.10** or newer |
| 🌐 | Google Chrome (the matching driver is managed for you) |
| 💼 | A LinkedIn account |

### 2️⃣ &nbsp;Launch the control panel

The launcher creates a private virtual environment, installs everything and opens the panel in your browser.

<details open>
<summary><b>🪟 &nbsp;Windows</b></summary>

<br/>

Double-click [`start.bat`](start.bat), or run:

```powershell
./start.bat
```

</details>

<details>
<summary><b>🍎 &nbsp;macOS</b></summary>

<br/>

```bash
chmod +x start.command
./start.command
```

</details>

<details>
<summary><b>🐧 &nbsp;Linux</b></summary>

<br/>

```bash
chmod +x start.sh
./start.sh
```

</details>

### 3️⃣ &nbsp;Set it up in five tabs

| Step | Tab | What you do |
|:---:|---|---|
| 🔑 | **Account** | Optional LinkedIn login and optional AI provider |
| 👤 | **Profile** | Name, phone, work authorization, salary, notice period, resume |
| 🔍 | **Search** | Titles, location, experience, job type, work setting |
| 🧹 | **Filters** | Companies and description terms to include or skip |
| ⚙️ | **Run settings** | Conservative limits and review behaviour |

> [!TIP]
> Start with a **narrow search** and a **low application limit**. Turn on `stop_before_submit` for a review-only run, check what the bot filled in, then switch it off.

<img src="assets/divider.svg" alt="" width="100%"/>

## <img src="https://fonts.gstatic.com/s/e/notoemoji/latest/1f9ed/512.gif" alt="" width="34" align="center"> How it works

<div align="center">

<img src="assets/pipeline.svg" alt="Configure, Search, Filter, Easy Apply, Answer, Submit and log" width="100%"/>

</div>

<details open>
<summary><b>🗺️ &nbsp;Full decision flow</b></summary>

```mermaid
%%{init: {'theme':'base','themeVariables':{'primaryColor':'#EEF2FF','primaryTextColor':'#1E1B4B','primaryBorderColor':'#7C3AED','lineColor':'#7C3AED','secondaryColor':'#FDF2F8','tertiaryColor':'#ECFDF5','fontFamily':'Inter, Segoe UI, sans-serif'}}}%%
flowchart LR
    A([⚙️ Configure locally]) --> B[🔍 Search LinkedIn]
    B --> C{🧹 Matches<br/>filters?}
    C -- No --> D[⏭️ Skip & continue]
    C -- Yes --> E[⚡ Open Easy Apply]
    E --> F{🧠 Question<br/>known?}
    F -- Yes --> G[✍️ Fill from answer bank]
    F -- No --> H{🤖 AI on?}
    H -- Yes --> I[💡 Ask AI]
    H -- No --> J[📝 Save for review]
    G --> K[👀 Review application]
    I --> K
    J --> K
    K --> L([✅ Submit or stop before submit])
    L --> M[(📊 History & logs)]

    style A fill:#0A66C2,color:#fff,stroke:#0A66C2
    style L fill:#10B981,color:#fff,stroke:#10B981
    style M fill:#7C3AED,color:#fff,stroke:#7C3AED
    style D fill:#F3F4F6,stroke:#9CA3AF
    style J fill:#FEF3C7,stroke:#F59E0B
```

</details>

<details>
<summary><b>🔎 &nbsp;What happens to a single job</b></summary>

<br/>

1. The bot opens the job card and waits for the details pane, then reads the **About the job** text.
2. Filters run: blacklisted companies, bad words, clearance wording, experience and sponsorship language.
3. If the job passes, it opens **Easy Apply** and walks the form step by step.
4. Each question is answered from the **answer bank**, then (optionally) AI, then a safe fallback. Anything it cannot answer honestly is left alone and written to the review queue.
5. The outcome is saved to your history CSVs, with a screenshot on failure.

</details>

<img src="assets/divider.svg" alt="" width="100%"/>

## <img src="https://fonts.gstatic.com/s/e/notoemoji/latest/1f527/512.gif" alt="" width="34" align="center"> Configuration

The browser panel is the easiest path. It writes to `user_config.json` and overlays the defaults in `config/`, so the shipped files stay untouched.

| 📁 Area | 📖 Guide |
|---|---|
| Installation & manual launch | [`docs/install.md`](docs/install.md) |
| How configuration works | [`docs/configuration.md`](docs/configuration.md) |
| Personal details | [`docs/config-personals.md`](docs/config-personals.md) |
| Application answers | [`docs/config-questions.md`](docs/config-questions.md) |
| Search & filters | [`docs/config-search.md`](docs/config-search.md) |
| LinkedIn & AI credentials | [`docs/config-secrets.md`](docs/config-secrets.md) |
| Runtime behaviour | [`docs/config-settings.md`](docs/config-settings.md) |

<details>
<summary><b>📄 &nbsp;Resume setup</b></summary>

<br/>

Put your PDF inside the project:

```text
all resumes/default/resume.pdf
```

Then point to it in the panel, or in the config:

```python
default_resume_path = "all resumes/default/resume.pdf"
```

</details>

<details>
<summary><b>🤖 &nbsp;Optional AI setup</b></summary>

<br/>

| Provider | Notes |
|---|---|
| 🔷 **Gemini** | Cloud, needs an API key |
| 🟢 **OpenAI** | Cloud, needs an API key |
| 🐋 **DeepSeek** | OpenAI-compatible endpoint |
| 🦙 **Ollama / LM Studio** | Fully local, no key needed |

Turn on **Use AI** only after choosing a provider and model. If the provider is unavailable, the bot falls back to your answer bank and safe defaults for the rest of the run.

> [!CAUTION]
> Never commit API keys or share `user_config.json` when it contains secrets. It is git-ignored for exactly that reason.

</details>

<img src="assets/divider.svg" alt="" width="100%"/>

## <img src="https://fonts.gstatic.com/s/e/notoemoji/latest/1f4ca/512.gif" alt="" width="34" align="center"> Outputs

| 📂 File | 🧾 What it holds |
|---|---|
| `all excels/all_applied_applications_history.csv` | Applications the bot completed |
| `all excels/all_failed_applications_history.csv` | Applications that could not be completed |
| `all excels/questions_to_review.csv` | New questions waiting for your answer |
| `all excels/question_answers.csv` | Your reusable answer bank |
| `logs/` | Run logs and failure screenshots |

> [!NOTE]
> These folders are git-ignored, so your history, answers and logs never leave your machine.

### 🔁 The answer-bank loop

```mermaid
%%{init: {'theme':'base','themeVariables':{'primaryColor':'#FDF2F8','primaryBorderColor':'#EC4899','lineColor':'#EC4899','fontFamily':'Inter, Segoe UI, sans-serif'}}}%%
flowchart LR
    Q[❓ New question] --> R[(📝 questions_to_review.csv)]
    R --> Y[🧑 You write the ideal answer]
    Y --> B[(🧠 question_answers.csv)]
    B --> N[🔁 Next run answers it automatically]
```

<img src="assets/divider.svg" alt="" width="100%"/>

## <img src="https://fonts.gstatic.com/s/e/notoemoji/latest/1f512/512.gif" alt="" width="34" align="center"> Safety &amp; boundaries

- 🔒 **Local only.** The control panel binds to `127.0.0.1`; nothing is uploaded unless you enable an AI provider.
- 👀 **You stay in charge.** Use `stop_before_submit` to review before anything is sent.
- ⚖️ **Honest answers.** Attestations, consent boxes and legal questions are never ticked by guesswork.
- 🚫 **No promises.** The tool cannot guarantee quality, eligibility, interviews or offers. Don't delegate legal, immigration, salary or identity decisions to automation.
- 🤝 **Be a good citizen.** Respect LinkedIn's rules and rate limits.

<img src="assets/divider.svg" alt="" width="100%"/>

## <img src="https://fonts.gstatic.com/s/e/notoemoji/latest/1f6df/512.gif" alt="" width="34" align="center"> Troubleshooting

<details>
<summary><b>🖥️ &nbsp;The panel does not open</b></summary>

<br/>

Run `python app.py` from the project folder and open the URL printed in the terminal. If the port is busy, the app picks another one.

</details>

<details>
<summary><b>🌐 &nbsp;Chrome or the driver fails</b></summary>

<br/>

Make sure Google Chrome is installed and up to date. The matching driver is managed automatically. See [`docs/install.md`](docs/install.md) for manual driver settings.

</details>

<details>
<summary><b>⏭️ &nbsp;Jobs are being skipped</b></summary>

<br/>

Check the run log, then open `all excels/questions_to_review.csv`. Add the missing answers to the answer bank, or loosen the matching filter, and run again.

</details>

<details>
<summary><b>🧪 &nbsp;I want to test without submitting</b></summary>

<br/>

Enable `stop_before_submit`, use a small search, and inspect the filled-in application before turning it off.

</details>

<details>
<summary><b>⏱️ &nbsp;The bot stopped by itself</b></summary>

<br/>

LinkedIn caps Easy Apply per day. When it shows the limit dialog the bot stops cleanly. Run again the next day.

</details>

<img src="assets/divider.svg" alt="" width="100%"/>

## <img src="https://fonts.gstatic.com/s/e/notoemoji/latest/1f4bb/512.gif" alt="" width="34" align="center"> Manual launch

```bash
python -m venv .venv

# Windows PowerShell
.venv\Scripts\Activate.ps1

# macOS / Linux
# source .venv/bin/activate

python -m pip install -r requirements.txt
python app.py          # control panel
python runAiBot.py     # classic bot entry point
```

<img src="assets/divider.svg" alt="" width="100%"/>

## <img src="https://fonts.gstatic.com/s/e/notoemoji/latest/1f9f1/512.gif" alt="" width="34" align="center"> Tech stack

<div align="center">

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Selenium](https://img.shields.io/badge/Selenium-43B02A?style=flat-square&logo=selenium&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=flat-square&logo=flask&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=flat-square&logo=langchain&logoColor=white)
![LangGraph](https://img.shields.io/badge/LangGraph-7C3AED?style=flat-square)
![Gemini](https://img.shields.io/badge/Gemini-8E75B2?style=flat-square&logo=googlegemini&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=flat-square&logo=openai&logoColor=white)
![Chrome](https://img.shields.io/badge/Chrome-4285F4?style=flat-square&logo=googlechrome&logoColor=white)

</div>

<img src="assets/divider.svg" alt="" width="100%"/>

## <img src="https://fonts.gstatic.com/s/e/notoemoji/latest/1f91d/512.gif" alt="" width="34" align="center"> Contributing

Bug reports, doc fixes and focused pull requests are welcome. Start with [`CONTRIBUTING.md`](CONTRIBUTING.md), keep changes small, and never include credentials, private resumes or application history.

## <img src="https://fonts.gstatic.com/s/e/notoemoji/latest/1f4dc/512.gif" alt="" width="34" align="center"> License

Released under the [MIT License](LICENSE). Read the [disclaimer and terms](docs/legal.md) before you use the tool. Need help? See [`docs/support.md`](docs/support.md).

<img src="assets/divider.svg" alt="" width="100%"/>

<div align="center">

### 👨‍💻 Built by **Mohd Rizwan**

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Mohd%20Rizwan-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/rizwansaifi2614/)
[![GitHub](https://img.shields.io/badge/GitHub-Rizwansaifi571-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Rizwansaifi571)
[![Portfolio](https://img.shields.io/badge/Portfolio-rizwansaifi571.github.io-EC4899?style=for-the-badge&logo=googlechrome&logoColor=white)](https://rizwansaifi571.github.io/)

<a href="https://github.com/Rizwansaifi571"><img src="https://github-readme-stats.vercel.app/api?username=Rizwansaifi571&show_icons=true&theme=radical&hide_border=true&border_radius=16" alt="GitHub stats" height="165"/></a>
<a href="https://github.com/Rizwansaifi571"><img src="https://github-readme-streak-stats.herokuapp.com/?user=Rizwansaifi571&theme=radical&hide_border=true&border_radius=16" alt="GitHub streak" height="165"/></a>

⭐ **If this saved you time, drop a star. It really helps!** ⭐

<img src="assets/footer.svg" alt="" width="100%"/>

</div>
