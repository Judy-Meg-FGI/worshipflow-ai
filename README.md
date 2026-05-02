# LinkedIn Outreach Agent

An AI-powered Gradio app that generates natural, conversation-starting LinkedIn messages tailored to your prospect.

---

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.9+
- An [Anthropic API key](https://console.anthropic.com/)

### 2. Install dependencies

```bash
pip install gradio anthropic
```

### 3. Set your API key

**Mac/Linux:**
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

**Windows (Command Prompt):**
```cmd
set ANTHROPIC_API_KEY=sk-ant-...
```

**Windows (PowerShell):**
```powershell
$env:ANTHROPIC_API_KEY = "sk-ant-..."
```

### 4. Run the app

```bash
python linkedin_outreach_agent.py
```

Then open your browser to: **http://localhost:7860**

---

## 📋 What It Generates

| Message | Description | Length |
|---|---|---|
| **Connection Request Note** | A short, personalized note to send with your LinkedIn connection request | Max 300 chars |
| **First Outreach Message** | A warm intro message after connecting | 3–5 short paragraphs |
| **Follow-Up Message** | A light, non-pushy follow-up if they haven't replied | 2–3 short paragraphs |

---

## 🎛️ Input Fields

| Field | Required | Purpose |
|---|---|---|
| Target Role(s) | ✅ | Who you're reaching out to |
| Industry or Field | ✅ | Their sector/domain |
| Outreach Goal | ✅ | What you want from the conversation |
| Offer Summary | ✅ | What you do or bring to the table |
| Common Ground | ❌ | Shared context or personalization hook |
| Tone | ✅ | Professional / Warm / Confident |
| Message Type | ✅ | Which messages to generate |

---

## 💡 Tips

- **Be specific** — "We help SaaS companies reduce churn" beats "I work in software"
- **Add personalization** — Even a simple hook ("saw your post about X") dramatically improves reply rates
- **Edit before sending** — The output is a strong starting point, not a final draft
- **LinkedIn limits** — Connection notes are capped at 300 characters; the app respects this

---

## 🛠 Tech Stack

- [Gradio](https://gradio.app/) — UI framework
- [Anthropic Claude](https://www.anthropic.com/) — Message generation (claude-sonnet-4)
- Python 3.9+
