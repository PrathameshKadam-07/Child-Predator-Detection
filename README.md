# Child Predator Detection Toolkit

This project is a **Sentiment Analysis and OSINT Toolkit** aimed at identifying potential child predators online. It uses a custom keyword-based sentiment analysis engine to flag suspicious language typically used in grooming, exploitation, or harassment.

---

## 🚀 Project Goal

Our ultimate goal is to:

1. Monitor platforms (e.g., Reddit) using their APIs to collect public conversations.
2. Analyze messages using our custom keyword-based sentiment analysis engine.
3. Flag posts/comments with grooming or predatory language.
4. Use OSINT (Open Source Intelligence) techniques to identify potential bad actors for reporting to relevant authorities.

---

## 📚 Current Status

We have completed:

* ✅ Keyword-based sentiment analysis engine using hand-curated grooming and exploitation terms.
* ✅ Interactive CLI tool that accepts user input for analysis.

In progress:

* ⏳ Integration with Reddit API to fetch and analyze messages.
* ⏳ Development of automated OSINT modules to gather public information about flagged users.

---

## ⚙️ How to Use (Sentiment Analysis Only)

### Run from CLI:

```bash
python keyword_sentiment_analysis.py "your text here"
```

### Or run interactively:

```bash
python keyword_sentiment_analysis.py
```

Then enter the message when prompted.

---

## 🔍 What It Detects

The engine scans for:

* Sexual grooming and manipulation
* Explicit or inappropriate content
* Requests for personal info
* Cyberbullying and harassment
* Slang and evasive terms often used to bypass filters

---

## 📊 Output Example

```json
{
  "score": 3,
  "matched_categories": ["Sexual Grooming and Manipulation", "Requests for Personal Information"],
  "matched_keywords": ["Love you", "Send me a pic"]
}
```

## 🔗 Reddit API Integration (Live Monitoring)

This module connects to Reddit using the PRAW (Python Reddit API Wrapper) library. It streams real-time public comments from selected subreddits and uses our custom sentiment analysis engine to flag potentially harmful content.

---

## 🎯 Objective

* Monitor Reddit comments in sensitive subreddits.
* Analyze each comment using the analysis.py sentiment engine.
* Flag and log messages with grooming, bullying, or predatory intent.
* Display author, comment, sentiment score, and permalink.

---

## 🧰 Requirements

Create a Reddit app at https://www.reddit.com/prefs/apps

Collect your:
  * client_id
  * client_secret
  * user_agent

Install the required library:

```bash
pip install praw
```

---

## ✅ How to Run

1) Add your Reddit credentials in reddit_monitor.py.
2)Ensure analysis.py exists and contains the analyze_sentiment function.

Run the monitor:

```bash
python reddit_monitor.py
```

---

## 📊 Example Output

```bash
Suspicious Comment Detected
Author: u/someuser123
Comment: "Hey cutie, wanna play a game? Send me a pic 😉"
Analysis: {'sentiment': 'negative', 'score': -3.4, 'matched_keywords': ['cutie', 'send me a pic']}
Link: https://reddit.com/r/teenagers/comments/abc123/comment/xyz456
```

---

## 📅 Roadmap

* [x] Keyword-driven sentiment detection
* [X] Reddit API integration
* [ ] Suspicious account flagging
* [ ] OSINT automation for flagged accounts
* [ ] Reporting pipeline to legal authorities/NGOs

---

## 💡 Motivation

Online predators often use a pattern of emotionally manipulative and evasive language to target minors. Our system aims to bring transparency and automate early detection before harm is done.

---

## 💼 Disclaimer

This project is for **educational and research purposes only**. We strongly discourage vigilante behavior. Any findings should be responsibly reported to appropriate child protection or law enforcement agencies.This integration processes only public data. Do not engage in unauthorized surveillance or misuse.

---

## 📢 Contributions

We welcome contributions in:

* Expanding the keyword database
* Improving detection algorithms
* Integrating social media APIs
* Building the OSINT pipeline

---

## 🙏 Acknowledgements

This work is inspired by the ongoing efforts of cybersecurity professionals, child protection agencies, and ethical hackers working to create a safer internet.

---

## 📁 Repository Structure

```
.
├── keyword_sentiment_analysis.py
├── reddit_monitor.py
├── keywords.json
├── README.md
```

---
