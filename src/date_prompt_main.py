from prompt.date_prompt import DatePrompt
from datetime import datetime

# pass in the vals of course
# today = datetime.today().strftime('%Y-%m-%d')
# prompt = DatePrompt(today=today,
#                     promptTempateFilename="src/date_prompt_demo/date_prompt_template.txt", 
#                     calJsonFilename="src/date_prompt_demo/weha_town_ical.jsonl").build()

# or use the sensible defaults
template = DatePrompt()
prompt = template.build()

print(f"{prompt}")
print(f"today {template.today}")
