import matplotlib
import pandas as pd
import dateutil.parser
import matplotlib.pyplot as plt
import numpy as np

keywords = ['.wlox.com', 'wtvq.com',
            'abc3340.com', 'abccolumbia.com', 'abcnews.go.com', 'arabnews.com', 'asiaone.com', 'al.com',
            'article', 'articles',
            'bakingbusiness.com', 'bbc.co.uk', 'bbc.com', 'business-standard.com', 'bloomberg.Com',
            'cbc.ca', 'cbs42.com', 'cbs58.com', 'cbsnews.com', 'cnn.com', 'carsonnow.org',
            'dailymail.co.uk', 'dailysabah.com', 'dawn.com', 'dw.com', 'dispatch.com',
            'euronews.com', 'express.co.uk',
            'factory+fire',
            'huffpost.com',
            'foodbusinessnews.net', 'foxnews.com', 'firerescue1.com', 'foodmanufacture.co.uk',
            'independent.co.uk',
            'justthenews.com',
            'kare11.com', 'kgw.com', 'ktla.com',
            'lfpress.com', 'localmemphis.com', 'latimes.com',
            'm.daily-bangladesh.com', 'meatpoultry.com', 'medium.com',
            'nbcrightnow.com', 'news', 'news.google', 'news.sky', 'news.yahoo', 'news.yahoo.com', 'newsweek.com',
            'nytime.com', 'nbcnews.com', 'nationalgeographic.com', 'newsnow.co.uk',
            'off-guardian.org', 'oann.com',
            'pakistantoday.com', 'powderbulksolids.com',
            'reuters.com', 'reutersagency.com', 'rollingstone.com', 'www.rt.com',
            'thediplomat.com', 'theguardian.com', 'thesun.co.uk', 'time.com', 'timesinternet.in', 'telegraph.co.uk',
            'today', 'theepochtimes.com', 'theverge.com', 'theledger.com', 'times',
            'usfa.fema.gov', 'usatoday.com',
            'washingtonpost.com', 'washingtontimes.com', 'wkow.com', 'wkyt.com', 'wsj.com',
            'yaktrinews.com', "news.yahoo"]

file = "google_scraper/fires3.csv"

df = pd.read_csv(file)
df["date"] = None
headerNames = ["title", "snippet", "link", "position", "date"]
df.columns = headerNames
df.drop_duplicates(subset=["title"], keep="first", inplace=True)

# Write scraped links in a new text file.
# links = open("Links.txt", "a")
# for i in df["link"]:
# links.write(f"{i}\n")
# links.close()

# Drop links from pages not included in keywords list.
df = df[df["link"].str.contains('|'.join(keywords), na=False)]

# Extract dates from snippet column and deposit them in dates column.
format_list = ["[0-9]{1,2}(?:\,|\.|\/|\-)(?:\s)?[0-9]{1,2}(?:\,|\.|\/|\-)(?:\s)?[0-9]{2,4}",
               "[0-9]{1,2}(?:\.)(?:\s)?(?:(?:(?:j|J)a)|(?:(?:f|F)e)|(?:(?:m|M)a)|(?:(?:a|A)p)|(?:(?:m|M)a)|(?:(?:j|J)u)|(?:(?:a|A)u)|(?:(?:s|S)e)|(?:(?:o|O)c)|(?:(?:n|N)o)|(?:(?:d|D)e))\w*(?:\s)?[0-9]{2,4}",
               "(?:(?:(?:j|J)an)|(?:(?:f|F)eb)|(?:(?:m|M)ar)|(?:(?:a|A)pr)|(?:(?:m|M)ay)|(?:(?:j|J)un)|(?:(?:j|J)ul)|(?:(?:a|A)ug)|(?:(?:s|S)ep)|(?:(?:o|O)ct)|(?:(?:n|N)ov)|(?:(?:d|D)ec))\w*(?:\s)?(?:\n)?[0-9]{1,2}(?:\s)?(?:\,|\.|\/|\-)?(?:\s)?[0-9]{2,4}(?:\,|\.|\/|\-)?(?:\s)?[0-9]{2,4}",
               "[0-9]{1,2}(?:\.)?(?:\s)?(?:\n)?(?:(?:(?:j|J)a)|(?:(?:f|F)e)|(?:(?:m|M)a)|(?:(?:a|A)p)|(?:(?:m|M)a)|(?:(?:j|J)u)|(?:(?:a|A)u)|(?:(?:s|S)e)|(?:(?:o|O)c)|(?:(?:n|N)o)|(?:(?:d|D)e))\w*(?:\,|\.|\/|\-)?(?:\s)?[0-9]{2,4}"]
