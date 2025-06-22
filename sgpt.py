import csv, re, os, argparse, requests
import openai

# --- Argument Parser ---
parser = argparse.ArgumentParser()
parser.add_argument('-t', '--turbo', action='store_true', help='use gpt-3.5-turbo instead of gpt-4')
parser.add_argument('-c', '--combined', action='store_true', help='send and receive all the headlines in bulk (cheaper but probably less good)')
parser.add_argument('-T', '--temp', default=0.3, help='temperature (variability) of the model. a value between 0.0 and 1.0 (default: 0.3)')
args = parser.parse_args()

# --- Model Setup ---
modelV = 'gpt-3.5-turbo' if args.turbo else 'gpt-4'
openai.api_key = open('auth.txt', 'r').readlines()[0].strip()
newsapi_key = open('newsapi_key.txt', 'r').read().strip()
apiCost = 0
tScores = []

# --- System Prompts ---
sysPromptSingle = 'You are a financial advisor. When the user gives you a headline, ' \
                  'respond with a number between -1.0 and 1.0, signifying whether the ' \
                  'headline is extremely negative (-1.0), neutral (0.0), or extremely ' \
                  'positive (1.0) for the stock value of {}.'

sysPromptBatch = 'You are a financial advisor. When the user gives you a list of headlines, ' \
                 'respond with a number between -1.0 and 1.0 for each headline, signifying whether the ' \
                 'headline is extremely negative (-1.0), neutral (0.0), or extremely ' \
                 'positive (1.0) for the stock value of {}.'

# --- Create Report Directory ---
if not os.path.isdir('Individual_Reports'):
    os.mkdir('Individual_Reports')

# --- GPT Ask Function ---
def askGPT(prompt, system_prompt):
    global apiCost
    response = openai.ChatCompletion.create(
        model=modelV,
        temperature=float(args.temp),
        messages=[
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': prompt}
        ]
    )
    costFactor = [0.03, 0.06] if modelV == 'gpt-4' else [0.002, 0.002]
    apiCost += response['usage']['prompt_tokens'] / 1000 * costFactor[0] + response['usage']['completion_tokens'] / 1000 * costFactor[1]
    return response['choices'][0]['message']['content']

# --- News Fetcher via NewsAPI ---
def fetch_news(company):
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": company,
        "language": "en",
        "pageSize": 10,
        "sortBy": "publishedAt",
        "apiKey": newsapi_key
    }
    response = requests.get(url, params=params)
    articles = response.json().get("articles", [])
    return [article["title"] for article in articles]

# --- Main Execution Loop ---
for company in open('companies.txt', 'r').readlines():
    company = company.strip()
    headlines = fetch_news(company)
    scores = []
    sum_score = 0
    num = 0
    system_prompt = sysPromptBatch if args.combined else sysPromptSingle
    system_prompt = system_prompt.format(company)

    # Batch Mode
    if args.combined:
        headlineStr = '\n'.join(f"{i+1}. {headline}" for i, headline in enumerate(headlines))
        gpt_response = askGPT(headlineStr, system_prompt)
        for x, score in enumerate(re.findall(r'-?\d+\.\d+', gpt_response)):
            try:
                score = float(score)
                scores.append([headlines[x], score])
                sum_score += score
                num += 1
            except:
                scores.append([headlines[x], ''])
    # Single Mode
    else:
        for headline in headlines:
            try:
                score = float(re.findall(r'-?\d+\.\d+', askGPT(headline, system_prompt))[0])
                scores.append([headline, score])
                sum_score += score
                num += 1
            except:
                scores.append([headline, ''])

    # Mean Score
    mean = sum_score / num if num else 0
    scores.append(['Mean Score', mean])
    tScores.append([company, mean])

    # Save Company Report
    filename = f'Individual_Reports/{company}.csv'
    with open(filename, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['Headline', 'Score'])
        writer.writerows(scores)
    print(f'[*] Saved {filename}')

# --- Final Summary Report ---
tScores.append(['Total Cost', apiCost])
with open('report.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['Company', 'Mean Score'])
    writer.writerows(tScores)
print('[*] Saved report.csv')
