import streamlit as st
import random as r
import pandas as pd
import altair as alt

# A priori Knoten / Elternknoten
familiaeres_uUmfeld = {
    'stabil': 0.7,
    'instabil': 0.3
}

psychische_gesundheit = {
    'unauffällig': 0.96,
    'auffällig': 0.04
}

schulische_unterstuetzung = {
    'vorhanden': 0.55,
    'mangelhaft': 0.45
}

# Mediatoren / Verhaltens- und Leistungsmerkmale

aggressives_verhalten = {
    'stabil,unauffällig': {"aggressivja": 0.03, "aggressivnein": 0.97},
    'stabil,auffällig': {"aggressivja": 0.25, "aggressivnein": 0.75},
    'instabil,unauffällig': {"aggressivja": 0.3, "aggressivnein": 0.7},
    'instabil,auffällig': {"aggressivja": 0.9, "aggressivnein": 0.1}
}

soziale_isolation = {
    "stabil,unauffällig": {"sozialisoliertja": 0.04, "sozialisoliertnein": 0.96},
    "stabil,auffällig": {"sozialisoliertja": 0.25, "sozialisoliertnein": 0.75},
    "instabil,unauffällig": {"sozialisoliertja": 0.3, "sozialisoliertnein": 0.7},
    "instabil,auffällig": {"sozialisoliertja": 0.9, "sozialisoliertnein": 0.1}
}

leistungsabfall = {
    "unauffällig,vorhanden": {"leistungsabfallja": 0.04, "leistungsabfallnein": 0.96},
    "unauffällig,mangelhaft": {"leistungsabfallja": 0.25, "leistungsabfallnein": 0.75},
    "auffällig,vorhanden": {"leistungsabfallja": 0.3, "leistungsabfallnein": 0.7},
    "auffällig,mangelhaft": {"leistungsabfallja": 0.9, "leistungsabfallnein": 0.1}
}

# Abh. von aggr. Verhalten und soziale isolation
warnsignale_im_gespraech = {
    "aggressivja,sozialisoliertja": {"warnsignaleja": 0.9, "warnsignalenein": 0.1},
    "aggressivja,sozialisoliertnein": {"warnsignaleja": 0.4, "warnsignalenein": 0.6},
    "aggressivnein,sozialisoliertja": {"warnsignaleja": 0.3, "warnsignalenein": 0.7},
    "aggressivnein,sozialisoliertnein": {"warnsignaleja": 0.03, "warnsignalenein": 0.97}
}

# Abh. von Aggr. Verhalten
vorherige_vorfaelle = {
    "aggressivja": {"vorherigefaelleja": 0.9, "vorherigefaellenein": 0.1},
    "aggressivnein": {"vorherigefaelleja": 0.03, "vorherigefaellenein": 0.97}
}

