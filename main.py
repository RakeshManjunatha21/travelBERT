import streamlit as st
import pandas as pd
import numpy as np
import re
import os
import json
import google.generativeai as genai
import requests
import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode, GridUpdateMode


def TravelScore(text:str):
    senti_analysis_prompt = f"""Analyse the following list of feedback '{text}' and generate Below
    1. What is the Probablity Score of people visiting that place. (Just give one score from 0 to 100% based on Negative aspects and Positive aspects) //Heading: Probalility Score of People Visiting
    2. What is the Negative Aspect, how can a Travel Agence Improve.
    only give above two

    """
    return senti_analysis_prompt

def llm():
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
    gemini_model = genai.GenerativeModel("gemini-pro",
                                         generation_config=genai.types.GenerationConfig(
                                             max_output_tokens=64000,
                                             temperature=0.0
                                         ))
    return gemini_model

def responseFunc(prompt):
    model = llm()
    response = model.generate_content(prompt)
    return response


# Dataset
data = {
    "Questions": [
"Top 5 trekking place in india?",
"The Himalayan region",
"The Western Ghats",
"The Eastern Ghats",
"The Markha Valley",
"The Valley of Flowers",
"Top 5 temples to visit in tamil nadu?",
"I want to visit some waterfalls places in india?",
"Shimla NORTH Himachal Pradesh",
"Manali   NORTH  Himachal Pradesh",
"Haridwar and Rishikesh Uttarakhand",
"Amritsar  Punjab",
"Varanasi Uttar Pradesh",
"Leh-Ladakh Jammu Kashmir",
"Coorg Karnataka",
"Kodaikanal   Tamil Nadu",
"Ooty Tamil Nadu",
"Hampi  Karnataka",
"Wayanad Kerala",
"Visakhapatnam",
"GOA"

    ],
    "Suggestions": [
"The Himalayan region: This region is home to some of the highest peaks in the world, including Mount Everest, and offers a wide range of trekking routes for all levels of experience @ The Western Ghats: Located in southwestern India, the Western Ghats are a mountain range that offers a diverse range of trekking trails, from easy to challenging @ The Eastern Ghats: These mountains, located in eastern India, are known for their picturesque waterfalls and forests, and offer a variety of trekking routes @ The Markha Valley: Located in Ladakh, this popular trekking destination offers stunning views of the Himalayas and passes through several traditional villages, @ The Valley of Flowers: Located in Uttarakhand, this beautiful valley is home to a wide variety of flora and fauna, and offers several trekking routes for nature enthusiasts",
"Himalayan Treks is the company you want to go on a hike. They are experienced, professional and with a good sense of the culture that is so present in Nepal. You first come to Nepal for the mountains but from then on you come for the people. Himalayan Treks knows this and brings people together for very memorable moments. Thank you so much Eva and all the others for the once-in-a-lifetime adventure @ One of the most amazing life changing events of my life with Himalayan Treks. Thank you so much. I’ve been on a lot of excursions and have done a lot of travelling before but have never had an experience.",
"There are no summer treks in the Western Ghats, You cannot trek in the Western Ghats in the monsoons @ Treks in the Western Ghats are easy, awesome experience",
"In some parts of the Eastern Ghats, the trekking infrastructure may be limited, which can make it difficult to find accommodations and other services along the way @ The weather in the Eastern Ghats can be unpredictable, and you may encounter heavy rain or other adverse conditions during your trek. It's important to plan accordingly and be prepared for potential weather challenges @ The Eastern Ghats are known for their waterfalls, forests, and wildlife, which can make for a beautiful and scenic trekking experience.",
"The Markha Valley is known for its beautiful landscapes, including snow-capped peaks, rugged mountains, and picturesque villages. @ The Markha Valley trek takes place at high altitudes, and some people may experience altitude sickness. It's important to acclimatize properly and take necessary precautions to avoid altitude sickness.",
"The Valley of Flowers is located in a remote area, and accessing it can be challenging. You may need to travel long distances to get to the starting point of your trek. @ The Valley of Flowers is a popular trekking destination, and you may encounter crowds of people during the peak season. This can be a challenge if you are looking for a more solitary trekking experience",
"Brihadeeswarar Temple: Located in Thanjavur, this temple is a UNESCO World Heritage Site and is known for its towering gopuram (gateway tower) and intricate carvings.@Meenakshi Temple: Located in Madurai, this temple is dedicated to the goddess Meenakshi and is known for its beautiful architecture and sculptures.@Ranganathaswamy Temple: Located in Srirangam, this temple is one of the largest temple complexes in India and is dedicated to the Hindu god Vishnu.@Nataraja Temple: Located in Chidambaram, this temple is dedicated to the Hindu god Shiva and is known for its beautiful sculptures and brass image of Nataraja, the dancing form of Shiva.@Rameshwaram Temple: Located on the island of Rameswaram, this temple is an important pilgrimage site for Hindus and is known for its long corridors and tall gopurams.",
"Jog Falls: Located in Karnataka, these are the tallest waterfalls in India, with a height of over 830 feet.@Nohkalikai Falls: Located in Meghalaya, these are the tallest plunge waterfalls in India, with a height of over 1100 feet.@Kempty Falls: Located in Uttarakhand, these are among the most popular waterfalls in India and are known for their picturesque setting.@Athirapally Falls: Located in Kerala, these waterfalls are known for their scenic beauty and are a popular spot for swimming and picnicking.@Dhuandhar Falls: Located in Madhya Pradesh, these waterfalls are known for the mist and foam that forms at the base of the falls, giving them a unique and dramatic appearance.",
"Queen of hills @  This hill station is well-connected to some of the main cities in the country. @ Best Time to Visit: March to June. November to February is ideal for experiencing snowfall and enjoying snow-related adventure activities @ Trekking, paragliding, skydiving, bunjee jumping like activities easily available. @  plenty of accommodation options in the hill station @ Weather is decent. Can vary from -5°C to 35°C. It's clean, beautiful and quite safe. If you want peace, stay in himachal. @ Kasol and shimla @ Water crisis @ Narrow roads @ Less parking space @ more crowded and congested during peak tourist season",
"This hill station is less crowded since it's a bit further away from some of the main cities @  Manali is more for adventure seekers and best visited during winter season @ bring your own vehicle for convenience as the attractions here are far from each other@Manali is full of snow and mesmerizing snowcapped mountains which would blow your mind completely @ you need to carry some winter’s stuff ",
"Best Time to Visit: March to June and October to NovemberConsidered to be twin national heritage cities, Haridwar and Rishikesh have a spiritual aura that attracts soul seekers and pilgrims from across the world. @ Ganges is meditated upon @ white rapids call out to thrill-seekers making it one of the most popular adventure spots in North India @ towns have a vegetarian food culture and are known for delicious street food spread @ large chunk of plastic waste flows into the local water bodies, including the Ganges @ result of the breakage of the glacier which caused a swell in the river water leading to flooding and subsequently destroying many houses on the riverside.",
"Reach the city maximum at 5 am or 5.30 am in the morning! @ Great food at highly affordable price @ Most beautiful women i have ever seen @ High pollution level and dust on the roads @ Problem of drugs and alcohol. Eve teasing and chain snatching is common @  you can get each and everything at one place ",
"one of the cities -oldest than history it just feels unexplainable@Alcohol and non-vegetarian food are not allowed here@Alcohol and non-vegetarian food are not allowed here@Varanasi can get cold during the winter months so remember to bring a shawl or sweater for chilly morning boat trips@booking a pickup from the airport or train station for your arrival for less hassle and avoid a few scams.there are many businessmen (and women) who will be all too happy to overcharge you, and scams abound@One of the must-do’s of any visit to Varanasi is taking a boat trip on the river Ganges. There are two best times of day to do this: For sunrise, and in the evening to see the the Ganga aarti that takes place each evening on the Dasaswamedh Ghat from the water.@Charming Musical Events@Pocket-Friendly Place@Mesmerizing Ganga Aarti ( offering of lighted Diya)@Captivating Temples and Forts@ Enthralling and Unique Rituals@Enchanting Ghats (river landing steps or passage)",
"Best Time to Visit: April to September. November to March offers a unique chance to see the lakes frozen into solid ice @ The sunshine of the Kashmir valley particularly high altitudes like Gulmarg can be very harsh to your skin and you might easily get sun burn so don’t forget to apply a thick coat of sunscreen before you go out during summers.@climate of Kashmir is varied, very cold in winter and blazing sunny in summer@SIM card is not going to work in Kashmir as roaming is blocked  due to what India claims as security reasons.  If you’re a foreigner, your hotel owner might provide you with a local sim or you can easily purchase a local sim card from mobile telecom operators.@there’s a lot of electricity crisis in Kashmir, make sure you carry a torch with you.@ Don’t discuss with your driver or guide your shopping list. Go shop on your own.@scenic splendour @ snow-capped mountains, plentiful wildlife, exquisite monuments, hospitable people and local handicrafts.",
"Best Time to Visit: October to March@an alluring hill station in Karnataka, blessed with mesmerizing waterfalls, towering hills, scenic views, and sprawling coffee plantations. Referred to as ‘the Scotland of India@India’s second-largest Tibetan settlement@whitewater rafting. During monsoons, it can be a challenging yet thrilling activity to indulge in.@Coorg has all those expensive resorts and hotels where one can splurge, and make your trip worth it. Most of them are between Madikeri ( the main town ) and Kushal Nagar ( 30 kms apart ) @Bylakuppe Tibetan Monastery : Huge and beautiful, it definitely is worth a visit. Its near Kushal Nagar.@Its an extremely overrated tourist destination, with literally no decent tourist spot. @‘Abbey Falls’ is literally the saddest waterfall ever. You cant even go and take a dip in the water.@There are hardly any good food options. No cafes, only restaurants serving Coorg cuisine ( Mostly non veg ) and North Indian – South Indian food. Food is most definitely better at the hotels, which serve all kinds of cuisines.",
"The cool breeze of Kodaikanal, a hill town in Tamil Nadu, is a welcome respite from the humidity typically associated with southern India@hill station is rightly called the Princess of Hill Stations.@hill station is rightly called the Princess of Hill Stations.@Using water infested with weed can lead to serious health problems@ there aren't many things to view@There are fewer hotels and guesthouses to choose from. If you’re going to be here on a weekend, be sure you reserve your room in advance.@ Boating on the lake or hiking to the lookout spots is the only options for visitors.@Trekking to Dolphin’s Nose in Kodaikanal is one of the most exciting things to do in the area. The cliff of Dolphin Nose is a breathtaking sight to see as you journey through the lush woodlands and well indicated pathways.@One kilometre of Coakers Walk provides amazing views of the city, mountains, and valleys. Enjoy the designated pedestrian path for cycling and the Telescopic house for panoramic views of Kodaikanal.@Less pollution due to better weather.A more authentic, ‘closer to nature,’ and less marketed experience.Compared to Ooty, hotel rates and taxi charges are cheaper.",
"Best Time to Visit: October to June@Ooty, the Queen of Hill Stations, balances the hustle and bustle of city life with expansive tea gardens.@The charming bungalows from the British-Raj era add a romantic flavor to Ooty, making it one of the most popular honeymoon destinations in South India.@Good road connectivity with all major cities and towns in South India.@Good road connectivity with all major cities and towns in South India.@Good road connectivity with all major cities and towns in South India.@Too much commercialized. Nature takes a back-seat.@Too many tourists. If you are looking for a relaxing trip away from the mad rush of tourists, Ooty may not be the ideal choice.@Too many tourists. If you are looking for a relaxing trip away from the mad rush of tourists, Ooty may not be the ideal choice.",
"One of India's top historical destinations @Hampi is home to more than 2000 stunning monuments that have stood the test of time@Hampi as the favourite playground for those into bouldering and rock climbing@You can book a stay at one of Hampi’s quirky and uber-relaxing guesthouses and chill out after a full day of exploring.@you can take a boat trip in a Dongi, a bowl-shaped boat made of reed, saplings and hide.@monument have been facing serious damage from illegal quarrying and rampant blasting activities.@Be prepared for harsh weather",
"his area is famous for hills, forests and rivers@The food that is available here is so tasty and healthy@It is a clean and maintained city with the beauty of the nature@Lush green coffee estates, Pepper plantation, Supari and Coconut groves are amazing. Small town lifestyle, beautiful and clean settlements of people, narrow winding roads, pleasant weather.",
"known as Vizag, is one of the oldest port cities in the country. @known as Vizag, is one of the oldest port cities in the country. @a lot cleaner and a lot less crowded than other famous beaches along the Indian coastline,@ a lot cleaner and a lot less crowded than other famous beaches along the Indian coastline,@a lot cleaner and a lot less crowded than other famous beaches along the Indian coastline,@ During summer it would be really humid even though the temperature may not reach 40(it does go beyond 40)@air quality in vizag is relatively bad due to industries which use a ton of coal and due to port. @air quality in vizag is relatively bad due to industries which use a ton of coal and due to port.",
"Goa offers you the very enticing option of renting a bike and getting around. @Goa is completely safe to explore at night. You will be thrilled with the late-night parties on the beaches and water sports.@there are many museums in Goa where photography is banned, along with many temples, churches, caves, and forts.@Goa houses one of the best shopping destinations and is a shopaholic’s dream place as well.@The best time of visit in Goa is between the months of October and March.@There are some of the beaches in Goa where swimming is not really allowed. It is because of the frequent high waves in the sea. Moreover, you have to be cautious when facing high waves for safety reasons." 
    ]
}

