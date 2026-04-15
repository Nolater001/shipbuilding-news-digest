import datetime, json, os, urllib.request, urllib.parse, ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

today = datetime.date.today()
date_str = today.strftime("%Y年%m月%d日")

topics = [
    ("\u65b0\u9020\u8239", "new shipbuilding order launched 2024"),
    ("\u8239\u5382", "shipyard newbuilding 2024"),
    ("\u8239\u8fd0\u4f01\u4e1a", "shipping company maritime 2024"),
    ("\u7eff\u8272\u8239\u8239", "green ship LNG methanol ammonia 2024"),
    ("\u8239\u8fd0\u6cd5\u89c4", "maritime regulation IMO 2024"),
    ("\u8239\u8fd0\u91d1\u878d\u4fdd\u9669", "shipping finance marine insurance 2024"),
]

results = []
for topic, kw in topics:
    try:
        url = "https://api.duckduckgo.com/?q=" + urllib.parse.quote(kw) + "&format=json"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=20, context=ctx) as r:
            data = json.loads(r.read())
        items = []
        for item in data.get("RelatedTopics", [])[:5]:
            if "Text" in item and item["Text"]:
                t = item["Text"][:120].replace(chr(10), " ")
                src = item.get("URL", "").split("/")[-1][:20]
                items.append("- " + t + " [`" + src + "`]")
        results.append((topic, items if items else ["(\u6682\u65e0\u76f8\u5173\u8d44\u8baf)"]))
    except Exception as e:
        results.append((topic, ["\u83b7\u53d6\u5931\u8d25: " + str(e)[:60]]))

lines = [
    "# \u0232\u0255 \u9020\u8239\u8981\u95fb\u7b80\u62a5",
    "",
    "**\u65e5\u671f**: " + date_str,
    "",
    "> \u672c\u7b80\u62a5\u7531 QClaw AI + GitHub Actions \u81ea\u52a8\u751f\u6210 | \u6570\u636e\u6765\u6e90: DuckDuckGo",
    "",
    "---",
]
for topic, items in results:
    lines.append("## " + topic)
    lines.append("")
    lines.extend(items)
    lines.append("")

body = "\n".join(lines)
os.makedirs("digests", exist_ok=True)
d = os.path.join("digests", today.strftime("%Y-%m-%d") + ".md")
with open(d, "w", encoding="utf-8") as f:
    f.write(body)
print("DONE:" + d + " size=" + str(len(body)))
