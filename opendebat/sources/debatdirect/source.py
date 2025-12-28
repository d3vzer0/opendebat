# @dlt.resource(parallelized=True)
# def politicians():
#     response = debatclient.get("/api/actors/2025-12-18").json()
#     for politician in response["politicians"]:
#         yield politician

# @dlt.resource(parallelized=True)
# def parties():
#     response = debatclient.get("/api/actors/2025-12-18").json()
#     for party in response["parties"]:
#         yield party

# @dlt.transformer(data_from=debatten, parallelized=True)
# def debat_events(debat):
#     response = debatclient.get(f"/api/debates/{debat['id']}").json()
#     for event in response["events"]:
#         yield {"debat_id": debat["id"], **event}

# @dlt.resource(parallelized=True)
# def subtitles():
#     start = "2025-12-18T19:29:11.0000000+01:00"
#     end = "2025-12-18T21:02:16.0000000+01:00"
#     response = videoclient.get(
#         "/2025-12-18/plenairezaal//subtitles/nl-pol/vod.vtt",
#         params={"start": start, "end": end},
#     ).text

#     pattern = r"(\d{2}:\d{2}:\d{2}\.\d{3}) --> (\d{2}:\d{2}:\d{2}\.\d{3})\n(.+?)(?=\n\n|\Z)"
#     matches = re.findall(pattern, response, re.DOTALL)
#     match_simplified = [
#         {
#             "start": m[0],
#             "end": m[1],
#             "caption": m[2].strip(),
#             "debat_id": "a7f9c170-6e2a-4d6c-be67-95bd2624c22c",
#         }
#         for m in matches
#     ]
#     yield match_simplified

# return (politicians, parties, debatten, debat_events, subtitles)
