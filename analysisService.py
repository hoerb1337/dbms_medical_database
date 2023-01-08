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
        if combo == "True":
            db_cur.execute("select distinct mc.combo_side_effect_name " + 
                           "from dbms.medicines m0, dbms.medicines m1, dbms.medicines_combo mc " + 
                           "where m0.stitch = mc.stitch1 and m1.stitch = mc.stitch2;")
            list_sideEffects = []
            for sideEffect_i in db_cur:
                list_sideEffects.append(f"{sideEffect_i[0]}")
        else:
            db_cur.execute("select distinct mm.individual_side_effect_name " +
                           "from dbms.medicines m0, dbms.medicine_mono mm " +
                           "where m0.stitch = mm.stitch;")
            list_sideEffects = []
            for sideEffect_i in db_cur:
                list_sideEffects.append(f"{sideEffect_i[0]}")
        
        # Close connection
        close_db_connection = db.disconnect_postgres(db_connection, db_cur)

        return list_sideEffects

    
    def do_reverse_lookup(self, selected_sideEffects, nr_sideEffects, combo):
        """Perform reverse lookup analysis.

        Args:
            selected_sideEffects:
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

        st.write(nr_sideEffects)
        st.write(selected_sideEffects)

        if combo == "False":
            if nr_sideEffects > 1:

                # Create input for execution
                sideEffects4query = "" 
                
                i = 0
                for sideEffect_i in range(nr_sideEffects):
                    if sideEffect_i == nr_sideEffects - 1:
                        sideEffects4query = sideEffects4query + "mm.individual_side_effect_name = " + "'" + selected_sideEffects[i] + "' "
                    elif sideEffect_i == 0:
                        sideEffects4query = sideEffects4query + "mm.individual_side_effect_name = '" + selected_sideEffects[i] + "' or "
                        i += 1
                    else:
                        sideEffects4query = sideEffects4query + " mm.individual_side_effect_name = " + "'" + selected_sideEffects[i] + "' or "
                        i += 1

                query = "select m0.commercial_name, count(*) from dbms.medicines m0, dbms.medicine_mono mm where m0.stitch = mm.stitch  and (" + sideEffects4query + ") group by m0.commercial_name order by count(*) desc;"

                db_cur.execute(query)

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
                st.write(concat_dfs)
                
                return concat_dfs

            elif nr_sideEffects == 1:
                
                db_cur.execute("""select m0.commercial_name, count(*) from dbms.medicines m0, dbms.medicine_mono mm where m0.stitch = mm.stitch and mm.individual_side_effect_name = %(side_effect)s group by m0.commercial_name order by count(*) desc;""", {'side_effect': selected_sideEffects[0]})

                query_result = db_cur.fetchall()

                commercial_name = []
                count = []
                for row_i in query_result:
                    #st.write(row_i)
                    commercial_name.append(f"{row_i[0]}")
                    count.append(f"{row_i[1]}")

                df1_definition_names = {'commercial_name': commercial_name}
                df1 = pd.DataFrame(data=df1_definition_names)
                df2_definition_names = {'count': count}
                df2 = pd.DataFrame(data=df2_definition_names)

                concat_dfs = pd.concat([df1, df2], ignore_index=False, axis=1)
                st.write(concat_dfs)

                return concat_dfs

if __name__ == "__main__":
    pass