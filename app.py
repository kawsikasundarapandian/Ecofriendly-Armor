import streamlit as st
from gtts import gTTS
from io import BytesIO
import pandas as pd
import altair as alt
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Eco-Friendly Armor Units",
    page_icon="🌱",
    layout="wide"
)

if "theme" not in st.session_state:
    st.session_state.theme = "Light"

theme = st.selectbox("🌗 Choose Theme", ["Light", "Dark"])
st.session_state.theme = theme

if st.session_state.theme == "Dark":
    st.markdown(
        """<style>.stApp { background-color: #0e1117; color: white; }</style>""",
        unsafe_allow_html=True
    )
else:
    st.markdown(
        """<style>.stApp { background-color: white; color: black; }</style>""",
        unsafe_allow_html=True
    )

languages = ["English","Hindi","Tamil","Spanish","French","German","Japanese"]
language = st.selectbox("🌐 Choose Language", languages)

translations = {
    "English": {"title":"🌊 Coastal Protection Using Eco-Friendly Armor Units",
                "wave":"Average Wave Height (meters)","cyclone":"Cyclone Frequency",
                "soil":"Coastal Soil Type","env":"Environmental Priority",
                "recommend":"Recommend Armor Unit","inputs":"📝 Your Inputs",
                "suggestion":"🛡️ Suggested Armor Unit","reason":"📌 Reason",
                "summary":"📊 Recommendation Summary","chart":"🌊 Coastal Condition Overview",
                "low":"Low","medium":"Medium","high":"High"},
    
    "Hindi": {"title":"🌊 पर्यावरण-अनुकूल कंक्रीट इकाइयों का उपयोग करके तटीय सुरक्षा",
              "wave":"औसत तरंग ऊँचाई (मीटर में)","cyclone":"साइक्लोन की आवृत्ति",
              "soil":"तटीय मिट्टी का प्रकार","env":"पर्यावरण प्राथमिकता",
              "recommend":"अमर इकाई की सिफारिश करें","inputs":"📝 आपके इनपुट",
              "suggestion":"🛡️ सुझाई गई अमर इकाई","reason":"📌 कारण",
              "summary":"📊 सिफारिश सारांश","chart":"🌊 तटीय स्थिति अवलोकन",
              "low":"कम","medium":"मध्यम","high":"उच्च"},
    
    "Tamil": {"title":"🌊 சுற்றுப்புற நட்பான ஆர்மர் யூனிட்டுகளை பயன்படுத்தி கடலோர பாதுகாப்பு",
              "wave":"சராசரி அலை உயரம் (மீட்டரில்)","cyclone":"சைக்கிளோன் முறை",
              "soil":"கடலோர மண் வகை","env":"சுற்றுச்சூழல் முன்னுரிமை",
              "recommend":"ஆர்மர் யூனிட் பரிந்துரை செய்யவும்","inputs":"📝 உங்கள் உள்ளீடுகள்",
              "suggestion":"🛡️ பரிந்துரைக்கப்பட்ட ஆர்மர் யூனிட்","reason":"📌 காரணம்",
              "summary":"📊 பரிந்துரை சுருக்கம்","chart":"🌊 கடலோர நிலை அறிமுகம்",
              "low":"குறைந்தது","medium":"நடுத்தரம்","high":"அதிகம்"},
    
    "Spanish": {"title":"🌊 Protección Costera con Unidades de Armadura Ecológicas",
                "wave":"Altura Media de Olas (metros)","cyclone":"Frecuencia de Ciclones",
                "soil":"Tipo de Suelo Costero","env":"Prioridad Ambiental",
                "recommend":"Recomendar Unidad de Armadura","inputs":"📝 Sus Entradas",
                "suggestion":"🛡️ Unidad de Armadura Sugerida","reason":"📌 Razón",
                "summary":"📊 Resumen de Recomendación","chart":"🌊 Resumen de Condición Costera",
                "low":"Bajo","medium":"Medio","high":"Alto"},
    
    "French": {"title":"🌊 Protection Côtière avec des Unités d'Armure Écologiques",
               "wave":"Hauteur Moyenne des Vagues (mètres)","cyclone":"Fréquence des Cyclones",
               "soil":"Type de Sol Côtier","env":"Priorité Environnementale",
               "recommend":"Recommander l'Unité d'Armure","inputs":"📝 Vos Entrées",
               "suggestion":"🛡️ Unité d'Armure Suggérée","reason":"📌 Raison",
               "summary":"📊 Résumé de la Recommandation","chart":"🌊 Vue d'ensemble de l'État Côtier",
               "low":"Faible","medium":"Moyen","high":"Élevé"},
    
    "German": {"title":"🌊 Küstenschutz mit Umweltfreundlichen Rüstungseinheiten",
               "wave":"Durchschnittliche Wellenhöhe (Meter)","cyclone":"Zyklonhäufigkeit",
               "soil":"Küstentyp Boden","env":"Umweltpriorität",
               "recommend":"Rüstungseinheit Empfehlen","inputs":"📝 Ihre Eingaben",
               "suggestion":"🛡️ Vorgeschlagene Rüstungseinheit","reason":"📌 Grund",
               "summary":"📊 Empfehlung Zusammenfassung","chart":"🌊 Küstenzustand Übersicht",
               "low":"Niedrig","medium":"Mittel","high":"Hoch"},
    
    "Japanese": {"title":"🌊 環境に優しいアーマーユニットによる沿岸保護",
                 "wave":"平均波高（メートル）","cyclone":"サイクロン頻度",
                 "soil":"沿岸土壌タイプ","env":"環境優先度",
                 "recommend":"アーマーユニットを推奨","inputs":"📝 入力内容",
                 "suggestion":"🛡️ 推奨アーマーユニット","reason":"📌 理由",
                 "summary":"📊 推奨サマリー","chart":"🌊 沿岸状況概要",
                 "low":"低","medium":"中","high":"高"}
}
t = translations[language]

