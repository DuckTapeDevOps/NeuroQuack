# Talking to an LLM
{user}: I want to request Coconut Skins by Damien Rice.

 !sr Damien Rice - Coconut Skins
{llm}: I'm sorry, @DuckTapeDevOps doesn't have that one, but he does have some by Jason Mraz that you may like. How's Butterfly sound? (We also found 1 of @DuckTapeDevOps's friends that has your request, follow @KerryLongMusic and ask @DuckTapeDevOps if he knows when he'll be on next!)
![Alt text](image.png)
# API calls:
curl 'https://api.streamersonglist.com/v1/streamers/37006/songs?size=10&current=0&showInactive=false&isNew=false&order=asc' \
  -H 'authority: api.streamersonglist.com' \
  -H 'accept: application/json, text/plain, */*' \
  -H 'accept-language: en-US,en;q=0.9' \
  -H 'authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOjU4NzYxNCwidXNlcm5hbWUiOiJkdWNrdGFwZWRldm9wcyIsInN0cmVhbWVySWQiOjM3MDA2LCJpYXQiOjE3MDIzOTcwMDksImV4cCI6MTcwNDk4OTAwOSwiaXNzIjoic3RyZWFtZXJzb25nbGlzdC5jb20ifQ.JOb7cGiCGGfMyjUA3_a73IjQDmMzrBSXcRtR934cmrM' \
  -H 'if-none-match: W/"18e-T5ggXN4g1BF8Y78fVF8MQo8p3ug"' \
  -H 'origin: https://www.streamersonglist.com' \
  -H 'referer: https://www.streamersonglist.com/' \
  -H 'sec-ch-ua: "Opera";v="105", "Chromium";v="119", "Not?A_Brand";v="24"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Windows"' \
  -H 'sec-fetch-dest: empty' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-site: same-site' \
  -H 'sec-gpc: 1' \
  -H 'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 OPR/105.0.0.0' \
  -H 'x-ssl-user-types: streamer' \
  --compressed