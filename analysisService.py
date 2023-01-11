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
            selected_sideEffects: list of chosen side effects
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
                query = "select cm.m0_commercial_name, cm.nr_matched_se, cm.nr_matched_se::float/6 as per_matched_se, cm.nr_matched_se::float/nr.to_nr_matched_se as to_per_matched_se from (select m0.commercial_name as m0_commercial_name, count(*) as nr_matched_se from dbms.medicines m0, dbms.medicine_mono mm where m0.stitch = mm.stitch and (" + sideEffects4query + ") group by m0.commercial_name order by count(*) desc)cm, (select m1.commercial_name as m1_commercial_name, count(*) as to_nr_matched_se from dbms.medicines m1, dbms.medicine_mono mm where m1.stitch = mm.stitch group by m1.commercial_name)nr where cm.m0_commercial_name = nr.m1_commercial_name order by per_matched_se desc"
                # old query = "select m0.commercial_name, count(*) from dbms.medicines m0, dbms.medicine_mono mm where m0.stitch = mm.stitch  and (" + sideEffects4query + ") group by m0.commercial_name order by count(*) desc;"

                db_cur.execute(query)

                query_result = db_cur.fetchall()

                commercial_name = []
                count = []
                percent_matched_sideEffects = []
                total_percent_matched_sideEffects = []

                for row_i in query_result:
                    #st.write(row_i)
                    commercial_name.append(f"{row_i[0]}")
                    count.append(f"{row_i[1]}")
                    percent_matched_sideEffects.append(f"{row_i[2]}")
                    total_percent_matched_sideEffects.append(f"{row_i[3]}")

                df1_definition_names = {'Commercial Name': commercial_name}
                df1 = pd.DataFrame(data=df1_definition_names)
                df2_definition_names = {'Number of side effects matched': count}
                df2 = pd.DataFrame(data=df2_definition_names)
                df3_definition_names = {'Portion of matched side effects: Nr. of side effects matched/nr. selected side effects': percent_matched_sideEffects}
                df3 = pd.DataFrame(data=df3_definition_names)
                df4_definition_names = {'Portion of matched side effects: Nr. of side effects matched/nr. reported side effects': total_percent_matched_sideEffects}
                df4 = pd.DataFrame(data=df4_definition_names)

                concat_dfs = pd.concat([df1, df2, df3, df4], ignore_index=False, axis=1)
                #st.write(concat_dfs)
                
                return concat_dfs

            elif nr_sideEffects == 1:
                
                db_cur.execute("""select m0.commercial_name, count(*) from dbms.medicines m0, dbms.medicine_mono mm where m0.stitch = mm.stitch and mm.individual_side_effect = %(side_effect)s group by m0.commercial_name order by count(*) desc;""", {'side_effect': selected_sideEffects_id[0]})

                query_result = db_cur.fetchall()

                commercial_name = []
                count = []
                for row_i in query_result:
                    #st.write(row_i)
                    commercial_name.append(f"{row_i[0]}")
                    count.append(f"{row_i[1]}")

                df1_definition_names = {'Commercial Name': commercial_name}
                df1 = pd.DataFrame(data=df1_definition_names)
                df2_definition_names = {'Number of side effects matched': count}
                df2 = pd.DataFrame(data=df2_definition_names)

                concat_dfs = pd.concat([df1, df2], ignore_index=False, axis=1)
                #st.write(concat_dfs)

                return concat_dfs

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
                query = "select m0.commercial_name, m1.commercial_name, count(*) from dbms.medicines m0, dbms.medicines m1, dbms.medicines_combo mc where m0.stitch = mc.stitch1 and m1.stitch = mc.stitch2 and (" + sideEffects4query + ") group by m0.commercial_name, m1.commercial_name order by count(*) desc;"
                #old query = "select m0.commercial_name, count(*) from dbms.medicines m0, dbms.medicine_mono mm where m0.stitch = mm.stitch  and (" + sideEffects4query + ") group by m0.commercial_name order by count(*) desc;"

                db_cur.execute(query)

                query_result = db_cur.fetchall()

                commercial_name1 = []
                commercial_name2 = []
                count = []
                for row_i in query_result:
                    commercial_name1.append(f"{row_i[0]}")
                    commercial_name2.append(f"{row_i[1]}")
                    count.append(f"{row_i[2]}")

                df1_definition_names = {'Commercial Name Medicine 1': commercial_name1}
                df1 = pd.DataFrame(data=df1_definition_names)
                df2_definition_names = {'Commercial Name Medicine 2': commercial_name2}
                df2 = pd.DataFrame(data=df2_definition_names)
                df3_definition_names = {'Number of side effects matched': count}
                df3 = pd.DataFrame(data=df3_definition_names)

                concat_dfs = pd.concat([df1, df2, df3], ignore_index=False, axis=1)
                #st.write(concat_dfs)
                    
                return concat_dfs
            
            elif nr_sideEffects == 1:
                
                #db_cur.execute("""select m0.commercial_name, count(*) from dbms.medicines m0, dbms.medicines_combo mm where m0.stitch = mm.stitch and mm.individual_side_effect = %(side_effect)s group by m0.commercial_name order by count(*) desc;""", {'side_effect': selected_sideEffects_id[0]})
                db_cur.execute("""select m0.commercial_name, m1.commercial_name, count(*) from dbms.medicines m0, dbms.medicines m1, dbms.medicines_combo mc where m0.stitch = mc.stitch1 and m1.stitch = mc.stitch2 and mc.polypharmacy_side_effect = %(side_effect)s group by m0.commercial_name, m1.commercial_name order by count(*) desc;""", {'side_effect': selected_sideEffects_id[0]})
                query_result = db_cur.fetchall()

                commercial_name1 = []
                commercial_name2 = []
                count = []
                for row_i in query_result:
                    commercial_name1.append(f"{row_i[0]}")
                    commercial_name2.append(f"{row_i[1]}")
                    count.append(f"{row_i[2]}")

                df1_definition_names = {'Commercial Name Medicine 1': commercial_name1}
                df1 = pd.DataFrame(data=df1_definition_names)
                df2_definition_names = {'Commercial Name Medicine 2': commercial_name2}
                df2 = pd.DataFrame(data=df2_definition_names)
                df3_definition_names = {'Number of side effects matched': count}
                df3 = pd.DataFrame(data=df3_definition_names)

                concat_dfs = pd.concat([df1, df2, df3], ignore_index=False, axis=1)
                #st.write(concat_dfs)
                    
                return concat_dfs

if __name__ == "__main__":
    pass