# Zielvariable: gefahrenpotential
gefahrenpotential = {
    "aggressivnein,sozialisoliertnein,leistungsabfallnein,warnsignalenein,vorherigefaellenein": {"gefahrniedrig": 0.995, "gefahrmittel": 0.005, "gefahrhoch": 0.0},
    "aggressivnein,sozialisoliertnein,leistungsabfallnein,warnsignalenein,vorherigefaelleja": {"gefahrniedrig": 0.9, "gefahrmittel": 0.08, "gefahrhoch": 0.02},
    "aggressivnein,sozialisoliertnein,leistungsabfallnein,warnsignaleja,vorherigefaellenein": {"gefahrniedrig": 0.89, "gefahrmittel": 0.09, "gefahrhoch": 0.02},
    "aggressivnein,sozialisoliertnein,leistungsabfallnein,warnsignaleja,vorherigefaelleja": {"gefahrniedrig": 0.75, "gefahrmittel": 0.18, "gefahrhoch": 0.07},
    "aggressivnein,sozialisoliertnein,leistungsabfallja,warnsignalenein,vorherigefaellenein": {"gefahrniedrig": 0.92, "gefahrmittel": 0.07, "gefahrhoch": 0.01},
    "aggressivnein,sozialisoliertnein,leistungsabfallja,warnsignalenein,vorherigefaelleja": {"gefahrniedrig": 0.82, "gefahrmittel": 0.15, "gefahrhoch": 0.03},
    "aggressivnein,sozialisoliertnein,leistungsabfallja,warnsignaleja,vorherigefaellenein": {"gefahrniedrig": 0.75, "gefahrmittel": 0.18, "gefahrhoch": 0.07},
    "aggressivnein,sozialisoliertnein,leistungsabfallja,warnsignaleja,vorherigefaelleja": {"gefahrniedrig": 0.55, "gefahrmittel": 0.25, "gefahrhoch": 0.2},
    "aggressivnein,sozialisoliertja,leistungsabfallnein,warnsignalenein,vorherigefaellenein": {"gefahrniedrig": 0.91, "gefahrmittel": 0.08, "gefahrhoch": 0.01},
    "aggressivnein,sozialisoliertja,leistungsabfallnein,warnsignalenein,vorherigefaelleja": {"gefahrniedrig": 0.8, "gefahrmittel": 0.16, "gefahrhoch": 0.04},
    "aggressivnein,sozialisoliertja,leistungsabfallnein,warnsignaleja,vorherigefaellenein": {"gefahrniedrig": 0.75, "gefahrmittel": 0.18, "gefahrhoch": 0.07},
    "aggressivnein,sozialisoliertja,leistungsabfallnein,warnsignaleja,vorherigefaelleja": {"gefahrniedrig": 0.55, "gefahrmittel": 0.25, "gefahrhoch": 0.2},
    "aggressivnein,sozialisoliertja,leistungsabfallja,warnsignalenein,vorherigefaellenein": {"gefahrniedrig": 0.75, "gefahrmittel": 0.18, "gefahrhoch": 0.07},
    "aggressivnein,sozialisoliertja,leistungsabfallja,warnsignalenein,vorherigefaelleja": {"gefahrniedrig": 0.55, "gefahrmittel": 0.25, "gefahrhoch": 0.2},
    "aggressivnein,sozialisoliertja,leistungsabfallja,warnsignaleja,vorherigefaellenein": {"gefahrniedrig": 0.4, "gefahrmittel": 0.3, "gefahrhoch": 0.3},
    "aggressivnein,sozialisoliertja,leistungsabfallja,warnsignaleja,vorherigefaelleja": {"gefahrniedrig": 0.2, "gefahrmittel": 0.35, "gefahrhoch": 0.45},
    "aggressivja,sozialisoliertnein,leistungsabfallnein,warnsignalenein,vorherigefaellenein": {"gefahrniedrig": 0.78, "gefahrmittel": 0.2, "gefahrhoch": 0.02},
    "aggressivja,sozialisoliertnein,leistungsabfallnein,warnsignalenein,vorherigefaelleja": {"gefahrniedrig": 0.65, "gefahrmittel": 0.3, "gefahrhoch": 0.05},
    "aggressivja,sozialisoliertnein,leistungsabfallnein,warnsignaleja,vorherigefaellenein": {"gefahrniedrig": 0.6, "gefahrmittel": 0.35, "gefahrhoch": 0.05},
    "aggressivja,sozialisoliertnein,leistungsabfallnein,warnsignaleja,vorherigefaelleja": {"gefahrniedrig": 0.4, "gefahrmittel": 0.4, "gefahrhoch": 0.2},
    "aggressivja,sozialisoliertnein,leistungsabfallja,warnsignalenein,vorherigefaellenein": {"gefahrniedrig": 0.6, "gefahrmittel": 0.35, "gefahrhoch": 0.05},
    "aggressivja,sozialisoliertnein,leistungsabfallja,warnsignalenein,vorherigefaelleja": {"gefahrniedrig": 0.4, "gefahrmittel": 0.4, "gefahrhoch": 0.2},
    "aggressivja,sozialisoliertnein,leistungsabfallja,warnsignaleja,vorherigefaellenein": {"gefahrniedrig": 0.3, "gefahrmittel": 0.35, "gefahrhoch": 0.35},
    "aggressivja,sozialisoliertnein,leistungsabfallja,warnsignaleja,vorherigefaelleja": {"gefahrniedrig": 0.15, "gefahrmittel": 0.35, "gefahrhoch": 0.5},
    "aggressivja,sozialisoliertja,leistungsabfallnein,warnsignalenein,vorherigefaellenein": {"gefahrniedrig": 0.6, "gefahrmittel": 0.35, "gefahrhoch": 0.05},
    "aggressivja,sozialisoliertja,leistungsabfallnein,warnsignalenein,vorherigefaelleja": {"gefahrniedrig": 0.4, "gefahrmittel": 0.4, "gefahrhoch": 0.2},
    "aggressivja,sozialisoliertja,leistungsabfallnein,warnsignaleja,vorherigefaellenein": {"gefahrniedrig": 0.3, "gefahrmittel": 0.35, "gefahrhoch": 0.35},
    "aggressivja,sozialisoliertja,leistungsabfallnein,warnsignaleja,vorherigefaelleja": {"gefahrniedrig": 0.15, "gefahrmittel": 0.35, "gefahrhoch": 0.5},
    "aggressivja,sozialisoliertja,leistungsabfallja,warnsignalenein,vorherigefaellenein": {"gefahrniedrig": 0.3, "gefahrmittel": 0.35, "gefahrhoch": 0.35},
    "aggressivja,sozialisoliertja,leistungsabfallja,warnsignalenein,vorherigefaelleja": {"gefahrniedrig": 0.12, "gefahrmittel": 0.28, "gefahrhoch": 0.6},
    "aggressivja,sozialisoliertja,leistungsabfallja,warnsignaleja,vorherigefaellenein": {"gefahrniedrig": 0.08, "gefahrmittel": 0.22, "gefahrhoch": 0.7},
    "aggressivja,sozialisoliertja,leistungsabfallja,warnsignaleja,vorherigefaelleja": {"gefahrniedrig": 0.02, "gefahrmittel": 0.08, "gefahrhoch": 0.9}
}

