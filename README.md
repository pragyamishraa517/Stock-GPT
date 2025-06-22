Stock-GPT: Stock Sentiment Analyzer

This project uses OpenAI's GPT (GPT-3.5 / GPT-4) and NewsAPI to estimate the **sentiment impact** of news headlines on the stock price of companies. Inspired by real-world sentiment-based prediction research, it helps understand how daily news might affect stock movement.

🚀 How It Works

1. **Input Companies**  
   Add a list of company names in `companies.txt`, one per line.

2. **Fetch News**  
   For each company, the script uses [NewsAPI](https://newsapi.org) to fetch recent headlines.

3. **Analyze Sentiment with GPT**  
   Headlines are analyzed using OpenAI's GPT (via `auth.txt` API key). Each headline gets a score between `-1.0` (very negative) to `+1.0` (very positive).

4. **Generate Reports**  
   - Individual CSV reports for each company are saved in `/Individual_Reports/`
   - A `report.csv` file is generated with mean sentiment score and estimated API usage cost

📁 File Structure

- `sgpt.py` – Main script
- `auth.txt` – Your OpenAI API key (one line)
- `newsapi_key.txt` – Your NewsAPI key (one line)
- `companies.txt` – List of companies to analyze
- `report.csv` – Overall summary output
- `/Individual_Reports/` – Folder with per-company results

🧪 API Limitations (Important)

- **OpenAI Free Tier:** Has limited usage per day/month. Once exhausted, sentiment scoring will not occur, resulting in all scores being `0`.
- **NewsAPI Free Plan:** Sometimes returns no articles for lesser-known companies or due to quota limits.
- ✅ The code handles these gracefully — it skips empty cases without crashing.

⚙️ Setup Instructions

1. Clone or download the repository and extract it.
2. Add your API keys:
   - OpenAI key in `auth.txt`
   - NewsAPI key in `newsapi_key.txt`
3. Install dependencies:
   ```bash
   pip3 install openai requests

4. Run the program:  python3 sgpt.py -t -c


