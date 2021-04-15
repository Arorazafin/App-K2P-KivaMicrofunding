# Dash Imports

import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
from dash.dependencies import Input, Output

# tensorflow
import tensorflow as tf
from tensorflow.keras.models import load_model



# Non Dash Imports

import base64
import pandas as pd
import numpy as np 
from joblib import dump, load
from app import app


# Data

data_folder = 'models'

Humidite_finale = 2.69
Temps_de_granulation=0.00118827160493827
Temps_de_mouillage=0.0003125
Temps_de_melange=0.00142361111111111
Temps_de_sechage=0.0613387345679012
Temperature_enceinte_GRANULATION=25.2433333333333
Temperature_enceinte_MELANGE=15.2166666666667
Temperature_enceinte_MOUILLAGE=25.5366666666667
Temperature_entree_REFROIDISSEMENT=30.4733333333333
Temperature_entree_SECHAGE=8.01
Temperature_sortie_REFROIDISSEMENT=38.97
Temperature_sortie_SECHAGE=8.0333333333333
Debit_air_REFROIDISSEMENT=4350.34333333333
Debit_air_SECHAGE=4292.4
Puissance_GRANULATION=4.46166666666667
Puissance_MELANGE=5.47
Puissance_MOUILLAGE=2.61666666666667

def float_to_secondes(time_to_convert):
    time_secondes = round(time_to_convert*24*60*60, 0)
    return time_secondes

def secondes_to_float(time_to_convert):
    time_float = time_to_convert / (24*60*60)
    return time_float

# Slider Functions
   
def select_hf():
    """
    :return: A Div containing slider to select Humidité Finale.
    """
    hf_select = dcc.Slider(
                    id="humidite_finale",
                    min=0,
                    max=5,
                    step=0.1,
                    marks={
                        0: '0',
                        5: '5',
                    },
                    tooltip={
                        'always_visible': True,
                        'placement': 'bottom'
                    },
                    # vertical=True,
                    value=Humidite_finale,  
                )

    return hf_select

def select_temps_granulation():
    """
    :return: A Div containing slider to select Temps de Granulation.
    """
    temps_granulation_select = dcc.Slider(
                    id="temps_granulation",
                    min=0,
                    max=500,
                    step=1,
                    marks={
                        0: '0s',
                        500: '500s',
                    },
                    tooltip={
                        'always_visible': True,
                        'placement': 'bottom'
                    },
                    # vertical=True,
                    value=float_to_secondes(Temps_de_granulation),  
                )

    return temps_granulation_select

def select_temps_mouillage():
    """
    :return: A Div containing dropdown to select Temps de Mouillage.
    """
    temps_mouillage_select = dcc.Slider(
                    id="temps_mouillage",
                    min=0,
                    max=500,
                    step=1,
                    marks={
                        0: '0s',
                        500: '500s',
                    },
                    tooltip={
                        'always_visible': True,
                        'placement': 'bottom'
                    },
                    # vertical=True,
                    value=float_to_secondes(Temps_de_mouillage),  
                )

    return temps_mouillage_select

def select_temps_melange():
    """
    :return: A Div containing dropdown to select Temps de Mélange.
    """
    temps_melange_select = dcc.Slider(
                    id="temps_melange",
                    min=0,
                    max=500,
                    step=1,
                    marks={
                        0: '0s',
                        500: '500s ',
                    },
                    tooltip={
                        'always_visible': True,
                        'placement': 'bottom'
                    },
                    # vertical=True,
                    value=float_to_secondes(Temps_de_melange),  
                )

    return temps_melange_select

def select_temps_sechage():
    """
    :return: A Div containing dropdown to select Temps de Séchage.
    """
    temps_sechage_select = dcc.Slider(
                    id="temps_sechage",
                    min=0,
                    max=8000,
                    step=1,
                    marks={
                        0: '0s',
                        8000: '8000s',
                    },
                    tooltip={
                        'always_visible': True,
                        'placement': 'bottom'
                    },
                    # vertical=True,
                    value=float_to_secondes(Temps_de_sechage),  
                )

    return temps_sechage_select

