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
            combo: "True" or "Fals"
            type: str 
        Returns:
            list_sideEffects: list of side effects
            type: list
        """

        # Open connection
        db = database.db_connection()
        db_connection, db_cur = db.connect_postgres()
        # combo
        if combo == "True":
            query = "select distinct concat(combo_side_effect_name, ' (', polypharmacy_side_effect, ')') as se_name_se_id from dbms.medicines_combo order by se_name_se_id;"

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
        close_db_connection = db.disconnect_postgres(db_connection, db_cur)

        return list_sideEffects

    
    def norm_list_se(self, se_selected):
        """Normalise selected side effects to name w/o id.

        Args:
            n: 
            type: 
        Returns:
            sum over n:
            type: 
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
        """Perform reverse lookup analysis.

        Args:
            selected_sideEffects_name:
            type: list
            nr_sideEffects:
            type: int
        Returns:
            concat_dfs: table of all values
            type: dataframe
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

                # query: calcualte nr of matched side effects per medicine
                query = "select left_table.med_name, left_table.nr_matched_se, left_table.per_matched_se, left_table.to_per_matched_se, user_reports_mono.sum_user_reports from (select cm.m0_commercial_name as med_name, cm.nr_matched_se as nr_matched_se, to_char((cm.nr_matched_se::float/" + str(nr_sideEffects) + ") * 100, 'fm900D00%') as per_matched_se, to_char((cm.nr_matched_se::float/nr.to_nr_matched_se) * 100, '990D00%') as to_per_matched_se from (select m0.commercial_name as m0_commercial_name, count(*) as nr_matched_se from dbms.medicines m0, dbms.medicine_mono mm where m0.stitch = mm.stitch and (" + sideEffects4query + ") group by m0.commercial_name order by count(*) desc)cm, (select m1.commercial_name as m1_commercial_name, count(*) as to_nr_matched_se from dbms.medicines m1, dbms.medicine_mono mm where m1.stitch = mm.stitch group by m1.commercial_name)nr where cm.m0_commercial_name = nr.m1_commercial_name)left_table left join (select user_reports.med_name as med_name, to_char((user_reports.nr_reported/sum_user_reports.sum_user)* 100, 'fm900D00%') as sum_user_reports from (select sum(user_reports.nr_reported) as sum_user from (select commerCIAL_NAME as med_name, count(*) as nr_reported from dbms.mono_side_effects_reported group by commerCIAL_NAME)user_reports)sum_user_reports, (select commerCIAL_NAME as med_name, count(*) as nr_reported from dbms.mono_side_effects_reported group by commerCIAL_NAME)user_reports)user_reports_mono on left_table.med_name = user_reports_mono.med_name order by left_table.nr_matched_se desc"
                #query = "select cm.m0_commercial_name, cm.nr_matched_se, to_char((cm.nr_matched_se::float/" + str(nr_sideEffects) + ")*100, 'fm900D00%')as per_matched_se, to_char((cm.nr_matched_se::float/nr.to_nr_matched_se)*100, 'fm990D00%') as to_per_matched_se from (select m0.commercial_name as m0_commercial_name, count(*) as nr_matched_se from dbms.medicines m0,dbms.medicine_mono mm where m0.stitch = mm.stitch and (" + sideEffects4query + ") group by m0.commercial_name order by count(*) desc)cm, (select m1.commercial_name as m1_commercial_name, count(*) as to_nr_matched_se from dbms.medicines m1, dbms.medicine_mono mm where m1.stitch = mm.stitch group by m1.commercial_name)nr where cm.m0_commercial_name = nr.m1_commercial_name order by cm.nr_matched_se desc"
                
                db_cur.execute(query)

                query_result = db_cur.fetchall()

                #commercial_name = []
                #count = []
                #percent_matched_sideEffects = []
                #total_percent_matched_sideEffects = []
                #p_user_reports = []

                # Fill empty lists with data from query
                #for row_i in query_result:
                    #commercial_name.append(f"{row_i[0]}")
                    #count.append(int(f"{row_i[1]}"))
                    #percent_matched_sideEffects.append(f"{row_i[2]}")
                    #total_percent_matched_sideEffects.append(f"{row_i[3]}")
                    #p_user_reports.append(f"{row_i[4]}")

                # Probability compared to all meds with at
                # least one matched side effect
                #sum_count = sum(count)
                #nr_rows = len(count)
                #p_med = []
                #for i in range(nr_rows):
                    #p = count[i]/sum_count
                    #p_med.append("{0:0.2f}%".format(p * 100))

                # dataframes
                #df1_definition_names = {'Commercial Name': commercial_name}
                #df1 = pd.DataFrame(data=df1_definition_names)
                #df2_definition_names = {'Nr of side effects matched': count}
                #df2 = pd.DataFrame(data=df2_definition_names)
                #df3_definition_names = {'Nr. of side effects matched/ \n nr. selected side effects': percent_matched_sideEffects}
                #df3 = pd.DataFrame(data=df3_definition_names)
                #df4_definition_names = {'Nr. of side effects matched/ \n nr. reported side effects': total_percent_matched_sideEffects}
                #df4 = pd.DataFrame(data=df4_definition_names)
                #df5_definition_names = {'Probability of all meds with at least one matched side effect': p_med}
                #df5 = pd.DataFrame(data=df5_definition_names)
                #df6_definition_names = {'Probability of med based on user reports': p_user_reports}
                #df6 = pd.DataFrame(data=df6_definition_names)

                #concat_dfs = pd.concat([df1, df2, df3, df5, df6, df4], ignore_index=False, axis=1)
                
                #return concat_dfs, commercial_name, count, percent_matched_sideEffects, total_percent_matched_sideEffects, p_user_reports

            elif nr_sideEffects == 1:
                query = "select left_table.med_name, left_table.nr_matched_se, left_table.per_matched_se, left_table.to_per_matched_se, user_reports_mono.sum_user_reports from (select cm.m0_commercial_name as med_name, cm.nr_matched_se as nr_matched_se, to_char((cm.nr_matched_se::float/" + str(nr_sideEffects) + ") * 100, 'fm900D00%') as per_matched_se, to_char((cm.nr_matched_se::float/nr.to_nr_matched_se) * 100, '990D00%') as to_per_matched_se from (select m0.commercial_name as m0_commercial_name, count(*) as nr_matched_se from dbms.medicines m0, dbms.medicine_mono mm where m0.stitch = mm.stitch and mm.individual_side_effect = '" + selected_sideEffects_id[0] + "' group by m0.commercial_name order by count(*) desc)cm, (select m1.commercial_name as m1_commercial_name, count(*) as to_nr_matched_se from dbms.medicines m1, dbms.medicine_mono mm where m1.stitch = mm.stitch group by m1.commercial_name)nr where cm.m0_commercial_name = nr.m1_commercial_name)left_table left join (select user_reports.med_name as med_name, to_char((user_reports.nr_reported/sum_user_reports.sum_user)* 100, 'fm900D00%') as sum_user_reports from (select sum(user_reports.nr_reported) as sum_user from (select commerCIAL_NAME as med_name, count(*) as nr_reported from dbms.mono_side_effects_reported group by commerCIAL_NAME)user_reports)sum_user_reports, (select commerCIAL_NAME as med_name, count(*) as nr_reported from dbms.mono_side_effects_reported group by commerCIAL_NAME)user_reports)user_reports_mono on left_table.med_name = user_reports_mono.med_name order by left_table.nr_matched_se desc"
                
                #query = "select cm.m0_commercial_name, cm.nr_matched_se, to_char((cm.nr_matched_se::float/" + str(nr_sideEffects) + ")*100, 'fm900D00%') as per_matched_se, to_char((cm.nr_matched_se::float/nr.to_nr_matched_se)*100, 'fm990D00%') as to_per_matched_se from (select m0.commercial_name as m0_commercial_name, count(*) as nr_matched_se from dbms.medicines m0, dbms.medicine_mono mm where m0.stitch = mm.stitch and mm.individual_side_effect = '" + selected_sideEffects_id[0] + "' group by m0.commercial_name order by count(*) desc)cm, (select m1.commercial_name as m1_commercial_name, count(*) as to_nr_matched_se from dbms.medicines m1, dbms.medicine_mono mm where m1.stitch = mm.stitch group by m1.commercial_name)nr where cm.m0_commercial_name = nr.m1_commercial_name order by cm.nr_matched_se desc;"

                db_cur.execute(query)

                #db_cur.execute("""select m0.commercial_name, count(*) from dbms.medicines m0, dbms.medicine_mono mm where m0.stitch = mm.stitch and mm.individual_side_effect = %(side_effect)s group by m0.commercial_name order by count(*) desc;""", {'side_effect': selected_sideEffects_id[0]})

                query_result = db_cur.fetchall()

                #commercial_name = []
                #count = []
                #percent_matched_sideEffects = []
                #total_percent_matched_sideEffects = []
                #p_user_reports = []
                #for row_i in query_result:
                    #commercial_name.append(f"{row_i[0]}")
                    #count.append(int(f"{row_i[1]}"))
                    #percent_matched_sideEffects.append(f"{row_i[2]}")
                    #total_percent_matched_sideEffects.append(f"{row_i[3]}")
                    #p_user_reports.append(f"{row_i[4]}")

                # Probability compared to all meds with at
                # least one matched side effect
                #sum_count = sum(count)
                #nr_rows = len(count)
                #p_med = []
                #for i in range(nr_rows):
                    #p = count[i]/sum_count
                    #p_percentage = ("{0:0.2f}%".format(p * 100))
                    #p_med.append("{0:0.2f}%".format(p * 100))

                # dataframes
                #df1_definition_names = {'Commercial Name': commercial_name}
                #df1 = pd.DataFrame(data=df1_definition_names)
                #df2_definition_names = {'Number of side effects matched': count}
                #df2 = pd.DataFrame(data=df2_definition_names)
                #df3_definition_names = {'Nr. of side effects matched/\nnr. selected side effects': percent_matched_sideEffects}
                #df3 = pd.DataFrame(data=df3_definition_names)
                #df4_definition_names = {'Nr. of side effects matched/\nnr. reported side effects': total_percent_matched_sideEffects}
                #df4 = pd.DataFrame(data=df4_definition_names)
                #df5_definition_names = {'Probability of all meds with at least one matched side effect': p_med}
                #df5 = pd.DataFrame(data=df5_definition_names)
                #df6_definition_names = {'Probability of med based on user reports': p_user_reports}
                #df6 = pd.DataFrame(data=df6_definition_names)

                #concat_dfs = pd.concat([df1, df2, df3, df5, df6, df4], ignore_index=False, axis=1)

                #return concat_dfs, commercial_name, count, percent_matched_sideEffects, total_percent_matched_sideEffects, p_user_reports

            commercial_name = []
            count = []
            percent_matched_sideEffects = []
            total_percent_matched_sideEffects = []
            p_user_reports = []

            # Fill empty lists with data from query
            for row_i in query_result:
                commercial_name.append(f"{row_i[0]}")
                count.append(int(f"{row_i[1]}"))
                percent_matched_sideEffects.append(f"{row_i[2]}")
                total_percent_matched_sideEffects.append(f"{row_i[3]}")
                p_user_reports.append(f"{row_i[4]}")

            # Probability compared to all meds with at
            # least one matched side effect
            sum_count = sum(count)
            nr_rows = len(count)
            p_med = []
            for i in range(nr_rows):
                p = count[i]/sum_count
                p_med.append("{0:0.2f}%".format(p * 100))

            # Algo for the most likely medicines in combination....
            
            # first value is uniquely highest
            if count[0] > count[1]:
                med_high_p_name = commercial_name[0]
                med_high_p_name2 = None
                med_high_p_pct = percent_matched_sideEffects[0]
                med_high_p_prop = p_med[0]
                med_high_p_user = p_user_reports[0]
                med_high_p_total = total_percent_matched_sideEffects[0]
            
            # first value = second value
            elif count[0] == count[1]:
                index = 0
                for i in count:
                    # find first value lower than max value
                    if i < count[0]:
                        index = index
                        break
                    
                    # end of list reached = all values same
                    elif index == len(count)-1:
                        break
                    
                    index = index + 1
                
                # Lookup highest value of matched side effects compared to total
                # list of side effects from specific medicine
                max_p_total = max(total_percent_matched_sideEffects[0:index])
                max_p_total_index = total_percent_matched_sideEffects[0:index].index(max_p_total)
                
                med_high_p_name = commercial_name[max_p_total_index]
                med_high_p_name2 = None
                med_high_p_pct = percent_matched_sideEffects[max_p_total_index]
                med_high_p_prop = p_med[max_p_total_index]
                med_high_p_user = p_user_reports[max_p_total_index]
                med_high_p_total = total_percent_matched_sideEffects[max_p_total_index]

                    

            # dataframes
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

                # query: calcualte nr of matched side effects per medicine combination
                query = "select left_table.med_name1, left_table.med_name2, left_table.nr_matched_se, left_table.per_matched_se, left_table.to_per_matched_se, user_reports_combo.sum_user_reports from (select cm.m0_commercial_name as med_name1, cm.m1_commercial_name as med_name2, cm.nr_matched_se as nr_matched_se, to_char((cm.nr_matched_se::float/" + str(nr_sideEffects) + ")*100, 'fm900D00%') as per_matched_se, to_char((cm.nr_matched_se::float/nr.to_nr_matched_se)*100, 'fm990D00%') as to_per_matched_se from (select m0.commercial_name as m0_commercial_name, m1.commercial_name as m1_commercial_name, count(*) as nr_matched_se from dbms.medicines m0, dbms.medicines m1, dbms.medicines_combo mc where m0.stitch = mc.stitch1 and m1.stitch = mc.stitch2 and (" + sideEffects4query + ") group by m0.commercial_name, m1.commercial_name order by count(*) desc)cm, (select m0.commercial_name as m0_commercial_name, m1.commercial_name as m1_commercial_name, count(*) as to_nr_matched_se from dbms.medicines m0, dbms.medicines m1, dbms.medicines_combo mc where m0.stitch = mc.stitch1 and m1.stitch = mc.stitch2 group by m0.commercial_name, m1.commercial_name)nr where cm.m0_commercial_name = nr.m0_commercial_name and cm.m1_commercial_name = nr.m1_commercial_name)left_table left join (select user_reports2.med_name1 as med_name1, user_reports2.med_name2 as med_name2, to_char((user_reports2.nr_reported/sum_user_reports.sum_user)* 100, 'fm900D00%') as sum_user_reports from (select sum(user_reports.nr_reported) as sum_user from (select commercial_name1 as med_name1, commercial_name2 as med_name2, count(*) as nr_reported from dbms.combo_side_effects_reported group by med_name1, med_name2)user_reports)sum_user_reports, (select commercial_name1 as med_name1, commercial_name2 as med_name2, count(*) as nr_reported from dbms.combo_side_effects_reported group by med_name1, med_name2)user_reports2)user_reports_combo on left_table.med_name1 = user_reports_combo.med_name1 and left_table.med_name2 = user_reports_combo.med_name2 order by left_table.nr_matched_se desc"
                
                # query = "select cm.m0_commercial_name, cm.m1_commercial_name, cm.nr_matched_se, to_char((cm.nr_matched_se::float/" + str(nr_sideEffects) + ")*100, 'fm900D00%') as per_matched_se, to_char((cm.nr_matched_se::float/nr.to_nr_matched_se)*100, 'fm990D00%') as to_per_matched_se from (select m0.commercial_name as m0_commercial_name, m1.commercial_name as m1_commercial_name, count(*) as nr_matched_se from dbms.medicines m0, dbms.medicines m1, dbms.medicines_combo mc where m0.stitch = mc.stitch1 and m1.stitch = mc.stitch2 and (" + sideEffects4query + ") group by m0.commercial_name, m1.commercial_name order by count(*) desc)cm, (select m0.commercial_name as m0_commercial_name, m1.commercial_name as m1_commercial_name, count(*) as to_nr_matched_se from dbms.medicines m0, dbms.medicines m1, dbms.medicines_combo mc where m0.stitch = mc.stitch1 and m1.stitch = mc.stitch2 group by m0.commercial_name, m1.commercial_name)nr where cm.m0_commercial_name = nr.m0_commercial_name and cm.m1_commercial_name = nr.m1_commercial_name order by cm.nr_matched_se desc"
                
                #query = "select m0.commercial_name, m1.commercial_name, count(*) from dbms.medicines m0, dbms.medicines m1, dbms.medicines_combo mc where m0.stitch = mc.stitch1 and m1.stitch = mc.stitch2 and (" + sideEffects4query + ") group by m0.commercial_name, m1.commercial_name order by count(*) desc;"

                db_cur.execute(query)

                query_result = db_cur.fetchall()

                #commercial_name1 = []
                #commercial_name2 = []
                #count = []
                #percent_matched_sideEffects = []
                #total_percent_matched_sideEffects = []
                #p_user_reports = []
                
                #for row_i in query_result:
                    #commercial_name1.append(f"{row_i[0]}")
                    #commercial_name2.append(f"{row_i[1]}")
                    #count.append(int(f"{row_i[2]}"))
                    #percent_matched_sideEffects.append(f"{row_i[3]}")
                    #total_percent_matched_sideEffects.append(f"{row_i[4]}")
                    #p_user_reports.append(f"{row_i[5]}")

                # Probability compared to all meds with at
                # least one matched side effect
                #sum_count = sum(count)
                #nr_rows = len(count)
                #p_med = []
                #for i in range(nr_rows):
                    #p = count[i]/sum_count
                    #p_med.append("{0:0.2f}%".format(p * 100))

                # dataframes
                #df1_definition_names = {'Commercial Name Medicine 1': commercial_name1}
                #df1 = pd.DataFrame(data=df1_definition_names)
                #df2_definition_names = {'Commercial Name Medicine 2': commercial_name2}
                #df2 = pd.DataFrame(data=df2_definition_names)
                #df3_definition_names = {'Number of side effects matched': count}
                #df3 = pd.DataFrame(data=df3_definition_names)
                #df4_definition_names = {'Nr. of side effects matched/\nnr. selected side effects': percent_matched_sideEffects}
                #df4 = pd.DataFrame(data=df4_definition_names)
                #df5_definition_names = {'Nr. of side effects matched/\nnr. reported side effects': total_percent_matched_sideEffects}
                #df5 = pd.DataFrame(data=df5_definition_names)
                #df6_definition_names = {'Probability of all meds with at least one matched side effect': p_med}
                #df6 = pd.DataFrame(data=df6_definition_names)
                #df7_definition_names = {'Probability of med based on user reports': p_user_reports}
                #df7 = pd.DataFrame(data=df7_definition_names)

                #concat_dfs = pd.concat([df1, df2, df3, df4, df6, df7, df5], ignore_index=False, axis=1)
                    
                #return concat_dfs, commercial_name, count, percent_matched_sideEffects, total_percent_matched_sideEffects, p_user_reports
            
            elif nr_sideEffects == 1:
                
                #db_cur.execute("""select m0.commercial_name, count(*) from dbms.medicines m0, dbms.medicines_combo mm where m0.stitch = mm.stitch and mm.individual_side_effect = %(side_effect)s group by m0.commercial_name order by count(*) desc;""", {'side_effect': selected_sideEffects_id[0]})
                query = "select left_table.med_name1, left_table.med_name2, left_table.nr_matched_se, left_table.per_matched_se, left_table.to_per_matched_se, user_reports_combo.sum_user_reports from (select cm.m0_commercial_name as med_name1, cm.m1_commercial_name as med_name2, cm.nr_matched_se as nr_matched_se, to_char((cm.nr_matched_se::float/" + str(nr_sideEffects) + ")*100, 'fm900D00%') as per_matched_se, to_char((cm.nr_matched_se::float/nr.to_nr_matched_se)*100, 'fm990D00%') as to_per_matched_se from (select m0.commercial_name as m0_commercial_name, m1.commercial_name as m1_commercial_name, count(*) as nr_matched_se from dbms.medicines m0, dbms.medicines m1, dbms.medicines_combo mc where m0.stitch = mc.stitch1 and m1.stitch = mc.stitch2 and mc.polypharmacy_side_effect = '" + selected_sideEffects_id[0] + "' group by m0.commercial_name, m1.commercial_name order by count(*) desc)cm, (select m0.commercial_name as m0_commercial_name, m1.commercial_name as m1_commercial_name, count(*) as to_nr_matched_se from dbms.medicines m0, dbms.medicines m1, dbms.medicines_combo mc where m0.stitch = mc.stitch1 and m1.stitch = mc.stitch2 group by m0.commercial_name, m1.commercial_name)nr where cm.m0_commercial_name = nr.m0_commercial_name and cm.m1_commercial_name = nr.m1_commercial_name)left_table left join (select user_reports2.med_name1 as med_name1, user_reports2.med_name2 as med_name2, to_char((user_reports2.nr_reported/sum_user_reports.sum_user)* 100, 'fm900D00%') as sum_user_reports from (select sum(user_reports.nr_reported) as sum_user from (select commercial_name1 as med_name1, commercial_name2 as med_name2, count(*) as nr_reported from dbms.combo_side_effects_reported group by med_name1, med_name2)user_reports)sum_user_reports, (select commercial_name1 as med_name1, commercial_name2 as med_name2, count(*) as nr_reported from dbms.combo_side_effects_reported group by med_name1, med_name2)user_reports2)user_reports_combo on left_table.med_name1 = user_reports_combo.med_name1 and left_table.med_name2 = user_reports_combo.med_name2 order by left_table.nr_matched_se desc"
                #query = "select cm.m0_commercial_name, cm.m1_commercial_name, cm.nr_matched_se, to_char((cm.nr_matched_se::float/" + str(nr_sideEffects) + ") * 100, 'fm900D00%') as per_matched_se, to_char((cm.nr_matched_se::float/nr.to_nr_matched_se) * 100, '990D00%') as to_per_matched_se from (select m0.commercial_name as m0_commercial_name, m1.commercial_name as m1_commercial_name, count(*) as nr_matched_se from dbms.medicines m0, dbms.medicines m1, dbms.medicines_combo mc where m0.stitch = mc.stitch1 and m1.stitch = mc.stitch2 and mc.polypharmacy_side_effect = '" + selected_sideEffects_id[0] + "' group by m0.commercial_name, m1.commercial_name order by count(*) desc)cm, (select m0.commercial_name as m0_commercial_name, m1.commercial_name as m1_commercial_name, count(*) as to_nr_matched_se from dbms.medicines m0, dbms.medicines m1, dbms.medicines_combo mc where m0.stitch = mc.stitch1 and m1.stitch = mc.stitch2 group by m0.commercial_name, m1.commercial_name)nr where cm.m0_commercial_name = nr.m0_commercial_name and cm.m1_commercial_name = nr.m1_commercial_name order by cm.nr_matched_se desc"

                db_cur.execute(query)

                query_result = db_cur.fetchall()

                #commercial_name1 = []
                #commercial_name2 = []
                #count = []
                #percent_matched_sideEffects = []
                #total_percent_matched_sideEffects = []
                #p_user_reports = []
                #for row_i in query_result:
                    #commercial_name1.append(f"{row_i[0]}")
                    #commercial_name2.append(f"{row_i[1]}")
                    #count.append(int(f"{row_i[2]}"))
                    #percent_matched_sideEffects.append(f"{row_i[3]}")
                    #total_percent_matched_sideEffects.append(f"{row_i[4]}")
                    #p_user_reports.append(f"{row_i[5]}")

                # Probability compared to all meds with at
                # least one matched side effect
                #sum_count = sum(count)
                #nr_rows = len(count)
                #p_med = []
                #for i in range(nr_rows):
                    #p = count[i]/sum_count
                    #p_med.append("{0:0.2f}%".format(p * 100))

                # Dataframes
                #df1_definition_names = {'Commercial Name Medicine 1': commercial_name1}
                #df1 = pd.DataFrame(data=df1_definition_names)
                #df2_definition_names = {'Commercial Name Medicine 2': commercial_name2}
                #df2 = pd.DataFrame(data=df2_definition_names)
                #df3_definition_names = {'Number of side effects matched': count}
                #df3 = pd.DataFrame(data=df3_definition_names)
                #df4_definition_names = {'Nr. of side effects matched/\nnr. selected side effects': percent_matched_sideEffects}
                #df4 = pd.DataFrame(data=df4_definition_names)
                #df5_definition_names = {'Nr. of side effects matched/\nnr. reported side effects': total_percent_matched_sideEffects}
                #df5 = pd.DataFrame(data=df5_definition_names)
                #df6_definition_names = {'Probability of all meds with at least one matched side effect': p_med}
                #df6 = pd.DataFrame(data=df6_definition_names)
                #df7_definition_names = {'Probability of med based on user reports': p_user_reports}
                #df7 = pd.DataFrame(data=df7_definition_names)

                #concat_dfs = pd.concat([df1, df2, df3, df4, df6, df7, df5], ignore_index=False, axis=1)
                    
                #return concat_dfs, commercial_name, count, percent_matched_sideEffects, total_percent_matched_sideEffects, p_user_reports


            commercial_name1 = []
            commercial_name2 = []
            count = []
            percent_matched_sideEffects = []
            total_percent_matched_sideEffects = []
            p_user_reports = []
                
            for row_i in query_result:
                commercial_name1.append(f"{row_i[0]}")
                commercial_name2.append(f"{row_i[1]}")
                count.append(int(f"{row_i[2]}"))
                percent_matched_sideEffects.append(f"{row_i[3]}")
                total_percent_matched_sideEffects.append(f"{row_i[4]}")
                p_user_reports.append(f"{row_i[5]}")

            # Probability compared to all meds with at
            # least one matched side effect
            sum_count = sum(count)
            nr_rows = len(count)
            p_med = []
            for i in range(nr_rows):
                p = count[i]/sum_count
                p_med.append("{0:0.2f}%".format(p * 100))

            # dataframes
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

            # here algo for the most likely medicines in combination....

        total_nr_meds_found = len(count)

        return concat_dfs, total_nr_meds_found, med_high_p_name, med_high_p_name2, med_high_p_pct, med_high_p_prop, med_high_p_user, med_high_p_total
        

    def create_kpi1(self, commercial_name):
        """Create value for KPI1:
        
        Nr. meds with at least one matched side effect.

        Args:
            commercial_name: list of medicines found in query
            type: list
        Returns:
            kpi1: number of medicines with >=1 matched side effects
            type: int
        """

        # KPI: nr. meds with at least one matched side effect
        kpi1 = len(commercial_name)

        return kpi1


    def create_kpi2(self, commercial_name, percent_matched_sideEffects):
        """Create value for KPI1:

        Medicine with highest percentage matched side effects.

        Args:
            percent_matched_sideEffects: list of medicines found in query
            type: list
        Returns:
            kpi2: list with name, percentage and delta to second
            type: list
        """

        # Percentage of highest value
        kpi2_perc = max(percent_matched_sideEffects)
        # Identify index of two highest percentage in list
        kpi2_perc_index = percent_matched_sideEffects.index(kpi2_perc)

        # Second highest
        perc_match_sideEffects_wo_max = percent_matched_sideEffects.copy()
        perc_match_sideEffects_wo_max.pop(kpi2_perc_index)
        
        kpi2_perc2 = max(perc_match_sideEffects_wo_max)
        kpi2_perc2_index = perc_match_sideEffects_wo_max.index(kpi2_perc2)


        # Define name of two highest med based on index
        kpi2_name = commercial_name[kpi2_perc_index]
        kpi2_name2 = commercial_name[kpi2_perc2_index]

        # delta calc.
        
        # first max
        kpi2_perc_len = len(kpi2_perc)
        kpi2_perc_float = float(kpi2_perc[:kpi2_perc_len-1:])
        
        # second max
        kpi2_perc2_len = len(kpi2_perc2)
        kpi2_perc2_float = float(kpi2_perc2[:kpi2_perc2_len-1:])
        
        kpi2_delta = str(kpi2_perc_float - kpi2_perc2_float)

        # result
        kpi2 = []
        kpi2.append(kpi2_name)
        kpi2.append(kpi2_perc)
        kpi2.append(kpi2_delta + "%")
        
        
        return kpi2


if __name__ == "__main__":
    pass