st.title(t["title"])
st.divider()

wave_height = st.slider(t["wave"], 0.5, 10.0, 3.0)
cyclone_frequency = st.selectbox(t["cyclone"], [t["low"],t["medium"],t["high"]])
soil_type = st.selectbox(t["soil"], ["Sandy","Clay","Rocky"])
environment_priority = st.selectbox(t["env"], [t["low"],t["medium"],t["high"]])
st.divider()
left_col, right_col = st.columns(2)

if left_col.button(t["recommend"]):
    cyclone_map_en = {t["low"]:"Low", t["medium"]:"Medium", t["high"]:"High"}
    env_map_en = {t["low"]:"Low", t["medium"]:"Medium", t["high"]:"High"}
    cyclone_en = cyclone_map_en[cyclone_frequency]
    env_en = env_map_en[environment_priority]
    if wave_height >= 6 or cyclone_en=="High":
        armor_unit = {
            "English":"Interlocking Eco-Concrete Armor Units",
            "Hindi":"इंटरलॉकिंग पर्यावरण-अनुकूल कंक्रीट इकाइयाँ",
            "Tamil":"இணைக்கக்கூடிய சுற்றுப்புற நட்பான காங்கிரீட் யூனிட்டுகள்",
            "Spanish":"Unidades de Armadura Ecológicas Interconectadas",
            "French":"Unités d'Armure Écologiques Interconnectées",
            "German":"Interlock-Umweltfreundliche Rüstungseinheiten",
            "Japanese":"相互接続型エココンクリートアーマーユニット"
        }[language]
        explanation = {
            "English":"High wave energy and frequent cyclones require strong interlocking armor units.",
            "Hindi":"उच्च तरंग ऊर्जा और बार-बार आने वाले साइक्लोन के लिए मजबूत इंटरलॉकिंग अमर इकाइयाँ आवश्यक हैं।",
            "Tamil":"உயர் அலை சக்தி மற்றும் அடிக்கடி வரும் சைக்கிளோன்கள் சக்திவாய்ந்த இணைக்கக்கூடிய ஆர்மர் யூனிட்டுகளை தேவையாக உருவாக்குகின்றன.",
            "Spanish":"Las altas olas y los ciclones frecuentes requieren unidades de armadura interconectadas fuertes.",
            "French":"Les vagues fortes et les cyclones fréquents nécessitent des unités d'armure interconnectées solides.",
            "German":"Hohe Wellenenergie und häufige Zyklone erfordern starke interlock-Rüstungseinheiten.",
            "Japanese":"高い波エネルギーと頻繁なサイクロンには、強力な相互接続型アーマーユニットが必要です。"
        }[language]
    elif soil_type=="Sandy" and env_en=="High":
        armor_unit = {
            "English":"Geotextile-Based Eco Armor Units",
            "Hindi":"जियोटेक्सटाइल आधारित पर्यावरण-अनुकूल अमर इकाइयाँ",
            "Tamil":"ஜியோடெக்ஸ்டைல் அடிப்படையிலான சுற்றுப்புற நட்பான ஆர்மர் யூனிட்டுகள்",
            "Spanish":"Unidades de Armadura Ecológicas Basadas en Geotextiles",
            "French":"Unités d'Armure Écologiques Basées sur le Géotextile",
            "German":"Geotextilbasierte Umweltfreundliche Rüstungseinheiten",
            "Japanese":"ジオテキスタイルベースのエコアーマーユニット"
        }[language]
        explanation = {
            "English":"Sandy soil and high environmental concern favor geotextile units.",
            "Hindi":"रेतीली मिट्टी और उच्च पर्यावरण चिंता जियोटेक्सटाइल इकाइयों को पसंद करती है।",
            "Tamil":"மணலான மண் மற்றும் உயர்ந்த சுற்றுச்சூழல் கவலை ஜியோடெக்ஸ்டைல் யூனிட்டுகளை ஆதரிக்கின்றது.",
            "Spanish":"El suelo arenoso y la alta preocupación ambiental favorecen las unidades geotextiles.",
            "French":"Le sol sableux et une forte préoccupation environnementale favorisent les unités géotextiles.",
            "German":"Sandiger Boden und hohe Umweltpriorität begünstigen Geotextileinheiten.",
            "Japanese":"砂質の土壌と高い環境配慮はジオテキスタイルユニットを推奨します。"
        }[language]
    else:
        armor_unit = {
            "English":"Modular Eco-Friendly Concrete Blocks",
            "Hindi":"मॉड्यूलर पर्यावरण-अनुकूल कंक्रीट ब्लॉक्स",
            "Tamil":"மாடுலர் சுற்றுப்புற நட்பான காங்கிரீட் பிரிவுகள்",
            "Spanish":"Bloques de Hormigón Ecológicos Modulares",
            "French":"Blocs de Béton Écologiques Modulaires",
            "German":"Modulare Umweltfreundliche Betonblöcke",
            "Japanese":"モジュラー環境対応コンクリートブロック"
        }[language]
        explanation = {
            "English":"Moderate coastal conditions can be protected using modular eco-friendly concrete armor units.",
            "Hindi":"मध्यम तटीय परिस्थितियों की रक्षा मॉड्यूलर पर्यावरण-अनुकूल कंक्रीट अमर इकाइयों से की जा सकती है।",
            "Tamil":"மிதமான கடலோர சூழ்நிலைகள் மாடுலர் சுற்றுப்புற நட்பான காங்கிரீட் ஆர்மர் யூனிட்டுகளால் பாதுகாக்கப்படலாம்.",
            "Spanish":"Las condiciones costeras moderadas se pueden proteger usando bloques modulares ecológicos.",
            "French":"Les conditions côtières modérées peuvent être protégées à l'aide de blocs de béton modulaires écologiques.",
            "German":"Moderate Küstenbedingungen können mit modularen umweltfreundlichen Betonblöcken geschützt werden.",
            "Japanese":"穏やかな沿岸条件は、モジュラー環境対応コンクリートブロックで保護できます。"
        }[language]

    left_col.subheader(t["inputs"])
    left_col.write(f"🌊 Wave Height: {wave_height} m")
    left_col.write(f"🌀 Cyclone Frequency: {cyclone_frequency}")
    left_col.write(f"🌱 Environmental Priority: {environment_priority}")
    left_col.write(f"🪨 Soil Type: {soil_type}")

    left_col.success("✅ Recommended Protection Method")
    left_col.subheader(t["suggestion"])
    left_col.write(f"**{armor_unit}**")
    left_col.subheader(t["reason"])
    left_col.write(explanation)

    lang_code_map = {"English":"en","Hindi":"hi","Tamil":"ta","Spanish":"es","French":"fr","German":"de","Japanese":"ja"}
    tts = gTTS(text=explanation, lang=lang_code_map[language])
    audio_bytes = BytesIO()
    tts.write_to_fp(audio_bytes)
    audio_bytes.seek(0)
    left_col.audio(audio_bytes, format="audio/mp3")

    # Recommendation table
    recommendation_df = pd.DataFrame({"Recommended Armor Unit":[armor_unit],"Reason":[explanation]})
    left_col.subheader(t["summary"])
    left_col.table(recommendation_df)

    cyclone_map_num = {t["low"]:1, t["medium"]:2, t["high"]:3}
    env_map_num = {t["low"]:1, t["medium"]:2, t["high"]:3}
    soil_map_num = {"Sandy":1, "Clay":2, "Rocky":3}

    wave_pct = (wave_height/10)*100
    cyclone_pct = (cyclone_map_num[cyclone_frequency]/3)*100
    env_pct = (env_map_num[environment_priority]/3)*100
    soil_pct = (soil_map_num[soil_type]/3)*100

    data_pct = pd.DataFrame({
        "Parameter":["Wave Height","Cyclone Frequency","Environmental Priority","Soil Type"],
        "Percentage":[wave_pct, cyclone_pct, env_pct, soil_pct]
    })

    bar_chart = alt.Chart(data_pct).mark_bar(color="#00BFFF").encode(x='Parameter', y='Percentage').properties(width=400,height=250,title="Bar Chart (%)")
    right_col.altair_chart(bar_chart)
    area_chart = alt.Chart(data_pct).mark_area(opacity=0.3,color="green").encode(x='Parameter', y='Percentage').properties(width=400,height=250,title="Area Chart (%)")
    right_col.altair_chart(area_chart)   
    fig_pie = px.pie(data_pct,names='Parameter',values='Percentage',title='Pie Chart (%)',color_discrete_sequence=px.colors.sequential.Blues)
    right_col.plotly_chart(fig_pie)
    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(r=[wave_pct,cyclone_pct,env_pct,soil_pct],theta=['Wave Height','Cyclone Frequency','Environmental Priority','Soil Type'],fill='toself',name='Coastal Condition'))
    fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True,range=[0,100])),showlegend=True,title="Radar Chart (%)")
    right_col.plotly_chart(fig_radar)