samplelist = []
def forward_sampling(noSamples):
    samplelist = []
    for _ in range(noSamples):
        aktSample = {}

        # Sampling der A-priori-Knoten
        rnd = r.random()
        aktSample['familiaeres_uUmfeld'] = 'stabil' if rnd <= familiaeres_uUmfeld['stabil'] else 'instabil'

        rnd = r.random()
        aktSample['psychische_gesundheit'] = 'unauffällig' if rnd < psychische_gesundheit['unauffällig'] else 'auffällig'

        rnd = r.random()
        aktSample['schulische_unterstuetzung'] = 'vorhanden' if rnd < schulische_unterstuetzung['vorhanden'] else 'mangelhaft'

        # Sample aggressives Verhalten
        key_aggr = f"{aktSample['familiaeres_uUmfeld']},{aktSample['psychische_gesundheit']}"
        rnd = r.random()
        aktSample['aggressives_verhalten'] = 'aggressivja' if rnd <= aggressives_verhalten[key_aggr]['aggressivja'] else 'aggressivnein'

        # Sample soziale isolation
        key_soz = f"{aktSample['familiaeres_uUmfeld']},{aktSample['psychische_gesundheit']}"
        rnd = r.random()
        aktSample['soziale_isolation'] = 'sozialisoliertja' if rnd < soziale_isolation[key_soz]['sozialisoliertja'] else 'sozialisoliertnein'

        # Sample Leistungsabfall
        key_leist = f"{aktSample['psychische_gesundheit']},{aktSample['schulische_unterstuetzung']}"
        rnd = r.random()
        aktSample['leistungsabfall'] = 'leistungsabfallja' if rnd < leistungsabfall[key_leist]['leistungsabfallja'] else 'leistungsabfallnein'

        # Sample warnsignale im Gespräch
        key_warn = f"{aktSample['aggressives_verhalten']},{aktSample['soziale_isolation']}"
        rnd = r.random()
        aktSample['warnsignale_im_gespraech'] = 'warnsignaleja' if rnd < warnsignale_im_gespraech[key_warn]['warnsignaleja'] else 'warnsignalenein'

        # Sample vorherige Vorfälle
        rnd = r.random()
        aktSample['vorherige_vorfaelle'] = 'vorherigefaelleja' if rnd < vorherige_vorfaelle[aktSample['aggressives_verhalten']]['vorherigefaelleja'] else 'vorherigefaellenein'

        # Sample Zielvariable
        key_gefahr = (f"{aktSample['aggressives_verhalten']},{aktSample['soziale_isolation']},{aktSample['leistungsabfall']},{aktSample['warnsignale_im_gespraech']},{aktSample['vorherige_vorfaelle']}")
        rnd = r.random()
        if rnd < gefahrenpotential[key_gefahr]['gefahrniedrig']:
            aktSample['gefahrenpotential'] = 'gefahrniedrig'
        elif rnd < gefahrenpotential[key_gefahr]['gefahrniedrig'] + gefahrenpotential[key_gefahr]['gefahrmittel']:
            aktSample['gefahrenpotential'] = 'gefahrmittel'
        else:
            aktSample['gefahrenpotential'] = 'gefahrhoch'

        samplelist.append(aktSample)

    return samplelist