# Manually pop rows with unacceptable format strings for date extraction. Not the best solution, but hey, it works.
df = df[df["snippet"].str.contains("58, 99,600") == False]
df = df[df["snippet"].str.contains("1.4/30") == False]
df = df[df["snippet"].str.contains("June 10, 2008. 28") == False]
df = df[df["snippet"].str.contains("3.4. 1897") == False]
df = df[df["snippet"].str.contains("14, 23, 24") == False]
df = df[df["snippet"].str.contains("5 noob 3135") == False]
df = df[df["snippet"].str.contains("00-10,000") == False]
df = df[df["snippet"].str.contains("22.80-09") == False]
df = df[df["snippet"].str.contains("12.47. 17") == False]

f = lambda x: dateutil.parser.parse(x).strftime("%Y-%m-%d")
df["date"] = df["snippet"].str.extractall(f'({"|".join(format_list)})')[0].apply(f).groupby(level=0).agg(','.join)
# If a date row has an extra date, move it to a new column.
df[["date", "extra_date"]] = df["date"].str.split(',', 1, expand=True)
# Delete the extra dates column.
del df["extra_date"]
df = df.dropna()

# Creating empty df to work with only dates and counts.
fires_df = pd.DataFrame()
# Grab dates from main df, filter to display only dates from year 2000 to present day.
filtered_df = df.loc[df["date"].between("2000-01-01", "2022-08-01")]

fires_df["date"] = filtered_df["date"]
fires_df["date"] = pd.to_datetime(fires_df["date"])
# Group dates by months. Count days in months and record count in new column.
fires_df["fires"] = fires_df.groupby([pd.Grouper(key="date", freq="M")])["date"].transform("size").astype(int)
# Reformat dates, drop days, keep months.
fires_df["date"] = fires_df["date"].dt.strftime("%Y-%b")
# Drop the duplicates.
fires_df.drop_duplicates(subset=None, keep="first", inplace=True)
# Sort by date in ascending order.
fires_df["date"] = pd.to_datetime(fires_df["date"], format="%Y-%b")
fires_df = fires_df.sort_values(by=["date"], ascending=False)

fires_df = fires_df.set_index("date")
fires_df = fires_df.reset_index()

# print(fires_df)

years = matplotlib.dates.YearLocator(base=2)
years_fmt = matplotlib.dates.DateFormatter("%Y")

# Plot
fig, ax = plt.subplots()
ax.plot(fires_df["date"], fires_df["fires"], linewidth=1.2, color="orangered")

ax.set_title("Timeline of the number of news articles about fires in a variety of "
             "\nfood factories and food processing plants worldwide.\n", fontsize=12)

ax.xaxis.set_major_locator(years)
ax.xaxis.set_major_formatter(years_fmt)

N = 150
data = np.linspace(0, N, N)

ax.set_facecolor("oldlace")
plt.grid(color="wheat", linestyle="--", linewidth=0.6)
# plt.xticks(fires_df["date"], fires_df["date"].dt.strftime("%b %Y"), rotation=90, fontsize=10, ha="left")
plt.yticks(np.arange(0, max(fires_df["fires"]), 20))
plt.margins(x=0, y=0, tight=True)
plt.ylim(0, None)

# plt.gca().margins(x=0)
# plt.gcf().canvas.draw()
# tl = plt.gca().get_xticklabels()
# maxsize = max([t.get_window_extent().width for t in tl])
# m = 0.2 # inch margin
# s = maxsize/plt.gcf().dpi*N+2*m
# margin = m/plt.gcf().get_size_inches()[0]

# plt.gcf().subplots_adjust(left=margin, right=1.-margin)
# plt.gcf().set_size_inches(s, plt.gcf().get_size_inches()[1])

# fig.subplots_adjust(left=0.01, bottom=0.2)

# plt.savefig("Full plot.")
plt.show()