def select_temperature_enceinte_granulation():
    """
    :return: A Div containing dropdown to select Température Enceinte Granulation.
    """
    temperature_enceinte_granulation_select = dcc.Slider(
                    id="temperature_enceinte_granulation",
                    min=20,
                    max=50,
                    step=0.01,
                    marks={
                        20: '20°C',
                        50: '50°C',
                    },
                    tooltip={
                        'always_visible': True,
                        'placement': 'bottom'
                    },
                    # vertical=True,
                    value=Temperature_enceinte_GRANULATION,  
                )

    return temperature_enceinte_granulation_select

def select_temperature_enceinte_melange():
    """
    :return: A Div containing dropdown to select Température Enceinte Mélange.
    """
    temperature_enceinte_melange_select = dcc.Slider(
                    id="temperature_enceinte_melange",
                    min=10,
                    max=30,
                    step=0.01,
                    marks={
                        10: '10°C',
                        30: '30°C',
                    },
                    tooltip={
                        'always_visible': True,
                        'placement': 'bottom'
                    },
                    # vertical=True,
                    value=Temperature_enceinte_MELANGE,  
                )

    return temperature_enceinte_melange_select

def select_temperature_enceinte_mouillage():
    """
    :return: A Div containing dropdown to select Température Enceinte Mouillage.
    """
    temperature_enceinte_mouillage_select = dcc.Slider(
                    id="temperature_enceinte_mouillage",
                    min=20,
                    max=50,
                    step=0.01,
                    marks={
                        20: '20°C',
                        50: '50°C',
                    },
                    tooltip={
                        'always_visible': True,
                        'placement': 'bottom'
                    },
                    # vertical=True,
                    value=Temperature_enceinte_MOUILLAGE,  
                )

    return temperature_enceinte_mouillage_select

def select_temperature_entree_refroidissement():
    """
    :return: A Div containing dropdown to select Température Entrée Refroidissement.
    """
    temperature_entree_refroidissement_select = dcc.Slider(
                    id="temperature_entree_refroidissement",
                    min=20,
                    max=50,
                    step=0.01,
                    marks={
                        20: '20°C',
                        50: '50°C',
                    },
                    tooltip={
                        'always_visible': True,
                        'placement': 'bottom'
                    },
                    # vertical=True,
                    value=Temperature_entree_REFROIDISSEMENT,  
                )

    return temperature_entree_refroidissement_select

def select_temperature_entree_sechage():
    """
    :return: A Div containing dropdown to select Température Entrée Séchage.
    """
    temperature_entree_sechage_select = dcc.Slider(
                    id="temperature_entree_sechage",
                    min=0,
                    max=20,
                    step=0.01,
                    marks={
                        0: '0°C',
                        20: '20°C',
                    },
                    tooltip={
                        'always_visible': True,
                        'placement': 'bottom'
                    },
                    # vertical=True,
                    value=Temperature_entree_SECHAGE,  
                )

    return temperature_entree_sechage_select

def select_temperature_sortie_refroidissement():
    """
    :return: A Div containing dropdown to select Température Sortie Refroidissement.
    """
    temperature_sortie_refroidissement_select = dcc.Slider(
                    id="temperature_sortie_refroidissement",
                    min=30,
                    max=50,
                    step=0.01,
                    marks={
                        30: '30°C',
                        50: '50°C',
                    },
                    tooltip={
                        'always_visible': True,
                        'placement': 'bottom'
                    },
                    # vertical=True,
                    value=Temperature_sortie_REFROIDISSEMENT,  
                )

    return temperature_sortie_refroidissement_select

def select_temperature_sortie_sechage():
    """
    :return: A Div containing dropdown to select Température Sortie Séchage.
    """
    temperature_sortie_sechage_select = dcc.Slider(
                    id="temperature_sortie_sechage",
                    min=0,
                    max=20,
                    step=0.01,
                    marks={
                        0: '0°C',
                        20: '20°C',
                    },
                    tooltip={
                        'always_visible': True,
                        'placement': 'bottom'
                    },
                    # vertical=True,
                    value=Temperature_sortie_SECHAGE,  
                )

    return temperature_sortie_sechage_select

