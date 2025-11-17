ঠিক আছে ভাই। আমি তোমার স্ক্রিপ্ট অনুযায়ী **পুরো `README.md` সম্পূর্ণভাবে Termux / Android-র জন্য professional এবং clean করে লিখে দিলাম**। এতে সব দরকারি তথ্য, installation, usage, output sections, এবং disclaimer আছে।

---

# 🛡️ FCF LINK INFO – Google Document Metadata & Security Analyzer (Termux)

**Developer:** Feni Cyber Force
**Version:** 3.1.1

---

## 📌 Overview

**FCF LINK INFO** হলো একটি advanced Python-based টুল, যা Google Docs / Drive ফাইলের **metadata, owner info, permissions, capabilities** extract করে।
এটি শিক্ষামূলক উদ্দেশ্যে তৈরি করা হয়েছে **digital forensics, security auditing, document analysis** এর জন্য।

---

## 🎯 Key Features

* 🔍 **Advanced Metadata Extraction:** Title, description, size, created/modified date, MIME type, WebView link
* 👑 **Owner Info:** Name, email, Google ID, profile photo
* 🔐 **Permission & Security Analysis:** Public permissions, edit/download/comment capabilities
* 🔑 **Password Pattern Generator:** Owner info থেকে সম্ভাব্য password ideas
* 🖥️ **Beautiful UI + Animation:** ASCII banner, colored output, loading animation
* 🔗 **Auto Social Verification:** Facebook & Telegram links open in correct sequence

---

## ⚙️ Requirements (Termux / Android)

* **Termux app installed**
* **Python:** 3.8+ (Python 3.10+ recommended)
* **Dependencies:** `httpx`, `requests`, `colorama`, `tqdm`

---

## 📦 Installation (Termux / Android)

### 1️⃣ Update Termux packages and install Python & Git

```bash
pkg update && pkg upgrade -y
pkg install python git -y
```

### 2️⃣ Clone repository

```bash
git clone https://github.com/yourrepo/FCF-Link-Info.git
cd FCF-Link-Info
```

### 3️⃣ Create virtual environment (optional but recommended)

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 4️⃣ Install dependencies

```bash
pip install -r requirements.txt
# or individually
pip install httpx requests colorama tqdm
```

### 5️⃣ Install Termux tools for opening social links

```bash
pkg install termux-tools
```

---

## 🚀 Usage

### 1️⃣ Run the script

```bash
python3 fcflinkinfo.py
```

### 2️⃣ Main Menu Options

```
1. 📄 Google Document Analyzer
0. 🚪 Exit
```

### 3️⃣ Enter Google Document URL

* Input any **Google Docs / Drive link**
* Tool automatically extracts metadata, owner info, permissions, and capabilities

---

### 🔹 Example Commands

```bash
# Analyze a document
python3 fcflinkinfo.py
# Enter: https://docs.google.com/document/d/1AbCdEfGhIjkLMNOPqrstuVWXYZ12345

# Exit tool
0
```

---

## 🖼️ Output Sections

1. **BASIC DOCUMENT INFO:** Title, description, size, type, WebView link
2. **DOCUMENT OWNER INFO:** Name, email, Google ID, profile photo
3. **PASSWORD SECURITY ANALYSIS:** Suggested password patterns
4. **PUBLIC PERMISSIONS:** Anyone/domain access roles
5. **DOCUMENT CAPABILITIES:** Can edit/download/comment/rename

> All outputs are **color-coded** for better readability in Termux.

---

## ⚠️ Disclaimer

* Tool is for **educational purposes only**.
* Do not use for **unauthorized access** or **malicious purposes**.
* Developer is **not responsible** for misuse.

---

## 📣 Official Channels

* **Facebook:** [facebook.com/feni_cyber_force_official](https://www.facebook.com/feni_cyber_force_official)
* **Telegram Channel:** [t.me/feni_cyber_force](https://t.me/feni_cyber_force)
* **Helpline Bot:** [@FCF_helping_bot](https://t.me/FCF_helping_bot)

---

## 👨‍💻 Developer

**Feni Cyber Force** – Cybersecurity, Automation & Ethical Analysis Tools

---

## ⭐ Support

* Join the FCF community for updates and new tools
* Feature requests & bug reports: [GitHub Issues](https://github.com/yourrepo/FCF-Link-Info/issues)

---

💡 **Pro Tip:**

* Use `Ctrl + C` to safely exit the tool.
* Ensure Termux has storage permission if working with local downloads.
 
