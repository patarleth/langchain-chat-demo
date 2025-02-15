import pandas as pd
import io, os
import logging

from datetime import datetime

class DatePrompt:

    def __init__(self, today=None,
                 origin="US",
                 message_date_format = "MM/DD/YYYY hh:mm:ss p zzz",
                 prompt_tempate_filename=None, 
                 cal_json_filename=None):
        if today is None:
            today = datetime.today().strftime('%Y-%m-%d')
        if prompt_tempate_filename is None:
            prompt_tempate_filename = os.path.dirname(os.path.realpath(__file__)) + "/date_prompt_template.txt"
        if cal_json_filename is None:
            cal_json_filename = os.path.dirname(os.path.realpath(__file__)) + "/weha_town_ical.jsonl"

        # print(f"logger name {__name__}")
        self.logger = logging.getLogger(__name__)

        self.today = today
        self.origin = origin
        self.message_date_format = message_date_format
        self.promptTempateFilename = prompt_tempate_filename        
        self.prompt_template_txt = self.readPromptTemplateFromFile(self.promptTempateFilename)

        self.calJsonFilename = cal_json_filename
        self.weha_town_ical_json = self.readCalJsonFromFile(self.calJsonFilename)

    def readPromptTemplateFromFile(self, filename : str) -> str:
        prompt_template_file = open(filename, "r")
        prompt_template_txt = prompt_template_file.read()
        return prompt_template_txt

    def readCalJsonFromFile(self, filename :str) -> str:
        weha_town_ical_json_file = open(filename, "r")
        weha_town_ical_json = weha_town_ical_json_file.read()
        return weha_town_ical_json

    def parseCalJsonToContextString(self, weha_town_ical_json) -> str:
        ical_entries  = pd.read_json(path_or_buf=io.StringIO(weha_town_ical_json), lines=True, chunksize=1)

        context_text = ""
        start : datetime
        end : datetime
        diff = 0.0

        for entry in ical_entries:
            msg = entry["message"].values[0]
            self.logger.debug(f"{msg}")
            context_text += msg
            context_text += "\n"
            start_str = entry["start"].values[0]
            # 2024-11-14T22:00:00.000Z
            start = datetime.strptime(start_str, '%Y-%m-%dT%H:%M:%S.%fZ')
            startMs = start.timestamp()
            
            end_str = entry["end"].values[0]
            end = datetime.strptime(end_str, '%Y-%m-%dT%H:%M:%S.%fZ')
            endMs = end.timestamp()

            diff = endMs - startMs
            if diff > 0:
                self.logger.debug(f"{diff} - {msg}")
            
        return context_text

    def build(self) -> str:
        # 6/24/2025 7:30:00 PM EDT

        prompt = self.prompt_template_txt.replace("__TODAY__", self.today)
        prompt = prompt.replace("__ORIGIN__", self.origin)
        
        prompt = prompt.replace("__MESSAGE_DATE_FORMAT__", self.message_date_format)
        context_text = self.parseCalJsonToContextString(self.weha_town_ical_json)
        prompt = prompt.replace("__CONTEXT__", context_text)

        return prompt
