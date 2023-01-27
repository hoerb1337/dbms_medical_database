###### Production Version 1.0 main #####

# External libraries
import streamlit as st
import webbrowser

# Frontend modules
import sideEffects
import analysis
import user
import protein

# Backend sevices
import userService

class Frontend:
    
    def __init__(self):
        
        ## Layout an Design ##
        st.set_page_config(page_title="Medical Database",
                           layout="wide")

        # Style definition of web app
        css_style = """
                        <style>
                        #MainMenu {
                            visibility: hidden;
                        }
                        .footer {
                            visibility: visibility;
                            position: fixed;
                            left: 0;
                            bottom: 0;
                            width: 100%;
                            background-color: red;
                            z-index: 99999999999999999999999999999999999999999999999999999;
                        }
                        .subheader {
                            color: grey;
                            font-size: 18px;
                        }
                        .info_box {
                            background-color: #f2f3f4;
                            margin-top: 5px;
                            margin-bottom: 30px;
                            padding-left: 20px;
                            padding-top: 20px;
                            padding-right: 20px;
                            padding-bottom: 15px;
                            border-radius: 5px;
                        }
                        .tooltip {
                            position: relative;
                            display: inline-block;
                        }

                        .tooltip .tooltiptext {
                            visibility: hidden;
                            width: 300px;
                            background-color: #555;
                            color: #fff;
                            text-align: justify;
                            border-radius: 6px;
                            padding-left: 10px;
                            padding-top: 10px;
                            padding-right: 10px;
                            padding-bottom: 10px;
                            position: absolute;
                            z-index: 1;
                            bottom: 120%;
                            left: 10%;
                            margin-left: 0px;
                            opacity: 0;
                            transition: opacity 0.3s;
                        }

                        .tooltip .tooltiptext::after {
                            content: "";
                            position: absolute;
                            top: 100%;
                            right: 40%;
                            margin-left: -30px;
                            border-width: 5px;
                            border-style: solid;
                            border-color: #555 transparent transparent transparent;
                        }

                        .tooltip:hover .tooltiptext {
                            visibility: visible;
                            opacity: 1;
                            }
                        
                        .expander {
                                margin-top: 10px;
                                margin-bottom: 20px;
                                padding-left: 20px;
                                padding-top: 10px;
                                padding-right: 20px;
                                padding-bottom: 10px;
                                        
                        }
                        .result_box_negative {
                            margin-top: 20px;
                            margin-bottom: 30px;
                            padding-left: 20px;
                            padding-top: 20px;
                            padding-right: 20px;
                            padding-bottom: 15px;
                            border-radius: 5px;
                            border-style: solid;
                            border-color: #fa8072;
                            border-width: 2px;
                        }
                        .result_box_positive {
                            margin-top: 20px;
                            margin-bottom: 30px;
                            padding-left: 20px;
                            padding-top: 20px;
                            padding-right: 20px;
                            padding-bottom: 15px;
                            border-radius: 5px;
                            border-style: solid;
                            border-color: #ace1af;
                            border-width: 2px;
                        }
                        </style>
                    """
        st.markdown(css_style, unsafe_allow_html=True)
       
        header = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        .subheader {color: grey; font-size: 18px;}
        </style>
        <h1>Welcome to the Medical Database</h1>
        <div class="subheader">Our data is based on the <i>"Molecular network and polypharmacy data"</i>.
        The data mainly provides information on medicines and their side effects.</div>
        <br>
        """
        st.markdown(header, unsafe_allow_html=True)

        # User management:
        userAuthenticated = user.UserUI()
        
        # Check if user logged-in is already in database.
        # If not, register the user in database. Get user data
        # to save their access history.
        userData = userAuthenticated.authenticate()
        if userData == "Error":
            webbrowser.open('https://medbase.dashboardauth.com/home', new=0, autoraise=True)

        # Navigation bar
        tab1, tab2, tab3, tab4 = st.tabs(["Lookup and Report Side Effects", 
                                    "Reverse Lookup Analysis",
                                    "Shared Protein Analysis",
                                    "Your Usage Data"])
        #
        
        # Tab1: sideEffects
        with tab1:
            tab1_rendered = sideEffects.render_tab1()
            
            # Return list of selected medicines
            selected_meds, combo, nr_selected_meds = tab1_rendered.selection()
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Start search for side effects
            if combo != None:
                
                # Show dataframe/side effects
                tab1_rendered.lookup_sideEffects(nr_selected_meds,
                                                selected_meds, combo)
            
            st.markdown("<br>", unsafe_allow_html=True)        
            
            # Reporting side effects:
            if nr_selected_meds >=1 and nr_selected_meds <=2:
                # list of selected own side effects/multi select UI 
                medicine1_side_effects, medicine2_side_effects = tab1_rendered.select_own_side_effects(combo,
                                                                                                       nr_selected_meds,
                                                                                                       selected_meds)
                if len(medicine1_side_effects) > 0:
                # Reporting Button
                    if st.button(label="Report side effects", key="reporting"):
                        # Post own side effects to database
                        tab1_rendered.report_side_effects(combo, nr_selected_meds,
                                                        selected_meds, medicine1_side_effects,
                                                        medicine2_side_effects, userData["id"])
                        
                        # Store usage data from user in database
                        store_usage_date = userService.UsageData()
                        store_usage_date.post_usage_data_se(userData["id"], selected_meds, combo,
                                                            medicine1_side_effects, medicine2_side_effects)
                        
                        # Process reporting in frontend
                        session_sate = st.session_state.keys()
                        tab1_rendered.process_reporting(session_sate)
        # End of tab1

        # Tab2: reverse lookup analysis
        with tab2:
            tab2_rendered = analysis.render_tab2()

            # 1. Selection side effects
            selected_sideEffects_name,selected_sideEffects_id, nr_sideEffects, combo, selected_sideEffects = tab2_rendered.show_selection_sideEffects()
            # 2. perform reverse lookup and display results
            predicted_med = tab2_rendered.show_reverse_lookup(selected_sideEffects_name,
                                              selected_sideEffects_id,
                                              nr_sideEffects, combo)    
            #st.write(predicted_med)
            # Store usage data from user in database
            if predicted_med != None:
                store_usage_data = userService.UsageData()
                store_usage_data.post_usage_data_reLookup(userData["id"], selected_sideEffects, 
                                                        predicted_med, combo)
        # End of tab2

        # Tab3: shared protein analysis
        with tab3:
            tab3_rendered = protein.render_tab3()
            analysis_executed = tab3_rendered.show_protein_analysis()
            if analysis_executed != None:
                store_usage_data = userService.UsageData()
                analysis_executed = "Execute Analysis"
                store_usage_data.post_usage_data_protein(userData["id"], analysis_executed)
            
            st.markdown("<br>", unsafe_allow_html=True) 
            
            analysis_details_executed = tab3_rendered.show_protein_analysis_details()

            if analysis_details_executed != None:
                store_usage_data = userService.UsageData()
                analysis_details_executed = "Execute Query"
                store_usage_data.post_usage_data_protein(userData["id"], analysis_details_executed)
        # End of tab3

        # Tab4: usage data
        with tab4:
            tab4_rendered = user.render_tab4(userData["id"])
            tab4_rendered.show_accessHistory_tab1(userData["id"])
            tab4_rendered.show_accessHistory_tab2(userData["id"])
            tab4_rendered.show_accessHistory_tab3(userData["id"])
        # End of tab4

        footer = """<div class="footer">
                    <p>Medical Database</p>
                    </div>"""
        st.markdown(footer, unsafe_allow_html=True) 

if __name__ == "__main__":
    rendered_frondend = Frontend()
    