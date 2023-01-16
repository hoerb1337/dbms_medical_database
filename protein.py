# External libraries
import streamlit as st


# Backend modules
import analysisService

class render_tab3:
    def __init__(self):
        st.info("Analysis of drugs with shared proteins:\n" +
                "Do drugs with shared proteins have common side effects?")
    
    def show_protein_analysis(self):
        """UI for displaying results of shared protein analysis.

        Args:
            selected_sideEffects:
            type: list
            nr_sideEffects:
            type: int
        Returns:
            selected_sideEffects: list of chosen side effects
            type: dataframe
        """

        st.subheader("Procedure of Analysis")
        proc_descr = """
                    The basic idea is to check whether (1) at least one side effect occuring with drugs that share a protein, (2) are listed with all drugs that share the protein. The analysis excluded proteins that are targeted only from one drug.<br>In more detail, the analysis proceeded as follows:<br>
                    (1):
                    <ul>
                    <li>For each protein, find the side effects of drugs that share the protein.</li>
                    <li>Calculate the number of occurence of same side effects for each protein.</li>
                    </ul>
                    <br>
                    (2):
                    <br>
                    <ul>
                    <li>Find proteins with their shared drugs.</li>
                    <li>For each protein, calculate the total number of drugs that share the protein.</li>
                    </ul>
                    <br>
                    Connect results from (1) and (2):
                    <ul>
                    <li>Join the tables from (1) and (2) on the proteins.</li>
                    <li>For each protein, calculate the ratio of side effects to the number of drugs that share the protein.</li>
                    </ul>
                    <ul>
                    Make general statement with an average:
                    <li>Calculate the average ratio from step 6 over all proteins and side effects.</li>
                    </ul>
                    """
        #st.write(proc_descr)
        st.markdown(proc_descr, unsafe_allow_html=True)
        #st.subheader("Result of Analysis: No")
        #protein_data = analysisService.data4Analysis()
        #avg_ratio_se_meds = protein_data.lookup_avg_ratio_se_meds()
        #result = "No, drugs with shared proteins do not - on average - have common side effects. On average only " + avg_ratio_se_meds + " of side effects are common in drugs with shared proteins."
        
        #st.write(result)



        query = """
/* Calculate avg. ratio from side effects common in meds with a shared protein */
select to_char((avg(full_table.ratio_common_se))*100, 'fm900D00%') as avg_ratio_common_se
from

/* Calculate the ratio from side effects common in meds with a shared protein */
(select gene_sideeffects.gene1 as gene, gene_sideeffects.se as side_effect,
gene_sideeffects.nr_shared_se as nr_common_se, shared_meds.nr_shared_meds as nr_shared_meds,
gene_sideeffects.nr_shared_se::float/shared_meds.nr_shared_meds as ratio_common_se,
to_char((gene_sideeffects.nr_shared_se::float/shared_meds.nr_shared_meds)*100, 'fm900D00%') as per_ratio_common_se

from
/* Table 1 with proteins with side effects from shared meds */
(select mp1.gene as gene1, mm.individual_side_effect as se, count(*) as nr_shared_se
from dbms.medicine_protein mp1, dbms.medicine_mono mm
where mp1.stitch = mm.stitch
group by mp1.gene, mm.individual_side_effect)gene_sideeffects,

/* Table 2 with proteins with their shared meds */
(select mp.gene as gene2, count(*) as nr_shared_meds
from dbms.medicine_protein mp
group by gene)shared_meds

/* Join Table 1 with Table 2 on the protein and exclude proteins that are targeted
   only in one medicine */
where gene_sideeffects.gene1 = shared_meds.gene2
and shared_meds.nr_shared_meds > 1)full_table
                """
       
        st.code(query, language="sql")
        


        return None


if __name__ == "__main__":
    pass