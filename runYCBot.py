'''
Work at a Startup (Y Combinator) auto-applier.

Flow, per search term:
  1. open workatastartup.com/companies with the configured filters + ?query=<term>
  2. collect every "View job" link in the results list
  3. open each job, read the description, write a personalised message with the AI
  4. click Apply, fill the "Reach out to ..." box, click Send
  5. go on to the next job

Run it:   python runYCBot.py
You must be logged in to workatastartup.com in the Chrome profile the bot opens. If you are
not, the bot waits for you to log in (up to YC_LOGIN_WAIT_SECONDS) and then carries on.
'''

import csv
import os
import re
import time
from datetime import datetime
from random import uniform, shuffle
from urllib.parse import urlencode, urljoin, urlparse

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import WebDriverException

from config.personals import first_name, last_name
from config.questions import (user_information_all, linkedin_summary, years_of_experience,
                              require_visa, legally_authorized, desired_salary, notice_period)
from config.search import bad_words
from config.secrets import use_AI

from modules.open_chrome import driver
from modules.helpers import print_lg, make_directories

if use_AI:
    from modules.ai.connections import create_ai_client, close_ai_client, answer_question, _msg_text, _with_deadline


#< Settings
YC_SEARCH_TERMS = ["Software Engineer", "Software Developer", "Full Stack Developer", "Backend Engineer",
                   "Python Developer", "React Developer", "AI Engineer", "Machine Learning Engineer"]
YC_RANDOMIZE_ORDER = False
YC_APPLICATIONS_PER_TERM = 30       # messages to send for each search term, then move to the next term
YC_MAX_JOBS_PER_TERM = 150          # "View job" links to collect per term; skipped/already-applied ones don't count toward the 30
YC_OPEN_TO_RELOCATE = True          # tick the "I'm open to relocating" box when YC shows it
YC_LOGIN_WAIT_SECONDS = 300
YC_DRY_RUN = False                  # True = write the message but do NOT click Send
YC_APPLIED_FILE = "all excels/yc_applied_jobs.csv"

# Same filters as the manual search; only `query` changes per term.
YC_FILTERS = [
    ("demographic", "any"), ("hasEquity", "any"), ("hasSalary", "any"), ("industry", "any"),
    ("interviewProcess", "any"), ("jobType", "fulltime"), ("jobType", "intern"),
    ("layout", "list-compact"), ("remote", "yes"), ("role", "eng"),
    ("role_type", "ai"), ("role_type", "be"), ("role_type", "data_sci"), ("role_type", "fs"),
    ("role_type", "ml"), ("sortBy", "keyword"), ("tab", "any"), ("usVisaNotRequired", "any"),
]
YC_BASE = "https://www.workatastartup.com"
#>


FALLBACK_MESSAGE = (
    "Hi! I'm {name}, a software engineer with {years}+ years of experience building and shipping "
    "full stack and backend systems in Python, React and Node.js. The {title} role at {company} "
    "looks like a strong fit for my background, and I'd love to talk about how I can help the team. "
    "Thanks for your time!"
)

MESSAGE_PROMPT = """Write the short message a candidate sends to a startup founder when applying on Y Combinator's Work at a Startup.

Rules:
- 60 to 110 words, plain text, no markdown, no subject line, no placeholders like [Name].
- First person, warm, direct, human. Do not open with "I hope this email finds you well".
- Mention one or two specific things from the company/role description that genuinely interest the candidate.
- Connect them to 2-3 concrete skills or experiences from the candidate profile. Never invent employers, degrees or numbers that are not in the profile.
- End with a simple invitation to chat.
- Output ONLY the message text.

Candidate name: {name}
Candidate profile:
{profile}

Job title: {title}
Company: {company}

Job posting:
{description}
"""


# A timed-out AI call costs 45s, so after one failure stay on templates for a while.
AI_COOLDOWN_SECONDS = 300
ai_down_until = [0.0]


class RateLimited(Exception):
    """Work at a Startup is refusing us (too many requests/messages). The run stops at once."""


RATE_LIMIT_RE = re.compile(
    r"rate.?limit|too many (?:requests|applications|messages|attempts)|slow down|"
    r"(?:limit|quota) (?:has been )?(?:reached|exceeded)|daily (?:application |message )?limit|"
    r"try again (?:later|tomorrow)|temporarily (?:blocked|restricted)", re.I)


