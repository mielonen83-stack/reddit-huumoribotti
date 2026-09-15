import requests
import streamlit as st

st.set_page_config(
    page_title="Reddit Huumorivideot", page_icon="😂", layout="wide"
)

st.title("😂 Redditin Huumorivideot")
st.write(
    "Tämä sovellus hakee suosittuja videoita suoraan netistä ilman erillisiä"
    " tunnuksia."
)

# Sivupalkin asetukset
subreddit_nimi = st.sidebar.selectbox(
    "Valitse kanava:",
    ["funny", "ContagiousLaughter", "Unexpected", "HoldMyBeer"],
)
maara = st.sidebar.slider("Videoiden määrä:", 1, 10, 3)


@st.cache_data(ttl=300)
def hae_videot_ilman_tunnuksia(sub):
  # Käytetään eri User-Agentia, jotta pyyntö näyttää normaalilta selaimelta
  headers = {
      "User-Agent": (
          "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
          " (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
      )
  }
  url = f"https://www.reddit.com/r/{sub}/hot.json?limit=50"

  try:
    vastaus = requests.get(url, headers=headers)
    if vastaus.status_code == 200:
      data = vastaus.json()
      videot = []
      for postaus in data["data"]["children"]:
        tiedot = postaus["data"]
        # Etsitään videotarkistus
        onko_video = tiedot.get("is_video", False)
        video_url = None

        if onko_video and "media" in tiedot and tiedot["media"]:
          reddit_video = tiedot["media"].get("reddit_video", {})
          video_url = reddit_video.get("fallback_url")

        if not video_url and "v.redd.it" in tiedot.get("url", ""):
          video_url = tiedot.get("url") + "/DASH_1080.mp4"

        if video_url:
          videot.append({
              "title": tiedot.get("title"),
              "score": tiedot.get("score"),
              "url": video_url,
              "permalink": f"https://reddit.com{tiedot.get('permalink')}",
          })
      return videot
    else:
      return f"Virhe: Reddit palautti koodin {vastaus.status_code}"
  except Exception as e:
    return str(e)


if st.button("Hae videot! 🚀", type="primary"):
  with st.spinner("Haetaan nauruja..."):
    tulos = hae_videot_ilman_tunnuksia(subreddit_nimi)

    if isinstance(tulos, str):
      st.error(
          f"Reddit esti pyynnön ({tulos}). Tämä johtuu Streamlit Cloudin"
          " pilvipalvelimen IP-osoitteesta."
      )
      st.info(
          "💡 **Vinkki:** Jos tämä ei toimi pilvessä, koodi toimii varmasti, jos"
          " ajat sitä omalla koneellasi!"
      )
    elif not tulos:
      st.info("Ei videoita löytynyt.")
    else:
      st.success(f"Löytyi {len(tulos)} videota!")
      for v in tulos[:maara]:
        st.subheader(v["title"])
        st.write(f"💬 Ääniä: {v['score']}")
        try:
          st.video(v["url"])
        except Exception:
          st.write(f"[Katso video Redditissä]({v['permalink']})")
        st.markdown("---")
