##################################################################################################
# This script is part of the following article paper 
# Title: "Current Consumption Analysis of LCD and # AMOLED Display Technologies: An Approach Based 
# on Multi-Text Input Modalities"
# authors: Jussif Junior Abularach Arnez 
#           Rafael Monteiro Ribeiro, 
#           Janislley Oliveira De Sousa, 
#           Maria Gabriela Lima Damasceno, 
#           Bruno S. Da Silva, 
#           Gidy C. F. Navarro
# version date: 10/28/2025
#################################################################################################

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.io as pio
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Rectangle
from matplotlib.collections import PathCollection
from matplotlib.patches import Path
from scipy.stats import gaussian_kde

class Display_Consumption(object):
    my_figure= {'ESPESSURA_LINHA': 4, 
            'TAMANHO_FONTE': 25, 
            'TAMANHO_LEG': 25, 
            'TAMANHO_TICK':25, 
            'xtick_angle': 290,
            'TAMANHO_AX': 25,
            'TAMANHO_ARROW_T': 20,
            'ESPESSURA_LINHA_MARKER': 5,
            'ESPESSURA_TAMH_MARKER': 1,
            'COR': 'black',
            'FONTE': "Courier New, monospace"}

    def __init__(self):
        """ Class to compute the Power Consumption for Different Display Technologies
        """
        self.limiar= 450 #mA

    def Sleep_Mode(self):
        #$ A146M
        a146m_sleep_dark = pd.DataFrame()
        for val in range(1,4):
            df_a146m_sleep_dark = pd.read_csv("D:\\Users\\jussif.arnez\\Documents\\2021_IMS\\my_documents\\my_Research\\my_plotting\\Display_Power\\Reteste\\A146M_dark_mode\\sleep\\sleep_screen_A146M_test_" + str(val) + ".csv")
            select_ = df_a146m_sleep_dark[df_a146m_sleep_dark['Main Avg Current (mA)'] <= self.limiar]['Main Avg Current (mA)']
            #data_a146m = { 'a146m_normal_t'+ str(val) : select_}
            a146m_sleep_dark['a146m_dark_sleept'+ str(val)] = select_ 
    
        a146m_sleep_dark_mean = a146m_sleep_dark.mean()
        df_a146m_sleep_dark_mean = pd.DataFrame(a146m_sleep_dark_mean).transpose()

        self.df_a146m_sleep_dark_mean_reshaped= pd.DataFrame(
                df_a146m_sleep_dark_mean.values.reshape(3,1), 
                columns = ['a146m_dark_sleep'],
                index = ['t1', 't2', 't3']
        )

        #$S918B
        s918b_sleep_dark = pd.DataFrame()
        for val in range(1,4):
            df_s918b_sleep_dark = pd.read_csv("D:\\Users\\jussif.arnez\\Documents\\2021_IMS\\my_documents\\my_Research\\my_plotting\\Display_Power\\Reteste\\S918B_dark_mode\\sleep\\sleep_screen_S918B_test_" + str(val) + ".csv")
            select_ = df_s918b_sleep_dark[df_s918b_sleep_dark['Main Avg Current (mA)'] <= self.limiar]['Main Avg Current (mA)']
            #data_s918b = { 's918b_normal_t'+ str(val) : select_}
            s918b_sleep_dark['s918b_dark_sleept'+ str(val)] = select_ 
        
        s918b_sleep_dark_mean = s918b_sleep_dark.mean()
        df_s918b_sleep_dark_mean = pd.DataFrame(s918b_sleep_dark_mean).transpose()

        self.df_s918b_sleep_dark_mean_reshaped= pd.DataFrame(
                df_s918b_sleep_dark_mean.values.reshape(3,1), 
                columns = ['s918b_dark_sleep'],
                index = ['t1', 't2', 't3']
        )

        #$Plotting
        fig_bar_sleep_comparison_dark = go.Figure(
        layout_title_text="Comparison of Average Current Consumption For Different DuTs for Screen Off",
        )

        fig_bar_sleep_comparison_dark.add_bar(y=['Test 1', 'Test 2', 'Test 3'], 
                            x=self.df_a146m_sleep_dark_mean_reshaped['a146m_dark_sleep'], 
                            text=[round(val, 3) for val in self.df_a146m_sleep_dark_mean_reshaped['a146m_dark_sleep']],
                            name="PLS LCD for Turn Off Screen",
                            orientation="h",
                            textposition="inside", insidetextanchor="middle", textfont=dict(size=20),
                            marker=dict(line=dict(width=2), color='#ff33ff')
                        )

        fig_bar_sleep_comparison_dark.add_bar(y=['Test 1', 'Test 2', 'Test 3'], 
                            x=self.df_s918b_sleep_dark_mean_reshaped['s918b_dark_sleep'], 
                            text=[round(val, 3) for val in self.df_s918b_sleep_dark_mean_reshaped['s918b_dark_sleep']],
                            name="Dynamic Amoled for Turn Off Screen",
                            orientation="h",
                            textposition="inside", insidetextanchor="middle", textfont=dict(size=20),
                            marker=dict(line=dict(width=2), color='blue')
                        )

        fig_bar_sleep_comparison_dark.update_layout(
                        title={'text': "", 'font': {'size': 1}},

                        xaxis_title={'text': "Average Current Consumption (mA)", 'font': {'size': self.my_figure['TAMANHO_LEG']}},
                        width=1500, height=800,
                        yaxis=dict(
                            tickfont=dict(size=self.my_figure['TAMANHO_TICK']),
                        ),
                        xaxis=dict(tickfont=dict(size=self.my_figure['TAMANHO_TICK']),
                                range=[0, 8]),
                        legend=dict(
                            font=dict(size=self.my_figure['TAMANHO_LEG']),
                            orientation='h',
                            yanchor='top',
                            y=1.09,
                            xanchor='center',
                            x=0.5
                        ),
                        plot_bgcolor='white',
                        shapes=[
                            dict(
                                type='rect',
                                xref='paper',
                                yref='paper',
                                x0=0,
                                y0=0,
                                x1=1.001,
                                y1=1.001,
                                line=dict(
                                    color='black',
                                    width=1,
                                )
                            )
                        ],
        )
        fig_bar_sleep_comparison_dark.show(renderer="browser")
        #fig_bar_sleep_comparison_dark.write_html("lcd_amolead_sleep_mode.html")
        #! to avoid the message appears on the pdf file.
        # pio.full_figure_for_development(fig_bar_sleep_comparison_dark, warn=False)
        # fig_bar_sleep_comparison_dark.write_image("lcd_amoled_sleep_mode.pdf", width= 1500 , height= 800, engine="kaleido")

    def Home_Screens(self):
        # A146M
        #$ Light Mode
        a146m_home = pd.DataFrame()
        for val in range(1,4):
            df_a146m_home = pd.read_csv("D:\\Users\\jussif.arnez\\Documents\\2021_IMS\\my_documents\\my_Research\\my_plotting\\Display_Power\\Reteste\\A146M_normal\\idle\\idle_screen_A146M_test_" + str(val) + ".csv")
            select_ = df_a146m_home[df_a146m_home['Main Avg Current (mA)'] <= self.limiar]['Main Avg Current (mA)']
            #data_a146m = { 'a146m_normal_t'+ str(val) : select_}
            a146m_home['a146m_normal_idt'+ str(val)] = select_ 
        fig_a146m_home = go.Figure()

        trace_a146m_idt1 = go.Scatter(y=a146m_home['a146m_normal_idt1'], 
                                        name= 'A146M Home Screen Test 1',
                                        mode='lines', 
                                        line=dict(width=1, color ='green')
        )
        trace_a146m_idt2 = go.Scatter(y=a146m_home['a146m_normal_idt2'], 
                                        name= 'A146M Home Screen Test 2',
                                        mode='lines', 
                                        line=dict(width=1, color ='blue')
        )
        trace_a146m_idt3 = go.Scatter(y=a146m_home['a146m_normal_idt3'], 
                                        name= 'A146M Home Screen Test 3',
                                        mode='lines', 
                                        line=dict(width=1, color ='orange')
        )

        fig_a146m_home.add_trace(trace_a146m_idt1)
        fig_a146m_home.add_trace(trace_a146m_idt2)
        fig_a146m_home.add_trace(trace_a146m_idt3)
        fig_a146m_home.update_layout(yaxis=dict(range=[300,1000]))
        #fig_a146m_home.show(renderer="browser")
        a146m_home_mean = a146m_home.mean()
        df_a146m_home_mean = pd.DataFrame(a146m_home_mean).transpose()

        self.df_a146m_home_mean_reshaped= pd.DataFrame(
                df_a146m_home_mean.values.reshape(3,1), 
                columns = ['a146m_light_idle'],
                index = ['t1', 't2', 't3']
        )

        #$ Dark Mode
        a146m_home_dark = pd.DataFrame()
        for val in range(1,4):
            df_a146m_home_dark = pd.read_csv("D:\\Users\\jussif.arnez\\Documents\\2021_IMS\\my_documents\\my_Research\\my_plotting\\Display_Power\\Reteste\\A146M_dark_mode\\idle\\idle_screen_A146M_test_" + str(val) + ".csv")
            select_ = df_a146m_home_dark[df_a146m_home_dark['Main Avg Current (mA)'] <= self.limiar]['Main Avg Current (mA)']
            #data_a146m = { 'a146m_normal_t'+ str(val) : select_}
            a146m_home_dark['a146m_dark_idt'+ str(val)] = select_ 
        a146m_home_dark_mean = a146m_home_dark.mean()
        df_a146m_home_dark_mean = pd.DataFrame(a146m_home_dark_mean).transpose()

        self.df_a146m_home_dark_mean_reshaped= pd.DataFrame(
                df_a146m_home_dark_mean.values.reshape(3,1), 
                columns = ['a146m_dark_idle'],
                index = ['t1', 't2', 't3']
        )


        #--- S918B
        #$ Light Mode
        s918b_home = pd.DataFrame()
        for val in range(1,4):
            df_s918b_home = pd.read_csv("D:\\Users\\jussif.arnez\\Documents\\2021_IMS\\my_documents\\my_Research\\my_plotting\\Display_Power\\Reteste\\S918B_normal\\idle\\idle_screen_S918B_test_" + str(val) + ".csv")
            select_ = df_s918b_home[df_s918b_home['Main Avg Current (mA)'] <= self.limiar]['Main Avg Current (mA)']
            s918b_home['s918b_normal_idt'+ str(val)] = select_ 
        fig_s918b_home = go.Figure()

        trace_s918b_idt1 = go.Scatter(y=s918b_home['s918b_normal_idt1'], 
                                        name= 'S918B Home Screen Test 1',
                                        mode='lines', 
                                        line=dict(width=1, color ='#008ae6')
        )
        trace_s918b_idt2 = go.Scatter(y=s918b_home['s918b_normal_idt2'], 
                                        name= 'S918B Home Screen Test 2',
                                        mode='lines', 
                                        line=dict(width=1, color ='#00b36b')
        )
        trace_s918b_idt3 = go.Scatter(y=s918b_home['s918b_normal_idt3'], 
                                        name= 'S918B Home Screen Test 3',
                                        mode='lines', 
                                        line=dict(width=1, color ='#ff8080')
        )

        fig_s918b_home.add_trace(trace_s918b_idt1)
        fig_s918b_home.add_trace(trace_s918b_idt2)
        fig_s918b_home.add_trace(trace_s918b_idt3)
        fig_s918b_home.update_layout(yaxis=dict(range=[100,1000]))
        # fig_s918b_home.show(renderer="browser")
        s918b_home_mean = s918b_home.mean()
        df_s918b_home_mean = pd.DataFrame(s918b_home_mean).transpose()

        self.df_s918b_home_mean_reshaped= pd.DataFrame(
                df_s918b_home_mean.values.reshape(3,1), 
                columns = ['s918b_light_idle'],
                index = ['t1', 't2', 't3']
        )

        #$ Dark Mode
        s918b_home_dark = pd.DataFrame()
        for val in range(1,4):
            df_s918b_home_dark = pd.read_csv("D:\\Users\\jussif.arnez\\Documents\\2021_IMS\\my_documents\\my_Research\\my_plotting\\Display_Power\\Reteste\\S918B_dark_mode\\idle\\idle_screen_S918B_test_" + str(val) + ".csv")
            select_ = df_s918b_home_dark[df_s918b_home_dark['Main Avg Current (mA)'] <= self.limiar]['Main Avg Current (mA)']
            #data_s918b = { 's918b_normal_t'+ str(val) : select_}
            s918b_home_dark['s918b_dark_idt'+ str(val)] = select_
        
        s918b_home_dark_mean = s918b_home_dark.mean()
        df_s918b_home_dark_mean = pd.DataFrame(s918b_home_dark_mean).transpose()

        self.df_s918b_home_dark_mean_reshaped= pd.DataFrame(
                df_s918b_home_dark_mean.values.reshape(3,1), 
                columns = ['s918b_dark_idle'],
                index = ['t1', 't2', 't3']
        )

    def Plotting_Home(self):
        #Comparison
        fig_bar_home_comparison = go.Figure(
        layout_title_text="Comparison of Average Current Consumption For Different DuTs in Idle for Light and Dark Modes",
        )

        #$ light and dark mode for A146M
        fig_bar_home_comparison.add_bar(y=['Test 1', 'Test 2', 'Test 3'], 
                    x=self.df_a146m_home_mean_reshaped['a146m_light_idle'], 
                    text=[round(val, 3) for val in self.df_a146m_home_mean_reshaped['a146m_light_idle']],
                    name="PLS LCD in Idle for Light Mode",
                    orientation="h",
                    textposition="inside", insidetextanchor="middle", textfont=dict(size=20),
                    marker=dict(line=dict(width=2), color='#ff33ff')
                )

        fig_bar_home_comparison.add_bar(y=['Test 1', 'Test 2', 'Test 3'], 
                            x=self.df_a146m_home_dark_mean_reshaped['a146m_dark_idle'], 
                            text=[round(val, 3) for val in self.df_a146m_home_dark_mean_reshaped['a146m_dark_idle']],
                            name="PLS LCD in Idle for Dark Mode",
                            orientation="h",
                            textposition="inside", insidetextanchor="middle", textfont=dict(size=20),
                            marker=dict(line=dict(width=2), color='#751aff')
                        )

        #$ light and dark mode for S918b
        fig_bar_home_comparison.add_bar(y=['Test 1', 'Test 2', 'Test 3'], 
                    x=self.df_s918b_home_mean_reshaped['s918b_light_idle'], 
                    text=[round(val, 3) for val in self.df_s918b_home_mean_reshaped['s918b_light_idle']],
                    name="Dynamic Amoled in Idle for Light Mode",
                    orientation="h",
                    textposition="inside", insidetextanchor="middle", textfont=dict(size=20),
                    marker=dict(line=dict(width=2), color='blue')
                )

        fig_bar_home_comparison.add_bar(y=['Test 1', 'Test 2', 'Test 3'], 
                            x=self.df_s918b_home_dark_mean_reshaped['s918b_dark_idle'], 
                            text=[round(val, 3) for val in self.df_s918b_home_dark_mean_reshaped['s918b_dark_idle']],
                            name="Dynamic Amoled in Idle for Dark Mode",
                            orientation="h",
                            textposition="inside", insidetextanchor="middle", textfont=dict(size=20),
                            marker=dict(line=dict(width=2), color='purple')
                        )

        fig_bar_home_comparison.update_layout(
                        title={'text': "", 'font': {'size': 1}},

                        xaxis_title={'text': "Average Current Consumption (mA)", 'font': {'size': self.my_figure['TAMANHO_LEG']}},
                        width=1500, height=800,
                        yaxis=dict(
                            tickfont=dict(size=self.my_figure['TAMANHO_TICK']),
                        ),
                        xaxis=dict(tickfont=dict(size=self.my_figure['TAMANHO_TICK']),
                                range=[0, 365]),
                        legend=dict(
                            font=dict(size=self.my_figure['TAMANHO_LEG']),
                            orientation='h',
                            yanchor='top',
                            y=1.15,
                            xanchor='center',
                            x=0.5
                        ),
                        plot_bgcolor='white',
                        shapes=[
                            dict(
                                type='rect',
                                xref='paper',
                                yref='paper',
                                x0=0,
                                y0=0,
                                x1=1.001,
                                y1=1.001,
                                line=dict(
                                    color='black',
                                    width=1,
                                )
                            )
                        ],
        )
        fig_bar_home_comparison.show(renderer="browser")
        # fig_bar_home_comparison.write_html("lcd_amolead_home_screens.html")
        #! to avoid the message appears on the pdf file.
        # pio.full_figure_for_development(fig_bar_home_comparison, warn=False)
        # fig_bar_home_comparison.write_image("lcd_amoled_home_screens.pdf", width= 1500 , height= 800, engine="kaleido")

    def Screens_s918b(self):
        #$ White and Black Screens
        s918b_ = pd.DataFrame()
        for val in range(1,4):
            #dark mode white screen
            df_s918b = pd.read_csv("D:\\Users\\jussif.arnez\\Documents\\2021_IMS\\my_documents\\my_Research\\my_plotting\\Display_Power\\Reteste\\S918B_dark_mode\\white\\white_screen_S918B_test_" + str(val) + ".csv")
            select_dark_w = df_s918b[df_s918b['Main Avg Current (mA)'] <= self.limiar]['Main Avg Current (mA)']
            s918b_['s918b_dark_wt'+ str(val)] = select_dark_w 

            #dark mode black screen
            df_s918b = pd.read_csv("D:\\Users\\jussif.arnez\\Documents\\2021_IMS\\my_documents\\my_Research\\my_plotting\\Display_Power\\Reteste\\S918B_dark_mode\\black\\black_screen_S918B_test_" + str(val) + ".csv")
            select_dark_b = df_s918b[df_s918b['Main Avg Current (mA)'] <= self.limiar]['Main Avg Current (mA)']
            s918b_['s918b_dark_bt'+ str(val)] = select_dark_b
        
        fig_s918b = go.Figure()
        #---- dark mode
        trace_s918b_dark_wt1 = go.Scatter(y=s918b_['s918b_dark_wt1'], 
                                        name= 's918b Dark White Screen Test 1',
                                        mode='lines', 
                                        line=dict(width=1, color ='#008ae6')
        )
        trace_s918b_dark_wt2 = go.Scatter(y=s918b_['s918b_dark_wt2'], 
                                        name= 's918b Dark White Screen Test 2',
                                        mode='lines', 
                                        line=dict(width=1, color =' #00b36b')
        )
        trace_s918b_dark_wt3 = go.Scatter(y=s918b_['s918b_dark_wt3'], 
                                        name= 's918b Dark White Screen Test 3',
                                        mode='lines', 
                                        line=dict(width=1, color ='#ff8080')
        )

        trace_s918b_dark_bt1 = go.Scatter(y=s918b_['s918b_dark_bt1'], 
                                        name= 's918b Dark Black Screen Test 1',
                                        mode='lines', 
                                        line=dict(width=1, color ='#a6ff4d')
        )
        trace_s918b_dark_bt2 = go.Scatter(y=s918b_['s918b_dark_bt2'], 
                                        name= 's918b Dark Black Screen Test 2',
                                        mode='lines', 
                                        line=dict(width=1, color ='#009900')
        )
        trace_s918b_dark_bt3 = go.Scatter(y=s918b_['s918b_dark_bt3'], 
                                        name= 's918b Dark Black Screen Test 3',
                                        mode='lines', 
                                        line=dict(width=1, color ='#e67300')
        )

        #dark mode
        fig_s918b.add_trace(trace_s918b_dark_wt1)
        fig_s918b.add_trace(trace_s918b_dark_wt2)
        fig_s918b.add_trace(trace_s918b_dark_wt3)
        fig_s918b.add_trace(trace_s918b_dark_bt1)
        fig_s918b.add_trace(trace_s918b_dark_bt2)
        fig_s918b.add_trace(trace_s918b_dark_bt3)

        fig_s918b.update_layout(yaxis=dict(range=[300,1000]))
        # fig_s918b.show(renderer="browser")

        #computing mean
        s9128b_mean = s918b_.mean()
        df_s9128b_mean = pd.DataFrame(s9128b_mean).transpose()
        # new_order = ['s918b_dark_wt1', 's918b_dark_wt2', 's918b_dark_wt3',
        #                 's918b_dark_bt1', 's918b_dark_bt2', 's918b_dark_bt3'
        # ]
        # df_s9128b_mean = df_s9128b_mean[new_order]
        self.df_s9128b_mean_reshaped= pd.DataFrame(
                df_s9128b_mean.values.reshape(3,2), 
                columns = ['s918b_dark_white', 's918b_dark_black'],
                index = ['t1', 't2', 't3']
        )

    def Screens_a146m(self):
        #$ White and Black Screens
        a146m_ = pd.DataFrame()
        for val in range(1,4):
            #light mode white screen
            df_a146m = pd.read_csv("D:\\Users\\jussif.arnez\\Documents\\2021_IMS\\my_documents\\my_Research\\my_plotting\\Display_Power\\Reteste\\A146M_normal\\white\\white_screen_A146M_test_" + str(val) + ".csv")
            select_nw = df_a146m[df_a146m['Main Avg Current (mA)'] <= self.limiar]['Main Avg Current (mA)']
            a146m_['a146m_normal_wt'+ str(val)] = select_nw

            #light mode black screen
            df_a146m_b = pd.read_csv("D:\\Users\\jussif.arnez\\Documents\\2021_IMS\\my_documents\\my_Research\\my_plotting\\Display_Power\\Reteste\\A146M_normal\\black\\black_screen_A146M_test_" + str(val) + ".csv")
            select_nb = df_a146m_b[df_a146m_b['Main Avg Current (mA)'] <= self.limiar]['Main Avg Current (mA)']
            a146m_['a146m_normal_bt'+ str(val)] = select_nb 

        fig_a146m = go.Figure()

        trace_a146m_wt1 = go.Scatter(y=a146m_['a146m_normal_wt1'], 
                                        name= 'A146M White Screen Test 1',
                                        mode='lines', 
                                        line=dict(width=1, color ='green')
        )
        trace_a146m_wt2 = go.Scatter(y=a146m_['a146m_normal_wt2'], 
                                        name= 'A146M White Screen Test 2',
                                        mode='lines', 
                                        line=dict(width=1, color ='blue')
        )
        trace_a146m_wt3 = go.Scatter(y=a146m_['a146m_normal_wt3'], 
                                        name= 'A146M White Screen Test 3',
                                        mode='lines', 
                                        line=dict(width=1, color ='orange')
        )

        trace_a146m_bt1 = go.Scatter(y=a146m_['a146m_normal_bt1'], 
                                        name= 'A146M Black Screen Test 1',
                                        mode='lines', 
                                        line=dict(width=1, color ='pink')
        )
        trace_a146m_bt2 = go.Scatter(y=a146m_['a146m_normal_bt2'], 
                                        name= 'A146M Black Screen Test 2',
                                        mode='lines', 
                                        line=dict(width=1, color ='cyan')
        )
        trace_a146m_bt3 = go.Scatter(y=a146m_['a146m_normal_bt3'], 
                                        name= 'A146M Black Screen Test 3',
                                        mode='lines', 
                                        line=dict(width=1, color ='purple')
        )

        fig_a146m.add_trace(trace_a146m_wt1)
        fig_a146m.add_trace(trace_a146m_wt2)
        fig_a146m.add_trace(trace_a146m_wt3)
        fig_a146m.add_trace(trace_a146m_bt1)
        fig_a146m.add_trace(trace_a146m_bt2)
        fig_a146m.add_trace(trace_a146m_bt3)
        fig_a146m.update_layout(yaxis=dict(range=[300,1000]))
        # fig_a146m.show(renderer="browser")

        #computing mean
        a146m_mean = a146m_.mean()
        df_a146m_mean = pd.DataFrame(a146m_mean).transpose()
        # new_order = ['s918b_dark_wt1', 's918b_dark_wt2', 's918b_dark_wt3',
        #                 's918b_dark_bt1', 's918b_dark_bt2', 's918b_dark_bt3'
        # ]
        # df_s9128b_mean = df_s9128b_mean[new_order]

        self.df_a146m_mean_reshaped= pd.DataFrame(
                df_a146m_mean.values.reshape(3,2), 
                columns = ['a146m_light_white', 'a146m_light_black'],
                index = ['t1', 't2', 't3']
        )

    def Measurements_jj(self):
        #$ Type-input(i), Swipe(s) and Talk(t) 

        #A146M i79
        df1_jj_i79 = pd.read_csv("D:\\Users\\jussif.arnez\\Documents\\2021_IMS\\my_documents\\my_Research\\my_plotting\\Display_Power\\Reteste\\grafico editado\\Jussif A146M\\input 79 char\\input_char79_screen_dark_A146M_test_1_edit.csv")

        df2_jj_i79 = pd.read_csv("D:\\Users\\jussif.arnez\\Documents\\2021_IMS\\my_documents\\my_Research\\my_plotting\\Display_Power\\Reteste\\grafico editado\\Jussif A146M\\input 79 char\\input_char79_screen_dark_A146M_test_2_edit.csv")
        df3_jj_i79 = pd.read_csv("D:\\Users\\jussif.arnez\\Documents\\2021_IMS\\my_documents\\my_Research\\my_plotting\\Display_Power\\Reteste\\grafico editado\\Jussif A146M\\input 79 char\\input_char79_screen_dark_A146M_test_3_edit.csv")

        #A146M i202
        df1_jj_i202 = pd.read_csv("D:\\Users\\jussif.arnez\\Documents\\2021_IMS\\my_documents\\my_Research\\my_plotting\\Display_Power\\Reteste\\grafico editado\\Jussif A146M\\input 202 char\\input_char202_screen_dark_A146M_test_1_edit.csv")
        df2_jj_i202 = pd.read_csv("D:\\Users\\jussif.arnez\\Documents\\2021_IMS\\my_documents\\my_Research\\my_plotting\\Display_Power\\Reteste\\grafico editado\\Jussif A146M\\input 202 char\\input_char202_screen_dark_A146M_test_2_edit.csv")
        df3_jj_i202 = pd.read_csv("D:\\Users\\jussif.arnez\\Documents\\2021_IMS\\my_documents\\my_Research\\my_plotting\\Display_Power\\Reteste\\grafico editado\\Jussif A146M\\input 202 char\\input_char202_screen_dark_A146M_test_3_edit.csv")

        #A146M s79
        df1_jj_s79 = pd.read_csv("D:\\Users\\jussif.arnez\\Documents\\2021_IMS\\my_documents\\my_Research\\my_plotting\\Display_Power\\Reteste\\grafico editado\\Jussif A146M\\swipe 79 char\\swipe_char79_screen_dark_A146M_test_1_edit.csv")
        df2_jj_s79 = pd.read_csv("D:\\Users\\jussif.arnez\\Documents\\2021_IMS\\my_documents\\my_Research\\my_plotting\\Display_Power\\Reteste\\grafico editado\\Jussif A146M\\swipe 79 char\\swipe_char79_screen_dark_A146M_test_2_edit.csv")
        df3_jj_s79 = pd.read_csv("D:\\Users\\jussif.arnez\\Documents\\2021_IMS\\my_documents\\my_Research\\my_plotting\\Display_Power\\Reteste\\grafico editado\\Jussif A146M\\swipe 79 char\\swipe_char79_screen_dark_A146M_test_3_edit.csv")

        #A146M s202
        df1_jj_s202 = pd.read_csv("D:\\Users\\jussif.arnez\\Documents\\2021_IMS\\my_documents\\my_Research\\my_plotting\\Display_Power\\Reteste\\grafico editado\\Jussif A146M\\swipe 202 char\\swipe_char202_screen_dark_A146M_test_1_edit.csv")
        df2_jj_s202 = pd.read_csv("D:\\Users\\jussif.arnez\\Documents\\2021_IMS\\my_documents\\my_Research\\my_plotting\\Display_Power\\Reteste\\grafico editado\\Jussif A146M\\swipe 202 char\\swipe_char202_screen_dark_A146M_test_2_edit.csv")
        df3_jj_s202 = pd.read_csv("D:\\Users\\jussif.arnez\\Documents\\2021_IMS\\my_documents\\my_Research\\my_plotting\\Display_Power\\Reteste\\grafico editado\\Jussif A146M\\swipe 202 char\\swipe_char202_screen_dark_A146M_test_3_edit.csv")

        #A146M t79 no edit
        df1_jj_t79 = pd.read_csv("D:\\Users\\jussif.arnez\\Documents\\2021_IMS\\my_documents\\my_Research\\my_plotting\\Display_Power\\Reteste\\grafico editado\\Jussif A146M\\talk 79 char\\talk_char79_screen_dark_A146M_test_1.csv")
        df2_jj_t79 = pd.read_csv("D:\\Users\\jussif.arnez\\Documents\\2021_IMS\\my_documents\\my_Research\\my_plotting\\Display_Power\\Reteste\\grafico editado\\Jussif A146M\\talk 79 char\\talk_char79_screen_dark_A146M_test_2.csv")
        df3_jj_t79 = pd.read_csv("D:\\Users\\jussif.arnez\\Documents\\2021_IMS\\my_documents\\my_Research\\my_plotting\\Display_Power\\Reteste\\grafico editado\\Jussif A146M\\talk 79 char\\talk_char79_screen_dark_A146M_test_3.csv")

        #A146M t202 no edit
        df1_jj_t202 = pd.read_csv("D:\\Users\\jussif.arnez\\Documents\\2021_IMS\\my_documents\\my_Research\\my_plotting\\Display_Power\\Reteste\\grafico editado\\Jussif A146M\\talk 202 char\\talk_char202_screen_dark_A146M_test_1.csv")
        df2_jj_t202 = pd.read_csv("D:\\Users\\jussif.arnez\\Documents\\2021_IMS\\my_documents\\my_Research\\my_plotting\\Display_Power\\Reteste\\grafico editado\\Jussif A146M\\talk 202 char\\talk_char202_screen_dark_A146M_test_2.csv")
        df3_jj_t202 = pd.read_csv("D:\\Users\\jussif.arnez\\Documents\\2021_IMS\\my_documents\\my_Research\\my_plotting\\Display_Power\\Reteste\\grafico editado\\Jussif A146M\\talk 202 char\\talk_char202_screen_dark_A146M_test_3.csv")

        #S918B i79
        df1_jj_i79_S = pd.read_csv("D:\\Users\\jussif.arnez\\Documents\\2021_IMS\\my_documents\\my_Research\\my_plotting\\Display_Power\\Reteste\\grafico editado\\Jussif S918B\\input 79 char\\input_char79_screen_dark_S918B_test1_edit.csv")

        df2_jj_i79_S = pd.read_csv("D:\\Users\\jussif.arnez\\Documents\\2021_IMS\\my_documents\\my_Research\\my_plotting\\Display_Power\\Reteste\\grafico editado\\Jussif S918B\\input 79 char\\input_char79_screen_dark_S918B_test2_edit.csv")
        df3_jj_i79_S = pd.read_csv("D:\\Users\\jussif.arnez\\Documents\\2021_IMS\\my_documents\\my_Research\\my_plotting\\Display_Power\\Reteste\\grafico editado\\Jussif S918B\\input 79 char\\input_char79_screen_dark_S918B_test3_edit.csv")

        #S918B i202
        df1_jj_i202_S = pd.read_csv("D:\\Users\\jussif.arnez\\Documents\\2021_IMS\\my_documents\\my_Research\\my_plotting\\Display_Power\\Reteste\\grafico editado\\Jussif S918B\\input 202 char\\input_char202_screen_dark_S918B_test1_edit.csv")
        df2_jj_i202_S = pd.read_csv("D:\\Users\\jussif.arnez\\Documents\\2021_IMS\\my_documents\\my_Research\\my_plotting\\Display_Power\\Reteste\\grafico editado\\Jussif S918B\\input 202 char\\input_char202_screen_dark_S918B_test2_edit.csv")
        df3_jj_i202_S = pd.read_csv("D:\\Users\\jussif.arnez\\Documents\\2021_IMS\\my_documents\\my_Research\\my_plotting\\Display_Power\\Reteste\\grafico editado\\Jussif S918B\\input 202 char\\input_char202_screen_dark_S918B_test3_edit.csv")

        #S918B s79
        df1_jj_s79_S = pd.read_csv("D:\\Users\\jussif.arnez\\Documents\\2021_IMS\\my_documents\\my_Research\\my_plotting\\Display_Power\\Reteste\\grafico editado\\Jussif S918B\\swipe 79 char\\swipe_char79_screen_dark_S918B_test1_edit.csv")
        df2_jj_s79_S = pd.read_csv("D:\\Users\\jussif.arnez\\Documents\\2021_IMS\\my_documents\\my_Research\\my_plotting\\Display_Power\\Reteste\\grafico editado\\Jussif S918B\\swipe 79 char\\swipe_char79_screen_dark_S918B_test2_edit.csv")
        df3_jj_s79_S = pd.read_csv("D:\\Users\\jussif.arnez\\Documents\\2021_IMS\\my_documents\\my_Research\\my_plotting\\Display_Power\\Reteste\\grafico editado\\Jussif S918B\\swipe 79 char\\swipe_char79_screen_dark_S918B_test3_edit.csv")

        #S918B s202
        df1_jj_s202_S = pd.read_csv("D:\\Users\\jussif.arnez\\Documents\\2021_IMS\\my_documents\\my_Research\\my_plotting\\Display_Power\\Reteste\\grafico editado\\Jussif S918B\\swipe 202 char\\swipe_char202_screen_dark_S918B_test1_edit.csv")
        df2_jj_s202_S = pd.read_csv("D:\\Users\\jussif.arnez\\Documents\\2021_IMS\\my_documents\\my_Research\\my_plotting\\Display_Power\\Reteste\\grafico editado\\Jussif S918B\\swipe 202 char\\swipe_char202_screen_dark_S918B_test2_edit.csv")
        df3_jj_s202_S = pd.read_csv("D:\\Users\\jussif.arnez\\Documents\\2021_IMS\\my_documents\\my_Research\\my_plotting\\Display_Power\\Reteste\\grafico editado\\Jussif S918B\\swipe 202 char\\swipe_char202_screen_dark_S918B_test3_edit.csv")

        #S918B t79 no edit
        df1_jj_t79_S = pd.read_csv("D:\\Users\\jussif.arnez\\Documents\\2021_IMS\\my_documents\\my_Research\\my_plotting\\Display_Power\\Reteste\\grafico editado\\Jussif S918B\\talk 79 char\\talk_char79_screen_dark_S918B_test1.csv")
        df2_jj_t79_S = pd.read_csv("D:\\Users\\jussif.arnez\\Documents\\2021_IMS\\my_documents\\my_Research\\my_plotting\\Display_Power\\Reteste\\grafico editado\\Jussif S918B\\talk 79 char\\talk_char79_screen_dark_S918B_test2.csv")
        df3_jj_t79_S = pd.read_csv("D:\\Users\\jussif.arnez\\Documents\\2021_IMS\\my_documents\\my_Research\\my_plotting\\Display_Power\\Reteste\\grafico editado\\Jussif S918B\\talk 79 char\\talk_char79_screen_dark_S918B_test3.csv")

        #S918B t202 no edit
        df1_jj_t202_S = pd.read_csv("D:\\Users\\jussif.arnez\\Documents\\2021_IMS\\my_documents\\my_Research\\my_plotting\\Display_Power\\Reteste\\grafico editado\\Jussif S918B\\talk 202 char\\talk_char202_screen_dark_S918B_test1.csv")
        df2_jj_t202_S = pd.read_csv("D:\\Users\\jussif.arnez\\Documents\\2021_IMS\\my_documents\\my_Research\\my_plotting\\Display_Power\\Reteste\\grafico editado\\Jussif S918B\\talk 202 char\\talk_char202_screen_dark_S918B_test2.csv")
        df3_jj_t202_S = pd.read_csv("D:\\Users\\jussif.arnez\\Documents\\2021_IMS\\my_documents\\my_Research\\my_plotting\\Display_Power\\Reteste\\grafico editado\\Jussif S918B\\talk 202 char\\talk_char202_screen_dark_S918B_test3.csv")

        data_jj={
        'A146M_input_char79': 
            [df1_jj_i79['Main Avg Current (mA)'].mean(), 
            df2_jj_i79['Main Avg Current (mA)'].mean(),
            df3_jj_i79['Main Avg Current (mA)'].mean()
            ],
        'A146M_input_char202': 
            [df1_jj_i202['Main Avg Current (mA)'].mean(), 
            df2_jj_i202['Main Avg Current (mA)'].mean(),
            df3_jj_i202['Main Avg Current (mA)'].mean()
            ],
        'A146M_swipe_char79': 
            [df1_jj_s79['Main Avg Current (mA)'].mean(), 
            df2_jj_s79['Main Avg Current (mA)'].mean(),
            df3_jj_s79['Main Avg Current (mA)'].mean()
            ],
        'A146M_swipe_char202': 
            [df1_jj_s202['Main Avg Current (mA)'].mean(), 
            df2_jj_s202['Main Avg Current (mA)'].mean(),
            df3_jj_s202['Main Avg Current (mA)'].mean()
            ],
        'A146M_talk_char79': 
            [df1_jj_t79['Main Avg Current (mA)'].mean(), 
            df2_jj_t79['Main Avg Current (mA)'].mean(),
            df3_jj_t79['Main Avg Current (mA)'].mean()
            ],
        'A146M_talk_char202': 
            [df1_jj_t202['Main Avg Current (mA)'].mean(), 
            df2_jj_t202['Main Avg Current (mA)'].mean(),
            df3_jj_t202['Main Avg Current (mA)'].mean()
            ],
        #s198b
        'S918B_input_char79': 
            [df1_jj_i79_S['Main Avg Current (mA)'].mean(), 
            df2_jj_i79_S['Main Avg Current (mA)'].mean(),
            df3_jj_i79_S['Main Avg Current (mA)'].mean()
            ],
        'S918B_input_char202': 
            [df1_jj_i202_S['Main Avg Current (mA)'].mean(), 
            df2_jj_i202_S['Main Avg Current (mA)'].mean(),
            df3_jj_i202_S['Main Avg Current (mA)'].mean()
            ],
        'S918B_swipe_char79': 
            [df1_jj_s79_S['Main Avg Current (mA)'].mean(), 
            df2_jj_s79_S['Main Avg Current (mA)'].mean(),
            df3_jj_s79_S['Main Avg Current (mA)'].mean()
            ],
        'S918B_swipe_char202': 
            [df1_jj_s202_S['Main Avg Current (mA)'].mean(), 
            df2_jj_s202_S['Main Avg Current (mA)'].mean(),
            df3_jj_s202_S['Main Avg Current (mA)'].mean()
            ],
        'S918B_talk_char79': 
            [df1_jj_t79_S['Main Avg Current (mA)'].mean(), 
            df2_jj_t79_S['Main Avg Current (mA)'].mean(),
            df3_jj_t79_S['Main Avg Current (mA)'].mean()
            ],
        'S918B_talk_char202': 
            [df1_jj_t202_S['Main Avg Current (mA)'].mean(), 
            df2_jj_t202_S['Main Avg Current (mA)'].mean(),
            df3_jj_t202_S['Main Avg Current (mA)'].mean()
            ]
        }

        self.jussif_energy = pd.DataFrame(data=data_jj, index=['t1','t2','t3'])

    def Measurements_gg(self):
        #$ Type-input(i), Swipe(s) and Talk(t)
        #GIDY
        #A146M i79; teste 3 não editado
        df1_gg_i79 = pd.read_csv("D:\\Users\\jussif.arnez\\Documents\\2021_IMS\\my_documents\\my_Research\\my_plotting\\Display_Power\\Reteste\\grafico editado\\Gidy A146M\\input 79 char\\input_char79_screen_dark_A146M_test_1_edit.csv")

        df2_gg_i79 = pd.read_csv("D:\\Users\\jussif.arnez\\Documents\\2021_IMS\\my_documents\\my_Research\\my_plotting\\Display_Power\\Reteste\\grafico editado\\Gidy A146M\\input 79 char\\input_char79_screen_dark_A146M_test_2_edit.csv")
        df3_gg_i79 = pd.read_csv("D:\\Users\\jussif.arnez\\Documents\\2021_IMS\\my_documents\\my_Research\\my_plotting\\Display_Power\\Reteste\\grafico editado\\Gidy A146M\\input 79 char\\input_char79_screen_dark_A146M_test_3.csv")

        #A146M i202
        df1_gg_i202 = pd.read_csv("D:\\Users\\jussif.arnez\\Documents\\2021_IMS\\my_documents\\my_Research\\my_plotting\\Display_Power\\Reteste\\grafico editado\\Gidy A146M\\input 202 char\\input_char202_screen_dark_A146M_test_1_edit.csv")
        df2_gg_i202 = pd.read_csv("D:\\Users\\jussif.arnez\\Documents\\2021_IMS\\my_documents\\my_Research\\my_plotting\\Display_Power\\Reteste\\grafico editado\\Gidy A146M\\input 202 char\\input_char202_screen_dark_A146M_test_2_edit.csv")
        df3_gg_i202 = pd.read_csv("D:\\Users\\jussif.arnez\\Documents\\2021_IMS\\my_documents\\my_Research\\my_plotting\\Display_Power\\Reteste\\grafico editado\\Gidy A146M\\input 202 char\\input_char202_screen_dark_A146M_test_3_edit.csv")

        #A146M s79
        df1_gg_s79 = pd.read_csv("D:\\Users\\jussif.arnez\\Documents\\2021_IMS\\my_documents\\my_Research\\my_plotting\\Display_Power\\Reteste\\grafico editado\\Gidy A146M\\swipe 79 char\\swipe_char79_screen_dark_A146M_test_1_edit.csv")
        df2_gg_s79 = pd.read_csv("D:\\Users\\jussif.arnez\\Documents\\2021_IMS\\my_documents\\my_Research\\my_plotting\\Display_Power\\Reteste\\grafico editado\\Gidy A146M\\swipe 79 char\\swipe_char79_screen_dark_A146M_test_2_edit.csv")
        df3_gg_s79 = pd.read_csv("D:\\Users\\jussif.arnez\\Documents\\2021_IMS\\my_documents\\my_Research\\my_plotting\\Display_Power\\Reteste\\grafico editado\\Gidy A146M\\swipe 79 char\\swipe_char79_screen_dark_A146M_test_3_edit.csv")

        #A146M s202
        df1_gg_s202 = pd.read_csv("D:\\Users\\jussif.arnez\\Documents\\2021_IMS\\my_documents\\my_Research\\my_plotting\\Display_Power\\Reteste\\grafico editado\\Gidy A146M\\swipe 202 char\\swipe_char202_screen_dark_A146M_test_1_edit.csv")
        df2_gg_s202 = pd.read_csv("D:\\Users\\jussif.arnez\\Documents\\2021_IMS\\my_documents\\my_Research\\my_plotting\\Display_Power\\Reteste\\grafico editado\\Gidy A146M\\swipe 202 char\\swipe_char202_screen_dark_A146M_test_2_edit.csv")
        df3_gg_s202 = pd.read_csv("D:\\Users\\jussif.arnez\\Documents\\2021_IMS\\my_documents\\my_Research\\my_plotting\\Display_Power\\Reteste\\grafico editado\\Gidy A146M\\swipe 202 char\\swipe_char202_screen_dark_A146M_test_3_edit.csv")

        #A146M t79 no edit
        df1_gg_t79 = pd.read_csv("D:\\Users\\jussif.arnez\\Documents\\2021_IMS\\my_documents\\my_Research\\my_plotting\\Display_Power\\Reteste\\grafico editado\\Gidy A146M\\talk 79 char\\talk_char79_screen_dark_A146M_test_1.csv")
        df2_gg_t79 = pd.read_csv("D:\\Users\\jussif.arnez\\Documents\\2021_IMS\\my_documents\\my_Research\\my_plotting\\Display_Power\\Reteste\\grafico editado\\Gidy A146M\\talk 79 char\\talk_char79_screen_dark_A146M_test_2.csv")
        df3_gg_t79 = pd.read_csv("D:\\Users\\jussif.arnez\\Documents\\2021_IMS\\my_documents\\my_Research\\my_plotting\\Display_Power\\Reteste\\grafico editado\\Gidy A146M\\talk 79 char\\talk_char79_screen_dark_A146M_test_3.csv")

        #A146M t202 no edit
        df1_gg_t202 = pd.read_csv("D:\\Users\\jussif.arnez\\Documents\\2021_IMS\\my_documents\\my_Research\\my_plotting\\Display_Power\\Reteste\\grafico editado\\Gidy A146M\\talk 202 char\\talk_char202_screen_dark_A146M_test_1.csv")
        df2_gg_t202 = pd.read_csv("D:\\Users\\jussif.arnez\\Documents\\2021_IMS\\my_documents\\my_Research\\my_plotting\\Display_Power\\Reteste\\grafico editado\\Gidy A146M\\talk 202 char\\talk_char202_screen_dark_A146M_test_2.csv")
        df3_gg_t202 = pd.read_csv("D:\\Users\\jussif.arnez\\Documents\\2021_IMS\\my_documents\\my_Research\\my_plotting\\Display_Power\\Reteste\\grafico editado\\Gidy A146M\\talk 202 char\\talk_char202_screen_dark_A146M_test_3.csv")

        #Gidy S918B i79
        df1_gg_i79_S = pd.read_csv("D:\\Users\\jussif.arnez\\Documents\\2021_IMS\\my_documents\\my_Research\\my_plotting\\Display_Power\\Reteste\\grafico editado\\Gidy S918B\\input 79 char\\input_char79_screen_dark_S918B_test_1_edit.csv")

        df2_gg_i79_S = pd.read_csv("D:\\Users\\jussif.arnez\\Documents\\2021_IMS\\my_documents\\my_Research\\my_plotting\\Display_Power\\Reteste\\grafico editado\\Gidy S918B\\input 79 char\\input_char79_screen_dark_S918B_test_2_edit.csv")
        df3_gg_i79_S = pd.read_csv("D:\\Users\\jussif.arnez\\Documents\\2021_IMS\\my_documents\\my_Research\\my_plotting\\Display_Power\\Reteste\\grafico editado\\Gidy S918B\\input 79 char\\input_char79_screen_dark_S918B_test_3_edit.csv")

        #S918B i202
        df1_gg_i202_S = pd.read_csv("D:\\Users\\jussif.arnez\\Documents\\2021_IMS\\my_documents\\my_Research\\my_plotting\\Display_Power\\Reteste\\grafico editado\\Gidy S918B\\input 202 char\\input_char202_screen_dark_S918B_test_1_edit.csv")
        df2_gg_i202_S = pd.read_csv("D:\\Users\\jussif.arnez\\Documents\\2021_IMS\\my_documents\\my_Research\\my_plotting\\Display_Power\\Reteste\\grafico editado\\Gidy S918B\\input 202 char\\input_char202_screen_dark_S918B_test_2_edit.csv")
        df3_gg_i202_S = pd.read_csv("D:\\Users\\jussif.arnez\\Documents\\2021_IMS\\my_documents\\my_Research\\my_plotting\\Display_Power\\Reteste\\grafico editado\\Gidy S918B\\input 202 char\\input_char202_screen_dark_S918B_test_3_edit.csv")

        #S918B s79, test 3 no edit
        df1_gg_s79_S = pd.read_csv("D:\\Users\\jussif.arnez\\Documents\\2021_IMS\\my_documents\\my_Research\\my_plotting\\Display_Power\\Reteste\\grafico editado\\Gidy S918B\\swipe 79 char\\swipe_char79_screen_dark_S918B_test_1_edit.csv")
        df2_gg_s79_S = pd.read_csv("D:\\Users\\jussif.arnez\\Documents\\2021_IMS\\my_documents\\my_Research\\my_plotting\\Display_Power\\Reteste\\grafico editado\\Gidy S918B\\swipe 79 char\\swipe_char79_screen_dark_S918B_test_2_edit.csv")
        df3_gg_s79_S = pd.read_csv("D:\\Users\\jussif.arnez\\Documents\\2021_IMS\\my_documents\\my_Research\\my_plotting\\Display_Power\\Reteste\\grafico editado\\Gidy S918B\\swipe 79 char\\swipe_char79_screen_dark_S918B_test_3.csv")

        #S918B s202
        df1_gg_s202_S = pd.read_csv("D:\\Users\\jussif.arnez\\Documents\\2021_IMS\\my_documents\\my_Research\\my_plotting\\Display_Power\\Reteste\\grafico editado\\Gidy S918B\\swipe 202 char\\swipe_char202_screen_dark_S918B_test_1_edit.csv")
        df2_gg_s202_S = pd.read_csv("D:\\Users\\jussif.arnez\\Documents\\2021_IMS\\my_documents\\my_Research\\my_plotting\\Display_Power\\Reteste\\grafico editado\\Gidy S918B\\swipe 202 char\\swipe_char202_screen_dark_S918B_test_2_edit.csv")
        df3_gg_s202_S = pd.read_csv("D:\\Users\\jussif.arnez\\Documents\\2021_IMS\\my_documents\\my_Research\\my_plotting\\Display_Power\\Reteste\\grafico editado\\Gidy S918B\\swipe 202 char\\swipe_char202_screen_dark_S918B_test_3_edit.csv")

        #S918B t79 no edit
        df1_gg_t79_S = pd.read_csv("D:\\Users\\jussif.arnez\\Documents\\2021_IMS\\my_documents\\my_Research\\my_plotting\\Display_Power\\Reteste\\grafico editado\\Gidy S918B\\talk 79 char\\talk_char79_screen_dark_S918B_test_1.csv")
        df2_gg_t79_S = pd.read_csv("D:\\Users\\jussif.arnez\\Documents\\2021_IMS\\my_documents\\my_Research\\my_plotting\\Display_Power\\Reteste\\grafico editado\\Gidy S918B\\talk 79 char\\talk_char79_screen_dark_S918B_test_2.csv")
        df3_gg_t79_S = pd.read_csv("D:\\Users\\jussif.arnez\\Documents\\2021_IMS\\my_documents\\my_Research\\my_plotting\\Display_Power\\Reteste\\grafico editado\\Gidy S918B\\talk 79 char\\talk_char79_screen_dark_S918B_test_3.csv")

        #S918B t202
        df1_gg_t202_S = pd.read_csv("D:\\Users\\jussif.arnez\\Documents\\2021_IMS\\my_documents\\my_Research\\my_plotting\\Display_Power\\Reteste\\grafico editado\\Gidy S918B\\talk 202 char\\talk_char202_screen_dark_S918B_test_1.csv")
        df2_gg_t202_S = pd.read_csv("D:\\Users\\jussif.arnez\\Documents\\2021_IMS\\my_documents\\my_Research\\my_plotting\\Display_Power\\Reteste\\grafico editado\\Gidy S918B\\talk 202 char\\talk_char202_screen_dark_S918B_test_2.csv")
        df3_gg_t202_S = pd.read_csv("D:\\Users\\jussif.arnez\\Documents\\2021_IMS\\my_documents\\my_Research\\my_plotting\\Display_Power\\Reteste\\grafico editado\\Gidy S918B\\talk 202 char\\talk_char202_screen_dark_S918B_test_3.csv")

        data_gg={
        'A146M_input_char79': 
            [df1_gg_i79['Main Avg Current (mA)'].mean(), 
            df2_gg_i79['Main Avg Current (mA)'].mean(),
            df3_gg_i79['Main Avg Current (mA)'].mean()
            ],
        'A146M_input_char202': 
            [df1_gg_i202['Main Avg Current (mA)'].mean(), 
            df2_gg_i202['Main Avg Current (mA)'].mean(),
            df3_gg_i202['Main Avg Current (mA)'].mean()
            ],
        'A146M_swipe_char79': 
            [df1_gg_s79['Main Avg Current (mA)'].mean(), 
            df2_gg_s79['Main Avg Current (mA)'].mean(),
            df3_gg_s79['Main Avg Current (mA)'].mean()
            ],
        'A146M_swipe_char202': 
            [df1_gg_s202['Main Avg Current (mA)'].mean(), 
            df2_gg_s202['Main Avg Current (mA)'].mean(),
            df3_gg_s202['Main Avg Current (mA)'].mean()
            ],
        'A146M_talk_char79': 
            [df1_gg_t79['Main Avg Current (mA)'].mean(), 
            df2_gg_t79['Main Avg Current (mA)'].mean(),
            df3_gg_t79['Main Avg Current (mA)'].mean()
            ],
        'A146M_talk_char202': 
            [df1_gg_t202['Main Avg Current (mA)'].mean(), 
            df2_gg_t202['Main Avg Current (mA)'].mean(),
            df3_gg_t202['Main Avg Current (mA)'].mean()
            ],
        #s198b
        'S918B_input_char79': 
            [df1_gg_i79_S['Main Avg Current (mA)'].mean(), 
            df2_gg_i79_S['Main Avg Current (mA)'].mean(),
            df3_gg_i79_S['Main Avg Current (mA)'].mean()
            ],
        'S918B_input_char202': 
            [df1_gg_i202_S['Main Avg Current (mA)'].mean(), 
            df2_gg_i202_S['Main Avg Current (mA)'].mean(),
            df3_gg_i202_S['Main Avg Current (mA)'].mean()
            ],
        'S918B_swipe_char79': 
            [df1_gg_s79_S['Main Avg Current (mA)'].mean(), 
            df2_gg_s79_S['Main Avg Current (mA)'].mean(),
            df3_gg_s79_S['Main Avg Current (mA)'].mean()
            ],
        'S918B_swipe_char202': 
            [df1_gg_s202_S['Main Avg Current (mA)'].mean(), 
            df2_gg_s202_S['Main Avg Current (mA)'].mean(),
            df3_gg_s202_S['Main Avg Current (mA)'].mean()
            ],
        'S918B_talk_char79': 
            [df1_gg_t79_S['Main Avg Current (mA)'].mean(), 
            df2_gg_t79_S['Main Avg Current (mA)'].mean(),
            df3_gg_t79_S['Main Avg Current (mA)'].mean()
            ],
        'S918B_talk_char202': 
            [df1_gg_t202_S['Main Avg Current (mA)'].mean(), 
            df2_gg_t202_S['Main Avg Current (mA)'].mean(),
            df3_gg_t202_S['Main Avg Current (mA)'].mean()
            ]
        }

        self.gidy_energy = pd.DataFrame(data=data_gg, index=['t1','t2','t3'])

    def Plotting_Screen_Bar(self):
        fig_bar_comparison = go.Figure(
        layout_title_text="Comparison of Average Current Consumption For Different Screens",
        )

        fig_bar_comparison.add_bar(y=['Test 1', 'Test 2', 'Test 3'], 
                            x=self.df_a146m_mean_reshaped['a146m_light_white'], 
                            text=[round(val, 2) for val in self.df_a146m_mean_reshaped['a146m_light_white']],
                            name="PLS LCD for White Screen",
                            orientation="h",
                            textposition="inside", insidetextanchor="middle", textfont=dict(size=20),
                            marker=dict(line=dict(width=2), color='#ff33ff')
                        )

        fig_bar_comparison.add_bar(y=['Test 1', 'Test 2', 'Test 3'], 
                            x=self.df_a146m_mean_reshaped['a146m_light_black'], 
                            text=[round(val, 2) for val in self.df_a146m_mean_reshaped['a146m_light_black']],
                            name="PLS LCD for Black Screen",
                            orientation="h",
                            textposition="inside", insidetextanchor="middle", textfont=dict(size=20),
                            marker=dict(line=dict(width=2), color='#751aff')
                        )

        fig_bar_comparison.add_bar(y=['Test 1', 'Test 2', 'Test 3'], 
                            x=self.df_s9128b_mean_reshaped['s918b_dark_white'], 
                            text=[round(val, 2) for val in self.df_s9128b_mean_reshaped['s918b_dark_white']],
                            name="Dynamic Amoled for White Screen",
                            orientation="h",
                            textposition="inside", insidetextanchor="middle", textfont=dict(size=20),
                            marker=dict(line=dict(width=2), color='blue')
                        )

        fig_bar_comparison.add_bar(y=['Test 1', 'Test 2', 'Test 3'], 
                            x=self.df_s9128b_mean_reshaped['s918b_dark_black'], 
                            text=[round(val, 2) for val in self.df_s9128b_mean_reshaped['s918b_dark_black']],
                            name="Dynamic Amoled for Black Screen",
                            orientation="h",
                            textposition="inside", insidetextanchor="middle", textfont=dict(size=20),
                            marker=dict(line=dict(width=2), color='purple')
                        )

        fig_bar_comparison.update_layout(
                        title={'text': "", 'font': {'size': 1}},

                        xaxis_title={'text': "Average Current Consumption (mA)", 'font': {'size': self.my_figure['TAMANHO_LEG']}},
                        width=1500, height=800,
                        yaxis=dict(
                            tickfont=dict(size=self.my_figure['TAMANHO_TICK']),
                        ),
                        xaxis=dict(tickfont=dict(size=self.my_figure['TAMANHO_TICK']),
                                range=[0, 350]),
                        legend=dict(
                            font=dict(size=self.my_figure['TAMANHO_LEG']),
                            orientation='h',
                            yanchor='top',
                            y=1.20,
                            xanchor='center',
                            x=0.5
                        ),
                        plot_bgcolor='white',
                        shapes=[
                            dict(
                                type='rect',
                                xref='paper',
                                yref='paper',
                                x0=0,
                                y0=0,
                                x1=1.001,
                                y1=1.001,
                                line=dict(
                                    color='black',
                                    width=1,
                                )
                            )
                        ],
        )
        fig_bar_comparison.show(renderer="browser")
        #! to avoid the message appears on the pdf file.
        # pio.full_figure_for_development(fig_bar_comparison, warn=False)
        # fig_bar_comparison.write_image("lcd_amolead_screens.pdf", width= 1500 , height= 800, engine="kaleido")

    def Plotting_Text_Bar_Swipe(self):
        fig = go.Figure(
        layout_title_text="Consumption Battery Base",
        )
        # Available df columns names
        # ['A146M_input_char79', 'A146M_input_char202', 'A146M_swipe_char79', 'A146M_swipe_char202', 'A146M_talk_char79', 'A146M_talk_char202', 'S918B_input_char79', 'S918B_input_char202', 'S918B_swipe_char79', 'S918B_swipe_char202', 'S918B_talk_char79', 'S918B_talk_char202']
        # 
        flag_s918b = 'S918B_swipe_char202' #replace accordingly
        flag_a146m= 'A146M_swipe_char202'  #replace accordingly
        flag_title= 'Screen Swipe Tests (char 202)' #replace accordingly
        #user1 - Gidy
        fig.add_bar(y=['Test 1', 'Test 2', 'Test 3'], 
                    x=self.gidy_energy[flag_s918b], 
                    text=[round(val, 2) for val in self.gidy_energy[flag_s918b]],
                    name="AMOLED Display User 1",
                    orientation="h",
                    textposition="inside", insidetextanchor="middle", textfont=dict(size=20),
                    marker=dict(line=dict(width=2), color='blue'))
        fig.add_bar(y=['Test 1', 'Test 2', 'Test 3'], 
                    x=self.gidy_energy[flag_a146m], 
                    text=[round(val, 2) for val in self.gidy_energy[flag_a146m]],
                    name="LCD Display User 1",
                    orientation="h",
                    textposition='inside', insidetextanchor="middle", textfont=dict(size=20),
                    marker=dict(line=dict(width=2),  color='purple'))

        #user 2 - Jussif
        fig.add_bar(y=['Test 1', 'Test 2', 'Test 3'],
                    x=self.jussif_energy[flag_s918b], 
                    text=[round(val,2) for val in self.jussif_energy[flag_s918b]],
                    name="AMOLED Display User 2",
                    orientation="h",
                    textposition="inside", insidetextanchor="middle", textfont=dict(size=20),
                    marker=dict(line=dict(width=2), color='orange'))
        fig.add_bar(y=['Test 1', 'Test 2', 'Test 3'], 
                    x=self.jussif_energy[flag_a146m], 
                    text=[round(val,2) for val in self.jussif_energy[flag_a146m]],
                    name="LCD Display User 2",
                    orientation="h",
                    textposition='inside', insidetextanchor="middle", textfont=dict(size=20))

        fig.update_layout(
            title={'text': "", 'font': {'size': 1}},
            yaxis_title={'text': flag_title, 'font': {'size': self.my_figure['TAMANHO_LEG']}},

            xaxis_title={'text': "Average Current Consumption (mA)", 'font': {'size': self.my_figure['TAMANHO_LEG']}},
            width=1500, height=800,
            yaxis=dict(
                tickfont=dict(size=self.my_figure['TAMANHO_TICK']),
            ),
            xaxis=dict(tickfont=dict(size=self.my_figure['TAMANHO_TICK']),
                    range=[0, 480]),
            legend=dict(
                font=dict(size=self.my_figure['TAMANHO_LEG']),
                orientation='h',
                yanchor='top',
                y=1.08,
                xanchor='center',
                x=0.5
            ),
            plot_bgcolor='white',
            shapes=[
                dict(
                    type='rect',
                    xref='paper',
                    yref='paper',
                    x0=0,
                    y0=0,
                    x1=1.001,
                    y1=1.001,
                    line=dict(
                        color='black',
                        width=1,
                    )
                )
            ],
        )

        fig.show(renderer="browser")

        #! to avoid the message appears on the pdf file.
        # pio.full_figure_for_development(fig, warn=False)
        # fig.write_image("Swipe_char_79.pdf", width= 1500 , height= 800, engine="kaleido")

    def Plotting_Text_Bar_Type(self):
        fig = go.Figure(
        layout_title_text="Consumption Battery Base",
        )
        # Available df columns names
        # ['A146M_input_char79', 'A146M_input_char202', 'A146M_swipe_char79', 'A146M_swipe_char202', 'A146M_talk_char79', 'A146M_talk_char202', 'S918B_input_char79', 'S918B_input_char202', 'S918B_swipe_char79', 'S918B_swipe_char202', 'S918B_talk_char79', 'S918B_talk_char202']
        # 
        flag_s918b = 'S918B_input_char202' 
        flag_a146m= 'A146M_input_char202' 
        flag_title= 'Screen Type Tests (char 202)' 
        #user1 - Gidy
        fig.add_bar(y=['Test 1', 'Test 2', 'Test 3'], 
                    x=self.gidy_energy[flag_s918b], 
                    text=[round(val, 2) for val in self.gidy_energy[flag_s918b]],
                    name="AMOLED Display User 1",
                    orientation="h",
                    textposition="inside", insidetextanchor="middle", textfont=dict(size=20),
                    marker=dict(line=dict(width=2), color='blue'))
        fig.add_bar(y=['Test 1', 'Test 2', 'Test 3'], 
                    x=self.gidy_energy[flag_a146m], 
                    text=[round(val, 2) for val in self.gidy_energy[flag_a146m]],
                    name="LCD Display User 1",
                    orientation="h",
                    textposition='inside', insidetextanchor="middle", textfont=dict(size=20),
                    marker=dict(line=dict(width=2),  color='purple'))

        #user 2 - Jussif
        fig.add_bar(y=['Test 1', 'Test 2', 'Test 3'],
                    x=self.jussif_energy[flag_s918b], 
                    text=[round(val,2) for val in self.jussif_energy[flag_s918b]],
                    name="AMOLED Display User 2",
                    orientation="h",
                    textposition="inside", insidetextanchor="middle", textfont=dict(size=20),
                    marker=dict(line=dict(width=2), color='orange'))
        fig.add_bar(y=['Test 1', 'Test 2', 'Test 3'], 
                    x=self.jussif_energy[flag_a146m], 
                    text=[round(val,2) for val in self.jussif_energy[flag_a146m]],
                    name="LCD Display User 2",
                    orientation="h",
                    textposition='inside', insidetextanchor="middle", textfont=dict(size=20))

        fig.update_layout(
            title={'text': "", 'font': {'size': 1}},
            yaxis_title={'text': flag_title, 'font': {'size': self.my_figure['TAMANHO_LEG']}},

            xaxis_title={'text': "Average Current Consumption (mA)", 'font': {'size': self.my_figure['TAMANHO_LEG']}},
            width=1500, height=800,
            yaxis=dict(
                tickfont=dict(size=self.my_figure['TAMANHO_TICK']),
            ),
            xaxis=dict(tickfont=dict(size=self.my_figure['TAMANHO_TICK']),
                    range=[0, 480]),
            legend=dict(
                font=dict(size=self.my_figure['TAMANHO_LEG']),
                orientation='h',
                yanchor='top',
                y=1.08,
                xanchor='center',
                x=0.5
            ),
            plot_bgcolor='white',
            shapes=[
                dict(
                    type='rect',
                    xref='paper',
                    yref='paper',
                    x0=0,
                    y0=0,
                    x1=1.001,
                    y1=1.001,
                    line=dict(
                        color='black',
                        width=1,
                    )
                )
            ],
        )

        fig.show(renderer="browser")

    def Plotting_Text_Bar_Talk(self):
        fig = go.Figure(
        layout_title_text="Consumption Battery Base",
        )
        # Available df columns names
        # ['A146M_input_char79', 'A146M_input_char202', 'A146M_swipe_char79', 'A146M_swipe_char202', 'A146M_talk_char79', 'A146M_talk_char202', 'S918B_input_char79', 'S918B_input_char202', 'S918B_swipe_char79', 'S918B_swipe_char202', 'S918B_talk_char79', 'S918B_talk_char202']
        # 
        flag_s918b = 'S918B_talk_char202' 
        flag_a146m= 'A146M_talk_char202' 
        flag_title= 'Screen Talk Tests (char 202)' 
        #user1 - Gidy
        fig.add_bar(y=['Test 1', 'Test 2', 'Test 3'], 
                    x=self.gidy_energy[flag_s918b], 
                    text=[round(val, 2) for val in self.gidy_energy[flag_s918b]],
                    name="AMOLED Display User 1",
                    orientation="h",
                    textposition="inside", insidetextanchor="middle", textfont=dict(size=20),
                    marker=dict(line=dict(width=2), color='blue'))
        fig.add_bar(y=['Test 1', 'Test 2', 'Test 3'], 
                    x=self.gidy_energy[flag_a146m], 
                    text=[round(val, 2) for val in self.gidy_energy[flag_a146m]],
                    name="LCD Display User 1",
                    orientation="h",
                    textposition='inside', insidetextanchor="middle", textfont=dict(size=20),
                    marker=dict(line=dict(width=2),  color='purple'))

        #user 2 - Jussif
        fig.add_bar(y=['Test 1', 'Test 2', 'Test 3'],
                    x=self.jussif_energy[flag_s918b], 
                    text=[round(val,2) for val in self.jussif_energy[flag_s918b]],
                    name="AMOLED Display User 2",
                    orientation="h",
                    textposition="inside", insidetextanchor="middle", textfont=dict(size=20),
                    marker=dict(line=dict(width=2), color='orange'))
        fig.add_bar(y=['Test 1', 'Test 2', 'Test 3'], 
                    x=self.jussif_energy[flag_a146m], 
                    text=[round(val,2) for val in self.jussif_energy[flag_a146m]],
                    name="LCD Display User 2",
                    orientation="h",
                    textposition='inside', insidetextanchor="middle", textfont=dict(size=20))

        fig.update_layout(
            title={'text': "", 'font': {'size': 1}},
            yaxis_title={'text': flag_title, 'font': {'size': self.my_figure['TAMANHO_LEG']}},

            xaxis_title={'text': "Average Current Consumption (mA)", 'font': {'size': self.my_figure['TAMANHO_LEG']}},
            width=1500, height=800,
            yaxis=dict(
                tickfont=dict(size=self.my_figure['TAMANHO_TICK']),
            ),
            xaxis=dict(tickfont=dict(size=self.my_figure['TAMANHO_TICK']),
                    range=[0, 480]),
            legend=dict(
                font=dict(size=self.my_figure['TAMANHO_LEG']),
                orientation='h',
                yanchor='top',
                y=1.08,
                xanchor='center',
                x=0.5
            ),
            plot_bgcolor='white',
            shapes=[
                dict(
                    type='rect',
                    xref='paper',
                    yref='paper',
                    x0=0,
                    y0=0,
                    x1=1.001,
                    y1=1.001,
                    line=dict(
                        color='black',
                        width=1,
                    )
                )
            ],
        )

        fig.show(renderer="browser")
    
    def Error_Bar(self):
        df_jj_mean = self.jussif_energy.mean()
        df_jj_std = self.jussif_energy.std()

        df_gg_mean = self.gidy_energy.mean()
        df_gg_std = self.gidy_energy.std()

        df_jj_mean.index = ['LCD_Input_79', 'LCD_Input_202',
                                'LCD_Swipe_79','LCD_Swipe_202',
                                'LCD_Talk_79','LCD_Talk_202',
                                'AMOLED_Input_79', 'AMOLED_Input_202',
                                'AMOLED_Swipe_79','AMOLED_Swipe_202',
                                'AMOLED_Talk_79','AMOLED_Talk_202'
                                ]

        df_jj_std.index = ['LCD_Input_79', 'LCD_Input_202',
                    'LCD_Swipe_79','LCD_Swipe_202',
                    'LCD_Talk_79','LCD_Talk_202',
                    'AMOLED_Input_79', 'AMOLED_Input_202',
                    'AMOLED_Swipe_79','AMOLED_Swipe_202',
                    'AMOLED_Talk_79','AMOLED_Talk_202'
                    ]

        df_gg_mean.index = ['LCD_Input_79', 'LCD_Input_202',
                                'LCD_Swipe_79','LCD_Swipe_202',
                                'LCD_Talk_79','LCD_Talk_202',
                                'AMOLED_Input_79', 'AMOLED_Input_202',
                                'AMOLED_Swipe_79','AMOLED_Swipe_202',
                                'AMOLED_Talk_79','AMOLED_Talk_202'
                                ]

        df_gg_std.index = ['LCD_Input_79', 'LCD_Input_202',
                    'LCD_Swipe_79','LCD_Swipe_202',
                    'LCD_Talk_79','LCD_Talk_202',
                    'AMOLED_Input_79', 'AMOLED_Input_202',
                    'AMOLED_Swipe_79','AMOLED_Swipe_202',
                    'AMOLED_Talk_79','AMOLED_Talk_202'
                    ]

        #$ plotting
        colors= ['skyblue'] * 6 + ['#ff6699'] * 6
        #% Custom legend
        first_group = mpatches.Patch(color='skyblue', label='PLS LCD Display') 
        second_group = mpatches.Patch(color='#ff6699', label='Dynamic Amoled Display') 

        values = [df_jj_mean, df_gg_mean]

        for idx, val in enumerate(values):
            fig, ax = plt.subplots(figsize=(12,8))
            
            if idx == 0: 
                std= df_gg_std
            else: 
                std= df_jj_std

            bars = ax.bar(val.index, 
                    val, 
                    yerr=std,
                    capsize=5,  #controls the length of the little horizontal lines (caps) of the erros bars
                    color=colors)
            
            #* annotation
            for bar, std_val in zip(bars, std):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2, height + std_val + 0.2, f'STD: {std_val:.2f}',
                        ha='center', va='bottom', fontsize=8, color='black')

            for bar, mean in zip(bars, val):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2, height - 50, f'{mean:.2f}',
                        ha='center', va='bottom', fontsize=8, color='black')

            plt.xlabel('Scenarios', fontsize=self.my_figure['TAMANHO_FONTE']-10)
            plt.xticks(rotation=90, fontsize=self.my_figure['TAMANHO_FONTE']-10)
            plt.ylabel('Mean Value for User #' + str(idx+1) + ' (mA)', fontsize=self.my_figure['TAMANHO_FONTE']-10)
            plt.yticks(fontsize=self.my_figure['TAMANHO_FONTE']-10)
            plt.xticks(fontsize=self.my_figure['TAMANHO_FONTE']-10)
            plt.legend(handles=[first_group, second_group])
            # plt.savefig('erro_bar_' + str(idx+1) + '.pdf')


        #Power Consumption Difference
        plt.figure(figsize=(12, 8))

        mylabels = ["Input_79", "Input_202", "Swipe_79", "Swipe_202", "Talk_79", "Talk_202"]

        differences_gg = [((df_gg_mean[i] - df_gg_mean[i+6])/df_gg_mean[i])*100 for i in range(len(df_gg_mean)-6)]
        differences_jj = [((df_jj_mean[i] - df_jj_mean[i+6])/df_jj_mean[i])*100 for i in range(len(df_jj_mean)-6)]

        plt.vlines(x=mylabels, ymin=0, ymax=differences_gg, colors='black', linestyles='-', label='User#1')
        plt.scatter(mylabels, differences_gg, marker='o', c='black', label='User#1')

        plt.vlines(x=mylabels, ymin=0, ymax=differences_jj, colors='green', linestyles='--', label='User#2')
        plt.scatter(mylabels, differences_jj, marker='o', c='green', label='User#2')
        plt.ylabel(r'$\Delta$ Power Consumtion (%) for PLS LCD')

        ymin, ymax = 0, max(max(differences_gg), max(differences_jj))
        plt.xticks(fontsize=self.my_figure['TAMANHO_FONTE']-10)
        plt.yticks(np.arange(ymin, ymax + 2, 2 ),fontsize=self.my_figure['TAMANHO_FONTE']-10)
        plt.ylim(bottom=0)  # Set the lower limit of the y-axis to 0
        plt.tight_layout
        plt.legend()
        # plt.savefig("delta_consumption.pdf")

        # plt.show()
        #plt.savefig("erro_bar_jj.pdf")

        #Densities
        data_gg= np.array(differences_gg)
        data_jj= np.array(differences_jj)

        # plt.hist(data_gg, bins=20, density=True, alpha=0.4)
        plt.figure()

        kde_gg = gaussian_kde(data_gg)
        xs_gg = np.linspace(data_gg.min(), data_gg.max(), 200)
        ys_gg = kde_gg(xs_gg)

        plt.plot(xs_gg, ys_gg, linewidth=2, color='black', label='User 1')
        plt.fill_between(xs_gg, ys_gg, 0 , alpha = 0.3, color='black')


        kde_jj = gaussian_kde(data_jj)
        xs_jj = np.linspace(data_jj.min(), data_jj.max(), 200)
        ys_jj = kde_jj(xs_jj)

        plt.plot(xs_jj, ys_jj, linewidth=2, color='green', label='User 2')
        plt.fill_between(xs_jj, ys_jj, 0 , alpha = 0.3, color='green')

        ##############RED
        # Rectangle coordinates (adjust these to your desired position)
        x_rect = 24
        y_rect = 0.00
        width_rect = 8
        height_rect = 0.042

        # Create the rectangle
        rect = plt.Rectangle((x_rect, y_rect), width_rect, height_rect, linewidth=1.5, edgecolor='red', facecolor='none')
        plt.gca().add_patch(rect)

        # Define points for the left side (to color)
        # side_points = np.array([
        #     [x_rect, y_rect],
        #     [x_rect, y_rect + height_rect]
        # ])

        # Define points for the bottom side (to color)
        bottom_points = np.array([
            [x_rect, y_rect],
            [x_rect + width_rect, y_rect]
        ])


        path = Path(bottom_points)
        # Create a PathCollection to draw the colored side
        colored_side = PathCollection([path], facecolors='black', edgecolors='black', linewidths=0.5)
        plt.gca().add_collection(colored_side)

        # Add text
        space = 0.005  # Adjust this value to control the space
        plt.text(x_rect + space, y_rect + height_rect - space, "Most values", fontsize=14, ha='left', va='top', color='red')

        # Rectangle 2 coordinates (adjust these to your desired position)
        x_rect_2 = 28
        y_rect_2 = 0.00
        width_rect_2 = 1
        height_rect_2 = 0.096

        # Create the rectangle 2
        rect = plt.Rectangle((x_rect_2, y_rect_2), width_rect_2, height_rect_2, linewidth=1.5, edgecolor='red', linestyle='--', facecolor='none')
        plt.gca().add_patch(rect)

        # Define points for the bottom side (to color) rect 2
        bottom_points = np.array([
            [x_rect_2, y_rect_2],
            [x_rect_2 + width_rect_2, y_rect_2]
        ])


        path = Path(bottom_points)
        # Create a PathCollection to draw the colored side
        colored_side = PathCollection([path], facecolors='black', edgecolors='black', linewidths=0.5)
        plt.gca().add_collection(colored_side)

        # Add text
        # Adjust this value to control the space
        plt.text(x_rect_2 - 0.005, y_rect_2 + height_rect_2 + 0.002, "Peak 0.10", fontsize=14, ha='left', va='bottom', color='red')
        # Add a horizontal line at y = 0.5
        plt.axhline(y=0.096, xmin=plt.xlim()[0], xmax=28, color='red', linestyle='-', linewidth=5)


        ###############BLUE
        # Rectangle coordinates (adjust these to your desired position)
        x_rect_b = 32
        y_rect_b = 0.00
        width_rect_b = 3
        height_rect_b = height_rect_2

        # Create the rectangle 
        rect = plt.Rectangle((x_rect_b, y_rect_b), width_rect_b, height_rect_b, linewidth=1.5, edgecolor='blue', facecolor='none')
        plt.gca().add_patch(rect)


        # Define points for the bottom side (to color)
        bottom_points = np.array([
            [x_rect_b, y_rect_b],
            [x_rect_b + width_rect_b, y_rect_b]
        ])

        path = Path(bottom_points)
        # Create a PathCollection to draw the colored side
        colored_side = PathCollection([path], facecolors='black', edgecolors='black', linewidths=0.5)
        plt.gca().add_collection(colored_side)

        # Add text
        space = 0.005  # Adjust this value to control the space
        plt.text(x_rect_b + space, y_rect_b + height_rect_b - space, "Most values", fontsize=14, ha='left', va='top', color='blue')

        # Rectangle 2 coordinates (adjust these to your desired position)
        x_rect_b_2 = 33
        y_rect_b_2 = 0.00
        width_rect_b_2 = 1
        height_rect_b_2 = 0.128

        # Create the rectangle 2
        rect_b = plt.Rectangle((x_rect_b_2, y_rect_b_2), width_rect_b_2, height_rect_b_2, linewidth=1.5, edgecolor='blue', linestyle='--', facecolor='none')
        plt.gca().add_patch(rect_b)

        # Define points for the bottom side (to color) rect 2
        bottom_points = np.array([
            [x_rect_b_2, y_rect_b_2],
            [x_rect_b_2 + width_rect_b_2, y_rect_b_2]
        ])


        path = Path(bottom_points)
        # Create a PathCollection to draw the colored side
        colored_side = PathCollection([path], facecolors='black', edgecolors='black', linewidths=0.5)
        plt.gca().add_collection(colored_side)

        # Add text
        # Adjust this value to control the space
        plt.text(x_rect_b_2 - 0.005, y_rect_b_2 + height_rect_b_2 + 0.002, "Peak 0.13", fontsize=14, ha='left', va='bottom', color='blue')
        # Add a horizontal line at y = 0.5
        plt.axhline(y=0.096, xmin=plt.xlim()[0], xmax=28, color='blue', linestyle='-', linewidth=5)

        ############ Set axis limits
        plt.xlim(22, 32)
        plt.ylim(0, 0.05)

        # Add labels and title
        plt.xlabel(r'$\Delta$ Power Consumption (%)', fontsize=self.my_figure['TAMANHO_FONTE']-10)
        plt.xticks(np.arange(22, 35 + 2, 1 ), fontsize=self.my_figure['TAMANHO_FONTE']-10)

        plt.yticks(np.arange(0, 0.15 + 0.01, 0.01 ), fontsize=self.my_figure['TAMANHO_FONTE']-10)
        plt.ylabel('pdf', fontsize=self.my_figure['TAMANHO_FONTE']-10)
        plt.tight_layout()
        plt.legend()
        plt.show()
        # plt.savefig("pdf_users.pdf")


if __name__ == '__main__':
    my_display = Display_Consumption()
    my_display.Measurements_gg()
    my_display.Measurements_jj()
    my_display.Screens_a146m()
    my_display.Screens_s918b()
    my_display.Home_Screens()

    my_display.Plotting_Home() #Fig. 5
    my_display.Plotting_Screen_Bar() #Fig. 6
    my_display.Sleep_Mode() #Fig. 7
    my_display.Plotting_Text_Bar_Swipe() # Fig. 8, Fig. 11 (replace accordingly)
    my_display.Plotting_Text_Bar_Type() # Fig. 9, Fig. 10 (replace accordingly)
    my_display.Plotting_Text_Bar_Talk() # Fig. 12, Fig. 13 (replace accordingly)
    my_display.Error_Bar() #Fig. 14, Fig. 15, Fig. 16