def calculate_conditional_probability(samples, condition_node, condition_value):
    conditioned_samples = [s for s in samples if s[condition_node] == condition_value]
    if not conditioned_samples:
        return 0.0
    high_risk_conditioned = [s for s in conditioned_samples if s['gefahrenpotential'] == 'gefahrhoch']
    return len(high_risk_conditioned) / len(conditioned_samples)

st.title('Netzwerk zur Gefährdervorhersage')

# Eingabefelder für die A-priori-Wahrscheinlichkeiten
st.sidebar.header('Beobachtungsparameter für die Person')

p_familiaeres_stabil = st.sidebar.slider('Wahrscheinlichkeit für ein stabiles familiäres Umfeld:', 0.0, 1.0, 0.7)
p_psychische_unauffaellig = st.sidebar.slider('Wahrscheinlichkeit für unauffällige psychische Gesundheit:', 0.0, 1.0, 0.96)
p_schulische_unterstuetzung_vorhanden = st.sidebar.slider('Wahrscheinlichkeit für vorhandene schulische Unterstützung oder Inanspruchnahme:', 0.0, 1.0, 0.55)

# Aktualisiere die A-priori-Knoten basierend auf den Eingaben
familiaeres_uUmfeld['stabil'] = p_familiaeres_stabil
familiaeres_uUmfeld['instabil'] = 1.0 - p_familiaeres_stabil
psychische_gesundheit['unauffällig'] = p_psychische_unauffaellig
psychische_gesundheit['auffällig'] = 1.0 - p_psychische_unauffaellig
schulische_unterstuetzung['vorhanden'] = p_schulische_unterstuetzung_vorhanden
schulische_unterstuetzung['mangelhaft'] = 1.0 - p_schulische_unterstuetzung_vorhanden

num_samples = st.slider('Anzahl der Stichproben:', min_value=100, max_value=100000, value=1000, step=50)

