import streamlit as st
import pandas as pd

# Backend service
import sideEffectsService


class render_tab1:
    def __init__(self):
        st.info("Browse and report for side effects of selected medicines")
  
    def selection(self):
        st.subheader("1. Selection of medicines:")
        # Call Backendservice
        callSideEffectsBackend = sideEffectsService.data4SideEffects()
        # Get list of medicines
        getListMedicines = callSideEffectsBackend.list_medicines()
        
        # Multiselect UI
        medicine_selection = st.multiselect('Select up to two medicines:',
                                            getListMedicines, key="medicines_selected")
        # Check number of meds
        check_nr_meds, nr_selected_meds = callSideEffectsBackend.max_nr_medicines(medicine_selection)

        if check_nr_meds == 200:
            combo = "False"
            if nr_selected_meds == 2:
                if st.checkbox('I want side effects of combination'):
                    combo = "True"

            return medicine_selection, combo, nr_selected_meds
            
        elif check_nr_meds == 422:
            st.warning("Please choose at least one medicine.")
            combo = None
            return medicine_selection, combo, nr_selected_meds

        elif check_nr_meds == 401:
            st.error("You chose more than two medicines. Please select only two medicines.")
            combo = None
            return medicine_selection, combo, nr_selected_meds
    

    def lookup_sideEffects(self, nr_selected_meds, selected_meds, combo):
        st.subheader("2. Reported side effects from selected medicines:")
        
        #if st.button(label="Lookup side effects", key='lookup'):
                    #if 'my_button' not in st.session_state:
                        #st.session_state.my_button = True
                    # Show dataframe
                    #displayed_side_effects = tab1_rendered.lookup_sideEffects(nr_selected_meds, selected_meds, combo)
        #if st.session_state.my_button == True:
        # No combination of meds
        if combo == "False":
            # Call Backendservice
            callSideEffectsBackend = sideEffectsService.data4SideEffects()
            
            # 2 chosen meds
            if nr_selected_meds == 2:
                listSideEffects_med1 = callSideEffectsBackend.get_listSideEffects(selected_meds[0])
                listSideEffects_med2 = callSideEffectsBackend.get_listSideEffects(selected_meds[1])
                
                # Create dataframes
                df1 = callSideEffectsBackend.create_DataFrame(selected_meds[0], listSideEffects_med1)
                df2 = callSideEffectsBackend.create_DataFrame(selected_meds[1], listSideEffects_med2)

                concat_dfs = pd.concat([df1, df2], ignore_index=False, axis=1)
                #st.subheader("Results from lookup")
                return st.dataframe(concat_dfs, use_container_width=True)
            
            # 1 chosen med
            elif nr_selected_meds == 1:
                listSideEffects_med1 = callSideEffectsBackend.get_listSideEffects(selected_meds[0])
                
                # Create dataframe
                df1 = callSideEffectsBackend.create_DataFrame(selected_meds[0], listSideEffects_med1)
                #st.subheader("Results from lookup")
                return st.dataframe(df1, use_container_width=True)
        
        # Combination of meds
        elif combo == "True":
            # Call Backendservice
            callSideEffectsBackend = sideEffectsService.data4SideEffects()
            listSideEffects = callSideEffectsBackend.get_listSideEffects_combo(selected_meds)

            if len(listSideEffects) == 0:
                st.error("For the selected combination of medicines are any side effects registered yet!")
            else:
                # Create dataframes
                df1 = callSideEffectsBackend.create_DataFrame_combo(selected_meds, listSideEffects)
                #st.subheader("Results from lookup")
                return st.dataframe(df1, use_container_width=True)
    
    
    def select_own_side_effects(self, combo, nr_selected_meds, selected_meds):
        """Render frontend for reporting side effects.

        Args:
            n: 
            type: 
        Returns:
            sum over n:
            type: 
        """
        st.subheader("3. Report own side effects from selected medicines:")
        st.write("Select side effects from the list")

        if combo == "False":
            # Call Backendservice
            callSideEffectsBackend = sideEffectsService.data4SideEffects()
     
            # 2 chosen meds
            if nr_selected_meds == 2:
                
                getListSideEffectsMono1 = callSideEffectsBackend.list_side_effects_mono(selected_meds[0])
                getListSideEffectsMono2 = callSideEffectsBackend.list_side_effects_mono(selected_meds[1])
                
                col1, col2 = st.columns(2)
                with col1:
                    # Multiselect UI
                    medicine1_side_effects = st.multiselect('Select side effects for ' + selected_meds[0],
                                                            getListSideEffectsMono1, key="medicine1_side_effects")
                with col2:
                    # Multiselect UI
                    medicine2_side_effects = st.multiselect('Select side effects for ' + selected_meds[1],
                                                            getListSideEffectsMono2, key="medicine2_side_effects")
                
                #if st.button(label="Report side effects"):
                    #report_side_effects_mono = callSideEffectsBackend.report_side_effects_mono(nr_selected_meds,
                                                                                               #selected_meds,
                                                                                               #medicine1_side_effects,
                                                                                               #medicine2_side_effects)
                
                return medicine1_side_effects, medicine2_side_effects
            
            # 1 chosen med
            elif nr_selected_meds == 1:
                getListSideEffectsMono = callSideEffectsBackend.list_side_effects_mono(selected_meds[0])
                
                medicine1_side_effects = st.multiselect('Select side effects for ' + selected_meds[0],
                                                            getListSideEffectsMono, key="medicine1_side_effects")
                
                medicine2_side_effects = None
                
                #if st.button(label="Report side effects"):
                    #report_side_effects_mono = callSideEffectsBackend.report_side_effects_mono(nr_selected_meds,
                                                                                               #selected_meds,
                                                                                               #medicine1_side_effects,
                                                                                               #medicine2_side_effects)

                return medicine1_side_effects, medicine2_side_effects
        
        # Combination of meds
        elif combo == "True":
            # Call Backendservice
            callSideEffectsBackend = sideEffectsService.data4SideEffects()
            
            # Get list of side effects from medicines taken
            # independently from each other
            getListSideEffectsCombo = callSideEffectsBackend.list_side_effects_combo(selected_meds)
            
            # Multi-select UI
            side_effects_combo = st.multiselect('Select side effects for the combination of '
                                                + selected_meds[0] +
                                                ' and ' + selected_meds[1],
                                                getListSideEffectsCombo, key="side_effects_combo")
            # Button
            #if st.button(label="Report side effects"):
                #report_side_effects_combo = callSideEffectsBackend.report_side_effects_combo(selected_meds,
            dummy_medicine2_side_effects = None                                                                              #side_effects_combo)
            return side_effects_combo, dummy_medicine2_side_effects
    
    
    def report_side_effects(self, combo, nr_selected_meds, selected_meds, medicine1_side_effects, medicine2_side_effects):
        """Render frontend for reporting side effects.

        Args:
            n: 
            type: 
        Returns:
            sum over n:
            type: 
        """
        #st.subheader("3. Report own side effects from selected medicines:")
        #st.write("Select side effects from the list")

        if combo == "False":
            # Call Backendservice
            callSideEffectsBackend = sideEffectsService.data4SideEffects()
            
            # Get list of side effects from medicines taken
            # independently from each other
            #getListSideEffectsMono = callSideEffectsBackend.list_side_effects_mono()
        
            # 2 chosen meds
            if nr_selected_meds == 2:
                report_side_effects_mono = callSideEffectsBackend.report_side_effects_mono(nr_selected_meds,
                                                                                           selected_meds,
                                                                                           medicine1_side_effects,
                                                                                           medicine2_side_effects)
                # Return 200
                return report_side_effects_mono
            
            # 1 chosen med
            elif nr_selected_meds == 1:
                #medicine1_side_effects = st.multiselect('Select side effects for ' + selected_meds[0],
                                                            #getListSideEffectsMono)
                
                #medicine2_side_effects = None
                
                
                report_side_effects_mono = callSideEffectsBackend.report_side_effects_mono(nr_selected_meds,
                                                                                           selected_meds,
                                                                                           medicine1_side_effects,
                                                                                           medicine2_side_effects)
                # Return 200
                return report_side_effects_mono
        
        # Combination of meds
        elif combo == "True":
            # Call Backendservice
            callSideEffectsBackend = sideEffectsService.data4SideEffects()
            
            # Get list of side effects from medicines taken
            # independently from each other
            #getListSideEffectsCombo = callSideEffectsBackend.list_side_effects_combo()
            
            # Multi-select UI
            #side_effects_combo = st.multiselect('Select side effects for the combination of '
                                                #+ selected_meds[0] +
                                                #' and ' + selected_meds[1],
                                                #getListSideEffectsCombo)
            # Button
            #if st.button(label="Report side effects"):
            report_side_effects_combo = callSideEffectsBackend.report_side_effects_combo(selected_meds,
                                                                                         medicine1_side_effects)
            # Return 200
            return report_side_effects_combo


if __name__ == "__main__":
    pass