from gaptest import *
from pprint import pprint as pp

wait_ratio = 1

insight = {}

get_screen_size()

search_btn = find_element(get_ui(), "Search", "content-desc")
tap(search_btn)

top_chart = requests.get("https://trends.google.com/trends/api/topcharts?hl=en-AU&tz=-420&date=2016&geo=GLOBAL&isMobile=false").text
top_chart = json.loads(re.sub(r"^\)\]\}\'\n",'',top_chart))
list_trends = top_chart["topCharts"][0]["listItems"]
titles = []
for a in range(len(list_trends)) :
    titles.append(list_trends[a]["title"])
print( "Google trends 2016 List : " + str(titles))

for c in range(len((titles))):
    time.sleep(0.5*wait_ratio)
    close_keyboard()
    type(titles[c])

    time.sleep(0.5*wait_ratio)
    history = find_elements(get_ui(),"com.google.android.youtube:id/text","text",False)
    print(history)

    clear_search_btn = find_element(get_ui(),"com.google.android.youtube:id/search_clear","resuorce-id")
    tap(clear_search_btn)

    insight[titles[c]] = history

pp(insight)

back()
