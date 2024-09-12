import pandas as pd
import streamlit as st
import time
import numpy as np
import plotly.express as px


# The title
st.title(":blue[Vehicle Market in the USA]")

# The subtitle
st.write('Filter the data below to see the ads by manufacturer')

# The data frame
vehicles = pd.read_csv('vehicles_us.csv')


vehicles['model_year'] = vehicles['model_year'].astype('Int64', errors='ignore')


# The extraction of the 'brand' name from the 'model' column:
def extract_brand(name123):
    name_parts = str(name123).split(' ')
    return name_parts[0]


vehicles['brand'] = vehicles['model'].apply(extract_brand)

colors = vehicles.groupby(['brand', 'model_year'])['paint_color'].apply(lambda x: x.mode()[0] if not x.mode().empty else None).reset_index().rename(columns={'paint_color': 'most_common_color'})


vehicles = vehicles.merge(colors, on=['model_year', 'brand'], how='left')


vehicles['paint_color'] = vehicles['paint_color'].fillna(vehicles['most_common_color'])


manufacturer_choice = vehicles['brand'].unique()

# Select manufacterer bottom section
#vehicles['model_year'] = vehicles['model_year'].astype('Int64', errors='ignore')
select_menu = st.selectbox('Select a brand', manufacturer_choice)
# Slider section below:
min_year, max_year = int(vehicles['model_year'].min()), int(vehicles['model_year'].max())
year_range = st.slider("Choose a range of years", value=(min_year, max_year), min_value=min_year,max_value= max_year)

#Dataframe

actual_range = list(range(year_range[0], year_range[1]+1))
vehicles_filtered = vehicles[(vehicles.brand == select_menu) & (vehicles.model_year.isin(list(actual_range)))]

# Formatting
#vehicles_filtered = vehicles_filtered.style.format({
#    'price': '${:,.2f}',  # Format as dollar amount with two decimal places
#}).format({
#    'model_year': lambda x: f"{x:.0f}"  # Remove commas from years (treated as float/int)
#})
vehicles_filtered

# Price Analysis section starts here:

st.header(':heavy_dollar_sign::moneybag: :green[Price Analysis] :moneybag::heavy_dollar_sign:')
st.write(""" **Let's analyze what influences price the most** :mag:""")
st.write(""" _See below how distribution of price varies depending on 
         **brand**, **transmission**, **body type** and **:blue[c]:orange[o]:green[l]:orange[o]:green[r]**._ """)

list_of_hist = ['brand', 'transmission', 'type', 'paint_color']
select_type = st.selectbox('Split for Price Distribution', list_of_hist)

fig1 = px.histogram(vehicles, x=select_type, y="price", color="brand", log_y=True)
fig1.update_layout(title="Split of price by", xaxis_title="Type of Car", yaxis_title="Price")
st.plotly_chart(fig1)

if select_type == 'brand':
    st.write("""**This graphic shows the average price of different car brands**     
             Ford has the highest average price, followed by Chevrolet and Toyota.   
             The lowest average price is for Acura. Overall, the prices are clustered around the 10 million mark, with some brands having higher average prices than others.""")
elif select_type == 'transmission':
    st.write("""**This chart shows the average price of cars with different transmission types**    
             Cars with automatic transmission are more expensive than cars with manual transmission and other types of transmission.  
             The average price of cars with automatic transmission is over 1 billion.  
             The average price of cars with manual transmission is around 50 million and the average price of cars with other types of transmission is around 25 million.  
             It seems that the automatic transmission is a common choice when it comes to price and luxury.""")
elif select_type == 'type':
    st.write("""**This graphic shows the average price of cars by type of car**    
             The average price is highest for SUVs, followed by sedans and trucks.  
             The average price is lowest for buses and other types of cars.  
             The average prices of vans, hatchbacks, pickups, and convertibles are similar to one another, and all are around 50 million.  
             The average prices of coupes and minivans are also similar to one another, and are around 20 million.  
             Overall, the average price of cars varies depending on the type of car.""")
