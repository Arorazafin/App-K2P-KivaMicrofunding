# Dash Imports

import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
from dash.dependencies import Input, Output

# tensorflow
import tensorflow as tf
from tensorflow.keras.models import load_model


# Vectorizer & nlp
from sklearn.feature_extraction.text import CountVectorizer 
from sklearn.feature_extraction import text 
from spacy.lang.en.stop_words import STOP_WORDS as en_stop
# nlp tools
import nlp_process as nlp


# Non Dash Imports
import re
import base64
import pandas as pd
import numpy as np 
import joblib 
from app import app



#Load models
path = 'models/'

path_vec = path+'vectorizer_v0.sav'
loaded_vec = CountVectorizer(stop_words = en_stop,
                             analyzer = 'word', 
                             preprocessor=lambda x: re.sub(r'([\n\r\t])|([\d_\d_\d_\d])|([^\x00-\x7F])|(\d[\d\.])+','', x.lower()), 
                             min_df = 10,
                             max_df = 0.70, 
                             vocabulary=joblib.load(open(path_vec, "rb"))
                            )

filename = path+'le_sector_v0.sav'
loaded_le_sector = joblib.load(filename)

filename = path+'le_country_code_v0.sav'
loaded_le_country_code = joblib.load(filename)

filename = path+'le_partner_id_v0.sav'
loaded_le_partner_id = joblib.load(filename)

filename = path+'minMax_v0.sav'
loaded_minMax = joblib.load(filename)

filename = path+'pca_v0.sav'
loaded_pca = joblib.load(filename)

filename = path+'nn_v0.h5'
loaded_nn = load_model(filename)



# Data initial

funded_amount0 = 200
term_in_months0  = 10
sector0 = 'Retail'
country_code0 ='MG'
partner_id0 ='443'
X1_0 = "Lalao thanks the KIVA lenders for her last loan. She was able to diversify her stock with varieties of bracelets and necklaces for her loyal customers. Since she has a lot of orders right now, she has renewed her loan to buy more packs of bracelets and necklaces. Her goal is to develop her business even more."

col_features2 = ['funded_amount','term_in_months', 'sector','country_code','partner_id']

sector =[
 'Agriculture',
 'Arts',
 'Clothing',
 'Construction',
 'Education',
 'Entertainment',
 'Food',
 'Health',
 'Housing',
 'Manufacturing',
 'Personal Use',
 'Retail',
 'Services',
 'Transportation',
 'Wholesale'
]




country_code = [
"AL",
"AM",
"BF",
"BO",
"BR",
"CD",
"CM",
"CO",
"CR",
"DO",
"EC",
"EG",
"FJ",
"GE",
"GH",
"GT",
"HN",
"HT",
"ID",
"IL",
"IN",
"JO",
"KE",
"KG",
"KH",
"LB",
"LR",
"LS",
"MD",
"MG",
"ML",
"MW",
"MX",
"MZ",
"NG",
"NI",
"NP",
"PA",
"PE",
"PG",
"PK",
"PR",
"PS",
"PY",
"RW",
"SB",
"SL",
"SN",
"SV",
"TG",
"TH",
"TJ",
"TL",
"TO",
"TR",
"TZ",
"UG",
"US",
"VN",
"WS",
"XK",
"ZM",
"ZW",
"PH",
 ]

partner_id =[
    "9",
"15",
"23",
"44",
"48",
"55",
"58",
"59",
"62",
"63",
"65",
"77",
"80",
"87",
"93",
"97",
"100",
"105",
"106",
"115",
"117",
"118",
"119",
"120",
"121",
"123",
"125",
"127",
"133",
"137",
"138",
"143",
"144",
"145",
"150",
"154",
"156",
"160",
"161",
"163",
"167",
"169",
"171",
"175",
"176",
"177",
"181",
"182",
"183",
"185",
"187",
"188",
"198",
"199",
"201",
"202",
"210",
"215",
"217",
"222",
"225",
"226",
"231",
"239",
"240",
"243",
"245",
"246",
"275",
"288",
"292",
"294",
"295",
"296",
"305",
"311",
"319",
"342",
"357",
"358",
"359",
"361",
"363",
"367",
"379",
"380",
"381",
"386",
"388",
"389",
"394",
"395",
"398",
"402",
"404",
"406",
"411",
"412",
"413",
"428",
"429",
"435",
"438",
"440",
"441",
"442",
"443",
"449",
"452",
"454",
"455",
"457",
"458",
"461",
"464",
"466",
"468",
"483",
"484",
"493",
"499",
"504",
"507",
"527",
"537",
"538",
"549",
"550",
"551",
"554",
"561",
"562",
"564",
"572",
"578",
"582",
"588",
"590",
"596",
]


# Prediction Function