def select_debit_air_refroidissement():
    """
    :return: A Div containing dropdown to select Débit Air Refroidissement.
    """
    debit_air_refroidissement_select = dcc.Slider(
                    id="debit_air_refroidissement",
                    min=4000,
                    max=4500,
                    step=0.01,
                    marks={
                        4000: '4000',
                        4500: '4500',
                    },
                    tooltip={
                        'always_visible': True,
                        'placement': 'bottom'
                    },
                    # vertical=True,
                    value=Debit_air_REFROIDISSEMENT,  
                )

    return debit_air_refroidissement_select

def select_debit_air_sechage():
    """
    :return: A Div containing dropdown to select Débit Air Séchage.
    """
    debit_air_sechage_select = dcc.Slider(
                    id="debit_air_sechage",
                    min=4000,
                    max=4500,
                    step=0.01,
                    marks={
                        4000: '4000',
                        4500: '4500',
                    },
                    tooltip={
                        'always_visible': True,
                        'placement': 'bottom'
                    },
                    # vertical=True,
                    value=Debit_air_SECHAGE,  
                )

    return debit_air_sechage_select

def select_puissance_granulation():
    """
    :return: A Div containing dropdown to select Puissance Granulation.
    """
    puissance_granulation_select = dcc.Slider(
                    id="puissance_granulation",
                    min=0,
                    max=10,
                    step=0.01,
                    marks={
                        0: '0',
                        10: '10',
                    },
                    tooltip={
                        'always_visible': True,
                        'placement': 'bottom'
                    },
                    # vertical=True,
                    value=Puissance_GRANULATION,  
                )

    return puissance_granulation_select

def select_puissance_melange():
    """
    :return: A Div containing dropdown to select Puissance Mélange.
    """
    puissance_melange_select = dcc.Slider(
                    id="puissance_melange",
                    min=0,
                    max=10,
                    step=0.01,
                    marks={
                        0: '0',
                        10: '10',
                    },
                    tooltip={
                        'always_visible': True,
                        'placement': 'bottom'
                    },
                    # vertical=True,
                    value=Puissance_MELANGE,  
                )

    return puissance_melange_select

def select_puissance_mouillage():
    """
    :return: A Div containing dropdown to select Puissance Mouillage.
    """
    puissance_mouillage_select = dcc.Slider(
                    id="puissance_mouillage",
                    min=0,
                    max=10,
                    step=0.01,
                    marks={
                        0: '0',
                        10: '10',
                    },
                    tooltip={
                        'always_visible': True,
                        'placement': 'bottom'
                    },
                    # vertical=True,
                    value=Puissance_MOUILLAGE,  
                )

    return puissance_mouillage_select


# Model Choice Dropdown Funtion

def select_model():
    model_select = dcc.Dropdown(
                id="model_chosen",
                #options=[{"label": i, "value": i} for i in ['Random Forest', 'Support Vector Machine']],
                options=[{"label": i, "value": i} for i in ['Random Forest', 'Support Vector Machine', 'Neural Network']],
                value='Support Vector Machine',
                placeholder="Choisir le modèle voulu",
                clearable=True,
                # multi=True
            )

    return model_select


# Prediction Function