def check_rate_limit() -> None:
    """Raise RateLimited when the page, or a dialog/alert/toast on it, reports a rate limit.

    Only short, UI-sized text is checked (an error page, a dialog, a toast), never a whole job
    description, so a posting that merely mentions "rate limiting" can't stop the run.
    """
    try:
        texts = [driver.title or ""]
        for element in driver.find_elements(By.XPATH, "//*[@role='alert' or @role='dialog' or @role='status' or contains(@class,'toast') or contains(@class,'Toastify') or contains(@class,'error')]"):
            try:
                if element.is_displayed():
                    texts.append(element.text or "")
            except WebDriverException:
                continue
        body = driver.find_element(By.TAG_NAME, "body").text
        if len(body) < 700:             # an error page has almost no text
            texts.append(body)
    except WebDriverException:
        return
    for text in texts:
        if text and len(text) < 1500 and RATE_LIMIT_RE.search(text):
            raise RateLimited(re.sub(r"\s+", " ", text).strip()[:200])


def pause(low: float = 1.0, high: float = 2.5) -> None:
    time.sleep(uniform(low, high))


def search_url(term: str) -> str:
    return f"{YC_BASE}/companies?" + urlencode(YC_FILTERS + [("query", term)])


def job_id(url: str) -> str:
    '''Stable id for a job link: the last path segment, e.g. /jobs/12345-senior-engineer -> 12345-senior-engineer.'''
    return urlparse(url).path.rstrip("/").split("/")[-1]


def load_applied() -> set[str]:
    if not os.path.exists(YC_APPLIED_FILE):
        return set()
    with open(YC_APPLIED_FILE, newline="", encoding="utf-8") as f:
        return {row["job_id"] for row in csv.DictReader(f) if row.get("job_id")}


def log_job(jid: str, url: str, title: str, company: str, status: str, message: str) -> None:
    new_file = not os.path.exists(YC_APPLIED_FILE)
    with open(YC_APPLIED_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if new_file:
            writer.writerow(["job_id", "time", "company", "title", "status", "url", "message"])
        writer.writerow([jid, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), company, title, status, url, message])


def is_logged_in() -> bool:
    '''Logged-out pages show a "Log in" / "Sign up" link in the header; logged-in ones show a profile menu.'''
    try:
        links = driver.find_elements(By.XPATH, "//a[normalize-space()='Log in' or normalize-space()='Sign up' or normalize-space()='Log In']")
        return not any(link.is_displayed() for link in links)
    except WebDriverException:
        return False


def ensure_login() -> None:
    driver.get(f"{YC_BASE}/companies")
    pause(3, 4)
    deadline = time.time() + YC_LOGIN_WAIT_SECONDS
    announced = False
    while not is_logged_in():
        if not announced:
            print_lg("Not logged in to Work at a Startup. Please log in in the browser window, the bot continues by itself.")
            announced = True
        if time.time() > deadline:
            raise SystemExit("Gave up waiting for the Work at a Startup login.")
        time.sleep(3)


def collect_job_links(limit: int) -> list[str]:
    '''Scroll the results list until `limit` "View job" links are loaded, or no more appear.'''
    links: dict[str, str] = {}
    stale_rounds = 0
    while len(links) < limit and stale_rounds < 3:
        before = len(links)
        for anchor in driver.find_elements(By.XPATH, "//a[normalize-space()='View job' or contains(@href,'/jobs/')]"):
            try:
                href = anchor.get_attribute("href") or ""
            except WebDriverException:
                continue
            if "/jobs/" in href:
                links.setdefault(job_id(href), urljoin(YC_BASE, href))
        stale_rounds = stale_rounds + 1 if len(links) == before else 0
        driver.execute_script("window.scrollBy(0, document.body.scrollHeight);")
        # The results can sit in their own scroll container, so scroll the last link into view too.
        try:
            driver.execute_script("arguments[0].scrollIntoView();", driver.find_elements(By.XPATH, "//a[contains(@href,'/jobs/')]")[-1])
        except (IndexError, WebDriverException):
            pass
        pause(1.2, 2.0)
    return list(links.values())[:limit]