def make_prediction(loan_description,funded_amount,term_in_months,sector,country_code,partner_id):
    
    X1 = loan_description
    
    X2 = {
        'funded_amount':[funded_amount],
        'term_in_months':[term_in_months],
        'sector': [sector],
        'country_code': [country_code],
        'partner_id': [partner_id]
    }
    X2 = pd.DataFrame(X2)

    X1b = [nlp.cleanText(X1)]
    X1c = loaded_vec.transform(X1b) 
    X1c = pd.DataFrame(columns = [loaded_vec.get_feature_names()], data = X1c.todense()) 

    X2['sector']= loaded_le_sector.transform([X2['sector']])[0] 
    X2['country_code']= loaded_le_country_code.transform([X2['country_code']])[0] 
    X2['partner_id']= loaded_le_partner_id.transform([X2['partner_id']])[0] 
    X2b = loaded_minMax.transform(X2)
    X2b = pd.DataFrame(X2b, columns = col_features2)
    X= pd.concat([X1c,X2b], axis =1)
    Xb = loaded_pca.transform(X) 

    pred = np.argmax(loaded_nn.predict(Xb), axis = 1)
    pred = float(pred[0])
    if pred == 1:
        pred ='funded'
    if pred == 0:
        pred ='expired'

    pred_proba =  np.max(loaded_nn.predict_proba(Xb), axis=1)
    pred_proba = float(pred_proba[0])*100
    
    return pred, pred_proba




# Layout

