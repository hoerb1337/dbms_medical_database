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

        st.subheader("Result of Analysis: No")
        protein_data = analysisService.data4Analysis()
        avg_ratio_se_meds = protein_data.lookup_avg_ratio_se_meds()
        result = "No, drugs with shared proteins do not - on average - have common side effects. On average only " + avg_ratio_se_meds + " of side effects are common in drugs with shared proteins."
        
        st.write(result)



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
       
        st.markdown("<br>", unsafe_allow_html=True)
        st.code(query, language="sql")
        


        return None


if __name__ == "__main__":
    pass