def make_prediction(model_selected, Humidite_finale_get, Temps_de_granulation_get, Temps_de_mouillage_get, Temps_de_melange_get, Temps_de_sechage_get, Temperature_enceinte_GRANULATION_get, Temperature_enceinte_MELANGE_get, Temperature_enceinte_MOUILLAGE_get, Temperature_entree_REFROIDISSEMENT_get, Temperature_entree_SECHAGE_get, Temperature_sortie_REFROIDISSEMENT_get, Temperature_sortie_SECHAGE_get, Debit_air_REFROIDISSEMENT_get, Debit_air_SECHAGE_get, Puissance_GRANULATION_get, Puissance_MELANGE_get, Puissance_MOUILLAGE_get):
    
    X_to_pred = {
        "Humidite_finale" : [Humidite_finale_get] ,
        "Temps_de_granulation":[Temps_de_granulation_get],
        "Temps_de_mouillage":[Temps_de_mouillage_get],
        "Temps_de_melange":[Temps_de_melange_get],
        "Temps_de_sechage":[Temps_de_sechage_get],
        "Temperature_enceinte_GRANULATION":[Temperature_enceinte_GRANULATION_get],
        "Temperature_enceinte_MELANGE":[Temperature_enceinte_MELANGE_get],
        "Temperature_enceinte_MOUILLAGE":[Temperature_enceinte_MOUILLAGE_get],
        "Temperature_entree_REFROIDISSEMENT":[Temperature_entree_REFROIDISSEMENT_get],
        "Temperature_entree_SECHAGE":[Temperature_entree_SECHAGE_get],
        "Temperature_sortie_REFROIDISSEMENT":[Temperature_sortie_REFROIDISSEMENT_get],
        "Temperature_sortie_SECHAGE":[Temperature_sortie_SECHAGE_get],
        "Debit_air_REFROIDISSEMENT":[Debit_air_REFROIDISSEMENT_get],
        "Debit_air_SECHAGE":[Debit_air_SECHAGE_get],
        "Puissance_GRANULATION":[Puissance_GRANULATION_get],
        "Puissance_MELANGE":[Puissance_MELANGE_get],
        "Puissance_MOUILLAGE":[Puissance_MOUILLAGE_get]    
    }

    if model_selected == 'Neural Network':
        model_selected2 = 'nn_tf_v0.h5'
        model = load_model(data_folder + '/' + model_selected2)
        X_to_pred = pd.DataFrame(X_to_pred)
        X_to_pred = np.asarray(X_to_pred)
        pred = model.predict(X_to_pred)
        pred = float(pred[0][0])

    if model_selected == 'Random Forest':
        model_selected2= 'rf_v0.sav'
        model = load(data_folder + '/' + model_selected2)
        X_to_pred = pd.DataFrame(X_to_pred)
        pred = model.predict(X_to_pred)
        pred = pred[0]

    elif model_selected == 'Support Vector Machine':
        model_selected2= 'svr_v0.sav'
        model = load(data_folder + '/' + model_selected2)
        X_to_pred = pd.DataFrame(X_to_pred)
        pred = model.predict(X_to_pred)
        pred = pred[0]



    return pred


# Layout Functions

def slider_card(slider_title, slider_function):
    card_for_slider = dbc.Card(
        [
            dbc.CardHeader(slider_title, className="card-title", style={'background-color': '#C5DDF0'}),
            dbc.CardBody(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    slider_function,
                                ]
                            )
                        ]
                    )
                ],
                className="card-text"
            )
        ],
        # color='primary',
        # outline=True,
    )

    return card_for_slider