if st.button('Vorhersage starten'):
    with st.spinner(f'Führe {num_samples} Simulationen durch...'):
        sampled_data = forward_sampling(num_samples)

        # Berechne die Wahrscheinlichkeiten des Gefahrenpotenzials
        gefahr_counts = {'gefahrniedrig': 0, 'gefahrmittel': 0, 'gefahrhoch': 0}
        for s in sampled_data:
            if 'gefahrenpotential' in s:
                gefahr_counts[s['gefahrenpotential']] += 1

        total_samples = len(sampled_data)
        if total_samples > 0:
            probabilities = {
                'niedrig': gefahr_counts['gefahrniedrig'] / total_samples,
                'mittel': gefahr_counts['gefahrmittel'] / total_samples,
                'hoch': gefahr_counts['gefahrhoch'] / total_samples
            }

            st.subheader('Wahrscheinlichkeiten des Gefahrenpotenzials:')
            prob_df = pd.DataFrame(list(probabilities.items()), columns=['Gefahrenpotenzial', 'Wahrscheinlichkeit'])
            chart_gefahr = alt.Chart(prob_df).mark_bar().encode(
                x=alt.X('Wahrscheinlichkeit:Q', axis=alt.Axis(format='%')),
                y=alt.Y('Gefahrenpotenzial:N', sort='-x', title='Gefahrenpotenzial'),
                tooltip=['Gefahrenpotenzial', alt.Tooltip('Wahrscheinlichkeit', format='.2%')]
            ).properties(
                title='Verteilung des Gefahrenpotenzials'
            )
            st.altair_chart(chart_gefahr, use_container_width=True)

            # Berechne die bedingten Wahrscheinlichkeiten für hohes Gefahrenpotenzial
            conditional_probs = {}
            for node in ['familiaeres_uUmfeld', 'psychische_gesundheit', 'schulische_unterstuetzung',
                         'aggressives_verhalten', 'soziale_isolation', 'leistungsabfall',
                         'warnsignale_im_gespraech', 'vorherige_vorfaelle']:
                unique_values = sorted(list(set(s[node] for s in sampled_data if node in s)))
                for value in unique_values:
                    prob = calculate_conditional_probability(sampled_data, node, value)
                    conditional_probs[f"P(hoch | {node}={value})"] = prob

            conditional_df = pd.DataFrame(list(conditional_probs.items()), columns=['Bedingung', 'Wahrscheinlichkeit für hohes Gefahrenpotenzial'])
            conditional_df_sorted = conditional_df.sort_values(by='Wahrscheinlichkeit für hohes Gefahrenpotenzial', ascending=False).reset_index(drop=True)

            st.subheader('Bedingte Wahrscheinlichkeit für hohes Gefahrenpotenzial (Hervorgehoben):')

            # Funktion zum Hervorheben der höchsten Wahrscheinlichkeiten
            def highlight_max(s):
                is_max = s == s.max()
                return ['background-color: yellow' if v else '' for v in is_max]

            st.dataframe(conditional_df_sorted.style.apply(highlight_max, subset=['Wahrscheinlichkeit für hohes Gefahrenpotenzial']).format({'Wahrscheinlichkeit für hohes Gefahrenpotenzial': '{:.2f}'}))

            st.subheader('Psychologisches Profil:')
            profile_data = {}

            def calculate_node_probabilities_named(samples, node_name, value_map):
                counts = {value: 0 for value in value_map.keys()}
                for sample in samples:
                    if node_name in sample:
                        for internal_value, display_name in value_map.items():
                            if sample[node_name] == internal_value:
                                counts[display_name] += 1
                                break
                total = len(samples)
                return {display_name: count / total if total > 0 else 0 for display_name, count in counts.items()}

            profile_data['Familiäres Umfeld'] = calculate_node_probabilities_named(sampled_data, 'familiaeres_uUmfeld', {'stabil': 'Stabiles Umfeld', 'instabil': 'Instabiles Umfeld'})
            profile_data['Psychische Gesundheit'] = calculate_node_probabilities_named(sampled_data, 'psychische_gesundheit', {'unauffällig': 'Unauffällig', 'auffällig': 'Auffällig'})
            profile_data['Schulische Unterstützung'] = calculate_node_probabilities_named(sampled_data, 'schulische_unterstuetzung', {'vorhanden': 'Vorhanden', 'mangelhaft': 'Mangelhaft'})
            profile_data['Aggressives Verhalten'] = calculate_node_probabilities_named(sampled_data, 'aggressives_verhalten', {'aggressivja': 'Ja', 'aggressivnein': 'Nein'})
            profile_data['Soziale Isolation'] = calculate_node_probabilities_named(sampled_data, 'soziale_isolation', {'sozialisoliertja': 'Ja', 'sozialisoliertnein': 'Nein'})
            profile_data['Leistungsabfall'] = calculate_node_probabilities_named(sampled_data, 'leistungsabfall', {'leistungsabfallja': 'Ja', 'leistungsabfallnein': 'Nein'})
            profile_data['Warnsignale im Gespräch'] = calculate_node_probabilities_named(sampled_data, 'warnsignale_im_gespraech', {'warnsignaleja': 'Ja', 'warnsignalenein': 'Nein'})
            profile_data['Vorherige Vorfälle'] = calculate_node_probabilities_named(sampled_data, 'vorherige_vorfaelle', {'vorherigefaelleja': 'Ja', 'vorherigefaellenein': 'Nein'})
            profile_data['Gefahrenpotenzial'] = {'Niedrig': probabilities['niedrig'], 'Mittel': probabilities['mittel'], 'Hoch': probabilities['hoch']}

            st.subheader('Psychologisches Profil (Visualisierung):')
            profile_df = pd.DataFrame.from_dict(profile_data, orient='index')
            for index, row in profile_df.iterrows():
                st.markdown(f"**{index}**")
                chart_data = pd.DataFrame({'Zustand': row.index, 'Wahrscheinlichkeit': row.values})
                chart = alt.Chart(chart_data).mark_bar().encode(
                    x=alt.X('Wahrscheinlichkeit:Q', axis=alt.Axis(format='%')),
                    y=alt.Y('Zustand:N', sort='-x'),
                    color=alt.Color('Wahrscheinlichkeit:Q', scale=alt.Scale(range=['lightblue', 'darkblue'])),
                    tooltip=['Zustand', alt.Tooltip('Wahrscheinlichkeit', format='.2%')]
                ).properties(
                    title=index
                )
                st.altair_chart(chart, use_container_width=True)

        else:
            st.warning('Es wurden keine Stichproben generiert.')
            profile_data = {}