layout = html.Div(
    children=[
        html.Div(
            id='dashboard_title',
            children=[
                html.Br(),
                dbc.Card(
                    [
                        dbc.CardHeader(html.H3("Funding Probability on KIVA"), className='card-title', style={'background-color': '#4faf4e', 'color': '#ffffff'}),
                        dbc.CardBody(
                            [
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            [
                                                html.H2("Enter the loan characteristics", className='card-text')
                                            ],
                                        )
                                    ]
                                )
                            ]
                        )
                    ],
                    style={
                        'border': '3px solid',
                        'border-color': '#4faf4e'},
                    # color='primary',
                    outline=True
                )
            ]
        ),
        html.Div(className='row',
            children=[
                html.Div(
                    id="part1",
                    className='col-md-6',
                    children=[
                        html.Br(),
                        html.Div(
                            children=[
                                dbc.Card(
                                    [
                                        dbc.CardHeader("Partner & Entrepreneur profil", className="card-title", style={'background-color': '#4faf4e', 'color': '#ffffff'}),
                                        dbc.CardBody(
                                            [
                                                dbc.Row(
                                                    [
                                                        dbc.Col(
                                                            [
                                                                dbc.Card(
                                                                    [
                                                                        dbc.CardHeader("Partner ID", className="card-title", style={'background-color': '#90EE90', 'color': '#000000'}),
                                                                        dbc.CardBody(
                                                                            [
                                                                                dbc.Row(
                                                                                    [
                                                                                        dbc.Col(
                                                                                            [
                                                                                               dcc.Dropdown(
                                                                                                    id='dd-partener-id',
                                                                                                    options=[
                                                                                                        {'label': i, 'value': i} for i in partner_id
                                                                                                    ],
                                                                                                    value=partner_id0,
                                                                                                    clearable=False
                                                                                                ),
                                                                                            ]
                                                                                        )
                                                                                    ]
                                                                                )
                                                                            ],
                                                                            className="card-text",
                                                                            id="pred_card",
                                                                        )
                                                                    ],
                                                                )
                                                            ],
                                                            width=4
                                                        ),
                                                        dbc.Col(
                                                            [
                                                                dbc.Card(
                                                                    [
                                                                        dbc.CardHeader("Country Code", className="card-title", style={'background-color': '#90EE90', 'color': '#000000'}),
                                                                        dbc.CardBody(
                                                                            [
                                                                                dbc.Row(
                                                                                    [
                                                                                        dbc.Col(
                                                                                            [
                                                                                               dcc.Dropdown(
                                                                                                    id='dd-country-code',
                                                                                                    options=[
                                                                                                        {'label': i, 'value': i} for i in country_code
                                                                                                    ],
                                                                                                    value=country_code0,
                                                                                                    clearable = False
                                                                                                ),
                                                                                            ]
                                                                                        )
                                                                                    ]
                                                                                )
                                                                            ],
                                                                            className="card-text",
                                                                            id="pred_card",
                                                                        )
                                                                    ],
                                                                )

                                                            ],
                                                            width=4
                                                        ),

                                                        dbc.Col(
                                                            [
                                                                dbc.Card(
                                                                    [
                                                                        dbc.CardHeader("Sector", className="card-title", style={'background-color': '#90EE90', 'color': '#000000'}),
                                                                        dbc.CardBody(
                                                                            [
                                                                                dbc.Row(
                                                                                    [
                                                                                        dbc.Col(
                                                                                            [
                                                                                               dcc.Dropdown(
                                                                                                    id='dd-sector',
                                                                                                    options=[
                                                                                                        {'label': i, 'value': i} for i in sector
                                                                                                    ],
                                                                                                    value=sector0,
                                                                                                    clearable = False
                                                                                                ),

                                                                                            ]
                                                                                        )
                                                                                    ]
                                                                                )
                                                                            ],
                                                                            className="card-text",
                                                                            id="pred_card",
                                                                        )
                                                                    ],
                                                                )
                                                            ],
                                                            width=4
                                                        ),


                                                    ],
                                                    align='center',
                                                    no_gutters=True
                                                )
                                            ]
                                        )
                                    ],
                                    style={
                                        'border': '3px solid',
                                        'border-color': '#4faf4e'},
                                    # color='primary',
                                    outline=True
                                )
                            ],                            

                        ),
                        html.Br(),
                        html.Div(
                           children=[
                                dbc.Card(
                                    [
                                        dbc.CardHeader("Loan Description", className="card-title", style={'background-color': '#4faf4e', 'color': '#ffffff'}),
                                        dbc.CardBody(
                                            [
                                                dbc.Row(
                                                    [
                                                        dbc.Col(
                                                            [
                                                                dcc.Textarea(
                                                                    id = 'input-t-loan-des',
                                                                    placeholder='Enter the text...',
                                                                    #type='text',
                                                                    value=X1_0,
                                                                    #className="mb-3",
                                                                    style={'width': '100%', 'height': 150},
                                                                )  
                                                                # dbc.Card(
                                                                #     [
                                                                #         dbc.CardHeader("1", className="card-title", style={'background-color': '#C5DDF0'}),
                                                                #         dbc.CardBody(
                                                                #             [
                                                                #                 dbc.Row(
                                                                #                     [
                                                                #                         dbc.Col(
                                                                #                             [
                                                                #                                 dcc.Input(
                                                                #                                     id = 'input-t-loan-des',
                                                                #                                     placeholder='Enter the text...',
                                                                #                                     type='text',
                                                                #                                     value=X1_0
                                                                #                                 )  
                                                                #                             ]
                                                                #                         )
                                                                #                     ]
                                                                #                 )
                                                                #             ],
                                                                #             className="card-text",
                                                                #             id="pred_card",
                                                                #         )
                                                                #     ],
                                                                # )
                                                            ],
                                                            width=12,
                                                        ),
                                                    ],
                                                    align='center',
                                                    no_gutters=True
                                                )
                                            ]
                                        )
                                    ],
                                    style={
                                        'border': '3px solid',
                                        'border-color': '#4faf4e'},
                                    # color='primary',
                                    outline=True
                                )
                            ],
                        ),
                    ]
                ),
                html.Div(
                    id="part2",
                    className='col-md-6',
                    children=[
                        html.Br(),
                        html.Div(
                           children=[
                                dbc.Card(
                                    [
                                        dbc.CardHeader("Loan characteristics ", className="card-title", style={'background-color': '#4faf4e', 'color': '#ffffff'}),
                                        dbc.CardBody(
                                            [
                                                dbc.Row(
                                                    [
                                                        # dbc.Col(
                                                        #     [
                                                        #         dbc.Card(
                                                        #             [
                                                        #                 dbc.CardHeader("Sector", className="card-title", style={'background-color': '#90EE90', 'color': '#000000'}),
                                                        #                 dbc.CardBody(
                                                        #                     [
                                                        #                         dbc.Row(
                                                        #                             [
                                                        #                                 dbc.Col(
                                                        #                                     [
                                                        #                                        dcc.Dropdown(
                                                        #                                             id='dd-sector',
                                                        #                                             options=[
                                                        #                                                 {'label': i, 'value': i} for i in sector
                                                        #                                             ],
                                                        #                                             value=sector0,
                                                        #                                             clearable = False
                                                        #                                         ),

                                                        #                                     ]
                                                        #                                 )
                                                        #                             ]
                                                        #                         )
                                                        #                     ],
                                                        #                     className="card-text",
                                                        #                     id="pred_card",
                                                        #                 )
                                                        #             ],
                                                        #         )
                                                        #     ],
                                                        #     width=4
                                                        # ),
                                                        dbc.Col(
                                                            [
                                                                dbc.Card(
                                                                    [
                                                                        dbc.CardHeader("Loan Amount ($)", className="card-title", style={'background-color': '#90EE90', 'color': '#000000'}),
                                                                        dbc.CardBody(
                                                                            [
                                                                                dbc.Row(
                                                                                    [
                                                                                        dbc.Col(
                                                                                            [
                                                                                                dcc.Input(
                                                                                                    id='input-t-loan-amount',
                                                                                                    placeholder='...',
                                                                                                    type='number',
                                                                                                    value=funded_amount0
                                                                                                )  


                                                                                            ]
                                                                                        )
                                                                                    ]
                                                                                )
                                                                            ],
                                                                            className="card-text",
                                                                            id="pred_card",
                                                                        )
                                                                    ],
                                                                )
                                                            ],
                                                            width=6
                                                        ),
                                                        dbc.Col(
                                                            [
                                                                dbc.Card(
                                                                    [
                                                                        dbc.CardHeader("Loan terms in month", className="card-title", style={'background-color': '#90EE90', 'color': '#000000'}),
                                                                        dbc.CardBody(
                                                                            [
                                                                                dbc.Row(
                                                                                    [
                                                                                        dbc.Col(
                                                                                            [
                                                                                               dcc.Dropdown(
                                                                                                    id='dd-terms-month',
                                                                                                    options=[
                                                                                                        {'label': i, 'value': i} for i in range(1,13)
                                                                                                    ],
                                                                                                    value=term_in_months0,
                                                                                                    clearable = False
                                                                                                ),

                                                                                            ]
                                                                                        )
                                                                                    ]
                                                                                )
                                                                            ],
                                                                            className="card-text",
                                                                            id="pred_card",
                                                                        )
                                                                    ],
                                                                )
                                                            ],
                                                            width=6
                                                        ),

                                                    ],
                                                    align='center',
                                                    no_gutters=True
                                                )
                                            ]
                                        )
                                    ],
                                    style={
                                        'border': '3px solid',
                                        'border-color': '#4faf4e'},
                                    # color='primary',
                                    outline=True
                                )
                            ],
                        ),
                        html.Br(),
                        html.Div(
                            id='prediction-display',
                            children=[
                                dbc.Card(
                                    [
                                        dbc.CardHeader("AI PREDICTION", className="card-title", style={'background-color': '#4faf4e', 'color': '#ffffff'}),
                                        dbc.CardBody(
                                            [
                                                dbc.Row(
                                                    [
                                                        dbc.Col(
                                                            [
                                                                dbc.Card(
                                                                    [
                                                                        dbc.CardHeader("Prediction", className="card-title", style={'background-color': '#90EE90', 'color': '#000000'}),
                                                                        dbc.CardBody(
                                                                            [
                                                                                dbc.Row(
                                                                                    [
                                                                                        dbc.Col(
                                                                                            [
                                                                                                html.H1([""], className="card-text", style={'line-height': '1.3'})
                                                                                            ]
                                                                                        )
                                                                                    ]
                                                                                )
                                                                            ],
                                                                            className="card-text",
                                                                            id="pred_card",
                                                                        )
                                                                    ],
                                                                )
                                                            ],
                                                            width=6
                                                        ),
                                                        dbc.Col(
                                                            [
                                                                dbc.Card(
                                                                    [
                                                                        dbc.CardHeader("Probability", className="card-title", style={'background-color': '#90EE90', 'color': '#000000'}),
                                                                        dbc.CardBody(
                                                                            [
                                                                                dbc.Row(
                                                                                    [
                                                                                        dbc.Col(
                                                                                            [
                                                                                                html.H1([""], className="card-text", style={'line-height': '1.3'})
                                                                                            ]
                                                                                        )
                                                                                    ]
                                                                                )
                                                                            ],
                                                                            className="card-text",
                                                                            id="pred_proba_card",
                                                                        )
                                                                    ],
                                                                )

                                                            ],
                                                            width=6
                                                        ),
                                                    ],
                                                    align='center',
                                                    no_gutters=True
                                                )
                                            ]
                                        )
                                    ],
                                    style={
                                        'border': '3px solid',
                                        'border-color': '#4faf4e'},
                                    # color='primary',
                                    outline=True
                                )
                            ],
                        ),

                        html.Br(),
                        
 
                    ]
                ),
            ]
        ),

    ]
)


# Callbacks

@app.callback(
    [
    Output("pred_card", "children"),
    Output("pred_proba_card", "children"),
    ],
    [
        Input("input-t-loan-des", "value"),
        Input("input-t-loan-amount", "value"),
        Input("dd-terms-month", "value"),
        Input("dd-sector", "value"),
        Input("dd-country-code", "value"),
        Input("dd-partener-id", "value"),
    ]
)
def prediction_print(loan_description,funded_amount,term_in_months,sector,country_code,partner_id):
    xpred, xpred_proba =   make_prediction(loan_description,funded_amount,term_in_months,sector,country_code,partner_id)
    res1 =  html.H1([xpred], className="card-text", style={'line-height': '1.3'})
    res2 = html.H1([round(xpred_proba, 2), "%"], className="card-text", style={'line-height': '1.3'})
    
    return res1, res2