df = pd.DataFrame(data)

# Streamlit app title
st.title('Choose a Place to Visit in India')


# Option to select a place
place = st.selectbox("Select the place you want to visit", df["Questions"])

if st.button('Submit'):

    # Filter dataframe based on selected place
    selected_suggestions = df[df["Questions"] == place]["Suggestions"].iloc[0].split("@")

    # Convert suggestions to dataframe
    suggestions_df = pd.DataFrame({"Suggestions": selected_suggestions})

    # Add a column for thumbs up/down
    suggestions_df["Thumbs"] = ""

    # Display suggestions with thumbs up/down buttons

    st.write("Suggestions:")
    gb = GridOptionsBuilder.from_dataframe(suggestions_df)
    thumbs_renderer = JsCode('''
        class ThumbRenderer {
            init(params) {
                this.params = params;
                this.eGui = document.createElement('span');
                if (params.value === '👍') {
                    this.eGui.innerHTML = '👍';
                } else if (params.value === '👎') {
                    this.eGui.innerHTML = '👎';
                } else {
                    this.eGui.innerHTML = 'None';
                }
            }

            getGui() {
                return this.eGui;
            }

            refresh(params) {
                return false;
            }
        }
    ''')

    button_handler = JsCode('''
        function onCellClicked(params) {
            if (params.colDef.field === 'Thumbs') {
                let newValue = params.value === '👍' ? '👎' : '👍';
                params.api.applyTransaction({ update: [{ ...params.data, Thumbs: newValue }] });
            }
        }
    ''')

    # gb.configure_column('Thumbs', cellRenderer=thumbs_renderer, onCellClicked=button_handler, editable=False,wrapText=True)
    # grid_options = gb.build()
    # gb.configure_column('Thumbs', cellRenderer=thumbs_renderer, onCellClicked=button_handler, editable=False)

    # Configure the 'Suggestions' column with text wrapping enabled
    gb.configure_column('Thumbs', cellRenderer=thumbs_renderer, onCellClicked=button_handler, editable=False)

    # Configure the 'Suggestions' column with text wrapping enabled
    gb.configure_column('Suggestions', wrapText=True, autoHeight=True)
    grid_options = gb.build()

    response = AgGrid(
        suggestions_df,
        gridOptions=grid_options,
        update_mode=GridUpdateMode.MODEL_CHANGED,
        fit_columns_on_grid_load=True,
        allow_unsafe_jscode=True,
        height=200,
        width='100%',
    )

    # Retrieve updated DataFrame after interaction
    updated_suggestions_df = pd.DataFrame(response['data'])

    #Feedback
    GeminiKeys = [
        "AIzaSyCcVUOyL2M9aNRUhgO6lzTAJ-BjOUXZrt0",
        "AIzaSyC9JxomOkNel9uy0qdqixDcI6UH6KhMcho"
    ]
    os.environ["GOOGLE_API_KEY"] = GeminiKeys[0]
    cmt = []
    for val in suggestions_df['Suggestions']:
        cmt.append(val)
    cmtnd = cmt[:10]
    prompt = TravelScore(cmtnd)
    response = responseFunc(prompt)
    llm_response  = response.text
    st.success(llm_response)


    
feedback_message = st.text_area('Your Feedback', help='Enter your feedback here')

# Button to submit feedback
if st.button('Submit Feedback'):
    # You can add your logic here to save the feedback data to a database or file
    st.success('Thank you for your feedback!')



