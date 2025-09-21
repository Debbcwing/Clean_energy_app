## Clean Energy App :bubbles:🇨🇭
https://clean-energy-app.streamlit.app/
### Overview

This is a interactive web app (API) to helps users explore, analyze, and visualize clean energy scenarios in Switzerland. It provides interactive tools and data-driven insights to inform decisions related to renewable energy, energy cost for local households, and sustainable practices.
<br><br>
**Data visualization**<br>
A brief geographical summary on clean energy generation in Switzerland among the 26 Cantons including the below information:
- Electrical capacity
- Tariff
- Production
- Facility count
- Production efficiency
<br>

**A simple model for the energy flexibility**<br><br>
A simple conceptual model that targets at single households to showcase the basic mechanism of local energy markets in Switzerland, and also shares what kinds of flexibility products houehold have. The model aims at find an optimal flexibility product based on market information and forecasts (**not applied yet**) to facilitate households' decision-making process. 

<br>

------------------------------------------------------------------------------------------------------------------------------

The structure of the app is as follow:
```
clean-energy-app/
│── Home.py
│── pages/
│   ├── Data_visualization.py
│   ├── Simple_household_model.py
```
