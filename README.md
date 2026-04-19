# 🏋️ Automated Gym Booking Bot

A Python-based browser automation script that automatically books gym classes on the [App Brewery Gym](https://appbrewery.github.io/gym/) demo platform. Built using Selenium WebDriver, it logs in, finds target classes by day and time, books or joins waitlists, and then verifies all bookings on the "My Bookings" page.

---

## 🚀 Features

- Automatically logs into the gym booking platform
- Filters classes by specific days (**Wednesday & Thursday**) and time (**6:00 PM**)
- Books available slots or joins the waitlist if fully booked
- Skips classes already booked or waitlisted
- Verifies bookings on the "My Bookings" page and reports success/mismatch
- Retry logic to handle slow page loads and timing issues

---

## 🛠️ Tech Stack

- **Python 3**
- **Selenium** – Browser automation
- **WebDriver Manager** – Auto-manages ChromeDriver installation

---

## 📦 Installation

1. **Clone the repository**
```bash
   git clone https://github.com/Roboig/Automated_Gym_Booking.git
   cd Automated_Gym_Booking
```

2. **Install dependencies**
```bash
   pip install selenium webdriver-manager
```

3. **Configure credentials**

   Open `main.py` and update the following variables with your account details:
```python
   ACCOUNT_EMAIL = "your_email@example.com"
   ACCOUNT_PASSWORD = "your_password"
```

---

## ▶️ Usage

Run the script with:

```bash
python main.py
```

The script will:
1. Open Chrome and navigate to the gym booking site
2. Log in with the provided credentials
3. Scan all class cards for Wednesday/Thursday 6:00 PM slots
4. Book, waitlist, or skip each class as appropriate
5. Navigate to "My Bookings" and verify all expected bookings are present

---

## 📋 Output Example

<img width="1851" height="840" alt="Screenshot 2026-04-19 143006" src="https://github.com/user-attachments/assets/95e02e15-5e81-47d4-9960-9b6409a55a32" />
<img width="1853" height="882" alt="Screenshot 2026-04-19 143017" src="https://github.com/user-attachments/assets/f646a31c-87ef-45b3-90b4-6bf619648ef3" />
<img width="1847" height="906" alt="image" src="https://github.com/user-attachments/assets/b464c352-48a5-4e72-a739-76317aff9e44" />

---

## ⚠️ Notes

- A persistent Chrome profile is saved locally in a `chrome_profile/` folder to preserve session data between runs.
- The script targets the [App Brewery Gym](https://appbrewery.github.io/gym/) demo site. To adapt it for a real gym website, update the URL and element selectors accordingly.
- Hardcoded credentials are included for demo purposes — **do not commit real credentials to a public repository**. Consider using environment variables or a `.env` file instead.

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