def slider_group(slider_group_title, slider_title_1, slider_function_1, slider_title_2, slider_function_2, slider_title_3, slider_function_3):
    group_of_sliders = dbc.Card(
        [
            dbc.CardHeader(slider_group_title, className="card-title", style={'background-color': '#525CA3', 'color': '#ffffff'}),
            dbc.CardBody(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    slider_card(slider_title_1, slider_function_1)
                                ],
                                width=4
                            ),
                            dbc.Col(
                                [
                                    slider_card(slider_title_2, slider_function_2)
                                ],
                                width=4
                            ),
                            dbc.Col(
                                [
                                    slider_card(slider_title_3, slider_function_3)
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
            'border-color': '#525CA3'},
        # color='primary',
        outline=True
    )

    return group_of_sliders

def slider_group_large(slider_group_title, slider_title_1, slider_function_1, slider_title_2, slider_function_2, slider_title_3, slider_function_3, slider_title_4, slider_function_4):
    group_of_sliders_large = dbc.Card(
        [
            dbc.CardHeader(slider_group_title, className="card-title", style={'background-color': '#525CA3', 'color': '#ffffff'}),
            dbc.CardBody(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    slider_card(slider_title_1, slider_function_1)
                                ],
                                width=3
                            ),
                            dbc.Col(
                                [
                                    slider_card(slider_title_2, slider_function_2)
                                ],
                                width=3
                            ),
                            dbc.Col(
                                [
                                    slider_card(slider_title_3, slider_function_3)
                                ],
                                width=3
                            ),
                            dbc.Col(
                                [
                                    slider_card(slider_title_4, slider_function_4)
                                ],
                                width=3
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
            'border-color': '#525CA3'},
        # color='primary',
        outline=True
    )

    return group_of_sliders_large


# Layout

layout = html.Div(
    children=[
        html.Div(
            id='dashboard_title',
            children=[
                html.Br(),
                dbc.Card(
                    [
                        dbc.CardHeader(html.H3("Prédiction en Fonction des Paramètres de Process"), className='card-title', style={'background-color': '#525CA3', 'color': '#ffffff'}),
                        dbc.CardBody(
                            [
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            [
                                                html.H2("DRONEDARONE - Taux de Dissolution à 30mn", className='card-text')
                                            ],
                                        )
                                    ]
                                )
                            ]
                        )
                    ],
                    style={
                        'border': '3px solid',
                        'border-color': '#525CA3'},
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
                            slider_group(
                                "MELANGE",
                                "Temps",
                                select_temps_melange(),
                                "Température Enceinte",
                                select_temperature_enceinte_melange(),
                                "Puissance",
                                select_puissance_melange()
                            )
                        ),
                        html.Br(),
                        html.Div(
                            slider_group(
                                "MOUILLAGE",
                                "Temps",
                                select_temps_mouillage(),
                                "Température Enceinte",
                                select_temperature_enceinte_mouillage(),
                                "Puissance",
                                select_puissance_mouillage()
                            )
                        ),
                        html.Br(),
                        html.Div(
                            slider_group(
                                "GRANULATION",
                                "Temps",
                                select_temps_granulation(),
                                "Température Enceinte",
                                select_temperature_enceinte_granulation(),
                                "Puissance",
                                select_puissance_granulation()
                            )
                        ),
                    ]
                ),
                html.Div(
                    id="part2",
                    className='col-md-6',
                    children=[
                        html.Br(),
                        html.Div(
                            slider_group_large(
                                "SECHAGE",
                                "Temps",
                                select_temps_sechage(),
                                "Température Entrée",
                                select_temperature_entree_sechage(),
                                "Température Sortie",
                                select_temperature_sortie_sechage(),
                                "Débit d'Air",
                                select_debit_air_sechage()
                            )
                        ),
                        html.Br(),
                        html.Div(
                            slider_group(
                                "REFROIDISSEMENT",
                                "Température Entrée",
                                select_temperature_entree_refroidissement(),
                                "Température Sortie",
                                select_temperature_sortie_refroidissement(),
                                "Débit d'Air",
                                select_debit_air_refroidissement()
                            )
                        ),
                        html.Br(),
                        html.Div(
                            dbc.Card(
                                [
                                    dbc.CardHeader("ANALYSE DU GRAIN", className="card-title", style={'background-color': '#525CA3', 'color': '#ffffff'}),
                                    dbc.CardBody(
                                        [
                                            dbc.Row(
                                                [
                                                    dbc.Col(
                                                        [
                                                            slider_card("Humidité Finale", select_hf())
                                                        ]
                                                    )
                                                ]
                                            )
                                        ]
                                    )
                                ],
                                style={
                                    'border': '3px solid',
                                    'border-color': '#525CA3'},
                                # color='primary',
                                outline=True
                            )
                        )
                    ]
                ),
            ]
        ),
        html.Div(
            id="part3",
            children=[
                html.Br(),
                html.Div(
                    id='prediction-display',
                    children=[
                        dbc.Card(
                            [
                                dbc.CardHeader("Prédiction du TAUX DE DISSOLUTION A 30 MINUTES", className="card-title", style={'background-color': '#525CA3', 'color': '#ffffff'}),
                                dbc.CardBody(
                                    [
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    [
                                                        slider_card("Choix du Modèle", select_model())
                                                    ],
                                                    width=4
                                                ),
                                                dbc.Col(
                                                    [
                                                        dbc.Card(
                                                            [
                                                                dbc.CardHeader("Prédiction", className="card-title", style={'background-color': '#C5DDF0'}),
                                                                dbc.CardBody(
                                                                    [
                                                                        dbc.Row(
                                                                            [
                                                                                dbc.Col(
                                                                                    [
                                                                                        html.H3([""], className="card-text", style={'line-height': '1.3'})
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
                                                        slider_card("Norme Maxi (Valeurs Individuelles)", html.P(["Stage 1 : 50%", html.Br(), "Stage 2 : 60%"], style={'line-height': '1.2', 'margin-top': 0, 'margin-bottom': 0}))
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
                                'border-color': '#525CA3'},
                            # color='primary',
                            outline=True
                        )
                    ],
                )
            ]
        )
    ]
)


# Callbacks

@app.callback(
    Output("pred_card", "children"),
    [
        Input("model_chosen", "value"),
        Input("humidite_finale", "value"),
        Input("temps_granulation", "value"),
        Input("temps_mouillage", "value"),
        Input("temps_melange", "value"),
        Input("temps_sechage", "value"),
        Input("temperature_enceinte_granulation", "value"),
        Input("temperature_enceinte_melange", "value"),
        Input("temperature_enceinte_mouillage", "value"),
        Input("temperature_entree_refroidissement", "value"),
        Input("temperature_entree_sechage", "value"),
        Input("temperature_sortie_refroidissement", "value"),
        Input("temperature_sortie_sechage", "value"),
        Input("debit_air_refroidissement", "value"),
        Input("debit_air_sechage", "value"),
        Input("puissance_granulation", "value"),
        Input("puissance_melange", "value"),
        Input("puissance_mouillage", "value")
    ]
)
def prediction_print(model_chosen, humidite_finale_value, temps_granulation_value, temps_mouillage_value, temps_melange_value, temps_sechage_value, temperature_enceinte_granulation_value, temperature_enceinte_melange_value, temperature_enceinte_mouillage_value, temperature_entree_refroidissement_value, temperature_entree_sechage_value, temperature_sortie_refroidissement_value, temperature_sortie_sechage_value, debit_air_refroidissement_value, debit_air_sechage_value, puissance_granulation_value, puissance_melange_value, puissance_mouillage_value):
    temps_melange_value = secondes_to_float(temps_melange_value)
    temps_mouillage_value = secondes_to_float(temps_mouillage_value)
    temps_granulation_value = secondes_to_float(temps_granulation_value)
    temps_sechage_value = secondes_to_float(temps_sechage_value)
    
    prediction_disso =   make_prediction(model_chosen, humidite_finale_value, temps_granulation_value, temps_mouillage_value, temps_melange_value, temps_sechage_value, temperature_enceinte_granulation_value, temperature_enceinte_melange_value, temperature_enceinte_mouillage_value, temperature_entree_refroidissement_value, temperature_entree_sechage_value, temperature_sortie_refroidissement_value, temperature_sortie_sechage_value, debit_air_refroidissement_value, debit_air_sechage_value, puissance_granulation_value, puissance_melange_value, puissance_mouillage_value)

    return html.H1([round(prediction_disso, 2), "%"], className="card-text", style={'line-height': '1.3'})



# @app.callback(Output('humidite_finale', 'children'),
#               Input('humidite_finale', 'value'))
# def display_value(value):
#     return '{}'.format(value)

# needed only if running this as a single page app
# if __name__ == '__main__':
#     app.run_server(host='127.0.0.1', debug=True)