elif select_type == 'paint_color':
    st.write("""**This chart shows the average price of cars by paint color**  
             The acumulation of all the prices for black and white cars are the highest, around 100 million.  
            The acumulation of all the prices for purple cars are the lowest, around 1 million.    
            Also we can see that Ford and Chevrolet sold all the colors evenly distributed, being Ford the one who acumulates most of the prices.  
            Toyota and Mecedes Benz cars are usually painted gray or silver 
            BMW black cars are more sold with the sum of price of 1 million and BMW purple cars are less sold with a sum of price of 5500.   
             It seems that :red[the color of a car does not have a significant impact on its price].  
            Although car color appears to reveal minimal impact on price, black and white paint colors sells the most while orange and purple paint colors sells the least. .""")
else:
    st.write("""No conclusion""")


#Scatter section
# Calculating the median price for odometer
average_pricein_odometer = vehicles.groupby(['brand', 'odometer'])['price'].median().reset_index()

fig2 = px.scatter(average_pricein_odometer, x="odometer", y="price", color="brand", log_y=True, log_x=True)
fig2.update_layout(title_text='Median Price by Vehicle Brand and Odometer', xaxis_title='Odometer', yaxis_title='Median Price')
st.plotly_chart(fig2)
#fig2.show()

#Conclusion of odometer scatter plot
odometer_conclusion = st.checkbox("Click on this checkbox to comprehend more about the median price by Vehicle Brand and Odometer.")
if odometer_conclusion:
    st.write("""A significant drop in price is noticeable as odometer readings increase from low to mid-range (10 to 100k).   
             After this range, the decrease in price becomes less steep, indicating that the initial mileage has a more substantial impact on price depreciation.   
             The graph effectively demonstrates the expected negative correlation between odometer readings and vehicle prices, with significant variability between different brands.   
             It also highlights how certain brands maintain their value better over time, providing useful insights for consumers looking to buy or sell vehicles based on mileage and brand reputation.""")


# Model histogram
fig3 = px.histogram(vehicles, x="model", y="price", color="brand", log_y=True)
fig3.update_layout(title="Split of price by Model", xaxis_title="Model Name", yaxis_title="Price")
st.plotly_chart(fig3)
#fig1.show()

# Conclusion of Model Histogram
model_conclusion = st.checkbox("Click on this checkbox to see more about Split of price by Model.") 
if model_conclusion:
    st.write("""This chart illustrates the diversity and price distribution of vehicle models by brand.  
             Ford has the most extensive range of models and price points, with some models showing significantly higher prices.  
             Other brands like Toyota, Honda, and Kia show more consistent pricing within their ranges, highlighting their respective market positions.""")




# The Psychology Behind Car Color
st.header(':red_car: Ψ PSYCHOLOGY OF COLOR IN CARS Ψ :blue_car:')
st.image("https://miro.medium.com/v2/resize:fit:1400/format:webp/1*RcVl8m737uHs4JP0UgE92A.jpeg", caption="Although the color of the car has no significant impact on its price, psychologically speaking it does have an impact on the personality of the owner.", use_column_width=True)
st.write(""" :rainbow:**Select a car color and see the psychological meaning behind it** :rainbow:""")
# Checkbox bottom black
choose_color_black = st.checkbox(":black_heart: Black Car")
if choose_color_black:
    st.write("""The color black is associated with a variety of psychological traits, including **power**, **sophistication**, and **elegance**. 
 
**Power and authority**:
Black is a color that symbolizes authority and power, and is often associated with success in business settings. 
 
**Confidence**:
People who drive black cars may be perceived as confident and sophisticated, and may value professionalism and luxury. 
 
**Enigma**:
Black can also exude an air of mystery, and is seen as a statement of class and power. 
 
**Rebelliousness**:
Some say that people who drive black cars may be rebellious. 
 
**Conservatism**:
People who drive black cars may value order and rules, and tend to be conservative. 
 
However, black cars can also have **lower visibility** and **conspicuity**, making them **harder for other drivers to see**, especially in low light conditions. 
""" )
    

#Checkbox bottom grey
choose_color_gray = st.checkbox(":white_heart: Gray Car")
if choose_color_gray:
    st.write("""**Stability and reliability**:
Gray is associated with psychological neutrality, stability, and reliability. Drivers of gray cars are often considered to be safe and responsible drivers who are unlikely to show road rage or erratic driving behavior. 
 
**Modesty and humility**:
Gray cars are associated with people who are **modest** and **humble**, and who don't want to stand out. 
 
**Practicality and caution**:
Gray is a color that represents compromise and caution.  
Drivers of gray cars are often seen as people who **recognize usefulness over appearance**, and who consider things more for all intents and purposes. 
 
**Levelheadedness**:
Gray cars are associated with people who are levelheaded, and who talk out problems. 
 
**Quiet lifestyle**:
Gray is a muted color that is often associated with people who prefer a quiet lifestyle. """)


