import streamlit as st
import pandas as pd

# Backend service
import database

class data4Analysis:
    def __init__(self):
        pass

    def get_sideEffects(self, combo):
        """Get list of side effects from mono/combo medicines
        stored in database.

        Args:
            combo: "True" or "False"
            type: str 
        Returns:
            list_sideEffects: list of side effects name
            and id in the form ['<side effect name> (id)', '...', ...]
            type: list
        """

        # Open connection
        db = database.db_connection()
        db_connection, db_cur = db.connect_postgres()
       
        # combo
        if combo == "True":
            query = "select rcse.se_name_se_id from dbms.relookup_combo_se rcse;"
            db_cur.execute(query)
            list_sideEffects = []
            for sideEffect_i in db_cur:
                list_sideEffects.append(f"{sideEffect_i[0]}")
        
        # no combo
        else:
            query = "select distinct concat(individual_side_effect_name, ' (', individual_side_effect, ')') as se_name_se_id from dbms.medicine_mono order by se_name_se_id;"
            db_cur.execute(query)
            
            list_sideEffects = []
            for sideEffect_i in db_cur:
                list_sideEffects.append(f"{sideEffect_i[0]}")
        
        # Close connection
        db.disconnect_postgres(db_connection, db_cur)

        return list_sideEffects

    
    def norm_list_se(self, se_selected):
        """Normalise selected side effects to name w/o id.

        Args:
            se_selected: list of side effects name
            and id in the form ['<side effect name> (id)', '...', ...]
            type: 
        Returns:
            norm_se_selection_name: names of side effects w/o id
            type: list
            norm_se_selection_id: ids of side effects w/o name
            type: list
        """

        len_list = len(se_selected)
        norm_se_selection_name = []
        norm_se_selection_id = []
        for i in range(len_list):
            len_sel_se = len(se_selected[i])
            norm_se_selection_name.append(se_selected[i][:len_sel_se-11:])
            norm_se_selection_id.append(se_selected[i][-9:-1:])     

        return norm_se_selection_name, norm_se_selection_id


    def do_reverse_lookup(self, selected_sideEffects_name,
                          selected_sideEffects_id,
                          nr_sideEffects, combo):
        """Perform reverse lookup analysis for medicines.

        Based on selected side effects, we predict possible medicines
        you could have taken.
        Results provide the table with data for analysis, as well
        as specific values for the two best options of prediction.

        Args:
            selected_sideEffects_name: names of side effects w/o id
            type: list
            selected_sideEffects_id: ids of side effects w/o name
            type: list
            nr_sideEffects: nr. of selected side effects
            type: int
            combo: "True" or "False"
            type: str 
        Returns:
            concat_dfs: table for analysis
            type: dataframe
            total_nr_meds_found: nr. of meds with at least
            one matched side effect
            type: int
            med_high_p_name: Name of best predicted medicine 1
            type: str
            med_high_p_name2: Name of best predicted medicine 2,
            if combo="True". Otherwise None.
            type: str or None
            med_high_p_pct: Percentage of matched side effects
            compared to nr. of selected side effects for predicted medicine 1
            type: str
            med_high_p_prop: Probability predicted medicines compared to all
            other meds with at least one matched side effect
            type: str
            med_high_p_user: Percentage of reports by user for
            best predicted medicines
            type: str
            med_high_p_total: Percentage of matched side effects
            compared to total nr. of side effects for predicted medicine 1
            type: str
            med_high_p_name_2: Name of 2nd best predicted medicine 1
            type: str
            med_high_p_name2_2: Name of 2nd best predicted medicine 2,
            if combo="True". Otherwise None.
            type: str
            med_high_p_pct_2: Percentage of matched side effects
            compared to nr. of selected side effects for 2nd
            best predicted medicine 1
            type: str
            med_high_p_prop_2: Probability 2nd best predicted medicines compared to all
            other meds with at least one matched side effect
            type: str
            med_high_p_user_2: Percentage of reports by user for
            2nd best predicted medicines
            type: str
            med_high_p_total_2: Percentage of matched side effects
            compared to total nr. of side effects for 2nd best predicted medicines
            type: str
        """
        
        # Open db connection
        db = database.db_connection()
        db_connection, db_cur = db.connect_postgres()

        # single meds
        if combo == "False":
            if nr_sideEffects > 1:

                # Create input for execution
                sideEffects4query = "" 
                
                i = 0
                for sideEffect_i in range(nr_sideEffects):
                    if sideEffect_i == nr_sideEffects - 1:
                        sideEffects4query = sideEffects4query + "mm.individual_side_effect = " + "'" + selected_sideEffects_id[i] + "' "
                    elif sideEffect_i == 0:
                        sideEffects4query = sideEffects4query + "mm.individual_side_effect = '" + selected_sideEffects_id[i] + "' or "
                        i += 1
                    else:
                        sideEffects4query = sideEffects4query + " mm.individual_side_effect = " + "'" + selected_sideEffects_id[i] + "' or "
                        i += 1

                # query to get data for analysis
                query = "select left_table.med_name, left_table.nr_matched_se, left_table.per_matched_se, left_table.to_matched_se, left_table.to_per_matched_se, user_reports_mono.sum_user_reports_wo_per, user_reports_mono.sum_user_reports from (select cm.m0_commercial_name as med_name, cm.nr_matched_se as nr_matched_se, to_char((cm.nr_matched_se::float/" + str(nr_sideEffects) + ") * 100, 'fm900D00%') as per_matched_se, (cm.nr_matched_se::float/nr.to_nr_matched_se) as to_matched_se, to_char((cm.nr_matched_se::float/nr.to_nr_matched_se) * 100, '990D00%') as to_per_matched_se from (select m0.commercial_name as m0_commercial_name, count(*) as nr_matched_se from dbms.medicines m0, dbms.medicine_mono mm where m0.stitch = mm.stitch and (" + sideEffects4query + ") group by m0.commercial_name order by count(*) desc)cm, (select m1.commercial_name as m1_commercial_name, count(*) as to_nr_matched_se from dbms.medicines m1, dbms.medicine_mono mm where m1.stitch = mm.stitch group by m1.commercial_name)nr where cm.m0_commercial_name = nr.m1_commercial_name)left_table left join (select user_reports.med_name as med_name, (user_reports.nr_reported/sum_user_reports.sum_user) as sum_user_reports_wo_per, to_char((user_reports.nr_reported/sum_user_reports.sum_user)* 100, 'fm900D00%') as sum_user_reports from (select sum(user_reports.nr_reported) as sum_user from (select commerCIAL_NAME as med_name, count(*) as nr_reported from dbms.mono_side_effects_reported group by commerCIAL_NAME)user_reports)sum_user_reports, (select commerCIAL_NAME as med_name, count(*) as nr_reported from dbms.mono_side_effects_reported group by commerCIAL_NAME)user_reports)user_reports_mono on left_table.med_name = user_reports_mono.med_name order by left_table.nr_matched_se desc"

                
                db_cur.execute(query)

                query_result = db_cur.fetchall()

            
            elif nr_sideEffects == 1:
                
                # query to get data for analysis
                query = "select left_table.med_name, left_table.nr_matched_se, left_table.per_matched_se, left_table.to_matched_se, left_table.to_per_matched_se, user_reports_mono.sum_user_reports_wo_per, user_reports_mono.sum_user_reports from (select cm.m0_commercial_name as med_name, cm.nr_matched_se as nr_matched_se, to_char((cm.nr_matched_se::float/" + str(nr_sideEffects) + ") * 100, 'fm900D00%') as per_matched_se, (cm.nr_matched_se::float/nr.to_nr_matched_se) as to_matched_se, to_char((cm.nr_matched_se::float/nr.to_nr_matched_se) * 100, '990D00%') as to_per_matched_se from (select m0.commercial_name as m0_commercial_name, count(*) as nr_matched_se from dbms.medicines m0, dbms.medicine_mono mm where m0.stitch = mm.stitch and mm.individual_side_effect = '" + selected_sideEffects_id[0] + "' group by m0.commercial_name order by count(*) desc)cm, (select m1.commercial_name as m1_commercial_name, count(*) as to_nr_matched_se from dbms.medicines m1, dbms.medicine_mono mm where m1.stitch = mm.stitch group by m1.commercial_name)nr where cm.m0_commercial_name = nr.m1_commercial_name)left_table left join (select user_reports.med_name as med_name, (user_reports.nr_reported/sum_user_reports.sum_user) as sum_user_reports_wo_per, to_char((user_reports.nr_reported/sum_user_reports.sum_user)* 100, 'fm900D00%') as sum_user_reports from (select sum(user_reports.nr_reported) as sum_user from (select commerCIAL_NAME as med_name, count(*) as nr_reported from dbms.mono_side_effects_reported group by commerCIAL_NAME)user_reports)sum_user_reports, (select commerCIAL_NAME as med_name, count(*) as nr_reported from dbms.mono_side_effects_reported group by commerCIAL_NAME)user_reports)user_reports_mono on left_table.med_name = user_reports_mono.med_name order by left_table.nr_matched_se desc"
                

                db_cur.execute(query)

                query_result = db_cur.fetchall()

            # Process query results into lists
            commercial_name = []
            count = []
            percent_matched_sideEffects = []
            total_matched_sideEffects = []
            total_percent_matched_sideEffects = []
            p_user_reports_calc = []
            p_user_reports = []

            # Fill empty lists with data from query
            for row_i in query_result:
                commercial_name.append(f"{row_i[0]}")
                count.append(row_i[1])
                percent_matched_sideEffects.append(f"{row_i[2]}")
                total_matched_sideEffects.append(row_i[3])
                total_percent_matched_sideEffects.append(f"{row_i[4]}")
                p_user_reports_calc.append(f"{row_i[5]}")
                p_user_reports.append(f"{row_i[6]}")

            
            # Calculate probability compared to all meds with at
            # least one matched side effect
            sum_count = sum(count)
            nr_rows = len(count)
            p_med = []
            for i in range(nr_rows):
                p = count[i]/sum_count
                p_med.append("{0:0.2f}%".format(p * 100))

            
            ##### Algo for the most likely mono medicines... #####

            # Only one medicine with selected side effects found
            if len(count) < 2:
                med_high_p_name = commercial_name[0]
                med_high_p_name2 = None
                med_high_p_pct = percent_matched_sideEffects[0]
                med_high_p_prop = p_med[0]
                med_high_p_user = p_user_reports[0]
                med_high_p_total = total_percent_matched_sideEffects[0]

                # No second best medicine possible.
                med_high_p_name_2 = None
                med_high_p_name2_2 = None
                med_high_p_pct_2 = None
                med_high_p_prop_2 = None
                med_high_p_user_2 = None
                med_high_p_total_2 = None
            
            # First value is uniquely highest.
            elif count[0] > count[1]:
                med_high_p_name = commercial_name[0]
                med_high_p_name2 = None
                med_high_p_pct = percent_matched_sideEffects[0]
                med_high_p_prop = p_med[0]
                med_high_p_user = p_user_reports[0]
                med_high_p_total = total_percent_matched_sideEffects[0]

                # Find second best values.
                # Second best value is the second index.
                if count[1] > count[2]:
                    med_high_p_name_2 = commercial_name[1]
                    med_high_p_name2_2 = None
                    med_high_p_pct_2 = percent_matched_sideEffects[1]
                    med_high_p_prop_2 = p_med[1]
                    med_high_p_user_2 = p_user_reports[1]
                    med_high_p_total_2 = total_percent_matched_sideEffects[1]
                
                # At least third value is same as second value.
                elif count[1] == count[2]:
                    index = 1
                    for i in count[1:]:
                        # Find first value lower than max value.
                        if i < count[1]:
                            break
                        
                        # end of list reached = all values same
                        elif index == len(count)-1:
                            break
                        
                        index = index + 1

                    # user reports for second best value
                    max_user_reported_2 = float(0.00)
                    for i in p_user_reports_calc[1:index+1]:
                        if i != "None":
                            float_i = float(i)
                            if float_i > float(max_user_reported_2):
                                max_user_reported_2 = i

                    # No reporting value available for second best predicted
                    if max_user_reported_2 == float(0.00):
                        max_user_reported_2 = "Any reported yet"

                    # Highest reporting value available for second best predicted
                    if max_user_reported_2 != "Any reported yet":
                        
                        # Find index of highest reporting value
                        max_user_reported_index_2 = p_user_reports_calc[1:index+1].index(max_user_reported_2)
                        
                        # Define second best predicted medicine
                        med_high_p_name_2 = commercial_name[max_user_reported_index_2+1]
                        med_high_p_name2_2 = None
                        med_high_p_pct_2 = percent_matched_sideEffects[max_user_reported_index_2+1]
                        med_high_p_prop_2 = p_med[max_user_reported_index_2+1]
                        med_high_p_user_2 = p_user_reports[max_user_reported_index_2+1]
                        med_high_p_total_2 = total_percent_matched_sideEffects[max_user_reported_index_2+1]


                    # No reporting value available for second best predicted.
                    # Then for each possible medicine lookup highest value of matched
                    # side effects compared to total list of side effects of this medicine.
                    else:

                        max_p_total_calc_2 = max(total_matched_sideEffects[1:index+1])
                        
                        max_p_total_calc_index_2 = total_matched_sideEffects[1:index+1].index(max_p_total_calc_2)
                        max_p_total_2 = total_percent_matched_sideEffects[max_p_total_calc_index_2]
                        
                        med_high_p_name_2 = commercial_name[max_p_total_calc_index_2+1]
                        med_high_p_name2_2 = None
                        med_high_p_pct_2 = percent_matched_sideEffects[max_p_total_calc_index_2+1]
                        med_high_p_prop_2 = p_med[max_p_total_calc_index_2+1]
                        med_high_p_user_2 = p_user_reports[max_p_total_calc_index_2+1]
                        med_high_p_total_2 = total_percent_matched_sideEffects[max_p_total_calc_index_2+1]

            # First value = second value
            elif count[0] == count[1]:
                index = 0
                for i in count:
                    # find first value lower than max value
                    if i < count[0]:
                        break
                    
                    # end of list reached = all values same
                    elif index == len(count)-1:
                        break
                    
                    index = index + 1
                st.write(index)
                # Check if there is a max value for user reports for the best
                # predicted medicine.
                max_user_reported = float(0.00)
                sec_p_user_reports_calc = []
                for i in p_user_reports_calc[0:index]:
                    sec_p_user_reports_calc.append(i)
                    if i != "None":
                        float_i = float(i)
                        if float_i > float(max_user_reported):
                            max_user_reported = i

                
                # No value for user reports available for best value
                if max_user_reported == float(0.00):
                    max_user_reported = "Any reported yet"

                # There is a value for user reports available for best value
                if max_user_reported != "Any reported yet":
                    # Find index of max. value for user reports
                    max_user_reported_index = p_user_reports_calc[0:index].index(max_user_reported)

                    med_high_p_name = commercial_name[max_user_reported_index]
                    med_high_p_name2 = None
                    med_high_p_pct = percent_matched_sideEffects[max_user_reported_index]
                    med_high_p_prop = p_med[max_user_reported_index]
                    med_high_p_user = p_user_reports[max_user_reported_index]
                    med_high_p_total = total_percent_matched_sideEffects[max_user_reported_index]
                
                # No reporting value available for best predicted medicine.
                # Then for each possible medicine, lookup highest value of matched
                # side effects compared to total list of side effects of this medicine.
                else:
                    max_p_total_calc = max(total_matched_sideEffects[0:index])
                    
                    max_p_total_calc_index = total_matched_sideEffects[0:index].index(max_p_total_calc)
                    max_p_total = total_percent_matched_sideEffects[max_p_total_calc_index]
                    
                    med_high_p_name = commercial_name[max_p_total_calc_index]
                    med_high_p_name2 = None
                    med_high_p_pct = percent_matched_sideEffects[max_p_total_calc_index]
                    med_high_p_prop = p_med[max_p_total_calc_index]
                    med_high_p_user = p_user_reports[max_p_total_calc_index]
                    med_high_p_total = total_percent_matched_sideEffects[max_p_total_calc_index]


                # Start looking for second best predicted medicine.
                # Check if there is a value for user reports. If so,
                # then find a max value for user reports.
                max_user_reported_2 = float(0.00)
                if max_user_reported != "Any reported yet":
                    sec_index = sec_p_user_reports_calc.index(max_user_reported)
                    sec_p_user_reports_calc.pop(sec_index)
                    for i in sec_p_user_reports_calc:
                        if i != "None":
                            float_i = float(i)
                            if float_i > float(max_user_reported_2):
                                max_user_reported_2 = i

                
                # Second best value in reporting does not exist.
                if max_user_reported_2 == float(0.00):
                    max_user_reported_2 = "Any reported yet"
                
                # 1st and 2nd best value in reporting does exist
                if (max_user_reported != "Any reported yet") and (max_user_reported_2 != "Any reported yet"):
                    
                    max_user_reported_index_2 = sec_p_user_reports_calc.index(max_user_reported_2)
                    
                    if max_user_reported_index_2 < sec_index:
                        med_high_p_name_2 = commercial_name[max_user_reported_index_2]
                        med_high_p_name2_2 = None
                        med_high_p_pct_2 = percent_matched_sideEffects[max_user_reported_index_2]
                        med_high_p_prop_2 = p_med[max_user_reported_index_2]
                        med_high_p_user_2 = p_user_reports[max_user_reported_index_2]
                        med_high_p_total_2 = total_percent_matched_sideEffects[max_user_reported_index_2]
                    else:
                        med_high_p_name_2 = commercial_name[max_user_reported_index_2+1]
                        med_high_p_name2_2 = None
                        med_high_p_pct_2 = percent_matched_sideEffects[max_user_reported_index_2+1]
                        med_high_p_prop_2 = p_med[max_user_reported_index_2+1]
                        med_high_p_user_2 = p_user_reports[max_user_reported_index_2+1]
                        med_high_p_total_2 = total_percent_matched_sideEffects[max_user_reported_index_2+1]

                    # Both reporting values same
                    if med_high_p_user == med_high_p_user_2:
                    
                        if med_high_p_total < med_high_p_total_2:

                            med_high_p_name = commercial_name1[max_user_reported_index_2]
                            med_high_p_name2 = commercial_name2[max_user_reported_index_2]
                            med_high_p_pct = percent_matched_sideEffects[max_user_reported_index_2]
                            med_high_p_prop = p_med[max_user_reported_index_2]
                            med_high_p_user = p_user_reports[max_user_reported_index_2]
                            med_high_p_total = total_percent_matched_sideEffects[max_user_reported_index_2]

                            med_high_p_name_2 = commercial_name1[max_user_reported_index]
                            med_high_p_name2_2 = commercial_name2[max_user_reported_index]
                            med_high_p_pct_2 = percent_matched_sideEffects[max_user_reported_index]
                            med_high_p_prop_2 = p_med[max_user_reported_index]
                            med_high_p_user_2 = p_user_reports[max_user_reported_index]
                            med_high_p_total_2 = total_percent_matched_sideEffects[max_user_reported_index]

                
                # For best and 2nd best predicted medicines any user reports are available
                elif (max_user_reported == "Any reported yet") and (max_user_reported_2 == "Any reported yet"):
                    
                    # Copy list to later find 2nd best value 
                    sec_total_matched_sideEffects = total_matched_sideEffects.copy()
                    # value best value
                    max1_p_total_calc = max(sec_total_matched_sideEffects[0:index+1])
                    # index best value
                    max1_p_total_calc_index = sec_total_matched_sideEffects[0:index+1].index(max1_p_total_calc)
                    # delete best value
                    sec_total_matched_sideEffects.pop(max1_p_total_calc_index)
                    # find 2nd best value
                    max_p_total_calc_2 = max(sec_total_matched_sideEffects[0:index+1])

                    # find index of 2nd best value in original list
                    max_p_total_calc_index_2 = sec_total_matched_sideEffects[0:index].index(max_p_total_calc_2)

                    max_p_total_2 = total_percent_matched_sideEffects[max_p_total_calc_index_2+1]
                    
                    # Define 2nd best predicted medicine
                    if max_p_total_calc_index_2 < max1_p_total_calc_index:
                        med_high_p_name_2 = commercial_name[max_p_total_calc_index_2]
                        med_high_p_name2_2 = None
                        med_high_p_pct_2 = percent_matched_sideEffects[max_p_total_calc_index_2]
                        med_high_p_prop_2 = p_med[max_p_total_calc_index_2]
                        med_high_p_user_2 = p_user_reports[max_p_total_calc_index_2]
                        med_high_p_total_2 = total_percent_matched_sideEffects[max_p_total_calc_index_2]
                    else:
                        med_high_p_name_2 = commercial_name[max_p_total_calc_index_2+1]
                        med_high_p_name2_2 = None
                        med_high_p_pct_2 = percent_matched_sideEffects[max_p_total_calc_index_2+1]
                        med_high_p_prop_2 = p_med[max_p_total_calc_index_2+1]
                        med_high_p_user_2 = p_user_reports[max_p_total_calc_index_2+1]
                        med_high_p_total_2 = total_percent_matched_sideEffects[max_p_total_calc_index_2+1]

                # first best with reporting, second without reporting
                elif (max_user_reported != "Any reported yet") and (max_user_reported_2 == "Any reported yet"):
                    
                    # Copy list
                    sec_total_matched_sideEffects = total_matched_sideEffects.copy() 
                    # Delete value from best
                    sec_total_matched_sideEffects.pop(sec_index)
                    # find 2nd best value
                    max_p_total_calc_2 = max(sec_total_matched_sideEffects[0:index+1])

                    # find index 2nd best value in original list
                    max_p_total_calc_index_2 = sec_total_matched_sideEffects[0:index].index(max_p_total_calc_2)
                    max_p_total_2 = total_percent_matched_sideEffects[max_p_total_calc_index_2+1]
                    
                    # Define 2nd best predicted medicine
                    if max_p_total_calc_index_2 < sec_index:
                        med_high_p_name_2 = commercial_name[max_p_total_calc_index_2]
                        med_high_p_name2_2 = None
                        med_high_p_pct_2 = percent_matched_sideEffects[max_p_total_calc_index_2]
                        med_high_p_prop_2 = p_med[max_p_total_calc_index_2]
                        med_high_p_user_2 = p_user_reports[max_p_total_calc_index_2]
                        med_high_p_total_2 = total_percent_matched_sideEffects[max_p_total_calc_index_2]
                    else:
                        med_high_p_name_2 = commercial_name[max_p_total_calc_index_2+1]
                        med_high_p_name2_2 = None
                        med_high_p_pct_2 = percent_matched_sideEffects[max_p_total_calc_index_2+1]
                        med_high_p_prop_2 = p_med[max_p_total_calc_index_2+1]
                        med_high_p_user_2 = p_user_reports[max_p_total_calc_index_2+1]
                        med_high_p_total_2 = total_percent_matched_sideEffects[max_p_total_calc_index_2+1]


            # build dataframes
            df1_definition_names = {'Commercial Name': commercial_name}
            df1 = pd.DataFrame(data=df1_definition_names)
            df2_definition_names = {'Nr of side effects matched': count}
            df2 = pd.DataFrame(data=df2_definition_names)
            df3_definition_names = {'Nr. of side effects matched/ \n nr. selected side effects': percent_matched_sideEffects}
            df3 = pd.DataFrame(data=df3_definition_names)
            df4_definition_names = {'Nr. of side effects matched/ \n nr. reported side effects': total_percent_matched_sideEffects}
            df4 = pd.DataFrame(data=df4_definition_names)
            df5_definition_names = {'Probability of all meds with at least one matched side effect': p_med}
            df5 = pd.DataFrame(data=df5_definition_names)
            df6_definition_names = {'Probability of med based on user reports': p_user_reports}
            df6 = pd.DataFrame(data=df6_definition_names)

            concat_dfs = pd.concat([df1, df2, df3, df5, df6, df4], ignore_index=False, axis=1)


        # combo of medicines
        elif combo == "True":
            
            if nr_sideEffects > 1:
                # Create input for execution
                sideEffects4query = "" 
                    
                i = 0
                for sideEffect_i in range(nr_sideEffects):
                    if sideEffect_i == nr_sideEffects - 1:
                        sideEffects4query = sideEffects4query + "mc.polypharmacy_side_effect = " + "'" + selected_sideEffects_id[i] + "' "
                    elif sideEffect_i == 0:
                        sideEffects4query = sideEffects4query + "mc.polypharmacy_side_effect = '" + selected_sideEffects_id[i] + "' or "
                        i += 1
                    else:
                        sideEffects4query = sideEffects4query + " mc.polypharmacy_side_effect = " + "'" + selected_sideEffects_id[i] + "' or "
                        i += 1

                # query to get data for analysis when user selected
                # more than one side effect.
                query = "select left_table.med_name1, left_table.med_name2, left_table.nr_matched_se, left_table.per_matched_se, left_table.to_per_matched_se, left_table.to_matched_se, user_reports_combo.sum_user_reports_wo_per, user_reports_combo.sum_user_reports from (select cm.m0_commercial_name as med_name1, cm.m1_commercial_name as med_name2, cm.nr_matched_se as nr_matched_se, to_char((cm.nr_matched_se::float/" + str(nr_sideEffects) + ")*100, 'fm900D00%') as per_matched_se, to_char((cm.nr_matched_se::float/nr.to_nr_matched_se)*100, 'fm990D00%') as to_per_matched_se, (cm.nr_matched_se::float/nr.to_nr_matched_se) as to_matched_se from (select m0.commercial_name as m0_commercial_name, m1.commercial_name as m1_commercial_name, count(*) as nr_matched_se from dbms.medicines m0, dbms.medicines m1, dbms.medicines_combo mc where m0.stitch = mc.stitch1 and m1.stitch = mc.stitch2 and (" + sideEffects4query + ") group by m0.commercial_name, m1.commercial_name order by count(*) desc)cm, (select m0.commercial_name as m0_commercial_name, m1.commercial_name as m1_commercial_name, count(*) as to_nr_matched_se from dbms.medicines m0, dbms.medicines m1, dbms.medicines_combo mc where m0.stitch = mc.stitch1 and m1.stitch = mc.stitch2 group by m0.commercial_name, m1.commercial_name)nr where cm.m0_commercial_name = nr.m0_commercial_name and cm.m1_commercial_name = nr.m1_commercial_name)left_table left join (select user_reports2.med_name1 as med_name1, user_reports2.med_name2 as med_name2, (user_reports2.nr_reported/sum_user_reports.sum_user) as sum_user_reports_wo_per, to_char((user_reports2.nr_reported/sum_user_reports.sum_user)* 100, 'fm900D00%') as sum_user_reports from (select sum(user_reports.nr_reported) as sum_user from (select commercial_name1 as med_name1, commercial_name2 as med_name2, count(*) as nr_reported from dbms.combo_side_effects_reported group by med_name1, med_name2)user_reports)sum_user_reports, (select commercial_name1 as med_name1, commercial_name2 as med_name2, count(*) as nr_reported from dbms.combo_side_effects_reported group by med_name1, med_name2)user_reports2)user_reports_combo on left_table.med_name1 = user_reports_combo.med_name1 and left_table.med_name2 = user_reports_combo.med_name2 order by left_table.nr_matched_se desc"

                db_cur.execute(query)

                query_result = db_cur.fetchall()


            elif nr_sideEffects == 1:
                
                # query to get data for analysis when user selected
                # one side effect.
                query = "select left_table.med_name1, left_table.med_name2, left_table.nr_matched_se, left_table.per_matched_se, left_table.to_per_matched_se, left_table.to_matched_se, user_reports_combo.sum_user_reports_wo_per, user_reports_combo.sum_user_reports from (select cm.m0_commercial_name as med_name1, cm.m1_commercial_name as med_name2, cm.nr_matched_se as nr_matched_se, to_char((cm.nr_matched_se::float/" + str(nr_sideEffects) + ")*100, 'fm900D00%') as per_matched_se, to_char((cm.nr_matched_se::float/nr.to_nr_matched_se)*100, 'fm990D00%') as to_per_matched_se, (cm.nr_matched_se::float/nr.to_nr_matched_se) as to_matched_se from (select m0.commercial_name as m0_commercial_name, m1.commercial_name as m1_commercial_name, count(*) as nr_matched_se from dbms.medicines m0, dbms.medicines m1, dbms.medicines_combo mc where m0.stitch = mc.stitch1 and m1.stitch = mc.stitch2 and mc.polypharmacy_side_effect = '" + selected_sideEffects_id[0] + "' group by m0.commercial_name, m1.commercial_name order by count(*) desc)cm, (select m0.commercial_name as m0_commercial_name, m1.commercial_name as m1_commercial_name, count(*) as to_nr_matched_se from dbms.medicines m0, dbms.medicines m1, dbms.medicines_combo mc where m0.stitch = mc.stitch1 and m1.stitch = mc.stitch2 group by m0.commercial_name, m1.commercial_name)nr where cm.m0_commercial_name = nr.m0_commercial_name and cm.m1_commercial_name = nr.m1_commercial_name)left_table left join (select user_reports2.med_name1 as med_name1, user_reports2.med_name2 as med_name2, (user_reports2.nr_reported/sum_user_reports.sum_user) as sum_user_reports_wo_per, to_char((user_reports2.nr_reported/sum_user_reports.sum_user)* 100, 'fm900D00%') as sum_user_reports from (select sum(user_reports.nr_reported) as sum_user from (select commercial_name1 as med_name1, commercial_name2 as med_name2, count(*) as nr_reported from dbms.combo_side_effects_reported group by med_name1, med_name2)user_reports)sum_user_reports, (select commercial_name1 as med_name1, commercial_name2 as med_name2, count(*) as nr_reported from dbms.combo_side_effects_reported group by med_name1, med_name2)user_reports2)user_reports_combo on left_table.med_name1 = user_reports_combo.med_name1 and left_table.med_name2 = user_reports_combo.med_name2 order by left_table.nr_matched_se desc"
                
                db_cur.execute(query)

                query_result = db_cur.fetchall()

            # Processing query results into lists
            commercial_name1 = []
            commercial_name2 = []
            count = []
            percent_matched_sideEffects = []
            total_percent_matched_sideEffects = []
            total_matched_sideEffects = []
            p_user_reports_calc = []
            p_user_reports = []
                
            for row_i in query_result:
                commercial_name1.append(f"{row_i[0]}")
                commercial_name2.append(f"{row_i[1]}")
                count.append(row_i[2])
                percent_matched_sideEffects.append(f"{row_i[3]}")
                total_percent_matched_sideEffects.append(f"{row_i[4]}")
                total_matched_sideEffects.append(row_i[5])
                p_user_reports_calc.append(f"{row_i[6]}")
                p_user_reports.append(f"{row_i[7]}")

            
            # Calculate probability compared to all meds with at
            # least one matched side effect
            sum_count = sum(count)
            nr_rows = len(count)
            p_med = []
            for i in range(nr_rows):
                p = count[i]/sum_count
                p_med.append("{0:0.2f}%".format(p * 100))


            ##### Algo for the most likely medicines in combination... #####

            # Only one medicine with selected side effects identified
            if len(count) < 2:
                med_high_p_name = commercial_name1[0]
                med_high_p_name2 = commercial_name2[0]
                med_high_p_pct = percent_matched_sideEffects[0]
                med_high_p_prop = p_med[0]
                med_high_p_user = p_user_reports[0]
                med_high_p_total = total_percent_matched_sideEffects[0]

                # No 2nd best predicted medicine possible
                med_high_p_name_2 = None
                med_high_p_name2_2 = None
                med_high_p_pct_2 = None
                med_high_p_prop_2 = None
                med_high_p_user_2 = None
                med_high_p_total_2 = None
            
            # First value is uniquely highest
            elif count[0] > count[1]:
                med_high_p_name = commercial_name1[0]
                med_high_p_name2 = commercial_name2[0]
                med_high_p_pct = percent_matched_sideEffects[0]
                med_high_p_prop = p_med[0]
                med_high_p_user = p_user_reports[0]
                med_high_p_total = total_percent_matched_sideEffects[0]

                ## start finding second best values ##
                
                # second best value is the second index
                if count[1] > count[2]:
                    med_high_p_name_2 = commercial_name1[1]
                    med_high_p_name2_2 = commercial_name2[1]
                    med_high_p_pct_2 = percent_matched_sideEffects[1]
                    med_high_p_prop_2 = p_med[1]
                    med_high_p_user_2 = p_user_reports[1]
                    med_high_p_total_2 = total_percent_matched_sideEffects[1]
                
                # at least third value is same as second value
                elif count[1] == count[2]:
                    index = 1
                    for i in count[1:]:
                        # find first value lower than max value
                        if i < count[1]:
                            break
                        
                        # end of list reached = all values same
                        elif index == len(count)-1:
                            break
                        
                        index = index + 1

                    # check if there is a value available for user reports
                    max_user_reported_2 = float(0.00)
                    for i in p_user_reports_calc[1:index+1]:
                        if i != "None":
                            float_i = float(i)
                            if float_i > float(max_user_reported_2):
                                max_user_reported_2 = i

                    # no value for user reports available
                    if max_user_reported_2 == float(0.00):
                        max_user_reported_2 = "Any reported yet"

                    # there is a max value available for 2nd best predicted medicine.
                    if max_user_reported_2 != "Any reported yet":
                        
                        max_user_reported_index_2 = p_user_reports_calc[1:index+1].index(max_user_reported_2)

                        med_high_p_name_2 = commercial_name[max_user_reported_index_2+1]
                        med_high_p_name2_2 = None
                        med_high_p_pct_2 = percent_matched_sideEffects[max_user_reported_index_2+1]
                        med_high_p_prop_2 = p_med[max_user_reported_index_2+1]
                        med_high_p_user_2 = p_user_reports[max_user_reported_index_2+1]
                        med_high_p_total_2 = total_percent_matched_sideEffects[max_user_reported_index_2+1]
                    
                    
                    # no value for user reports available.
                    # Then lookup highest value of matched side effects
                    # compared to total list of side effects from specific medicine.
                    else:

                        max_p_total_calc_2 = max(total_matched_sideEffects[1:index+1])
                        max_p_total_calc_index_2 = total_matched_sideEffects[1:index+1].index(max_p_total_calc_2)
                        max_p_total_2 = total_percent_matched_sideEffects[max_p_total_calc_index_2]
                        
                        # Define second best predicted medicine.
                        med_high_p_name_2 = commercial_name1[max_p_total_calc_index_2+1]
                        med_high_p_name2_2 = commercial_name2[max_p_total_calc_index_2+1]
                        med_high_p_pct_2 = percent_matched_sideEffects[max_p_total_calc_index_2+1]
                        med_high_p_prop_2 = p_med[max_p_total_calc_index_2+1]
                        med_high_p_user_2 = p_user_reports[max_p_total_calc_index_2+1]
                        med_high_p_total_2 = total_percent_matched_sideEffects[max_p_total_calc_index_2+1]

            # first value = second value
            elif count[0] == count[1]:
                index = 0
                for i in count:
                    # find first value lower than max value
                    if i < count[0]:
                        break
                    
                    # end of list reached = all values same
                    elif index == len(count)-1:
                        break
                    
                    index = index + 1

                # check if there is a best value for user reports
                max_user_reported = float(0.00)
                sec_p_user_reports_calc = []
                for i in p_user_reports_calc[0:index]:
                    sec_p_user_reports_calc.append(i)
                    if i != "None":
                        float_i = float(i)
                        if float_i > float(max_user_reported):
                            max_user_reported = i

                
                # no best value for user reports available
                if max_user_reported == float(0.00):
                    max_user_reported = "Any reported yet"

                # best value for user reports available
                if max_user_reported != "Any reported yet":
                    max_user_reported_index = p_user_reports_calc[0:index].index(max_user_reported)

                     # Define best predicted medicine.
                    med_high_p_name = commercial_name1[max_user_reported_index]
                    med_high_p_name2 = commercial_name2[max_user_reported_index]
                    med_high_p_pct = percent_matched_sideEffects[max_user_reported_index]
                    med_high_p_prop = p_med[max_user_reported_index]
                    med_high_p_user = p_user_reports[max_user_reported_index]
                    med_high_p_total = total_percent_matched_sideEffects[max_user_reported_index]
                
                # no value for user reports available.
                # Then lookup highest value of matched side effects
                # compared to total list of side effects from specific medicine.
                else:
                    max_p_total_calc = max(total_matched_sideEffects[0:index])
                    max_p_total_calc_index = total_matched_sideEffects[0:index].index(max_p_total_calc)
                    max_p_total = total_percent_matched_sideEffects[max_p_total_calc_index]
                    
                    # Define best predicted medicine.
                    med_high_p_name = commercial_name1[max_p_total_calc_index]
                    med_high_p_name2 = commercial_name2[max_p_total_calc_index]
                    med_high_p_pct = percent_matched_sideEffects[max_p_total_calc_index]
                    med_high_p_prop = p_med[max_p_total_calc_index]
                    med_high_p_user = p_user_reports[max_p_total_calc_index]
                    med_high_p_total = total_percent_matched_sideEffects[max_p_total_calc_index]


                # find second best predicted medicine
                
                # check if there is max value for user reports
                max_user_reported_2 = float(0.00)
                if max_user_reported != "Any reported yet":
                    sec_index = sec_p_user_reports_calc.index(max_user_reported)
                    sec_p_user_reports_calc.pop(sec_index)
                    for i in sec_p_user_reports_calc:
                        if i != "None":
                            float_i = float(i)
                            if float_i > max_user_reported_2:
                                max_user_reported_2 = i

                # no value for user reporting available
                if max_user_reported_2 == float(0.00):
                    max_user_reported_2 = "Any reported yet"

                # first and second best value in reporting does exist
                if (max_user_reported != "Any reported yet") and (max_user_reported_2 != "Any reported yet"):

                    max_user_reported_index_2 = sec_p_user_reports_calc.index(max_user_reported_2)
                    
                    # Define 2nd best predicted medicine.
                    if max_user_reported_index_2 < sec_index:
                        med_high_p_name_2 = commercial_name1[max_user_reported_index_2]
                        med_high_p_name2_2 = commercial_name2[max_user_reported_index_2]
                        med_high_p_pct_2 = percent_matched_sideEffects[max_user_reported_index_2]
                        med_high_p_prop_2 = p_med[max_user_reported_index_2]
                        med_high_p_user_2 = p_user_reports[max_user_reported_index_2]
                        med_high_p_total_2 = total_percent_matched_sideEffects[max_user_reported_index_2]
                    else:
                        med_high_p_name_2 = commercial_name1[max_user_reported_index_2+1]
                        med_high_p_name2_2 = commercial_name2[max_user_reported_index_2+1]
                        med_high_p_pct_2 = percent_matched_sideEffects[max_user_reported_index_2+1]
                        med_high_p_prop_2 = p_med[max_user_reported_index_2+1]
                        med_high_p_user_2 = p_user_reports[max_user_reported_index_2+1]
                        med_high_p_total_2 = total_percent_matched_sideEffects[max_user_reported_index_2+1]
                
                    # both reporting values same
                    if med_high_p_user == med_high_p_user_2:
                        # then the best predicted medicine is the one with highest
                        # med_high_p_total. 
                        if med_high_p_total < med_high_p_total_2:

                            med_high_p_name = commercial_name1[max_user_reported_index_2]
                            med_high_p_name2 = commercial_name2[max_user_reported_index_2]
                            med_high_p_pct = percent_matched_sideEffects[max_user_reported_index_2]
                            med_high_p_prop = p_med[max_user_reported_index_2]
                            med_high_p_user = p_user_reports[max_user_reported_index_2]
                            med_high_p_total = total_percent_matched_sideEffects[max_user_reported_index_2]

                            med_high_p_name_2 = commercial_name1[max_user_reported_index]
                            med_high_p_name2_2 = commercial_name2[max_user_reported_index]
                            med_high_p_pct_2 = percent_matched_sideEffects[max_user_reported_index]
                            med_high_p_prop_2 = p_med[max_user_reported_index]
                            med_high_p_user_2 = p_user_reports[max_user_reported_index]
                            med_high_p_total_2 = total_percent_matched_sideEffects[max_user_reported_index]
                
                # First and second best value without reporting values
                elif (max_user_reported == "Any reported yet") and (max_user_reported_2 == "Any reported yet"):

                    sec_total_matched_sideEffects = total_matched_sideEffects.copy()
                    # value best value
                    max1_p_total_calc = max(sec_total_matched_sideEffects[0:index])
                    # index best value
                    max1_p_total_calc_index = sec_total_matched_sideEffects[0:index].index(max1_p_total_calc)
                    # delete best value
                    sec_total_matched_sideEffects.pop(max1_p_total_calc_index)
                    # find 2nd best value
                    max_p_total_calc_2 = max(sec_total_matched_sideEffects[0:index])
                    # find index 2nd best value in original list
                    max_p_total_calc_index_2 = sec_total_matched_sideEffects[0:index].index(max_p_total_calc_2)
                    max_p_total_2 = total_percent_matched_sideEffects[max_p_total_calc_index_2+1]
                    
                    # Define 2nd best predicted medicine.
                    if max_p_total_calc_index_2 < max1_p_total_calc_index:
                        med_high_p_name_2 = commercial_name1[max_p_total_calc_index_2]
                        med_high_p_name2_2 = commercial_name2[max_p_total_calc_index_2]
                        med_high_p_pct_2 = percent_matched_sideEffects[max_p_total_calc_index_2]
                        med_high_p_prop_2 = p_med[max_p_total_calc_index_2]
                        med_high_p_user_2 = p_user_reports[max_p_total_calc_index_2]
                        med_high_p_total_2 = total_percent_matched_sideEffects[max_p_total_calc_index_2]
                    else:
                        med_high_p_name_2 = commercial_name1[max_p_total_calc_index_2+1]
                        med_high_p_name2_2 = commercial_name2[max_p_total_calc_index_2+1]
                        med_high_p_pct_2 = percent_matched_sideEffects[max_p_total_calc_index_2+1]
                        med_high_p_prop_2 = p_med[max_p_total_calc_index_2+1]
                        med_high_p_user_2 = p_user_reports[max_p_total_calc_index_2+1]
                        med_high_p_total_2 = total_percent_matched_sideEffects[max_p_total_calc_index_2+1]

                # First best value with reporting, second without
                elif (max_user_reported != "Any reported yet") and (max_user_reported_2 == "Any reported yet"):
                    
                    sec_total_matched_sideEffects = total_matched_sideEffects.copy()
                    sec_total_matched_sideEffects.pop(sec_index)
                    # find 2nd best value
                    max_p_total_calc_2 = max(sec_total_matched_sideEffects[0:index])
                    # find index 2nd best value in original list
                    max_p_total_calc_index_2 = sec_total_matched_sideEffects[0:index].index(max_p_total_calc_2)
                    max_p_total_2 = total_percent_matched_sideEffects[max_p_total_calc_index_2+1]
                    
                    # Define 2nd best predicted medicine.
                    if max_p_total_calc_index_2 < sec_index:
                        med_high_p_name_2 = commercial_name1[max_p_total_calc_index_2]
                        med_high_p_name2_2 = commercial_name2[max_p_total_calc_index_2]
                        med_high_p_pct_2 = percent_matched_sideEffects[max_p_total_calc_index_2]
                        med_high_p_prop_2 = p_med[max_p_total_calc_index_2]
                        med_high_p_user_2 = p_user_reports[max_p_total_calc_index_2]
                        med_high_p_total_2 = total_percent_matched_sideEffects[max_p_total_calc_index_2]
                    else:
                        med_high_p_name_2 = commercial_name1[max_p_total_calc_index_2+1]
                        med_high_p_name2_2 = commercial_name2[max_p_total_calc_index_2+1]
                        med_high_p_pct_2 = percent_matched_sideEffects[max_p_total_calc_index_2+1]
                        med_high_p_prop_2 = p_med[max_p_total_calc_index_2+1]
                        med_high_p_user_2 = p_user_reports[max_p_total_calc_index_2+1]
                        med_high_p_total_2 = total_percent_matched_sideEffects[max_p_total_calc_index_2+1]


            # build dataframes
            df1_definition_names = {'Commercial Name Medicine 1': commercial_name1}
            df1 = pd.DataFrame(data=df1_definition_names)
            df2_definition_names = {'Commercial Name Medicine 2': commercial_name2}
            df2 = pd.DataFrame(data=df2_definition_names)
            df3_definition_names = {'Number of side effects matched': count}
            df3 = pd.DataFrame(data=df3_definition_names)
            df4_definition_names = {'Nr. of side effects matched/\nnr. selected side effects': percent_matched_sideEffects}
            df4 = pd.DataFrame(data=df4_definition_names)
            df5_definition_names = {'Nr. of side effects matched/\nnr. reported side effects': total_percent_matched_sideEffects}
            df5 = pd.DataFrame(data=df5_definition_names)
            df6_definition_names = {'Probability of all meds with at least one matched side effect': p_med}
            df6 = pd.DataFrame(data=df6_definition_names)
            df7_definition_names = {'Probability of med based on user reports': p_user_reports}
            df7 = pd.DataFrame(data=df7_definition_names)

            concat_dfs = pd.concat([df1, df2, df3, df4, df6, df7, df5], ignore_index=False, axis=1)


        total_nr_meds_found = len(count)

        db.disconnect_postgres(db_connection, db_cur)

        return concat_dfs, total_nr_meds_found, med_high_p_name, med_high_p_name2, med_high_p_pct, med_high_p_prop, med_high_p_user, med_high_p_total, med_high_p_name_2, med_high_p_name2_2, med_high_p_pct_2, med_high_p_prop_2, med_high_p_user_2, med_high_p_total_2
        

    def lookup_avg_ratio_se_meds(self):
        """Create value for KPI1:
        
        Nr. meds with at least one matched side effect.

        Args:
            commercial_name: list of medicines found in query
            type: list
        Returns:
            kpi1: number of medicines with >=1 matched side effects
            type: int
        """

        # Open db connection
        db = database.db_connection()
        db_connection, db_cur = db.connect_postgres()

        query = "select to_char((avg(full_table.ratio_common_se))*100, 'fm900D00%') as avg_ratio_common_se from (select gene_sideeffects.gene1 as gene, gene_sideeffects.se as side_effect, gene_sideeffects.nr_shared_se as nr_common_se, shared_meds.nr_shared_meds as nr_shared_meds, gene_sideeffects.nr_shared_se::float/shared_meds.nr_shared_meds as ratio_common_se, to_char((gene_sideeffects.nr_shared_se::float/shared_meds.nr_shared_meds)*100, 'fm900D00%') as per_ratio_common_se from (select mp1.gene as gene1, mm.individual_side_effect as se, count(*) as nr_shared_se from dbms.medicine_protein mp1, dbms.medicine_mono mm where mp1.stitch = mm.stitch group by mp1.gene, mm.individual_side_effect)gene_sideeffects, (select mp.gene as gene2, count(*) as nr_shared_meds from dbms.medicine_protein mp group by gene)shared_meds where gene_sideeffects.gene1 = shared_meds.gene2 and shared_meds.nr_shared_meds > 1)full_table"
        
        db_cur.execute(query)
        query_result = db_cur.fetchall()

        avg_ratio_se_meds = []

        for row_i in query_result:
            avg_ratio_se_meds.append(f"{row_i[0]}")
        
        if avg_ratio_se_meds[0] == "100.00%":
            result = "True"
        else:
            result = "False"
        
        db.disconnect_postgres(db_connection, db_cur)
        
        return avg_ratio_se_meds[0], result

    
    def lookup_protein_se_meds(self):
        """Create value for KPI1:
        
        Nr. meds with at least one matched side effect.

        Args:
            commercial_name: list of medicines found in query
            type: list
        Returns:
            kpi1: number of medicines with >=1 matched side effects
            type: int
        """

        # Open db connection
        db = database.db_connection()
        db_connection, db_cur = db.connect_postgres()
        #st.write("Hello")
        query = "select gene_sideeffects.gene1 as gene, gene_sideeffects.se as side_effect, gene_sideeffects.nr_shared_se as nr_common_se, shared_meds.nr_shared_meds as nr_shared_meds, to_char((gene_sideeffects.nr_shared_se::float/shared_meds.nr_shared_meds)*100, 'fm900D00%') as per_ratio_common_se from (select mp1.gene as gene1, mm.individual_side_effect as se, count(*) as nr_shared_se from dbms.medicine_protein mp1, dbms.medicine_mono mm where mp1.stitch = mm.stitch group by mp1.gene, mm.individual_side_effect)gene_sideeffects, (select mp.gene as gene2, count(*) as nr_shared_meds from dbms.medicine_protein mp group by gene)shared_meds where gene_sideeffects.gene1 = shared_meds.gene2 and shared_meds.nr_shared_meds > 1 limit 100"
        
        db_cur.execute(query)
        query_result = db_cur.fetchall()
        #st.write(query_result)
        gene = []
        side_effect = []
        nr_common_se = []
        nr_shared_meds = []
        per_ratio_common_se = []

        for row_i in query_result:
            gene.append(int(f"{row_i[0]}"))
            side_effect.append(f"{row_i[1]}")
            nr_common_se.append(int(f"{row_i[2]}"))
            nr_shared_meds.append(int(f"{row_i[3]}"))
            per_ratio_common_se.append(f"{row_i[4]}")

        # dataframes
        df1_definition_names = {'Protein': gene}
        df1 = pd.DataFrame(data=df1_definition_names)
        df2_definition_names = {'Side effect from med.': side_effect}
        df2 = pd.DataFrame(data=df2_definition_names)
        df3_definition_names = {'Occurence side effect in each protein': nr_common_se}
        df3 = pd.DataFrame(data=df3_definition_names)
        df4_definition_names = {'Nr. of meds sharing this protein': nr_shared_meds}
        df4 = pd.DataFrame(data=df4_definition_names)
        df5_definition_names = {'Ratio on how common the side effect is': per_ratio_common_se}
        df5 = pd.DataFrame(data=df5_definition_names)

        concat_dfs = pd.concat([df1, df2, df3, df4, df5], ignore_index=False, axis=1)
        
        db.disconnect_postgres(db_connection, db_cur)
        

        return concat_dfs


if __name__ == "__main__":
    pass