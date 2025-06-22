# StockGPT
This project uses OpenAI's GPT (GPT-3.5 / GPT-4) and NewsAPI to estimate the **sentiment impact** of news headlines on the stock price of companies. Inspired by real-world sentiment-based prediction research, it helps understand how daily news might affect stock movement.


### Currently Untested!

# DISCLAIMER
Please only use this to see how it correlates to stock movements rather than use it to invest.
it's probably not very good at it anyways.

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

# How to use it
1. If you haven't installed the dependencies already, run, ```pip install -r requirements.txt```
2. If you haven't already, put your OpenAI api token in the file called auth.txt
3. Put a list of companies you want to track in companies.txt
4. Run ```python sgpt.py -h``` to see your options, then run the command as you want.

# Examples
```python sgpt.py -t -c``` gpt-3.5-turbo, sending the headlines in a batch (for minimum cost)

<img width="257" alt="Screen Shot 2023-04-22 at 4 07 07 AM" src="https://user-images.githubusercontent.com/29033313/233757108-6ddd34af-e3df-4bb4-a71c-34519166e785.png">

<img width="239" alt="Screen Shot 2023-04-22 at 4 11 01 AM" src="https://user-images.githubusercontent.com/29033313/233757155-63018c25-6a6f-4f19-ade4-cc0f0a43610c.png">

Stock movements the next day:

<img width="1103" alt="Screen Shot 2023-04-22 at 8 11 42 PM" src="https://user-images.githubusercontent.com/29033313/233800089-d4b72d8c-8bf0-438c-a657-5a6c901dec75.png">



# Full options
```optional arguments:
  -h, --help            show this help message and exit
  -t, --turbo           use gpt-3.5-turbo instead of gpt-4
  -c, --combined        send and receive all the headlines in bulk (cheaper but probabaly less good)
  -T TEMP, --temp TEMP  temperature (variability) of the model. a value between 0.0 and 1.0 (default: 0.3)```