def read_job() -> tuple[str, str, str]:
    '''Return (title, company, description text) of the open job page.'''
    heading = ""
    try:
        heading = driver.find_element(By.XPATH, "//h1").text.strip()
    except WebDriverException:
        pass
    title, company = heading, ""
    match = re.match(r"(.+?)\s+at\s+(.+?)(?:\s*\(\w+\d*\))?$", heading)
    if match:
        title, company = match.group(1).strip(), match.group(2).strip()
    body = driver.find_element(By.TAG_NAME, "body").text
    return title, company, body[:7000]


def banned_word(description: str) -> str | None:
    low = description.lower()
    for word in bad_words:
        if re.search(r"(?<!\w)" + re.escape(word.lower()) + r"(?!\w)", low):
            return word
    return None


def write_message(client, title: str, company: str, description: str) -> str:
    name = f"{first_name.strip()} {last_name.strip()}".strip()
    fallback = FALLBACK_MESSAGE.format(name=name, years=years_of_experience, title=title or "engineering", company=company or "your team")
    if not client or time.time() < ai_down_until[0]:
        return fallback
    profile = (user_information_all.strip() + "\n" + linkedin_summary.strip()).strip()
    prompt = MESSAGE_PROMPT.format(name=name, profile=profile, title=title, company=company, description=description)
    try:
        text = _msg_text(_with_deadline(client.model.invoke, prompt)).strip().strip('"')
    except Exception as e:
        print_lg(f"AI message failed ({type(e).__name__}), using the template instead. Skipping AI for {AI_COOLDOWN_SECONDS}s.")
        ai_down_until[0] = time.time() + AI_COOLDOWN_SECONDS
        return fallback
    return text if len(text) >= 50 else fallback


def click(element) -> None:
    try:
        element.click()
    except WebDriverException:
        driver.execute_script("arguments[0].click();", element)


def first_displayed(xpath: str):
    for element in driver.find_elements(By.XPATH, xpath):
        try:
            if element.is_displayed():
                return element
        except WebDriverException:
            continue
    return None


def wait_displayed(xpath: str, seconds: float = 10):
    end = time.time() + seconds
    while time.time() < end:
        element = first_displayed(xpath)
        if element:
            return element
        time.sleep(0.4)
    return None


READ_FIELDS_JS = """
const root = document.querySelector('[role="dialog"]') || document.querySelector('[class*="modal" i]') || document.body;
const strip = (node) => { const c = node.cloneNode(true); c.querySelectorAll('textarea,input,select,button').forEach(x => x.remove()); return c.innerText.trim(); };
const labelOf = (el) => {
  const aria = el.getAttribute('aria-label'); if (aria) return aria.trim();
  if (el.id) { const l = root.querySelector('label[for="' + CSS.escape(el.id) + '"]'); if (l && l.innerText.trim()) return l.innerText.trim(); }
  let node = el;
  for (let i = 0; i < 5 && node.parentElement && node.parentElement !== root; i++) {
    node = node.parentElement;
    const t = strip(node); if (t) return t.slice(0, 400);
  }
  return (el.getAttribute('placeholder') || '').trim();
};
const optionText = (r) => {
  if (r.id) { const l = root.querySelector('label[for="' + CSS.escape(r.id) + '"]'); if (l) return l.innerText.trim(); }
  const l = r.closest('label'); if (l) return l.innerText.trim();
  return ((r.parentElement && r.parentElement.innerText) || '').trim();
};
const out = [];
root.querySelectorAll('textarea, input, select').forEach(el => {
  const type = el.tagName === 'INPUT' ? (el.type || 'text').toLowerCase() : el.tagName.toLowerCase();
  if (['hidden', 'submit', 'button', 'file', 'radio'].includes(type)) return;
  if (!(el.offsetWidth || el.offsetHeight || el.getClientRects().length)) return;
  const item = { kind: type, label: labelOf(el), options: [], els: [el] };
  if (type === 'select') item.options = Array.from(el.options).map(o => o.text.trim()).filter(Boolean);
  out.push(item);
});
const groups = {};
root.querySelectorAll('input[type=radio]').forEach(r => { (groups[r.name || r.id] = groups[r.name || r.id] || []).push(r); });
Object.values(groups).forEach(rs => {
  let node = rs[0].parentElement;
  while (node && node !== root && !rs.every(r => node.contains(r))) node = node.parentElement;
  let label = node ? strip(node) : '';
  const options = rs.map(optionText);
  options.forEach(o => { label = label.split(o).join(''); });
  out.push({ kind: 'radio', label: label.trim().slice(0, 400), options: options, els: rs });
});
return { text: root.innerText.slice(0, 3000), fields: out };
"""


