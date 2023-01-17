import streamlit as st
import pandas as pd

# Backend service
import sideEffectsService
import userService


class render_tab1:
    def __init__(self):
        info = """
                Browse and report for side effects of selected medicines:
                1. Select up to two medicines from the list.
                2. Choose whether you combine selected medicines.
                3. Browse side effect symptoms registered in the database.
                4. Select your own side effect symptoms from the list.
                5. Send your side effects for our analysis.
               """
        st.info(info)
        st.markdown("<br>", unsafe_allow_html=True)

    def selection(self):
        st.subheader("1. Selection of medicines:")
        # Call Backendservice
        callSideEffectsBackend = sideEffectsService.data4SideEffects()
        # Get list of medicines
        getListMedicines = callSideEffectsBackend.list_medicines()
        if 'getListMedicines' not in st.session_state:
            st.session_state.getListMedicines = getListMedicines

        # Multiselect UI
        medicine_selection = st.multiselect('Select up to two medicines:',
                                            getListMedicines, key="medicines_selected")
        
        # Check number of meds
        check_nr_meds, nr_selected_meds = callSideEffectsBackend.max_nr_medicines(medicine_selection)

        # normalise list of selected medicines
        medicine_selection = callSideEffectsBackend.norm_list_meds(medicine_selection)

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
        """Get user data from service provider (SP)

        Args:
            n: 
            type: 
        Returns:
            sum over n:
            type: 
        """
        
        st.subheader("2. Reported side effects from selected medicines:")
        
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
                
                return medicine1_side_effects, medicine2_side_effects
            
            # 1 chosen med
            elif nr_selected_meds == 1:
                getListSideEffectsMono = callSideEffectsBackend.list_side_effects_mono(selected_meds[0])
                
                medicine1_side_effects = st.multiselect('Select side effects for ' + selected_meds[0],
                                                            getListSideEffectsMono, key="medicine1_side_effects")
                
                medicine2_side_effects = None

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

            medicine2_side_effects = None
            return side_effects_combo, medicine2_side_effects 
    
    
    def report_side_effects(self, combo, nr_selected_meds,
                            selected_meds, medicine1_side_effects,
                            medicine2_side_effects, userID):
        """Render frontend for reporting side effects.

        Args:
            n: 
            type: 
        Returns:
            sum over n:
            type: 
        """

        if combo == "False":
            # Call Backendservice
            callSideEffectsBackend = sideEffectsService.data4SideEffects()
        
            # 2 chosen meds
            if nr_selected_meds == 2:
                report_side_effects_mono = callSideEffectsBackend.report_side_effects_mono(nr_selected_meds,
                                                                                           selected_meds,
                                                                                           medicine1_side_effects,
                                                                                           medicine2_side_effects, userID)

                # Return 200
                return report_side_effects_mono
            
            # 1 chosen med
            elif nr_selected_meds == 1:
             
                report_side_effects_mono = callSideEffectsBackend.report_side_effects_mono(nr_selected_meds,
                                                                                           selected_meds,
                                                                                           medicine1_side_effects,
                                                                                           medicine2_side_effects, userID)
                # Return 200
                return report_side_effects_mono
        
        # Combination of meds
        elif combo == "True":
            # Call Backendservice
            callSideEffectsBackend = sideEffectsService.data4SideEffects()

            report_side_effects_combo = callSideEffectsBackend.report_side_effects_combo(selected_meds,
                                                                                         medicine1_side_effects, userID)
            # Return 200
            return report_side_effects_combo

    def process_reporting(self, session_sate):
        """Render frontend for processing the reported side effects.

        Args:
            n: 
            type: 
        Returns:
            sum over n:
            type: 
        """

        for key in session_sate:
            del st.session_state[key]
                    
        st.success("Thank you! Your provided side effects have been successfully reported. You will be automatically forwarded back to the selection of medicines...")

        n = 150000000
        while n >= 0:
            n = n-1
            
        return st.experimental_rerun()

if __name__ == "__main__":
    pass