# Checkbox bottom brown 
choose_color_brown = st.checkbox(""":brown_heart: Brown Car""")
if choose_color_brown:
    st.write("""According to color psychology, drivers of brown cars are often seen as **down to earth**, **reliable**, and **comfortable**. 
 
**Longevity**: Brown and beige cars can symbolize longevity, and drivers may keep their car until it's no longer functional. 
 
**Comfort** and **reliability**: Drivers of brown cars may prioritize comfort and reliability over flashy colors. 
 
**Fiscal responsibility**: Drivers of brown cars may be fiscally responsible and may not be tempted by flashy gadgets. 
 
**Calm driving style**: Drivers of brown cars may have a calm and smooth driving style and avoid aggressive encounters on the road. 
 
**Helping others**: Drivers of brown cars may be the first to stop to help other road users. 
 
**Honesty**: Drivers of brown cars may be humble, honest, and frugal. 
 
**Simple**: Drivers of brown cars may be simple and not bothered by following trends. 
 
**Practical**: Drivers of brown cars may be practical and not care what others think of them. 
 
**Good at budgeting**: Drivers of brown cars may be good at budgeting due to their level-headed mindset. 
""") 

# Checkbox bottom white
choose_color_white = st.checkbox(":white_heart: White Car")
if choose_color_white:
    st.write("""**Purity and modernity**: White cars can represent **purity**, **perfection**, and **modernity**. 
 
**Cleanliness and order**: White cars are often associated with cleanliness and order, and drivers are thought to be organized and efficient. 
 
**Honesty**: White cars can represent honesty, and drivers are thought to be honest in their personal and professional lives. 
 
**Calmness**: White cars can reflect sunlight, which can provide a sense of coolness and energy efficiency. Drivers of white cars are thought to be calmer. 
 
**Friendliness**: White cars can make drivers seem friendly yet classy. 
 
**Practicality**: White cars can suggest practicality and a sense of responsibility, making them a common choice for family vehicles. 
 
**Contemporary vibe**: White cars can reflect style, taste, and a craving to stick out.""")

#Checkbox bottom Red
choose_color_red = st.checkbox(":heart: Red Car")
if choose_color_red:
    st.write("""The color red has a strong psychological influence on people: 
 
**Personality**: Red cars are associated with people who are **confident**, **extroverted**, and **ambitious**.  
             They may also be seen as **dynamic**, **adventurous**, and **energetic**. 
 
**Attention**: Red cars can be attention-grabbing, which may cause other drivers to be more cautious. 
 
**Business**: In a business setting, a red car can be associated with assertiveness. 
 
**Performance**: Red is often used on performance-oriented cars that are known for their high speeds. 
 
**Love**: Red is also associated with love, passion, and desire. 
 
**Safety**: Red cars are noted as some of the safest on America's roadways. 
""")

#Checkbox bottom Orange
choose_color_orange = st.checkbox(":orange_heart: Orange Car")
if choose_color_orange:
    st.write("""The color of a car can say a lot about the driver, and orange is no exception: 
 
**Optimistic**: People who drive orange cars are often **optimistic** and **adventurous**.  
             They may be more likely to take risks and be overconfident in their driving abilities. 
 
**Extroverted**: Orange car owners are often extroverted and sunny, and enjoy being in the driver's seat. 
 
**Creative**: Orange car drivers are often creative, artistic, and original. 
 
**Unique**: Orange cars are unique and can attract attention. 
 
**Confident**: Orange car drivers may have a similar confident energy to them. 
 
**Fun-loving**: Orange car drivers may be fun-loving adventurers who are looking for something different. 
 
**Individualistic**: Orange car drivers may be individualistic, unique, and value their self-expression. 
 
In general, the color orange is associated with positive words like **warmth**, **security**, **sensuality**, **passion**, **abundance**, **fun**, and **happiness**.""")
    