def fallback_answer(label: str) -> str:
    '''Answers from config for the common questions, used when the AI is down or gave nothing.'''
    low = label.lower()
    if re.search(r"sponsor|visa", low):
        return require_visa
    if re.search(r"authori[sz]ed|eligible to work|legally|right to work", low):
        return legally_authorized
    if re.search(r"salary|compensation|ctc|expect", low):
        return str(desired_salary)
    if re.search(r"notice", low):
        return str(notice_period)
    if re.search(r"year|experience", low):
        return str(years_of_experience)
    if re.search(r"relocat|remote|on-?site|commute|available|willing|comfortable", low):
        return "Yes"
    return ""


def pick_option(answer: str, options: list[str]) -> int | None:
    '''Index of the option that best matches `answer`, or None.'''
    norm = lambda t: re.sub(r"\s+", " ", t.strip().lower())
    a = norm(answer)
    for i, o in enumerate(options):
        if norm(o) == a:
            return i
    for i, o in enumerate(options):
        if a and (a in norm(o) or norm(o) in a):
            return i
    return None


def fill_field(field: dict, answer: str) -> bool:
    kind, els = field["kind"], field["els"]
    try:
        if kind == "radio":
            i = pick_option(answer, field["options"])
            if i is None:
                return False
            driver.execute_script("arguments[0].click();", els[i])
            return True
        if kind == "select":
            i = pick_option(answer, field["options"])
            if i is None:
                return False
            Select(els[0]).select_by_visible_text(field["options"][i])
            return True
        if kind == "checkbox":
            if not els[0].is_selected():
                click(els[0])
            return True
        els[0].click()
        els[0].send_keys(Keys.CONTROL, "a")
        els[0].send_keys(Keys.DELETE)
        els[0].send_keys(answer)
        return True
    except WebDriverException:
        return False


def answer_field(client, field: dict, title: str, company: str, description: str) -> str:
    label = re.sub(r"\s+", " ", field["label"]).strip()
    options = field["options"]
    answer = ""
    if client and time.time() >= ai_down_until[0]:
        qtype = "single_select" if options else "text"
        answer = answer_question(client, label, options or None, qtype, description,
                                 f"{company} - {title}", user_information_all)
    return (answer or fallback_answer(label)).strip()


def apply_with_message(client, message: str, title: str, company: str, description: str) -> tuple[str, str]:
    '''Click Apply, fill every field the dialog shows, Send.

    The dialog is not always the same: besides the "Reach out to ..." message it can ask extra
    questions (text, select, radio, checkbox), and how many differs per job. Returns
    (status, notes): status is "applied", "dry-run", "already-applied" or "failed: why", notes
    lists each question with the answer given.
    '''
    apply_button = wait_displayed("//a[normalize-space()='Apply'] | //button[normalize-space()='Apply']", 6)
    if not apply_button:
        if first_displayed("//*[normalize-space()='Applied' or contains(normalize-space(),'You applied')]"):
            return "already-applied", ""
        return "failed: no Apply button", ""
    handles = set(driver.window_handles)
    click(apply_button)
    pause(1.5, 2.5)
    check_rate_limit()
    # If Apply opened a new tab, work in it and close it afterwards.
    new_tabs = [h for h in driver.window_handles if h not in handles]
    origin = driver.current_window_handle
    if new_tabs:
        driver.switch_to.window(new_tabs[0])
    notes: list[str] = []
    try:
        if not wait_displayed("//textarea | //input[@type='text'] | //select", 10):
            return "failed: application dialog did not open", ""
        pause(0.8, 1.2)
        dialog = driver.execute_script(READ_FIELDS_JS)
        is_reach_out = "reach out" in dialog["text"].lower()
        message_done = False
        for field in dialog["fields"]:
            label = re.sub(r"\s+", " ", field["label"]).strip()
            if field["kind"] == "checkbox":
                if YC_OPEN_TO_RELOCATE or re.search(r"agree|acknowledge|confirm", label.lower()):
                    fill_field(field, "")
                continue
            if field["kind"] == "textarea" and is_reach_out and not message_done:
                fill_field(field, message)
                message_done = True
                continue
            answer = answer_field(client, field, title, company, description)
            ok = bool(answer) and fill_field(field, answer)
            notes.append(f"Q: {label[:150]} | A: {answer if ok else '(unanswered)'}")
            print_lg(notes[-1])
        pause(0.8, 1.5)
        joined = "\n".join(notes)
        if YC_DRY_RUN:
            print_lg("[dry run] fields filled, not sending.")
            return "dry-run", joined
        send = wait_displayed("//button[normalize-space()='Send' or normalize-space()='Submit' or normalize-space()='Submit application']", 5)
        if not send:
            return "failed: no Send button", joined
        click(send)
        pause(2.5, 3.5)
        check_rate_limit()
        if first_displayed("//textarea | //select | //input[@type='text']"):
            return "failed: dialog still open after Send (a required field is missing or invalid)", joined
        return "applied", joined
    finally:
        if new_tabs:
            try:
                driver.close()
            except WebDriverException:
                pass
            driver.switch_to.window(origin)


def close_dialog() -> None:
    '''Dismiss a leftover message dialog so the next job starts clean.'''
    close = first_displayed("//button[normalize-space()='Close']")
    if close:
        click(close)
        pause(0.5, 1)


def run() -> None:
    make_directories([YC_APPLIED_FILE])
    client = create_ai_client() if use_AI else None
    applied = load_applied()
    sent = [0]      # a list so run_terms can update it and a rate-limit exit still reports the count

    ensure_login()
    terms = list(YC_SEARCH_TERMS)
    if YC_RANDOMIZE_ORDER:
        shuffle(terms)

    try:
        run_terms(client, terms, applied, sent)
    except RateLimited as e:
        print_lg(f"\nRATE LIMITED by Work at a Startup: {e}")
        print_lg("Stopping now so the account is not pushed further. Try again later (hours, or tomorrow).")
    print_lg(f"\nDone. Messages sent this run: {sent[0]}. Log: {YC_APPLIED_FILE}")
    if client:
        close_ai_client(client)


def run_terms(client, terms, applied, sent) -> None:
    for term in terms:
        term_sent = 0
        print_lg(f'\n=== Searching Work at a Startup for "{term}" ===')
        driver.get(search_url(term))
        pause(3, 4.5)
        check_rate_limit()
        links = collect_job_links(YC_MAX_JOBS_PER_TERM)
        print_lg(f"Found {len(links)} jobs.")

        for url in links:
            if term_sent >= YC_APPLICATIONS_PER_TERM:
                print_lg(f'Sent {term_sent} messages for "{term}", moving to the next term.')
                break
            jid = job_id(url)
            if jid in applied:
                print_lg(f"Already handled {jid}, skipping.")
                continue
            try:
                driver.get(url)
                pause(2, 3.5)
                check_rate_limit()
                title, company, description = read_job()
                print_lg(f"\n{title} @ {company}  ({url})")

                bad = banned_word(description)
                if bad:
                    print_lg(f'Skipping, description contains "{bad}".')
                    log_job(jid, url, title, company, f"skipped: {bad}", "")
                    applied.add(jid)
                    continue

                message = write_message(client, title, company, description)
                print_lg(f"Message:\n{message}")
                status, notes = apply_with_message(client, message, title, company, description)
                if notes:
                    message = f"{message}\n\n{notes}"
                print_lg(f"Result: {status}")
                if status in ("applied", "already-applied"):
                    applied.add(jid)
                    if status == "applied":
                        sent[0] += 1
                        term_sent += 1
                    log_job(jid, url, title, company, status, message)
                elif status == "dry-run":
                    term_sent += 1
                    close_dialog()
                else:
                    close_dialog()
                    log_job(jid, url, title, company, status, message)
                    applied.add(jid)
            except WebDriverException as e:
                print_lg(f"Browser error on {url}: {type(e).__name__}. Moving on.")
                try:
                    close_dialog()
                except WebDriverException:
                    pass
            pause(2, 4)


if __name__ == "__main__":
    try:
        run()
    finally:
        try:
            driver.quit()
        except Exception:
            pass