#Checkbox bottom yellow
choose_color_yellow = st.checkbox(":yellow_heart: Yellow Car")
if choose_color_yellow:
    st.write("""The psychology of yellow cars is associated with **optimism**, **happiness**, and **attention-grabbing**: 
 
**Cheerfulness**: Yellow is the brightest color the human eye can see and is associated with cheerfulness and optimism. 
 
**Attention-grabbing**: Yellow cars are bright and bold on the road, making them stand out and capture the attention of onlookers. 
 
**Creativity and innovation**: Yellow's optimistic and fun connotations make it a popular choice for drivers associated with creativity and innovation. 
 
**Personality**: Yellow car owners are commonly seen as optimistic, outgoing, and full of energy. They tend to radiate positivity, enjoy the little things, and have a zest for life. 
 
**Attracting attention**: People driving yellow cars tend to enjoy attracting other people's attention and value differentiation from others. 
 
**Leading and setting trends**: People driving yellow cars have a relatively strong sense of leading and setting the trends. 
 """)

#Checkbox bottom green
choose_color_green = st.checkbox(":green_heart: Green Car")
if choose_color_green:
    st.write("""The color green can have several psychological associations when applied to a car, including: 
 
**Environmental consciousness**:
Green cars are often associated with **eco-friendliness** and **environmental consciousness**, and are appealing to drivers who want to reduce their carbon footprint. 
 
**Nature lovers**:
Green is the color of nature, and green cars are often associated with nature lovers. 
 
**Strong sense of self**:
Green cars can indicate that the driver has a strong sense of self and doesn't care what others think. 
 
**Independent and unconventional**:
Green cars can be seen as a rebellious choice, and drivers of green cars may be independent and unconventional. 
 
**Making a statement**:
Brighter, bolder shades of green can be seen as a way to make a statement. 
 
The color green can also have a **soothing** and **relaxing effect**, and is known to help **alleviate depression**, **nervousness**, and **anxiety**. 
""")

#Checkbox bottom blue
choose_color_blue = st.checkbox(":blue_heart: Blue Car")
if choose_color_blue:
    st.write("""The color of a car can convey a range of psychological associations, and blue cars are often associated with **calmness**, **stability**, and **trustworthiness**: 
 
**Calmness**:
Blue is a calming color that can have a calming effect on drivers and observers. 
 
**Trustworthiness**:
Blue is seen as a trustworthy and dependable color, making it a good choice for a safe driving experience. 
 
**Openness and freedom**:
Blue is associated with the sky and ocean, which can contribute to a sense of openness and freedom. 
 
**Strength**, **wisdom**, and **trust**:
Blue is seen as a cool and calm color that can express **strength**, **wisdom**, and trust. 
 
**Intelligence** and **creativity**:
People who favor the color blue are likely to be intelligent and creative. 
 
**Introspection**:
Blue is connected to introspection, suggesting that people who own blue cars might be thoughtful and contemplative. 
 
**Stability** and **sensibility**:
Blue is a stable and sensible choice that stands out against more monotone colors on the road. 
 
**Shades of blue**:
Different shades of blue can have different associations, such as light blue, which can enhance feelings of **calmness** and **approachability**, and navy blue, which can exude **authority**. 
 """)

#Checkbox bottom blue
choose_color_purple = st.checkbox(":purple_heart: Purple Car")
if choose_color_purple:
    st.write("""The color of a car can say something about the driver's personality, and purple cars are often associated with **uniqueness**, **creativity**, and a **desire to make a statement**: 
 
**Unique**: Purple car drivers may enjoy being unique and making a statement. 
 
**Creative**: Purple car drivers may be highly creative and have a **unique personality**. 
 
**Authentic**: Purple car drivers may be authentic and unconventional. 
 
**Luxury**: Purple car drivers may gravitate towards luxury and relish a sense of mystery and the unexpected. 
 
The color purple has many associations, including **wisdom**, **royalty**, **power**, **ambition**, and **luxury**.  
             It can also represent **magic**, **extravagance**, **peace**, **pride**, **independence**, and **wealth**. 
""")



result = st.button("Gentle Reminder")
st.write(result)
if result:
    st.header("""_Life is too short to drive boring cars_:face_with_hand_over_mouth:""")